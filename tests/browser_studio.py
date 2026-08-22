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
import time
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
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._cors()
        self.end_headers()

    def _answer(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        """What an OpenAI-compatible endpoint says its key can reach.

        Including the things that cannot hold a conversation, because a real
        list is full of them and offering them as a choice is a trap.
        """
        if not self.path.rstrip("/").endswith("/models"):
            self.send_error(404)
            return
        listed = ["fake-chat", "fake-chat-lite", "fake-chat-pro",
                  "models/fake-prefixed", "fake-embed-001", "fake-tts-1"]
        self._answer(200, json.dumps({"data": [{"id": name} for name in listed]}).encode())

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        request = json.loads(self.rfile.read(length) or b"{}")
        if Provider.mode == "slow":
            # A request that never comes back is what "seems stuck" was. The
            # page has to stay usable and stoppable for as long as this runs.
            time.sleep(30)
            return
        if Provider.mode == "google-error":
            # Google's OpenAI-compatible endpoint wraps errors in an array. A
            # page that assumes {"error": {...}} shows "HTTP 400" and nothing.
            self._answer(400, json.dumps([{"error": {
                "code": 400, "status": "INVALID_ARGUMENT",
                "message": "API key not valid. Please pass a valid API key.",
            }}]).encode())
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
        if Provider.mode == "cut":
            # The strongest edit a CV can get is often the one that takes a
            # line out, so the six seconds go to the lines that count.
            picks = [{"line": int(line.partition(": ")[0]), "text": "",
                      "why": "Says nothing this advert asks about."}
                     for line in numbered if "grasp planner" in line]
        if Provider.mode == "paraphrase":
            # What the complaint was: every line comes back as itself with the
            # words moved around. None of it is worth a reader's attention.
            picks = []
            for line in numbered:
                index, _, text = line.partition(": ")
                words = text.split()
                words[0], words[1] = words[1], words[0]
                picks.append({"line": int(index), "text": " ".join(words),
                              "why": "Reworded."})
        answer = "```json\\n" + json.dumps({"rewrites": picks}) + "\\n```"
        if Provider.mode == "truncated":
            # An answer that ran out of room: complete objects, then half of
            # one more. The complete ones are still advice.
            answer = json.dumps({"rewrites": picks})
            answer = answer[:answer.rindex("]")] + ', {"line": 4, "text": "half a li'
        self._answer(200, json.dumps({"choices": [{"message": {"content": answer}}]}).encode())

    def log_message(self, *args) -> None:
        pass


class Docs(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS), **kwargs)

    def log_message(self, *args) -> None:
        pass


def serve(handler) -> socketserver.TCPServer:
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
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


def a_real_cv_pdf(target: Path) -> Path:
    """A PDF of the kind people actually have: reportlab, compressed streams.

    Built with the project's own renderer, so what the studio has to read back
    is exactly what the local editor hands people to send to employers.
    """
    from reportlab.lib.enums import TA_RIGHT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table

    document = SimpleDocTemplate(str(target), pagesize=A4,
                                 leftMargin=15 * mm, rightMargin=15 * mm,
                                 topMargin=13 * mm, bottomMargin=14 * mm)
    name = ParagraphStyle("name", fontName="Times-Bold", fontSize=22, leading=25,
                          alignment=1)
    head = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=10, leading=14,
                          spaceBefore=10)
    body = ParagraphStyle("body", fontName="Times-Roman", fontSize=10, leading=13)
    def track(value: str) -> str:
        """Letterspacing the way this project's CV generator does it: the
        glyphs are the word and the spaces are typography, so a reader that
        takes them literally hands back A D A   L O V E L A C E."""
        return ("&nbsp;" * 4).join(" ".join(word) for word in value.split(" "))

    # What this project's own CV generator writes under the name, and the
    # bulleted list it writes under a project: ReportLab draws that bullet as
    # byte 127, which WinAnsi leaves undefined and therefore renders as a
    # bullet. Read as Latin-1 it is an invisible control character.
    tagline = ParagraphStyle("tagline", fontName="Times-Italic", fontSize=11.5,
                             leading=14, alignment=1, spaceBefore=6)
    bullet = ParagraphStyle("bullet", parent=body, leftIndent=9, bulletIndent=0,
                            spaceBefore=1.8, bulletFontName="Times-Roman",
                            bulletFontSize=10)
    right = ParagraphStyle("right", fontName="Helvetica-Bold", fontSize=8.4,
                           leading=13, alignment=TA_RIGHT)
    label = ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8.4, leading=12)

    def row(left_text: str, right_text: str, left_style, right_style, widths):
        """A two-column row, which is how a CV puts a date at the right margin
        and a skills label beside its values — and how their baselines end up a
        fraction apart, which is what broke reading them as one line."""
        table = Table([[Paragraph(left_text, left_style),
                        Paragraph(right_text, right_style)]], colWidths=widths)
        table.setStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2)])
        return table

    document.build([
        Paragraph(track("ADA LOVELACE"), name),
        Paragraph("Robot Learning &amp; Embodied AI &nbsp;&#183;&nbsp; "
                  "Simulation, Perception &amp; Evaluation", tagline),
        Paragraph("London &#183; ada@example.test", body),
        Spacer(1, 8),
        Paragraph(track("EXPERIENCE AND ML WORK"), head),
        row("<b>Research Assistant</b>", "May 2026 &#8211; Present",
            body, right, [330, 150]),
        Paragraph("University of London &#183; Internship", body),
        Paragraph("Ran the study end to end and analysed the results.", body),
        Paragraph("Robotics Intern &#8212; Robot Co, Summer 2025", body),
        Paragraph("Built a vision pipeline for a pick-and-place arm in Python and ROS.", body),
        Paragraph("Rewrote the grasp planner and cut cycle time by 20 percent.", body),
        Paragraph("Trained the policy in simulation and shipped it to the cell, "
                  "measuring every rollout.", bullet, bulletText="\u2022"),
        Paragraph("Wrote the evaluation harness the team now runs before every "
                  "release, in Python,", bullet, bulletText="\u2022"),
        Paragraph("NumPy and PyTorch.", body),
        Paragraph(track("EDUCATION"), head),
        Paragraph("BSc Computer Science, University of London, 2027", body),
        Paragraph(track("SKILLS"), head),
        row("AI / ML", "Machine Learning, Deep Learning, Computer Vision, NLP, "
            "Imitation Learning, Model Evaluation &amp; Calibration",
            label, body, [90, 390]),
        row("ROBOTICS", "Semantic Mapping, Closed-Loop Policy Evaluation, "
            "Demonstration Data Pipelines", label, body, [90, 390]),
    ])
    return target


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

        print("\n[2a] the CV people already have, read here")
        # The step that made this page worse than the editor it stands in for
        # was retyping a CV that already exists as a PDF.
        source = a_real_cv_pdf(Path(tempfile.mkdtemp()) / "Ada Lovelace CV.pdf")
        page.set_input_files("#file", str(source))
        page.wait_for_selector("#sheet .b", timeout=20000)
        imported = page.inner_text("#sheet")
        check("the name came through", "ADA LOVELACE" in imported, imported[:120])
        # Letterspaced heads are drawn as loose glyphs; taken literally they
        # would go into the CV as "A D A   L O V E L A C E" and be read that
        # way by every system that parses it.
        check("letterspacing was undone, including the short words",
              "EXPERIENCE AND ML WORK" in imported, imported[:200])
        check("and the lines stayed lines",
              "Rewrote the grasp planner and cut cycle time by 20 percent." in imported,
              imported[:300])
        check("the em dash survived", "—" in imported, imported[:200])
        # A date at the right margin and a skills label are separate text runs
        # whose baselines differ by a fraction of a point. Reading them as
        # their own lines is what turned a job into an entry called "May 2026".
        entries = {page.locator("#sheet .entry").nth(i).locator(".title").inner_text():
                   page.locator("#sheet .entry").nth(i).locator(".when").inner_text()
                   for i in range(page.locator("#sheet .entry").count())}
        check("a right-aligned date stayed with its job",
              entries.get("Research Assistant") == "May 2026 – Present", str(entries))
        pairs = {page.locator("#sheet .pair").nth(i).locator(".label").inner_text():
                 page.locator("#sheet .pair").nth(i).locator(".values").inner_text()
                 for i in range(page.locator("#sheet .pair").count())}
        check("the skills table came back as a table",
              "AI / ML" in pairs and "ROBOTICS" in pairs, str(list(pairs)))
        check("including the values that wrapped onto the next line",
              pairs.get("AI / ML", "").endswith("Calibration"), pairs.get("AI / ML", ""))
        check("the headline under the name is set as one, not as a subtitle",
              page.locator("#sheet .tagline").count() == 1,
              str(page.locator("#sheet .tagline").count()))
        check("a bulleted list comes back bulleted",
              page.locator("#sheet .bullet").count() == 2,
              str(page.locator("#sheet .bullet").count()))
        # ReportLab draws the bullet as byte 127. Read as Latin-1 that is an
        # invisible control character, which then exported as "?".
        check("and the bullet is a bullet, not a control character",
              "\u007f" not in imported and "\u2022" in imported,
              repr(imported[:200]))
        check("a bullet broken across two lines is one bullet again",
              "in Python, NumPy and PyTorch." in imported, imported[-300:])
        check("it says the file stayed here",
              "this browser only" in page.inner_text("#notice"), page.inner_text("#notice"))
        check("a scanned or unreadable file is refused honestly",
              page.evaluate("looksLikeText('\\x01\\x02\\x03 \\x7f'.repeat(40))") is False)

        print("\n[2] the CV can also be pasted, and is set as a document")
        page.click("#editRaw")
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

        print("\n[2b] more than one CV, and each posting remembers the one it used")
        before = page.locator("#cvPick option").count()
        second = Path(tempfile.mkdtemp()) / "Ada Robotics CV.txt"
        second.write_text("Ada Lovelace\nLondon · ada@example.test\n\nEXPERIENCE\n"
                          "Robotics Intern — Robot Co, Summer 2025\n"
                          "Tuned the grasp planner on the production cell.\n",
                          encoding="utf-8")
        page.click("#addCv")
        page.set_input_files("#file", str(second))
        page.wait_for_function(
            f"document.querySelectorAll('#cvPick option').length === {before + 1}", timeout=15000)
        check("a second CV is kept beside the first, not instead of it",
              page.locator("#cvPick option").count() == before + 1)
        check("named after the file it came from",
              page.input_value("#cvName") == "Ada Robotics CV", page.input_value("#cvName"))
        check("and the document is the one just added",
              "Tuned the grasp planner on the production cell." in page.inner_text("#sheet"))
        page.select_option("#cvPick", index=0)   # "Edit raw text" replaced the imported one
        page.wait_for_timeout(200)
        check("switching back brings the other one back, whole",
              "Built a vision pipeline" in page.inner_text("#sheet"),
              page.inner_text("#sheet")[:160])
        page.reload(wait_until="networkidle")
        page.wait_for_selector("#sheet .b")
        check("and this posting reopens on the CV it was left on",
              "Built a vision pipeline" in page.inner_text("#sheet"))
        # A posting never seen before has no CV of its own to remember, so it
        # opens on the one used last rather than on an empty page.
        page.goto(page_url.replace("12345678", "87654321"), wait_until="networkidle")
        page.wait_for_selector("#sheet .b")
        check("a posting never opened before starts from the CV used last",
              "Ada Lovelace" in page.inner_text("#sheet"), page.inner_text("#sheet")[:120])
        check("and it offers every CV on the device",
              page.locator("#cvPick option").count() == 2,
              str(page.locator("#cvPick option").count()))
        page.goto(page_url, wait_until="networkidle")
        page.wait_for_selector("#sheet .b")

        print("\n[3] the advert is pasted, because a web page cannot fetch it")
        page.fill("#advert", "We need ROS 2 and C++ for a production pick-and-place cell. "
                             "Tell us what you measured.")
        check("the page counts what it was given",
              "words" in page.inner_text("#advertNote"), page.inner_text("#advertNote"))

        print("\n[4] rewriting, straight from the page to the provider")
        page.select_option("#provider", "custom")
        page.fill("#customBase", base)
        page.fill("#key", "test-key-not-a-real-one")
        # Three names hard-coded in a page go stale in months. What the reader's
        # own key can reach is the only list worth showing.
        page.wait_for_function("document.querySelectorAll('#model option').length > 2",
                               timeout=15000)
        offered_models = page.eval_on_selector_all("#model option", "n => n.map(o => o.value)")
        check("the endpoint was asked what this key can reach",
              "fake-chat-lite" in offered_models, str(offered_models))
        check("a models/ prefix is stripped off",
              "fake-prefixed" in offered_models, str(offered_models))
        check("what cannot hold a conversation is left out",
              not [name for name in offered_models if "embed" in name or "tts" in name],
              str(offered_models))
        check("and anything unlisted can still be typed in",
              "Type a model name" in page.inner_text("#model"), page.inner_text("#model"))
        page.select_option("#model", "fake-chat")

        page.click('#modes button[data-mode="hard"]')
        check("how hard to go is a choice, and it says what it means",
              "cuts whatever does not earn its place" in page.inner_text("#modeNote"),
              page.inner_text("#modeNote"))
        page.click('#modes button[data-mode="full"]')
        page.fill("#instruction", "lead with the perception work")
        check("the chosen mode is the marked one",
              page.eval_on_selector("#modes button.on", "b => b.dataset.mode") == "full")
        check("what the applicant asked for reaches the model",
              "lead with the perception work" in page.evaluate("tailoringPrompt()"))

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

        print("\n[8] a provider that hangs can be given up on")
        # "its taking too long seems stuck": a page that says Rewriting… and
        # nothing else cannot be told apart from one that has died.
        Provider.mode = "slow"
        page.click("#rewrite")
        page.wait_for_function(
            "/[0-9]+s/.test(document.getElementById('status').textContent)", timeout=15000)
        check("the wait is counted out loud, in seconds",
              "Stop" in page.inner_text("#status"), page.inner_text("#status"))
        check("and the button is now the way out",
              page.inner_text("#rewrite").strip() == "Stop", page.inner_text("#rewrite"))
        page.click("#rewrite")
        page.wait_for_function(
            "document.getElementById('notice').textContent.includes('Stopped')", timeout=10000)
        check("stopping says so and gives the button back",
              page.inner_text("#rewrite").strip().startswith("Rewrite"),
              page.inner_text("#rewrite"))
        check("and the CV was not touched",
              "cut cycle time by 20 percent." in page.inner_text("#sheet"))

        print("\n[9] the same line with the words moved is not a suggestion")
        Provider.mode = "paraphrase"
        page.click("#rewrite")
        page.wait_for_function(
            "document.getElementById('notice').textContent.includes('swapped')", timeout=20000)
        check("nothing was offered for review",
              page.locator(".proposal").count() == 0, str(page.locator(".proposal").count()))
        check("and it says what to do about it",
              "Go hard" in page.inner_text("#notice"), page.inner_text("#notice"))

        print("\n[10] an answer cut off mid-sentence still yields what it managed")
        Provider.mode = "truncated"
        page.click("#rewrite")
        page.wait_for_selector(".proposal", timeout=20000)
        check("the complete suggestions survived the truncation",
              page.locator(".proposal").count() >= 1, str(page.locator(".proposal").count()))
        page.click("#rejectAll")
        Provider.mode = "ok"

        print("\n[10b] a line that earns nothing can be cut, with your say-so")
        Provider.mode = "cut"
        page.click("#rewrite")
        page.wait_for_selector(".proposal", timeout=20000)
        check("taking a line out is offered as an edit",
              "Cut this line" in page.inner_text(".proposal"),
              page.inner_text(".proposal")[:160])
        check("nothing is removed before it is accepted",
              "grasp planner" in page.inner_text("#sheet"))
        page.locator(".proposal .yes").first.click()
        page.wait_for_timeout(200)
        check("and the line goes when it is",
              "grasp planner" not in page.inner_text("#sheet"),
              page.inner_text("#sheet")[:200])
        page.reload(wait_until="networkidle")
        page.wait_for_selector("#sheet .b")
        check("a cut survives a reload, like every other edit",
              "grasp planner" not in page.inner_text("#sheet"))
        Provider.mode = "ok"

        print("\n[11] the PDF is a real file, written here")
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

        print("\n[11b] a long CV runs onto more pages")
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

        print("\n[12] and everything can be deleted from this device")
        page.evaluate("window.confirm = () => true")
        page.click("#forget")
        page.wait_for_timeout(300)
        check("the CV is gone", "Ada Lovelace" not in page.inner_text("#sheet"))
        check("the key is gone", page.input_value("#key") == "")
        check("storage is empty",
              page.evaluate("Object.keys(localStorage).filter(k=>k.startsWith('studio.')).length") == 0)

        print("\n[13] the page stayed clean")
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
