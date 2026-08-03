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
from urllib.parse import parse_qs, quote, urlparse

from .config import (
    academic_path,
    database_path,
    facts_path,
    load_yaml,
    profile_path,
    reject_placeholders,
)
from .cv_editor import (
    TAILORING_MODES,
    facts_from_document,
    load_draft,
    master_document,
    rename_drafts,
    resume_from_document,
    save_draft,
)
from .cv_library import (
    MASTER_CV_ID,
    delete_cv,
    library_directory,
    list_cvs,
    load_cv,
    rename_cv,
    safe_cv_id,
    save_cv,
)
from .editor_ui import EDITOR_PAGE
from .fit import assess_all, read_postings
from .jobs import jobs_from_tracker
from .openai_tailoring import (
    OPENAI_MODEL_DEFAULT,
    available_models,
    find_questions,
    load_model,
    save_model,
    generate_suggestions,
    load_openai_key,
    openai_key_configured,
    save_openai_key,
    write_answers,
)
from .resume import render_resume
from .runner import prepare
from .store import Store


MAX_REQUEST_BYTES = 262144
DOWNLOAD_TTL = timedelta(minutes=5)

# The published dashboard is a different origin from this loopback server, so
# reading fit verdicts from it needs an explicit grant. Exactly one origin is
# allowed and only for the read-only verdict route: everything else on this
# server stays same-origin, and every route still requires the bridge token.
DASHBOARD_ORIGINS = ("https://abyyworld.github.io",)


def _allowed_origin(value: str) -> str:
    origin = str(value or "").strip()
    return origin if origin in DASHBOARD_ORIGINS else ""


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(".-")
    return (cleaned[:100] or "tailored-resume") + ".pdf"


def _download_name(person: str, job: Any) -> str:
    """Name a downloaded CV after the job it was tailored for.

    The Downloads folder fills up with one PDF per application, so the company
    and role have to be readable in the filename without opening anything.
    """
    parts = [
        part
        for part in (
            str(person or "").strip(),
            str(getattr(job, "company", "")).strip(),
            str(getattr(job, "role", "")).strip(),
        )
        if part
    ]
    name = " - ".join(parts) + " - CV"
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]+', " ", name)
    return re.sub(r"\s+", " ", name).strip()[:150] + ".pdf"


def _suggested_cv_name(job: Any) -> str:
    """A default name for saving this tailoring as its own CV."""
    company = str(getattr(job, "company", "")).strip()
    role = str(getattr(job, "role", "")).strip()
    name = " - ".join(part for part in (company, role) if part)
    return re.sub(r"\s+", " ", name).strip()[:80]


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

    def _cors(self) -> None:
        origin = _allowed_origin(self.headers.get("Origin", ""))
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")

    def do_OPTIONS(self) -> None:
        # Preflight for the dashboard's verdict fetch, which carries the token
        # header. Only that one route is offered.
        if urlparse(self.path).path != "/api/fit" or not _allowed_origin(
            self.headers.get("Origin", "")
        ):
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self.send_response(204)
        self._cors()
        self.send_header("Access-Control-Allow-Headers", "X-Autoapply-Token")
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Access-Control-Max-Age", "600")
        # A public page reaching a loopback address is a private-network
        # request, which Chrome refuses unless the preflight grants it.
        if self.headers.get("Access-Control-Request-Private-Network") == "true":
            self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _json(self, status: int, value: dict[str, Any]) -> None:
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
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

    def _models(self) -> list[str]:
        """What this account can actually run, so the picker is never a guess."""
        try:
            return available_models(load_openai_key(self.server.home))[:12]
        except (FileNotFoundError, RuntimeError):
            return []

    def _person_name(self) -> str:
        try:
            identity = load_yaml(profile_path(self.server.home)).get("identity", {})
        except (OSError, ValueError):
            return ""
        return " ".join(
            str(identity.get(key, "")).strip()
            for key in ("first_name", "last_name")
        ).strip()

    def _document(
        self,
        cv_id: str = MASTER_CV_ID,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        profile = load_yaml(profile_path(self.server.home))
        if cv_id and cv_id != MASTER_CV_ID:
            facts = load_cv(self.server.home, cv_id)
        else:
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
                cv_id = safe_cv_id(query.get("cv", [""])[0]) or MASTER_CV_ID
                job = self._find_job(url)
                document, _profile = self._document(cv_id)
                draft = load_draft(self.server.home, job.id, cv_id)
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
                        "cv_id": cv_id,
                        "cvs": list_cvs(self.server.home),
                        "cv_storage": str(library_directory(self.server.home)),
                        # Pre-fills the "save as" box so the CV is named after
                        # the job by default; the user edits it before saving.
                        "suggested_cv_name": _suggested_cv_name(job),
                        "ai_configured": openai_key_configured(
                            self.server.home
                        ),
                        "model": load_model(self.server.home),
                        "models": self._models(),
                    },
                )
            except (FileNotFoundError, KeyError, OSError, RuntimeError, ValueError) as exc:
                self._json(422, {"error": str(exc)})
            return
        if parsed_request.path == "/dashboard":
            # The published page is public and carries no personal verdicts.
            # Served from here it is same-origin with the API, so the fit
            # judgements load without a cross-origin grant — which Chrome now
            # gates behind a permission prompt for loopback addresses anyway.
            page = Path(__file__).resolve().parent.parent / "docs" / "index.html"
            if not page.is_file():
                self._html(404, LOCAL_PAGE_ERROR.replace(
                    "__ERROR__",
                    "docs/index.html has not been built yet. Run python3 dashboard.py.",
                ))
                return
            self._html(200, page.read_text(encoding="utf-8"))
            return
        if parsed_request.path == "/api/fit":
            # Verdicts live here, never in docs/index.html: the public page must
            # not carry anybody's visa status or graduation date.
            if not self._authorized():
                self._json(401, {"error": "Bridge token required"})
                return
            try:
                profile = load_yaml(profile_path(self.server.home))
                # Straight from the tracker rather than the database: this is a
                # read of the current listing, and it must not wait behind a
                # generation holding the SQLite write lock.
                jobs = read_postings(self.server.tracker)
                verdicts = assess_all(jobs, profile, today_year=_now().year)
                self._json(
                    200,
                    {
                        "ok": True,
                        "fit": {job.url: verdicts[job.id] for job in jobs},
                        "counts": {
                            status: sum(
                                1 for value in verdicts.values()
                                if value["status"] == status
                            )
                            for status in ("apply", "sponsor", "check", "mismatch")
                        },
                    },
                )
            except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
                self._json(422, {"error": str(exc)})
            return
        if parsed_request.path == "/api/cvs":
            if not self._authorized():
                self._json(401, {"error": "Bridge token required"})
                return
            try:
                self._json(200, {"ok": True, "cvs": list_cvs(self.server.home)})
            except (OSError, RuntimeError, ValueError) as exc:
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
            ascii_name = (
                download.filename.encode("ascii", "replace")
                .decode("ascii")
                .replace('"', "")
            )
            self.send_header(
                "Content-Disposition",
                f'attachment; filename="{ascii_name}"; '
                f"filename*=UTF-8''{quote(download.filename)}",
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
            "/api/settings/model",
            "/api/suggest",
            "/api/answers",
            "/api/draft",
            "/api/export",
            "/api/cv/save",
            "/api/cv/delete",
            "/api/cv/rename",
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

        if parsed_request.path == "/api/settings/model":
            try:
                chosen = save_model(self.server.home, payload.get("model", ""))
                self._json(200, {"ok": True, "model": chosen})
            except (OSError, RuntimeError, ValueError) as exc:
                self._json(422, {"error": str(exc)})
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

        # Managing the CV library is independent of any job posting.
        if parsed_request.path in {"/api/cv/delete", "/api/cv/rename"}:
            try:
                if parsed_request.path == "/api/cv/delete":
                    delete_cv(self.server.home, payload.get("target", ""))
                    self._json(
                        200, {"ok": True, "cvs": list_cvs(self.server.home)}
                    )
                    return
                info = rename_cv(
                    self.server.home,
                    payload.get("target", ""),
                    payload.get("label", ""),
                )
                rename_drafts(
                    self.server.home, info.get("previous_id", ""), info["id"]
                )
                self._json(
                    200,
                    {"ok": True, "cv": info, "cvs": list_cvs(self.server.home)},
                )
            except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
                self._json(422, {"error": str(exc)})
            return

        try:
            url = self._job_url(payload.get("url"))
            cv_id = safe_cv_id(payload.get("cv_id", "")) or MASTER_CV_ID
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
                document, _profile = self._document(cv_id)
                instructions = str(payload.get("instructions", ""))[:4000]
                mode = str(payload.get("mode", "") or "full")
                if mode not in TAILORING_MODES:
                    raise ValueError("Unknown tailoring mode")
                generated = generate_suggestions(
                    job,
                    document,
                    api_key=load_openai_key(self.server.home),
                    instructions=instructions,
                    mode=mode,
                    model=load_model(self.server.home),
                )
                generated["cv_id"] = cv_id
                saved = save_draft(
                    self.server.home,
                    document,
                    job.id,
                    generated,
                    existing=generated,
                )
                self._json(200, {"ok": True, "draft": saved})
                return

            if parsed_request.path == "/api/answers":
                # Questions come from the advert, so the description must be
                # live here for the same reason it must be for a rewrite.
                from .runner import _fetch_resume_description

                description, _source = _fetch_resume_description(job)
                if description != job.description:
                    with Store(database_path(self.server.home)) as store:
                        store.update_description(job.id, description)
                    job.description = description
                document, _profile = self._document(cv_id)
                draft = load_draft(self.server.home, job.id, cv_id)
                key = load_openai_key(self.server.home)
                questions = [
                    question
                    for question in (draft.get("questions") or [])
                    if str(question.get("question", "")).strip()
                ]
                if not questions:
                    questions = find_questions(
                        job, api_key=key, model=load_model(self.server.home)
                    )
                extra = str(payload.get("question", "")).strip()
                if extra:
                    questions = questions + [{
                        "id": f"q{len(questions)}",
                        "question": extra[:800],
                        "answer": "",
                        "word_limit": 0,
                        "source": "custom",
                    }]
                written = write_answers(
                    job, document, draft, questions,
                    api_key=key,
                    model=load_model(self.server.home),
                    instructions=str(payload.get("instructions", ""))[:2000],
                    want_cover_letter=bool(payload.get("cover_letter", True)),
                    want_outreach=bool(payload.get("outreach", False)),
                )
                answers = {item["id"]: item["answer"] for item in written["answers"]}
                for question in questions:
                    if answers.get(question["id"]):
                        question["answer"] = answers[question["id"]]
                draft["questions"] = questions
                if written["cover_letter"]:
                    draft["cover_letter"] = written["cover_letter"]
                if written["outreach_email"]:
                    draft["outreach_email"] = written["outreach_email"]
                saved = save_draft(
                    self.server.home, document, job.id, draft, existing=draft
                )
                self._json(
                    200,
                    {
                        "ok": True,
                        "draft": saved,
                        "unverified_claims": written["unverified_claims"],
                    },
                )
                return

            if parsed_request.path == "/api/cv/save":
                document, _profile = self._document(cv_id)
                draft = load_draft(self.server.home, job.id, cv_id)
                label = str(payload.get("label", "")).strip()
                target = safe_cv_id(payload.get("save_as", "") or label)
                if not target:
                    raise ValueError("Choose a name for the saved CV")
                info = save_cv(
                    self.server.home,
                    target,
                    label or target,
                    facts_from_document(document, draft),
                )
                self._json(
                    200,
                    {"ok": True, "cv": info, "cvs": list_cvs(self.server.home)},
                )
                return

            with Store(database_path(self.server.home)) as store:
                if parsed_request.path == "/api/draft":
                    document, _profile = self._document(cv_id)
                    incoming = payload.get("draft")
                    if not isinstance(incoming, dict):
                        raise ValueError("Expected a CV draft object")
                    incoming.setdefault("cv_id", cv_id)
                    existing = load_draft(self.server.home, job.id, cv_id)
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
                    document, _profile = self._document(cv_id)
                    draft = load_draft(self.server.home, job.id, cv_id)
                    resume = resume_from_document(document, draft)
                    person = str(document.get("header", {}).get("name", ""))
                    filename = _download_name(person, job)
                    output = (
                        self.server.home
                        / "generated"
                        / _safe_filename(job.id).removesuffix(".pdf")
                        / "full-tailored-resume.pdf"
                    )
                    resume_hash = render_resume(
                        resume, output, title=filename.removesuffix(".pdf")
                    )
                    ticket = self.server.new_download(output, filename)
                    host, port = self.server.server_address
                    self._json(
                        200,
                        {
                            "ok": True,
                            "resume_sha256": resume_hash,
                            "resume_download_url": (
                                f"http://{host}:{port}/resume/{ticket}"
                            ),
                            "resume_filename": filename,
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
                _download_name(self._person_name(), refreshed),
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
