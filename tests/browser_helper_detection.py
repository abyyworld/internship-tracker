"""Detecting the local helper, against the three states that actually occur.

A false "not running" is the expensive failure: it locks someone out of a
helper that is working, and it happened — the favicon probe was added in one
build, and every helper installed before it answered 404 to the probe and was
declared dead. So the check is two probes and a bias toward opening the editor.

Not named test_*, so `unittest discover` leaves it alone: it needs a browser.

    python3 tests/browser_helper_detection.py
"""
import http.server, socketserver, os, sys, threading, functools
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from playwright.sync_api import sync_playwright

DOCS = Path(__file__).resolve().parent.parent / "docs"
POSTING = "https://www.amazon.jobs/en/jobs/3136266/robotics-intern"

class Docs(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(DOCS), **k)
    def log_message(self, *a): pass

class Reusable(http.server.HTTPServer):
    """Bind even while the previous test's socket is still in TIME_WAIT."""
    def server_bind(self):
        import socket as _s
        self.socket.setsockopt(_s.SOL_SOCKET, _s.SO_REUSEADDR, 1)
        try:
            self.socket.setsockopt(_s.SOL_SOCKET, _s.SO_REUSEPORT, 1)
        except (AttributeError, OSError):
            pass
        super().server_bind()


class OldBridge(http.server.BaseHTTPRequestHandler):
    """An Aug-15 bridge: serves /connect and /editor, 404s /favicon.ico."""
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path.startswith("/favicon.ico"):
            self.send_error(404); return
        body = b"<!doctype html><title>editor</title>old build editor"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)

def main():
    docs = http.server.HTTPServer(("127.0.0.1", 0), Docs)
    threading.Thread(target=docs.serve_forever, daemon=True).start()
    port = docs.server_address[1]
    fails = []
    def check(label, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"   [{detail}]" if not ok and detail else ""))
        if not ok: fails.append(label)

    with sync_playwright() as play:
        chromium = os.environ.get("CHROMIUM_PATH", "")
        b = (play.chromium.launch(executable_path=chromium) if chromium
             else play.chromium.launch())

        print("\n[1] nothing listening at all")
        page = b.new_page()
        page.goto(f"http://127.0.0.1:{port}/open.html?url={POSTING}", wait_until="domcontentloaded")
        # No helper is not a dead end any more: the browser studio does the job
        # with nothing installed, so deciding "not running" has to land there.
        page.wait_for_url("**studio.html**", timeout=12000)
        page.wait_for_selector("#cvPaste")
        check("hands the posting to the browser studio", "studio.html" in page.url, page.url)
        check("which is usable immediately", page.is_visible("#cvPaste"))

        print("\n[2] an older helper that does not serve /favicon.ico")
        old = Reusable(("127.0.0.1", 8765), OldBridge)
        threading.Thread(target=old.serve_forever, daemon=True).start()
        page2 = b.new_page()
        page2.goto(f"http://127.0.0.1:{port}/open.html?url={POSTING}", wait_until="domcontentloaded")
        try:
            page2.wait_for_url("**127.0.0.1:8765/editor**", timeout=12000)
            check("opens the editor anyway", True)
        except Exception:
            check("opens the editor anyway", False, page2.url + " | " + page2.inner_text("h1"))
        old.shutdown(); old.server_close()
        import time; time.sleep(1)   # let the port clear before the next server

        print("\n[3] a current helper that does serve it")
        from autoapply.bridge import BridgeServer
        import tempfile
        home = Path(tempfile.mkdtemp()); (home/"tracker.csv").write_text("")
        bridge = BridgeServer(("127.0.0.1", 8765), home=home, tracker=home/"tracker.csv", token="t"*40)
        threading.Thread(target=bridge.serve_forever, daemon=True).start()
        page3 = b.new_page()
        page3.goto(f"http://127.0.0.1:{port}/open.html?url={POSTING}", wait_until="domcontentloaded")
        try:
            page3.wait_for_url("**127.0.0.1:8765/editor**", timeout=12000)
            check("opens the editor", True)
        except Exception:
            check("opens the editor", False, page3.url)
        bridge.shutdown(); bridge.server_close()
        b.close()
    docs.shutdown()
    print("\n" + ("ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILED: {fails}"))
    return 1 if fails else 0

if __name__ == "__main__":
    raise SystemExit(main())
