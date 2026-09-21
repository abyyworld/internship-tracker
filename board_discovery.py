#!/usr/bin/env python3
"""Every posting we read names the board it came from. Keep the address.

The watcher polls a hand-written list of company boards. That list is the
ceiling on what it can ever find, and a hand-written list stops growing the
week somebody stops maintaining it — which is the whole difference between
this tracker and the aggregators it is measured against. They do not know a
technique we lack; they poll tens of thousands of boards where we poll a
hundred and fifty.

But we already meet far more boards than we poll. A community repo hands us a
posting at jobs.ashbyhq.com/zoox/<uuid>; we read the one job and throw away the
address of the board it came from — a board that will carry Zoox's next fifty
postings and that we would never have to be told about again. Measured against
the tracker as it stands: 147 boards polled, 690 board addresses sitting unread
in the URLs of rows already collected.

So the source list discovers itself. Any URL that names a Greenhouse, Lever or
Ashby board is remembered with the company name that posting carried, polled
from then on, and dropped again if it stops answering. Nothing here fetches
anything: it reads URLs the watcher already has and writes a list for it to
read. The three providers are the ones whose public APIs answer a plain GET and
that the watcher can already parse — Workday and iCIMS addresses are recorded
too, so the count is honest, but they are not polled, because nothing here can
read them yet.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

STORE = Path(__file__).resolve().parent / "data" / "discovered_boards.json"

# Providers whose public JSON the watcher can already read. Recorded-only
# providers are listed separately: pretending we can poll them would make the
# coverage number a lie.
POLLABLE = ("Greenhouse", "Lever", "Ashby")

BOARD_PATTERNS = [
    # Greenhouse embeds the board in a query string as often as in the path.
    ("Greenhouse", re.compile(r"greenhouse\.io/embed/job_board\?for=([A-Za-z0-9_-]+)", re.I)),
    ("Greenhouse", re.compile(r"(?:boards|job-boards)\.greenhouse\.io/([A-Za-z0-9_-]+)", re.I)),
    ("Greenhouse", re.compile(r"boards-api\.greenhouse\.io/v1/boards/([A-Za-z0-9_-]+)", re.I)),
    ("Lever", re.compile(r"jobs\.lever\.co/([A-Za-z0-9_-]+)", re.I)),
    ("Lever", re.compile(r"api\.lever\.co/v0/postings/([A-Za-z0-9_-]+)", re.I)),
    ("Ashby", re.compile(r"jobs\.ashbyhq\.com/([A-Za-z0-9_.-]+)", re.I)),
    ("Ashby", re.compile(r"api\.ashbyhq\.com/posting-api/job-board/([A-Za-z0-9_.-]+)", re.I)),
    # Recorded, not polled — see the module docstring.
    ("Workday", re.compile(r"([A-Za-z0-9-]+)\.(?:wd\d+\.)?myworkday(?:jobs|site)\.com", re.I)),
    ("iCIMS", re.compile(r"([A-Za-z0-9-]+)\.icims\.com", re.I)),
    ("SmartRecruiters", re.compile(r"jobs\.smartrecruiters\.com/([A-Za-z0-9_-]+)", re.I)),
    ("Workable", re.compile(r"apply\.workable\.com/([A-Za-z0-9_-]+)", re.I)),
]

# Path segments that are part of the URL's plumbing rather than a company. A
# board called "embed" or "job_board" would be polled forever and never answer.
NOT_A_BOARD = {
    "embed", "job_board", "jobs", "job", "api", "v1", "v0", "boards", "board",
    "posting-api", "postings", "www", "en", "us", "search", "careers", "career",
}


def slug_from(url: str):
    """The (provider, slug) a URL names, or None if it names no board."""
    if not url:
        return None
    for provider, pattern in BOARD_PATTERNS:
        found = pattern.search(url)
        if not found:
            continue
        slug = found.group(1).strip().lower().rstrip(".")
        if not slug or slug in NOT_A_BOARD or len(slug) < 2:
            continue
        return provider, slug
    return None


def load(path: Path = STORE) -> dict:
    try:
        stored = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return stored if isinstance(stored, dict) else {}


def save(store: dict, path: Path = STORE) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Sorted so the daily commit shows what changed rather than a reshuffle.
    ordered = {
        provider: dict(sorted(boards.items()))
        for provider, boards in sorted(store.items())
    }
    path.write_text(json.dumps(ordered, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def harvest(seen, store: dict, today: str, known=()) -> int:
    """Remember every board the given (url, company) pairs name.

    The company name comes from the posting rather than from the slug, because
    the slug is a guess at a name and the posting is the name. "sambanovasystems"
    is not what anybody calls SambaNova Systems.
    """
    already = {(provider, slug) for provider, slug in known}
    added = 0
    for url, company in seen:
        found = slug_from(url)
        if not found:
            continue
        provider, slug = found
        if (provider, slug) in already:
            continue
        boards = store.setdefault(provider, {})
        entry = boards.get(slug)
        name = (company or "").strip() or slug.replace("-", " ").replace("_", " ").title()
        if entry is None:
            boards[slug] = {"name": name, "first_seen": today, "last_seen": today,
                            "misses": 0, "roles": 0}
            added += 1
        else:
            entry["last_seen"] = today
            # A later sighting with a real company name beats a name derived
            # from the slug on the first sighting.
            if company and entry.get("name", "") != company:
                entry["name"] = company
    return added


def boards_for(provider: str, store: dict, exclude=()) -> list:
    """The (slug, name, term) triples the watcher's collect() wants.

    Curated boards win: they carry a hand-checked display name and sometimes a
    term override, and polling the same board twice would double every row.
    """
    skip = {slug.lower() for slug in exclude}
    boards = store.get(provider, {})
    return [
        (slug, entry.get("name") or slug, "None")
        for slug, entry in sorted(boards.items())
        if slug.lower() not in skip
    ]


def record(store: dict, provider: str, slug: str, roles, today: str) -> None:
    """What happened when we polled it. `roles` is None when it did not answer."""
    entry = store.get(provider, {}).get(slug)
    if entry is None:
        return
    if roles is None:
        entry["misses"] = int(entry.get("misses", 0)) + 1
        return
    entry["misses"] = 0
    entry["roles"] = roles
    entry["last_ok"] = today


def prune(store: dict, max_misses: int = 5) -> list:
    """Forget boards that have stopped answering.

    Five runs rather than one: a board that 500s for an afternoon is not a
    board that has gone, and re-discovering it costs a day of missed postings.
    """
    dropped = []
    for provider, boards in store.items():
        for slug in [s for s, e in boards.items()
                     if int(e.get("misses", 0)) >= max_misses]:
            dropped.append(f"{provider}/{slug}")
            del boards[slug]
    return dropped


def summary(store: dict) -> str:
    parts = []
    for provider in sorted(store):
        count = len(store[provider])
        if not count:
            continue
        parts.append(f"{provider} {count}" + ("" if provider in POLLABLE else "*"))
    return ", ".join(parts) + ("   (* recorded, not polled)" if any(
        p not in POLLABLE and store.get(p) for p in store) else "")
