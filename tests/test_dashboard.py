import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import dashboard


class DashboardTests(unittest.TestCase):
    def test_builds_filterable_public_dashboard_and_escapes_job_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tracker = root / "tracker.csv"
            output = root / "docs" / "index.html"
            fields = [
                "id", "company", "role", "category", "region", "record_kind",
                "source_status", "url", "company_type",
            ]
            with tracker.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow(
                    {
                        "id": "robot-job",
                        "company": "</script><script>alert(1)</script>",
                        "role": "Robotics Intern",
                        "category": "Robotics & Embodied AI",
                        "region": "UK",
                        "record_kind": "posting",
                        "source_status": "open",
                        "url": (
                            "https://jobs.ashbyhq.com/robot/"
                            "12345678-1234-1234-1234-123456789abc"
                        ),
                        "company_type": "emerging-startup",
                    }
                )
            with patch.object(dashboard, "TRACKER", tracker), patch.object(
                dashboard, "OUTPUT", output
            ):
                self.assertEqual(dashboard.build(), 1)
            page = output.read_text(encoding="utf-8")
            self.assertIn('id="search"', page)
            self.assertIn('id="region"', page)
            self.assertIn('id="startupOnly"', page)
            self.assertIn("data-autoapply-dashboard", page)
            # The CV button goes through open.html rather than straight at the
            # helper: a direct link answers with ERR_CONNECTION_REFUSED whenever
            # the helper is not running, which explains nothing to the reader.
            self.assertIn("./open.html?url=", page)
            self.assertNotIn("127.0.0.1:8765/editor", page)
            self.assertIn("✦ Edit CV for this job", page)
            self.assertIn(r"\u003c/script\u003e", page)
            self.assertNotIn("</script><script>alert(1)</script>", page)

    def test_the_opener_page_covers_every_local_destination(self):
        """Whatever the dashboard sends there must be handled, and the page has
        to work with no helper running — it is served from GitHub Pages."""
        page = (Path("docs") / "open.html").read_text(encoding="utf-8")
        for destination in ("/editor?url=", "/dashboard", "/connect"):
            self.assertIn(destination, page)
        # It tells the reader what to do, and needs nothing from the helper to
        # say it.
        self.assertIn("install-login-service.command", page)
        self.assertIn("127.0.0.1:8765", page)
        self.assertIn("favicon.ico", page)   # the liveness probe
        # Static and self-contained: no build step, no third-party origin.
        self.assertNotIn("<script src", page)
        self.assertNotIn("https://cdn", page)

    def test_ats_detection_and_url_safety_are_independent(self):
        self.assertTrue(
            dashboard.ats_supported(
                "https://jobs.lever.co/company/"
                "12345678-1234-1234-1234-123456789abc"
            )
        )
        self.assertFalse(dashboard.ats_supported("https://example.com/job"))
        self.assertEqual(dashboard.safe_url("javascript:alert(1)"), "")


if __name__ == "__main__":
    unittest.main()
