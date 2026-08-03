#!/usr/bin/env python3
"""Tell when a source has quietly stopped working.

A scraper rarely dies loudly. It returns HTTP 200 and an empty list, or a
third of the rows it used to, or pages whose text no longer contains the job
description — and the tracker keeps running, thinner and wronger, for weeks.
That is exactly what happened here: EU-hosted Greenhouse boards moved API
host, every description silently became the tracker's own one-line metadata,
and the only visible symptom was that the AI got worse.

So this keeps a per-source history of how many rows each run produced and
compares each run against it. A source that returns nothing where it reliably
returned twenty is reported as broken even though nothing raised.

Standard library only: the daily GitHub Actions run has no dependencies.
"""

from __future__ import annotations

import json
from pathlib import Path
import statistics
from typing import Any


ROOT = Path(__file__).resolve().parent
HISTORY_PATH = ROOT / "data" / "source-health.json"
SCHEMA_VERSION = 1

# Runs of history to keep. Enough to see a weekly pattern and to give a median
# that one bad day cannot move.
MAX_RUNS = 60
# A source needs this many past runs before its median means anything.
MIN_HISTORY = 3
# Below this share of its own median, a source is treated as having collapsed
# rather than merely having a quiet day.
COLLAPSE_RATIO = 0.4
# A source that used to carry at least this many rows is worth alerting on.
SIGNIFICANT_ROWS = 4
# Share of sampled postings whose description must still resolve.
DESCRIPTION_FLOOR = 0.8
# Consecutive failed runs before a source is called broken rather than watched.
# One failure is usually the provider rate-limiting a burst of requests, and a
# monitor that cries wolf on those stops being read at all.
BROKEN_AFTER_RUNS = 2


def load_history(path: Path = HISTORY_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": SCHEMA_VERSION, "runs": []}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"schema_version": SCHEMA_VERSION, "runs": []}
    if not isinstance(value, dict) or not isinstance(value.get("runs"), list):
        return {"schema_version": SCHEMA_VERSION, "runs": []}
    return value


def record_run(
    date: str,
    counts: dict[str, int],
    states: dict[str, str],
    *,
    descriptions: dict[str, int] | None = None,
    path: Path = HISTORY_PATH,
) -> dict[str, Any]:
    """Append one run's per-source row counts to the history."""
    history = load_history(path)
    history["schema_version"] = SCHEMA_VERSION
    history["runs"] = [run for run in history["runs"] if run.get("date") != date]
    history["runs"].append({
        "date": date,
        "sources": {
            name: {"rows": int(counts.get(name, 0)), "state": states.get(name, "ok")}
            for name in sorted(set(counts) | set(states))
        },
        "descriptions": descriptions or {},
    })
    history["runs"] = history["runs"][-MAX_RUNS:]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(history, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return history


def _past_counts(runs: list[dict[str, Any]], source: str) -> list[int]:
    return [
        int(run.get("sources", {}).get(source, {}).get("rows", 0))
        for run in runs
        if source in run.get("sources", {})
    ]


def _failing_streak(runs: list[dict[str, Any]], source: str) -> int:
    """How many runs in a row this source has failed, counting back."""
    streak = 0
    for run in reversed(runs):
        entry = run.get("sources", {}).get(source)
        if entry is None:
            break
        if str(entry.get("state", "ok")) in {"failed", "degraded"}:
            streak += 1
        else:
            break
    return streak


def alerts(history: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Everything currently wrong, worst first."""
    history = history or load_history()
    runs = history.get("runs") or []
    if not runs:
        return []
    latest = runs[-1]
    earlier = runs[:-1]
    found: list[dict[str, Any]] = []

    for source, entry in sorted(latest.get("sources", {}).items()):
        rows = int(entry.get("rows", 0))
        state = str(entry.get("state", "ok"))
        past = [count for count in _past_counts(earlier, source) if count >= 0]
        median = statistics.median(past) if len(past) >= MIN_HISTORY else None

        if state in {"failed", "degraded"}:
            streak = _failing_streak(runs, source)
            severity = "broken" if streak >= BROKEN_AFTER_RUNS else "watch"
            wording = (
                "raised an error and returned nothing" if state == "failed"
                else "responded but its format was not recognised"
            )
            found.append({
                "source": source, "severity": severity, "kind": state,
                "detail": (
                    f"The source {wording}"
                    + (f", {streak} runs running" if streak > 1 else " this run")
                ),
            })
            continue
        if median and median >= SIGNIFICANT_ROWS and rows == 0:
            # The quiet failure: a clean response carrying nothing.
            found.append({
                "source": source, "severity": "broken", "kind": "silent_empty",
                "detail": (
                    f"Returned nothing this run, having typically returned "
                    f"{median:.0f}. Nothing raised, so this is only visible here."
                ),
            })
            continue
        if (
            median
            and median >= SIGNIFICANT_ROWS
            and rows < median * COLLAPSE_RATIO
        ):
            found.append({
                "source": source, "severity": "watch", "kind": "collapsed",
                "detail": (
                    f"Returned {rows} against a usual {median:.0f}"
                ),
            })

    # Sources that used to report and have now vanished from the run entirely.
    if earlier:
        previous = set(earlier[-1].get("sources", {}))
        for source in sorted(previous - set(latest.get("sources", {}))):
            found.append({
                "source": source, "severity": "watch", "kind": "absent",
                "detail": "Present in the previous run, missing from this one",
            })

    sample = latest.get("descriptions") or {}
    tried, resolved = int(sample.get("tried", 0)), int(sample.get("resolved", 0))
    if tried:
        rate = resolved / tried
        if rate < DESCRIPTION_FLOOR:
            found.append({
                "source": "job descriptions", "severity": "broken",
                "kind": "descriptions",
                "detail": (
                    f"Only {resolved} of {tried} sampled postings returned their "
                    "advert. Tailoring reads whatever this returns, so it "
                    "degrades without any error."
                ),
            })

    order = {"broken": 0, "watch": 1}
    found.sort(key=lambda item: (order.get(item["severity"], 2), item["source"]))
    return found


def summary(history: dict[str, Any] | None = None) -> dict[str, Any]:
    """Headline reliability figures, for the dashboard and for a reader."""
    history = history or load_history()
    runs = history.get("runs") or []
    if not runs:
        return {"runs": 0, "sources": 0, "healthy": 0, "broken": 0, "watch": 0}
    latest = runs[-1]
    current = alerts(history)
    broken = {item["source"] for item in current if item["severity"] == "broken"}
    watch = {item["source"] for item in current if item["severity"] == "watch"}
    sources = set(latest.get("sources", {}))
    sample = latest.get("descriptions") or {}
    return {
        "date": latest.get("date", ""),
        "runs": len(runs),
        "sources": len(sources),
        "healthy": len(sources - broken - watch),
        "broken": len(broken),
        "watch": len(watch),
        "rows": sum(
            int(entry.get("rows", 0)) for entry in latest.get("sources", {}).values()
        ),
        "description_rate": (
            round(int(sample.get("resolved", 0)) / int(sample["tried"]), 3)
            if sample.get("tried") else None
        ),
    }


def sample_descriptions(tracker: Path, limit: int = 12) -> dict[str, int]:
    """Check that postings still hand back their advert.

    Spread across providers rather than taken from the top of the file, so one
    provider changing its API is visible instead of averaged away.
    """
    try:
        from autoapply.jobs import fetch_description, jobs_from_tracker
    except ImportError:
        return {}
    try:
        jobs = [job for job in jobs_from_tracker(tracker, include_unknown=True)]
    except (OSError, ValueError):
        return {}
    if not jobs:
        return {}
    by_ats: dict[str, list[Any]] = {}
    for job in jobs:
        by_ats.setdefault(job.ats, []).append(job)
    chosen: list[Any] = []
    while len(chosen) < limit and any(by_ats.values()):
        for group in by_ats.values():
            if group and len(chosen) < limit:
                chosen.append(group.pop(len(group) // 2))
    resolved = 0
    for job in chosen:
        try:
            if len(fetch_description(job) or "") >= 400:
                resolved += 1
        except Exception:
            pass
    return {"tried": len(chosen), "resolved": resolved}


def report(history: dict[str, Any] | None = None) -> str:
    history = history or load_history()
    figures = summary(history)
    if not figures.get("runs"):
        return "No source history recorded yet. Run the watcher once."
    lines = [
        f"Source health for {figures.get('date', 'the latest run')}",
        f"  {figures['sources']} sources, {figures['rows']} rows, "
        f"{figures['runs']} runs of history",
        f"  {figures['healthy']} healthy · {figures['broken']} broken · "
        f"{figures['watch']} worth watching",
    ]
    if figures.get("description_rate") is not None:
        lines.append(
            f"  descriptions resolving: {figures['description_rate'] * 100:.0f}%"
        )
    current = alerts(history)
    if not current:
        lines.append("\nNothing to report.")
        return "\n".join(lines)
    lines.append("")
    for item in current:
        mark = "BROKEN " if item["severity"] == "broken" else "watch  "
        lines.append(f"{mark} {item['source']}: {item['detail']}")
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover - operator entry point
    print(report())
