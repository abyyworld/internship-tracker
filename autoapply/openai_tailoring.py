from __future__ import annotations

from collections import Counter
import json
import os
from pathlib import Path
import re
from typing import Any

import requests

from .ai_tailoring import _validate_rewrite, _validate_summary
from .cv_editor import empty_draft
from .models import Job


OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL_DEFAULT = "gpt-4o-mini"
# Latency is dominated by how much text the model has to read and write. A job
# description repeats itself well before 8k characters, so the input stays
# capped. The output cap cannot be: entries in this CV are prose paragraphs, and
# 3-6 rewrites of them do not fit in a bullet-sized budget — a short cap would
# truncate the JSON mid-string and waste the whole call.
MAX_DESCRIPTION_CHARS = 8000
MAX_FACTS = 100
MAX_OUTPUT_TOKENS = 4000


def openai_key_path(home: Path) -> Path:
    return home / "openai.key"


def openai_key_configured(home: Path) -> bool:
    try:
        return bool(load_openai_key(home))
    except (FileNotFoundError, RuntimeError):
        return False


def load_openai_key(home: Path) -> str:
    # Allow env var override (useful for CI / cloud runners)
    env_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if env_key and len(env_key) >= 20 and not any(c.isspace() for c in env_key):
        return env_key
    path = openai_key_path(home)
    if not path.exists():
        raise FileNotFoundError("OpenAI API key is not configured")
    if path.is_symlink() or path.stat().st_mode & 0o077:
        raise RuntimeError("OpenAI key must be a private regular file with mode 0600")
    value = path.read_text(encoding="utf-8").strip()
    if len(value) < 20 or any(character.isspace() for character in value):
        raise RuntimeError("OpenAI API key is invalid")
    return value


def save_openai_key(home: Path, value: str) -> None:
    key = str(value).strip()
    if len(key) < 20 or any(character.isspace() for character in key):
        raise ValueError("Paste a valid OpenAI API key (sk-...)")
    home.mkdir(parents=True, exist_ok=True, mode=0o700)
    home.chmod(0o700)
    path = openai_key_path(home)
    if path.exists() and path.is_symlink():
        raise RuntimeError("Refusing a symbolic-link OpenAI key")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = -1
            handle.write(key + "\n")
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    path.chmod(0o600)


def _json_object(value: str) -> dict[str, Any]:
    cleaned = re.sub(r"<think>.*?</think>", "", value or "", flags=re.S).strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end <= start:
        raise RuntimeError("OpenAI returned no JSON suggestion object")
    try:
        parsed = json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError as exc:
        raise RuntimeError("OpenAI returned malformed suggestion JSON") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError("OpenAI returned an invalid suggestion object")
    return parsed


def _master_facts(document: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": bullet["id"],
            "verified_text": bullet["text"],
            # The model must match the rewrite to the shape of what it replaces:
            # a bold opening claim stays a claim, a prose body stays prose.
            "role_in_entry": "opening claim" if bullet.get("style") == "lead" else "body",
            "approx_chars": len(bullet["text"]),
            "entry": str(entry.get("title", "")),
            "organization": str(entry.get("organization", "")),
            "section": str(section.get("name", "")),
        }
        for section in document["sections"]
        for entry in section["entries"]
        for bullet in entry["bullets"]
    ][:MAX_FACTS]


def _prompt(
    job: Job,
    document: dict[str, Any],
    instructions: str,
) -> tuple[str, str]:
    system = (
        "You are a meticulous CV editor. Suggest a small patch, never a replacement "
        "CV. Return JSON only, with no markdown.\n"
        "METHOD. First read the posting and list the concrete requirements it "
        "states: named technologies, methods, domains, degree level, and "
        "responsibilities. Then pick the 3 to 6 verified facts whose existing "
        "evidence already speaks to those requirements, and rewrite only those so "
        "the matching evidence is stated plainly and early. Every rewrite must name "
        "the requirement it addresses in its rationale, quoting the posting's own "
        "wording. If the CV holds no evidence for a requirement, do not patch "
        "anything for it — report it in advice instead.\n"
        "RULES. The complete master CV is immutable: do not delete, merge, or omit "
        "any entry. Never invent or infer a skill, tool, metric, employer, date, "
        "responsibility, qualification, award, or result. A job requirement is not "
        "candidate evidence. Preserve every number and named technology exactly. "
        "Keep each proposal within roughly 20 percent of its original's "
        "approx_chars: a prose body stays a prose paragraph of similar depth, and "
        "an opening claim stays one or two sentences. Keep all material meaning of "
        "the verified original, write in natural language, and never keyword-stuff. "
        "The summary is optional and must rest only on the supplied evidence.\n"
        "Return exactly: "
        '{"requirements":["requirement quoted from the posting"],'
        '"summary":{"proposal":"...","rationale":"..."} or null,'
        '"bullets":[{"fact_id":"exact-id","proposal":"...",'
        '"rationale":"addresses <requirement> because ...","keywords":["..."]}],'
        '"advice":["gap the CV cannot evidence, or a short application note"]}.'
    )
    user = json.dumps(
        {
            "target_job": {
                "company": job.company,
                "role": job.role,
                "location": job.location,
                "description": job.description[:MAX_DESCRIPTION_CHARS],
            },
            "candidate_master_cv": {
                "existing_summary": document["summary"],
                "existing_summary_chars": len(document["summary"]),
                "education": document["education"],
                "verified_facts": _master_facts(document),
            },
            "candidate_instructions": instructions[:4000],
        },
        ensure_ascii=False,
    )
    return system, user


def generate_suggestions(
    job: Job,
    document: dict[str, Any],
    *,
    api_key: str,
    instructions: str = "",
    model: str = OPENAI_MODEL_DEFAULT,
    timeout: int = 120,
) -> dict[str, Any]:
    system, user = _prompt(job, document, instructions)
    try:
        response = requests.post(
            OPENAI_ENDPOINT,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": 0.2,
                "max_completion_tokens": MAX_OUTPUT_TOKENS,
                # Constrain decoding to valid JSON so a stray prose preamble
                # cannot waste a whole generation and force the user to retry.
                "response_format": {"type": "json_object"},
            },
            timeout=timeout,
        )
        response.raise_for_status()
        payload = response.json()
        content = payload["choices"][0]["message"]["content"]
        if isinstance(content, list):
            content = "".join(
                str(part.get("text", ""))
                for part in content
                if isinstance(part, dict)
            )
        generated = _json_object(str(content))
    except requests.Timeout as exc:
        raise RuntimeError(
            "OpenAI timed out. Retry once; no CV changes were saved."
        ) from exc
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        if status == 401:
            raise RuntimeError(
                "OpenAI API key is invalid or expired. Check your key."
            ) from exc
        if status == 429:
            raise RuntimeError(
                "OpenAI rate limit hit. Wait a moment and retry."
            ) from exc
        raise RuntimeError(
            f"OpenAI API returned HTTP {status}. Check the key and account balance."
        ) from exc
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as exc:
        raise RuntimeError(f"OpenAI request failed: {exc}") from exc

    originals = {
        bullet["id"]: bullet["text"]
        for section in document["sections"]
        for entry in section["entries"]
        for bullet in entry["bullets"]
    }
    draft = empty_draft(job.id, job.description_hash)
    draft["instructions"] = instructions[:4000]
    draft["requirements"] = [
        re.sub(r"\s+", " ", str(item)).strip()[:200]
        for item in list(generated.get("requirements") or [])[:12]
        if str(item).strip()
    ]
    draft["advice"] = [
        re.sub(r"\s+", " ", str(item)).strip()[:300]
        for item in list(generated.get("advice") or [])[:5]
        if str(item).strip()
    ]
    rejected: dict[str, str] = {}
    for raw in list(generated.get("bullets") or [])[:12]:
        if not isinstance(raw, dict):
            continue
        fact_id = str(raw.get("fact_id", "")).strip()
        if fact_id not in originals:
            rejected[fact_id or "<missing>"] = "unknown_fact_id"
            continue
        try:
            proposal = _validate_rewrite(
                originals[fact_id],
                str(raw.get("proposal", "")),
            )
        except ValueError as exc:
            rejected[fact_id] = str(exc)
            continue
        draft["bullets"][fact_id] = {
            "id": fact_id,
            "original": originals[fact_id],
            "proposal": proposal,
            "rationale": re.sub(
                r"\s+", " ", str(raw.get("rationale", ""))
            ).strip()[:800],
            "keywords": [
                re.sub(r"\s+", " ", str(item)).strip()[:80]
                for item in list(raw.get("keywords") or [])[:12]
                if str(item).strip()
            ],
            "status": "pending",
        }

    raw_summary = generated.get("summary")
    if isinstance(raw_summary, dict) and str(raw_summary.get("proposal", "")).strip():
        all_evidence = " ".join(
            [document["summary"], *originals.values(), *document["skills"]]
        )
        try:
            proposal = _validate_summary(
                all_evidence,
                str(raw_summary.get("proposal", "")),
                max_chars=int(len(document["summary"]) * 1.25),
            )
            draft["summary"] = {
                "id": "summary",
                "original": document["summary"],
                "proposal": proposal,
                "rationale": re.sub(
                    r"\s+", " ", str(raw_summary.get("rationale", ""))
                ).strip()[:800],
                "keywords": [],
                "status": "pending",
            }
        except ValueError as exc:
            rejected["summary"] = str(exc)
    draft["rejected_by_validator"] = rejected
    if not draft["bullets"] and not draft["summary"]:
        reasons = ", ".join(
            f"{reason}: {count}"
            for reason, count in sorted(Counter(rejected.values()).items())
        )
        raise RuntimeError(
            "OpenAI produced no evidence-safe suggestions. "
            f"Try a more specific instruction ({reasons or 'empty response'})."
        )
    return draft
