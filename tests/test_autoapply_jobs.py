import csv
import tempfile
from pathlib import Path
import unittest

from autoapply.browser import assert_allowed_url
from autoapply.jobs import canonicalize_url, detect_ats, external_id, jobs_from_tracker


class JobImportTests(unittest.TestCase):
    def test_ats_detection_and_canonicalization(self):
        url = (
            "https://job-boards.greenhouse.io/acme/jobs/123"
            "?utm_source=test&gh_jid=123"
        )
        canonical = canonicalize_url(url)
        self.assertNotIn("utm_source", canonical)
        self.assertIn("gh_jid=123", canonical)
        self.assertEqual(detect_ats(canonical), "greenhouse")
        self.assertEqual(external_id(canonical), "123")
        self.assertEqual(
            detect_ats("https://jobs.lever.co/acme/abc"), "lever"
        )
        self.assertEqual(
            detect_ats("https://jobs.ashbyhq.com/acme/abc"), "ashby"
        )
        self.assertEqual(
            external_id(
                "https://jobs.ashbyhq.com/acme/"
                "91e0686e-272a-4780-b33d-d7860b94a7b4/application"
            ),
            "91e0686e-272a-4780-b33d-d7860b94a7b4",
        )
        self.assertEqual(
            external_id(
                "https://jobs.lever.co/acme/"
                "9755ae0f-f740-40bc-bc13-be52c505748b/apply"
            ),
            "9755ae0f-f740-40bc-bc13-be52c505748b",
        )

    def test_tracker_import_skips_rows_without_url(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tracker.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "id", "company", "role", "url", "location", "region",
                        "source_status",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "id": "one",
                        "company": "Acme",
                        "role": "Intern",
                        "url": "https://jobs.lever.co/acme/abc",
                        "location": "London",
                        "region": "UK",
                        "source_status": "open",
                    }
                )
                writer.writerow({"id": "two", "company": "No URL", "role": "Intern"})
            jobs = jobs_from_tracker(path)
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0].ats, "lever")

    def test_tracker_import_only_includes_open_supported_postings(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tracker.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "id", "company", "role", "url",
                        "record_kind", "source_status",
                    ],
                )
                writer.writeheader()
                writer.writerows(
                    [
                        {
                            "id": "open",
                            "company": "Acme",
                            "role": "Intern",
                            "url": "https://jobs.lever.co/acme/abc",
                            "record_kind": "posting",
                            "source_status": "open",
                        },
                        {
                            "id": "watch",
                            "company": "Acme",
                            "role": "Careers",
                            "url": "https://jobs.lever.co/acme",
                            "record_kind": "watchlist",
                            "source_status": "watchlist",
                        },
                        {
                            "id": "stale",
                            "company": "Acme",
                            "role": "Old Intern",
                            "url": "https://jobs.ashbyhq.com/acme/old",
                            "record_kind": "posting",
                            "source_status": "stale/not-seen",
                        },
                        {
                            "id": "unsupported",
                            "company": "Acme",
                            "role": "Intern",
                            "url": "https://example.com/jobs/1",
                            "record_kind": "posting",
                            "source_status": "open",
                        },
                    ]
                )
            jobs = jobs_from_tracker(path)
            self.assertEqual([job.id for job in jobs], ["open"])

    def test_browser_host_allowlist_is_exact(self):
        assert_allowed_url(
            "https://job-boards.greenhouse.io/acme/jobs/1", "greenhouse"
        )
        with self.assertRaises(RuntimeError):
            assert_allowed_url(
                "https://greenhouse.io.attacker.invalid/acme/jobs/1", "greenhouse"
            )
        with self.assertRaisesRegex(RuntimeError, "non-HTTPS"):
            assert_allowed_url(
                "http://job-boards.greenhouse.io/acme/jobs/1", "greenhouse"
            )


if __name__ == "__main__":
    unittest.main()
