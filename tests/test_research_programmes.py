"""A funded research programme is not a job posting, and that is why it was missing.

A posting is rolling: it appears, it sits there, it closes quietly and the
tracker notices within a run or two. A programme opens on a fixed date, closes
on a fixed date, and is then gone for a year. Nothing in this repository could
express that — 3,302 rows carried twelve deadlines between them, every one a
finance spring week written as "Oct-Nov 2026", which is not a date a filter can
read. So the entire funded-research lane, the one that actually leads to a PhD
and that handles the visa as part of its own process, was invisible here.

These tests pin the two halves of the fix: the loader that refuses a programme
it cannot state a deadline for, and the dashboard's willingness to carry a
record that is not a posting.
"""

from pathlib import Path
import csv
import json
import tempfile
import unittest
from unittest.mock import patch

import dashboard
import internship_watcher as watcher


class OnlyProgrammesWeCanDateGetIn(unittest.TestCase):
    def write(self, listed):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                             encoding="utf-8")
        json.dump(listed, handle)
        handle.close()
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return handle.name

    def test_a_dated_programme_is_kept(self):
        path = self.write([{
            "name": "CMU Robotics Institute Summer Scholars",
            "host": "Carnegie Mellon University",
            "url": "https://riss.ri.cmu.edu/",
            "deadline": "2027-01-21",
        }])
        self.assertEqual(len(watcher.load_research_programmes(path)), 1)

    def test_a_programme_with_no_deadline_is_dropped(self):
        # Worse than absent: it reads as covered, and leaves the reader to
        # find out for themselves when it closes. Which is the failure that
        # started this — a deadline missed by five days costs a year.
        path = self.write([{"name": "Some Programme", "url": "https://x.test/",
                            "deadline": ""}])
        self.assertEqual(watcher.load_research_programmes(path), [])

    def test_a_programme_with_no_url_is_dropped(self):
        path = self.write([{"name": "Some Programme", "url": "",
                            "deadline": "2027-01-21"}])
        self.assertEqual(watcher.load_research_programmes(path), [])

    def test_a_missing_or_broken_file_costs_the_programmes_not_the_run(self):
        # This file is edited by hand and by a scheduled job. A half-written
        # one must not stop the tracker refreshing three thousand postings.
        self.assertEqual(watcher.load_research_programmes("/nonexistent.json"), [])
        broken = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                             encoding="utf-8")
        broken.write("{not json")
        broken.close()
        self.addCleanup(lambda: Path(broken.name).unlink(missing_ok=True))
        self.assertEqual(watcher.load_research_programmes(broken.name), [])

    def test_the_shipped_file_is_readable_and_every_entry_is_dated(self):
        listed = json.loads(
            (Path(watcher.__file__).resolve().parent
             / "data" / "research_programmes.json").read_text(encoding="utf-8"))
        self.assertIsInstance(listed, list)
        for entry in listed:
            self.assertTrue(entry.get("deadline"), f"{entry.get('name')} has no deadline")
            self.assertTrue(entry.get("url"), f"{entry.get('name')} has no url")
            # Each field is a claim checked against the programme's own page on
            # a particular day, so it says how sure it is and what it read.
            self.assertIn(entry.get("deadline_confidence"),
                          {"verified-2027", "previous-round", "unknown"},
                          f"{entry.get('name')} does not say how sure the date is")
            self.assertTrue(entry.get("evidence"), f"{entry.get('name')} cites nothing")


class TheDashboardCarriesThem(unittest.TestCase):
    def test_a_programme_row_reaches_the_page(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tracker = root / "tracker.csv"
            output = root / "docs" / "index.html"
            fields = ["id", "company", "role", "category", "region", "record_kind",
                      "source_status", "url", "company_type", "deadline", "term"]
            with tracker.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow({
                    "id": "riss", "company": "Carnegie Mellon University",
                    "role": "Robotics Institute Summer Scholars",
                    "category": "Robotics & Embodied AI", "region": "US",
                    "record_kind": "programme", "source_status": "open",
                    "url": "https://riss.ri.cmu.edu/",
                    "company_type": "university",
                    "deadline": "2027-01-21", "term": "Summer 2027",
                })
            with patch.object(dashboard, "TRACKER", tracker), \
                 patch.object(dashboard, "OUTPUT", output):
                self.assertEqual(dashboard.build(), 1)
            page = output.read_text(encoding="utf-8")
            self.assertIn("Robotics Institute Summer Scholars", page)
            # The date has to survive the trip, or the filter built for it has
            # nothing to filter.
            self.assertIn("2027-01-21", page)

    def test_a_watchlist_row_still_does_not(self):
        # Widening the door for programmes must not let the career-hub entries
        # through as if they were opportunities with dates.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tracker = root / "tracker.csv"
            output = root / "docs" / "index.html"
            fields = ["id", "company", "role", "category", "region", "record_kind",
                      "source_status", "url", "company_type"]
            with tracker.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow({
                    "id": "hub", "company": "Amazon", "role": "→ Student Programs",
                    "category": "Software Engineering", "region": "Global",
                    "record_kind": "watchlist", "source_status": "watchlist",
                    "url": "https://www.amazon.jobs/", "company_type": "unknown",
                })
            with patch.object(dashboard, "TRACKER", tracker), \
                 patch.object(dashboard, "OUTPUT", output):
                self.assertEqual(dashboard.build(), 0)


class TheWatcherKnowsWhatAProgrammeIs(unittest.TestCase):
    def test_it_is_filed_as_a_programme_rather_than_a_posting(self):
        source = Path(watcher.__file__).read_text(encoding="utf-8")
        self.assertIn('record_kind="programme"', source)
        self.assertIn('role_type="research programme"', source)
        self.assertIn("load_research_programmes()", source)
        # The eligibility line is a checked finding, not the "review required"
        # every posting gets by default.
        self.assertIn('eligibility=programme.get("eligibility_note", "")', source)


if __name__ == "__main__":
    unittest.main()
