import unittest

from autoapply.models import FormField, FormSnapshot, Job
from autoapply.policy import build_fill_plan
from autoapply.questions import Category, classify


def profile():
    return {
        "identity": {"first_name": "Ada", "last_name": "Lovelace"},
        "contact": {
            "email": "ada@invalid.test",
            "phone": "+440000000000",
            "location": "London, United Kingdom",
            "linkedin": "https://linkedin.invalid/ada",
            "github": "https://github.invalid/ada",
            "website": "",
        },
        "education": {
            "institution": "Example University",
            "degree": "BSc",
            "field_of_study": "Computer Science",
            "graduation_month": "June",
            "graduation_year": "2028",
        },
        "work_authorization": {
            "GB": {
                "authorized_now": True,
                "authorization_scope": "unrestricted",
                "requires_sponsorship_now_or_future": False,
            },
            "US": {
                "authorized_now": "unknown",
                "requires_sponsorship_now_or_future": "unknown",
            },
        },
        "preferences": {"eeo": "manual"},
        "reviewed_answers": {},
    }


def snapshot(*fields):
    return FormSnapshot("greenhouse", "https://job-boards.greenhouse.io/x/jobs/1", list(fields))


class QuestionPolicyTests(unittest.TestCase):
    def test_sensitive_categories_are_classified_before_identity(self):
        self.assertEqual(
            classify(FormField("citizenship", "What is your citizenship?", "select")),
            Category.CITIZENSHIP,
        )
        self.assertEqual(
            classify(FormField("gender", "Gender identity", "select")), Category.EEO
        )
        self.assertEqual(
            classify(FormField("signature", "Electronic signature", "text")),
            Category.LEGAL,
        )

    def test_uk_authorization_never_leaks_to_us(self):
        job = Job(
            "j1", "Acme", "Robotics Intern",
            "https://job-boards.greenhouse.io/acme/jobs/1",
            ats="greenhouse", location="Boston, MA", region="US",
        )
        field = FormField(
            "auth",
            "Are you authorized to work in the United States?",
            "radio",
            required=True,
            options=["Yes", "No"],
            option_selectors={"Yes": "#yes", "No": "#no"},
        )
        plan = build_fill_plan(job, snapshot(field), profile(), "/tmp/resume.pdf", "hash")
        self.assertFalse(plan.safe_to_submit)
        self.assertEqual(plan.blocking[0].category, "work_authorization")
        self.assertIn("US", plan.blocking[0].reason)

    def test_exact_uk_authorization_is_resolved(self):
        job = Job(
            "j2", "Acme", "Robotics Intern",
            "https://job-boards.greenhouse.io/acme/jobs/2",
            ats="greenhouse", location="London", region="UK",
        )
        field = FormField(
            "auth",
            "Are you authorised to work in the United Kingdom?",
            "radio",
            required=True,
            options=["Yes", "No"],
            option_selectors={"Yes": "#yes", "No": "#no"},
        )
        plan = build_fill_plan(job, snapshot(field), profile(), "/tmp/resume.pdf", "hash")
        self.assertTrue(plan.safe_to_submit)
        self.assertEqual(plan.actions[0].value, "Yes")
        self.assertEqual(plan.actions[0].option_selector, "#yes")

    def test_limited_uk_authorization_requires_exact_job_form_review(self):
        configured = profile()
        configured["work_authorization"]["GB"] = {
            "authorized_now": True,
            "authorization_scope": "limited",
            "requires_sponsorship_now_or_future": True,
        }
        job = Job(
            "limited", "Acme", "Robotics Intern",
            "https://job-boards.greenhouse.io/acme/jobs/20",
            ats="greenhouse", location="London", region="UK",
        )
        field = FormField(
            "auth",
            "Are you authorised to work in the United Kingdom?",
            "radio",
            required=True,
            options=["Yes", "No"],
            option_selectors={"Yes": "#yes", "No": "#no"},
        )
        plan = build_fill_plan(
            job, snapshot(field), configured, "/tmp/resume.pdf", "hash"
        )
        self.assertFalse(plan.safe_to_submit)
        self.assertIn("scope_limited", plan.blocking[0].reason)

    def test_explicit_question_country_overrides_job_location(self):
        job = Job(
            "j2b", "Acme", "Global Intern",
            "https://job-boards.greenhouse.io/acme/jobs/22",
            ats="greenhouse", location="London", region="UK",
        )
        field = FormField(
            "auth",
            "Are you authorized to work in the United States?",
            "radio",
            required=True,
            options=["Yes", "No"],
            option_selectors={"Yes": "#yes", "No": "#no"},
        )
        plan = build_fill_plan(job, snapshot(field), profile(), "/tmp/resume.pdf", "hash")
        self.assertFalse(plan.safe_to_submit)
        self.assertIn("US", plan.blocking[0].reason)

    def test_named_global_country_never_falls_back_to_job_country(self):
        job = Job(
            "j2de", "Acme", "Global Intern",
            "https://job-boards.greenhouse.io/acme/jobs/220",
            ats="greenhouse", location="Boston", region="US",
        )
        configured = profile()
        configured["work_authorization"]["US"] = {
            "authorized_now": True,
            "authorization_scope": "unrestricted",
            "requires_sponsorship_now_or_future": False,
        }
        configured["work_authorization"]["DE"] = {
            "authorized_now": False,
            "requires_sponsorship_now_or_future": True,
        }
        field = FormField(
            "auth",
            "Are you authorized to work in Germany?",
            "radio",
            required=True,
            options=["Yes", "No"],
            option_selectors={"Yes": "#yes", "No": "#no"},
        )
        plan = build_fill_plan(
            job, snapshot(field), configured, "/tmp/resume.pdf", "hash"
        )
        self.assertTrue(plan.safe_to_submit)
        self.assertEqual(plan.actions[0].value, "No")
        self.assertIn(".DE.", plan.actions[0].source)

    def test_unknown_named_place_fails_closed_instead_of_falling_back(self):
        job = Job(
            "j2mars", "Acme", "Global Intern",
            "https://job-boards.greenhouse.io/acme/jobs/221",
            ats="greenhouse", location="Boston", region="US",
        )
        configured = profile()
        configured["work_authorization"]["US"] = {
            "authorized_now": True,
            "authorization_scope": "unrestricted",
            "requires_sponsorship_now_or_future": False,
        }
        field = FormField(
            "auth", "Are you authorized to work in Mars?", "radio", True,
            ["Yes", "No"], option_selectors={"Yes": "#yes", "No": "#no"},
        )
        plan = build_fill_plan(
            job, snapshot(field), configured, "/tmp/resume.pdf", "hash"
        )
        self.assertFalse(plan.safe_to_submit)
        self.assertEqual(plan.blocking[0].reason, "job_jurisdiction_unknown")

    def test_plain_pronoun_us_is_not_misread_as_united_states(self):
        job = Job(
            "j2pronoun", "Acme", "Intern",
            "https://job-boards.greenhouse.io/acme/jobs/222",
            ats="greenhouse", location="London", region="UK",
        )
        field = FormField(
            "auth", "Are you authorised to work with us?", "radio", True,
            ["Yes", "No"], option_selectors={"Yes": "#yes", "No": "#no"},
        )
        plan = build_fill_plan(job, snapshot(field), profile(), "", "")
        self.assertTrue(plan.safe_to_submit)
        self.assertIn(".GB.", plan.actions[0].source)

    def test_sensitive_free_text_answer_is_never_autofilled(self):
        job = Job(
            "j2c", "Acme", "Intern",
            "https://job-boards.greenhouse.io/acme/jobs/23",
            ats="greenhouse", location="London", region="UK",
        )
        field = FormField(
            "auth", "Are you authorised to work in the United Kingdom?", "text", True
        )
        plan = build_fill_plan(job, snapshot(field), profile(), "/tmp/resume.pdf", "hash")
        self.assertFalse(plan.safe_to_submit)
        self.assertEqual(
            plan.blocking[0].reason,
            "sensitive_answer_requires_an_exact_choice_control",
        )

    def test_exact_job_scoped_override_can_match_an_ats_identity_option(self):
        job = Job(
            "j-location", "Acme", "Intern",
            "https://job-boards.greenhouse.io/acme/jobs/230",
            ats="greenhouse", location="London", region="UK",
        )
        field = FormField(
            "location", "Current location", "combobox", True,
            ["London, England, United Kingdom", "London, Ontario, Canada"],
        )
        form = snapshot(field)
        configured = profile()
        configured["reviewed_answers"] = {
            job.id: {
                f"{form.form_hash} :: location :: {field.prompt}":
                    "London, England, United Kingdom"
            }
        }
        plan = build_fill_plan(job, form, configured, "", "")
        self.assertTrue(plan.safe_to_submit)
        self.assertEqual(
            plan.actions[0].value, "London, England, United Kingdom"
        )
        self.assertEqual(
            plan.actions[0].source,
            "profile.reviewed_answers.exact_prompt",
        )

    def test_compound_permit_question_requires_exact_review(self):
        job = Job(
            "j2d", "Acme", "Intern",
            "https://jobs.lever.co/acme/9755ae0f-f740-40bc-bc13-be52c505748b",
            ats="lever", location="Zurich", region="Switzerland",
        )
        configured = profile()
        configured["work_authorization"]["CH"] = {
            "authorized_now": False,
            "requires_sponsorship_now_or_future": True,
        }
        field = FormField(
            "permit",
            "Do you have a valid permit or are you legally eligible to apply "
            "for a permit to work in Switzerland?",
            "radio",
            required=True,
            options=["Yes", "No"],
        )
        form = FormSnapshot("lever", job.url + "/apply", [field])
        plan = build_fill_plan(job, form, configured, "", "")
        self.assertFalse(plan.safe_to_submit)
        self.assertEqual(
            plan.blocking[0].reason,
            "nuanced_immigration_question_requires_exact_review",
        )

        configured["reviewed_answers"] = {
            job.id: {
                f"{form.form_hash} :: permit :: {field.prompt}": "Yes"
            }
        }
        reviewed = build_fill_plan(job, form, configured, "", "")
        self.assertTrue(reviewed.safe_to_submit)
        self.assertEqual(reviewed.actions[0].value, "Yes")

    def test_required_eeo_and_unknown_questions_block(self):
        job = Job(
            "j3", "Acme", "Intern",
            "https://job-boards.greenhouse.io/acme/jobs/3",
            ats="greenhouse", region="UK",
        )
        fields = [
            FormField("gender", "Gender", "select", True, ["Woman", "Man", "Decline"]),
            FormField("mystery", "Tell us a secret", "text", True),
        ]
        plan = build_fill_plan(job, snapshot(*fields), profile(), "", "")
        self.assertFalse(plan.safe_to_submit)
        self.assertEqual(
            {item.category for item in plan.blocking}, {"eeo", "unknown"}
        )

    def test_optional_unknown_does_not_block(self):
        job = Job(
            "j4", "Acme", "Intern",
            "https://job-boards.greenhouse.io/acme/jobs/4",
            ats="greenhouse", region="UK",
        )
        plan = build_fill_plan(
            job,
            snapshot(FormField("optional", "Anything else?", "textarea", False)),
            profile(),
            "",
            "",
        )
        self.assertTrue(plan.safe_to_submit)
        self.assertEqual(len(plan.unresolved), 1)

    def test_exact_reviewed_custom_answer_only(self):
        job = Job(
            "j5", "Acme", "Intern",
            "https://job-boards.greenhouse.io/acme/jobs/5",
            ats="greenhouse", region="UK",
        )
        configured = profile()
        form = snapshot(
            FormField(
                "custom",
                "Favourite programming language?",
                "select",
                True,
                ["Python", "Rust"],
            )
        )
        configured["reviewed_answers"] = {
            job.id: {
                f"{form.form_hash} :: custom :: Favourite programming language?":
                    "Python"
            }
        }
        plan = build_fill_plan(
            job,
            form,
            configured,
            "",
            "",
        )
        self.assertTrue(plan.safe_to_submit)
        self.assertEqual(plan.actions[0].value, "Python")

    def test_reviewed_answer_is_not_reused_across_job_or_form(self):
        job = Job(
            "j5b", "Acme", "Intern",
            "https://job-boards.greenhouse.io/acme/jobs/55",
            ats="greenhouse", region="UK",
        )
        field = FormField(
            "custom", "Can you start in September?", "radio", True, ["Yes", "No"]
        )
        form = snapshot(field)
        configured = profile()
        configured["reviewed_answers"] = {
            "another-job": {
                f"{form.form_hash} :: custom :: Can you start in September?": "Yes"
            },
            job.id: {
                f"old-form-hash :: custom :: Can you start in September?": "Yes"
            },
        }
        plan = build_fill_plan(job, form, configured, "", "")
        self.assertFalse(plan.safe_to_submit)
        self.assertEqual(plan.blocking[0].reason, "unrecognized_question")

    def test_optionless_dynamic_combobox_blocks(self):
        job = Job(
            "j5c", "Acme", "Intern",
            "https://job-boards.greenhouse.io/acme/jobs/56",
            ats="greenhouse", region="UK",
        )
        form = snapshot(
            FormField("school", "School", "combobox", True, options=[])
        )
        plan = build_fill_plan(job, form, profile(), "", "")
        self.assertFalse(plan.safe_to_submit)
        self.assertEqual(
            plan.blocking[0].reason,
            "configured_answer_does_not_match_one_exact_option",
        )

    def test_captcha_always_blocks(self):
        job = Job(
            "j6", "Acme", "Intern",
            "https://job-boards.greenhouse.io/acme/jobs/6",
            ats="greenhouse", region="UK",
        )
        value = snapshot()
        value.captcha = True
        plan = build_fill_plan(job, value, profile(), "", "")
        self.assertFalse(plan.safe_to_submit)


if __name__ == "__main__":
    unittest.main()
