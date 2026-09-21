"""Reading board names out of a public crawl index.

The network call is one function and everything else is pure, so the part where
mistakes would actually live is tested here without touching the web. That
matters more than usual: this code runs only inside the daily job, against an
index this development environment's network policy cannot reach, so if it is
wrong it is wrong in production and silent.
"""

import collections
import unittest

import board_harvest as harvest


def record(url, status="200"):
    return ('{"urlkey":"x","timestamp":"20260101","url":"%s","status":"%s"}'
            % (url, status))


class ReadingABoardOutOfACrawledUrl(unittest.TestCase):
    def test_the_shapes_each_provider_serves(self):
        cases = [
            ("https://boards.greenhouse.io/stripe/jobs/4012345", "Greenhouse", "stripe"),
            ("https://job-boards.greenhouse.io/nuro", "Greenhouse", "nuro"),
            ("https://boards.greenhouse.io/embed/job_board?for=anduril",
             "Greenhouse", "anduril"),
            ("https://jobs.lever.co/wayve/9f3a-77", "Lever", "wayve"),
            ("https://jobs.ashbyhq.com/zoox/12345678", "Ashby", "zoox"),
            ("http://jobs.ashbyhq.com/1x", "Ashby", "1x"),
        ]
        for url, provider, expected in cases:
            self.assertEqual(harvest.slug_of(url, provider), expected, url)

    def test_the_plumbing_is_not_a_company(self):
        # A board named "jobs" or "sitemap.xml" would be polled every day
        # forever, never answer, and still be counted as coverage.
        for url, provider in (("https://boards.greenhouse.io/", "Greenhouse"),
                              ("https://boards.greenhouse.io/robots.txt", "Greenhouse"),
                              ("https://jobs.lever.co/jobs/1234", "Lever"),
                              ("https://jobs.ashbyhq.com/api/v1/x", "Ashby")):
            self.assertIsNone(harvest.slug_of(url, provider), url)

    def test_a_url_from_another_provider_is_not_read_as_this_one(self):
        self.assertIsNone(harvest.slug_of("https://jobs.lever.co/wayve", "Ashby"))
        self.assertIsNone(harvest.slug_of("https://jobs.ashbyhq.com/zoox", "Lever"))

    def test_nonsense_in_the_slug_position_is_refused(self):
        for url in ("https://jobs.lever.co/-/x",
                    "https://jobs.lever.co/A%20B/x",
                    "https://jobs.lever.co/" + "x" * 90):
            self.assertIsNone(harvest.slug_of(url, "Lever"), url)


class CountingWhatTheIndexSays(unittest.TestCase):
    def test_a_board_is_counted_once_per_crawled_page(self):
        lines = [record("https://jobs.lever.co/wayve/a"),
                 record("https://jobs.lever.co/wayve/b"),
                 record("https://jobs.lever.co/dexterity/c")]
        counted = harvest.slugs_in(lines, "Lever")
        self.assertEqual(counted, collections.Counter({"wayve": 2, "dexterity": 1}))

    def test_junk_in_the_stream_costs_that_line_and_no_more(self):
        # The index API answers a bad query with a plain-text error, and a
        # truncated page ends mid-record. Neither may end the harvest.
        lines = ["No Captures found for: boards.greenhouse.io/*",
                 "",
                 '{"url":"https://jobs.lever.co/wayve/a"}',
                 '{"url": "https://jobs.lever.co/trunca',
                 record("https://jobs.lever.co/wayve/b")]
        self.assertEqual(harvest.slugs_in(lines, "Lever"),
                         collections.Counter({"wayve": 2}))


class TheQueryItself(unittest.TestCase):
    def test_it_asks_for_one_prefix_of_one_crawl(self):
        url = harvest.index_url("CC-MAIN-2026-30", "jobs.lever.co/", page=2)
        self.assertIn("CC-MAIN-2026-30-index", url)
        self.assertIn("url=jobs.lever.co%2F%2A", url)
        self.assertIn("output=json", url)
        self.assertIn("page=2", url)
        # A crawl record for a page that 404ed names a board that has gone.
        self.assertIn("filter=%3Dstatus%3A200", url)


class WhichCrawlToRead(unittest.TestCase):
    def test_the_newest_crawl_is_asked_for_rather_than_hardcoded(self):
        listing = ('[{"id":"CC-MAIN-2026-38","name":"September 2026"},'
                   ' {"id":"CC-MAIN-2026-30","name":"July 2026"}]')
        self.assertEqual(harvest.latest_crawl(lambda url: listing), "CC-MAIN-2026-38")

    def test_a_listing_that_will_not_load_returns_nothing_rather_than_a_guess(self):
        # A hardcoded crawl id works until it is retired and then fails
        # silently, which is the shape of failure this repository keeps meeting.
        def fetch(url):
            raise OSError("no route")

        self.assertEqual(harvest.latest_crawl(fetch), "")
        self.assertEqual(harvest.latest_crawl(lambda url: "not json"), "")
        self.assertEqual(harvest.latest_crawl(lambda url: '[{"id":"OTHER-1"}]'), "")


class HarvestingWithoutTheNetwork(unittest.TestCase):
    def test_it_collects_per_provider_and_drops_the_barely_seen(self):
        pages = {
            "boards.greenhouse.io/": [record("https://boards.greenhouse.io/stripe/jobs/1"),
                                      record("https://boards.greenhouse.io/stripe/jobs/2"),
                                      record("https://boards.greenhouse.io/typo1/jobs/3")],
            "jobs.lever.co/": [record("https://jobs.lever.co/wayve/a"),
                               record("https://jobs.lever.co/wayve/b")],
        }

        def fetch(url):
            import urllib.parse
            asked = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["url"][0]
            return "\n".join(pages.get(asked.rstrip("*"), []))

        found = harvest.harvest("CC-MAIN-2026-30", fetch, pages=1, seen_at_least=2)
        self.assertEqual(dict(found["Greenhouse"]), {"stripe": 2})
        self.assertEqual(dict(found["Lever"]), {"wayve": 2})
        # Seen once is as likely to be a typo as a company.
        self.assertNotIn("typo1", found["Greenhouse"])

    def test_a_page_that_will_not_load_costs_that_prefix_not_the_run(self):
        def fetch(url):
            if "lever" in url:
                raise OSError("index is down")
            if "job-boards" in url:
                return ""          # only one of Greenhouse's two prefixes answers
            return record("https://boards.greenhouse.io/stripe/jobs/1") + "\n" + \
                   record("https://boards.greenhouse.io/stripe/jobs/2")

        found = harvest.harvest("CC-MAIN-2026-30", fetch, pages=1, seen_at_least=2)
        self.assertEqual(dict(found["Greenhouse"]), {"stripe": 2})
        self.assertEqual(dict(found["Lever"]), {})


class FilingTheHarvest(unittest.TestCase):
    def test_the_best_attested_boards_are_taken_first(self):
        found = {"Lever": collections.Counter({"rare": 2, "common": 900, "middling": 50})}
        store = {}
        added = harvest.add_to(store, found, "2026-09-21", cap=2)
        self.assertEqual(added, ["Lever/common", "Lever/middling"])

    def test_the_cap_holds(self):
        found = {"Ashby": collections.Counter({f"co{n}": 100 - n for n in range(50)})}
        store = {}
        self.assertEqual(len(harvest.add_to(store, found, "2026-09-21", cap=10)), 10)
        self.assertEqual(len(store["Ashby"]), 10)

    def test_a_board_already_known_is_not_filed_twice(self):
        found = {"Lever": collections.Counter({"wayve": 900})}
        store = {}
        added = harvest.add_to(store, found, "2026-09-21",
                               known={("Lever", "wayve")})
        self.assertEqual(added, [])
        self.assertEqual(store, {})

    def test_it_carries_the_evidence_for_itself(self):
        found = {"Ashby": collections.Counter({"zoox": 42})}
        store = {}
        harvest.add_to(store, found, "2026-09-21")
        entry = store["Ashby"]["zoox"]
        self.assertEqual(entry["crawl_seen"], 42)
        self.assertTrue(entry["from_crawl"])
        # No posting taught us this one, so there is no company name to take.
        self.assertEqual(entry["name"], "Zoox")
        self.assertEqual(entry["misses"], 0)

    def test_a_second_harvest_updates_the_count_without_resetting_the_board(self):
        store = {"Ashby": {"zoox": {"name": "Zoox", "misses": 3, "roles": 9,
                                    "crawl_seen": 10}}}
        harvest.add_to(store, {"Ashby": collections.Counter({"zoox": 88})},
                       "2026-09-22")
        entry = store["Ashby"]["zoox"]
        self.assertEqual(entry["crawl_seen"], 88)
        # Its polling history is the discovery store's business, not this one's.
        self.assertEqual(entry["misses"], 3)
        self.assertEqual(entry["roles"], 9)


class TheWatcherActuallyRunsIt(unittest.TestCase):
    def test_the_harvest_is_wired_in_and_capped(self):
        from pathlib import Path

        source = (Path(harvest.__file__).resolve().parent
                  / "internship_watcher.py").read_text(encoding="utf-8")
        self.assertIn("board_harvest.latest_crawl", source)
        self.assertIn("board_harvest.harvest(crawl", source)
        self.assertIn("cap=1000", source)
        # Every board already known is excluded, or the same company is polled
        # twice and every row it carries is counted twice.
        self.assertIn("known=already", source)
        # And it can be turned off from the workflow without editing code.
        self.assertIn('os.environ.get("HARVEST_BOARDS"', source)

    def test_the_pool_grew_with_the_board_count(self):
        from pathlib import Path

        source = (Path(harvest.__file__).resolve().parent
                  / "internship_watcher.py").read_text(encoding="utf-8")
        # 433 boards twelve at a time was comfortable; two thousand is not, and
        # the daily job has twenty minutes.
        self.assertIn("max_workers=min(32,", source)


class ItOnlyClaimsProvidersTheWatcherCanRead(unittest.TestCase):
    def test_no_prefix_is_listed_without_a_parser_behind_it(self):
        import board_discovery

        self.assertEqual(set(harvest.PREFIXES), set(board_discovery.POLLABLE))


if __name__ == "__main__":
    unittest.main()
