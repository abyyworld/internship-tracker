"""Drive docs/studio.html in a browser against a fake provider.

The studio is the version of the CV editor that needs nothing installed: the CV
lives in the browser, the key lives in the browser, and the rewrite request goes
straight from the page to whichever provider the reader chose. That last part is
the whole risk — there is no server of ours in the path to be careful on the
reader's behalf, so the page has to get the request, the JSON, the errors and
the storage right by itself.

Not named test_*, so `unittest discover` leaves it alone: it needs a browser.

    python3 tests/browser_studio.py
"""
from __future__ import annotations

import http.server
import json
import os
import re
import tempfile
from pathlib import Path
import socketserver
import sys
import threading

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from playwright.sync_api import sync_playwright  # noqa: E402

DOCS = Path(__file__).resolve().parent.parent / "docs"

CV = """Ada Lovelace
London · ada@example.test

EXPERIENCE
Robotics Intern — Robot Co, Summer 2025
Built a vision pipeline for a pick-and-place arm in Python and ROS.
Rewrote the grasp planner and cut cycle time by 20 percent.

EDUCATION
BSc Computer Science, University of London, 2027"""


class Provider(http.server.BaseHTTPRequestHandler):
    """An OpenAI-compatible endpoint that answers a browser.

    Browser requests carrying an Authorization header are preflighted, so a fake
    provider that does not answer OPTIONS tests nothing at all — the real
    request would never leave the page.
    """

    mode = "ok"

    def _cors(self) -> None:
        origin = self.headers.get("Origin", "*")
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Headers", "authorization,content-type")
        self.send_header("Access-Control-Allow-Methods", "POST,OPTIONS")

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        request = json.loads(self.rfile.read(length) or b"{}")
        if Provider.mode == "google-error":
            # Google's OpenAI-compatible endpoint wraps errors in an array. A
            # page that assumes {"error": {...}} shows "HTTP 400" and nothing.
            body = json.dumps([{"error": {
                "code": 400, "status": "INVALID_ARGUMENT",
                "message": "API key not valid. Please pass a valid API key.",
            }}]).encode()
            self.send_response(400)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        prompt = request["messages"][-1]["content"]
        # Answer against the lines the page actually numbered, in a fenced code
        # block — which is what models do however firmly they are told not to.
        numbered = [line for line in prompt.splitlines() if line[:1].isdigit()]
        picks = []
        for line in numbered:
            index, _, text = line.partition(": ")
            if "grasp planner" in text:
                picks.append({"line": int(index),
                              "text": "Rewrote the grasp planner in C++, cutting cycle "
                                      "time by 20 percent on the production arm.",
                              "why": "The advert asks for C++ and for measured results."})
            elif "vision pipeline" in text:
                picks.append({"line": int(index),
                              "text": "Built the vision pipeline for a pick-and-place arm "
                                      "in Python and ROS 2.",
                              "why": "The advert names ROS 2 explicitly."})
        answer = "```json\\n" + json.dumps({"rewrites": picks}) + "\\n```"
        body = json.dumps({"choices": [{"message": {"content": answer}}]}).encode()
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args) -> None:
        pass


class Docs(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS), **kwargs)

    def log_message(self, *args) -> None:
        pass


def serve(handler) -> socketserver.TCPServer:
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def pdf_text(blob: bytes) -> str:
    """The text a reader would see, out of a PDF this page wrote itself.

    Nothing general: the streams are uncompressed and every string is written
    as a literal, because that is what the studio emits. It is enough to prove
    the CV is in the file rather than an empty page of the right size.
    """
    out = []
    for literal in re.findall(rb"\((?:[^()\\]|\\.)*\)", blob):
        out.append(literal[1:-1].replace(rb"\(", b"(").replace(rb"\)", b")")
                   .decode("cp1252", "replace"))
    return " ".join(out)


def valid_xref(blob: bytes) -> bool:
    """Every offset in the cross-reference table lands on its own object.

    A PDF whose xref is wrong opens in some readers and not others, which is
    the worst way for this to fail: it would look fine here and be broken on
    the machine of whoever was sent the CV.
    """
    # Not rsplit(b"xref") — the last "xref" in a PDF is inside "startxref".
    table = blob.rsplit(b"\nxref\n", 1)[-1]
    rows = re.findall(rb"(\d{10}) 00000 n", table)
    if not rows:
        return False
    for number, row in enumerate(rows, start=1):
        offset = int(row)
        if not blob[offset:offset + 24].startswith(f"{number} 0 obj".encode()):
            return False
    return True


def launch_chromium(play):
    try:
        return play.chromium.launch()
    except Exception:
        path = os.environ.get("CHROMIUM_PATH", "")
        if not path:
            raise
        return play.chromium.launch(executable_path=path)


def main() -> int:
    site = serve(Docs)
    provider = serve(Provider)
    base = f"http://127.0.0.1:{provider.server_address[1]}/v1"
    page_url = (
        f"http://127.0.0.1:{site.server_address[1]}/studio.html"
        "?url=https%3A%2F%2Fjobs.ashbyhq.com%2Frobot%2F12345678-1234-1234-1234-123456789abc"
        "&role=Robotics%20Intern&company=Robot%20Co&location=London&tags=robotics,perception"
    )

    failures: list[str] = []

    def check(label: str, condition: bool, detail: str = "") -> None:
        print(f"  {'PASS' if condition else 'FAIL'}  {label}"
              + (f"   [{detail}]" if detail and not condition else ""))
        if not condition:
            failures.append(label)

    with sync_playwright() as play:
        browser = launch_chromium(play)
        page = browser.new_page()
        console: list[str] = []
        page.on("console", lambda m: console.append(f"{m.type}: {m.text}"))
        page.on("pageerror", lambda e: console.append(f"pageerror: {e}"))
        page.goto(page_url, wait_until="networkidle")

        print("\n[1] it opens knowing the posting, with nothing installed")
        check("the role is named", "Robotics Intern" in page.inner_text("#roleTitle"))
        check("the company is named and can be corrected",
              page.input_value("#companyInput") == "Robot Co",
              page.input_value("#companyInput"))
        check("what it is about is carried over",
              "perception" in page.inner_text("#jobFacts"), page.inner_text("#jobFacts"))
        check("the posting is one click away",
              "ashbyhq.com" in page.get_attribute("#postingLink", "href"))
        check("no helper banner when nothing is listening",
              not page.is_visible("#helperBanner"))

        print("\n[2] the CV is pasted once and set as a document")
        page.fill("#cvPaste", CV)
        page.click("#useCv")
        page.wait_for_selector("#sheet .b")
        check("the name is set as a name", page.locator("#sheet .name").count() == 1)
        check("contact details are set apart", page.locator("#sheet .contact").count() == 1)
        check("section heads are found", page.locator("#sheet .section").count() == 2,
              str(page.locator("#sheet .section").count()))
        check("the dated entry is split from its date",
              page.locator("#sheet .entry .when").first.inner_text() == "Summer 2025",
              page.locator("#sheet .entry").count()
              and page.locator("#sheet .entry .when").first.inner_text())
        check("the body lines are body", page.locator("#sheet .body").count() >= 2,
              str(page.locator("#sheet .body").count()))
        check("the sheet is A4 in points",
              abs(page.evaluate("document.getElementById('sheet').offsetWidth")
                  - 595.28 * 96 / 72) < 3,
              str(page.evaluate("document.getElementById('sheet').offsetWidth")))
        check("the paste box gets out of the way", not page.is_visible("#pasteCard"))

        print("\n[3] the advert is pasted, because a web page cannot fetch it")
        page.fill("#advert", "We need ROS 2 and C++ for a production pick-and-place cell. "
                             "Tell us what you measured.")
        check("the page counts what it was given",
              "words" in page.inner_text("#advertNote"), page.inner_text("#advertNote"))

        print("\n[4] rewriting, straight from the page to the provider")
        page.select_option("#provider", "custom")
        page.fill("#customBase", base)
        page.fill("#model", "fake-chat")
        page.fill("#key", "test-key-not-a-real-one")
        page.click("#rewrite")
        page.wait_for_selector(".proposal", timeout=20000)
        proposals = page.locator(".proposal")
        check("proposals came back", proposals.count() == 2, str(proposals.count()))
        check("a fenced JSON answer was still read",
              "ROS 2" in page.inner_text("#sheet"), page.inner_text("#sheet")[:160])
        check("each says what it answers",
              "advert" in page.locator(".proposal .why").first.inner_text())
        check("nothing was applied without being accepted",
              "cut cycle time by 20 percent." in page.inner_text("#sheet"))

        print("\n[5] accepting one and rejecting the other")
        page.locator(".proposal .yes").first.click()
        page.wait_for_timeout(200)
        check("the accepted line replaced the original",
              "ROS 2" in page.inner_text("#sheet .changed"), page.inner_text("#sheet")[:200])
        page.locator(".proposal .no").first.click()
        page.wait_for_timeout(200)
        check("the rejected one is gone", page.locator(".proposal").count() == 0)
        check("and its original line is untouched",
              "cut cycle time by 20 percent." in page.inner_text("#sheet"))

        print("\n[6] it is all still there after a reload")
        page.reload(wait_until="networkidle")
        page.wait_for_selector("#sheet .b")
        check("the CV came back", "Ada Lovelace" in page.inner_text("#sheet"))
        check("the accepted edit came back", "ROS 2" in page.inner_text("#sheet"))
        check("the advert came back", "production pick-and-place" in page.input_value("#advert"))
        check("the key came back", page.input_value("#key") == "test-key-not-a-real-one")

        print("\n[7] a provider that refuses is quoted, not swallowed")
        # From here the test provokes a 400 on purpose, and the browser logs
        # every failed request. What matters after that point is only whether
        # the page itself threw.
        before_provoking = len(console)
        Provider.mode = "google-error"
        page.click("#rewrite")
        page.wait_for_selector("#notice.error", timeout=20000)
        said = page.inner_text("#notice")
        check("the provider's own words are shown",
              "API key not valid" in said, said)
        check("and it names what kind of failure that is",
              "refused" in said.lower(), said)
        Provider.mode = "ok"

        print("\n[8] the PDF is a real file, written here")
        with page.expect_download(timeout=20000) as caught:
            page.click("#download")
        download = caught.value
        target = Path(tempfile.mkdtemp()) / "cv.pdf"
        download.save_as(target)
        blob = target.read_bytes()
        check("it downloaded without a print dialog", blob[:5] == b"%PDF-", str(blob[:16]))
        check("it ends properly", blob.rstrip().endswith(b"%%EOF"), str(blob[-24:]))
        check("named after the job and the person",
              download.suggested_filename == "Robot Co - Robotics Intern - Ada Lovelace - CV.pdf",
              download.suggested_filename)
        text = pdf_text(blob)
        check("the CV is in it", "Ada Lovelace" in text, text[:120])
        check("including the accepted rewrite", "ROS 2" in text, text[:200])
        check("set in the CV's own fonts",
              b"/Times-Roman" in blob and b"/Helvetica-Bold" in blob)
        check("on A4", b"/MediaBox [0 0 595.28 841.89]" in blob)
        check("and a reader can find every object",
              valid_xref(blob), "xref offsets do not point at their objects")

        print("\n[8b] a long CV runs onto more pages")
        page.click("#editRaw")
        page.fill("#cvPaste", CV + "\n\nEXPERIENCE\n"
                  + "\n".join(f"Did a thing worth writing down, number {n}, at some length "
                               f"so the line wraps and the page eventually fills up." 
                               for n in range(90)))
        page.click("#useCv")
        page.wait_for_selector("#sheet .b")
        with page.expect_download(timeout=20000) as caught_long:
            page.click("#download")
        long_pdf = Path(tempfile.mkdtemp()) / "long.pdf"
        caught_long.value.save_as(long_pdf)
        pages_in = long_pdf.read_bytes().count(b"/Type /Page ")
        check("it paginated", pages_in >= 2, f"{pages_in} pages")
        check("the page tree agrees", f"/Count {pages_in}".encode() in long_pdf.read_bytes())
        # Put the short CV back for the rest of the run.
        page.click("#editRaw")
        page.fill("#cvPaste", CV)
        page.click("#useCv")

        print("\n[9] and everything can be deleted from this device")
        page.evaluate("window.confirm = () => true")
        page.click("#forget")
        page.wait_for_timeout(300)
        check("the CV is gone", "Ada Lovelace" not in page.inner_text("#sheet"))
        check("the key is gone", page.input_value("#key") == "")
        check("storage is empty",
              page.evaluate("Object.keys(localStorage).filter(k=>k.startsWith('studio.')).length") == 0)

        print("\n[10] the page stayed clean")
        # The two probes for a local helper are expected to fail here — nothing
        # is listening on 8765 — and a refused loopback request is logged by the
        # browser itself. That noise is the feature working, not a fault.
        quiet = [c for c in console[:before_provoking] + [c for c in console if c.startswith("pageerror")]
                 if "error" in c.lower() and "ERR_CONNECTION_REFUSED" not in c]
        check("no console errors", not quiet, "; ".join(quiet[:4]))
        browser.close()

    site.shutdown()
    provider.shutdown()
    print("\n" + ("ALL CHECKS PASSED" if not failures
                  else f"{len(failures)} FAILED: {failures}"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
