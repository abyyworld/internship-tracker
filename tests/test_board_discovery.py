"""The source list has to grow by itself, or it stops growing.

A hand-written list of company boards is a ceiling, and the tracker was sitting
under it: 147 boards polled while 690 board addresses sat unread in the URLs of
rows already collected. These tests pin the behaviour that closes that gap and,
just as importantly, the behaviour that keeps it honest — a slug taken from a
URL's plumbing, or a board polled twice because it is also curated, would both
show up as coverage while doing nothing.
"""

from pathlib import Path
import json
import tempfile
import unittest

import board_discovery as bd


class ReadingTheBoardOutOfAUrl(unittest.TestCase):
    def test_every_shape_these_providers_publish(self):
        cases = {
            "https://boards.greenhouse.io/figureai/jobs/4012345": ("Greenhouse", "figureai"),
            "https://job-boards.greenhouse.io/nuro/jobs/5566": ("Greenhouse", "nuro"),
            "https://boards-api.greenhouse.io/v1/boards/skydio/jobs": ("Greenhouse", "skydio"),
            "https://boards.greenhouse.io/embed/job_board?for=anduril": ("Greenhouse", "anduril"),
            "https://jobs.lever.co/anybotics/9f3a-77": ("Lever", "anybotics"),
            "https://api.lever.co/v0/postings/wayve?mode=json": ("Lever", "wayve"),
            "https://jobs.ashbyhq.com/zoox/12345678-1234": ("Ashby", "zoox"),
            "https://api.ashbyhq.com/posting-api/job-board/1x": ("Ashby", "1x"),
            "https://wd1.myworkdaysite.com/recruiting/wf/Jobs/job/X": ("Workday", "wd1"),
        }
        for url, expected in cases.items():
            self.assertEqual(bd.slug_from(url), expected, url)

    def test_the_url_plumbing_is_not_a_company(self):
        # A board named "embed" or "jobs" would be polled every day forever and
        # never answer, and the coverage count would quietly include it.
        for url in ("https://boards.greenhouse.io/embed/job_board",
                    "https://jobs.lever.co/",
                    "https://example.com/careers/software-engineer",
                    ""):
            self.assertIsNone(bd.slug_from(url), url)

    def test_a_url_that_names_no_board_is_not_forced_into_one(self):
        self.assertIsNone(bd.slug_from(
            "https://wd1.myworkdaysite.com/recruiting/wf/Jobs/job/CHARLOTTE-NC/"
            "XMLNAME-2027-Quantitative-Analytics-Summer-Internship-Risk-Analytics-"
            "and-Decision-Sciences--RADS-PhD----Early-Careers_R-569912".replace(
                "wd1.myworkdaysite.com", "example.com"))
        )


class RememberingWhatWeMet(unittest.TestCase):
    def test_a_posting_teaches_us_its_board(self):
        store = {}
        added = bd.harvest([("https://jobs.ashbyhq.com/zoox/abc", "Zoox")],
                           store, "2026-09-21")
        self.assertEqual(added, 1)
        self.assertEqual(store["Ashby"]["zoox"]["name"], "Zoox")

    def test_the_company_name_comes_from_the_posting_not_the_slug(self):
        # "sambanovasystems" is not what anybody calls SambaNova Systems, and
        # the tracker shows this string to a reader as the employer.
        store = {}
        bd.harvest([("https://boards.greenhouse.io/sambanovasystems/jobs/1",
                     "SambaNova Systems")], store, "2026-09-21")
        self.assertEqual(store["Greenhouse"]["sambanovasystems"]["name"],
                         "SambaNova Systems")

    def test_a_slug_with_no_company_still_gets_a_readable_name(self):
        store = {}
        bd.harvest([("https://jobs.lever.co/applied-intuition/x", "")],
                   store, "2026-09-21")
        self.assertEqual(store["Lever"]["applied-intuition"]["name"],
                         "Applied Intuition")

    def test_a_board_already_curated_is_not_learned_again(self):
        # Polling the same board from both lists would double every row it
        # carries, which reads as a source doing twice the work it does.
        store = {}
        added = bd.harvest([("https://jobs.ashbyhq.com/zoox/abc", "Zoox")],
                           store, "2026-09-21", known={("Ashby", "zoox")})
        self.assertEqual(added, 0)
        self.assertEqual(store, {})

    def test_meeting_it_twice_is_not_two_boards(self):
        store = {}
        pairs = [("https://jobs.ashbyhq.com/zoox/a", "Zoox"),
                 ("https://jobs.ashbyhq.com/zoox/b", "Zoox")]
        self.assertEqual(bd.harvest(pairs, store, "2026-09-21"), 1)


class HandingThemToTheWatcher(unittest.TestCase):
    def test_curated_boards_are_left_out_of_the_discovered_list(self):
        store = {"Ashby": {"zoox": {"name": "Zoox"}, "1x": {"name": "1X"}}}
        given = bd.boards_for("Ashby", store, exclude={"zoox"})
        self.assertEqual(given, [("1x", "1X", "None")])

    def test_the_shape_is_the_one_collect_expects(self):
        store = {"Lever": {"wayve": {"name": "Wayve"}}}
        for slug, name, term in bd.boards_for("Lever", store):
            self.assertIsInstance(slug, str)
            self.assertIsInstance(name, str)
            self.assertEqual(term, "None")


class ForgettingWhatHasGone(unittest.TestCase):
    def test_a_board_that_answers_has_its_misses_cleared(self):
        store = {"Ashby": {"zoox": {"name": "Zoox", "misses": 3}}}
        bd.record(store, "Ashby", "zoox", 12, "2026-09-21")
        self.assertEqual(store["Ashby"]["zoox"]["misses"], 0)
        self.assertEqual(store["Ashby"]["zoox"]["roles"], 12)

    def test_one_bad_afternoon_does_not_lose_a_board(self):
        # Re-discovering a board costs a day of its postings, so a board is
        # given five runs to come back rather than one.
        store = {"Ashby": {"zoox": {"name": "Zoox", "misses": 0}}}
        for _ in range(4):
            bd.record(store, "Ashby", "zoox", None, "2026-09-21")
        self.assertEqual(bd.prune(store), [])
        self.assertIn("zoox", store["Ashby"])
        bd.record(store, "Ashby", "zoox", None, "2026-09-21")
        self.assertEqual(bd.prune(store), ["Ashby/zoox"])
        self.assertNotIn("zoox", store["Ashby"])


class WhatIsOnDisk(unittest.TestCase):
    def test_it_survives_a_round_trip_and_a_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "boards.json"
            self.assertEqual(bd.load(path), {})      # nothing there yet
            store = {"Ashby": {"zoox": {"name": "Zoox", "misses": 0}}}
            bd.save(store, path)
            self.assertEqual(bd.load(path), store)

    def test_a_corrupt_file_is_not_a_crash(self):
        # This file is written by a scheduled job and committed. A half-written
        # one must cost a day of discovery, not the whole run.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "boards.json"
            path.write_text("{not json", encoding="utf-8")
            self.assertEqual(bd.load(path), {})

    def test_it_is_written_sorted_so_the_daily_diff_is_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "boards.json"
            bd.save({"Lever": {"zzz": {"name": "Z"}, "aaa": {"name": "A"}}}, path)
            written = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(list(written["Lever"]), ["aaa", "zzz"])


class TheWatcherActuallyUsesIt(unittest.TestCase):
    def test_the_seeded_store_is_there_and_is_mostly_pollable_boards(self):
        store = bd.load()
        self.assertTrue(store, "data/discovered_boards.json has not been seeded")
        pollable = sum(len(bd.boards_for(p, store)) for p in bd.POLLABLE)
        self.assertGreater(pollable, 150,
                           "discovery should already be worth more than the curated list")

    def test_the_watcher_polls_the_discovered_boards_too(self):
        source = Path(bd.__file__).resolve().parent / "internship_watcher.py"
        text = source.read_text(encoding="utf-8")
        self.assertIn("board_discovery.harvest", text)
        self.assertIn('with_discovered(GREENHOUSE_BOARDS, "Greenhouse")', text)
        self.assertIn('with_discovered(ASHBY_BOARDS, "Ashby")', text)
        self.assertIn('with_discovered(LEVER_BOARDS, "Lever")', text)
        # And records what happened, or a dead board is polled forever.
        self.assertIn("board_discovery.record", text)
        self.assertIn("board_discovery.prune", text)

    def test_only_providers_the_watcher_can_read_are_called_pollable(self):
        # Workday and iCIMS addresses are recorded so the count is honest, but
        # nothing here can parse them — counting them as coverage would be a lie.
        self.assertEqual(set(bd.POLLABLE), {"Greenhouse", "Lever", "Ashby"})
        summary = bd.summary({"Workday": {"wd1": {}}, "Ashby": {"zoox": {}}})
        self.assertIn("recorded, not polled", summary)


if __name__ == "__main__":
    unittest.main()
