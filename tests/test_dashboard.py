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
            self.assertIn("127.0.0.1:8765/tailor", page)
            self.assertIn("⚡ Tailor CV + Apply", page)
            self.assertIn(r"\u003c/script\u003e", page)
            self.assertNotIn("</script><script>alert(1)</script>", page)

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
