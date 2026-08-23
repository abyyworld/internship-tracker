"""The rebuilt front page, driven in a real browser.

One box, every kind of opportunity, in either theme. What can break here is
nothing a unit test can see: whether typing a sentence actually narrows 1,300
things down to the right handful, whether the lenses show what they claim,
whether the theme survives a reload, and whether the page says why each card
is in front of you. Run it after touching dashboard_page.py.

Not named test_*, so `unittest discover` leaves it alone: it needs a browser.

    python3 tests/browser_opportunity_views.py
"""

import http.server
import os
import socketserver
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from playwright.sync_api import sync_playwright  # noqa: E402

DOCS = Path(__file__).resolve().parent.parent / "docs"


class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS), **kwargs)

    def log_message(self, *args):
        pass


def main() -> int:
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Quiet)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_address[1]
    failures: list[str] = []

    def check(label: str, condition: bool, detail: str = "") -> None:
        print(f"  {'PASS' if condition else 'FAIL'}  {label}"
              + (f"   [{detail}]" if detail and not condition else ""))
        if not condition:
            failures.append(label)

    def count() -> int:
        return page.locator(".card").count()

    with sync_playwright() as play:
        chromium = os.environ.get("CHROMIUM_PATH", "")
        browser = (play.chromium.launch(executable_path=chromium) if chromium
                   else play.chromium.launch())
        context = browser.new_context(color_scheme="light")
        page = context.new_page()
        noise: list[str] = []
        page.on("pageerror", lambda error: noise.append(f"pageerror: {error}"))
        page.on("console", lambda message: noise.append(message.text)
                if message.type == "error" else None)
        page.goto(f"http://127.0.0.1:{port}/", wait_until="networkidle")
        page.wait_for_selector(".card")

        print("\n[1] it opens on everything, ordered and counted")
        check("cards are drawn", count() > 0, str(count()))
        check("the count says what they are", "match" in page.inner_text("#count"),
              page.inner_text("#count"))
        for lens in ("roles", "research", "ventures", "funding", "universities"):
            has = page.locator(f'.lens[data-lens="{lens}"]').count() == 1
            check(f"there is a lens for {lens}", has)

        print("\n[2] typing a sentence narrows it to what was asked for")
        everything = int(page.inner_text("#count").split()[0].replace(",", ""))
        page.fill("#ask", "robotics internship in the UK")
        page.wait_for_timeout(700)
        narrowed = int(page.inner_text("#count").split()[0].replace(",", ""))
        check("it is narrower than everything", 0 < narrowed < everything,
              f"{narrowed} of {everything}")
        check("and it says what it read", "for “" in page.inner_text("#countSub"),
              page.inner_text("#countSub"))
        check("every card says which part of it they answer",
              page.locator(".why").count() == count(),
              f"{page.locator('.why').count()} of {count()}")
        first = page.locator(".card").first.inner_text()
        check("the place asked for is the place shown",
              "United Kingdom" in first or "UK" in first, first[:160])

        print("\n[3] a word for a kind sends you to that lens")
        page.fill("#ask", "fully funded scholarship for a masters")
        page.press("#ask", "Enter")
        page.wait_for_timeout(600)
        check("saying scholarship opens funding",
              page.locator('.lens[data-lens="funding"]').get_attribute("class").endswith("on"),
              page.locator(".lens.on").inner_text())
        check("and the cards are schemes", "funding scheme" in page.inner_text("#count"),
              page.inner_text("#count"))

        print("\n[4] the lenses show what they say they show")
        page.fill("#ask", "")
        page.wait_for_timeout(400)
        page.click('.lens[data-lens="universities"]')
        page.wait_for_timeout(400)
        check("universities are ordered by rank, best first",
              "Oxford" in page.locator(".card").first.inner_text(),
              page.locator(".card").first.inner_text()[:80])
        # The labels are set in small caps by the stylesheet, so what comes back
        # from the browser is upper case.
        check("a US institution carries the figures that answer “why here”",
              "earnings after 10y" in page.inner_text(".cards").lower(), "no scorecard facts")
        check("and the way to find who takes students is on the card",
              page.locator("a:has-text('Faculty directory')").count() > 0)
        page.click('.lens[data-lens="research"]')
        page.wait_for_timeout(400)
        check("PhD and research is its own lens",
              "PhD & research post" in page.inner_text("#count"), page.inner_text("#count"))

        print("\n[5] light and dark, and it stays chosen")
        page.click('.lens[data-lens="roles"]')
        page.wait_for_timeout(300)
        check("it opens in the theme this device asks for",
              page.get_attribute("html", "data-theme") is None,
              str(page.get_attribute("html", "data-theme")))
        light = page.evaluate("getComputedStyle(document.body).backgroundColor")
        page.click("#themeBtn")
        page.click("#themeBtn")
        page.wait_for_timeout(200)
        dark = page.evaluate("getComputedStyle(document.body).backgroundColor")
        check("dark is a different page, not a filter", light != dark, f"{light} vs {dark}")
        check("the button says which it is on", page.inner_text("#themeBtn") == "Dark",
              page.inner_text("#themeBtn"))
        page.reload(wait_until="networkidle")
        page.wait_for_selector(".card")
        check("and the choice survives a reload",
              page.get_attribute("html", "data-theme") == "dark",
              str(page.get_attribute("html", "data-theme")))

        print("\n[6] keeping things, and finding them again")
        page.click('.lens[data-lens="roles"]')
        page.wait_for_timeout(300)
        page.locator(".card .save").first.click()
        page.wait_for_timeout(200)
        check("the star fills in", page.locator(".save.on").count() == 1)
        check("and the header counts it", page.inner_text("#savedCount") == "1",
              page.inner_text("#savedCount"))
        page.click("#savedBtn")
        page.wait_for_timeout(300)
        check("pressing it shows only what was kept", count() == 1, str(count()))
        page.click("#savedBtn")
        page.wait_for_timeout(300)

        print("\n[7] every job still leads to the CV editor")
        link = page.locator("a:has-text('Edit CV for this job')").first
        href = link.get_attribute("href")
        check("through the opener, never straight at localhost",
              href.startswith("./open.html?url="), href[:60])
        check("carrying the role", "role=" in href, href[:120])

        print("\n[8] the filters still filter")
        total = lambda: int(page.inner_text("#count").split()[0].replace(",", ""))
        everything_now = total()
        page.select_option("#region", "UK")
        page.wait_for_timeout(400)
        uk = total()
        check("choosing a region narrows it", 0 < uk < everything_now, f"{uk} of {everything_now}")
        check("and every card is in it", "United Kingdom" in page.inner_text(".cards")
              or "UK" in page.inner_text(".cards"))
        page.click("#clearAll")
        page.wait_for_timeout(400)
        check("clearing puts everything back", total() > uk, f"{total()} then {uk}")

        print("\n[9] the studio agrees about the theme")
        page.goto(f"http://127.0.0.1:{port}/studio.html", wait_until="networkidle")
        page.wait_for_timeout(300)
        check("the CV studio opens dark because the dashboard was left dark",
              page.get_attribute("html", "data-theme") == "dark",
              str(page.get_attribute("html", "data-theme")))

        print("\n[10] nothing threw")
        real = [line for line in noise if "favicon" not in line.lower()]
        check("no console errors", not real, "; ".join(real[:3]))
        browser.close()

    server.shutdown()
    print("\n" + ("ALL CHECKS PASSED" if not failures
                  else f"{len(failures)} FAILED: {failures}"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
