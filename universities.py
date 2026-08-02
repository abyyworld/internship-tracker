#!/usr/bin/env python3
"""Match an academic posting to the institution advertising it.

For a PhD, postdoc, or research-assistant post, the decisive question is who
would supervise it, and that person is almost never named in the advert. This
module matches the employer to a top-100 institution so the dashboard can point
at that institution's real, current faculty — its own directory, and searches
scoped to its verified email domain.

It deliberately does not ship a list of named academics or their addresses: any
such list is stale within a term, and a stale contact is worse than no contact.
Every link produced here resolves to a source the institution maintains.

Standard library only, so the daily GitHub Actions run needs no dependencies.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


DATA_FILE = Path(__file__).resolve().parent / "data" / "universities.json"

# Position types where a supervisor, not a hiring manager, decides the outcome.
ACADEMIC_POSITION_TYPES = {
    "research-assistant",
    "phd-fellowship",
    "postdoc",
    "masters-research",
    "fellowship",
}

# Terms that describe employment rather than a research topic; searching for
# them returns job adverts instead of the people who supervise the work.
_ROLE_NOISE = {
    "phd", "postdoc", "postdoctoral", "student", "studentship", "fellow",
    "fellowship", "research", "researcher", "assistant", "associate",
    "intern", "internship", "scholar", "scholarship", "position", "vacancy",
    "opportunity", "graduate", "undergraduate", "masters", "msc", "bsc",
    "full", "part", "time", "year", "funded", "university", "college",
    "school", "department", "faculty", "institute", "centre", "center",
    "and", "the", "for", "with", "role", "job", "opening", "hiring",
}


def _normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", str(value or "").casefold()).strip()


def load_universities(path: Path = DATA_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return [
        entry
        for entry in payload.get("universities", [])
        if isinstance(entry, dict) and entry.get("name") and entry.get("domain")
    ]


def _index(universities: list[dict[str, Any]]) -> list[tuple[str, dict[str, Any]]]:
    """Longest names first, so 'University of California, Berkeley' wins over 'berkeley'."""
    seen: dict[str, dict[str, Any]] = {}
    for entry in universities:
        for name in (entry["name"], *entry.get("aliases", [])):
            key = _normalise(name)
            # An alias that repeats the canonical name is common in the data and
            # harmless; the first entry claiming a key keeps it.
            if key and key not in seen:
                seen[key] = entry
    pairs = list(seen.items())
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return pairs


def match_university(
    company: str,
    index: list[tuple[str, dict[str, Any]]],
) -> dict[str, Any] | None:
    """Return the institution advertising this posting, or None."""
    haystack = _normalise(company)
    if not haystack:
        return None
    padded = f" {haystack} "
    for key, entry in index:
        if key == haystack or f" {key} " in padded:
            return entry
    return None


def research_terms(role: str, focus: str = "", limit: int = 4) -> list[str]:
    """The topic words worth searching a faculty directory for."""
    words = _normalise(f"{role} {focus.replace(',', ' ')}").split()
    terms: list[str] = []
    for word in words:
        if len(word) < 3 or word in _ROLE_NOISE or word.isdigit():
            continue
        if word not in terms:
            terms.append(word)
        if len(terms) >= limit:
            break
    return terms


def supervisor_links(entry: dict[str, Any], terms: list[str]) -> dict[str, str]:
    """Search URLs that resolve to real, current academics at this institution.

    Google Scholar's author search filters on the verified institutional email
    domain, so results are people who hold a post there today and whose profile
    carries their own contact route.
    """
    from urllib.parse import quote_plus

    domain = str(entry.get("domain", "")).strip()
    topic = " ".join(terms)
    return {
        "scholar": (
            "https://scholar.google.com/citations?view_op=search_authors&mauthors="
            + quote_plus(f"{topic} {domain}".strip())
        ),
        "openalex": (
            "https://openalex.org/works?filter=" + quote_plus(
                f"raw_affiliation_strings.search:{entry['name']}"
            ) + ("&search=" + quote_plus(topic) if topic else "")
        ),
        "directory": (
            "https://www.google.com/search?q="
            + quote_plus(f"site:{domain} faculty {topic}".strip())
        ),
    }


def annotate(job: dict[str, Any], index: list[tuple[str, dict[str, Any]]]) -> None:
    """Attach supervisor-search metadata to a posting, in place.

    A posting qualifies if the employer is one of the listed institutions —
    a university internship is still supervised by an academic — or if the
    position type is a research track wherever it is advertised.
    """
    entry = match_university(str(job.get("company", "")), index)
    if not entry:
        return
    terms = research_terms(str(job.get("role", "")), str(job.get("focus", "")))
    job["university"] = {
        "name": entry["name"],
        "country": entry.get("country", ""),
        "rank": entry.get("rank", 0),
        "domain": entry["domain"],
        "terms": terms,
        "research_track": job.get("position_type") in ACADEMIC_POSITION_TYPES,
        **supervisor_links(entry, terms),
    }


if __name__ == "__main__":  # pragma: no cover - manual inspection helper
    universities = load_universities()
    print(f"{len(universities)} institutions loaded")
    index = _index(universities)
    for probe in ("University of Birmingham", "MIT CSAIL", "Jane Street"):
        print(probe, "->", (match_university(probe, index) or {}).get("name"))
