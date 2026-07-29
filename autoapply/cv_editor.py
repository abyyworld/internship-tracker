from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
from typing import Any

from .tailoring import TailoredResume


SCHEMA_VERSION = 1
MAX_INSTRUCTION_CHARS = 4000
MAX_PROPOSAL_CHARS = 600


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _safe_job_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(".-")
    return cleaned[:160] or "job"


def draft_path(home: Path, job_id: str) -> Path:
    return home / "editor-drafts" / f"{_safe_job_id(job_id)}.json"


def _private_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.parent.chmod(0o700)
    if path.exists() and path.is_symlink():
        raise RuntimeError("Refusing a symbolic-link CV draft")
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(temporary, flags, 0o600)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = -1
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    os.replace(temporary, path)
    path.chmod(0o600)


def _academic_as_sections(
    academic: dict[str, Any],
    seen: set[str],
) -> list[dict[str, Any]]:
    """Convert academic_profile.yaml into supplementary CV sections."""
    extra: list[dict[str, Any]] = []

    def _bullet_id(prefix: str, idx: int) -> str:
        raw = f"academic_{prefix}_{idx}"
        if raw in seen:
            raw = f"{raw}_x{len(seen)}"
        seen.add(raw)
        return raw

    # Publications
    pubs = [p for p in (academic.get("publications") or []) if isinstance(p, dict) and p.get("title")]
    if pubs:
        sec: dict[str, Any] = {"name": "Publications", "entries": []}
        for i, p in enumerate(pubs):
            venue = str(p.get("venue", "")).strip()
            year = str(p.get("year", "")).strip()
            authors = str(p.get("authors", "")).strip()
            contribution = str(p.get("contribution", "")).strip()
            label = f"{venue} {year}".strip() or "Publication"
            text = contribution or f"{str(p['title']).strip()}. {venue} {year}".strip()
            bid = _bullet_id("pub", i)
            entry: dict[str, Any] = {
                "title": str(p["title"]).strip(),
                "organization": venue,
                "dates": year,
                "bullets": [{"id": bid, "text": text or str(p["title"])}],
            }
            if authors:
                entry["authors"] = authors
            url = str(p.get("url") or p.get("arxiv") or "").strip()
            if url:
                entry["url"] = url
            sec["entries"].append(entry)
        extra.append(sec)

    # Awards & honours
    awards = [a for a in (academic.get("awards") or []) if isinstance(a, dict) and a.get("name")]
    if awards:
        sec = {"name": "Awards & Honours", "entries": []}
        for i, a in enumerate(awards):
            desc = str(a.get("description", "")).strip()
            text = desc or f"{str(a['name']).strip()} — {str(a.get('institution', '')).strip()}".strip(" —")
            bid = _bullet_id("award", i)
            sec["entries"].append({
                "title": str(a["name"]).strip(),
                "organization": str(a.get("institution", "")).strip(),
                "dates": str(a.get("year", "")).strip(),
                "bullets": [{"id": bid, "text": text}],
            })
        extra.append(sec)

    # Grants
    grants = [g for g in (academic.get("grants") or []) if isinstance(g, dict) and g.get("name")]
    if grants:
        sec = {"name": "Grants & Funding", "entries": []}
        for i, g in enumerate(grants):
            desc = str(g.get("description", "")).strip()
            amount = str(g.get("amount", "")).strip()
            text = desc or (f"{str(g['name']).strip()}" + (f" ({amount})" if amount else ""))
            bid = _bullet_id("grant", i)
            sec["entries"].append({
                "title": str(g["name"]).strip(),
                "organization": str(g.get("funder", "")).strip(),
                "dates": str(g.get("year", "")).strip(),
                "bullets": [{"id": bid, "text": text}],
            })
        extra.append(sec)

    # Talks
    talks = [t for t in (academic.get("talks") or []) if isinstance(t, dict) and t.get("title")]
    if talks:
        sec = {"name": "Talks & Presentations", "entries": []}
        for i, t in enumerate(talks):
            ttype = str(t.get("type", "")).title()
            venue = str(t.get("venue", "")).strip()
            text = f"{ttype} presentation at {venue}".strip() if venue else str(t["title"]).strip()
            bid = _bullet_id("talk", i)
            sec["entries"].append({
                "title": str(t["title"]).strip(),
                "organization": venue,
                "dates": str(t.get("date", "")).strip(),
                "bullets": [{"id": bid, "text": text}],
            })
        extra.append(sec)

    # Teaching
    teaching = [t for t in (academic.get("teaching") or []) if isinstance(t, dict) and t.get("role")]
    if teaching:
        sec = {"name": "Teaching", "entries": []}
        for i, t in enumerate(teaching):
            desc = str(t.get("description", "")).strip()
            course = str(t.get("course", "")).strip()
            text = desc or f"{str(t['role']).strip()}: {course}".strip(": ")
            bid = _bullet_id("teach", i)
            sec["entries"].append({
                "title": str(t["role"]).strip(),
                "organization": str(t.get("institution", "")).strip() + (f" — {course}" if course else ""),
                "dates": str(t.get("term", "")).strip(),
                "bullets": [{"id": bid, "text": text}],
            })
        extra.append(sec)

    return extra


def master_document(
    profile: dict[str, Any],
    facts: dict[str, Any],
    academic: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the complete fact bank in a stable, editor-friendly structure.

    If an academic_profile dict is supplied, publications, awards, grants,
    talks, and teaching sections are appended as additional CV sections.
    """
    identity = profile.get("identity", {})
    contact = profile.get("contact", {})
    seen: set[str] = set()
    sections: list[dict[str, Any]] = []
    for section in facts.get("sections", []):
        copied_section = {
            "name": str(section.get("name", "")).strip(),
            "entries": [],
        }
        for entry in section.get("entries", []):
            copied_entry = {
                key: deepcopy(value)
                for key, value in entry.items()
                if key != "bullets"
            }
            copied_entry["bullets"] = []
            for bullet in entry.get("bullets", []):
                fact_id = str(bullet.get("id", "")).strip()
                text = str(bullet.get("text", "")).strip()
                if not fact_id or not text:
                    raise ValueError("Every master CV bullet needs a non-empty id and text")
                if fact_id in seen:
                    raise ValueError(f"Duplicate master CV fact id: {fact_id}")
                seen.add(fact_id)
                copied_entry["bullets"].append({"id": fact_id, "text": text})
            copied_section["entries"].append(copied_entry)
        sections.append(copied_section)

    # Academic supplement
    if academic and isinstance(academic, dict):
        for sec in _academic_as_sections(academic, seen):
            sections.append(sec)

    # Research skills supplement
    research_skills = []
    if academic and isinstance(academic, dict):
        research_skills = [
            str(s).strip()
            for s in (academic.get("research_skills") or [])
            if str(s).strip()
        ]

    # Research statement for summary supplement
    research_statement = ""
    if academic and isinstance(academic, dict):
        rs = (academic.get("research") or {}).get("statement", "")
        if rs and rs != "REPLACE_ME":
            research_statement = str(rs).strip()

    # Supervisor info for rich header
    supervisors = []
    if academic and isinstance(academic, dict):
        for sup in (academic.get("supervisors") or []):
            if isinstance(sup, dict) and sup.get("name") and sup.get("name") != "REPLACE_ME":
                supervisors.append({
                    "name": str(sup.get("name", "")).strip(),
                    "title": str(sup.get("title", "")).strip(),
                    "institution": str(sup.get("institution", "")).strip(),
                    "lab": str(sup.get("lab", "")).strip(),
                    "relationship": str(sup.get("relationship", "")).strip(),
                })

    return {
        "schema_version": SCHEMA_VERSION,
        "header": {
            "name": (
                f"{identity.get('first_name', '')} "
                f"{identity.get('last_name', '')}"
            ).strip(),
            "email": str(contact.get("email", "")).strip(),
            "phone": str(contact.get("phone", "")).strip(),
            "location": str(contact.get("location", "")).strip(),
            "links": [
                str(value).strip()
                for value in (
                    contact.get("linkedin", ""),
                    contact.get("github", ""),
                    contact.get("website", ""),
                )
                if str(value).strip()
            ],
            "supervisors": supervisors,
        },
        "summary": str(facts.get("summary", "")).strip(),
        "research_statement": research_statement,
        "skills": [
            str(value).strip()
            for value in facts.get("skills", [])
            if str(value).strip()
        ] + research_skills,
        "education": deepcopy(list(facts.get("education", []))),
        "sections": sections,
        "fact_ids": sorted(seen),
        "has_academic": bool(academic),
    }


def empty_draft(job_id: str, description_hash: str = "") -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "job_id": job_id,
        "description_hash": description_hash,
        "provider": "openai",
        "model": "gpt-4o-mini",
        "instructions": "",
        "summary": None,
        "bullets": {},
        "advice": [],
        "rejected_by_validator": {},
        "updated_at": _now_iso(),
    }


def load_draft(home: Path, job_id: str) -> dict[str, Any]:
    path = draft_path(home, job_id)
    if not path.exists():
        return empty_draft(job_id)
    if path.is_symlink() or path.stat().st_mode & 0o077:
        raise RuntimeError("CV draft must be a private regular file with mode 0600")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(f"Cannot read CV draft: {exc}") from exc
    if not isinstance(value, dict) or value.get("job_id") != job_id:
        raise RuntimeError("Stored CV draft is invalid")
    return value


def _clean_patch(
    value: Any,
    *,
    original: str,
    expected_id: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Each CV suggestion must be an object")
    if str(value.get("id", expected_id)) != expected_id:
        raise ValueError("CV suggestion id does not match its fact id")
    proposal = re.sub(r"\s+", " ", str(value.get("proposal", ""))).strip()
    if not proposal or len(proposal) > MAX_PROPOSAL_CHARS:
        raise ValueError("A CV proposal is empty or too long")
    status = str(value.get("status", "pending"))
    if status not in {"pending", "accepted", "rejected"}:
        raise ValueError("CV suggestion status is invalid")
    return {
        "id": expected_id,
        "original": original,
        "proposal": proposal,
        "rationale": re.sub(
            r"\s+", " ", str(value.get("rationale", ""))
        ).strip()[:800],
        "keywords": [
            re.sub(r"\s+", " ", str(item)).strip()[:80]
            for item in list(value.get("keywords", []))[:12]
            if str(item).strip()
        ],
        "status": status,
    }


def normalize_draft(
    document: dict[str, Any],
    job_id: str,
    incoming: dict[str, Any],
    *,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate browser/provider draft data and bind it to immutable originals."""
    originals = {
        bullet["id"]: bullet["text"]
        for section in document["sections"]
        for entry in section["entries"]
        for bullet in entry["bullets"]
    }
    result = empty_draft(job_id, str(incoming.get("description_hash", "")))
    if existing:
        for key in (
            "description_hash",
            "provider",
            "model",
            "advice",
            "rejected_by_validator",
        ):
            result[key] = deepcopy(existing.get(key, result.get(key)))
    result["instructions"] = str(incoming.get("instructions", ""))[
        :MAX_INSTRUCTION_CHARS
    ]

    raw_summary = incoming.get("summary")
    if raw_summary:
        result["summary"] = _clean_patch(
            raw_summary,
            original=document["summary"],
            expected_id="summary",
        )

    raw_bullets = incoming.get("bullets", {})
    if not isinstance(raw_bullets, dict):
        raise ValueError("CV bullet suggestions must be an object")
    if set(map(str, raw_bullets)) - set(originals):
        raise ValueError("CV draft references an unknown fact id")
    result["bullets"] = {
        fact_id: _clean_patch(
            patch,
            original=originals[fact_id],
            expected_id=fact_id,
        )
        for fact_id, patch in raw_bullets.items()
    }
    result["updated_at"] = _now_iso()
    return result


def save_draft(
    home: Path,
    document: dict[str, Any],
    job_id: str,
    incoming: dict[str, Any],
    *,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    value = normalize_draft(
        document,
        job_id,
        incoming,
        existing=existing,
    )
    _private_write_json(draft_path(home, job_id), value)
    return value


def resume_from_document(
    document: dict[str, Any],
    draft: dict[str, Any] | None = None,
) -> TailoredResume:
    """Apply accepted patches while retaining every master CV line."""
    draft = draft or {}
    summary = document["summary"]
    summary_patch = draft.get("summary")
    if (
        isinstance(summary_patch, dict)
        and summary_patch.get("status") == "accepted"
    ):
        summary = str(summary_patch.get("proposal", summary))

    bullet_patches = draft.get("bullets", {})
    sections: list[dict[str, Any]] = []
    all_ids: list[str] = []
    accepted_ids: list[str] = []
    for section in document["sections"]:
        copied_section = {"name": section["name"], "entries": []}
        for entry in section["entries"]:
            copied_entry = {
                key: deepcopy(value)
                for key, value in entry.items()
                if key != "bullets"
            }
            copied_entry["bullets"] = []
            copied_entry["evidence_ids"] = []
            for bullet in entry["bullets"]:
                fact_id = bullet["id"]
                text = bullet["text"]
                patch = bullet_patches.get(fact_id, {})
                if isinstance(patch, dict) and patch.get("status") == "accepted":
                    text = str(patch.get("proposal", text))
                    accepted_ids.append(fact_id)
                copied_entry["bullets"].append(text)
                copied_entry["evidence_ids"].append(fact_id)
                all_ids.append(fact_id)
            copied_section["entries"].append(copied_entry)
        sections.append(copied_section)
    return TailoredResume(
        header=deepcopy(document["header"]),
        summary=summary,
        skills=deepcopy(document["skills"]),
        education=deepcopy(document["education"]),
        sections=sections,
        selected_fact_ids=all_ids,
        selection_audit={
            "algorithm": "non-destructive-cv-editor-v1",
            "master_fact_count": len(all_ids),
            "accepted_patch_ids": accepted_ids,
            "summary_patch_accepted": summary != document["summary"],
            "untouched_content_preserved": True,
            "review_required": True,
        },
    )
