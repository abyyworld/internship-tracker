#!/usr/bin/env python3
"""Match funding schemes to the person looking for them.

Funding is the part of academia that hurts most and is advertised worst. It
is scattered across research councils, embassies, charities, and single
university pages, each with its own calendar, and the usual failure is not
being rejected — it is finding out in March that the thing closed in
November.

There is no marketplace to build here. Nobody is sitting on PhD money
looking for a student: it flows from councils and trusts to institutions on
fixed annual cycles. What is missing is simply a list of what exists, who may
apply, and when it opens. That is what this is.

Deadlines are deliberately not stored as dates. They move every year, and a
stale date presented as fact is worse than no date at all, so each scheme
records its usual window and links to the page that actually governs it.

Standard library only.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


DATA_FILE = Path(__file__).resolve().parent / "data" / "funding.json"

# Study stages in order, so "what am I eligible for next" is answerable.
LEVEL_ORDER = ("undergraduate", "masters", "phd", "postdoc", "research")

LEVEL_ALIASES = {
    "bachelor": "undergraduate",
    "bachelors": "undergraduate",
    "bsc": "undergraduate",
    "undergrad": "undergraduate",
    "master": "masters",
    "msc": "masters",
    "meng": "masters",
    "doctoral": "phd",
    "doctorate": "phd",
    "postdoctoral": "postdoc",
}


def load_schemes(path: Path = DATA_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return [
        scheme
        for scheme in payload.get("schemes", [])
        if isinstance(scheme, dict) and scheme.get("id") and scheme.get("url")
    ]


def normalise_level(value: str) -> str:
    text = re.sub(r"[^a-z]+", "", str(value or "").lower())
    text = LEVEL_ALIASES.get(text, text)
    return text if text in LEVEL_ORDER else ""


def _next_levels(level: str) -> list[str]:
    """The stage someone is at, and the ones they are heading towards."""
    if level not in LEVEL_ORDER:
        return list(LEVEL_ORDER)
    index = LEVEL_ORDER.index(level)
    return list(LEVEL_ORDER[index:])


def match_schemes(
    profile: dict[str, Any],
    schemes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Order schemes by how close they are to being usable by this person.

    `now` is the stage they are at. `next` is the stage after, which is where
    almost every deadline that matters actually sits: a master's scholarship
    closes a year before the course starts, so an undergraduate who waits
    until they are a graduate has already missed it.
    """
    schemes = schemes if schemes is not None else load_schemes()
    education = profile.get("education") or {}
    level = normalise_level(
        education.get("level") if isinstance(education, dict) else ""
    )
    upcoming = _next_levels(level)
    following = upcoming[1] if len(upcoming) > 1 else ""

    citizenships = {
        str(code).upper() for code in profile.get("citizenships", []) if str(code).strip()
    }

    results = []
    for scheme in schemes:
        levels = {normalise_level(value) for value in scheme.get("levels", [])}
        levels.discard("")
        if level and level in levels:
            timing = "now"
        elif following and following in levels:
            timing = "next"
        elif levels & set(upcoming):
            timing = "later"
        else:
            timing = "past"

        eligibility = str(scheme.get("eligibility", ""))
        restricted = bool(
            re.search(r"\bUS citizens?\b|\bcitizens? of the (?:US|United States)\b",
                      eligibility)
        )
        blocked = restricted and "US" not in citizenships
        results.append({
            **scheme,
            "timing": timing,
            "blocked": blocked,
            "blocked_reason": (
                "Restricted to US citizens and permanent residents" if blocked else ""
            ),
        })

    order = {"now": 0, "next": 1, "later": 2, "past": 3}
    results.sort(
        key=lambda item: (
            item["blocked"],
            order.get(item["timing"], 4),
            item["name"],
        )
    )
    return results


def summary(matches: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(matches),
        "now": sum(1 for m in matches if m["timing"] == "now" and not m["blocked"]),
        "next": sum(1 for m in matches if m["timing"] == "next" and not m["blocked"]),
        "blocked": sum(1 for m in matches if m["blocked"]),
    }


def report(profile: dict[str, Any]) -> str:
    matches = match_schemes(profile)
    if not matches:
        return "No funding schemes are recorded."
    figures = summary(matches)
    lines = [
        f"{figures['total']} schemes · {figures['now']} open to you at your current "
        f"stage · {figures['next']} for the stage after",
    ]
    labels = {"now": "NOW  ", "next": "NEXT ", "later": "later", "past": "past "}
    for match in matches:
        if match["blocked"]:
            continue
        lines.append(
            f"  {labels.get(match['timing'], '     ')} {match['name'][:44]:46}"
            f"{match.get('cycle', '')[:52]}"
        )
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover - operator entry point
    import yaml  # noqa: PLC0415 - optional, only for the local report

    profile_path = Path(__file__).resolve().parent / "private" / "profile.yaml"
    loaded = yaml.safe_load(profile_path.read_text(encoding="utf-8")) if profile_path.exists() else {}
    print(report(loaded))
