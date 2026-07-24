from contextlib import redirect_stderr
from io import StringIO
import os
from pathlib import Path
import stat
import tempfile
import unittest

from autoapply.cli import (
    approval_token_path,
    build_parser,
    plan_for_output,
    read_approval_token,
    resolve_approval_token_path,
    write_approval_token,
)
from autoapply.models import FillAction, FillPlan


class CliSafetyDefaultsTests(unittest.TestCase):
    def test_fill_is_dry_run_unless_execute_is_explicit(self):
        parser = build_parser()
        default = parser.parse_args(["fill", "job-1"])
        explicit = parser.parse_args(["fill", "job-1", "--execute"])
        self.assertFalse(default.execute)
        self.assertTrue(explicit.execute)

    def test_personal_plan_values_are_redacted_from_stdout_by_default(self):
        plan = FillPlan(
            "job-1", "form", "/private/resume.pdf", "hash",
            actions=[
                FillAction(
                    "email", "Email", "email", "#email",
                    "ada@invalid.test", "profile.contact.email",
                )
            ],
        )
        redacted = plan_for_output(plan, show_values=False)
        self.assertEqual(redacted["actions"][0]["value"], "[redacted]")
        self.assertEqual(redacted["resume_path"], "[private]")
        visible = plan_for_output(plan, show_values=True)
        self.assertEqual(visible["actions"][0]["value"], "ada@invalid.test")

    def test_submit_uses_a_token_file_and_rejects_token_argv(self):
        parser = build_parser()
        parsed = parser.parse_args(["submit", "job-1"])
        self.assertIsNone(parsed.approval_file)
        self.assertFalse(hasattr(parsed, "headless"))
        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit):
                parser.parse_args(
                    ["submit", "job-1", "--approval", "one-time-token"]
                )
            with self.assertRaises(SystemExit):
                parser.parse_args(["submit", "job-1", "--headless"])

    def test_approval_token_file_is_private_and_round_trips(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            path = approval_token_path(home, "job/with spaces")
            write_approval_token(path, "one-time-secret")
            self.assertEqual(read_approval_token(path), "one-time-secret")
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)
            self.assertNotIn("job/with spaces", str(path))

    def test_approval_token_file_rejects_loose_permissions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "approval.token"
            path.write_text("secret\n", encoding="utf-8")
            os.chmod(path, 0o644)
            with self.assertRaisesRegex(RuntimeError, "mode 0600"):
                read_approval_token(path)

    def test_custom_token_path_cannot_escape_dedicated_private_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "private"
            home.mkdir(mode=0o700)
            shared = Path(directory) / "shared"
            shared.mkdir(mode=0o755)
            before = stat.S_IMODE(shared.stat().st_mode)
            with self.assertRaisesRegex(RuntimeError, "direct children"):
                resolve_approval_token_path(
                    home, "job-1", shared / "approval.token"
                )
            self.assertEqual(stat.S_IMODE(shared.stat().st_mode), before)


if __name__ == "__main__":
    unittest.main()
