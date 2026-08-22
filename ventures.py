#!/usr/bin/env python3
"""Match venture programmes to the person looking for them.

The tracker answers "who will employ me". This answers the other question a
student with a working project eventually asks: who will fund me to build it
instead. Accelerators, talent investors, founder fellowships, equity-free
grants and the occasional loan — all of them opportunities, none of them jobs.

The rules are the same as for funding, and for the same reasons:

* Cohort dates are not stored. They move every year, and a stale date
  presented as fact is worse than no date at all, so each programme records
  the shape of its cycle and links to the page that governs it.
* Cheque sizes and equity are recorded only where the programme publishes
  them. Where terms vary by location or batch, the entry says so rather than
  quoting a number that is right for one city and wrong for another.

What is worth matching on is not the money. It is whether a person is even
allowed to apply: a PhD student in the UK and a repeat founder in San
Francisco are shown almost disjoint lists, and the usual failure is never
learning that the first list existed.

Standard library only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATA_FILE = Path(__file__).resolve().parent / "data" / "ventures.json"

# What the programme is, in the order a person moves through them.
KINDS = (
    "grant",
    "fellowship",
    "talent investor",
    "accelerator",
    "venture studio",
    "venture fund",
    "programme",
    "loan",
)

# How far along the work is. "pre-team" is a real stage here: several
# programmes exist precisely to be joined before there is a company at all.
STAGE_ORDER = (
    "research",
    "pre-team",
    "idea",
    "pre-seed",
    "seed",
    "series-a",
)

AUDIENCES = ("students", "phd", "researchers", "anyone")

AUDIENCE_ALIASES = {
    "student": "students",
    "undergraduate": "students",
    "undergrad": "students",
    "masters": "students",
    "doctoral": "phd",
    "doctorate": "phd",
    "postgraduate": "phd",
    "postdoc": "researchers",
    "researcher": "researchers",
    "academic": "researchers",
    "everyone": "anyone",
    "": "anyone",
}


def load_programmes(path: Path = DATA_FILE) -> list[dict[str, Any]]:
    """Every programme in the dataset that is complete enough to show.

    A half-filled entry is worse than a missing one: it takes up a card and
    tells the reader nothing they can act on.
    """
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    required = ("id", "name", "kind", "url", "eligibility", "cycle")
    return [
        programme
        for programme in payload.get("programmes", [])
        if isinstance(programme, dict)
        and all(str(programme.get(field, "")).strip() for field in required)
        and str(programme.get("url", "")).startswith("https://")
    ]


def normalise_audience(value: str) -> str:
    text = str(value or "").strip().lower()
    return AUDIENCE_ALIASES.get(text, text if text in AUDIENCES else "anyone")


def takes_no_equity(programme: dict[str, Any]) -> bool:
    """Whether applying costs a share of the company.

    The most useful single filter in the set. A grant and an accelerator are
    both "funding", and choosing between them is a different decision from
    choosing between two accelerators.
    """
    return str(programme.get("equity", "")).strip().lower().startswith("none")


def open_to(programme: dict[str, Any], audience: str) -> bool:
    wanted = normalise_audience(audience)
    listed = {normalise_audience(item) for item in programme.get("audience", [])}
    # "anyone" in the data means no audience restriction, so it matches every
    # reader; "anyone" as a question means show everything.
    return wanted == "anyone" or "anyone" in listed or wanted in listed


def in_region(programme: dict[str, Any], region: str) -> bool:
    wanted = str(region or "").strip().upper()
    if not wanted:
        return True
    listed = {str(item).strip().upper() for item in programme.get("regions", [])}
    return not listed or "GLOBAL" in listed or wanted in listed


def at_stage(programme: dict[str, Any], stage: str) -> bool:
    wanted = str(stage or "").strip().lower()
    if not wanted:
        return True
    return wanted in {str(item).strip().lower() for item in programme.get("stage", [])}


def match_programmes(
    programmes: list[dict[str, Any]] | None = None,
    *,
    audience: str = "anyone",
    region: str = "",
    stage: str = "",
    equity_free_only: bool = False,
) -> list[dict[str, Any]]:
    """The programmes a particular person can actually apply to, best first.

    Ordered by how specifically they are aimed at that person: a fellowship
    written for PhD students beats a global accelerator open to everyone,
    because the first one is the one nobody told them about.
    """
    found = load_programmes() if programmes is None else list(programmes)
    matches = [
        programme
        for programme in found
        if open_to(programme, audience)
        and in_region(programme, region)
        and at_stage(programme, stage)
        and (not equity_free_only or takes_no_equity(programme))
    ]
    wanted = normalise_audience(audience)

    def rank(programme: dict[str, Any]) -> tuple[int, int, str]:
        listed = {normalise_audience(item) for item in programme.get("audience", [])}
        aimed_here = 0 if (wanted != "anyone" and wanted in listed) else 1
        regions = {str(item).strip().upper() for item in programme.get("regions", [])}
        local = 0 if (region and str(region).upper() in regions) else 1
        return (aimed_here, local, str(programme.get("name", "")).lower())

    return sorted(matches, key=rank)


def summary(matches: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"total": len(matches), "no_equity": 0}
    for programme in matches:
        if takes_no_equity(programme):
            counts["no_equity"] += 1
        kind = str(programme.get("kind", "other"))
        counts[kind] = counts.get(kind, 0) + 1
    return counts


def report(
    audience: str = "anyone", region: str = "", stage: str = ""
) -> str:
    """A plain-text listing, for the terminal and for the digests."""
    matches = match_programmes(audience=audience, region=region, stage=stage)
    if not matches:
        return "No venture programmes match that description."
    counts = summary(matches)
    lines = [
        f"{counts['total']} venture programmes "
        f"({counts['no_equity']} take no equity)",
        "",
    ]
    for programme in matches:
        equity = "no equity" if takes_no_equity(programme) else "takes equity"
        lines.append(f"{programme['name']} — {programme.get('organisation', '')}")
        lines.append(f"    {programme['kind']} · {equity}")
        lines.append(f"    who    : {programme['eligibility']}")
        lines.append(f"    cycle  : {programme['cycle']}")
        lines.append(f"    apply  : {programme['url']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audience", default="anyone", help="students, phd, researchers, anyone")
    parser.add_argument("--region", default="", help="GB, EU, US")
    parser.add_argument("--stage", default="", help=", ".join(STAGE_ORDER))
    args = parser.parse_args()
    print(report(args.audience, args.region, args.stage), end="")
