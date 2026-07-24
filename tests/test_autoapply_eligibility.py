import unittest

from autoapply.eligibility import assess_eligibility, jurisdiction_for
from autoapply.models import Job


class GlobalEligibilityTests(unittest.TestCase):
    def test_global_robotics_jurisdictions(self):
        cases = {
            ("Switzerland", "Zurich, Switzerland"): "CH",
            ("Germany", "Berlin, Germany"): "DE",
            ("France", "Paris, France"): "FR",
            ("Norway", "Oslo, Norway"): "NO",
            ("Singapore", "Singapore"): "SG",
            ("Japan", "Tokyo, Japan"): "JP",
            ("Australia", "Sydney, Australia"): "AU",
            ("China", "Shenzhen, China"): "CN",
            ("India", "Bengaluru, India"): "IN",
            ("South Korea", "Seoul, South Korea"): "KR",
            ("Israel", "Tel Aviv, Israel"): "IL",
        }
        for (region, location), expected in cases.items():
            with self.subTest(region=region):
                job = Job("j", "Robot Co", "Intern", "https://invalid.test",
                          region=region, location=location)
                self.assertEqual(jurisdiction_for(job), expected)

    def test_multi_country_role_never_infers_one_authorization(self):
        job = Job(
            "j", "Robot Co", "Intern", "https://invalid.test",
            region="US / UK", location="London / New York",
        )
        self.assertEqual(jurisdiction_for(job), "")
        report = assess_eligibility(job, {"work_authorization": {}})
        self.assertEqual(report.status, "review_required")

    def test_known_country_with_unknown_rights_requires_review(self):
        job = Job(
            "j", "Robot Co", "Intern", "https://invalid.test",
            region="Switzerland", location="Zurich",
        )
        report = assess_eligibility(
            job,
            {
                "work_authorization": {
                    "CH": {
                        "authorized_now": "unknown",
                        "requires_sponsorship_now_or_future": "unknown",
                    }
                }
            },
        )
        self.assertEqual(report.status, "review_required")
        self.assertIn("CH", report.reasons[0])


if __name__ == "__main__":
    unittest.main()
