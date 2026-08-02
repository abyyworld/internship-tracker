from __future__ import annotations

import csv
from html import unescape
from html.parser import HTMLParser
import ipaddress
import re
import socket
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import requests

from .models import Job, digest


TRACKING_QUERY_KEYS = {
    "ref",
    "source",
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
}


# Text inside these is never posting copy. Collecting it puts minified
# JavaScript into the job description the tailoring model reads.
_NON_TEXT_TAGS = {"script", "style", "noscript", "svg", "template", "head"}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag in _NON_TEXT_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in _NON_TEXT_TAGS and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if data.strip():
            self.parts.append(data.strip())

    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


def html_to_text(value: str) -> str:
    parser = _TextExtractor()
    parser.feed(unescape(value or ""))
    return parser.text()


def canonicalize_url(url: str) -> str:
    value = (url or "").strip()
    if not value:
        return ""
    parsed = urlparse(value)
    query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if key.lower() not in TRACKING_QUERY_KEYS
    ]
    return urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            re.sub(r"/+$", "", parsed.path) or "/",
            "",
            urlencode(query),
            "",
        )
    )


def detect_ats(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.endswith("greenhouse.io"):
        return "greenhouse"
    if host.endswith("lever.co"):
        return "lever"
    if host.endswith("ashbyhq.com"):
        return "ashby"
    return "unknown"


def external_id(url: str, ats: str | None = None) -> str:
    parsed = urlparse(url)
    ats = ats or detect_ats(url)
    path = parsed.path.rstrip("/").split("/")
    query = dict(parse_qsl(parsed.query))
    if ats == "greenhouse":
        return query.get("token") or query.get("gh_jid") or (path[-1] if path else "")
    if ats in {"lever", "ashby"}:
        # Hosted forms append `/apply` or `/application`; the stable posting ID
        # is the UUID before that suffix, not the suffix itself.
        match = re.search(
            r"/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
            r"[0-9a-f]{4}-[0-9a-f]{12})(?:/|$)",
            parsed.path,
            flags=re.I,
        )
        return match.group(1).lower() if match else ""
    return ""


def _tracker_description(row: dict[str, str]) -> str:
    details = [
        f"Job title: {row.get('role', '')}",
        f"Company: {row.get('company', '')}",
        f"Category: {row.get('category', '')}",
        f"Location: {row.get('location', '') or row.get('region', '')}",
        f"Term: {row.get('term', '')}",
        f"Degree evidence: {row.get('level', '')}",
        f"Technical focus: {row.get('robotics_focus', '') or row.get('focus_tags', '')}",
        f"Company type: {row.get('company_type', '')}",
    ]
    return ". ".join(value for value in details if not value.endswith(": ")) + "."


def jobs_from_tracker(path: Path, *, include_unknown: bool = False) -> list[Job]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    jobs: list[Job] = []
    for row in rows:
        if row.get("record_kind", "posting") != "posting":
            continue
        if row.get("source_status", "open") != "open":
            continue
        url = canonicalize_url(row.get("url", ""))
        if not url:
            continue
        ats = detect_ats(url)
        if (
            urlparse(url).scheme.lower() != "https"
            or (ats == "unknown" and not include_unknown)
        ):
            continue
        job_id = row.get("id") or digest(
            [row.get("company", ""), row.get("role", ""), url]
        )[:24]
        jobs.append(
            Job(
                id=job_id,
                company=row.get("company", ""),
                role=row.get("role", ""),
                url=url,
                ats=ats,
                external_id=external_id(url, ats),
                location=row.get("location", ""),
                region=row.get("region", ""),
                description=_tracker_description(row) if include_unknown else "",
                source_status=row.get("source_status", "open"),
            )
        )
    return jobs


def _get(url: str, as_json: bool = False) -> Any:
    response = requests.get(
        url,
        headers={
            "Accept": "application/json,text/html;q=0.8",
            "User-Agent": "internship-watcher-autoapply/0.1",
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json() if as_json else response.text


def assert_public_https_url(url: str) -> None:
    parsed = urlparse(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.port not in (None, 443)
    ):
        raise ValueError("Job URL must be a public HTTPS address")
    try:
        addresses = {
            item[4][0]
            for item in socket.getaddrinfo(
                parsed.hostname, 443, type=socket.SOCK_STREAM
            )
        }
    except socket.gaierror as exc:
        raise ValueError("Job hostname could not be resolved") from exc
    if not addresses or any(
        not ipaddress.ip_address(address).is_global for address in addresses
    ):
        raise ValueError("Job URL must not resolve to a private or local address")


def _get_public_page(url: str) -> str:
    return _get_public_page_with_url(url)[0]


def _get_public_page_with_url(url: str) -> tuple[str, str]:
    """Fetch a public page, returning its HTML and the URL it settled on."""
    current = url
    for _redirect in range(6):
        assert_public_https_url(current)
        response = requests.get(
            current,
            headers={
                "Accept": "text/html,application/xhtml+xml",
                "User-Agent": "Mozilla/5.0 internship-watcher-resume-tailor/1.0",
            },
            timeout=20,
            allow_redirects=False,
        )
        if response.status_code in {301, 302, 303, 307, 308}:
            destination = response.headers.get("Location", "")
            if not destination:
                return "", current
            current = urljoin(current, destination)
            continue
        response.raise_for_status()
        if "html" not in response.headers.get("Content-Type", "").lower():
            return "", current
        return response.text[:2_000_000], current
    return "", current


def _is_same_posting(requested: str, settled: str) -> bool:
    """True when a redirect stayed on the posting rather than leaving it.

    An expired posting commonly 302s to the employer's board index. Reading
    that page yields a list of every other opening, which is worse than no
    description: the tailoring model would target the wrong job entirely.
    """
    if canonicalize_url(requested) == canonicalize_url(settled):
        return True
    identifiers = [
        part
        for part in urlparse(requested).path.split("/")
        if len(part) > 3 and any(character.isdigit() for character in part)
    ]
    settled_path = urlparse(settled).path
    return any(identifier in settled_path for identifier in identifiers)


def _greenhouse_board_and_id(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    parts = [x for x in parsed.path.split("/") if x]
    query = dict(parse_qsl(parsed.query))
    if len(parts) >= 3 and parts[-2] == "jobs":
        return parts[-3], parts[-1]
    if "embed" in parts and "job_app" in parts:
        return query.get("for", ""), query.get("token", "")
    return "", query.get("gh_jid") or query.get("token", "")


MIN_DESCRIPTION_CHARS = 400


def _greenhouse_description(url: str) -> str:
    board, post_id = _greenhouse_board_and_id(url)
    if not board or not post_id:
        return ""
    # Boards hosted in the EU are not served by the US API host, and asking the
    # wrong one returns 404. Try both rather than giving up on the region.
    hosts = ["boards-api.greenhouse.io", "api.eu.greenhouse.io"]
    if ".eu." in urlparse(url).hostname or "":
        hosts.reverse()
    for host in hosts:
        try:
            data = _get(
                f"https://{host}/v1/boards/{board}/jobs/{post_id}?content=true",
                as_json=True,
            )
        except Exception:
            continue
        text = html_to_text(str(data.get("content", "")))
        if text:
            return text
    return ""


def _lever_description(url: str) -> str:
    parts = [x for x in urlparse(url).path.split("/") if x]
    if len(parts) < 2:
        return ""
    data = _get(f"https://api.lever.co/v0/postings/{parts[0]}/{parts[1]}", as_json=True)
    plain = data.get("descriptionPlain") or data.get("description") or ""
    lists = " ".join(
        f"{item.get('text', '')} {html_to_text(item.get('content', ''))}"
        for item in data.get("lists", [])
    )
    return re.sub(r"\s+", " ", f"{plain} {lists}").strip()


def _ashby_description(url: str) -> str:
    parts = [x for x in urlparse(url).path.split("/") if x]
    if len(parts) < 2:
        return ""
    data = _get(
        f"https://api.ashbyhq.com/posting-api/job-board/{parts[0]}", as_json=True
    )
    for posting in data.get("jobs", []):
        posting_url = posting.get("jobUrl") or posting.get("applyUrl") or ""
        if parts[1] in posting_url or posting.get("id") == parts[1]:
            return (
                posting.get("descriptionPlain")
                or html_to_text(posting.get("descriptionHtml", ""))
                or html_to_text(posting.get("description", ""))
            )
    return ""


def fetch_description(job: Job) -> str:
    """Fetch public posting text. Never calls an application submission endpoint.

    Each source is tried independently and a failure falls through to the next.
    Previously one raised request abandoned the whole attempt, and the caller
    silently substituted the tracker's own one-line metadata — so the tailoring
    model was handed "Degree evidence: Unknown" instead of the advert.
    """
    handlers = {
        "greenhouse": _greenhouse_description,
        "lever": _lever_description,
        "ashby": _ashby_description,
    }
    handler = handlers.get(job.ats)
    if handler:
        try:
            text = handler(job.url)
        except Exception:
            text = ""
        if len(text) >= MIN_DESCRIPTION_CHARS:
            return text
    # The public posting page, read through the SSRF-checked fetcher. This is
    # the fallback for every ATS whose API shape changed, moved region, or
    # never had one.
    try:
        html, settled = _get_public_page_with_url(job.url)
    except Exception:
        return ""
    if not _is_same_posting(job.url, settled):
        return ""
    return html_to_text(html)
    return ""
