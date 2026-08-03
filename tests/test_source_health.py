"""Catching the failures that do not raise."""

import json
import tempfile
import unittest
from pathlib import Path

from source_health import (
    BROKEN_AFTER_RUNS,
    MAX_RUNS,
    alerts,
    load_history,
    record_run,
    report,
    summary,
)


def history(runs):
    return {"schema_version": 1, "runs": runs}


def run(date, sources, descriptions=None):
    return {
        "date": date,
        "sources": {
            name: {"rows": rows, "state": state}
            for name, (rows, state) in sources.items()
        },
        "descriptions": descriptions or {},
    }


HEALTHY = [
    run("2026-07-30", {"Greenhouse/a": (20, "ok"), "Lever/b": (8, "ok")}),
    run("2026-07-31", {"Greenhouse/a": (22, "ok"), "Lever/b": (7, "ok")}),
    run("2026-08-01", {"Greenhouse/a": (19, "ok"), "Lever/b": (9, "ok")}),
]


class SilentFailureTests(unittest.TestCase):
    def test_a_clean_response_carrying_nothing_is_reported(self):
        found = alerts(history(HEALTHY + [
            run("2026-08-02", {"Greenhouse/a": (0, "ok"), "Lever/b": (8, "ok")})
        ]))
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["kind"], "silent_empty")
        self.assertEqual(found[0]["severity"], "broken")

    def test_a_large_drop_is_worth_watching(self):
        found = alerts(history(HEALTHY + [
            run("2026-08-02", {"Greenhouse/a": (4, "ok"), "Lever/b": (8, "ok")})
        ]))
        self.assertEqual([x["kind"] for x in found], ["collapsed"])
        self.assertEqual(found[0]["severity"], "watch")

    def test_a_normal_run_reports_nothing(self):
        self.assertEqual(alerts(history(HEALTHY)), [])

    def test_a_source_that_disappears_is_reported(self):
        found = alerts(history(HEALTHY + [
            run("2026-08-02", {"Greenhouse/a": (20, "ok")})
        ]))
        self.assertEqual([x["kind"] for x in found], ["absent"])

    def test_a_new_source_with_no_history_is_not_judged(self):
        found = alerts(history(HEALTHY + [
            run("2026-08-02", {"Greenhouse/a": (20, "ok"), "Lever/b": (8, "ok"),
                               "Ashby/new": (0, "ok")})
        ]))
        self.assertEqual(found, [])


class TransientFailureTests(unittest.TestCase):
    def test_one_failed_run_is_watched_rather_than_declared_broken(self):
        # Providers rate-limit bursts; a monitor that cries wolf goes unread.
        found = alerts(history(HEALTHY + [
            run("2026-08-02", {"Greenhouse/a": (0, "failed"), "Lever/b": (8, "ok")})
        ]))
        self.assertEqual(found[0]["severity"], "watch")

    def test_repeated_failure_is_broken(self):
        runs = HEALTHY + [
            run(f"2026-08-{day:02d}", {"Greenhouse/a": (0, "failed"), "Lever/b": (8, "ok")})
            for day in range(2, 2 + BROKEN_AFTER_RUNS)
        ]
        found = alerts(history(runs))
        self.assertEqual(found[0]["severity"], "broken")
        self.assertIn("runs running", found[0]["detail"])


class DescriptionTests(unittest.TestCase):
    def test_adverts_that_stop_resolving_are_reported(self):
        found = alerts(history(HEALTHY + [
            run("2026-08-02", {"Greenhouse/a": (20, "ok"), "Lever/b": (8, "ok")},
                descriptions={"tried": 12, "resolved": 5})
        ]))
        self.assertEqual([x["kind"] for x in found], ["descriptions"])

    def test_a_healthy_sample_is_silent(self):
        found = alerts(history(HEALTHY + [
            run("2026-08-02", {"Greenhouse/a": (20, "ok"), "Lever/b": (8, "ok")},
                descriptions={"tried": 12, "resolved": 12})
        ]))
        self.assertEqual(found, [])


class HistoryTests(unittest.TestCase):
    def test_a_run_is_written_and_read_back(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "health.json"
            record_run("2026-08-02", {"Greenhouse/a": 5}, {"Greenhouse/a": "ok"}, path=path)
            stored = load_history(path)
            self.assertEqual(stored["runs"][0]["sources"]["Greenhouse/a"]["rows"], 5)

    def test_rerunning_the_same_day_replaces_rather_than_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "health.json"
            record_run("2026-08-02", {"a": 5}, {"a": "ok"}, path=path)
            record_run("2026-08-02", {"a": 9}, {"a": "ok"}, path=path)
            stored = load_history(path)
            self.assertEqual(len(stored["runs"]), 1)
            self.assertEqual(stored["runs"][0]["sources"]["a"]["rows"], 9)

    def test_history_is_bounded(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "health.json"
            for day in range(MAX_RUNS + 12):
                record_run(f"day-{day:03d}", {"a": 1}, {"a": "ok"}, path=path)
            self.assertEqual(len(load_history(path)["runs"]), MAX_RUNS)

    def test_a_corrupt_history_does_not_take_the_run_down(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "health.json"
            path.write_text("{not json", encoding="utf-8")
            self.assertEqual(load_history(path)["runs"], [])
            record_run("2026-08-02", {"a": 1}, {"a": "ok"}, path=path)
            self.assertEqual(len(load_history(path)["runs"]), 1)


class SummaryTests(unittest.TestCase):
    def test_counts_split_healthy_from_broken(self):
        figures = summary(history(HEALTHY + [
            run("2026-08-02", {"Greenhouse/a": (0, "ok"), "Lever/b": (8, "ok")})
        ]))
        self.assertEqual(figures["sources"], 2)
        self.assertEqual(figures["broken"], 1)
        self.assertEqual(figures["healthy"], 1)

    def test_an_empty_history_reports_nothing_rather_than_failing(self):
        self.assertEqual(summary(history([]))["runs"], 0)
        self.assertIn("No source history", report(history([])))

    def test_the_report_names_what_is_wrong(self):
        text = report(history(HEALTHY + [
            run("2026-08-02", {"Greenhouse/a": (0, "ok"), "Lever/b": (8, "ok")})
        ]))
        self.assertIn("Greenhouse/a", text)
        self.assertIn("BROKEN", text)


class LiveHistoryTests(unittest.TestCase):
    def test_the_committed_history_is_valid(self):
        stored = load_history()
        self.assertTrue(stored["runs"], "no health history has been recorded")
        latest = stored["runs"][-1]
        self.assertTrue(latest["sources"])
        # Every recorded source carries both a count and a state.
        for name, entry in latest["sources"].items():
            self.assertIn("rows", entry, name)
            self.assertIn("state", entry, name)


if __name__ == "__main__":
    unittest.main()
