from datetime import datetime, timedelta, timezone
import tempfile
from pathlib import Path
import unittest

from autoapply.models import FillAction, FillPlan, Job
from autoapply.policy import token_hash
from autoapply.store import Store


class StoreApprovalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / "state.sqlite3")
        self.job = Job(
            "job-1",
            "Acme",
            "Robotics Intern",
            "https://job-boards.greenhouse.io/acme/jobs/123",
            ats="greenhouse",
            description="Build safe robot perception systems.",
        )
        self.store.upsert_job(self.job)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_approval_is_hash_bound_and_one_time(self):
        plan = FillPlan(
            job_id=self.job.id,
            form_hash="form-hash",
            resume_path="/private/resume.pdf",
            resume_hash="resume-hash",
            actions=[
                FillAction(
                    "email", "Email", "email", "#email",
                    "ada@invalid.test", "profile.contact.email",
                )
            ],
        )
        self.store.save_plan(self.job.id, plan)
        bound = plan.approval_hash(self.job)
        token = "one-time-secret"
        self.store.update_application(
            self.job.id,
            state="approved",
            approval_token_hash=token_hash(token),
            approval_bound_hash=bound,
            approval_expires_at=(
                datetime.now(timezone.utc) + timedelta(hours=1)
            ).isoformat(timespec="seconds"),
            approval_used=0,
        )
        self.assertTrue(
            self.store.claim_approval(self.job.id, token_hash(token), bound)
        )
        self.assertFalse(
            self.store.claim_approval(self.job.id, token_hash(token), bound)
        )
        self.assertEqual(self.store.application(self.job.id)["state"], "submitting")

    def test_changed_answer_changes_bound_hash(self):
        first = FillPlan(
            self.job.id, "form", "/x.pdf", "resume",
            actions=[FillAction("q", "Question", "text", "#q", "A", "reviewed")],
        )
        second = FillPlan(
            self.job.id, "form", "/x.pdf", "resume",
            actions=[FillAction("q", "Question", "text", "#q", "B", "reviewed")],
        )
        self.assertNotEqual(
            first.approval_hash(self.job), second.approval_hash(self.job)
        )

    def test_application_url_and_eligibility_are_bound(self):
        first = FillPlan(
            self.job.id,
            "form",
            "/x.pdf",
            "resume",
            application_url="https://job-boards.greenhouse.io/acme/jobs/123",
            eligibility_hash="eligibility-a",
        )
        changed_url = FillPlan(
            self.job.id,
            "form",
            "/x.pdf",
            "resume",
            application_url="https://job-boards.greenhouse.io/acme/jobs/123/apply",
            eligibility_hash="eligibility-a",
        )
        changed_eligibility = FillPlan(
            self.job.id,
            "form",
            "/x.pdf",
            "resume",
            application_url=first.application_url,
            eligibility_hash="eligibility-b",
        )
        self.assertNotEqual(
            first.approval_hash(self.job), changed_url.approval_hash(self.job)
        )
        self.assertNotEqual(
            first.approval_hash(self.job),
            changed_eligibility.approval_hash(self.job),
        )

    def test_initial_form_state_and_submit_control_are_bound(self):
        first = FillPlan(
            self.job.id,
            "form",
            "/x.pdf",
            "resume",
            initial_state_hash="state-a",
            submit_fingerprint="submit-a",
        )
        changed_state = FillPlan(
            self.job.id,
            "form",
            "/x.pdf",
            "resume",
            initial_state_hash="state-b",
            submit_fingerprint="submit-a",
        )
        changed_submit = FillPlan(
            self.job.id,
            "form",
            "/x.pdf",
            "resume",
            initial_state_hash="state-a",
            submit_fingerprint="submit-b",
        )
        self.assertNotEqual(
            first.approval_hash(self.job),
            changed_state.approval_hash(self.job),
        )
        self.assertNotEqual(
            first.approval_hash(self.job),
            changed_submit.approval_hash(self.job),
        )

    def test_expired_approval_cannot_be_claimed(self):
        plan = FillPlan(self.job.id, "form", "", "")
        bound = plan.approval_hash(self.job)
        token = "expired-secret"
        self.store.save_plan(self.job.id, plan)
        self.store.update_application(
            self.job.id,
            state="approved",
            approval_token_hash=token_hash(token),
            approval_bound_hash=bound,
            approval_expires_at=(
                datetime.now(timezone.utc) - timedelta(seconds=1)
            ).isoformat(timespec="seconds"),
            approval_used=0,
        )
        self.assertFalse(
            self.store.claim_approval(self.job.id, token_hash(token), bound)
        )

    def test_new_plan_invalidates_existing_approval(self):
        plan = FillPlan(self.job.id, "form", "", "")
        self.store.update_application(
            self.job.id,
            state="approved",
            approval_token_hash="old",
            approval_bound_hash="old",
            approval_expires_at="2999-01-01T00:00:00+00:00",
        )
        self.store.save_plan(self.job.id, plan)
        application = self.store.application(self.job.id)
        self.assertEqual(application["approval_token_hash"], "")
        self.assertEqual(application["approval_bound_hash"], "")
        self.assertEqual(application["approval_expires_at"], "")

    def test_latest_import_marks_absent_jobs_non_open_and_reappearance_restores(self):
        self.assertEqual(self.store.get_job(self.job.id).source_status, "open")
        self.assertEqual(self.store.import_jobs([]), 0)
        self.assertEqual(
            self.store.get_job(self.job.id).source_status,
            "not_in_latest_import",
        )
        self.store.import_jobs([self.job])
        self.assertEqual(self.store.get_job(self.job.id).source_status, "open")


if __name__ == "__main__":
    unittest.main()
