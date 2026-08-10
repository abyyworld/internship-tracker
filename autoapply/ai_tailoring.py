from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
import re
from typing import Any
from urllib.parse import urlparse

import requests

from .models import Job
from .tailoring import TailoredResume, concepts


DEFAULT_OLLAMA_ENDPOINT = "http://127.0.0.1:11434"
MAX_DESCRIPTION_CHARS = 12000
MIN_BULLET_CHARS = 24
MAX_BULLET_CHARS = 360
# Above this, an entry is a prose paragraph rather than a bullet.
LONG_ENTRY_CHARS = 800

RISKY_CLAIMS = {
    "award-winning",
    "certified",
    "expert",
    "expertise",
    "industry-leading",
    "patented",
    "professional",
    "published",
    "specialist",
    "state-of-the-art",
    "world-class",
}


def _local_ollama_endpoint(value: str) -> str:
    endpoint = (value or DEFAULT_OLLAMA_ENDPOINT).rstrip("/")
    parsed = urlparse(endpoint)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Ollama endpoint must be an HTTP loopback address")
    return endpoint


def ollama_models(endpoint: str = DEFAULT_OLLAMA_ENDPOINT) -> set[str]:
    endpoint = _local_ollama_endpoint(endpoint)
    response = requests.get(f"{endpoint}/api/tags", timeout=2)
    response.raise_for_status()
    return {
        str(item.get("name", ""))
        for item in response.json().get("models", [])
        if item.get("name")
    }


def _number_tokens(value: str) -> set[str]:
    return set(re.findall(r"(?<!\w)\d+(?:[.,]\d+)?%?", value or ""))


def _named_tokens(value: str) -> set[str]:
    values = set()
    for token in re.findall(r"\b[A-Za-z][A-Za-z0-9+#.-]*\b", value or ""):
        if (
            token.isupper()
            or any(character.isdigit() for character in token)
            or "+" in token
            or "#" in token
            or (any(character.isupper() for character in token[1:]))
        ):
            values.add(token.casefold())
    return values


# Words a CV line habitually opens with. Capitalisation at the start of a
# sentence is grammar, so an opener is only read as a name when it is neither
# one of these nor an inflected English verb.
SENTENCE_OPENERS = frozenset({
    "a", "across", "after", "also", "an", "and", "another", "as", "at",
    "because", "before", "both", "brings", "broke", "brought", "builds",
    "built", "but", "by", "chose", "core", "current", "cut", "de", "drives",
    "drove", "during", "each", "every", "final", "finds", "first", "for",
    "found", "from", "full", "gave", "gives", "grew", "grows", "he", "held",
    "helps", "her", "here", "his", "holds", "how", "however", "i", "in",
    "it", "its", "junior", "keeps", "kept", "key", "lead", "leads", "led",
    "made", "main", "makes", "meets", "met", "my", "no", "now", "of", "on",
    "one", "ongoing", "or", "other", "our", "over", "own", "owns", "part",
    "primary", "prior", "put", "ran", "read", "responsible", "runs", "saw",
    "second", "sends", "senior", "sent", "serves", "set", "sets", "she",
    "shipped", "ships", "shows", "since", "sold", "sole", "spoke", "such",
    "takes", "taught", "teaches", "team", "tells", "tests", "than", "that",
    "the", "their", "then", "there", "these", "they", "third", "this",
    "those", "three", "through", "throughout", "to", "today", "told",
    "took", "two", "under", "understood", "up", "uses", "we", "went",
    "were", "what", "when", "where", "which", "while", "why", "wins",
    "with", "within", "won", "work", "writes", "wrote", "you", "your",
})


# Prefixes that build a new verb out of an ordinary one: "Rebuilt", "Co-led",
# "Oversaw". Stripping them lets one wordlist cover the derived forms too.
VERB_PREFIXES = ("re", "un", "over", "under", "out", "pre", "co-", "co")


def _looks_like_english_opener(token: str, known: set[str] | None = None) -> bool:
    """True when a capitalised sentence opener is ordinary English, not a name.

    A wordlist cannot be complete, so this errs towards calling an unknown
    opener a name. That costs at most one discarded rewrite; the opposite
    mistake puts an employer the candidate never had on their CV.
    """
    candidates = {token}
    for prefix in VERB_PREFIXES:
        if token.startswith(prefix) and len(token) > len(prefix) + 2:
            candidates.add(token[len(prefix):])
    for word in candidates:
        if word in SENTENCE_OPENERS or word.endswith(("ed", "ing", "ly")):
            return True
        if known and word in known:
            return True
    return False


def _word_set(value: str) -> set[str]:
    """Every word of a text, casefolded, whatever its capitalisation."""
    return set(re.findall(r"[a-z0-9+#.-]+", (value or "").casefold()))


def _proper_tokens(value: str, *, known: set[str] | None = None) -> set[str]:
    """Ordinary capitalised words: Python, Docker, Unity, Neuralink, fMRI.

    ``_named_tokens`` only catches acronyms, CamelCase, and tokens carrying
    digits or symbols, so a plainly capitalised technology named in the posting
    could be written into an entry that never claimed it.

    A word opening a sentence is capitalised by grammar rather than because it
    names anything, so rewriting "Built a Python controller" as "Developed a
    Python controller" must not be rejected for introducing "Developed".
    Exempting the position outright was too generous: it let a rewrite open
    "Neuralink robotics work: built a Python controller" and smuggle in an
    employer the CV never mentions. An opener is therefore exempt only when it
    inflects like an English verb, is a known opener, or is a word ``known``
    already contains — and when ``known`` is None, nothing is exempt, so the
    text being used as evidence contributes its openers too.
    """
    text = value or ""
    found = set()
    for match in re.finditer(r"\b[A-Z][a-z][A-Za-z0-9+#.-]*\b", text):
        token = match.group(0).casefold()
        before = text[: match.start()].rstrip()
        if (not before or before[-1] in ".!?") and known is not None:
            if _looks_like_english_opener(token, known):
                continue
        found.add(token)
    return found


def _length_bounds(original: str, *, strict: bool = True) -> tuple[int, int]:
    """Allowed rewrite length, measured against the line being rewritten.

    A CV entry may be a one-line bullet or a full prose paragraph. A fixed cap
    sized for bullets rejects every rewrite of a paragraph, so the band tracks
    the original. Tightening prose is a legitimate result of rewriting for a
    job, so a deliberate rewrite may cut further than a touch-up may — but not
    so far that a paragraph becomes a sentence.
    """
    length = len(re.sub(r"\s+", " ", original or "").strip())
    if strict:
        floor = 0.6
    else:
        # Tightening is the point of a rewrite, and the longest paragraphs have
        # the most slack in them, so they may lose proportionally more. The
        # floor still keeps a paragraph a paragraph.
        floor = 0.45 if length < LONG_ENTRY_CHARS else 0.33
    ceiling = 1.25 if strict else 1.35
    return (
        # Never demand more than the original itself has: "SAT: 1500 (Dec 2023):"
        # is 21 characters, and a floor above that rejects every rewrite of it.
        min(length, max(MIN_BULLET_CHARS, int(length * floor))),
        max(MAX_BULLET_CHARS if strict else 420, int(length * ceiling)),
    )


# How much of the original's vocabulary a rewrite must still carry. The strict
# figure suits a light touch-up. A deliberate rewrite for a specific job
# reorders and re-words heavily on purpose, so holding it to the same figure
# rejects exactly the work that was asked for; the anti-fabrication checks
# above are what keep it honest, not this one.
STRICT_OVERLAP = 0.3
REWRITE_OVERLAP = 0.15


# Vocabulary a requirement is phrased in rather than vocabulary it names. A
# rewrite may freely say "ability" or "experience"; barring those would reject
# ordinary English, and they assert no domain the candidate has not worked in.
GENERIC_REQUIREMENT_WORDS = {
    "ability", "able", "academic", "advanced", "analysing", "analyzing",
    "applicant", "applied", "apply",
    "background", "candidate", "career", "collaborate", "collaboration",
    "communication", "company", "complex", "degree", "deliver", "demonstrate",
    "demonstrated", "detail", "develop", "development", "domain", "drive",
    "dynamic", "environment", "evidence", "excellent", "exceptional",
    "execution", "experience", "expertise",
    "experienced", "familiarity", "field", "focus", "fluency", "fluent",
    "graduate", "hands", "impact", "industry", "innovative", "internship",
    "knowledge", "language", "level", "master", "masters", "modern",
    "opportunity", "particularly", "principle", "principles",
    "phd", "position", "practical", "preferred", "proficiency", "proficient",
    "program", "project", "qualification", "quality", "related", "relevant",
    "requirement", "responsibility", "role", "skill", "solid", "strong",
    "student", "study", "team", "technical", "technique", "technology", "tool",
    "track", "understanding", "university", "work", "working", "year", "years",
}


# Words that assert a level of qualification. Unlike a technology, a
# credential cannot be inferred from anywhere else in the CV: this fact bank
# mentions "PhD" only as a category of posting its tracker watches, and that
# was enough for a rewrite to award its author a doctorate. A credential may
# therefore only appear in a rewrite if it appears in the exact line replaced.
CREDENTIAL_PATTERN = re.compile(
    r"\b(ph\.?d|d\.?phil|doctoral|doctorate|post-?doc(?:toral)?|"
    r"m\.?sc|m\.?eng|m\.?ba|master'?s?|bachelor'?s?|b\.?sc|b\.?eng|"
    r"professor|faculty|tenured|chartered|licen[cs]ed|accredited|"
    r"graduated|alumnus|alumna)\b",
    re.IGNORECASE,
)


def _credential_claims(value: str) -> set[str]:
    return {
        match.group(0).casefold().replace(".", "").replace("'", "")
        for match in CREDENTIAL_PATTERN.finditer(value or "")
    }


def borrowed_terms(requirements: Any, evidence: str) -> set[str]:
    """Domain vocabulary a requirement names that the CV never uses.

    The characteristic fabrication is not an invented number, it is echoing a
    requirement back as a credential: a posting asks for neuroscience, and the
    rewrite reports "a strong foundation in neuroscience". Lowercase domain
    nouns pass every other check here, so the words themselves are barred —
    but only the ones naming a subject, not the boilerplate around them.
    """
    lacking = concepts(evidence or "")
    wanted: set[str] = set()
    for requirement in requirements or []:
        wanted |= concepts(str(requirement))
    return {
        term
        for term in wanted - lacking
        if term not in GENERIC_REQUIREMENT_WORDS and len(term) > 2
    }


def _validate_rewrite(
    original: str,
    candidate: str,
    *,
    strict: bool = True,
    evidence: str = "",
    local_evidence: str | None = None,
    forbidden: set[str] | None = None,
) -> str:
    """Check a proposed rewrite of one CV line.

    ``evidence`` is what the CV asserts about this person in general: its
    skills, its summary, and the entry this line belongs to. A rewrite may
    draw on it to name a technology the candidate genuinely claims - that is
    what tailoring is.

    ``local_evidence`` is narrower: the one entry this line sits in. A
    number, a date, or a qualification is a claim about a specific piece of
    work, so it is checked against that entry alone. Checked document-wide, a
    metric earned on one project can be restated as the outcome of another -
    a sales figure of 40% reappearing as a robot's task success rate reads as
    evidence and collapses the moment anyone asks about it. When
    ``local_evidence`` is None the wider evidence is used for both, which is
    the behaviour the local-model path still relies on.
    """
    value = re.sub(r"\s+", " ", candidate or "").strip().lstrip("•- ").strip()
    supported = f"{evidence} {original}" if evidence else original
    attributable = (
        f"{local_evidence} {original}" if local_evidence is not None else supported
    )
    low, high = _length_bounds(original, strict=strict)
    if not low <= len(value) <= high:
        raise ValueError("length")
    if _number_tokens(value) - _number_tokens(attributable):
        raise ValueError("new_numeric_claim")
    # Scoped to the line replaced, never the wider document.
    if _credential_claims(value) - _credential_claims(original):
        raise ValueError("new_credential_claim")
    if _named_tokens(value) - _named_tokens(supported):
        raise ValueError("new_named_technology_or_entity")
    if _proper_tokens(value, known=_word_set(supported)) - _proper_tokens(supported):
        raise ValueError("new_named_technology_or_entity")
    attributable_lower = attributable.casefold()
    for phrase in RISKY_CLAIMS:
        if phrase in value.casefold() and phrase not in attributable_lower:
            raise ValueError("new_unsupported_qualification")
    original_terms = concepts(original)
    candidate_terms = concepts(value)
    if forbidden and candidate_terms & forbidden:
        raise ValueError("borrowed_requirement_not_in_cv")
    floor = STRICT_OVERLAP if strict else REWRITE_OVERLAP
    if original_terms and len(original_terms & candidate_terms) / len(original_terms) < floor:
        raise ValueError("insufficient_evidence_overlap")
    return value


def _validate_summary(
    evidence: str,
    candidate: str,
    *,
    max_chars: int = 420,
    strict: bool = True,
    forbidden: set[str] | None = None,
    original: str = "",
) -> str:
    value = re.sub(r"\s+", " ", candidate or "").strip().lstrip("•- ").strip()
    if not 40 <= len(value) <= max(420, max_chars):
        raise ValueError("length")
    if _credential_claims(value) - _credential_claims(original or evidence):
        raise ValueError("new_credential_claim")
    if _number_tokens(value) - _number_tokens(evidence):
        raise ValueError("new_numeric_claim")
    if _named_tokens(value) - _named_tokens(evidence):
        raise ValueError("new_named_technology_or_entity")
    if _proper_tokens(value, known=_word_set(evidence)) - _proper_tokens(evidence):
        raise ValueError("new_named_technology_or_entity")
    evidence_lower = evidence.casefold()
    for phrase in RISKY_CLAIMS:
        if phrase in value.casefold() and phrase not in evidence_lower:
            raise ValueError("new_unsupported_qualification")
    evidence_terms = concepts(evidence)
    candidate_terms = concepts(value)
    if forbidden and candidate_terms & forbidden:
        raise ValueError("borrowed_requirement_not_in_cv")
    # How much of the new summary must already appear in the evidence. A
    # summary written for one job leans on the posting's vocabulary, so a
    # deliberate rewrite is held to a lower share than a touch-up; the
    # fabrication checks above are what keep the claims themselves honest.
    floor = 0.7 if strict else 0.5
    if (
        candidate_terms
        and len(evidence_terms & candidate_terms) / len(candidate_terms) < floor
    ):
        raise ValueError("insufficient_evidence_coverage")
    return value


def _prompt(job: Job, resume: TailoredResume) -> tuple[str, str]:
    facts = [
        {"id": link.fact_id, "verified_text": link.text}
        for link in resume.evidence_links
    ]
    system = (
        "You edit one truthful CV for one job. Return JSON only. Rewrite wording "
        "for relevance and clarity, but never invent or infer a skill, tool, metric, "
        "employer, date, responsibility, qualification, award, or outcome. Preserve "
        "every number and named technology exactly. A job requirement is not proof "
        "the applicant has it. Do not use first person. Return exactly this shape: "
        '{"summary":"...","bullets":{"fact-id":"rewritten bullet"}}. '
        "The bullets object keys must be copied verbatim from verified_facts[].id. "
        "Include every supplied fact id exactly once. Keep each bullet under 38 words."
    )
    user = json.dumps(
        {
            "target": {
                "company": job.company,
                "role": job.role,
                "description": job.description[:MAX_DESCRIPTION_CHARS],
            },
            "existing_summary": resume.summary,
            "verified_facts": facts,
        },
        ensure_ascii=False,
    )
    return system, user


def rewrite_with_ollama(
    resume: TailoredResume,
    job: Job,
    *,
    model: str,
    endpoint: str = DEFAULT_OLLAMA_ENDPOINT,
) -> TailoredResume:
    """Create a locally generated draft while retaining evidence-linked fallbacks."""
    if not model.strip():
        raise ValueError("An Ollama model name is required")
    endpoint = _local_ollama_endpoint(endpoint)
    system, user = _prompt(job, resume)
    fact_ids = [link.fact_id for link in resume.evidence_links]
    output_schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "bullets": {
                "type": "object",
                "properties": {
                    fact_id: {"type": "string"} for fact_id in fact_ids
                },
                "required": fact_ids,
                "additionalProperties": False,
            },
        },
        "required": ["summary", "bullets"],
        "additionalProperties": False,
    }
    try:
        response = requests.post(
            f"{endpoint}/api/chat",
            json={
                "model": model,
                "stream": False,
                "format": output_schema,
                "think": False,
                "keep_alive": "30m",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "options": {"temperature": 0.1, "seed": 42},
            },
            timeout=120,
        )
        response.raise_for_status()
        content = response.json().get("message", {}).get("content", "")
        generated = json.loads(content)
    except (requests.RequestException, json.JSONDecodeError, TypeError) as exc:
        raise RuntimeError(
            f"Local AI tailoring failed for model {model!r}: {exc}"
        ) from exc
    proposed = generated.get("bullets", {})
    if not isinstance(proposed, dict):
        raise RuntimeError("Local AI returned an invalid bullets object")

    original_by_id = {link.fact_id: link.text for link in resume.evidence_links}
    accepted: dict[str, str] = {}
    rejected: dict[str, str] = {}
    for fact_id, original in original_by_id.items():
        candidate = proposed.get(fact_id)
        if not isinstance(candidate, str):
            rejected[fact_id] = "missing"
            continue
        try:
            accepted[fact_id] = _validate_rewrite(original, candidate)
        except ValueError as exc:
            rejected[fact_id] = str(exc)
    unknown_ids = sorted(set(map(str, proposed)) - set(original_by_id))
    if not accepted:
        reasons = ", ".join(
            f"{reason}: {count}"
            for reason, count in sorted(Counter(rejected.values()).items())
        )
        raise RuntimeError(
            "Local AI produced no evidence-safe bullet rewrites; "
            f"the CV was not generated ({reasons or 'no valid fact ids'})"
        )

    result = deepcopy(resume)
    for section in result.sections:
        for entry in section.get("entries", []):
            evidence_ids = list(entry.get("evidence_ids", []))
            original_bullets = list(entry.get("bullets", []))
            entry["bullets"] = [
                accepted.get(fact_id, original)
                for fact_id, original in zip(evidence_ids, original_bullets)
            ]

    summary = generated.get("summary", "")
    summary_status = "original"
    if isinstance(summary, str) and summary.strip():
        all_evidence = " ".join(original_by_id.values())
        combined_original = f"{resume.summary} {all_evidence}".strip()
        try:
            candidate_summary = _validate_summary(combined_original, summary)
            result.summary = candidate_summary
            summary_status = "accepted"
        except ValueError:
            summary_status = "rejected"

    result.selection_audit["ai_rewrite"] = {
        "provider": "ollama-local",
        "model": model,
        "accepted_fact_ids": sorted(accepted),
        "rejected_fact_ids": rejected,
        "unknown_fact_ids_ignored": unknown_ids,
        "summary": summary_status,
        "review_required": True,
    }
    return result
