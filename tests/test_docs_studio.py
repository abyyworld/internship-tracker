"""The published pages that hold someone's CV and API key.

docs/studio.html is the version of the editor that needs nothing installed, so
it is the one page in this project that holds a reader's CV and their provider
key inside a page served from the public internet. What it must never do is
load code from anywhere else, or send that data anywhere but the endpoint the
reader chose. Those are properties of the file, so they are checked here rather
than in a browser harness that has to be run by hand.
"""

from pathlib import Path
import re
import unittest


DOCS = Path(__file__).resolve().parent.parent / "docs"
STUDIO = DOCS / "studio.html"
OPENER = DOCS / "open.html"


class StudioIsSelfContainedTests(unittest.TestCase):
    def setUp(self):
        self.source = STUDIO.read_text(encoding="utf-8")

    def test_it_loads_no_code_or_assets_from_anywhere_else(self):
        # A CDN script on this page could read the CV and the key out of
        # storage. There is no version of that which is acceptable, so there
        # are no external sources at all.
        for pattern in (r'<script[^>]+\bsrc=', r'<link[^>]+stylesheet[^>]*href="https?:',
                        r'@import\b', r'<iframe'):
            self.assertIsNone(re.search(pattern, self.source, re.I),
                              f"studio.html pulls in {pattern}")

    def test_the_only_places_it_sends_anything_are_chosen_by_the_reader(self):
        # Every fetch in the file: the provider endpoint the reader configured,
        # and the loopback probe that asks whether the better editor is running.
        targets = re.findall(r'fetch\(\s*([^,)]+)', self.source)
        self.assertTrue(targets)
        for target in targets:
            self.assertTrue(
                "endpoint" in target or "BRIDGE" in target,
                f"studio.html sends a request somewhere unexpected: {target}")

    def test_the_key_is_never_put_in_a_url(self):
        # A key in a query string ends up in history, in referrers, and in any
        # log the endpoint keeps. It goes in the Authorization header only.
        self.assertIn('"Authorization": `Bearer ${key}`', self.source)
        self.assertNotRegex(self.source, r"[?&]key=\$\{")

    def test_everything_it_stores_is_namespaced_and_removable(self):
        keys = set(re.findall(r'"(studio\.[a-z]+)', self.source))
        self.assertTrue(keys, "the storage keys are not recognisable")
        self.assertIn("studio.cv", keys)
        # "Forget everything on this device" must catch all of them, which it
        # can only do if every key really does share the prefix.
        self.assertIn('key.startsWith("studio.")', self.source)

    def test_it_says_where_the_reader_data_goes(self):
        # The trade is: nothing to install, but the CV and the advert go
        # straight to a third party. Saying so is not optional.
        for phrase in ("stored in this browser", "never uploaded",
                       "directly to the provider"):
            self.assertIn(phrase, self.source,
                          f"studio.html does not say: {phrase}")


class NoDeadEndsTests(unittest.TestCase):
    def test_a_posting_with_no_helper_lands_in_the_studio(self):
        opener = OPENER.read_text(encoding="utf-8")
        self.assertIn("./studio.html", opener)
        # Not merely mentioned: it is where the "no helper" decision goes.
        self.assertRegex(opener, r'destination === "editor"\) location\.replace\(studioUrl\)')

    def test_the_dashboard_offers_it_without_a_role(self):
        index = DOCS / "index.html"
        if not index.exists():  # generated; a fresh checkout may not have it yet
            self.skipTest("docs/index.html has not been generated here")
        self.assertIn("./studio.html", index.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
