"""docs/open.html: helper down must explain itself, helper up must get out of the way.

Every "Edit CV for this job" button goes through that page, so its two states are
the two states of the whole product for anyone who has not started the helper
yet. Driven in a real browser because the detection is a cross-origin image
probe, which no unit test can stand in for.

Not named test_*, so `unittest discover` leaves it alone: it needs a browser.

    python3 tests/browser_opener_page.py
"""
import http.server, socketserver, sys, threading, functools, tempfile, shutil, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from playwright.sync_api import sync_playwright

DOCS = Path(__file__).resolve().parent.parent / "docs"
POSTING = "https://www.amazon.jobs/en/jobs/3136266/robotics-software-development-engineer-intern"

def serve_docs():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DOCS), **kwargs)
        def log_message(self, *a):
            pass
    httpd = socketserver.TCPServer(("127.0.0.1", 0), Quiet)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd

def main():
    docs = serve_docs()
    port = docs.server_address[1]
    failures = []
    def check(label, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"   [{detail}]" if not ok and detail else ""))
        if not ok: failures.append(label)

    with sync_playwright() as play:
        chromium = os.environ.get("CHROMIUM_PATH", "")
        browser = (play.chromium.launch(executable_path=chromium) if chromium
                   else play.chromium.launch())
        page = browser.new_page()

        print("\n[helper NOT running]")
        page.goto(f"http://127.0.0.1:{port}/open.html?url={POSTING}", wait_until="networkidle")
        page.wait_for_selector("#down:not(.hidden)", timeout=12000)
        text = page.inner_text("#down")
        check("explains the helper is not running", "isn’t running" in text or "isn't running" in text)
        check("names the port", "127.0.0.1:8765" in text)
        check("names the installer", "install-login-service.command" in text)
        check("offers a retry", page.is_visible("#retry"))
        check("links the posting", page.get_attribute("#postingLink", "href") == POSTING)
        check("did not leave the page", "open.html" in page.url)

        print("\n[helper running]")
        from autoapply.bridge import BridgeServer
        home = Path(tempfile.mkdtemp()); (home / "tracker.csv").write_text("")
        bridge = BridgeServer(("127.0.0.1", 8765), home=home, tracker=home / "tracker.csv",
                              token="t" * 40)
        threading.Thread(target=bridge.serve_forever, daemon=True).start()
        page2 = browser.new_page()
        page2.goto(f"http://127.0.0.1:{port}/open.html?url={POSTING}", wait_until="domcontentloaded")
        try:
            page2.wait_for_url("**127.0.0.1:8765/editor**", timeout=12000)
            check("redirected into the local editor", True)
        except Exception as exc:
            check("redirected into the local editor", False, page2.url)
        bridge.shutdown(); bridge.server_close()
        browser.close()
    docs.shutdown()
    print("\n" + ("ALL CHECKS PASSED" if not failures else f"{len(failures)} FAILED: {failures}"))
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
