"""Whether a posting is worth this applicant's time."""

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from autoapply.fit import assess_fit, parse_term, read_postings


UNDERGRAD_2028 = {
    "education": {"graduation_year": "2028", "level": "undergraduate"},
    "citizenships": ["UZ"],
    "work_authorization": {
        "GB": {
            "authorized_now": True,
            "authorization_scope": "limited",
            "requires_sponsorship_now_or_future": True,
        },
        "US": {
            "authorized_now": "unknown",
            "requires_sponsorship_now_or_future": True,
        },
    },
}


def posting(**values):
    base = {"id": "j1", "url": "https://example.invalid/j1", "company": "Acme",
            "role": "Engineer", "region": "", "location": "", "term": "",
            "position_type": "intern"}
    base.update(values)
    return SimpleNamespace(**base)


class TermParsingTests(unittest.TestCase):
    def test_a_season_and_year_are_read(self):
        self.assertEqual(parse_term("Summer 2027"), (2027, 6))

    def test_a_split_season_starts_at_the_earlier_one(self):
        self.assertEqual(parse_term("Fall/Winter 2026"), (2026, 1))

    def test_labels_that_commit_to_nothing_return_nothing(self):
        for label in ("", "Unknown", "Ambiguous"):
            self.assertEqual(parse_term(label), (None, None))


class TimingTests(unittest.TestCase):
    def test_a_graduate_role_before_graduation_is_ruled_out(self):
        fit = assess_fit(
            posting(term="New Grad 2026", position_type="new-grad", region="US"),
            UNDERGRAD_2028,
        )
        self.assertEqual(fit.status, "mismatch")
        self.assertEqual(fit.timing, "too_early")
        self.assertIn("2028", fit.reasons[0])

    def test_a_graduate_role_after_graduation_is_not_ruled_out(self):
        fit = assess_fit(
            posting(term="New Grad 2028", position_type="new-grad", region="UK"),
            UNDERGRAD_2028,
        )
        self.assertEqual(fit.timing, "fits")
        self.assertNotEqual(fit.status, "mismatch")

    def test_an_internship_during_the_degree_fits(self):
        fit = assess_fit(
            posting(term="Summer 2027", position_type="intern", region="UK"),
            UNDERGRAD_2028,
        )
        self.assertEqual(fit.timing, "fits")
        self.assertEqual(fit.status, "apply")

    def test_an_intake_that_has_already_started_is_ruled_out(self):
        fit = assess_fit(
            posting(term="Summer 2025", position_type="intern", region="UK"),
            UNDERGRAD_2028,
            today_year=2026,
        )
        self.assertEqual(fit.timing, "stale")
        self.assertEqual(fit.status, "mismatch")

    def test_a_profile_without_a_graduation_year_rules_nothing_out(self):
        fit = assess_fit(
            posting(term="New Grad 2026", position_type="new-grad", region="UK"),
            {"work_authorization": {}},
        )
        self.assertEqual(fit.timing, "unknown")
        self.assertNotEqual(fit.status, "mismatch")


class AuthorisationTests(unittest.TestCase):
    def test_a_country_you_may_work_in_is_separated_from_one_you_may_not(self):
        uk = assess_fit(
            posting(term="Summer 2027", region="UK"), UNDERGRAD_2028
        )
        us = assess_fit(
            posting(term="Summer 2027", region="US"), UNDERGRAD_2028
        )
        self.assertEqual(uk.authorization, "limited")
        self.assertEqual(us.authorization, "sponsorship")
        self.assertEqual(uk.status, "apply")
        self.assertEqual(us.status, "sponsor")

    def test_limited_permission_still_says_what_to_check(self):
        fit = assess_fit(posting(term="Summer 2027", region="UK"), UNDERGRAD_2028)
        self.assertTrue(any("limited" in reason for reason in fit.reasons))

    def test_a_posting_spanning_countries_is_not_judged(self):
        fit = assess_fit(posting(term="Summer 2027", region="US / Canada"), UNDERGRAD_2028)
        self.assertEqual(fit.authorization, "unknown")
        self.assertEqual(fit.status, "check")

    def test_a_country_absent_from_the_profile_is_not_assumed_open(self):
        fit = assess_fit(posting(term="Summer 2027", region="Japan"), UNDERGRAD_2028)
        self.assertEqual(fit.authorization, "unknown")
        self.assertNotEqual(fit.status, "apply")


class TrackerReadingTests(unittest.TestCase):
    def test_only_open_postings_are_read(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tracker.csv"
            path.write_text(
                "id,url,company,role,region,location,term,role_type,"
                "record_kind,source_status\n"
                "a,https://x.invalid/a,Acme,Dev,UK,London,Summer 2027,intern,posting,open\n"
                "b,https://x.invalid/b,Acme,Dev,UK,London,Summer 2027,intern,posting,closed\n"
                "c,https://x.invalid/c,Acme,Dev,UK,London,Summer 2027,intern,note,open\n",
                encoding="utf-8",
            )
            postings = read_postings(path)
            self.assertEqual([p.id for p in postings], ["a"])
            self.assertEqual(postings[0].position_type, "intern")


if __name__ == "__main__":
    unittest.main()
