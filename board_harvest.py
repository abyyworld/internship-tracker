#!/usr/bin/env python3
"""Find company job boards in a public crawl of the web, not by hand.

board_discovery.py learns a board from a posting the tracker happens to meet,
which is a good way to grow and a slow one: it can only ever know the companies
some community repo already listed. It took the source list from 147 boards to
433, and 433 is still three orders of magnitude short of what an aggregator
polls.

The aggregators are not doing anything clever. Greenhouse, Lever and Ashby each
serve a company's jobs as public JSON from a URL containing the company's board
name, and every one of those pages has been crawled. Common Crawl publishes an
index of every URL in its crawls, queryable by prefix, free, with no key — so
"every Greenhouse board the web knows about" is a query rather than a research
project. That is the same public record anyone can read, and it names only
boards their owners published.

What this does NOT do is read another tracker's database. Their postings are
their product; the boards are the open web.

Two deliberate limits. The index is queried for board addresses only, never for
postings — a posting read from a crawl is months stale, while the board it
names answers live. And the harvest is capped per run: a source list that
triples overnight is one whose failures nobody can read, and a board that
cannot be polled inside the daily job's twenty minutes is not coverage.
"""

from __future__ import annotations

import collections
import json
import re
import urllib.parse
import urllib.request

# The three whose public JSON the watcher can already parse. Adding a provider
# here without a parser would grow the board count and not the job count.
PREFIXES = {
    "Greenhouse": ["boards.greenhouse.io/", "job-boards.greenhouse.io/"],
    "Lever": ["jobs.lever.co/"],
    "Ashby": ["jobs.ashbyhq.com/"],
}

# Path segments that are the URL's plumbing rather than a company.
NOT_A_BOARD = {
    "embed", "job_board", "jobs", "job", "api", "v1", "v0", "boards", "board",
    "posting-api", "postings", "www", "en", "us", "search", "careers", "career",
    "index", "static", "assets", "favicon.ico", "robots.txt", "sitemap.xml",
}

SLUG = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")


def slug_of(url: str, provider: str):
    """The board name inside a crawled URL, or None if it names no board."""
    for prefix in PREFIXES.get(provider, []):
        cut = url.find(prefix)
        if cut < 0:
            continue
        rest = url[cut + len(prefix):]
        slug = rest.split("/")[0].split("?")[0].split("#")[0].strip().lower()
        # Greenhouse's embed form carries the board in a query string.
        if slug in {"embed", "job_board"}:
            query = urllib.parse.urlparse(url).query
            slug = urllib.parse.parse_qs(query).get("for", [""])[0].strip().lower()
        if not slug or slug in NOT_A_BOARD or not SLUG.match(slug):
            continue
        return slug
    return None


def slugs_in(lines, provider: str) -> collections.Counter:
    """Every board named in a page of index records, by how often it appears.

    Frequency is the only quality signal available here and it is a good one: a
    board crawled on a thousand pages is a company that has been hiring for
    years, and one seen once is as likely to be a typo as a company.
    """
    counted: collections.Counter = collections.Counter()
    for line in lines:
        line = line.strip()
        if not line or line[0] != "{":
            continue                      # blank lines and the API's own errors
        try:
            record = json.loads(line)
        except ValueError:
            continue
        url = record.get("url", "")
        if not url:
            continue
        slug = slug_of(url, provider)
        if slug:
            counted[slug] += 1
    return counted


def index_url(crawl: str, prefix: str, page: int, page_size: int = 5) -> str:
    query = urllib.parse.urlencode({
        "url": f"{prefix}*", "output": "json",
        "page": page, "pageSize": page_size, "filter": "=status:200",
    })
    return f"https://index.commoncrawl.org/{crawl}-index?{query}"


def harvest(crawl: str, fetch, pages: int = 4, seen_at_least: int = 2) -> dict:
    """Board names per provider, from `pages` pages of the crawl index.

    `fetch` is passed in rather than called directly so the parsing — which is
    where every mistake here would live — is testable without the network, and
    so a failing page costs that page rather than the run.
    """
    found: dict[str, collections.Counter] = {}
    for provider, prefixes in PREFIXES.items():
        counted: collections.Counter = collections.Counter()
        for prefix in prefixes:
            for page in range(pages):
                try:
                    body = fetch(index_url(crawl, prefix, page))
                except Exception:
                    break            # a page that will not load ends that prefix
                if not body:
                    break
                counted.update(slugs_in(body.splitlines(), provider))
        found[provider] = collections.Counter({
            slug: n for slug, n in counted.items() if n >= seen_at_least
        })
    return found


def latest_crawl(fetch) -> str:
    """Which crawl to read. Asked rather than hardcoded.

    Common Crawl publishes a new crawl every few weeks and retires the old
    identifiers from the query API. A hardcoded one works until it silently
    stops, which is the failure this repository has already met three times in
    a day, so the list is read and the newest taken.
    """
    try:
        listed = json.loads(fetch("https://index.commoncrawl.org/collinfo.json"))
    except Exception:
        return ""
    if not isinstance(listed, list):
        return ""
    for entry in listed:                       # newest first, per the API
        name = (entry or {}).get("id", "")
        if isinstance(name, str) and name.startswith("CC-MAIN-"):
            return name
    return ""


def fetch(url: str, timeout: int = 60) -> str:
    request = urllib.request.Request(url, headers={
        "User-Agent": "internship-tracker board harvest (+https://github.com/abyyworld/internship-tracker)",
    })
    with urllib.request.urlopen(request, timeout=timeout) as answer:
        return answer.read().decode("utf-8", "replace")


def add_to(store: dict, found: dict, today: str, known=(), cap: int = 1500) -> list:
    """File the harvest, best-attested first, up to the cap.

    Capped because the daily job has twenty minutes and because a source list
    that triples overnight produces a failure report nobody reads. What is left
    over is not lost: the crawl is still there next run, and the boards that
    matter most are the ones this takes first.
    """
    already = {(provider, slug) for provider, slug in known}
    ranked = sorted(
        ((provider, slug, n) for provider, counted in found.items()
         for slug, n in counted.items()),
        key=lambda row: (-row[2], row[0], row[1]),
    )
    added = []
    for provider, slug, seen in ranked:
        if len(added) >= cap:
            break
        if (provider, slug) in already:
            continue
        boards = store.setdefault(provider, {})
        if slug in boards:
            boards[slug]["crawl_seen"] = seen
            continue
        boards[slug] = {
            # No posting taught us this one, so there is no company name to
            # take. The board answers with its own once it is polled.
            "name": slug.replace("-", " ").replace("_", " ").title(),
            "first_seen": today, "last_seen": today,
            "misses": 0, "roles": 0, "crawl_seen": seen, "from_crawl": True,
        }
        added.append(f"{provider}/{slug}")
    return added
