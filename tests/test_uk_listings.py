"""UK listings, which are the only things here that know when they close.

Two gaps turned out to be one. UK coverage was 230 rows of 4,548 — 5% — for an
applicant whose Student visa makes them free to hire in the UK and nowhere
else. And twelve of those 4,548 rows carried a deadline, every one a finance
spring week written as "Oct-Nov 2026", which no filter can read.

Both follow from where the data comes from: the ATS APIs this scrapes serve
mostly US startups, and none of them publishes a closing date, because a
rolling posting has not got one. UK graduate schemes open on a date and close
on a date. So these rows come from the listing sites that track them, parsed
out of text rather than scraped.

The date is the one thing these tests are strict about. Everything else can be
missing; a row whose closing date cannot be read is dropped, because an undated
row in a deadline-driven lane reads as "no rush".
"""

from pathlib import Path
import json
import tempfile
import unittest

import uk_listings as uk


class ReadingADate(unittest.TestCase):
    def test_both_shapes_a_listing_site_writes(self):
        self.assertEqual(uk.as_date("15 Sep 26"), "2026-09-15")
        self.assertEqual(uk.as_date("September 25th, 2026"), "2026-09-25")
        self.assertEqual(uk.as_date("1 Jun 26"), "2026-06-01")
        self.assertEqual(uk.as_date("March 4, 2027"), "2027-03-04")
        self.assertEqual(uk.as_date("2026-11-30"), "2026-11-30")

    def test_a_two_digit_year_is_this_century(self):
        # Read as 1926, a live programme files as a century closed and
        # disappears from every filter without anyone noticing.
        self.assertEqual(uk.as_date("31 Jan 27"), "2027-01-31")

    def test_what_is_not_a_date_returns_nothing_rather_than_a_guess(self):
        for text in ("", "Rolling", "Oct–Nov 2026", "TBC", "Today",
                     "31 Sep 26", "soon", "Various"):
            self.assertEqual(uk.as_date(text), "", text)


class ParsingWhatAReaderCopies(unittest.TestCase):
    def test_a_tab_separated_row_with_both_dates(self):
        line = "Shell\tAssessed Internship Programme 2027\t15 Sep 26\t31 Jan 27\t10 Sep 25\t\tYes"
        row, = uk.parse_trackr(line)
        self.assertEqual(row["company"], "Shell")
        self.assertEqual(row["role"], "Assessed Internship Programme 2027")
        self.assertEqual(row["opens"], "2026-09-15")
        self.assertEqual(row["deadline"], "2027-01-31")
        self.assertEqual(row["sponsors_visa"], "yes")
        self.assertEqual(row["source"], "The Trackr")

    def test_a_row_with_an_opening_date_but_no_closing_one_is_dropped(self):
        # Most of that list is like this, and every one of them would read as
        # a live opportunity with no urgency attached.
        self.assertEqual(uk.parse_trackr("Amazon\t2027 SDE Intern\t21 Sep 26"), [])

    def test_a_listing_block_with_its_own_columns(self):
        line = ("Airbus|Software Developer (Full-Stack) Placement|September 27th, 2026|"
                "£24,500|Portsmouth|13 months|July 2027")
        row, = uk.parse_gradcracker(line)
        self.assertEqual(row["company"], "Airbus")
        self.assertEqual(row["deadline"], "2026-09-27")
        self.assertEqual(row["salary"], "£24,500")
        self.assertEqual(row["location"], "Portsmouth")
        self.assertEqual(row["duration"], "13 months")
        self.assertEqual(row["starts"], "July 2027")
        self.assertEqual(row["source"], "Gradcracker")

    def test_a_short_block_is_read_as_far_as_it_goes(self):
        row, = uk.parse_gradcracker("Zurich|Summer Internship 2027|18 Oct 26")
        self.assertEqual(row["deadline"], "2026-10-18")
        self.assertEqual(row["location"], "UK")     # nothing said, so nothing claimed
        self.assertEqual(row["salary"], "")

    def test_headers_and_blank_lines_are_not_rows(self):
        text = "\n".join(["", "Company\tProgramme\tOpening\tClosing", "   ",
                          "Shell\tInternship\t15 Sep 26\t31 Jan 27"])
        self.assertEqual(len(uk.parse_trackr(text)), 1)


class MergingTwoSites(unittest.TestCase):
    def test_the_same_scheme_in_two_cities_is_two_placements(self):
        rows = uk.parse_gradcracker(
            "Barclays|2027 Technology Developer Summer Internship Programme|"
            "September 25th, 2026|Competitive|London|10 weeks|June 2027\n"
            "Barclays|2027 Technology Developer Summer Internship Programme|"
            "September 25th, 2026|Competitive|Glasgow|10 weeks|June 2027")
        self.assertEqual(len(uk.merge(rows)), 2)

    def test_the_same_row_from_both_sites_is_one_row(self):
        trackr = uk.parse_trackr("Zurich\tSummer Internship 2027\t09 Sep 26\t18 Oct 26\t\t\tNo")
        grad = uk.parse_gradcracker("Zurich|Summer Internship 2027|18 Oct 26||UK||")
        merged = uk.merge(trackr, grad)
        self.assertEqual(len(merged), 1)

    def test_merging_keeps_whatever_either_site_knew(self):
        # The two carry different columns: one says whether the visa is
        # sponsored, the other says what it pays.
        trackr = uk.parse_trackr("Airbus\tSoftware Developer Placement\t01 Sep 26\t27 Sep 26\t\t\tYes")
        grad = uk.parse_gradcracker(
            "Airbus|Software Developer Placement|September 27th, 2026|£24,500|UK|13 months|July 2027")
        row, = uk.merge(trackr, grad)
        self.assertEqual(row["sponsors_visa"], "yes")
        self.assertEqual(row["salary"], "£24,500")
        self.assertEqual(row["duration"], "13 months")

    def test_they_come_back_soonest_to_close_first(self):
        rows = uk.merge(uk.parse_gradcracker(
            "B|Later|December 1st, 2026\nA|Sooner|October 1st, 2026"))
        self.assertEqual([row["role"] for row in rows], ["Sooner", "Later"])


class WhatIsOnDisk(unittest.TestCase):
    def test_a_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "uk.json"
            rows = uk.parse_gradcracker("Airbus|AI Placement|September 27th, 2026")
            uk.save(rows, path)
            self.assertEqual(uk.load(path), rows)

    def test_a_missing_or_broken_file_costs_the_listings_not_the_run(self):
        self.assertEqual(uk.load(Path("/nonexistent.json")), [])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "uk.json"
            path.write_text("{not json", encoding="utf-8")
            self.assertEqual(uk.load(path), [])

    def test_a_row_that_lost_its_date_is_not_loaded(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "uk.json"
            path.write_text(json.dumps([
                {"company": "A", "role": "R", "deadline": "2026-10-01"},
                {"company": "B", "role": "R", "deadline": "Rolling"},
                {"company": "C", "role": "R"},
            ]), encoding="utf-8")
            self.assertEqual([row["company"] for row in uk.load(path)], ["A"])

    def test_the_shipped_file_is_dated_throughout(self):
        rows = uk.load()
        self.assertGreater(len(rows), 30, "the UK listings have not been seeded")
        for row in rows:
            self.assertTrue(uk.as_date(row["deadline"]),
                            f"{row['company']} {row['role']} has no readable date")


class TheWatcherCarriesThem(unittest.TestCase):
    def test_they_are_filed_with_their_date_and_closed_when_past(self):
        source = (Path(uk.__file__).resolve().parent
                  / "internship_watcher.py").read_text(encoding="utf-8")
        self.assertIn("uk_listings.load()", source)
        self.assertIn('"uk_listings"', source)
        # A date already past is not a live posting.
        self.assertIn('"open" if closes >= TODAY else "closed"', source)
        # And the visa answer is carried, since for this reader it decides
        # whether an application is worth making at all.
        self.assertIn('sponsorship=listing.get("sponsors_visa"', source)


if __name__ == "__main__":
    unittest.main()
