"""Drive the real editor page in a browser against a fake provider.

Everything the applicant does, in the order they do it: open the editor, read the
provider card, switch to an endpoint of their own, test it, generate a rewrite,
accept it, export the PDF, draft the application answers, and save the tailoring
as its own CV. The page's own JavaScript runs — no stubs, no mocked fetch.

Not named test_*, so `unittest discover` leaves it alone: it needs a browser, and
the read-only CI job has no display. Run it by hand after touching the editor
page or the bridge routes, which is exactly where unit tests cannot see:

    python3 tests/browser_editor_flow.py

It has already earned its place — it caught an undefined variable in two bridge
routes and a validator that flagged the word "I" in every cover letter.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from playwright.sync_api import sync_playwright  # noqa: E402

from autoapply.bridge import BridgeServer  # noqa: E402
from autoapply.models import Job  # noqa: E402
from autoapply.store import Store  # noqa: E402

PROFILE = """
identity:
  first_name: Ada
  last_name: Lovelace
contact:
  email: ada@invalid.test
  phone: "+44 20 7946 0000"
  phone_country: GB
  location: London, United Kingdom
education:
  institution: University of London
  degree: BSc
  field_of_study: Computer Science
  level: bachelors
  graduation_date: 2027-06-30
citizenships: [GB]
"""

FACTS = """
summary: >-
  Engineering student building verified robotics and machine-learning projects,
  with a record of shipping working systems end to end and measuring them.
skills: [Python, C++, ROS, PyTorch]
education: []
sections:
  - name: Projects
    layout: entries
    entries:
      - title: Robot arm controller
        organization: Personal project
        dates: 2025
        bullets:
          - id: arm-lead
            style: lead
            text: >-
              Built a Python controller for a six-axis robot arm and cut command
              latency by 20 percent against the previous loop.
          - id: arm-body
            text: >-
              Wrote the inverse-kinematics solver in C++, tested it against
              recorded joint traces, and documented the calibration procedure so
              another student could repeat it without help.
      - title: Vision prototype
        organization: University lab
        dates: 2026
        bullets:
          - id: vision
            text: >-
              Tested a computer-vision grasp-detection prototype on recorded
              images in PyTorch and reported where it failed on reflective parts.
"""

# One rewrite per section, shaped like a real model answer.
STRATEGY = {
    "requirements": ["Python", "robotics", "computer vision"],
    "section_order": ["s0"],
    "entry_order": {"s0": ["s0e0", "s0e1"]},
    "drop": [],
    "priorities": ["lead with the robot arm work"],
    "keywords": [
        {"term": "Python", "status": "covered", "importance": "high"},
        {"term": "robotics", "status": "covered", "importance": "high"},
        {"term": "computer vision", "status": "covered", "importance": "medium"},
        {"term": "Kubernetes", "status": "missing", "importance": "low"},
    ],
    "summary": {
        "proposal": (
            "Engineering student who builds verified robotics and machine-learning "
            "systems in Python and C++, shipping each one end to end and measuring "
            "what it changed."
        ),
        "rationale": "leads on the robotics evidence the posting asks for",
    },
    "advice": [],
}
SECTION = {
    "bullets": [
        {
            "fact_id": "arm-lead",
            "proposal": (
                "Built a Python controller for a six-axis robot arm and cut command "
                "latency by 20 percent against the previous control loop."
            ),
            "variants": [],
            "rationale": 'answers Python robotics: replaces "the previous loop" with the measured control loop',
            "keywords": ["Python", "robotics"],
        },
        {
            "fact_id": "arm-body",
            "proposal": (
                "Wrote the inverse-kinematics solver in C++, tested it against recorded "
                "joint traces, and documented the calibration procedure so another "
                "student could repeat the robotics work unaided."
            ),
            "variants": [],
            "rationale": 'answers robotics: quotes the posting\'s "robotics" for the calibration work',
            "keywords": ["C++", "robotics"],
        },
        {
            "fact_id": "vision",
            "proposal": (
                "Tested a computer-vision grasp-detection prototype in PyTorch on "
                "recorded images and reported where it failed on reflective parts."
            ),
            "variants": [],
            "rationale": 'answers computer vision: leads on the posting\'s "computer vision" wording',
            "keywords": ["computer vision", "PyTorch"],
        },
    ],
    "add": [],
}


def fake_provider():
    """An OpenAI-compatible endpoint that answers the tailoring calls."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, status, payload):
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            self._send(200, {"data": [{"id": "fake-chat-1"}, {"id": "fake-chat-2"}]})

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            sent = json.loads(self.rfile.read(length) or b"{}")
            system = sent["messages"][0]["content"]
            if "CV strategist" in system:
                answer = STRATEGY
            elif "rewriting one section" in system:
                answer = SECTION
            elif "extract application questions" in system:
                answer = {"questions": [
                    {"question": "Why do you want to work on robots?", "word_limit": 120}
                ]}
            elif "drafting an application" in system:
                answer = {
                    "answers": [{"id": "q0", "answer":
                        "I build robot control systems: I wrote a Python controller "
                        "for a six-axis arm and an inverse-kinematics solver in C++, "
                        "and I want to do that work at a larger scale."}],
                    "cover_letter": "Dear hiring team, I build robot control systems "
                                    "in Python and C++, and I test what I build.",
                    "outreach_email": "",
                }
            else:
                answer = {"ok": True}
            self._send(200, {
                "choices": [{"message": {"content": json.dumps(answer)}}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 50},
            })

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def launch_chromium(play):
    """The browser Playwright installed, or one already on this machine.

    `playwright install` puts a browser where the installed client expects it. A
    machine that already has a matching Chromium — a CI image, a shared runner —
    can point at it with $CHROMIUM_PATH instead of downloading another copy.
    """
    try:
        return play.chromium.launch()
    except Exception:
        path = os.environ.get("CHROMIUM_PATH", "")
        if not path:
            raise
        return play.chromium.launch(executable_path=path)


def main() -> int:
    home = Path(tempfile.mkdtemp()) / "private"
    home.mkdir(parents=True)
    home.chmod(0o700)
    (home / "profile.yaml").write_text(PROFILE, encoding="utf-8")
    (home / "resume_facts.yaml").write_text(FACTS, encoding="utf-8")
    tracker = home.parent / "tracker.csv"
    tracker.write_text("", encoding="utf-8")

    job = Job(
        "job-1", "Robot Co", "Robotics Intern",
        "https://jobs.ashbyhq.com/robot/12345678-1234-1234-1234-123456789abc",
        location="London",
        description=(
            "We are hiring a robotics intern to work on Python control software "
            "and computer vision for grasping. C++ experience welcome."
        ),
        ats="ashby", source_status="open",
    )
    with Store(home / "autoapply.sqlite3") as store:
        store.upsert_job(job)

    provider = fake_provider()
    base = f"http://127.0.0.1:{provider.server_address[1]}/v1"
    token = "e2e-token-with-more-than-thirty-two-characters"
    bridge = BridgeServer(("127.0.0.1", 0), home=home, tracker=tracker, token=token)
    threading.Thread(target=bridge.serve_forever, daemon=True).start()
    port = bridge.server_address[1]
    editor = (
        f"http://127.0.0.1:{port}/editor?url="
        "https%3A%2F%2Fjobs.ashbyhq.com%2Frobot%2F12345678-1234-1234-1234-123456789abc"
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
        page.add_init_script(
            f'localStorage.setItem("autoapply_bridge_token_v1", "{token}")'
        )
        page.goto(editor, wait_until="networkidle")

        print("\n[1] the page loads with the CV and the job")
        page.wait_for_selector("#cvDoc .fact, #cvDoc", timeout=15000)
        check("job title shown", "Robotics Intern" in page.inner_text("#jobTitle"))
        check("CV lines rendered", "robot arm" in page.inner_text("#cvDoc").lower())
        check("no console errors", not [c for c in console if "error" in c.lower()],
              "; ".join(console[:3]))

        print("\n[2] the provider card names the provider, not OpenAI")
        print("      keyTitle:", repr(page.inner_text("#keyTitle")),
              "| keyStatus:", repr(page.inner_text("#keyStatus")[:60]),
              "| providerNote:", repr(page.inner_text("#providerNote")[:60]))
        # The card's heading is upper-cased by CSS, so compare case-insensitively.
        check("key card names the selected provider",
              "openai key" in page.inner_text("#keyTitle").lower())
        check("build is shown", "Bridge build" in page.inner_text("#buildNote"),
              page.inner_text("#buildNote"))

        print("\n[3] switching to my own endpoint")
        page.click("#customEndpoint summary")
        page.fill("#customBase", base)
        page.click("#saveCustomBase")
        # A loopback endpoint of one's own is a local runtime: no key needed.
        page.wait_for_function(
            "() => document.getElementById('modelNote').textContent.includes('fake-chat')",
            timeout=20000)
        check("the endpoint is treated as local",
              "Running locally" in page.inner_text("#providerNote"),
              page.inner_text("#providerNote"))
        check("the key card is hidden for a local endpoint",
              not page.is_visible("#keyCard"))
        check("model picker filled from the endpoint",
              "fake-chat" in page.inner_text("#modelNote"), page.inner_text("#modelNote"))

        print("\n[4] testing the provider")
        page.click("#testProvider")
        page.wait_for_selector("#testReport:visible", timeout=20000)
        report = page.inner_text("#testReport")
        check("test reports status 200", "status    200" in report, report[:200])
        check("test names the endpoint", "chat/completions" in report)
        check("test says rewriting will work",
              "will work" in page.inner_text("#testNote"))

        print("\n[5] generating a rewrite")
        page.fill("#instructions", "Lead with the robot arm work.")
        page.click("#generate")
        page.wait_for_function(
            "() => !document.getElementById('generate').disabled", timeout=60000)
        check("no error notice", page.inner_text("#notice").strip() == "",
              page.inner_text("#notice"))
        proposals = page.locator(".patch, .suggestion, [data-fact]")
        check("suggestions rendered", "20 percent" in page.inner_text("#cvDoc"),
              page.inner_text("#cvDoc")[:200])

        print("\n[6] accepting everything and exporting")
        page.click("#acceptAll")
        with page.expect_download(timeout=60000) as download:
            page.click("#exportPdf")
        name = download.value.suggested_filename
        check("a PDF downloaded", name.endswith(".pdf"), name)
        check("named after the job", "Robot Co" in name, name)

        print("\n[7] drafting the application answers")
        page.click("#writeAnswers")
        page.wait_for_function(
            "() => !document.getElementById('writeAnswers').disabled", timeout=60000)
        check("no error notice after answers",
              page.inner_text("#notice").strip() == "", page.inner_text("#notice"))

        print("\n[8] saving this tailoring as its own CV")
        page.fill("#newCvName", "Robot Co - Robotics Intern")
        page.click("#saveAsCv")
        page.wait_for_timeout(1500)
        check("CV saved to the library",
              "Robot Co" in page.inner_text("#cvList"), page.inner_text("#cvList")[:200])

        print("\n[9] the page is still clean")
        errors = [c for c in console if "error" in c.lower()]
        check("no console errors at the end", not errors, "; ".join(errors[:5]))
        browser.close()

    bridge.shutdown()
    bridge.server_close()
    provider.shutdown()
    print("\n" + ("ALL CHECKS PASSED" if not failures
                  else f"{len(failures)} FAILED: {failures}"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
