#!/usr/bin/env python3
"""US university reference data: how selective, how expensive, what happens after.

From the Department of Education's College Scorecard, which is the
authoritative public source and free to query. The figures people actually
want when deciding where to apply — admission rate, cost, completion, median
earnings — are published there and almost never shown next to the
opportunities themselves.

Fetched once and cached, because the underlying data is annual. The public
DEMO_KEY is enough for a refresh; a personal key from api.data.gov raises the
rate limit if the cache ever needs rebuilding often.

Standard library only.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import ssl
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
CACHE_PATH = ROOT / "data" / "us-universities.json"
ENDPOINT = "https://api.data.gov/ed/collegescorecard/v1/schools.json"
DEMO_KEY = "DEMO_KEY"

FIELDS = (
    "id",
    "school.name",
    "school.city",
    "school.state",
    "school.school_url",
    "latest.admissions.admission_rate.overall",
    "latest.admissions.sat_scores.average.overall",
    "latest.student.size",
    "latest.cost.tuition.out_of_state",
    "latest.completion.rate_suppressed.overall",
    "latest.earnings.10_yrs_after_entry.median",
)

# Common ways an institution's name is written on a job posting versus in the
# federal register.
_NOISE = re.compile(
    r"\b(the|university|univ|college|institute|of|at|and|main|campus)\b", re.I
)


def normalise(name: str) -> str:
    text = re.sub(r"[^a-z0-9 ]+", " ", str(name or "").lower())
    text = _NOISE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_cache(path: Path = CACHE_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "institutions": []}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"schema_version": 1, "institutions": []}
    if not isinstance(value, dict):
        return {"schema_version": 1, "institutions": []}
    return value


def _ssl_context() -> ssl.SSLContext:
    """Verify certificates, using certifi when the system store is unusable.

    Python builds on macOS frequently ship without a CA bundle wired up, which
    fails verification for every HTTPS call. Falling back to certifi keeps
    verification on rather than turning it off.
    """
    context = ssl.create_default_context()
    if context.cert_store_stats().get("x509_ca", 0):
        return context
    try:
        import certifi  # noqa: PLC0415 - optional fallback only
    except ImportError:
        return context
    return ssl.create_default_context(cafile=certifi.where())


def _get(params: dict[str, Any], timeout: int = 30) -> dict[str, Any]:
    request = Request(
        f"{ENDPOINT}?{urlencode(params)}",
        headers={"User-Agent": "internship-watcher/1.0", "Accept": "application/json"},
    )
    with urlopen(  # noqa: S310 - fixed https host
        request, timeout=timeout, context=_ssl_context()
    ) as response:
        return json.loads(response.read().decode("utf-8"))


def refresh(
    api_key: str = DEMO_KEY,
    *,
    path: Path = CACHE_PATH,
    max_pages: int = 30,
) -> dict[str, Any]:
    """Pull every institution that reports an admission rate, and cache it."""
    # Resume rather than restart: the demo key is rate limited to roughly a
    # page a minute, so a full pull takes several attempts and each one must
    # keep what the last managed to fetch.
    existing = {
        row.get("id"): row
        for row in load_cache(path).get("institutions", [])
        if row.get("id") is not None
    }
    institutions: list[dict[str, Any]] = []
    for page in range(max_pages):
        params = {
            "api_key": api_key,
            "fields": ",".join(FIELDS),
            "per_page": 100,
            "page": page,
            # Four-year institutions that actually publish a rate.
            "latest.admissions.admission_rate.overall__range": "0..1",
            "school.degrees_awarded.predominant__range": "3..4",
        }
        try:
            payload = _get(params)
        except HTTPError as exc:
            if exc.code == 429:
                time.sleep(5)
                try:
                    payload = _get(params)
                except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
                    break
            else:
                break
        except (URLError, TimeoutError, json.JSONDecodeError):
            break
        results = payload.get("results") or []
        if not results:
            break
        if all(row.get("id") in existing for row in results):
            continue
        for row in results:
            name = str(row.get("school.name", "")).strip()
            if not name:
                continue
            institutions.append({
                "id": row.get("id"),
                "name": name,
                "key": normalise(name),
                "city": row.get("school.city", ""),
                "state": row.get("school.state", ""),
                "site": row.get("school.school_url", ""),
                "admission_rate": row.get("latest.admissions.admission_rate.overall"),
                "sat_average": row.get("latest.admissions.sat_scores.average.overall"),
                "students": row.get("latest.student.size"),
                "tuition_out_of_state": row.get("latest.cost.tuition.out_of_state"),
                "completion_rate": row.get(
                    "latest.completion.rate_suppressed.overall"
                ),
                "earnings_10yr_median": row.get(
                    "latest.earnings.10_yrs_after_entry.median"
                ),
            })
        total = int((payload.get("metadata") or {}).get("total", 0))
        if len(institutions) >= total:
            break
        # The demo key is rate limited; a refresh is rare and can afford to wait.
        time.sleep(0.4)

    for row in institutions:
        existing[row["id"]] = row
    cache = {
        "schema_version": 1,
        "source": "US Department of Education College Scorecard",
        "endpoint": ENDPOINT,
        "institutions": sorted(existing.values(), key=lambda item: item["name"]),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return cache


def refresh_names(
    names: list[str],
    api_key: str = DEMO_KEY,
    *,
    path: Path = CACHE_PATH,
) -> int:
    """Fetch specific institutions by name, for topping up a partial cache.

    A full pull is 16 pages, which is more than the shared demo key allows in
    an hour. Asking for the handful of institutions actually referenced costs
    one request each and finishes.
    """
    cache = load_cache(path)
    existing = {row.get("id"): row for row in cache.get("institutions", [])}
    have = index(cache)
    added = 0
    for name in names:
        if lookup(name, have):
            continue
        try:
            payload = _get({
                "api_key": api_key,
                "fields": ",".join(FIELDS),
                "school.name": name,
                "per_page": 1,
            })
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
            break
        for row in payload.get("results") or []:
            label = str(row.get("school.name", "")).strip()
            if not label:
                continue
            existing[row.get("id")] = {
                "id": row.get("id"), "name": label, "key": normalise(label),
                "city": row.get("school.city", ""), "state": row.get("school.state", ""),
                "site": row.get("school.school_url", ""),
                "admission_rate": row.get("latest.admissions.admission_rate.overall"),
                "sat_average": row.get("latest.admissions.sat_scores.average.overall"),
                "students": row.get("latest.student.size"),
                "tuition_out_of_state": row.get("latest.cost.tuition.out_of_state"),
                "completion_rate": row.get("latest.completion.rate_suppressed.overall"),
                "earnings_10yr_median": row.get("latest.earnings.10_yrs_after_entry.median"),
            }
            added += 1
        time.sleep(0.3)
    cache["institutions"] = sorted(existing.values(), key=lambda item: item["name"])
    path.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return added


def index(cache: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    cache = cache if cache is not None else load_cache()
    built: dict[str, dict[str, Any]] = {}
    for row in cache.get("institutions", []):
        key = row.get("key") or normalise(row.get("name", ""))
        # Larger institutions win a name collision; a satellite campus should
        # not answer for the flagship.
        current = built.get(key)
        if current is None or (row.get("students") or 0) > (current.get("students") or 0):
            built[key] = row
    return built


def lookup(name: str, built: dict[str, dict[str, Any]] | None = None) -> dict[str, Any] | None:
    built = built if built is not None else index()
    key = normalise(name)
    if not key:
        return None
    if key in built:
        return built[key]
    # "Pennsylvania State University - College Park" against "Pennsylvania State".
    for candidate, row in built.items():
        if candidate and (candidate in key or key in candidate):
            return row
    return None


def describe(row: dict[str, Any]) -> str:
    parts = []
    rate = row.get("admission_rate")
    if isinstance(rate, (int, float)):
        parts.append(f"{rate * 100:.0f}% admitted")
    students = row.get("students")
    if students:
        parts.append(f"{int(students):,} students")
    tuition = row.get("tuition_out_of_state")
    if tuition:
        parts.append(f"${int(tuition):,} tuition")
    earnings = row.get("earnings_10yr_median")
    if earnings:
        parts.append(f"${int(earnings):,} median pay 10yr")
    return " · ".join(parts)


if __name__ == "__main__":  # pragma: no cover - operator entry point
    import sys

    if len(sys.argv) > 2 and sys.argv[1] == "names":
        from universities import load_universities  # noqa: PLC0415

        wanted = [
            entry["name"] for entry in load_universities()
            if entry.get("country") == "United States"
        ]
        print(f"added {refresh_names(wanted, sys.argv[2])} institutions")
    elif len(sys.argv) > 1 and sys.argv[1] == "refresh":
        key = sys.argv[2] if len(sys.argv) > 2 else DEMO_KEY
        cache = refresh(key)
        print(f"cached {len(cache['institutions'])} institutions -> {CACHE_PATH}")
    else:
        built = index()
        print(f"{len(built)} institutions cached")
        for probe in ("Stanford University", "Pennsylvania State University",
                      "University of Maryland - College Park"):
            row = lookup(probe, built)
            print(f"  {probe:42}{describe(row) if row else 'no match'}")
