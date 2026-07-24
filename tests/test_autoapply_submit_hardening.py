import unittest

from autoapply.adapters.base import BaseAdapter, _validated_temporal_value
from autoapply.models import FillAction, FillPlan, FormField, FormSnapshot, digest
from autoapply.runner import (
    _assert_post_fill_invariants,
    _capture_confirmation_states,
    _observed_value_issues,
    _submission_confirmed,
)


APPLICATION_URL = "https://job-boards.greenhouse.io/acme/jobs/123"


def field(
    key: str,
    prompt: str,
    kind: str,
    current_value,
    *,
    required: bool = False,
) -> FormField:
    return FormField(
        key=key,
        prompt=prompt,
        kind=kind,
        required=required,
        selector=f"#{key}",
        current_value=current_value,
    )


class FormInvariantTests(unittest.TestCase):
    def test_value_changes_affect_state_hash_but_not_form_hash(self):
        empty = FormSnapshot(
            "greenhouse",
            APPLICATION_URL,
            [field("email", "Email", "email", "")],
        )
        filled = FormSnapshot(
            "greenhouse",
            APPLICATION_URL,
            [field("email", "Email", "email", "ada@example.test")],
        )
        self.assertEqual(empty.form_hash, filled.form_hash)
        self.assertNotEqual(empty.state_hash, filled.state_hash)

    def test_unapproved_nonempty_optional_eeo_value_blocks_click(self):
        snapshot = FormSnapshot(
            "greenhouse",
            APPLICATION_URL,
            [
                field("email", "Email", "email", "ada@example.test"),
                field("gender", "Gender identity", "select", "Woman"),
            ],
        )
        plan = FillPlan(
            "job",
            snapshot.form_hash,
            "/resume.pdf",
            "resume",
            actions=[
                FillAction(
                    "email",
                    "Email",
                    "email",
                    "#email",
                    "ada@example.test",
                    "profile.contact.email",
                )
            ],
            application_url=APPLICATION_URL,
            submit_fingerprint="submit",
        )
        issues = _observed_value_issues(snapshot, plan, after_fill=True)
        self.assertEqual(
            [(item.key, reason) for item, reason in issues],
            [("gender", "nonempty_value_was_not_approved")],
        )
        with self.assertRaisesRegex(RuntimeError, "Gender identity"):
            _assert_post_fill_invariants(
                plan, snapshot, APPLICATION_URL, "submit"
            )

    def test_unobservable_value_blocks_even_when_it_looks_empty(self):
        hidden_state = field(
            "custom",
            "Custom legal answer",
            "combobox",
            "",
        )
        hidden_state.value_observable = False
        snapshot = FormSnapshot(
            "greenhouse",
            APPLICATION_URL,
            [hidden_state],
        )
        plan = FillPlan(
            "job",
            snapshot.form_hash,
            "/resume.pdf",
            "resume",
            application_url=APPLICATION_URL,
            submit_fingerprint="submit",
        )
        issues = _observed_value_issues(snapshot, plan, after_fill=True)
        self.assertEqual(
            [(item.key, reason) for item, reason in issues],
            [("custom", "field_value_could_not_be_observed")],
        )

    def test_exact_approved_optional_value_is_allowed(self):
        snapshot = FormSnapshot(
            "greenhouse",
            APPLICATION_URL,
            [field("gender", "Gender identity", "select", "Decline to answer")],
        )
        plan = FillPlan(
            "job",
            snapshot.form_hash,
            "/resume.pdf",
            "resume",
            actions=[
                FillAction(
                    "gender",
                    "Gender identity",
                    "select",
                    "#gender",
                    "Decline to answer",
                    "reviewed_answers",
                )
            ],
            application_url=APPLICATION_URL,
            submit_fingerprint="submit",
        )
        self.assertEqual(
            _observed_value_issues(snapshot, plan, after_fill=True), []
        )
        _assert_post_fill_invariants(
            plan, snapshot, APPLICATION_URL, "submit"
        )

    def test_new_conditional_field_blocks_click(self):
        approved_snapshot = FormSnapshot(
            "greenhouse",
            APPLICATION_URL,
            [field("sponsor", "Need sponsorship?", "select", "")],
        )
        post_fill_snapshot = FormSnapshot(
            "greenhouse",
            APPLICATION_URL,
            [
                field("sponsor", "Need sponsorship?", "select", "Yes"),
                field(
                    "visa",
                    "Describe your visa status",
                    "text",
                    "",
                    required=True,
                ),
            ],
        )
        plan = FillPlan(
            "job",
            approved_snapshot.form_hash,
            "/resume.pdf",
            "resume",
            actions=[
                FillAction(
                    "sponsor",
                    "Need sponsorship?",
                    "select",
                    "#sponsor",
                    "Yes",
                    "profile.work_authorization",
                )
            ],
            application_url=APPLICATION_URL,
            submit_fingerprint="submit",
        )
        with self.assertRaisesRegex(RuntimeError, "Form fields"):
            _assert_post_fill_invariants(
                plan, post_fill_snapshot, APPLICATION_URL, "submit"
            )

    def test_changed_approved_value_blocks_click(self):
        snapshot = FormSnapshot(
            "greenhouse",
            APPLICATION_URL,
            [field("email", "Email", "email", "other@example.test")],
        )
        plan = FillPlan(
            "job",
            snapshot.form_hash,
            "/resume.pdf",
            "resume",
            actions=[
                FillAction(
                    "email",
                    "Email",
                    "email",
                    "#email",
                    "ada@example.test",
                    "profile.contact.email",
                )
            ],
            application_url=APPLICATION_URL,
            submit_fingerprint="submit",
        )
        with self.assertRaisesRegex(RuntimeError, "Email"):
            _assert_post_fill_invariants(
                plan, snapshot, APPLICATION_URL, "submit"
            )


class ConfirmationTests(unittest.TestCase):
    class Body:
        def __init__(self, document):
            self.document = document

        def inner_text(self, timeout):
            if self.document.unobservable:
                raise RuntimeError("cross-origin body unavailable")
            return self.document.text

    class Document:
        def __init__(self, name, text="", url=APPLICATION_URL):
            self.name = name
            self.text = text
            self.url = url
            self.unobservable = False

        def locator(self, selector):
            if selector != "body":
                raise AssertionError(selector)
            return ConfirmationTests.Body(self)

    class Page(Document):
        def __init__(self, text=""):
            super().__init__("page", text)
            self.main_frame = ConfirmationTests.Document("main")
            self.frames = [self.main_frame]

    def test_preexisting_confirmation_text_is_not_confirmation(self):
        adapter = BaseAdapter()
        document = self.Document(
            "page", "Thank you for applying. Application details follow."
        )
        before = adapter.confirmation_state(document)
        self.assertFalse(adapter.confirmed(document, before))

    def test_generic_thank_you_is_never_confirmation(self):
        adapter = BaseAdapter()
        document = self.Document("page", "Thank you")
        before = adapter.confirmation_state(document)
        document.text = "Thank you for visiting our careers page"
        document.url = APPLICATION_URL + "/thank"
        self.assertFalse(adapter.confirmed(document, before))

    def test_new_precise_signal_is_confirmation(self):
        adapter = BaseAdapter()
        document = self.Document("page", "Review your answers")
        before = adapter.confirmation_state(document)
        document.text = "Your application has been successfully submitted."
        self.assertTrue(adapter.confirmed(document, before))

    def test_new_frame_confirmation_is_checked(self):
        adapter = BaseAdapter()
        page = self.Page("Application form")
        before = _capture_confirmation_states(adapter, page, (page,))
        page.frames.append(
            self.Document(
                "confirmation",
                "We have received your application.",
                APPLICATION_URL + "/confirmation",
            )
        )
        self.assertTrue(_submission_confirmed(adapter, page, before))

    def test_unobservable_required_baseline_prohibits_click(self):
        adapter = BaseAdapter()
        page = self.Page("Application form")
        page.unobservable = True
        with self.assertRaisesRegex(RuntimeError, "could not be observed"):
            _capture_confirmation_states(adapter, page, (page,))


class SubmitControlAndTemporalTests(unittest.TestCase):
    def test_exact_submit_node_is_bound_for_click(self):
        identity = {
            "path": ":scope > button:nth-of-type(1)",
            "tag": "button",
            "id": "submit",
            "name": "",
            "type": "submit",
            "text": "Submit application",
            "aria_label": "",
            "title": "",
            "form_action": APPLICATION_URL,
            "form_method": "post",
            "owner_form_action": APPLICATION_URL,
            "owner_form_method": "post",
        }

        class Handle:
            def is_visible(self):
                return True

            def is_enabled(self):
                return True

            def evaluate(self, _script):
                return identity

        handle = Handle()

        class Locator:
            def element_handle(self):
                return handle

        class Adapter(BaseAdapter):
            def submit_locator(self, _page):
                return Locator()

        adapter = Adapter()
        self.assertIs(
            adapter.submit_control_for_click(None, digest(identity)),
            handle,
        )
        with self.assertRaisesRegex(RuntimeError, "changed before click"):
            adapter.submit_control_for_click(None, "wrong-fingerprint")

    def test_month_and_datetime_local_are_strictly_validated(self):
        self.assertEqual(_validated_temporal_value("month", "2026-07"), "2026-07")
        self.assertEqual(
            _validated_temporal_value("datetime-local", "2026-07-24T09:30"),
            "2026-07-24T09:30",
        )
        for kind, value in (
            ("month", "0000-07"),
            ("month", "2026-13"),
            ("datetime-local", "2026-07-24T25:00"),
            ("datetime-local", "2026-07-24T09:30Z"),
        ):
            with self.subTest(kind=kind, value=value):
                with self.assertRaises(RuntimeError):
                    _validated_temporal_value(kind, value)


if __name__ == "__main__":
    unittest.main()
