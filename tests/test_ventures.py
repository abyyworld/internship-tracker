"""The venture dataset and its matcher.

The dataset is the product here, so most of this is integrity: an entry that
looks complete but says nothing actionable is worse than a missing one, and a
date written into a cycle string is a promise that goes stale.
"""

import json
from pathlib import Path
import re
import unittest

import ventures


DATA = json.loads(
    (Path(__file__).resolve().parent.parent / "data" / "ventures.json").read_text(
        encoding="utf-8"
    )
)
PROGRAMMES = DATA["programmes"]


class DatasetTests(unittest.TestCase):
    def test_every_programme_is_complete_enough_to_act_on(self):
        for programme in PROGRAMMES:
            with self.subTest(programme.get("id")):
                for field in (
                    "id", "name", "organisation", "kind", "gives", "equity",
                    "eligibility", "cycle", "url",
                ):
                    self.assertTrue(
                        str(programme.get(field, "")).strip(),
                        f"{programme.get('id')} is missing {field}",
                    )
                self.assertTrue(programme["stage"], "no stage listed")
                self.assertTrue(programme["audience"], "no audience listed")
                self.assertTrue(programme["regions"], "no regions listed")

    def test_ids_are_unique_and_urls_are_https(self):
        ids = [programme["id"] for programme in PROGRAMMES]
        self.assertEqual(len(ids), len(set(ids)))
        for programme in PROGRAMMES:
            self.assertTrue(programme["url"].startswith("https://"), programme["id"])

    def test_kinds_stages_and_audiences_stay_within_the_vocabulary(self):
        # The dashboard builds its filters from these, so a typo silently
        # creates a category of one.
        for programme in PROGRAMMES:
            with self.subTest(programme["id"]):
                self.assertIn(programme["kind"], ventures.KINDS)
                for stage in programme["stage"]:
                    self.assertIn(stage, ventures.STAGE_ORDER)
                for audience in programme["audience"]:
                    self.assertIn(audience, ventures.AUDIENCES)

    def test_no_cycle_pins_itself_to_a_date_that_will_go_stale(self):
        # Cohort dates move every year. Each entry describes the shape of the
        # cycle and links to the page that governs it.
        for programme in PROGRAMMES:
            with self.subTest(programme["id"]):
                self.assertNotRegex(programme["cycle"], r"\b20\d\d\b")
                self.assertNotRegex(
                    programme["cycle"],
                    r"\b\d{1,2}(st|nd|rd|th)?\s+(January|February|March|April|May|"
                    r"June|July|August|September|October|November|December)\b",
                )

    def test_equity_free_programmes_say_so_in_a_way_the_filter_can_read(self):
        free = [p for p in PROGRAMMES if ventures.takes_no_equity(p)]
        self.assertGreaterEqual(len(free), 8)
        for programme in free:
            self.assertTrue(programme["equity"].lower().startswith("none"))
        # And a programme that takes equity must never be read as free.
        yc = next(p for p in PROGRAMMES if p["id"] == "y-combinator")
        self.assertFalse(ventures.takes_no_equity(yc))


class MatchingTests(unittest.TestCase):
    def test_a_uk_phd_sees_the_programmes_written_for_them_first(self):
        matches = ventures.match_programmes(audience="phd", region="GB")
        names = [programme["name"] for programme in matches]
        self.assertIn("Conception X", names)
        # Ranked ahead of the global accelerators that accept everyone.
        self.assertLess(names.index("Conception X"), names.index("Y Combinator"))
        # And a US-only student scholarship is not shown to them at all.
        self.assertNotIn("Neo Scholars", names)

    def test_a_region_filter_keeps_global_programmes(self):
        matches = ventures.match_programmes(region="GB")
        names = [programme["name"] for programme in matches]
        self.assertIn("Start Up Loans", names)
        self.assertIn("Y Combinator", names)  # listed as global

    def test_asking_for_no_equity_removes_every_accelerator_that_takes_it(self):
        matches = ventures.match_programmes(equity_free_only=True)
        self.assertTrue(matches)
        for programme in matches:
            self.assertTrue(ventures.takes_no_equity(programme))

    def test_stage_filters_to_programmes_that_accept_that_stage(self):
        pre_team = ventures.match_programmes(stage="pre-team")
        names = [programme["name"] for programme in pre_team]
        self.assertIn("Entrepreneur First", names)
        self.assertNotIn("Techstars Accelerator", names)

    def test_anyone_means_everything_rather_than_nothing(self):
        self.assertEqual(
            len(ventures.match_programmes(audience="anyone")), len(PROGRAMMES)
        )

    def test_a_broken_entry_is_dropped_rather_than_half_shown(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ventures.json"
            path.write_text(json.dumps({"programmes": [
                {"id": "good", "name": "Good", "kind": "grant", "url": "https://x.test",
                 "eligibility": "anyone", "cycle": "rolling"},
                {"id": "no-url", "name": "Bad", "kind": "grant", "url": "",
                 "eligibility": "anyone", "cycle": "rolling"},
                {"id": "insecure", "name": "Bad", "kind": "grant",
                 "url": "http://x.test", "eligibility": "anyone", "cycle": "rolling"},
                {"id": "", "name": "Bad", "kind": "grant", "url": "https://x.test",
                 "eligibility": "anyone", "cycle": "rolling"},
            ]}), encoding="utf-8")
            loaded = ventures.load_programmes(path)
            self.assertEqual([p["id"] for p in loaded], ["good"])

    def test_a_missing_dataset_is_not_a_crash(self):
        self.assertEqual(ventures.load_programmes(Path("/nonexistent.json")), [])


class ReportTests(unittest.TestCase):
    def test_the_report_names_what_it_costs_and_where_to_apply(self):
        text = ventures.report(audience="students", region="GB")
        self.assertIn("no equity", text)
        self.assertIn("https://", text)
        self.assertIn("cycle", text)

    def test_summary_counts_by_kind_and_by_cost(self):
        counts = ventures.summary(ventures.match_programmes())
        self.assertEqual(counts["total"], len(PROGRAMMES))
        self.assertGreater(counts["no_equity"], 0)
        self.assertGreater(counts["accelerator"], 0)


if __name__ == "__main__":
    unittest.main()
