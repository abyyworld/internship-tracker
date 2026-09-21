#!/usr/bin/env python3
"""Build the public, filterable GitHub Pages job dashboard."""

from __future__ import annotations

import csv
from datetime import date
import json
from pathlib import Path
from urllib.parse import urlsplit

import scorecard
from funding import load_schemes
from ventures import load_programmes
from source_health import alerts as health_alerts, summary as health_summary
from dashboard_page import TEMPLATE
from universities import (
    _index,
    annotate,
    load_universities,
    supervisor_links,
)


ROOT = Path(__file__).resolve().parent
TRACKER = ROOT / "tracker.csv"
OUTPUT = ROOT / "docs" / "index.html"
ATS_SUFFIXES = ("greenhouse.io", "lever.co", "ashbyhq.com")

# Categories the dashboard chips can filter on. Must stay in sync with
# CATEGORY_ORDER in the page template and category_of() in the watcher.
KNOWN_CATEGORIES = {
    "AI / ML",
    "Software Engineering",
    "Quant / Finance",
    "Robotics & Embodied AI",
    "Security",
    "Data",
    "Systems & Infra",
    "Hardware / EE",
    "HCI / XR",
    "Computational Science",
}

# Rows scraped before the category rename keep their old label. Without this
# map their chip never matches and the jobs become unreachable by any filter.
LEGACY_CATEGORIES = {
    "Quant": "Quant / Finance",
    "HCI": "HCI / XR",
    "Robotics": "Robotics & Embodied AI",
    "Bioinformatics": "Computational Science",
    "Systems": "Systems & Infra",
    "Hardware": "Hardware / EE",
}


def normalize_tier(company: str, stored: str) -> str:
    """Recompute a row's tier from the current watchlists.

    Tier is written when a row is scraped, so a row discovered before the
    tiers were rebalanced keeps its old value — which is how every FAANG
    posting stayed on "high" while smaller firms showed as "elite".
    """
    try:
        from internship_watcher import tier_of
    except Exception:
        return (stored or "").strip()
    return tier_of(company or "") or ""


def normalize_category(stored: str, company: str, role: str) -> str:
    """Map a tracker row onto a current chip label.

    Rows keep whatever category the watcher assigned when it scraped them, so
    after a rename or a new category is added the stored value can be stale.
    Renames are mapped directly; anything still unrecognised is reclassified
    with the watcher's own classifier so there is a single source of truth.
    """
    value = (stored or "").strip()
    if value in KNOWN_CATEGORIES:
        return value
    if value in LEGACY_CATEGORIES:
        return LEGACY_CATEGORIES[value]
    try:
        from internship_watcher import category_of
    except Exception:
        return value or "Software Engineering"
    return category_of(company, role)


def safe_url(value: str) -> str:
    candidate = (value or "").strip()
    try:
        parsed = urlsplit(candidate)
    except ValueError:
        return ""
    if parsed.scheme != "https" or not parsed.hostname:
        return ""
    return candidate


def ats_supported(value: str) -> bool:
    hostname = (urlsplit(value).hostname or "").lower()
    return any(
        hostname == suffix or hostname.endswith(f".{suffix}")
        for suffix in ATS_SUFFIXES
    )


def load_jobs() -> list[dict[str, object]]:
    with TRACKER.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            # A funded research programme is not a job posting, but it is an
            # opportunity with a date, and the page it feeds is a matcher
            # rather than a job board.
            if row.get("record_kind", "posting") in {"posting", "programme"}
            and row.get("source_status") == "open"
        ]
    # Academic postings rarely name a supervisor, so match the institution once
    # and let each such job carry links to its real, current faculty.
    index = _index(load_universities())
    campuses = scorecard.index()
    jobs: list[dict[str, object]] = []
    for row in rows:
        url = safe_url(row.get("url", ""))
        jobs.append(
            {
                "id": row.get("id", ""),
                "company": row.get("company", ""),
                "role": row.get("role", ""),
                "category": normalize_category(
                    row.get("category", ""),
                    row.get("company", ""),
                    row.get("role", ""),
                ),
                "position_type": row.get("role_type", ""),
                "region": row.get("region", "Unknown"),
                "location": row.get("location", ""),
                "term": row.get("term", "Unknown"),
                "level": row.get("level", "Unknown"),
                "work_mode": row.get("work_mode", "unspecified"),
                "tier": normalize_tier(
                    row.get("company", ""), row.get("elite_tier", "")
                ),
                "focus": row.get("focus_tags", ""),
                "company_type": row.get("company_type", "unknown"),
                "company_signal": row.get("company_signal", ""),
                "equity_signal": row.get("equity_signal", "unknown"),
                "eligibility": row.get("eligibility", "review required"),
                "deadline": row.get("deadline", ""),
                "first_seen": row.get("first_seen", ""),
                "last_seen": row.get("last_seen", ""),
                # fix: column is "NEW" (all-caps), not "discovered_new"
                "new": row.get("NEW", "").upper() == "YES",
                "url": url,
                "tailor": bool(url),
                "official_ats": bool(url and ats_supported(url)),
            }
        )
        annotate(jobs[-1], index)
        university = jobs[-1].get("university")
        if university and university.get("country") == "United States":
            figures = scorecard.lookup(university["name"], campuses)
            if figures:
                university["scorecard"] = {
                    "admission_rate": figures.get("admission_rate"),
                    "students": figures.get("students"),
                    "tuition": figures.get("tuition_out_of_state"),
                    "earnings": figures.get("earnings_10yr_median"),
                    "summary": scorecard.describe(figures),
                }
    return jobs


def universities_for_page(jobs: list[dict[str, object]]) -> list[dict[str, object]]:
    """The institutions themselves, not only the postings at them.

    "Which university, and why" is a real question for anyone choosing where to
    apply, and the honest answer is figures somebody else publishes: the world
    rank, and for US institutions the federal Scorecard's admission rate, size,
    tuition and earnings. The links go to current faculty rather than to a list
    of names that would be stale within a term.
    """
    campuses = scorecard.index()
    openings: dict[str, int] = {}
    for job in jobs:
        university = job.get("university")
        if university:
            name = str(university.get("name", ""))
            openings[name] = openings.get(name, 0) + 1
    listed = []
    for entry in load_universities():
        name = str(entry.get("name", ""))
        record = {
            "name": name,
            "country": entry.get("country", ""),
            "rank": entry.get("rank"),
            "domain": entry.get("domain", ""),
            "openings": openings.get(name, 0),
            "links": supervisor_links(entry, []),
        }
        figures = scorecard.lookup(name, campuses)
        if figures:
            record["scorecard"] = {
                "admission_rate": figures.get("admission_rate"),
                "students": figures.get("students"),
                "tuition": figures.get("tuition_out_of_state"),
                "earnings": figures.get("earnings_10yr_median"),
                "summary": scorecard.describe(figures),
            }
        listed.append(record)
    return listed


def json_for_script(value: object) -> str:
    return (
        json.dumps(value, ensure_ascii=True, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def build() -> int:
    jobs = load_jobs()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    # Reliability is published deliberately. A job dataset nobody audits is
    # worth nothing, and the failures here are the kind that hide.
    health = {"summary": health_summary(), "alerts": health_alerts()[:8]}
    # Funding is listed for everyone rather than matched here: matching needs
    # the private profile, and this page is public.
    schemes = [
        {
            key: value for key, value in scheme.items()
            if key in {"id", "name", "funder", "country", "levels", "eligibility",
                       "covers", "cycle", "url"}
        }
        for scheme in load_schemes()
    ]
    page = (
        TEMPLATE.replace("__JOBS__", json_for_script(jobs))
        .replace("__HEALTH__", json_for_script(health))
        .replace("__FUNDING__", json_for_script(schemes))
        .replace("__VENTURES__", json_for_script(load_programmes()))
        .replace("__UNIVERSITIES__", json_for_script(universities_for_page(jobs)))
        .replace("__GENERATED__", date.today().isoformat())
    )
    OUTPUT.write_text(page, encoding="utf-8")
    return len(jobs)


# Both workflows publish this page by running `python dashboard.py`. Without
# this, that command imports the module, defines build(), and exits having
# written nothing — so the daily watch refreshed tracker.csv while the public
# dashboard kept serving whatever snapshot was last committed by hand.
if __name__ == "__main__":
    print(f"{OUTPUT.relative_to(ROOT)}: {build()} opportunities")
