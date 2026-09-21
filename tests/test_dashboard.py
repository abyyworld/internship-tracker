import csv
from pathlib import Path
import subprocess
import sys
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
            # The one box everything starts from, and the lenses over the
            # same corpus.
            self.assertIn('id="ask"', page)
            self.assertIn('id="region"', page)
            for lens in ("roles", "research", "ventures", "funding", "universities"):
                self.assertIn(f'data-lens="{lens}"', page)
            # Light and dark are a property of the page, not a preference to
            # be asked for twice: the reader's choice is stored once for the
            # whole site, and the default follows the device.
            self.assertIn("prefers-color-scheme: dark", page)
            self.assertIn('data-theme="dark"', page)
            self.assertIn('"radar.theme"', page)
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

    def test_the_page_reads_one_beside_the_list_it_was_chosen_from(self):
        # Reading a posting used to mean leaving the page, and what you were
        # comparing it against went with you.
        from dashboard_page import TEMPLATE

        self.assertIn('id="detail"', TEMPLATE)
        self.assertIn('id="detailBody"', TEMPLATE)
        self.assertIn("function rowHtml(row)", TEMPLATE)
        self.assertIn("function showDetail(id)", TEMPLATE)
        # Three panes on a wide screen, and a sheet over the list when there is
        # not room for three.
        self.assertRegex(TEMPLATE, r"\.frame\{[^}]*grid-template-columns:230px minmax\(0,1fr\) minmax")
        self.assertIn("@media (max-width:1180px)", TEMPLATE)
        # And movable without a mouse, or a list beside a pane is not worth it.
        self.assertIn('event.key === "ArrowDown"', TEMPLATE)

    def test_a_deadline_can_be_seen_and_asked_for(self):
        from dashboard_page import TEMPLATE

        self.assertIn('id="deadlineChips"', TEMPLATE)
        self.assertIn("function daysLeft(item)", TEMPLATE)
        self.assertIn("function matchesClosing(item, picks)", TEMPLATE)
        self.assertIn("closingPicks", TEMPLATE)
        for label in ("Closing this week", "Closing this month", "Has a deadline"):
            self.assertIn(label, TEMPLATE)
        # Counted against everything else already chosen, so the number says
        # what pressing it would leave rather than what it would leave from
        # nothing.
        self.assertIn("function closingCounts()", TEMPLATE)
        self.assertIn('["Closes"', TEMPLATE.replace(" ", "").replace('["Closes",', '["Closes"'))

    def test_running_the_script_is_what_publishes_the_page(self):
        """Both workflows publish by running `python dashboard.py`.

        This module had no entry point for a while, so that command imported
        it, defined build(), and exited having written nothing. The daily watch
        went on refreshing tracker.csv while the public page served whatever
        snapshot had last been generated by hand — three days and 153 unseen
        opportunities, the last time. Every test here called build() directly,
        so none of them could notice. This one runs the command the workflows
        run.
        """
        script = Path(dashboard.__file__).resolve()
        output = script.parent / "docs" / "index.html"
        before = output.read_bytes() if output.exists() else None
        try:
            output.unlink(missing_ok=True)
            run = subprocess.run([sys.executable, str(script)],
                                 capture_output=True, text=True, cwd=script.parent)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue(output.exists(),
                            "running dashboard.py published nothing at all")
            self.assertIn('data-lens="roles"', output.read_text(encoding="utf-8"))
        finally:
            if before is not None:
                output.write_bytes(before)

    def test_the_deploy_runs_on_every_file_the_page_is_built_from(self):
        # The page moved into dashboard_page.py and the trigger list did not
        # follow, so a change to the dashboard itself would be committed, pass
        # CI, and never reach the site.
        workflow = (Path(dashboard.__file__).resolve().parent
                    / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        for name in ("dashboard.py", "dashboard_page.py", "docs/**", "tracker.csv"):
            self.assertIn(f'- "{name}"', workflow, f"a change to {name} would not deploy")
        self.assertIn("python3 dashboard.py", workflow)


if __name__ == "__main__":
    unittest.main()
