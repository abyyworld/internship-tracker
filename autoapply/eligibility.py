from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

from .models import Job


COUNTRY_NAME_PATTERNS: tuple[tuple[str, str], ...] = (
    ("GB", r"\bunited kingdom\b|\bgreat britain\b|\bbritain\b|\bengland\b|"
           r"\bscotland\b|\bwales\b|\bnorthern ireland\b"),
    ("US", r"\bunited states(?: of america)?\b|\bamerica\b"),
    ("IE", r"\b(?:republic of )?ireland\b"),
    ("NL", r"\bnetherlands\b|\bdutch\b"),
    ("CA", r"\bcanada\b"),
    ("CH", r"\bswitzerland\b|\bswiss\b"),
    ("DE", r"\bgermany\b|\bgerman\b"),
    ("FR", r"\bfrance\b|\bfrench\b"),
    ("NO", r"\bnorway\b|\bnorwegian\b"),
    ("SG", r"\bsingapore\b"),
    ("JP", r"\bjapan\b|\bjapanese\b"),
    ("AU", r"\baustralia\b|\baustralian\b"),
    ("CN", r"\bchina\b|\bchinese\b"),
    ("IN", r"\bindia\b|\bindian\b"),
    ("KR", r"\bsouth korea\b|\brepublic of korea\b|\bkorean\b"),
    ("IL", r"\bisrael\b|\bisraeli\b"),
    ("SE", r"\bsweden\b|\bswedish\b"),
    ("DK", r"\bdenmark\b|\bdanish\b"),
    ("FI", r"\bfinland\b|\bfinnish\b"),
    ("ES", r"\bspain\b|\bspanish\b"),
    ("IT", r"\bitaly\b|\bitalian\b"),
    ("AT", r"\baustria\b|\baustrian\b"),
    ("BE", r"\bbelgium\b|\bbelgian\b"),
    ("PT", r"\bportugal\b|\bportuguese\b"),
    ("PL", r"\bpoland\b|\bpolish\b"),
    ("CZ", r"\bczechia\b|\bczech republic\b|\bczech\b"),
    ("EE", r"\bestonia\b|\bestonian\b"),
    ("NZ", r"\bnew zealand\b"),
    ("TW", r"\btaiwan\b|\btaiwanese\b"),
    ("HK", r"\bhong kong\b"),
    ("AE", r"\bunited arab emirates\b|\bu\.?a\.?e\.?\b"),
    ("BR", r"\bbrazil\b|\bbrazilian\b"),
    ("MX", r"\bmexico\b|\bmexican\b"),
)

COUNTRY_CODES = {code for code, _pattern in COUNTRY_NAME_PATTERNS}


def explicit_jurisdictions(value: str) -> set[str]:
    """Return countries explicitly named in text without treating pronouns as codes."""
    raw = value or ""
    matches = {
        code
        for code, pattern in COUNTRY_NAME_PATTERNS
        if re.search(pattern, raw, flags=re.I)
    }
    # Two-letter codes are accepted only when written in uppercase in the source
    # prompt. This avoids interpreting ordinary words such as "us", "in", or
    # "no" as countries after normalisation.
    for code in COUNTRY_CODES:
        if re.search(rf"(?<![A-Z]){re.escape(code)}(?![A-Z])", raw):
            matches.add(code)
    if re.search(r"\bU\.S\.(?:A\.)?(?=\s|$|[?,;:])", raw, flags=re.I):
        matches.add("US")
    if re.search(r"\bU\.K\.(?=\s|$|[?,;:])", raw, flags=re.I):
        matches.add("GB")
    return matches


@dataclass
class EligibilityReport:
    status: str
    reasons: list[str] = field(default_factory=list)


def jurisdiction_for(job: Job) -> str:
    region_parts = {
        part.strip().upper() for part in re.split(r"[/,]", job.region) if part.strip()
    }
    region_codes = {
        "UK": "GB",
        "UNITED KINGDOM": "GB",
        "GB": "GB",
        "US": "US",
        "UNITED STATES": "US",
        "IRELAND": "IE",
        "NETHERLANDS": "NL",
        "CANADA": "CA",
        "SWITZERLAND": "CH",
        "GERMANY": "DE",
        "FRANCE": "FR",
        "NORWAY": "NO",
        "SINGAPORE": "SG",
        "JAPAN": "JP",
        "AUSTRALIA": "AU",
        "CHINA": "CN",
        "INDIA": "IN",
        "SOUTH KOREA": "KR",
        "REPUBLIC OF KOREA": "KR",
        "ISRAEL": "IL",
        "SWEDEN": "SE",
        "DENMARK": "DK",
        "FINLAND": "FI",
        "SPAIN": "ES",
        "ITALY": "IT",
        "AUSTRIA": "AT",
        "BELGIUM": "BE",
        "PORTUGAL": "PT",
        "POLAND": "PL",
        "CZECHIA": "CZ",
        "CZECH REPUBLIC": "CZ",
        "ESTONIA": "EE",
        "NEW ZEALAND": "NZ",
        "TAIWAN": "TW",
        "HONG KONG": "HK",
        "UNITED ARAB EMIRATES": "AE",
        "BRAZIL": "BR",
        "MEXICO": "MX",
    }
    if len(region_parts) == 1:
        code = region_codes.get(next(iter(region_parts)))
        if code:
            return code
    if len(region_parts) > 1:
        return ""

    text = job.location.lower()
    matches = set()
    if re.search(r"\buk\b|united kingdom|england|scotland|wales|"
                 r"northern ireland|london", text):
        matches.add("GB")
    if re.search(
        r"\bus\b|united states|\busa\b|new york|california|"
        r"\b(?:ca|ma|tx|wa|ny|va|mi|ga|co|pa|az|or|il|nc|fl),?\s*(?:usa)?\b",
        text,
    ):
        matches.add("US")
    if ("republic of ireland" in text
            or (re.search(r"\bireland\b|\bdublin\b", text)
                and "northern ireland" not in text)):
        matches.add("IE")
    patterns = (
        ("NL", r"\bnetherlands\b|\bamsterdam\b"),
        ("CA", r"\bcanada\b|\btoronto\b|\bvancouver\b"),
        ("CH", r"\bswitzerland\b|\bzurich\b|\bzürich\b"),
        ("DE", r"\bgermany\b|\bberlin\b|\bmunich\b|\bmünchen\b"),
        ("FR", r"\bfrance\b|\bparis\b"),
        ("NO", r"\bnorway\b|\boslo\b"),
        ("SG", r"\bsingapore\b"),
        ("JP", r"\bjapan\b|\btokyo\b"),
        ("AU", r"\baustralia\b|\bsydney\b|\bmelbourne\b|\bbrisbane\b"),
        ("CN", r"\bchina\b|\bshanghai\b|\bbeijing\b|\bshenzhen\b"),
        ("IN", r"\bindia\b|\bbengaluru\b|\bbangalore\b|\bhyderabad\b"),
        ("KR", r"\bsouth korea\b|\brepublic of korea\b|\bseoul\b"),
        ("IL", r"\bisrael\b|\btel aviv\b"),
        ("SE", r"\bsweden\b|\bstockholm\b|\bgothenburg\b"),
        ("DK", r"\bdenmark\b|\bcopenhagen\b"),
        ("FI", r"\bfinland\b|\bhelsinki\b"),
        ("ES", r"\bspain\b|\bmadrid\b|\bbarcelona\b"),
        ("IT", r"\bitaly\b|\bmilan\b|\brome\b"),
        ("AT", r"\baustria\b|\bvienna\b"),
        ("BE", r"\bbelgium\b|\bbrussels\b"),
        ("PT", r"\bportugal\b|\blisbon\b"),
        ("PL", r"\bpoland\b|\bwarsaw\b|\bkrakow\b"),
        ("CZ", r"\bczechia\b|\bczech republic\b|\bprague\b"),
        ("EE", r"\bestonia\b|\btallinn\b"),
        ("NZ", r"\bnew zealand\b|\bauckland\b"),
        ("TW", r"\btaiwan\b|\btaipei\b"),
        ("HK", r"\bhong kong\b"),
        ("AE", r"\bunited arab emirates\b|\bdubai\b|\babu dhabi\b"),
        ("BR", r"\bbrazil\b|\bsao paulo\b|\bsão paulo\b"),
        ("MX", r"\bmexico\b|\bmexico city\b"),
    )
    for code, pattern in patterns:
        if re.search(pattern, text):
            matches.add(code)
    return next(iter(matches)) if len(matches) == 1 else ""


def assess_eligibility(job: Job, profile: dict[str, Any]) -> EligibilityReport:
    text = f"{job.role} {job.description}".lower()
    reasons: list[str] = []
    if re.search(r"\bu\.?s\.? citizens? only\b|must be (?:a )?u\.?s\.? citizen", text):
        citizenships = {
            str(x).upper() for x in profile.get("citizenships", []) if str(x).strip()
        }
        if "US" not in citizenships:
            return EligibilityReport("blocked", ["Posting explicitly requires US citizenship"])
    if re.search(r"\bph\.?d\.? (?:is )?required\b|must (?:have|hold) (?:a )?ph\.?d", text):
        level = str(profile.get("education", {}).get("level", "")).lower()
        if "phd" not in level and "doctor" not in level:
            return EligibilityReport("blocked", ["Posting explicitly requires a PhD"])
    jurisdiction = jurisdiction_for(job)
    auth = profile.get("work_authorization", {}).get(jurisdiction, {}) if jurisdiction else {}
    if re.search(r"no (?:visa )?sponsorship|unable to sponsor", text):
        authorised = auth.get("authorized_now", "unknown")
        if authorised is False:
            return EligibilityReport(
                "blocked", [f"No sponsorship and profile says not authorised in {jurisdiction}"]
            )
        if authorised == "unknown" or not jurisdiction:
            reasons.append("No sponsorship stated, but local work authorisation is unknown")
    if not jurisdiction:
        reasons.append("Job jurisdiction is unknown or spans multiple countries")
    elif auth.get("authorized_now", "unknown") == "unknown":
        reasons.append(f"Work authorisation for {jurisdiction} is not confirmed")
    return EligibilityReport("review_required" if reasons else "not_blocked", reasons)
