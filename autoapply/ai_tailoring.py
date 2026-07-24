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


def _validate_rewrite(original: str, candidate: str) -> str:
    value = re.sub(r"\s+", " ", candidate or "").strip().lstrip("•- ").strip()
    if not MIN_BULLET_CHARS <= len(value) <= MAX_BULLET_CHARS:
        raise ValueError("length")
    if _number_tokens(value) - _number_tokens(original):
        raise ValueError("new_numeric_claim")
    if _named_tokens(value) - _named_tokens(original):
        raise ValueError("new_named_technology_or_entity")
    original_lower = original.casefold()
    for phrase in RISKY_CLAIMS:
        if phrase in value.casefold() and phrase not in original_lower:
            raise ValueError("new_unsupported_qualification")
    original_terms = concepts(original)
    candidate_terms = concepts(value)
    if original_terms and len(original_terms & candidate_terms) / len(original_terms) < 0.3:
        raise ValueError("insufficient_evidence_overlap")
    return value


def _validate_summary(evidence: str, candidate: str) -> str:
    value = re.sub(r"\s+", " ", candidate or "").strip().lstrip("•- ").strip()
    if not 40 <= len(value) <= 420:
        raise ValueError("length")
    if _number_tokens(value) - _number_tokens(evidence):
        raise ValueError("new_numeric_claim")
    if _named_tokens(value) - _named_tokens(evidence):
        raise ValueError("new_named_technology_or_entity")
    evidence_lower = evidence.casefold()
    for phrase in RISKY_CLAIMS:
        if phrase in value.casefold() and phrase not in evidence_lower:
            raise ValueError("new_unsupported_qualification")
    evidence_terms = concepts(evidence)
    candidate_terms = concepts(value)
    if (
        candidate_terms
        and len(evidence_terms & candidate_terms) / len(candidate_terms) < 0.7
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
