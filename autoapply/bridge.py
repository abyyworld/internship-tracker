from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
import os
from pathlib import Path
import re
import secrets
from typing import Any
from urllib.parse import parse_qs, urlparse

from .config import (
    academic_path,
    database_path,
    facts_path,
    load_yaml,
    profile_path,
    reject_placeholders,
)
from .cv_editor import (
    load_draft,
    master_document,
    resume_from_document,
    save_draft,
)
from .editor_ui import EDITOR_PAGE
from .jobs import jobs_from_tracker
from .openai_tailoring import (
    generate_suggestions,
    load_openai_key,
    openai_key_configured,
    save_openai_key,
)
from .resume import render_resume
from .runner import prepare
from .store import Store


MAX_REQUEST_BYTES = 262144
DOWNLOAD_TTL = timedelta(minutes=5)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(".-")
    return (cleaned[:100] or "tailored-resume") + ".pdf"


def _application_url(job: Any) -> str:
    url = job.url.rstrip("/")
    if job.ats == "ashby" and not url.endswith("/application"):
        return f"{url}/application"
    if job.ats == "lever" and not url.endswith("/apply"):
        return f"{url}/apply"
    return job.url


def bridge_token_path(home: Path) -> Path:
    return home / "bridge.token"


def load_or_create_bridge_token(home: Path) -> str:
    path = bridge_token_path(home)
    if path.exists():
        if path.is_symlink():
            raise RuntimeError("Refusing a symbolic-link bridge token")
        if path.stat().st_mode & 0o077:
            raise RuntimeError("Bridge token file must have mode 0600")
        token = path.read_text(encoding="utf-8").strip()
        if len(token) < 32:
            raise RuntimeError("Bridge token is missing or too short")
        return token
    token = secrets.token_urlsafe(32)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = -1
            handle.write(token + "\n")
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    path.chmod(0o600)
    return token


@dataclass
class Download:
    path: Path
    filename: str
    expires_at: datetime


class BridgeServer(ThreadingHTTPServer):
    """Serve each request on its own thread.

    Generating suggestions fetches the live job page and then waits on the
    OpenAI API, which can take a minute. On a single-threaded server that
    blocks every other request, so opening another job or checking the local
    connection appears to hang until generation finishes.
    """

    daemon_threads = True

    def __init__(
        self,
        address: tuple[str, int],
        *,
        home: Path,
        tracker: Path,
        token: str,
    ) -> None:
        super().__init__(address, BridgeHandler)
        self.home = home.resolve()
        self.tracker = tracker.resolve()
        self.token = token
        self.downloads: dict[str, Download] = {}
        self._tracker_mtime = self._current_tracker_mtime()

    def _current_tracker_mtime(self) -> float:
        try:
            return self.tracker.stat().st_mtime
        except OSError:
            return 0.0

    def refresh_jobs_if_tracker_changed(self) -> bool:
        """Re-import the tracker when it has changed on disk.

        The bridge normally runs as a long-lived background service while the
        daily watcher rewrites tracker.csv underneath it. Without this the
        database keeps only the jobs that existed at start-up, so every newly
        discovered posting fails to open in the editor until a manual restart.
        """
        mtime = self._current_tracker_mtime()
        if mtime and mtime == self._tracker_mtime:
            return False
        self._tracker_mtime = mtime
        try:
            with Store(database_path(self.home)) as store:
                store.import_jobs(
                    jobs_from_tracker(self.tracker, include_unknown=True)
                )
        except (OSError, ValueError, RuntimeError):
            return False
        return True

    def new_download(self, path: Path, filename: str) -> str:
        ticket = secrets.token_urlsafe(32)
        self.downloads[ticket] = Download(
            path=path.resolve(),
            filename=filename,
            expires_at=_now() + DOWNLOAD_TTL,
        )
        return ticket

    def take_download(self, ticket: str) -> Download | None:
        for key, value in list(self.downloads.items()):
            if value.expires_at <= _now():
                self.downloads.pop(key, None)
        value = self.downloads.pop(ticket, None)
        if value is None or value.expires_at <= _now():
            return None
        generated = (self.home / "generated").resolve()
        if not value.path.is_relative_to(generated):
            return None
        return value


class BridgeHandler(BaseHTTPRequestHandler):
    server: BridgeServer

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def _json(self, status: int, value: dict[str, Any]) -> None:
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _html(self, status: int, value: str) -> None:
        body = value.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; style-src 'unsafe-inline'; "
            "script-src 'unsafe-inline'; connect-src 'self'",
        )
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self) -> bool:
        supplied = self.headers.get("X-Autoapply-Token", "")
        return bool(supplied) and secrets.compare_digest(supplied, self.server.token)

    def _payload(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_REQUEST_BYTES:
            raise ValueError("Invalid request size")
        try:
            value = json.loads(self.rfile.read(length))
        except json.JSONDecodeError as exc:
            raise ValueError("Expected a JSON request") from exc
        if not isinstance(value, dict):
            raise ValueError("Expected a JSON object")
        return value

    @staticmethod
    def _job_url(value: Any) -> str:
        url = str(value or "").strip()
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.hostname or len(url) > 2048:
            raise ValueError("Only absolute HTTPS job URLs are accepted")
        return url

    def _find_job(self, url: str):
        """Look up a job, re-importing the tracker once if it is not known yet.

        A posting discovered by a watcher run after this process started is not
        in the database, so the first lookup misses. Re-import and retry before
        telling the user the link is not tracked.
        """
        with Store(database_path(self.server.home)) as store:
            try:
                return store.find_job_by_url(url)
            except (KeyError, ValueError):
                pass
        self.server.refresh_jobs_if_tracker_changed()
        with Store(database_path(self.server.home)) as store:
            return store.find_job_by_url(url)

    def _document(self) -> tuple[dict[str, Any], dict[str, Any]]:
        profile = load_yaml(profile_path(self.server.home))
        facts = load_yaml(facts_path(self.server.home))
        reject_placeholders(profile)
        reject_placeholders(facts)
        # Academic profile is optional — load if present, skip silently otherwise
        academic: dict[str, Any] | None = None
        ap = academic_path(self.server.home)
        if ap.exists():
            try:
                academic = load_yaml(ap)
            except Exception:
                academic = None
        return master_document(profile, facts, academic), profile

    def do_GET(self) -> None:
        parsed_request = urlparse(self.path)
        if parsed_request.path == "/health":
            if not self._authorized():
                self._json(401, {"error": "Bridge token required"})
                return
            self._json(200, {"ok": True, "service": "autoapply-cv-bridge"})
            return
        if parsed_request.path == "/connect":
            self._html(200, CONNECT_PAGE)
            return
        if parsed_request.path == "/editor":
            query = parse_qs(parsed_request.query)
            try:
                self._job_url(query.get("url", [""])[0])
            except ValueError as exc:
                self._html(
                    400,
                    LOCAL_PAGE_ERROR.replace("__ERROR__", str(exc)),
                )
                return
            self._html(200, EDITOR_PAGE)
            return
        if parsed_request.path == "/api/editor":
            if not self._authorized():
                self._json(401, {"error": "Bridge token required"})
                return
            try:
                query = parse_qs(parsed_request.query)
                url = self._job_url(query.get("url", [""])[0])
                job = self._find_job(url)
                document, _profile = self._document()
                draft = load_draft(self.server.home, job.id)
                self._json(
                    200,
                    {
                        "ok": True,
                        "job": {
                            "id": job.id,
                            "company": job.company,
                            "role": job.role,
                            "location": job.location,
                            "description": bool(job.description.strip()),
                            "application_url": _application_url(job),
                        },
                        "document": document,
                        "draft": draft,
                        "ai_configured": openai_key_configured(
                            self.server.home
                        ),
                    },
                )
            except (FileNotFoundError, KeyError, OSError, RuntimeError, ValueError) as exc:
                self._json(422, {"error": str(exc)})
            return
        if parsed_request.path == "/tailor":
            query = parse_qs(parsed_request.query)
            url = str(query.get("url", [""])[0]).strip()
            parsed_job = urlparse(url)
            if (
                len(url) > 2048
                or parsed_job.scheme != "https"
                or not parsed_job.hostname
            ):
                self._html(400, LOCAL_PAGE_ERROR.replace("__ERROR__", "Invalid job URL"))
                return
            encoded_url = (
                json.dumps(url, ensure_ascii=True)
                .replace("<", "\\u003c")
                .replace(">", "\\u003e")
                .replace("&", "\\u0026")
            )
            self._html(200, TAILOR_PAGE.replace("__JOB_URL__", encoded_url))
            return
        if parsed_request.path.startswith("/resume/"):
            ticket = parsed_request.path.removeprefix("/resume/")
            if not re.fullmatch(r"[A-Za-z0-9_-]{32,}", ticket):
                self._json(404, {"error": "Download not found"})
                return
            download = self.server.take_download(ticket)
            if download is None or not download.path.is_file():
                self._json(404, {"error": "Download expired or already used"})
                return
            body = download.path.read_bytes()
            self.send_response(200)
            self.send_header(
                "Content-Type",
                mimetypes.guess_type(download.filename)[0] or "application/pdf",
            )
            self.send_header(
                "Content-Disposition",
                f'attachment; filename="{download.filename}"',
            )
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)
            return
        self._json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        parsed_request = urlparse(self.path)
        if parsed_request.path not in {
            "/prepare",
            "/api/settings/openai",
            "/api/suggest",
            "/api/draft",
            "/api/export",
        }:
            self._json(404, {"error": "Not found"})
            return
        if not self._authorized():
            self._json(401, {"error": "Bridge token required"})
            return
        try:
            payload = self._payload()
        except ValueError as exc:
            self._json(400, {"error": str(exc)})
            return

        if parsed_request.path == "/api/settings/openai":
            try:
                save_openai_key(
                    self.server.home,
                    str(payload.get("api_key", "")),
                )
                self._json(200, {"ok": True, "configured": True})
            except (OSError, RuntimeError, ValueError) as exc:
                self._json(422, {"error": str(exc)})
            return

        try:
            url = self._job_url(payload.get("url"))
            job = self._find_job(url)

            if parsed_request.path == "/api/suggest":
                # Fetch at generation time so opening the editor is instant and
                # no API credit is used before the user asks for suggestions.
                # The database is deliberately not held open across the network
                # fetch or the model call: both are slow, and another request
                # thread would block on the SQLite write lock behind them.
                from .runner import _fetch_resume_description

                description, _source = _fetch_resume_description(job)
                if description != job.description:
                    with Store(database_path(self.server.home)) as store:
                        store.update_description(job.id, description)
                    job.description = description
                document, _profile = self._document()
                instructions = str(payload.get("instructions", ""))[:4000]
                generated = generate_suggestions(
                    job,
                    document,
                    api_key=load_openai_key(self.server.home),
                    instructions=instructions,
                )
                saved = save_draft(
                    self.server.home,
                    document,
                    job.id,
                    generated,
                    existing=generated,
                )
                self._json(200, {"ok": True, "draft": saved})
                return

            with Store(database_path(self.server.home)) as store:
                if parsed_request.path == "/api/draft":
                    document, _profile = self._document()
                    incoming = payload.get("draft")
                    if not isinstance(incoming, dict):
                        raise ValueError("Expected a CV draft object")
                    existing = load_draft(self.server.home, job.id)
                    saved = save_draft(
                        self.server.home,
                        document,
                        job.id,
                        incoming,
                        existing=existing,
                    )
                    self._json(200, {"ok": True, "draft": saved})
                    return

                if parsed_request.path == "/api/export":
                    document, _profile = self._document()
                    draft = load_draft(self.server.home, job.id)
                    resume = resume_from_document(document, draft)
                    output = (
                        self.server.home
                        / "generated"
                        / _safe_filename(job.id).removesuffix(".pdf")
                        / "full-tailored-resume.pdf"
                    )
                    resume_hash = render_resume(resume, output)
                    ticket = self.server.new_download(
                        output,
                        _safe_filename(f"{job.company}-{job.role}"),
                    )
                    host, port = self.server.server_address
                    self._json(
                        200,
                        {
                            "ok": True,
                            "resume_sha256": resume_hash,
                            "resume_download_url": (
                                f"http://{host}:{port}/resume/{ticket}"
                            ),
                            "accepted_patch_count": len(
                                resume.selection_audit["accepted_patch_ids"]
                            )
                            + int(
                                resume.selection_audit[
                                    "summary_patch_accepted"
                                ]
                            ),
                            "master_fact_count": len(resume.selected_fact_ids),
                            "application_url": _application_url(job),
                        },
                    )
                    return

                result = prepare(
                    store, self.server.home, job.id, resume_only=True
                )
                refreshed = store.get_job(job.id)
            resume_path = Path(result["resume_path"]).resolve()
            ticket = self.server.new_download(
                resume_path,
                _safe_filename(f"{refreshed.company}-{refreshed.role}"),
            )
            host, port = self.server.server_address
            self._json(
                200,
                {
                    "ok": True,
                    "job_id": refreshed.id,
                    "company": refreshed.company,
                    "role": refreshed.role,
                    "application_url": _application_url(refreshed),
                    "resume_sha256": result["resume_hash"],
                    "selected_fact_ids": result["selected_fact_ids"],
                    "tailoring": result.get("tailoring", {}),
                    "description_source": result.get("description_source", ""),
                    "resume_download_url": f"http://{host}:{port}/resume/{ticket}",
                    "download_expires_seconds": int(DOWNLOAD_TTL.total_seconds()),
                    "note": (
                        "A role-specific CV was generated from verified facts. "
                        "Review it before selecting it in the employer form."
                    ),
                },
            )
        except (
            FileNotFoundError,
            KeyError,
            OSError,
            RuntimeError,
            ValueError,
        ) as exc:
            self._json(422, {"error": str(exc)})


def run_bridge(home: Path, tracker: Path, port: int) -> None:
    if not 1024 <= port <= 65535:
        raise ValueError("Bridge port must be between 1024 and 65535")
    token = load_or_create_bridge_token(home)
    with Store(database_path(home)) as store:
        imported = store.import_jobs(
            jobs_from_tracker(tracker, include_unknown=True)
        )
    server = BridgeServer(
        ("127.0.0.1", port),
        home=home,
        tracker=tracker,
        token=token,
    )
    print("")
    print("Autoapply CV bridge is ready")
    print(f"  address : http://127.0.0.1:{port}")
    print(f"  jobs    : {imported}")
    print(f"  token   : {token}")
    print("")
    print("Paste the token once into the GitHub CV + Apply userscript.")
    print("Keep this terminal open. Press Ctrl-C to stop.")
    print("")
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


PAGE_STYLE = """
:root{color-scheme:dark;--bg:#07110f;--panel:#10211c;--line:#315346;
--text:#f1f8f5;--muted:#a6b9b2;--green:#70efad;--green2:#25b875;--red:#ff8b82}
*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;
background:radial-gradient(circle at top,#174b3766,transparent 34rem),var(--bg);
color:var(--text);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{width:min(580px,calc(100% - 30px));background:linear-gradient(150deg,#13271f,#0c1714);
border:1px solid var(--line);border-radius:20px;padding:28px;box-shadow:0 24px 70px #0009}
.eyebrow{color:var(--green);font-size:11px;font-weight:900;letter-spacing:.14em;text-transform:uppercase}
h1{margin:8px 0 9px;font-size:34px;line-height:1.05;letter-spacing:-.04em}
p{color:var(--muted)}.progress{height:7px;background:#1b332a;border-radius:99px;overflow:hidden;margin:22px 0}
.progress i{display:block;width:35%;height:100%;background:var(--green2);border-radius:99px;
animation:move 1.2s ease-in-out infinite alternate}@keyframes move{to{transform:translateX(185%)}}
.ok{color:var(--green)}.error{color:var(--red)}button,a{display:inline-flex;align-items:center;
justify-content:center;min-height:42px;padding:0 15px;border-radius:10px;border:1px solid var(--line);
background:var(--green2);color:#03130c;text-decoration:none;font-weight:800;cursor:pointer}
.secondary{background:transparent;color:var(--text)}.actions{display:flex;gap:9px;margin-top:18px;flex-wrap:wrap}
code{word-break:break-word;color:#cce8dc}
"""


CONNECT_PAGE = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Connect local CV helper</title><style>{PAGE_STYLE}</style></head>
<body><main><div class="eyebrow">Private local helper</div>
<h1 id="title">Connecting…</h1><p id="message">The token stays in this browser on
127.0.0.1 and is never sent to GitHub.</p><div class="actions">
<a class="secondary" href="https://abyyworld.github.io/internship-tracker/">Open dashboard</a>
</div></main><script>
const fragmentToken=decodeURIComponent(location.hash.slice(1));
const token=fragmentToken||localStorage.getItem("autoapply_bridge_token_v1")||"";
if(token.length>=32){{
  if(fragmentToken) localStorage.setItem("autoapply_bridge_token_v1",token);
  history.replaceState(null,"","/connect");
  document.getElementById("title").textContent="Connected ✓";
  document.getElementById("title").className="ok";
  document.getElementById("message").textContent=
    "Every dashboard job can now generate and download a private tailored CV. Opening Role Radar…";
  setTimeout(()=>location.replace("https://abyyworld.github.io/internship-tracker/"),900);
}}else{{
  document.getElementById("title").textContent="Token missing";
  document.getElementById("title").className="error";
  document.getElementById("message").textContent=
    "Open start-autoapply.command again to connect this browser.";
}}
</script></body></html>"""


TAILOR_PAGE = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Generating tailored CV</title><style>{PAGE_STYLE}</style></head>
<body><main><div class="eyebrow">Local Qwen CV editor</div>
<h1 id="title">Reading the role…</h1>
<p id="message">Selecting verified evidence and rewriting the strongest bullets.
This normally takes 15–30 seconds.</p><div class="progress" id="progress"><i></i></div>
<div class="actions" id="actions"></div></main><script>
const jobUrl=__JOB_URL__;
const token=localStorage.getItem("autoapply_bridge_token_v1")||"";
const title=document.getElementById("title");
const message=document.getElementById("message");
const actions=document.getElementById("actions");
const progress=document.getElementById("progress");
function fail(value){{
  title.textContent="CV generation stopped";
  title.className="error";message.textContent=value;progress.hidden=true;
  actions.innerHTML='<a class="secondary" href="https://abyyworld.github.io/internship-tracker/">Back to dashboard</a>';
}}
async function run(){{
  if(token.length<32){{fail("Local browser connection is missing. Open start-autoapply.command once, then retry.");return}}
  try{{
    const response=await fetch("/prepare",{{method:"POST",headers:{{
      "Content-Type":"application/json","X-Autoapply-Token":token
    }},body:JSON.stringify({{url:jobUrl}})}});
    const result=await response.json();
    if(!response.ok)throw new Error(result.error||`Bridge returned ${{response.status}}`);
    title.textContent="Tailored CV ready ✓";title.className="ok";progress.hidden=true;
    const source=result.description_source==="public-tracker-metadata-fallback"
      ?" The employer blocked live text, so public tracker metadata was used."
      :" Live job-page text was used.";
    message.textContent=`Downloaded ${{result.company}} CV.${{source}} Opening the application for Simplify…`;
    const download=document.createElement("a");download.href=result.resume_download_url;
    download.download="";document.body.appendChild(download);download.click();download.remove();
    actions.innerHTML=`<a class="secondary" href="${{result.resume_download_url}}">Download again</a>`;
    setTimeout(()=>location.replace(result.application_url),1800);
  }}catch(error){{fail(error.message||String(error))}}
}}
run();
</script></body></html>"""


LOCAL_PAGE_ERROR = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Local CV helper</title><style>{PAGE_STYLE}</style></head><body><main>
<div class="eyebrow">Private local helper</div><h1 class="error">Cannot continue</h1>
<p>__ERROR__</p></main></body></html>"""
