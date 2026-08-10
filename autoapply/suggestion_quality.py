"""Deterministic measurement of how well a tailored CV answers a posting.

Everything here is a pure function of text. The model proposes; this module
decides what is actually true of the result, so the figures beside a suggestion
are counted rather than asserted. Nothing in here needs a network, which is
also what makes it testable.

The rule throughout is that a claim is only reported when it can be checked.
An honest "3 of 14 terms covered" is worth more to an applicant than a
flattering number they cannot act on.
"""

from __future__ import annotations

import re
from typing import Any, Iterable

from .ai_tailoring import GENERIC_REQUIREMENT_WORDS
from .tailoring import concepts


# A screening term is one to four words. Longer is a sentence, and a term
# carrying a year is a date rather than something an ATS matches on.
MAX_TERM_WORDS = 4
MAX_TERM_CHARS = 80
# Below this many checkable terms the coverage percentage says more about how
# few terms were extracted than about the CV, so no figure is offered.
MIN_SCORABLE_TERMS = 4
IMPORTANCE_WEIGHTS = {"high": 3.0, "medium": 2.0, "low": 1.0}
DEFAULT_WEIGHT = 2.0
MAX_GAPS = 4


def significant_parts(term: str) -> set[str]:
    """The parts of a term that actually carry the requirement.

    "Strong Python proficiency" screens on Python; "strong" and "proficiency"
    are how the posting phrases itself. Stripping them keeps a term matchable
    without letting boilerplate decide whether it matched.
    """
    return {
        part
        for part in concepts(term)
        if part not in GENERIC_REQUIREMENT_WORDS and len(part) > 1
    }


def is_screening_term(term: str) -> bool:
    """Whether a proposed keyword is the sort of thing a filter screens on."""
    text = (term or "").strip()
    if not text or len(text) > MAX_TERM_CHARS:
        return False
    if len(text.split()) > MAX_TERM_WORDS:
        return False
    if re.search(r"\d{4}", text):
        return False
    return bool(significant_parts(text))


def covers(term: str, cv_terms: set[str]) -> bool:
    """Whether a CV genuinely evidences a term.

    Every significant part must be present. Scoring a term on the share of its
    words that matched reported "distributed data processing" as covered by a
    CV that had only ever done data processing, which is the one word of the
    three the posting was not screening on. A partial match is a gap.
    """
    parts = significant_parts(term)
    return bool(parts) and parts <= cv_terms


def normalise_importance(value: Any) -> str:
    text = str(value or "").strip().casefold()
    return text if text in IMPORTANCE_WEIGHTS else "medium"


def keyword_panel(raw: Any, cv_text: str, *, limit: int = 24) -> list[dict[str, str]]:
    """Check the model's keyword list against the CV instead of trusting it.

    Whether the CV contains a term is a fact, so the status is recomputed here
    and the model's own claim about it is discarded. Terms that are not
    screening terms are dropped rather than carried as padding, because they
    would otherwise inflate the coverage figure derived from this list.
    """
    cv_terms = concepts(cv_text)
    panel: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in list(raw or [])[:64]:
        if isinstance(item, dict):
            term = str(item.get("term", ""))
            importance = item.get("importance")
        elif isinstance(item, str):
            term, importance = item, None
        else:
            # A None or a number is not a term; str() would turn it into one.
            continue
        term = re.sub(r"\s+", " ", term).strip()
        key = term.casefold()
        if key in seen or not is_screening_term(term):
            continue
        seen.add(key)
        panel.append({
            "term": term[:MAX_TERM_CHARS],
            "status": "covered" if covers(term, cv_terms) else "missing",
            "importance": normalise_importance(importance),
        })
        if len(panel) >= limit:
            break
    return panel


def coverage_score(panel: Iterable[dict[str, str]]) -> int | None:
    """Percentage of the posting's screening terms the CV evidences.

    Weighted, so a missing high-importance term costs more than a missing
    nice-to-have. Derived from the same checked statuses the panel shows, so
    the number and the list beside it can never disagree.
    """
    terms = list(panel or [])
    if len(terms) < MIN_SCORABLE_TERMS:
        return None
    total = sum(IMPORTANCE_WEIGHTS.get(t.get("importance", ""), DEFAULT_WEIGHT) for t in terms)
    if not total:
        return None
    earned = sum(
        IMPORTANCE_WEIGHTS.get(t.get("importance", ""), DEFAULT_WEIGHT)
        for t in terms
        if t.get("status") == "covered"
    )
    return int(round(100 * earned / total))


def evidence_gaps(panel: Iterable[dict[str, str]], *, limit: int = MAX_GAPS) -> list[str]:
    """The terms this CV cannot evidence, named plainly.

    A tailoring tool that only reports what it improved leaves the applicant
    believing the CV answers the posting. The gaps are the part they can still
    do something about before the deadline, so they are stated rather than
    smoothed over.
    """
    missing = [t for t in (panel or []) if t.get("status") == "missing"]
    missing.sort(
        key=lambda t: -IMPORTANCE_WEIGHTS.get(t.get("importance", ""), DEFAULT_WEIGHT)
    )
    return [
        f"No evidence on this CV for “{t['term']}” "
        f"({t.get('importance', 'medium')} importance). Add it only if you have "
        "genuinely done it."
        for t in missing[:limit]
    ]


def terms_gained(original: str, proposal: str, posting_terms: set[str]) -> list[str]:
    """Posting vocabulary a rewrite brings in that the line did not already use.

    This is what makes a suggestion reviewable: not "improved for this role"
    but "adds: distributed training". A rewrite that gains nothing is a
    rephrasing, and the applicant can spend their attention elsewhere.
    """
    before = concepts(original)
    after = concepts(proposal)
    return sorted((after - before) & set(posting_terms or set()))


def posting_vocabulary(requirements: Iterable[str], keywords: Iterable[dict[str, str]]) -> set[str]:
    """Every concept the posting screens on, from its requirements and terms."""
    found: set[str] = set()
    for requirement in requirements or []:
        found |= significant_parts(str(requirement))
    for keyword in keywords or []:
        found |= significant_parts(str(keyword.get("term", "")))
    return found


# Wording that would be true of any rewrite of any line for any job. A
# rationale built only from these tells the reader nothing they can check.
FILLER_RATIONALE_TERMS = frozenset({
    "active", "better", "clarity", "clear", "clearer", "compelling", "concise",
    "engaging", "flow", "impact", "impactful", "improve", "improved",
    "improves", "polished", "professional", "punchier", "read", "readable",
    "reads", "sharper", "sound", "stronger", "tighter", "tone", "verb",
    "voice", "wording",
})
QUOTE_MARKS = "\"'‘’“”"


def is_generic_rationale(text: str, posting_terms: Iterable[str]) -> bool:
    """Whether a rationale explains this edit or merely praises it.

    "Stronger action verb" is true of every rewrite ever proposed and gives the
    applicant nothing to accept or reject on. A useful rationale either names
    something the posting asked for or quotes the wording it changed, so those
    are what is required; anything else is treated as absent, and the measured
    keyword gain is shown in its place.
    """
    value = str(text or "").strip()
    if not value:
        return True
    if any(mark in value for mark in QUOTE_MARKS):
        return False
    words = concepts(value)
    if not words:
        return True
    if words & set(posting_terms or set()):
        return False
    # Names nothing the posting asked for and quotes nothing it changed.
    return True
