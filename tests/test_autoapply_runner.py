from datetime import datetime, timedelta, timezone
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

import yaml

from autoapply.eligibility import assess_eligibility
from autoapply.models import FillPlan, Job
from autoapply.policy import token_hash
from autoapply.resume import file_sha256
from autoapply.runner import (
    _eligibility_fingerprint,
    _submission_confirmed,
    approve,
    prepare,
    submit,
)
from autoapply.store import Store


class PrepareRunnerTests(unittest.TestCase):
    def test_prepare_builds_local_evidence_backed_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            (home / "generated").mkdir()
            profile = {
                "identity": {"first_name": "Ada", "last_name": "Lovelace"},
                "contact": {
                    "email": "ada@invalid.test",
                    "phone": "+440000000000",
                    "location": "London",
                    "linkedin": "",
                    "github": "",
                    "website": "",
                },
                "education": {
                    "institution": "Example University",
                    "degree": "BSc",
                    "field_of_study": "Computer Science",
                    "level": "undergraduate",
                    "graduation_month": "June",
                    "graduation_year": "2028",
                },
                "work_authorization": {},
                "citizenships": [],
                "preferences": {"eeo": "manual"},
                "reviewed_answers": {},
            }
            facts = {
                "summary": "Verified summary.",
                "skills": ["Python", "Robotics"],
                "education": [],
                "sections": [
                    {
                        "name": "Projects",
                        "entries": [
                            {
                                "title": "Robot",
                                "bullets": [
                                    {
                                        "id": "fact-1",
                                        "text": "Built a verified robotics prototype.",
                                        "tags": ["robotics"],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
            (home / "profile.yaml").write_text(
                yaml.safe_dump(profile), encoding="utf-8"
            )
            (home / "resume_facts.yaml").write_text(
                yaml.safe_dump(facts), encoding="utf-8"
            )
            with Store(home / "state.sqlite3") as store:
                job = Job(
                    "job",
                    "Acme",
                    "Robotics Intern",
                    "https://job-boards.greenhouse.io/acme/jobs/1",
                    ats="greenhouse",
                    region="UK",
                    location="London",
                    description="Build robotics systems with Python.",
                )
                store.upsert_job(job)
                with patch(
                    "autoapply.runner.fetch_description",
                    return_value=job.description,
                ):
                    result = prepare(store, home, job.id)
                self.assertEqual(result["selected_fact_ids"], ["fact-1"])
                self.assertTrue(Path(result["resume_path"]).is_file())
                self.assertEqual(store.application(job.id)["state"], "prepared")
                unknown = Job(
                    "unknown-job",
                    "Other Co",
                    "Robotics Intern",
                    "https://example.com/jobs/robot",
                    region="UK",
                    location="London",
                    description=(
                        "Job title: Robotics Intern. Category: Robotics. "
                        "Technical focus: robot perception."
                    ),
                )
                store.upsert_job(unknown)
                with patch(
                    "autoapply.runner.fetch_description", return_value=""
                ), patch("autoapply.runner.assert_public_https_url"):
                    fallback_result = prepare(
                        store, home, unknown.id, resume_only=True
                    )
                self.assertEqual(
                    fallback_result["description_source"],
                    "public-tracker-metadata-fallback",
                )

    def test_prepare_refuses_to_generate_resume_without_matching_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            (home / "generated").mkdir()
            profile = {
                "identity": {"first_name": "Ada", "last_name": "Lovelace"},
                "contact": {
                    "email": "ada@invalid.test",
                    "phone": "+440000000000",
                    "location": "London",
                    "linkedin": "",
                    "github": "",
                    "website": "",
                },
                "education": {
                    "institution": "Example University",
                    "degree": "BSc",
                    "field_of_study": "Computer Science",
                    "level": "undergraduate",
                    "graduation_month": "June",
                    "graduation_year": "2028",
                },
                "work_authorization": {},
                "citizenships": [],
                "preferences": {"eeo": "manual"},
                "reviewed_answers": {},
            }
            facts = {
                "summary": "Verified summary.",
                "skills": ["Writing"],
                "education": [],
                "sections": [
                    {
                        "name": "Projects",
                        "entries": [
                            {
                                "title": "Magazine",
                                "bullets": [
                                    {
                                        "id": "fact-writing",
                                        "text": "Edited a verified student magazine.",
                                        "tags": ["writing"],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
            (home / "profile.yaml").write_text(
                yaml.safe_dump(profile), encoding="utf-8"
            )
            (home / "resume_facts.yaml").write_text(
                yaml.safe_dump(facts), encoding="utf-8"
            )
            with Store(home / "state.sqlite3") as store:
                job = Job(
                    "job",
                    "Acme",
                    "Robotics Intern",
                    "https://job-boards.greenhouse.io/acme/jobs/1",
                    ats="greenhouse",
                    region="UK",
                    location="London",
                    description="Build robot perception systems.",
                )
                store.upsert_job(job)
                with patch(
                    "autoapply.runner.fetch_description",
                    return_value=job.description,
                ), patch("autoapply.runner.render_resume") as render:
                    with self.assertRaisesRegex(
                        RuntimeError, "No role-relevant verified evidence"
                    ):
                        prepare(store, home, job.id)
                render.assert_not_called()
                self.assertEqual(store.application(job.id)["state"], "needs_evidence")


class ApprovalGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
        self.profile = {
            "identity": {"first_name": "Ada", "last_name": "Lovelace"},
            "contact": {
                "email": "ada@invalid.test",
                "phone": "+440000000000",
                "location": "London",
                "linkedin": "",
                "github": "",
                "website": "",
            },
            "education": {
                "institution": "Example University",
                "degree": "BSc",
                "field_of_study": "Computer Science",
                "level": "undergraduate",
                "graduation_month": "June",
                "graduation_year": "2028",
            },
            "work_authorization": {
                "GB": {
                    "authorized_now": True,
                    "authorization_scope": "unrestricted",
                    "requires_sponsorship_now_or_future": False,
                }
            },
            "citizenships": [],
            "preferences": {"eeo": "manual"},
            "reviewed_answers": {},
        }
        self._write_profile()
        (self.home / "resume_facts.yaml").write_text(
            yaml.safe_dump(
                {
                    "summary": "Verified summary.",
                    "skills": ["Python"],
                    "education": [],
                    "sections": [],
                }
            ),
            encoding="utf-8",
        )
        self.store = Store(self.home / "state.sqlite3")
        self.job = Job(
            "gate-job",
            "Acme",
            "Robotics Intern",
            "https://job-boards.greenhouse.io/acme/jobs/123",
            ats="greenhouse",
            region="UK",
            location="London",
            description="Build safe robotics systems.",
        )
        self.store.upsert_job(self.job)
        self.resume = self.home / "resume.pdf"
        self.resume.write_bytes(b"%PDF-1.4 verified")
        report = assess_eligibility(self.job, self.profile)
        self.plan = FillPlan(
            job_id=self.job.id,
            form_hash="form-hash",
            resume_path=str(self.resume),
            resume_hash=file_sha256(self.resume),
            application_url=self.job.url,
            eligibility_hash=_eligibility_fingerprint(
                self.job, self.profile, report
            ),
            initial_state_hash="initial-state",
            submit_fingerprint="submit-control",
        )
        self.store.save_plan(self.job.id, self.plan)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def _write_profile(self):
        (self.home / "profile.yaml").write_text(
            yaml.safe_dump(self.profile), encoding="utf-8"
        )

    def test_approve_requires_not_blocked_and_sets_24_hour_expiry(self):
        with patch(
            "autoapply.runner.fetch_description",
            return_value=self.job.description,
        ):
            token, bound, expires_at = approve(
                self.store, self.home, self.job.id
            )
        self.assertTrue(token)
        self.assertEqual(bound, self.plan.approval_hash(self.job))
        expires = datetime.fromisoformat(expires_at)
        remaining = expires - datetime.now(timezone.utc)
        self.assertGreater(remaining, timedelta(hours=23, minutes=59))
        self.assertLessEqual(remaining, timedelta(hours=24))
        application = self.store.application(self.job.id)
        self.assertEqual(application["approval_expires_at"], expires_at)

    def test_approve_rejects_review_required_eligibility(self):
        self.profile["work_authorization"]["GB"]["authorized_now"] = "unknown"
        self._write_profile()
        with patch(
            "autoapply.runner.fetch_description",
            return_value=self.job.description,
        ):
            with self.assertRaisesRegex(RuntimeError, "exactly 'not_blocked'"):
                approve(self.store, self.home, self.job.id)

    def test_prepare_fails_closed_when_description_fetch_is_empty(self):
        with patch("autoapply.runner.fetch_description", return_value=""):
            with self.assertRaisesRegex(RuntimeError, "non-empty job description"):
                prepare(self.store, self.home, self.job.id)

    def test_submit_rejects_an_expired_approval_before_browser_launch(self):
        with patch(
            "autoapply.runner.fetch_description",
            return_value=self.job.description,
        ):
            token, _bound, _expires = approve(
                self.store, self.home, self.job.id
            )
            self.store.update_application(
                self.job.id,
                approval_expires_at=(
                    datetime.now(timezone.utc) - timedelta(seconds=1)
                ).isoformat(timespec="seconds"),
            )
            with self.assertRaisesRegex(RuntimeError, "Approval expired"):
                submit(
                    self.store,
                    self.home,
                    self.job.id,
                    token,
                    headed=True,
                )
        self.assertEqual(
            self.store.application(self.job.id)["state"], "approval_expired"
        )

    def test_submit_rechecks_eligibility_before_browser_launch(self):
        with patch(
            "autoapply.runner.fetch_description",
            return_value=self.job.description,
        ):
            token, _bound, _expires = approve(
                self.store, self.home, self.job.id
            )
            self.profile["work_authorization"]["GB"]["authorized_now"] = "unknown"
            self._write_profile()
            with self.assertRaisesRegex(RuntimeError, "exactly 'not_blocked'"):
                submit(
                    self.store,
                    self.home,
                    self.job.id,
                    token,
                    headed=True,
                )

    def test_submit_rejects_changed_eligibility_facts_even_when_still_allowed(self):
        with patch(
            "autoapply.runner.fetch_description",
            return_value=self.job.description,
        ):
            token, _bound, _expires = approve(
                self.store, self.home, self.job.id
            )
            self.profile["work_authorization"]["GB"][
                "requires_sponsorship_now_or_future"
            ] = True
            self._write_profile()
            with self.assertRaisesRegex(RuntimeError, "Eligibility facts changed"):
                submit(
                    self.store,
                    self.home,
                    self.job.id,
                    token,
                    headed=True,
                )

    def test_submit_fails_closed_when_latest_description_is_empty(self):
        with patch(
            "autoapply.runner.fetch_description",
            return_value=self.job.description,
        ):
            token, _bound, _expires = approve(
                self.store, self.home, self.job.id
            )
        with patch("autoapply.runner.fetch_description", return_value=""):
            with self.assertRaisesRegex(RuntimeError, "non-empty job description"):
                submit(
                    self.store,
                    self.home,
                    self.job.id,
                    token,
                    headed=True,
                )

    def test_submit_prohibits_headless_mode_before_any_other_work(self):
        with self.assertRaisesRegex(RuntimeError, "Headless final submission"):
            submit(
                self.store,
                self.home,
                self.job.id,
                "unused-token",
                headed=False,
            )

    def test_submission_confirmation_checks_child_frames(self):
        class Document:
            def __init__(self, name):
                self.name = name
                self.url = f"https://job-boards.greenhouse.io/{name}"

        class Page(Document):
            def __init__(self):
                super().__init__("page")
                self.main_frame = Document("main")
                self.frames = [self.main_frame, Document("confirmation")]

        class Adapter:
            def confirmed(self, document, _starting_state):
                return document.name == "confirmation"

        page = Page()
        starting = {
            id(page): {"url": page.url, "signals": {}},
            id(page.frames[1]): {
                "url": page.frames[1].url,
                "signals": {},
            },
        }
        self.assertTrue(_submission_confirmed(Adapter(), page, starting))


if __name__ == "__main__":
    unittest.main()
