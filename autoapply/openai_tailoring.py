"""Tailor a CV to one posting through the OpenAI API.

Three levels of intervention, chosen by the caller:

``targeted``    a handful of wording patches on the strongest lines.
``full``        every line rewritten for this posting, plus a rewritten
                summary and a section and entry order that leads with the
                most relevant work.
``aggressive``  as ``full``, and entries with nothing to say about this
                posting are left out of this job's CV.

Rewriting is unrestricted; inventing is not. The validators reject a proposal
that introduces a number, a named technology, an employer, or a qualification
the verified original did not contain, because a claim that collapses at
interview costs the offer that the rest of the tailoring won.

A full rewrite of this CV is far more text than one response can hold, so
generation runs as a small strategy call followed by one request per section,
issued in parallel. Wall time is roughly two round trips regardless of CV size.
"""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import threading
import json
import os
from pathlib import Path
import re
from typing import Any

import requests

from .ai_tailoring import (
    _credential_claims,
    _length_bounds,
    _named_tokens,
    _validate_rewrite,
    _validate_summary,
    borrowed_terms,
)
from .cv_editor import MAX_ANSWER_CHARS, MAX_QUESTIONS, empty_draft, ordered_sections
from .suggestion_quality import (
    coverage_score,
    is_generic_rationale,
    evidence_gaps,
    keyword_panel,
    posting_vocabulary,
    terms_gained,
)
from .tailoring import concepts
from .models import Job


# Any OpenAI-compatible endpoint. The wire format is the same across OpenAI,
# Ollama, Groq, OpenRouter, Google's compatibility layer, and GitHub Models,
# so pointing at a different base URL is the whole of switching provider —
# including to a model running on this machine for nothing.
OPENAI_BASE_DEFAULT = "https://api.openai.com/v1"
PROVIDERS = {
    "openai": {"label": "OpenAI", "base": "https://api.openai.com/v1",
               "key": "required", "models": []},
    "ollama": {"label": "Ollama (on this machine, free)",
               "base": "http://127.0.0.1:11434/v1", "key": "none", "models": []},
    "groq": {"label": "Groq (free tier)", "base": "https://api.groq.com/openai/v1",
             "key": "required", "models": []},
    "openrouter": {"label": "OpenRouter (has free models)",
                   "base": "https://openrouter.ai/api/v1", "key": "required",
                   "models": []},
    "cerebras": {"label": "Cerebras (free tier)", "base": "https://api.cerebras.ai/v1",
                 "key": "required", "models": []},
    "together": {"label": "Together AI", "base": "https://api.together.xyz/v1",
                 "key": "required", "models": []},
    "github": {"label": "GitHub Models (free with a GitHub account)",
               "base": "https://models.inference.ai.azure.com", "key": "required",
               "models": []},
    # Google serves an OpenAI-compatible chat endpoint but no model listing on
    # it, so the picker is seeded rather than discovered.
    "gemini": {"label": "Google AI Studio (free tier)",
               "base": "https://generativelanguage.googleapis.com/v1beta/openai",
               "key": "required",
               "models": ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]},
}


def base_url_path(home: Path) -> Path:
    return home / "ai-endpoint.txt"


def load_base_url(home: Path) -> str:
    path = base_url_path(home)
    if path.exists() and not path.is_symlink():
        value = path.read_text(encoding="utf-8").strip()
        if value.startswith(("https://", "http://127.0.0.1", "http://localhost")):
            return value.rstrip("/")
    return OPENAI_BASE_DEFAULT


def save_base_url(home: Path, value: str) -> str:
    url = str(value or "").strip().rstrip("/")
    # Remote providers must be HTTPS; a local runtime is exempt because
    # loopback traffic never leaves the machine.
    if not url.startswith(("https://", "http://127.0.0.1", "http://localhost")):
        raise ValueError("The endpoint must be HTTPS, or a local address")
    if len(url) > 200:
        raise ValueError("That endpoint URL is too long")
    home.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = base_url_path(home)
    path.write_text(url + "\n", encoding="utf-8")
    path.chmod(0o600)
    return url


def is_local(base_url: str) -> bool:
    return base_url.startswith(("http://127.0.0.1", "http://localhost"))
# Preference order, best value first. The account decides what it actually has;
# this only says which to reach for.
#
# Measured on one full rewrite of this CV against a software internship,
# counting lines the validators accepted and completion tokens billed:
#
#   gpt-5.4-mini  16s  29/45   8.9k out   rewrites read like the original
#   gpt-5.4       32s  41/45   9.6k out   strong verbs, real restructuring
#   gpt-5.5       48s  43/45  15.8k out   two more lines for 65% more output
#   gpt-5.6-sol   75s  44/45  15.1k out   best prose, 2.3x the wall time
#
# gpt-5.4 is the knee of that curve: 93% of the flagship's coverage for about
# 60% of the billed output and less than half the wait. The mini tier is a
# false economy — it returns fewer rewrites and the ones it returns barely
# differ from the text they replace. The picker still offers the rest, because
# a job worth 75 seconds is a decision only the applicant can make.
MODEL_PREFERENCE = (
    "gpt-5.4",
    "gpt-5.5",
    "gpt-5.6-sol",
    "gpt-5.1",
    "gpt-5",
    "gpt-4.1",
    "gpt-5.4-mini",
    "gpt-5-mini",
    "gpt-4o",
    "gpt-4o-mini",
)
OPENAI_MODEL_DEFAULT = MODEL_PREFERENCE[0]
# Newer models fix sampling temperature and reject the parameter outright.
FIXED_TEMPERATURE_MODELS = ("gpt-5.5", "gpt-5.6", "gpt-5-mini", "gpt-5-nano")
# Thinking models spend their reply budget on reasoning before writing a word,
# and every provider counts that against the same limit. A local Qwen3 burned
# all 2600 tokens deliberating and returned nothing at all; the same starvation
# is available to any hosted thinking model.
#
# These calls are extraction against a fixed schema, not problems that reward
# deliberation, so the ones that allow it are asked to think briefly or not at
# all. OpenAI's own default is deliberately left alone: it is what the measured
# quality here was measured with.
REASONING_EFFORT = {
    "gemini-2.5-flash": "none",
    # Pro cannot switch thinking off; it can be asked to keep it short.
    "gemini-2.5-pro": "low",
    "qwen": "none",
    "deepseek-r1": "low",
}


def _reasoning_effort(model: str) -> str:
    name = str(model or "").lower()
    for prefix, effort in REASONING_EFFORT.items():
        if name.startswith(prefix):
            return effort
    return ""
# A job description repeats itself well before 8k characters. The strategy call
# reads it in full; the section calls receive only the requirements it found,
# which keeps every parallel request small and fast.
MAX_DESCRIPTION_CHARS = 8000
MAX_SECTION_OUTPUT_TOKENS = 6000
# Alternatives are only worth generating for lines short enough that a reader
# will actually compare them. Three phrasings of an 1800-character paragraph
# cost three times the tokens, crowd out other sections, and nobody reads past
# the first — so long prose gets one considered rewrite instead.
VARIANT_MAX_CHARS = 420
# The strategy call returns requirements, a full running order, and a
# rewritten summary; 1200 tokens truncated it on postings with many
# requirements, and a truncated plan is a lost generation.
MAX_STRATEGY_OUTPUT_TOKENS = 2600
MAX_PARALLEL_REQUESTS = 6
# An alternative phrasing and an added line are both single CV lines.
MAX_VARIANTS = 3
MAX_VARIANT_CHARS = 2600
MIN_ADDED_CHARS = 40
MAX_ADDED_CHARS = 400
MAX_ADDED_PER_ENTRY = 2
# Rewriting whole prose entries at temperature 0 produces near-copies; a little
# freedom is what makes a rewrite actually read differently.
TEMPERATURE = 0.35


def openai_key_path(home: Path) -> Path:
    return home / "openai.key"


def openai_key_configured(home: Path) -> bool:
    if is_local(load_base_url(home)):
        return True
    try:
        return bool(load_openai_key(home))
    except (FileNotFoundError, RuntimeError):
        return False


def load_key_for(home: Path) -> str:
    """The key for the configured endpoint, or none when it is local."""
    if is_local(load_base_url(home)):
        return ""
    return load_openai_key(home)


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


def _salvage_json(text: str) -> dict[str, Any] | None:
    """Recover the complete part of a response that was cut off mid-value.

    Hitting the output token cap truncates the JSON, and discarding the whole
    response loses every rewrite that had already been written. Rewinding to
    the last finished element and closing the open brackets keeps them.
    """
    depth: list[str] = []
    in_string = escaped = False
    rewind: tuple[int, tuple[str, ...]] | None = None
    for index, character in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character in "{[":
            depth.append("}" if character == "{" else "]")
        elif character in "}]":
            if depth:
                depth.pop()
        elif character == "," and depth:
            rewind = (index, tuple(depth))
    if rewind is None:
        return None
    index, open_brackets = rewind
    try:
        parsed = json.loads(text[:index] + "".join(reversed(open_brackets)))
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def model_path(home: Path) -> Path:
    return home / "openai-model.txt"


def load_model(home: Path) -> str:
    path = model_path(home)
    if path.exists() and not path.is_symlink():
        chosen = path.read_text(encoding="utf-8").strip()
        if chosen and len(chosen) < 64:
            return chosen
    return OPENAI_MODEL_DEFAULT


def save_model(home: Path, value: str) -> str:
    chosen = re.sub(r"[^A-Za-z0-9._-]", "", str(value or "")).strip()
    if not chosen or len(chosen) > 63:
        raise ValueError("Choose a model from the list")
    home.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = model_path(home)
    path.write_text(chosen + "\n", encoding="utf-8")
    path.chmod(0o600)
    return chosen


def available_models(
    api_key: str,
    *,
    timeout: int = 20,
    base_url: str = OPENAI_BASE_DEFAULT,
) -> list[str]:
    """Chat models this endpoint offers, best first, then the rest."""
    try:
        response = requests.get(
            f"{base_url}/models",
            headers=({"Authorization": f"Bearer {api_key}"} if api_key else {}),
            timeout=timeout,
        )
        response.raise_for_status()
        found = {str(item.get("id", "")) for item in response.json().get("data", [])}
    except (requests.RequestException, KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(f"Could not list OpenAI models: {exc}") from exc
    skip = ("audio", "realtime", "transcribe", "tts", "image", "embedding",
            "moderation", "search", "codex", "instruct", "whisper", "guard")
    usable = sorted(
        name for name in found
        if not any(word in name for word in skip)
    )
    preferred = [name for name in MODEL_PREFERENCE if name in found]
    return preferred + [name for name in usable if name not in preferred]


def models_for(base_url: str, api_key: str) -> list[str]:
    """Models to offer for an endpoint, asking it first and seeding if it cannot say."""
    try:
        found = available_models(api_key, base_url=base_url)
    except RuntimeError:
        found = []
    if found:
        return found
    for provider in PROVIDERS.values():
        if provider["base"] == base_url and provider["models"]:
            return list(provider["models"])
    return []


def best_available_model(api_key: str) -> str:
    try:
        models = available_models(api_key)
    except RuntimeError:
        return OPENAI_MODEL_DEFAULT
    return models[0] if models else OPENAI_MODEL_DEFAULT


def _json_object(value: str) -> dict[str, Any]:
    cleaned = re.sub(r"<think>.*?</think>", "", value or "", flags=re.S).strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0:
        raise RuntimeError("OpenAI returned no JSON suggestion object")
    if end > start:
        try:
            parsed = json.loads(cleaned[start : end + 1])
            if not isinstance(parsed, dict):
                raise RuntimeError("OpenAI returned an invalid suggestion object")
            return parsed
        except json.JSONDecodeError:
            pass
    salvaged = _salvage_json(cleaned[start:])
    if salvaged is None:
        raise RuntimeError("OpenAI returned malformed suggestion JSON")
    return salvaged


def _clean_list(values: Any, *, limit: int, chars: int) -> list[str]:
    return [
        re.sub(r"\s+", " ", str(item)).strip()[:chars]
        for item in list(values or [])[:limit]
        if str(item).strip()
    ]


def _ask(
    system: str,
    user: str,
    *,
    api_key: str,
    model: str,
    max_tokens: int,
    timeout: int,
    base_url: str = OPENAI_BASE_DEFAULT,
) -> dict[str, Any]:
    """One chat completion, decoded as a JSON object.

    A timeout is retried once. The API's latency for a long prose generation
    varies by more than an order of magnitude minute to minute, and losing a
    whole section's rewrite to one slow response is worth a second attempt.
    """
    for attempt in (1, 2):
        try:
            return _ask_once(
                system, user,
                api_key=api_key, model=model,
                max_tokens=max_tokens, timeout=timeout, base_url=base_url,
            )
        except RuntimeError as exc:
            if attempt == 2 or "timed out" not in str(exc):
                raise
    raise RuntimeError("OpenAI request failed")


# Token accounting. Every provider reports usage the same way, so the cost of
# one tailoring is measurable rather than estimated — which is the only way to
# compare a free tier against a paid one honestly.
_usage_lock = threading.Lock()
_usage: dict[str, int] | None = None


@contextmanager
def track_usage():
    """Collect token usage for everything run inside the block."""
    global _usage
    with _usage_lock:
        _usage = {"input": 0, "output": 0, "calls": 0}
    try:
        yield lambda: dict(_usage or {})
    finally:
        with _usage_lock:
            _usage = None


def _record_usage(payload: dict[str, Any]) -> None:
    usage = payload.get("usage") or {}
    with _usage_lock:
        if _usage is None:
            return
        _usage["input"] += int(usage.get("prompt_tokens", 0) or 0)
        _usage["output"] += int(usage.get("completion_tokens", 0) or 0)
        _usage["calls"] += 1


# Parameters no provider is required to support. `max_completion_tokens` is
# the newer spelling; older and third-party endpoints still expect `max_tokens`.
OPTIONAL_PARAMS = (
    "response_format", "temperature", "max_completion_tokens", "reasoning_effort",
)


def _request_body(
    system: str, user: str, *, model: str, max_tokens: int
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_completion_tokens": max_tokens,
        # Constrain decoding to valid JSON so a stray prose preamble cannot
        # waste a whole generation and force the user to retry.
        "response_format": {"type": "json_object"},
    }
    if not model.startswith(FIXED_TEMPERATURE_MODELS):
        body["temperature"] = TEMPERATURE
    effort = _reasoning_effort(model)
    if effort:
        body["reasoning_effort"] = effort
    return body


def provider_label(base_url: str) -> str:
    """Name whoever is actually being called, for anything a person reads.

    Every message here used to say "OpenAI" because that was the only
    endpoint. Telling someone their OpenAI key is invalid while they are
    pointed at Google is a small lie that costs a long debugging session.
    """
    for provider in PROVIDERS.values():
        if provider["base"] == str(base_url or "").rstrip("/"):
            return str(provider["label"]).split(" (")[0]
    return "The AI endpoint"


_AUTH_WORDING = re.compile(
    r"\bauthoriz|\bauthentic|\bapi[ _-]?key\b|\bcredential|\bunauthenticated\b", re.I
)


def _is_auth_error(response: Any) -> bool:
    try:
        message = str(response.json().get("error", {}).get("message", ""))
    except Exception:
        return False
    return bool(_AUTH_WORDING.search(message))


def _without_rejected(
    body: dict[str, Any], response: Any
) -> dict[str, Any] | None:
    """Drop the parameter a 400 complained about, if it is an optional one."""
    try:
        message = str(response.json().get("error", {}).get("message", ""))
    except Exception:
        return None
    for name in OPTIONAL_PARAMS:
        if name in message and name in body:
            reduced = dict(body)
            value = reduced.pop(name)
            # An endpoint that rejects the new spelling wants the old one.
            if name == "max_completion_tokens":
                reduced["max_tokens"] = value
            return reduced
    return None


def _ask_once(
    system: str,
    user: str,
    *,
    api_key: str,
    model: str,
    max_tokens: int,
    timeout: int,
    base_url: str = OPENAI_BASE_DEFAULT,
) -> dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    body = _request_body(system, user, model=model, max_tokens=max_tokens)
    who = provider_label(base_url)
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=body,
            timeout=timeout,
        )
        # Providers differ on which optional parameters they accept. Rather
        # than maintain a compatibility matrix, drop whatever one objects to
        # and ask again: the request still works, just less constrained.
        if response.status_code == 400:
            reduced = _without_rejected(body, response)
            if reduced is not None:
                response = requests.post(
                    f"{base_url}/chat/completions",
                    headers=headers, json=reduced, timeout=timeout,
                )
        response.raise_for_status()
        payload = response.json()
        _record_usage(payload)
        content = payload["choices"][0]["message"]["content"]
        if isinstance(content, list):
            content = "".join(
                str(part.get("text", ""))
                for part in content
                if isinstance(part, dict)
            )
        return _json_object(str(content))
    except requests.Timeout as exc:
        raise RuntimeError(
            f"{who} timed out. Retry once; no CV changes were saved."
        ) from exc
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        # Not every provider answers a missing key with 401: Google returns a
        # 400 saying so. Reporting that as a generic bad request sends someone
        # hunting through their request instead of their key.
        if status == 401 or (status == 400 and _is_auth_error(exc.response)):
            raise RuntimeError(
                f"The {who} API key is missing, invalid, or expired. Check your key."
            ) from exc
        if status == 429:
            raise RuntimeError(
                f"{who} rate limit hit. Wait a moment and retry."
            ) from exc
        raise RuntimeError(
            f"{who} returned HTTP {status}. Check the key and account balance."
        ) from exc
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as exc:
        raise RuntimeError(f"{who} request failed: {exc}") from exc


# ── Rules every call shares ──────────────────────────────────────────────────

_TRUTH_RULES = (
    "TRUTH. Rewrite as freely as the evidence allows, but never introduce a "
    "skill, tool, metric, employer, date, responsibility, qualification, "
    "award, or result the verified text does not already contain. A "
    "requirement in the posting is not evidence the candidate meets it. Keep "
    "every number and named technology exactly as written, and never add one. "
    "Claiming what cannot be evidenced loses the offer at interview, which "
    "costs more than the wording gains."
)


def _entry_index(document: dict[str, Any]) -> list[dict[str, Any]]:
    """A compact map of the CV: enough to plan an order, small enough to be fast."""
    index: list[dict[str, Any]] = []
    for section in document["sections"]:
        entries = []
        for entry in section["entries"]:
            gist = " ".join(bullet["text"] for bullet in entry["bullets"])
            entries.append({
                "entry_id": entry.get("id", ""),
                "title": entry.get("title", ""),
                "context": entry.get("organization", ""),
                "gist": gist[:260],
            })
        index.append({
            "section_id": section.get("id", ""),
            "section": section.get("name", ""),
            "entries": entries,
        })
    return index


def _standing_order(instructions: str) -> str:
    """The applicant's own instruction, promoted to the top of the prompt.

    Buried in the payload as one field among many it was routinely ignored.
    It is the one part of the prompt the person actually wrote, so it outranks
    the defaults and is stated before them.
    """
    text = re.sub(r"\s+", " ", str(instructions or "")).strip()
    if not text:
        return ""
    return (
        "THE APPLICANT'S INSTRUCTION, WHICH OUTRANKS EVERY DEFAULT BELOW "
        "EXCEPT THE TRUTH RULES: " + text[:2000] + "\n"
        "Follow it exactly. If it conflicts with a default about emphasis, "
        "ordering, tone, or length, the instruction wins.\n\n"
    )


def _strategy(
    job: Job,
    document: dict[str, Any],
    instructions: str,
    mode: str,
    *,
    api_key: str,
    model: str,
    timeout: int,
    base_url: str = OPENAI_BASE_DEFAULT,
) -> dict[str, Any]:
    """Read the posting once: requirements, running order, and the summary."""
    drop_rule = (
        "Also list in `drop` the entry_ids that say nothing about this posting "
        "and would only dilute the CV. Never drop education, and leave at "
        "least half the entries of any section in place."
        if mode == "aggressive"
        else "Leave `drop` empty."
    )
    system = (
        _standing_order(instructions)
        + "You are a CV strategist. Return JSON only, no markdown.\n"
        "ORDER. Lead with the section a reader hiring for THIS posting opens "
        "with. For an engineering, software, quant, or industry role that is "
        "employment and the projects that look like the job; academic research "
        "and publications come after. For a research, PhD, postdoc, or lab "
        "role it is the research. Never lead with a section merely because it "
        "is the candidate's favourite work: match the reader.\n"
        "Read the posting and extract the concrete requirements it states: "
        "named technologies, methods, domains, degree level, and "
        "responsibilities, quoting its own wording. Then decide how this "
        "candidate's CV should be ordered so a reader who spends thirty "
        "seconds on it sees the most relevant evidence first. Order sections "
        "by relevance to this posting, and entries within each section the "
        "same way. Include every section_id and every entry_id you are given "
        "exactly once. " + drop_rule + "\n"
        "Write `priorities`: three short notes telling the rewriter what to "
        "foreground across the whole CV for this role.\n"
        "In `keywords`, list 12 to 20 terms an ATS would screen this "
        "application on — named technologies, methods, and domains, one to "
        "three words each, never a sentence or a date. Mark each covered when "
        "the CV already uses it and missing when it does not, with importance "
        "high, medium, or low. Fewer than a dozen makes the coverage figure "
        "derived from them meaningless.\n"
        "In `advice`, name only requirements this CV genuinely cannot evidence, "
        "and say what the applicant could honestly do before the deadline. "
        "Never suggest claiming something they have not done, and never pad the "
        "list: an empty `advice` is a better answer than a generic one.\n"
        "Rewrite the summary so it opens on the candidate's evidence that "
        "matters most for this posting. It describes the CANDIDATE, never the "
        "company or the vacancy: do not name the employer, do not restate the "
        "advert, and do not write that anyone is seeking or hiring anyone. "
        "Keep the original's third-person voice and stay within about 20 "
        "percent of its length.\n"
        + _TRUTH_RULES + "\n"
        "Return exactly: "
        '{"requirements":["..."],"section_order":["s0",...],'
        '"keywords":[{"term":"...","status":"covered|missing","importance":"high|medium|low"}],'
        '"entry_order":{"s0":["s0e1",...]},"drop":["s2e3"],'
        '"priorities":["..."],'
        '"summary":{"proposal":"...","rationale":"..."},'
        '"advice":["<a requirement this CV cannot evidence, and what the '
        'applicant could honestly do about it before the deadline; omit if '
        'there is none>"]}'
    )
    user = json.dumps(
        {
            "target_job": {
                "company": job.company,
                "role": job.role,
                "location": job.location,
                "description": job.description[:MAX_DESCRIPTION_CHARS],
            },
            "candidate_summary": document["summary"],
            "candidate_summary_chars": len(document["summary"]),
            "cv_map": _entry_index(document),
            "candidate_instructions": instructions[:4000],
        },
        ensure_ascii=False,
    )
    return _ask(
        system, user,
        api_key=api_key, model=model,
        max_tokens=MAX_STRATEGY_OUTPUT_TOKENS, timeout=timeout, base_url=base_url,
    )


def _rewrite_section(
    section: dict[str, Any],
    job: Job,
    requirements: list[str],
    priorities: list[str],
    instructions: str,
    mode: str,
    *,
    api_key: str,
    model: str,
    timeout: int,
    base_url: str = OPENAI_BASE_DEFAULT,
) -> dict[str, Any]:
    """Rewrite every line of one section against the posting's requirements."""
    scope = (
        "Rewrite EVERY fact you are given. Return one entry per fact_id, with "
        "no omissions."
        if mode != "targeted"
        else "Rewrite only the three or four facts that most answer the "
             "requirements. Leave the rest alone."
    )
    system = (
        _standing_order(instructions)
        + "You are rewriting one section of a CV for one job. Return JSON only, "
        "no markdown.\n" + scope + "\n"
        "Lead each line with the evidence this posting cares about, use the "
        "posting's own vocabulary wherever the verified text already supports "
        "it, and cut throat-clearing. Match the shape of what you replace: a "
        "fact whose role is `opening claim` stays one or two sentences and a "
        "`body` stays a paragraph of comparable depth. Every proposal MUST be "
        "between its own min_chars and max_chars; a shorter one is discarded "
        "unread, so keep the supporting detail rather than summarising it "
        "away. Write natural prose; never produce a keyword list.\n"
        "RATIONALE. Write it as the edit itself: name the posting requirement "
        "the line now answers, and quote the original wording you replaced and "
        "the posting's own phrase you replaced it with - for example: replaces "
        "\"worked on models\" with the posting's \"distributed training\". A "
        "rationale that would be true of any rewrite of any line (\"stronger "
        "verb\", \"clearer\", \"more impactful\") is discarded, because the "
        "reader cannot check it and cannot decide on it.\n"
        "In `keywords`, list only terms that appear in the proposal you just "
        "wrote. It is checked.\n"
        "When a fact says `alternatives: 2`, also give `variants`: two further "
        "phrasings of that same line which a reader would genuinely choose "
        "between — one plainer and more direct, one leading with a different "
        "piece of the same evidence. They are alternatives, not near-copies, "
        "and each must obey every rule above including the length band. When a "
        "fact says `alternatives: 0`, return `variants` empty: that line is a "
        "full paragraph and one considered rewrite is worth more than three "
        "hurried ones.\n"
        "In `add`, propose at most one extra line for an entry when that "
        "entry's own verified text already contains evidence for a requirement "
        "that its current lines bury. An added line restates evidence already "
        "present in that entry; if there is none to restate, add nothing.\n"
        + _TRUTH_RULES + "\n"
        'Return exactly: {"bullets":[{"fact_id":"exact-id","proposal":"...",'
        '"variants":["...","..."],'
        '"rationale":"answers <requirement> ...","keywords":["..."]}],'
        '"add":[{"entry_id":"s0e1","text":"...","rationale":"..."}]}'
    )
    facts = []
    for entry in section["entries"]:
        for bullet in entry["bullets"]:
            low, high = _length_bounds(bullet["text"], strict=mode == "targeted")
            facts.append({
                "fact_id": bullet["id"],
                "verified_text": bullet["text"],
                "role": "opening claim" if bullet.get("style") == "lead" else "body",
                # The exact band the validator enforces. Told a percentage, the
                # model compresses past the floor and the rewrite is discarded.
                "min_chars": low,
                "max_chars": high,
                "alternatives": 2 if len(bullet["text"]) <= VARIANT_MAX_CHARS else 0,
                "entry": entry.get("title", ""),
                "context": entry.get("organization", ""),
            })
    user = json.dumps(
        {
            "target_job": {"company": job.company, "role": job.role},
            "requirements": requirements,
            "priorities": priorities,
            "candidate_instructions": instructions[:2000],
            "section": section.get("name", ""),
            "entries": [
                {"entry_id": entry.get("id", ""), "title": entry.get("title", "")}
                for entry in section["entries"]
            ],
            "facts": facts,
        },
        ensure_ascii=False,
    )
    return _ask(
        system, user,
        api_key=api_key, model=model,
        max_tokens=MAX_SECTION_OUTPUT_TOKENS, timeout=timeout, base_url=base_url,
    )


# Rejections worth a second attempt. A proposal that was the wrong length or
# drifted off its own subject is badly shaped, not dishonest, and the model can
# fix it when told exactly what was wrong. The fabrication rejections are never
# retried: asking again for a claim the CV cannot support is asking for a
# better-disguised version of the same claim.
REPAIRABLE = {"length", "insufficient_evidence_overlap"}


def _repair(
    job: Job,
    broken: list[dict[str, Any]],
    requirements: list[str],
    *,
    api_key: str,
    model: str,
    timeout: int,
    base_url: str = OPENAI_BASE_DEFAULT,
) -> dict[str, Any]:
    """Re-request the rewrites that came back the wrong shape."""
    system = (
        "Your previous rewrites of these CV lines were rejected. Return JSON "
        "only, no markdown. For each one, produce a replacement that fixes the "
        "stated problem while still answering the posting's requirements.\n"
        "`length` means your text fell outside min_chars..max_chars. Count "
        "characters: below the floor, keep the original's supporting detail "
        "instead of summarising it away.\n"
        "`insufficient_evidence_overlap` means you drifted off the subject of "
        "the verified text. Stay on what that line is actually about.\n"
        "Each rationale must name the requirement answered or quote the wording "
        "changed; praise for the rewrite is discarded.\n"
        + _TRUTH_RULES + "\n"
        'Return exactly: {"bullets":[{"fact_id":"exact-id","proposal":"...",'
        '"rationale":"...","keywords":["..."]}]}'
    )
    user = json.dumps(
        {
            "target_job": {"company": job.company, "role": job.role},
            "requirements": requirements,
            "rejected": broken,
        },
        ensure_ascii=False,
    )
    return _ask(
        system, user,
        api_key=api_key, model=model,
        max_tokens=MAX_SECTION_OUTPUT_TOKENS, timeout=timeout, base_url=base_url,
    )


def generate_suggestions(
    job: Job,
    document: dict[str, Any],
    *,
    api_key: str,
    instructions: str = "",
    mode: str = "full",
    model: str = OPENAI_MODEL_DEFAULT,
    timeout: int = 120,
    base_url: str = OPENAI_BASE_DEFAULT,
) -> dict[str, Any]:
    if mode not in {"targeted", "full", "aggressive"}:
        raise ValueError("Unknown tailoring mode")

    plan = _strategy(
        job, document, instructions, mode,
        api_key=api_key, model=model, timeout=timeout, base_url=base_url,
    )
    requirements = _clean_list(plan.get("requirements"), limit=14, chars=200)
    priorities = _clean_list(plan.get("priorities"), limit=5, chars=200)

    sections = document["sections"]
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_REQUESTS) as pool:
        futures = [
            pool.submit(
                _rewrite_section,
                section, job, requirements, priorities, instructions, mode,
                api_key=api_key, model=model, timeout=timeout, base_url=base_url,
            )
            for section in sections
        ]
        results: list[dict[str, Any] | None] = []
        failures: list[str] = []
        for future in futures:
            try:
                results.append(future.result())
            except RuntimeError as exc:
                # One section failing must not discard the rest of the rewrite.
                results.append(None)
                failures.append(str(exc))

    originals = {
        bullet["id"]: bullet["text"]
        for section in sections
        for entry in section["entries"]
        for bullet in entry["bullets"]
    }
    # An entry's heading and sibling lines are already-verified evidence for
    # any line inside it.
    # Requirement words the CV never uses may not appear in any rewrite.
    cv_text = " ".join([
        document["summary"],
        *(str(skill) for skill in document.get("skills", [])),
        *(str(entry.get("title", "")) for section in sections for entry in section["entries"]),
        *(str(entry.get("organization", "")) for section in sections for entry in section["entries"]),
        *originals.values(),
    ])
    cv_terms = concepts(cv_text)
    forbidden = borrowed_terms(requirements, cv_text)
    document_evidence = " ".join([
        document["summary"],
        *(str(skill) for skill in document.get("skills", [])),
        *(str(entry.get("title", "")) for section in sections for entry in section["entries"]),
        *(str(entry.get("organization", "")) for section in sections for entry in section["entries"]),
        *originals.values(),
    ])
    entry_only_evidence = {
        str(entry.get("id", "")): " ".join([
            str(entry.get("title", "")),
            str(entry.get("organization", "")),
            *(bullet["text"] for bullet in entry["bullets"]),
        ])
        for section in sections
        for entry in section["entries"]
    }
    # What a line may draw on. General self-claims - the summary and the skills
    # list - plus the entry the line sits in. Every entry in the document used
    # to be in scope, which meant a metric from one project could be restated as
    # the result of another and pass every check.
    general_claims = " ".join([
        document["summary"],
        *(str(skill) for skill in document.get("skills", [])),
    ])
    entry_evidence = {
        bullet["id"]: f"{general_claims} {entry_only_evidence[str(entry.get('id', ''))]}"
        for section in sections
        for entry in section["entries"]
        for bullet in entry["bullets"]
    }
    # What a line may attribute to itself: numbers, dates, and qualifications
    # belong to the piece of work that earned them.
    bullet_entry_text = {
        bullet["id"]: entry_only_evidence[str(entry.get("id", ""))]
        for section in sections
        for entry in section["entries"]
        for bullet in entry["bullets"]
    }
    section_ids = [str(section.get("id", "")) for section in sections]
    entry_ids = {
        str(entry.get("id", ""))
        for section in sections
        for entry in section["entries"]
    }

    draft = empty_draft(job.id, job.description_hash)
    draft["mode"] = mode
    draft["instructions"] = instructions[:4000]
    draft["requirements"] = requirements
    # Whether the CV contains a term is a fact, so the model's own claim about
    # coverage is discarded and recomputed, and the score is derived from the
    # same checked statuses the panel shows rather than asserted separately.
    keywords = keyword_panel(plan.get("keywords"), cv_text)
    draft["keywords"] = keywords
    draft["match_score"] = coverage_score(keywords)
    posting_terms = posting_vocabulary(requirements, keywords)
    # The model's advice first, then the gaps counted from the panel. A term
    # the CV cannot evidence is the part of this application still worth the
    # applicant's time, so it is named rather than left out.
    draft["advice"] = _clean_list(plan.get("advice"), limit=6, chars=300)
    draft["gaps"] = evidence_gaps(keywords)
    for gap in draft["gaps"]:
        if gap not in draft["advice"]:
            draft["advice"].append(gap)
    if failures:
        draft["advice"].append(
            f"{len(failures)} section(s) could not be rewritten: {failures[0]}"
        )

    # Ordering. Anything the model omitted keeps its master position, so a
    # partial answer reorders what it named and leaves the rest alone.
    if mode != "targeted":
        wanted = [
            str(value) for value in list(plan.get("section_order") or [])[:64]
            if str(value) in section_ids
        ]
        draft["order"]["sections"] = wanted + [
            identifier for identifier in section_ids if identifier not in wanted
        ]
        raw_entries = plan.get("entry_order")
        if isinstance(raw_entries, dict):
            draft["order"]["entries"] = {
                str(key): [
                    str(value) for value in list(values or [])[:128]
                    if str(value) in entry_ids
                ]
                for key, values in list(raw_entries.items())[:64]
                if str(key) in section_ids
            }
    if mode == "aggressive":
        draft["hidden"] = [
            str(value) for value in list(plan.get("drop") or [])[:64]
            if str(value) in entry_ids
        ]

    rejected: dict[str, str] = {}

    def accept(raw: Any) -> None:
        if not isinstance(raw, dict):
            return
        fact_id = str(raw.get("fact_id", "")).strip()
        if fact_id not in originals:
            rejected[fact_id or "<missing>"] = "unknown_fact_id"
            return
        try:
            proposal = _validate_rewrite(
                originals[fact_id],
                str(raw.get("proposal", "")),
                strict=mode == "targeted",
                evidence=entry_evidence.get(fact_id, ""),
                local_evidence=bullet_entry_text.get(fact_id, ""),
                forbidden=forbidden,
            )
        except ValueError as exc:
            rejected[fact_id] = str(exc)
            return
        if proposal == originals[fact_id]:
            rejected.pop(fact_id, None)
            return
        # Alternatives go through exactly the same guards; one that fails is
        # dropped rather than failing the whole line.
        variants = [proposal]
        for candidate in _clean_list(raw.get("variants"), limit=4, chars=MAX_VARIANT_CHARS):
            if len(variants) >= MAX_VARIANTS:
                break
            try:
                checked = _validate_rewrite(
                    originals[fact_id], candidate,
                    strict=mode == "targeted",
                    evidence=entry_evidence.get(fact_id, ""),
                    local_evidence=bullet_entry_text.get(fact_id, ""),
                    forbidden=forbidden,
                )
            except ValueError:
                continue
            if checked not in variants and checked != originals[fact_id]:
                variants.append(checked)
        rejected.pop(fact_id, None)
        rationale = re.sub(r"\s+", " ", str(raw.get("rationale", ""))).strip()[:800]
        draft["bullets"][fact_id] = {
            "id": fact_id,
            "original": originals[fact_id],
            "proposal": proposal,
            "variants": variants,
            # A rationale that would be true of any rewrite is worse than none:
            # it fills the space where a reason should be. Dropped, so the
            # editor shows the counted keyword gain instead.
            "rationale": "" if is_generic_rationale(rationale, posting_terms)
            else rationale,
            "keywords": _clean_list(raw.get("keywords"), limit=12, chars=80),
            # Counted, not claimed: the posting vocabulary this rewrite brings
            # into the line and the original did not already use. A rewrite
            # that gains nothing is a rephrasing, and saying so lets the
            # applicant spend their review time on the ones that matter.
            "adds_keywords": terms_gained(originals[fact_id], proposal, posting_terms),
            "status": "pending",
            "source": "ai",
        }

    def accept_added(raw: Any) -> None:
        """A proposed extra line, checked against the entry it would join."""
        if not isinstance(raw, dict):
            return
        entry_id = str(raw.get("entry_id", "")).strip()
        evidence = entry_only_evidence.get(entry_id)
        if evidence is None:
            return
        text = re.sub(r"\s+", " ", str(raw.get("text", ""))).strip()
        if not MIN_ADDED_CHARS <= len(text) <= MAX_ADDED_CHARS:
            rejected[f"add:{entry_id}"] = "length"
            return
        try:
            # An added line has no original to measure against, so the entry's
            # own verified text is both its evidence and its subject.
            _validate_rewrite(
                evidence, text,
                strict=False,
                evidence=f"{general_claims} {evidence}",
                local_evidence=evidence,
                forbidden=forbidden,
            )
        except ValueError as exc:
            rejected[f"add:{entry_id}"] = str(exc)
            return
        lines = draft["added"].setdefault(entry_id, [])
        if len(lines) >= MAX_ADDED_PER_ENTRY or any(l["text"] == text for l in lines):
            return
        added_rationale = re.sub(
            r"\s+", " ", str(raw.get("rationale", ""))
        ).strip()[:800]
        lines.append({
            "id": f"{entry_id}-new{len(lines)}",
            "text": text,
            # Held to the same standard as a rewrite: a reason that would be
            # true of any added line is not a reason to add this one.
            "rationale": "" if is_generic_rationale(added_rationale, posting_terms)
            else added_rationale,
            # An added line is new text, so everything it says that the posting
            # screens on is a gain.
            "adds_keywords": terms_gained("", text, posting_terms),
            "status": "pending",
            "source": "ai",
        })

    for result in results:
        if not result:
            continue
        for raw in list(result.get("bullets") or [])[:80]:
            accept(raw)
        for raw in list(result.get("add") or [])[:12]:
            accept_added(raw)

    # One repair round for the badly-shaped ones, so a rewrite is not lost to a
    # character count the model can simply be told to correct.
    broken = [
        {
            "fact_id": fact_id,
            "verified_text": originals[fact_id],
            "problem": reason,
            "min_chars": _length_bounds(originals[fact_id], strict=mode == "targeted")[0],
            "max_chars": _length_bounds(originals[fact_id], strict=mode == "targeted")[1],
        }
        for fact_id, reason in list(rejected.items())
        if reason in REPAIRABLE and fact_id in originals
    ]
    if broken:
        try:
            repaired = _repair(
                job, broken[:16], requirements,
                api_key=api_key, model=model, timeout=timeout, base_url=base_url,
            )
        except RuntimeError:
            repaired = {}
        for raw in list(repaired.get("bullets") or [])[:32]:
            accept(raw)

    raw_summary = plan.get("summary")
    if isinstance(raw_summary, dict) and str(raw_summary.get("proposal", "")).strip():
        all_evidence = " ".join([document["summary"], *originals.values()])
        try:
            draft["summary"] = {
                "id": "summary",
                "original": document["summary"],
                "proposal": _validate_summary(
                    all_evidence,
                    str(raw_summary.get("proposal", "")),
                    max_chars=int(len(document["summary"]) * 1.25),
                    strict=mode == "targeted",
                    forbidden=forbidden,
                    original=document["summary"],
                ),
                "rationale": re.sub(
                    r"\s+", " ", str(raw_summary.get("rationale", ""))
                ).strip()[:800],
                "keywords": [],
                "status": "pending",
                "source": "ai",
            }
        except ValueError as exc:
            rejected["summary"] = str(exc)

    draft["rejected_by_validator"] = rejected
    # A running order identical to the master is not a suggestion. Compare the
    # order the draft actually produces, not merely whether one was recorded.
    master = [
        entry.get("id", "")
        for section in sections
        for entry in section["entries"]
    ]
    tailored = [
        entry.get("id", "")
        for section in ordered_sections(document, draft)
        for entry in section["entries"]
    ]
    # An accepted added line is a suggestion too. Leaving it out of this test
    # threw away a generation whose only output was a set of valid new lines,
    # and reported it as having produced nothing evidence-safe.
    if (
        not draft["bullets"]
        and not draft["summary"]
        and not draft["added"]
        and tailored == master
    ):
        reasons = ", ".join(
            f"{reason}: {count}"
            for reason, count in sorted(Counter(rejected.values()).items())
        )
        raise RuntimeError(
            "OpenAI produced no evidence-safe suggestions. "
            f"Try a more specific instruction ({reasons or 'empty response'})."
        )
    return draft


# ── Application questions, cover letter, outreach ────────────────────────────

MAX_ANSWER_OUTPUT_TOKENS = 3000
DEFAULT_ANSWER_WORDS = 150


def find_questions(
    job: Job,
    *,
    api_key: str,
    model: str = OPENAI_MODEL_DEFAULT,
    timeout: int = 120,
    base_url: str = OPENAI_BASE_DEFAULT,
) -> list[dict[str, Any]]:
    """Pull the open-ended questions the application itself asks.

    Postings state these in the advert ("in your cover letter, tell us…",
    "applicants must submit a statement of…") far more often than the form
    reveals before you start filling it in.
    """
    system = (
        "You extract application questions from a job posting. Return JSON "
        "only, no markdown. List every open-ended question or written "
        "submission the applicant is asked for: essay prompts, statements of "
        "purpose, 'why this company', 'describe a project', and anything the "
        "advert says to address in a cover letter. Quote each in the "
        "posting's own words. Give word_limit when the posting states one, "
        "otherwise 0. If the posting asks for nothing written, return an "
        "empty list — do not invent questions.\n"
        'Return exactly: {"questions":[{"question":"...","word_limit":0}]}'
    )
    user = json.dumps(
        {
            "company": job.company,
            "role": job.role,
            "description": job.description[:MAX_DESCRIPTION_CHARS],
        },
        ensure_ascii=False,
    )
    found = _ask(
        system, user,
        api_key=api_key, model=model,
        max_tokens=MAX_STRATEGY_OUTPUT_TOKENS, timeout=timeout, base_url=base_url,
    )
    questions = []
    for index, item in enumerate(list(found.get("questions") or [])[:12]):
        if not isinstance(item, dict):
            continue
        text = re.sub(r"\s+", " ", str(item.get("question", ""))).strip()
        if not text:
            continue
        try:
            limit = max(0, min(2000, int(item.get("word_limit") or 0)))
        except (TypeError, ValueError):
            limit = 0
        questions.append({
            "id": f"q{index}",
            "question": text[:800],
            "answer": "",
            "word_limit": limit,
            "source": "posting",
        })
    return questions


def _evidence_pack(document: dict[str, Any], draft: dict[str, Any]) -> dict[str, Any]:
    """What the applicant can truthfully say, as this job's CV now reads."""
    patches = (draft or {}).get("bullets", {})

    def text_of(bullet: dict[str, Any]) -> str:
        patch = patches.get(bullet["id"], {})
        if isinstance(patch, dict) and patch.get("status") == "accepted":
            return str(patch.get("proposal", bullet["text"]))
        return bullet["text"]

    summary_patch = (draft or {}).get("summary")
    summary = document["summary"]
    if isinstance(summary_patch, dict) and summary_patch.get("status") == "accepted":
        summary = str(summary_patch.get("proposal", summary))
    return {
        "summary": summary,
        "sections": [
            {
                "section": section.get("name", ""),
                "entries": [
                    {
                        "title": entry.get("title", ""),
                        "context": entry.get("organization", ""),
                        "dates": entry.get("dates", ""),
                        "text": " ".join(text_of(bullet) for bullet in entry["bullets"]),
                    }
                    for entry in section["entries"]
                ],
            }
            for section in ordered_sections(document, draft)
        ],
    }


def write_answers(
    job: Job,
    document: dict[str, Any],
    draft: dict[str, Any],
    questions: list[dict[str, Any]],
    *,
    api_key: str,
    instructions: str = "",
    want_cover_letter: bool = True,
    want_outreach: bool = False,
    model: str = OPENAI_MODEL_DEFAULT,
    timeout: int = 180,
    base_url: str = OPENAI_BASE_DEFAULT,
) -> dict[str, Any]:
    """Draft answers, a cover letter, and an outreach note from the CV alone."""
    name = str(document.get("header", {}).get("name", "")).strip()
    wanted = [
        {
            "id": question["id"],
            "question": question["question"],
            "words": question.get("word_limit") or DEFAULT_ANSWER_WORDS,
        }
        for question in questions[:MAX_QUESTIONS]
    ]
    pieces = []
    if wanted:
        pieces.append("the listed questions")
    if want_cover_letter:
        pieces.append("a cover letter")
    if want_outreach:
        pieces.append("a short outreach note to a recruiter")
    if not pieces:
        return {"answers": [], "cover_letter": None, "outreach_email": None}

    system = (
        "You are drafting an application in the applicant's own voice. Return "
        "JSON only, no markdown. Write " + ", ".join(pieces) + ".\n"
        "Every specific claim must come from the supplied CV: a project, a "
        "result, a role, a course. Where the CV has nothing relevant, write "
        "about what the applicant wants to learn rather than inventing "
        "experience. Never state a degree, employer, technology, or metric "
        "the CV does not contain, and never claim years of experience.\n"
        "Write first person, plainly, without flattery of the company and "
        "without opening on 'I am excited to'. Name the specific work you are "
        "drawing on. Respect each question's word budget within 10 percent.\n"
        "Nothing you write may contain a placeholder in brackets such as "
        "[Recruiter's Name] or [Company]: the applicant sends this text as it "
        "stands, and a bracket left in it is the most visible mistake "
        "possible. Address anyone you cannot name by their role.\n"
        "The cover letter is at most 300 words, addressed to the hiring team, "
        "with no address block. The recruiter note is at most 120 words and "
        "opens with a Subject line.\n"
        'Return exactly: {"answers":[{"id":"q0","answer":"..."}],'
        '"cover_letter":"...","outreach_email":"..."}'
    )
    user = json.dumps(
        {
            "applicant_name": name,
            "target_job": {
                "company": job.company,
                "role": job.role,
                "location": job.location,
                "description": job.description[:MAX_DESCRIPTION_CHARS],
            },
            "cv": _evidence_pack(document, draft),
            "questions": wanted,
            "applicant_instructions": instructions[:2000],
        },
        ensure_ascii=False,
    )
    written = _ask(
        system, user,
        api_key=api_key, model=model,
        max_tokens=MAX_ANSWER_OUTPUT_TOKENS, timeout=timeout, base_url=base_url,
    )

    # The same evidence rules the CV rewrites obey, applied to prose the
    # applicant will sign their name to.
    evidence = " ".join([
        # The posting's own particulars are facts about the application, not
        # claims about the applicant: a cover letter has to name the company.
        job.company, job.role, job.location,
        document["summary"],
        *(str(skill) for skill in document.get("skills", [])),
        *(
            f"{entry.get('title', '')} {entry.get('organization', '')} "
            + " ".join(bullet["text"] for bullet in entry["bullets"])
            for section in document["sections"]
            for entry in section["entries"]
        ),
    ])
    flagged: list[str] = []

    def checked(text: str, label: str) -> str:
        value = str(text or "").strip()
        if not value:
            return ""
        for placeholder in re.findall(r"\[[^\]\n]{2,40}\]", value):
            flagged.append(f"{label} still contains the placeholder {placeholder}")
        for claim in _credential_claims(value) - _credential_claims(evidence):
            flagged.append(f"{label} claims '{claim}', which your CV does not")
        for token in _named_tokens(value) - _named_tokens(evidence):
            flagged.append(f"{label} names '{token}', which your CV does not")
        return value[:MAX_ANSWER_CHARS]

    answers = []
    by_id = {question["id"]: question for question in questions}
    for item in list(written.get("answers") or [])[:MAX_QUESTIONS]:
        if not isinstance(item, dict):
            continue
        identifier = str(item.get("id", "")).strip()
        if identifier not in by_id:
            continue
        answers.append({
            "id": identifier,
            "answer": checked(item.get("answer", ""), "An answer"),
        })
    letter = checked(written.get("cover_letter", ""), "The cover letter")
    outreach = checked(written.get("outreach_email", ""), "The outreach note")
    return {
        "answers": answers,
        "cover_letter": {"text": letter} if letter else None,
        "outreach_email": {"text": outreach} if outreach else None,
        # Surfaced rather than silently stripped: unlike a CV line, prose is
        # the applicant's own voice and they must decide what to cut.
        "unverified_claims": sorted(set(flagged))[:12],
    }
