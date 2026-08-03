"""Funding schemes and university reference data."""

import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlparse

import scorecard
from funding import LEVEL_ORDER, load_schemes, match_schemes, normalise_level, summary


UNDERGRAD_UZ = {
    "education": {"level": "undergraduate", "graduation_year": "2028"},
    "citizenships": ["UZ"],
}
PHD_US = {"education": {"level": "phd"}, "citizenships": ["US"]}


class SchemeDataTests(unittest.TestCase):
    def setUp(self):
        self.schemes = load_schemes()

    def test_schemes_are_present(self):
        self.assertGreaterEqual(len(self.schemes), 20)

    def test_every_scheme_is_complete_and_https(self):
        for scheme in self.schemes:
            for field in ("id", "name", "funder", "levels", "eligibility", "url"):
                self.assertTrue(scheme.get(field), f"{scheme.get('id')} missing {field}")
            self.assertEqual(urlparse(scheme["url"]).scheme, "https", scheme["id"])

    def test_levels_use_the_known_vocabulary(self):
        for scheme in self.schemes:
            for level in scheme["levels"]:
                self.assertIn(normalise_level(level), LEVEL_ORDER, scheme["id"])

    def test_ids_are_unique(self):
        ids = [scheme["id"] for scheme in self.schemes]
        self.assertEqual(len(ids), len(set(ids)))

    def test_no_scheme_stores_a_hard_deadline_date(self):
        # Deadlines move every year; a stale date shown as fact is worse than
        # none, so only the usual window is recorded.
        for scheme in self.schemes:
            self.assertNotIn("deadline_date", scheme, scheme["id"])
            self.assertNotRegex(scheme.get("cycle", ""), r"\b20\d\d\b", scheme["id"])


class MatchingTests(unittest.TestCase):
    def test_an_undergraduate_sees_what_is_open_now_and_next(self):
        matches = match_schemes(UNDERGRAD_UZ)
        now = [m["id"] for m in matches if m["timing"] == "now"]
        nxt = [m["id"] for m in matches if m["timing"] == "next"]
        self.assertIn("daad-rise", now)
        self.assertIn("mitacs-globalink", now)
        # Master's funding closes a year before the course starts, so it has to
        # surface while they are still an undergraduate.
        self.assertIn("chevening", nxt)

    def test_us_only_schemes_are_marked_blocked_for_others(self):
        blocked = {m["id"] for m in match_schemes(UNDERGRAD_UZ) if m["blocked"]}
        self.assertIn("nsf-grfp", blocked)
        allowed = {m["id"] for m in match_schemes(PHD_US) if not m["blocked"]}
        self.assertIn("nsf-grfp", allowed)

    def test_blocked_schemes_say_why(self):
        for match in match_schemes(UNDERGRAD_UZ):
            if match["blocked"]:
                self.assertTrue(match["blocked_reason"])

    def test_a_phd_student_sees_phd_funding_as_current(self):
        now = {m["id"] for m in match_schemes(PHD_US) if m["timing"] == "now"}
        self.assertIn("google-phd", now)

    def test_blocked_and_past_schemes_sort_last(self):
        matches = match_schemes(UNDERGRAD_UZ)
        first_blocked = next(
            (i for i, m in enumerate(matches) if m["blocked"]), len(matches)
        )
        self.assertTrue(all(not m["blocked"] for m in matches[:first_blocked]))

    def test_a_profile_without_a_level_still_returns_everything(self):
        self.assertEqual(len(match_schemes({})), len(load_schemes()))

    def test_summary_counts_add_up(self):
        matches = match_schemes(UNDERGRAD_UZ)
        figures = summary(matches)
        self.assertEqual(figures["total"], len(matches))
        self.assertGreater(figures["now"], 0)


class ScorecardTests(unittest.TestCase):
    def setUp(self):
        self.index = scorecard.index()

    def test_the_cache_is_populated(self):
        self.assertGreater(len(self.index), 100)

    def test_names_normalise_past_the_usual_noise(self):
        self.assertEqual(
            scorecard.normalise("The University of Maryland at College Park"),
            scorecard.normalise("University of Maryland - College Park"),
        )

    def test_a_known_institution_is_found_with_plausible_figures(self):
        row = scorecard.lookup("University of Maryland - College Park", self.index)
        self.assertIsNotNone(row)
        self.assertTrue(0 < row["admission_rate"] <= 1)
        self.assertGreater(row["students"], 1000)

    def test_an_unknown_name_returns_nothing_rather_than_a_guess(self):
        self.assertIsNone(scorecard.lookup("Hogwarts", self.index))
        self.assertIsNone(scorecard.lookup("", self.index))

    def test_the_description_reads_as_figures_not_code(self):
        row = scorecard.lookup("University of Maryland - College Park", self.index)
        text = scorecard.describe(row)
        self.assertIn("% admitted", text)
        self.assertIn("students", text)

    def test_a_missing_cache_degrades_quietly(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "none.json"
            self.assertEqual(scorecard.load_cache(path)["institutions"], [])

    def test_a_corrupt_cache_degrades_quietly(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{oops", encoding="utf-8")
            self.assertEqual(scorecard.load_cache(path)["institutions"], [])

    def test_larger_campuses_win_a_name_collision(self):
        built = scorecard.index({"institutions": [
            {"id": 1, "name": "Example State", "key": "example state", "students": 500},
            {"id": 2, "name": "Example State", "key": "example state", "students": 40000},
        ]})
        self.assertEqual(built["example state"]["id"], 2)


if __name__ == "__main__":
    unittest.main()
