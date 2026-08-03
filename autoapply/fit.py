"""Decide whether a posting is worth this person's time.

The tracker is honest about the market and useless about the applicant: every
posting arrives marked "review required", so 723 of them look identical. Most
are not. Two things can be settled from the profile alone:

*Timing.* A new-graduate role starting in 2026 is not open to somebody who
graduates in June 2028, whatever else is true. This is arithmetic, and it
accounts for most of the noise.

*Work authorisation.* A posting in a country where the profile records no
right to work, for a passport that would need sponsorship, is a long shot
rather than an application. That is worth knowing before writing a cover
letter, not after.

Nothing here is published. The verdicts are computed on the applicant's own
machine and served by the local bridge, because a visa status is not something
a public job dashboard should carry.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any

from .eligibility import jurisdiction_for


# Roles you enter on graduating, as opposed to during a degree.
GRADUATE_ENTRY_TYPES = {"new-grad", "entry-level", "graduate", "summer-analyst"}
# Roles you take while still studying.
STUDENT_TYPES = {
    "intern", "co-op", "placement", "apprenticeship", "research-assistant",
}

SEASON_MONTH = {
    "winter": 1,
    "spring": 4,
    "summer": 6,
    "fall": 9,
    "autumn": 9,
}


@dataclass
class Posting:
    """The fields a fit verdict needs, which the Job model does not carry.

    Term and position type live only in the tracker, so this reads them from
    there rather than widening the database schema for a read-only judgement.
    """

    id: str
    url: str
    company: str = ""
    role: str = ""
    region: str = ""
    location: str = ""
    term: str = ""
    position_type: str = ""


def read_postings(tracker: Path) -> list[Posting]:
    with Path(tracker).open(newline="", encoding="utf-8") as handle:
        return [
            Posting(
                id=row.get("id", ""),
                url=row.get("url", ""),
                company=row.get("company", ""),
                role=row.get("role", ""),
                region=row.get("region", ""),
                location=row.get("location", ""),
                term=row.get("term", ""),
                position_type=row.get("role_type", ""),
            )
            for row in csv.DictReader(handle)
            if row.get("record_kind", "posting") == "posting"
            and row.get("source_status") == "open"
            and row.get("url")
        ]


@dataclass
class Fit:
    """Why a posting is or is not worth applying to."""

    status: str = "check"          # apply | sponsor | check | mismatch
    timing: str = "unknown"        # fits | too_early | stale | unknown
    authorization: str = "unknown" # authorized | limited | sponsorship | unknown
    reasons: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "timing": self.timing,
            "authorization": self.authorization,
            "reasons": self.reasons,
        }


def _graduation_year(profile: dict[str, Any]) -> int | None:
    education = profile.get("education") or {}
    if not isinstance(education, dict):
        return None
    try:
        year = int(str(education.get("graduation_year", "")).strip()[:4])
    except (TypeError, ValueError):
        return None
    return year if 1950 < year < 2100 else None


def parse_term(term: str) -> tuple[int | None, int | None]:
    """Return (year, month) a term starts, as far as the label commits to one."""
    text = str(term or "").strip().lower()
    if not text or text in {"unknown", "ambiguous"}:
        return None, None
    year_match = re.search(r"\b(20\d\d)\b", text)
    year = int(year_match.group(1)) if year_match else None
    month = None
    for season, value in SEASON_MONTH.items():
        if season in text:
            # "Spring/Summer" and "Fall/Winter" start at the earlier season.
            month = value if month is None else min(month, value)
    return year, month


def assess_fit(
    job: Any,
    profile: dict[str, Any],
    *,
    today_year: int | None = None,
) -> Fit:
    """Combine timing and work authorisation into one verdict for one posting."""
    fit = Fit()
    graduation = _graduation_year(profile)
    position_type = str(getattr(job, "position_type", "") or "").strip().lower()
    term_year, _month = parse_term(getattr(job, "term", ""))

    # ── Timing ───────────────────────────────────────────────────────────────
    if term_year and today_year and term_year < today_year:
        fit.timing = "stale"
        fit.reasons.append(f"The {job.term} intake has already started")
    elif graduation and term_year and position_type in GRADUATE_ENTRY_TYPES:
        if term_year < graduation:
            fit.timing = "too_early"
            fit.reasons.append(
                f"A graduate role starting {term_year}, and you graduate {graduation}"
            )
        else:
            fit.timing = "fits"
    elif graduation and term_year and position_type in STUDENT_TYPES:
        if term_year > graduation:
            fit.timing = "too_early"
            fit.reasons.append(
                f"A student placement in {term_year}, after you graduate in {graduation}"
            )
        else:
            fit.timing = "fits"
    elif graduation and not term_year and position_type in GRADUATE_ENTRY_TYPES:
        # No year stated. Graduate roles usually hire for the coming cycle, so
        # this is a question rather than a match.
        fit.reasons.append("A graduate role with no stated intake year")

    # ── Work authorisation ───────────────────────────────────────────────────
    jurisdiction = jurisdiction_for(job)
    authorizations = profile.get("work_authorization") or {}
    auth = authorizations.get(jurisdiction) or {} if jurisdiction else {}
    if not jurisdiction:
        fit.reasons.append("The posting does not settle which country it is in")
    else:
        authorized = auth.get("authorized_now", "unknown")
        scope = str(auth.get("authorization_scope", "") or "unknown")
        needs_sponsorship = auth.get("requires_sponsorship_now_or_future")
        if authorized is True and scope == "unrestricted":
            fit.authorization = "authorized"
        elif authorized is True:
            fit.authorization = "limited"
            fit.reasons.append(
                f"You may work in {jurisdiction}, but on {scope} terms worth checking "
                "against this role"
            )
        elif needs_sponsorship is True:
            fit.authorization = "sponsorship"
            fit.reasons.append(
                f"You would need sponsorship or a matching visa for {jurisdiction}"
            )
        else:
            fit.reasons.append(
                f"Your right to work in {jurisdiction} is not recorded as confirmed"
            )

    # ── Verdict ──────────────────────────────────────────────────────────────
    if fit.timing in {"too_early", "stale"}:
        # Arithmetic, not judgement: no amount of tailoring fixes a date.
        fit.status = "mismatch"
    elif fit.authorization in {"authorized", "limited"} and fit.timing != "unknown":
        fit.status = "apply"
    elif fit.authorization == "sponsorship":
        # Not blocked, but a different kind of application: worth separating so
        # the handful you can simply apply to are not buried under hundreds
        # that need a visa first.
        fit.status = "sponsor"
    else:
        fit.status = "check"
    return fit


def assess_all(
    jobs: Any,
    profile: dict[str, Any],
    *,
    today_year: int | None = None,
) -> dict[str, dict[str, Any]]:
    return {
        job.id: assess_fit(job, profile, today_year=today_year).as_dict()
        for job in jobs
    }
