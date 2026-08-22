"""The three opportunity views, driven in a real browser.

Roles, Ventures and Funding are alternatives to each other on one page, so the
thing that can break is the switching between them and the filters inside each —
none of which a unit test can see. Run it after touching dashboard.py.

Not named test_*, so `unittest discover` leaves it alone: it needs a browser.

    python3 tests/browser_opportunity_views.py
"""

import http.server, socketserver, os, sys, threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from playwright.sync_api import sync_playwright
DOCS = Path(__file__).resolve().parent.parent / "docs"

class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(DOCS), **k)
    def log_message(self, *a): pass

def main():
    httpd = socketserver.TCPServer(("127.0.0.1", 0), Quiet)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    port = httpd.server_address[1]
    fails=[]
    def check(label, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"   [{detail}]" if not ok and detail else ""))
        if not ok: fails.append(label)
    with sync_playwright() as play:
        chromium = os.environ.get("CHROMIUM_PATH", "")
        b = (play.chromium.launch(executable_path=chromium) if chromium
             else play.chromium.launch())
        page = b.new_page()
        errors=[]
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type=="error" else None)
        page.goto(f"http://127.0.0.1:{port}/", wait_until="networkidle")

        print("\n[roles view is still the default]")
        check("roles grid visible", page.is_visible("#cards"))
        check("ventures hidden", not page.is_visible("#venturesView"))
        check("tab shows role count", page.inner_text("#rolesCount").strip().isdigit())

        print("\n[switching to ventures]")
        page.click('button[data-view="ventures"]')
        page.wait_for_selector("#venturesView:not([hidden])", timeout=8000)
        check("roles hidden", not page.is_visible("#cards"))
        cards = page.locator(".opp")
        check("cards rendered", cards.count() >= 20, f"{cards.count()}")
        first = page.inner_text(".opp")
        check("Y Combinator present", "Y Combinator" in page.inner_text("#ventureGrid"))
        check("shows what it gives", "Gives" in first)
        check("shows what it takes", "Takes" in first)
        check("shows the cycle", "batch" in page.inner_text("#ventureGrid").lower())

        print("\n[filters]")
        total = cards.count()
        page.check("#vNoEquity")
        page.wait_for_timeout(250)
        noeq = page.locator(".opp").count()
        check("no-equity filter narrows", 0 < noeq < total, f"{noeq}/{total}")
        check("every remaining card says no equity",
              page.locator(".opp .tag.free").count() == noeq)
        page.uncheck("#vNoEquity")
        page.select_option("#vAudience", "phd")
        page.wait_for_timeout(250)
        phd = page.inner_text("#ventureGrid")
        check("PhD audience keeps Conception X", "Conception X" in phd)
        check("PhD audience drops student-only Neo", "Neo Scholars" not in phd)
        page.select_option("#vAudience", "")
        page.select_option("#vRegion", "GB")
        page.wait_for_timeout(250)
        gb = page.inner_text("#ventureGrid")
        check("UK filter keeps Start Up Loans", "Start Up Loans" in gb)
        check("UK filter drops US-only Neo", "Neo Scholars" not in gb)
        page.click("#vClear")
        page.wait_for_timeout(250)
        check("clear restores everything", page.locator(".opp").count() == total)
        page.fill("#vSearch", "robotics")
        page.wait_for_timeout(250)
        check("search finds the robotics-friendly fund", "Creator Fund" in page.inner_text("#ventureGrid"))
        page.fill("#vSearch", "")

        print("\n[funding tab and persistence]")
        page.click('button[data-view="funding"]')
        page.wait_for_selector("#funding:not([hidden])", timeout=8000)
        check("funding grid rendered", page.locator(".fund").count() > 0)
        page.reload(wait_until="networkidle")
        check("view is remembered across a reload", page.is_visible("#funding"))
        page.click('button[data-view="roles"]')
        page.wait_for_selector("#cards", timeout=8000)
        check("back to roles", page.is_visible("#cards"))

        check("no console errors", not errors, "; ".join(errors[:3]))
        b.close()
    httpd.shutdown()
    print("\n" + ("ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILED: {fails}"))
    return 1 if fails else 0
if __name__ == "__main__":
    raise SystemExit(main())
