import ssl
import unittest

import internship_watcher as watcher


def current_record(
    rid="role1",
    *,
    company="Robotics Co",
    role="Software Engineer Intern",
    location="London, UK",
    url="https://job-boards.greenhouse.io/robotics/jobs/1234567",
    source="Greenhouse/robotics",
    status="open",
    kind="posting",
):
    return {
        "id": rid,
        "company": company,
        "role": role,
        "location": location,
        "region": watcher.region_of(location),
        "work_mode": watcher.work_mode_of(location),
        "url": url,
        "term": "Unknown",
        "deadline": "",
        "level": "Unknown",
        "role_type": "intern",
        "citizenship": "unknown",
        "sponsorship": "unknown",
        "eligibility": "review required",
        "sources": [source],
        "flags": [],
        "elite_tier": "",
        "category": "Robotics & Embodied AI",
        "focus_tags": "robot-software",
        "robotics_focus": "robotics",
        "company_type": "startup",
        "equity_signal": "private company; verify offer",
        "record_kind": kind,
        "source_status": status,
    }


def stored_record(
    rid="role1",
    *,
    url="https://boards.greenhouse.io/robotics/jobs/1234567?gh_src=x",
    source="Greenhouse/robotics",
    missing_runs="0",
):
    return {
        "id": rid,
        "NEW": "",
        "company": "Robotics Co",
        "role": "Software Engineer Intern",
        "location": "London, UK",
        "url": url,
        "sources": source,
        "source_status": "open",
        "record_kind": "posting",
        "first_seen": "2026-07-01",
        "last_seen": "2026-07-23",
        "missing_runs": missing_runs,
        "new_on": "",
        "my_status": "",
        "priority": "",
        "applied_date": "",
        "notes": "keep this note",
    }


class LocationTests(unittest.TestCase):
    def test_explicit_geographies_and_remote_mode(self):
        cases = {
            "Cambridge, MA": "US",
            "Cambridge, UK": "UK",
            "Cambridge": "Unknown",
            "Birmingham, AL": "US",
            "London, ON": "Canada",
            "Dublin, CA": "US",
            "Belfast, Northern Ireland": "UK",
            "Remote in USA": "US",
            "Remote - London, UK": "UK",
            "London / New York": "US / UK",
            "US": "US",
            "Europe / US": "US / Europe",
            "Washington, D.C.": "US",
            "Bengaluru": "India",
            "Belgrade": "Serbia",
            "Israel": "Israel",
        }
        for location, expected in cases.items():
            with self.subTest(location=location):
                self.assertEqual(watcher.region_of(location), expected)
        self.assertEqual(watcher.work_mode_of("Remote in USA"), "remote")
        self.assertEqual(watcher.work_mode_of("In-Office"), "onsite")


class ClassificationTests(unittest.TestCase):
    def test_degree_evidence(self):
        self.assertEqual(
            watcher.degree_level("Quant Research Intern (BS/MS)"),
            "Undergraduate eligible",
        )
        self.assertEqual(
            watcher.degree_level("Research Intern", ["ADV-DEGREE"]),
            "Advanced/unknown",
        )
        self.assertEqual(watcher.degree_level("PhD Software Intern"), "PhD")
        self.assertEqual(
            watcher.degree_level("Machine Learning Engineer Intern"), "Unknown"
        )

    def test_term_inference(self):
        cases = {
            "Software Engineer Intern (Fall 2026)": "Fall 2026",
            "Software Engineer Intern (Fall/Winter 2026)": "Fall/Winter 2026",
            "Graduate Software Engineer (2026)": "2026",
            "2027 Internship": "2027",
            "Robotics Intern https://example.test/intern-co-op-2026": "2026",
            "Software Intern https://example.test/June-2026_R003": "2026",
            "No date": "Unknown",
        }
        for title, expected in cases.items():
            with self.subTest(title=title):
                self.assertEqual(watcher.infer_term(title), expected)
        self.assertEqual(
            watcher.term_from_evidence("Software Intern", "Summer 2027"),
            ("Summer 2027", False),
        )

    def test_strict_intern_signals(self):
        rejected = [
            "Campus AI Research Engineer (Full-Time)",
            "Graduate Software Engineer (2026)",
            "Internal Audit - Treasury",
            "Internationalization Engineer",
            "Sensor Placement and Analysis Engineer",
            "Engineering Technical Fellow, Solid Rocket Motors",
            "Resident Supplier Quality Engineer",
        ]
        for title in rejected:
            with self.subTest(title=title):
                self.assertFalse(watcher.early_career(title))
        self.assertTrue(watcher.early_career("Campus Software Engineer (Intern)"))
        self.assertTrue(watcher.early_career("Software Engineer Co-op"))
        self.assertTrue(watcher.early_career("Research Internships"))

    def test_robotics_category_and_company_signal(self):
        self.assertEqual(
            watcher.category_of("Physical Intelligence", "Research Intern"),
            "Robotics & Embodied AI",
        )
        focus, company_type, equity = watcher.company_signals(
            "Physical Intelligence"
        )
        self.assertEqual(focus, "embodied AI")
        self.assertEqual(company_type, "emerging-startup")
        self.assertIn("verify", equity)
        self.assertEqual(
            watcher.category_of("Example Co", "Mechatronics Intern"),
            "Robotics & Embodied AI",
        )
        self.assertEqual(
            watcher.company_signals("Robotics & AI Institute")[:2],
            ("robotics research", "nonprofit"),
        )

    def test_programme_table_is_not_parsed_as_location_bearing_jobs(self):
        text = """
| Company | Role | Location | Application/Link |
| --- | --- | --- | --- |
| Acme | Software Intern | London, UK | [apply](https://example.com/job) |
## programmes
| org | opportunity | type | deadline |
| --- | --- | --- | --- |
| Apple | [Student Programme](https://example.com/program) | SWE programme | rolling |
"""
        rows = watcher.parse_md_pipe(text, "Summer 2027")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["location"], "London, UK")

    def test_citizenship_mentions_require_requirement_language(self):
        self.assertNotIn(
            "US-CITIZEN-ONLY",
            watcher.derive_flags("US citizens and green card holders may apply"),
        )
        self.assertIn(
            "US-CITIZEN-ONLY",
            watcher.derive_flags("U.S. citizenship is required"),
        )


class IdentityTests(unittest.TestCase):
    def test_tracking_parameters_are_removed(self):
        a = (
            "https://boards.greenhouse.io/acme/jobs/1234567"
            "?gh_jid=1234567&utm_source=x"
        )
        b = "https://job-boards.greenhouse.io/acme/jobs/1234567"
        self.assertEqual(watcher.canonical_url(a), watcher.canonical_url(b))
        self.assertEqual(
            watcher.provider_job_key(a), "greenhouse:1234567"
        )

    def test_job_identity_crosses_employer_and_ats_url_variants(self):
        pairs = [
            (
                "https://www.imc.com/us/careers/jobs/4823924101",
                "https://job-boards.eu.greenhouse.io/imc/jobs/4823924101",
            ),
            (
                "https://jobs.apple.com/en-us/details/200664785/software",
                "https://jobs.apple.com/en-us/details/200664785-3810/software",
            ),
            (
                "https://relx.wd3.myworkdayjobs.com/relx/job/x/role_R112557-2",
                "https://relx.wd3.myworkdayjobs.com/RiskSolutions/job/y/role_R112557-1",
            ),
        ]
        for first, second in pairs:
            with self.subTest(first=first):
                self.assertEqual(
                    watcher.provider_job_key(first),
                    watcher.provider_job_key(second),
                )

    def test_greenhouse_query_identity_survives_on_custom_career_page(self):
        first = "https://careers.example.com/jobs?gh_jid=1001&utm_source=x"
        second = "https://careers.example.com/jobs?gh_jid=1002&utm_source=x"
        self.assertNotEqual(
            watcher.provider_job_key(first), watcher.provider_job_key(second)
        )
        self.assertIn("gh_jid=1001", watcher.canonical_url(first))

    def test_unsafe_application_url_is_rejected(self):
        self.assertEqual(watcher.safe_url("javascript:alert(1)"), "")
        self.assertEqual(watcher.safe_url("file:///tmp/private"), "")

    def test_spreadsheet_and_markdown_cells_are_neutralized(self):
        self.assertEqual(watcher.spreadsheet_safe("=HYPERLINK(...)"), "'=HYPERLINK(...)")
        rendered = watcher._cell("Role](javascript:alert(1))\\nnext")
        self.assertNotIn("](javascript:", rendered)
        self.assertNotIn("\n", rendered)


class ReconciliationTests(unittest.TestCase):
    def test_failed_source_never_closes_role_or_increments_miss(self):
        existing = {"role1": stored_record()}
        new_ids, rows = watcher.reconcile(
            {}, existing, {"Greenhouse/robotics": "failed"}, today="2026-07-24"
        )
        self.assertEqual(new_ids, [])
        self.assertEqual(rows[0]["source_status"], "stale/source-error")
        self.assertEqual(rows[0]["missing_runs"], "0")
        self.assertEqual(rows[0]["last_seen"], "2026-07-23")
        self.assertEqual(rows[0]["notes"], "keep this note")

    def test_two_consecutive_healthy_misses_are_required_to_close(self):
        existing = {"role1": stored_record()}
        _, once = watcher.reconcile(
            {}, existing, {"Greenhouse/robotics": "ok"}, today="2026-07-24"
        )
        self.assertEqual(once[0]["source_status"], "stale/not-seen")
        self.assertEqual(once[0]["missing_runs"], "1")
        _, twice = watcher.reconcile(
            {}, {"role1": once[0]}, {"Greenhouse/robotics": "ok"},
            today="2026-07-25",
        )
        self.assertEqual(twice[0]["source_status"], "gone/closed?")
        self.assertEqual(twice[0]["missing_runs"], "2")

    def test_repeated_run_on_same_day_is_not_a_second_miss(self):
        existing = {"role1": stored_record()}
        _, once = watcher.reconcile(
            {}, existing, {"Greenhouse/robotics": "ok"}, today="2026-07-24"
        )
        _, repeated = watcher.reconcile(
            {}, {"role1": once[0]}, {"Greenhouse/robotics": "ok"},
            today="2026-07-24",
        )
        self.assertEqual(repeated[0]["source_status"], "stale/not-seen")
        self.assertEqual(repeated[0]["missing_runs"], "1")

    def test_reappearance_resets_missing_count_and_preserves_user_data(self):
        existing = {"old": stored_record(rid="old", missing_runs="1")}
        current = {"new-semantic-id": current_record(rid="new-semantic-id")}
        new_ids, rows = watcher.reconcile(
            current, existing, {"Greenhouse/robotics": "ok"},
            today="2026-07-24",
        )
        self.assertEqual(new_ids, [])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["missing_runs"], "0")
        self.assertEqual(rows[0]["first_seen"], "2026-07-01")

    def test_same_day_rerun_preserves_new_marker(self):
        recent = stored_record()
        recent["first_seen"] = "2026-07-24"
        recent["new_on"] = "2026-07-24"
        current = {"role1": current_record()}
        new_ids, rows = watcher.reconcile(
            current, {"role1": recent}, {"Greenhouse/robotics": "ok"},
            today="2026-07-24",
        )
        self.assertEqual(new_ids, ["role1"])
        self.assertEqual(rows[0]["NEW"], "YES")

    def test_same_day_first_seen_without_new_marker_is_not_resurrected(self):
        recent = stored_record()
        recent["first_seen"] = "2026-07-24"
        current = {"role1": current_record()}
        new_ids, rows = watcher.reconcile(
            current, {"role1": recent}, {"Greenhouse/robotics": "ok"},
            today="2026-07-24",
        )
        self.assertEqual(new_ids, [])
        self.assertEqual(rows[0]["NEW"], "")

    def test_legacy_same_day_new_marker_migrates_to_new_on(self):
        recent = stored_record()
        recent["first_seen"] = "2026-07-24"
        recent["NEW"] = "YES"
        current = {"role1": current_record()}
        new_ids, rows = watcher.reconcile(
            current, {"role1": recent}, {"Greenhouse/robotics": "ok"},
            today="2026-07-24",
        )
        self.assertEqual(new_ids, ["role1"])
        self.assertEqual(rows[0]["new_on"], "2026-07-24")

    def test_same_day_new_survives_a_source_outage_in_daily_digest(self):
        recent = stored_record()
        recent["first_seen"] = "2026-07-24"
        recent["new_on"] = "2026-07-24"
        new_ids, rows = watcher.reconcile(
            {}, {"role1": recent}, {"Greenhouse/robotics": "failed"},
            today="2026-07-24",
        )
        self.assertEqual(new_ids, ["role1"])
        self.assertEqual(rows[0]["NEW"], "YES")
        self.assertEqual(rows[0]["source_status"], "stale/source-error")

    def test_new_marker_expires_on_next_day(self):
        recent = stored_record()
        recent["first_seen"] = "2026-07-24"
        recent["new_on"] = "2026-07-24"
        current = {"role1": current_record()}
        new_ids, rows = watcher.reconcile(
            current, {"role1": recent}, {"Greenhouse/robotics": "ok"},
            today="2026-07-25",
        )
        self.assertEqual(new_ids, [])
        self.assertEqual(rows[0]["NEW"], "")
        self.assertEqual(rows[0]["new_on"], "2026-07-24")

    def test_watchlist_is_never_new_or_open(self):
        record = current_record(
            status="watchlist", kind="watchlist", source="robotics_watchlist"
        )
        new_ids, rows = watcher.reconcile(
            {"watch": record}, {}, {}, today="2026-07-24"
        )
        self.assertEqual(new_ids, [])
        self.assertEqual(rows[0]["NEW"], "")
        self.assertEqual(rows[0]["source_status"], "watchlist")

    def test_duplicate_old_urls_collapse_to_one_current_row(self):
        first = stored_record(rid="one")
        first["notes"] = ""
        second = stored_record(
            rid="two",
            url="https://job-boards.greenhouse.io/robotics/jobs/1234567",
        )
        current = {"new": current_record(rid="new")}
        _, rows = watcher.reconcile(
            current, {"one": first, "two": second},
            {"Greenhouse/robotics": "ok"}, today="2026-07-24",
        )
        self.assertEqual(len(rows), 1)


class SecurityTests(unittest.TestCase):
    def test_tls_verification_is_enabled(self):
        self.assertEqual(watcher.SSL_CTX.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(watcher.SSL_CTX.check_hostname)


if __name__ == "__main__":
    unittest.main()


class GeneratedOutputTests(unittest.TestCase):
    """The watcher writes the repository's front page and its history files."""

    ROW = {
        "id": "x1", "company": "Acme", "role": "Robotics Intern", "region": "UK",
        "term": "Summer 2027", "url": "https://invalid.test", "source": "test",
        "source_status": "open", "category": "Robotics & Embodied AI",
        "tier": "elite", "deadline": "", "sponsorship": "", "location": "London",
        "record_kind": "posting", "NEW": "YES", "degree": "Undergraduate eligible",
        "company_type": "", "position_type": "Internship", "cv_support": "",
        "eligibility": "review",
    }

    def _in_sandbox(self, work):
        """Run a generator in a scratch directory: it writes to the cwd."""
        import os
        import tempfile

        original = os.getcwd()
        with tempfile.TemporaryDirectory() as directory:
            os.chdir(directory)
            try:
                work()
                return directory, sorted(
                    os.path.relpath(os.path.join(root, name), directory)
                    for root, _, names in os.walk(directory)
                    for name in names
                )
            finally:
                os.chdir(original)

    def test_the_public_readme_names_no_private_filesystem_path(self):
        """A public front page described the owner's own Desktop layout."""
        readme = self._readme([dict(self.ROW)])
        for leak in ("/Users/", "$HOME/Desktop", "other projects"):
            with self.subTest(leak=leak):
                self.assertNotIn(leak, readme)

    def _readme(self, rows):
        import os
        import tempfile

        original = os.getcwd()
        with tempfile.TemporaryDirectory() as directory:
            os.chdir(directory)
            try:
                watcher.build_dashboard(rows, ["x1"], {"x1": rows[0]})
                with open("README.md", encoding="utf-8") as handle:
                    return handle.read()
            finally:
                os.chdir(original)

    def test_the_readme_documents_a_command_that_exists(self):
        readme = self._readme([dict(self.ROW)])
        self.assertIn("python3 -m autoapply bridge", readme)
        # The command the README advertises must be a real subcommand. Read the
        # parser's own choices rather than invoking --help, which would print
        # the whole usage message into the test output.
        import argparse

        from autoapply.cli import build_parser

        subcommands = {
            name
            for action in build_parser()._actions
            if isinstance(action, argparse._SubParsersAction)
            for name in action.choices
        }
        self.assertIn("bridge", subcommands)

    def test_a_digest_is_written_under_the_digests_directory(self):
        """Generated history stays out of the repository root."""
        rows = [dict(self.ROW)]
        _, written = self._in_sandbox(lambda: watcher.write_new_digest(rows, ["x1"]))
        self.assertEqual(written, [f"digests/new_roles_{watcher.TODAY}.md"])

    def test_no_digest_is_written_when_nothing_is_new(self):
        _, written = self._in_sandbox(
            lambda: watcher.write_new_digest([dict(self.ROW)], [])
        )
        self.assertEqual(written, [])
