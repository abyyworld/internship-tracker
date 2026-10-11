"""The market warehouse: reading days out of git, and what the SQL decides.

Reading history and rendering the report are stdlib only and always run. The
SQL models need DuckDB, which the tracker's own CI does not install, so those
tests run wherever requirements-market.txt is installed (the market workflow)
and are skipped elsewhere.
"""

import csv
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from market import backfill, report

try:
    import duckdb
except ImportError:      # the tracker's CI: stdlib only
    duckdb = None

COLUMNS = ["company", "role", "category", "region", "source_status", "record_kind",
           "sources", "url", "first_seen", "last_seen", "id", "sponsorship"]


def tracker(rows, day=""):
    # The watcher stamps last_seen every run, so no two days' files are equal.
    out = io.StringIO()
    w = csv.DictWriter(out, COLUMNS)
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, "") for c in COLUMNS} | {"last_seen": day})
    return out.getvalue()


def role(id, status="open", sources="Simplify2027", url=None, **extra):
    return {"id": id, "company": extra.get("company", "Acme"), "role": f"Intern {id}",
            "category": extra.get("category", "Software Engineering"), "region": "US",
            "source_status": status, "record_kind": extra.get("record_kind", "posting"),
            "sources": sources, "url": url or f"https://example.com/{id}",
            "sponsorship": "unknown"}


class GitHistory(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args, date=None):
        env = {**os.environ, "TZ": "UTC"}
        if date:
            env |= {"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
        subprocess.run(["git", *args], cwd=self.repo, check=True,
                       capture_output=True, env=env)

    def commit(self, when, text, message="watcher: update", path="tracker.csv"):
        (self.repo / path).write_text(text)
        self.git("add", path)
        self.git("commit", "-q", "-m", message, date=when)


class ReadingOneSnapshotPerDay(GitHistory):
    def test_a_manual_rerun_replaces_that_mornings_run(self):
        self.commit("2026-08-01T07:00:00Z", tracker([role("a")]))
        self.commit("2026-08-01T15:00:00Z", tracker([role("a"), role("b")]))
        self.commit("2026-08-02T07:00:00Z", tracker([role("b")]))
        days = backfill.daily_commits(cwd=self.repo)
        self.assertEqual([d for d, _ in days], ["2026-08-01", "2026-08-02"])
        cache = self.repo / "cache"
        backfill.extract(days, cache_dir=cache, cwd=self.repo)
        self.assertIn("Intern b", (cache / "2026-08-01.csv").read_text())

    def test_extraction_is_incremental(self):
        self.commit("2026-08-01T07:00:00Z", tracker([role("a")]))
        cache = self.repo / "cache"
        first = backfill.extract(backfill.daily_commits(cwd=self.repo),
                                 cache_dir=cache, cwd=self.repo)
        self.commit("2026-08-02T07:00:00Z", tracker([role("a"), role("b")]))
        second = backfill.extract(backfill.daily_commits(cwd=self.repo),
                                  cache_dir=cache, cwd=self.repo)
        self.assertEqual((first, second), (["2026-08-01"], ["2026-08-02"]))

    def test_a_scraper_change_marks_the_next_snapshot(self):
        self.commit("2026-08-01T07:00:00Z", tracker([role("a")]))
        self.commit("2026-08-01T12:00:00Z", "# widened lanes\n",
                    message="Widen the lane filter", path="internship_watcher.py")
        self.commit("2026-08-02T07:00:00Z", tracker([role("a"), role("b")]))
        days = backfill.daily_commits(cwd=self.repo)
        self.assertEqual(backfill.coverage_changes(days, cwd=self.repo), ["2026-08-02"])


class RenderingTheReport(unittest.TestCase):
    def test_results_cannot_close_the_script_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            template = Path(tmp) / "t.html"
            template.write_text("<script>const R = /*RESULTS*/null;</script>")
            page = report.render({"label": "</script><b>x"}, template)
        self.assertNotIn("</script><b>", page)
        self.assertIn('"<\\/script><b>x"', page)

    def test_the_shipped_template_has_its_placeholder(self):
        self.assertIn(report.MARK, report.TEMPLATE.read_text())


@unittest.skipUnless(duckdb, "DuckDB not installed (pip install -r requirements-market.txt)")
class WhatTheModelsDecide(GitHistory):
    """Build a warehouse from a few synthetic days and read mart.role."""

    def build(self, days, changed=()):
        for i, rows in enumerate(days):
            day = f"2026-08-{i + 1:02d}"
            self.commit(f"{day}T07:00:00Z", tracker(rows, day))
        cache = self.repo / "cache"
        backfill.extract(backfill.daily_commits(cwd=self.repo), cache_dir=cache, cwd=self.repo)
        if changed:
            (cache / "coverage_changes.txt").write_text("".join(f"{d}\n" for d in changed))
        con = self.con = duckdb.connect()
        backfill.load(con, cache_dir=cache)
        cols = [c[0] for c in con.execute("SELECT * FROM mart.role LIMIT 0").description]
        return {r[cols.index("role_key")]: dict(zip(cols, r))
                for r in con.execute("SELECT * FROM mart.role").fetchall()}

    def test_a_closure_is_dated_to_the_first_missing_morning(self):
        roles = self.build([
            [role("old")],
            [role("old"), role("new")],
            [role("old"), role("new")],
            [role("old"), role("new", "stale/not-seen")],
            [role("old"), role("new", "gone/closed?")],
        ])
        new = roles["new"]
        self.assertTrue(new["closed"])
        self.assertEqual(str(new["closed_on"]), "2026-08-04")
        self.assertEqual(new["duration_days"], 2)

    def test_an_unconfirmed_absence_is_censored_not_closed(self):
        roles = self.build([
            [role("old")],
            [role("old"), role("new")],
            [role("old"), role("new", "stale/source-error")],
        ])
        self.assertFalse(roles["new"]["closed"])
        self.assertEqual(roles["new"]["duration_days"], 1)

    def test_a_role_that_came_back_is_not_closed(self):
        roles = self.build([
            [role("old")],
            [role("old"), role("new")],
            [role("old"), role("new", "gone/closed?")],
            [role("old"), role("new")],
        ])
        self.assertFalse(roles["new"]["closed"])
        self.assertTrue(roles["new"]["reopened"])

    def test_a_retitled_role_is_stitched_by_url(self):
        url = "https://example.com/advert"
        roles = self.build([
            [role("old")],
            [role("old"), role("v1", url=url)],
            [role("old"), role("v2", url=url)],
            [role("old"), role("v2", url=url)],
        ])
        self.assertNotIn("v2", roles)
        self.assertEqual(roles["v1"]["opened_on"].isoformat(), "2026-08-02")
        self.assertEqual(roles["v1"]["watcher_ids"], 2)
        self.assertFalse(roles["v1"]["closed"])

    def test_only_roles_on_an_already_watched_source_are_fresh(self):
        roles = self.build([
            [role("old")],                                    # launch day
            [role("old"), role("posted"), role("board", sources="Greenhouse/acme")],
        ])
        self.assertFalse(roles["old"]["fresh"])               # open at launch
        self.assertTrue(roles["posted"]["fresh"])
        self.assertFalse(roles["board"]["fresh"])             # the board was new

    def test_nothing_is_fresh_on_a_coverage_change_day(self):
        roles = self.build([[role("old")], [role("old"), role("widened")]],
                           changed=["2026-08-02"])
        self.assertFalse(roles["widened"]["fresh"])

    def test_watchlists_and_personal_columns_never_reach_the_warehouse(self):
        roles = self.build([[role("old"), role("hub", "watchlist", record_kind="watchlist")]])
        self.assertNotIn("hub", roles)
        # July's files carried my_status / notes; staging selects past them
        staged = {c[0] for c in self.con.execute("SELECT * FROM stg.snapshot LIMIT 0").description}
        self.assertFalse(staged & {"my_status", "priority", "applied_date", "notes"})


if __name__ == "__main__":
    unittest.main()
