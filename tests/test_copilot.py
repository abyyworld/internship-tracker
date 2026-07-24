import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import copilot


def posting(**updates):
    row = {
        "id": "role-1",
        "company": "Example Robotics",
        "role": "Machine Learning Engineer Intern",
        "category": "Robotics & Embodied AI",
        "focus_tags": "robot learning",
        "robotics_focus": "embodied AI",
        "company_type": "startup",
        "equity_signal": "private company; verify offer",
        "eligibility": "review required",
        "region": "UK",
        "location": "London, UK",
        "term": "Summer 2027",
        "level": "Undergraduate eligible",
        "role_type": "intern",
        "citizenship": "unknown",
        "sponsorship": "unknown",
        "elite_tier": "high",
        "deadline": "",
        "source_status": "open",
        "record_kind": "posting",
        "url": "https://jobs.ashbyhq.com/example/12345678-1234-1234-1234-123456789abc",
    }
    row.update(updates)
    return row


class UrlAndReadinessTests(unittest.TestCase):
    def test_application_url_allows_only_absolute_http_urls(self):
        self.assertEqual(
            copilot.safe_application_url(" https://jobs.example.com/apply "),
            "https://jobs.example.com/apply",
        )
        for value in (
            "",
            "javascript:alert(1)",
            "data:text/html,boom",
            "file:///tmp/private",
            "//jobs.example.com/apply",
            "https:///missing-host",
        ):
            with self.subTest(value=value):
                self.assertEqual(copilot.safe_application_url(value), "")

    def test_unreviewed_role_cannot_enter_approved_queue(self):
        _fit, reasons, tab = copilot.score_role(posting())
        self.assertEqual(tab, "needs_work")
        self.assertTrue(any("need your review" in reason for reason in reasons))

    def test_verified_eligibility_can_approve(self):
        _fit, _reasons, tab = copilot.score_role(
            posting(eligibility="verified eligible")
        )
        self.assertEqual(tab, "ready")

    def test_legacy_public_manual_status_is_not_treated_as_approval(self):
        _fit, _reasons, tab = copilot.score_role(posting(my_status="approved"))
        self.assertEqual(tab, "needs_work")

    def test_hard_gates_override_title_relevance_and_manual_status(self):
        cases = (
            {"url": "javascript:alert(1)", "eligibility": "verified eligible"},
            {"citizenship": "US only", "eligibility": "verified eligible"},
            {"level": "PhD", "eligibility": "verified eligible"},
            {"level": "MSc", "eligibility": "verified eligible"},
            {"level": "Masters", "eligibility": "verified eligible"},
            {"level": "Advanced/unknown", "eligibility": "verified eligible"},
            {"role_type": "graduate", "eligibility": "verified eligible"},
            {"role_type": "new-grad", "eligibility": "verified eligible"},
            {"role_type": "campus", "eligibility": "verified eligible"},
            {"role_type": "other", "eligibility": "verified eligible"},
            {"term": "Summer 2026", "eligibility": "verified eligible"},
        )
        for changes in cases:
            with self.subTest(changes=changes):
                _fit, _reasons, tab = copilot.score_role(posting(**changes))
                self.assertEqual(tab, "not_ready")


class InputFilteringTests(unittest.TestCase):
    def test_only_open_postings_are_loaded(self):
        fieldnames = [
            "id", "company", "role", "source_status", "record_kind", "url"
        ]
        rows = [
            {
                "id": "posting",
                "company": "A",
                "role": "Intern",
                "source_status": "open",
                "record_kind": "posting",
                "url": "https://jobs.example.com/a",
            },
            {
                "id": "hub",
                "company": "B",
                "role": "Careers",
                "source_status": "watchlist",
                "record_kind": "watchlist",
                "url": "https://jobs.example.com/b",
            },
            {
                "id": "stale",
                "company": "C",
                "role": "Intern",
                "source_status": "stale/source-error",
                "record_kind": "posting",
                "url": "https://jobs.example.com/c",
            },
        ]
        with tempfile.TemporaryDirectory() as directory:
            tracker = Path(directory) / "tracker.csv"
            with tracker.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            with patch.object(copilot, "TRACKER_FILE", str(tracker)):
                loaded = copilot.load_rows()
        self.assertEqual([row["id"] for row in loaded], ["posting"])


class GeneratedPageSecurityTests(unittest.TestCase):
    def build_page(self, rows):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        output = Path(directory.name) / "cockpit.html"
        with patch.object(copilot, "OUT_HTML", str(output)):
            counts = copilot.build(rows)
        return output.read_text(encoding="utf-8"), counts

    def test_script_data_url_and_tier_are_sanitized(self):
        payload = "</script><img src=x onerror=alert(1)>"
        page, counts = self.build_page([
            posting(
                company=payload,
                url="javascript:alert(1)",
                elite_tier='elite" onclick="alert(1)',
                eligibility="verified eligible",
            )
        ])
        self.assertEqual(counts["not_ready"], 1)
        self.assertEqual(page.count("</script>"), 1)
        self.assertNotIn(payload, page)
        self.assertIn("\\u003c/script\\u003e\\u003cimg", page)
        self.assertNotIn('href="javascript:', page)
        self.assertNotIn('elite" onclick=', page)

    def test_state_is_persisted_by_stable_role_id(self):
        page, counts = self.build_page([
            posting(id="approved-id", eligibility="verified eligible"),
            posting(id="review-id"),
        ])
        self.assertEqual(counts, {
            "ready": 1,
            "needs_work": 1,
            "not_ready": 0,
        })
        self.assertIn('const STORE_KEY = "internship-cockpit-v2"', page)
        self.assertIn("memoryState.selected[c.id]", page)
        self.assertIn("memoryState.overrides[CARDS[i].id]", page)
        self.assertIn("Object.prototype.hasOwnProperty.call", page)
        self.assertIn("localStorage.setItem", page)
        self.assertIn("CARDS.filter(selected)", page)

    def test_page_does_not_claim_it_tailored_or_submitted_anything(self):
        page, _counts = self.build_page([posting()])
        self.assertNotIn("Ready to submit", page)
        self.assertNotIn("Apply changes and move", page)
        self.assertIn("title relevance", page)
        self.assertIn("Mark reviewed as approved", page)


if __name__ == "__main__":
    unittest.main()
