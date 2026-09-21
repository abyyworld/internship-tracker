#!/usr/bin/env python3
"""UK listings that carry a closing date, which almost nothing else here does.

Two gaps in this tracker turned out to be the same gap. Its UK coverage was
230 rows out of 4,548 — 5% — for an applicant whose Student visa is the one
thing making them free to hire in the UK and nowhere else. And of those 4,548
rows, twelve carried a deadline, all of them finance spring weeks written as
"Oct-Nov 2026", which is not a date anything can filter.

The reason is structural. The ATS APIs this scrapes — Greenhouse, Lever, Ashby
— mostly serve US startups, and none of them publishes a closing date, because
a rolling posting does not have one. UK graduate schemes are the opposite: they
open on a date, close on a date, and are gone for a year. The places that
actually track them are UK listing sites, and those are read by people rather
than by APIs.

So this parses what a person can copy out of one. Two formats, both of which
survive a copy-paste out of a browser with the columns intact: a tab-separated
row of the kind The Trackr shows, and the pipe-joined block a Gradcracker
listing becomes. Neither is scraped here; both are parsed from text handed in.

The parsing is deliberately forgiving about everything except the date. A row
whose closing date cannot be read is dropped rather than kept undated, because
an undated row in a deadline-driven lane reads as "no rush" — which is the
failure this whole exercise exists to prevent.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

STORE = Path(__file__).resolve().parent / "data" / "uk_listings.json"

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

# "15 Sep 26" and "September 25th, 2026" are the two a reader meets.
SHORT = re.compile(r"^(\d{1,2})\s+([A-Za-z]{3,9})\s+(\d{2}|\d{4})$")
LONG = re.compile(r"^([A-Za-z]{3,9})\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})$")


def as_date(text: str) -> str:
    """An ISO date, or "" when the text is not one.

    Returning "" rather than guessing is the point: a wrong deadline is worse
    than no row, and a two-digit year read as 1926 would file a live programme
    as long closed.
    """
    text = (text or "").strip()
    if not text:
        return ""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        return text
    found = SHORT.match(text)
    if found:
        day, month, year = found.group(1), found.group(2)[:3].lower(), found.group(3)
    else:
        found = LONG.match(text)
        if not found:
            return ""
        month, day, year = found.group(1)[:3].lower(), found.group(2), found.group(3)
    if month not in MONTHS:
        return ""
    year = int(year)
    if year < 100:
        year += 2000
    try:
        from datetime import date
        return date(year, MONTHS[month], int(day)).isoformat()
    except ValueError:                       # 31 September and friends
        return ""


def _record(company, role, closes, opens="", location="", salary="",
            duration="", starts="", sponsors="", source=""):
    return {
        "company": company.strip(),
        "role": role.strip(),
        "deadline": closes,
        "opens": opens,
        "location": location.strip() or "UK",
        "salary": salary.strip(),
        "duration": duration.strip(),
        "starts": starts.strip(),
        # A UK scheme saying plainly whether it sponsors is rarer than it
        # should be and decides whether an application is worth making.
        "sponsors_visa": sponsors.strip().lower(),
        "source": source,
    }


def parse_trackr(text: str) -> list:
    """Tab-separated rows: company, programme, opening, closing, last year, ..."""
    found = []
    for line in text.splitlines():
        parts = [part.strip() for part in line.rstrip("\n").split("\t")]
        if len(parts) < 2 or not parts[0] or not parts[1]:
            continue
        opens = as_date(parts[2]) if len(parts) > 2 else ""
        closes = as_date(parts[3]) if len(parts) > 3 else ""
        if not closes:
            continue                      # undated reads as "no rush"
        sponsors = ""
        for cell in parts[4:]:
            if cell.lower() in {"yes", "no"}:
                sponsors = cell.lower()
                break
        found.append(_record(parts[0], parts[1], closes, opens=opens,
                             sponsors=sponsors, source="The Trackr"))
    return found


def parse_gradcracker(text: str) -> list:
    """Pipe-joined blocks: company | role | deadline | salary | where | how long | starts."""
    found = []
    for line in text.splitlines():
        parts = [part.strip() for part in line.rstrip("\n").split("|")]
        if len(parts) < 3 or not parts[0] or not parts[1]:
            continue
        closes = as_date(parts[2])
        if not closes:
            continue
        cell = lambda n: parts[n] if len(parts) > n else ""
        found.append(_record(parts[0], parts[1], closes, salary=cell(3),
                             location=cell(4), duration=cell(5), starts=cell(6),
                             source="Gradcracker"))
    return found


def merge(*groups) -> list:
    """One row per company, role, place and date, whichever list it came from.

    Both sites carry the same big employers, and the same Barclays programme in
    London and in Glasgow is two placements rather than a duplicate.
    """
    seen, merged = {}, []
    for group in groups:
        for row in group:
            key = (row["company"].lower(), row["role"].lower(),
                   row["location"].lower(), row["deadline"])
            if key in seen:
                # Keep whichever knows more; the sites carry different columns.
                for field, value in row.items():
                    if value and not seen[key].get(field):
                        seen[key][field] = value
                continue
            seen[key] = row
            merged.append(row)
    merged.sort(key=lambda row: (row["deadline"], row["company"], row["role"]))
    return merged


def load(path: Path = STORE) -> list:
    """What is on disk, keeping only rows that still say when they close."""
    try:
        listed = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if not isinstance(listed, list):
        return []
    return [row for row in listed
            if isinstance(row, dict) and row.get("company") and row.get("role")
            and as_date(row.get("deadline", ""))]


def save(rows: list, path: Path = STORE) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
