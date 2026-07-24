from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
import re
from typing import Any

from .models import Job


MAX_BULLETS = 8
MAX_BULLETS_PER_ENTRY = 3
MAX_ENTRIES = 4
MAX_SKILLS = 12

STOP = {
    "a", "ability", "an", "and", "are", "as", "at", "be", "been", "being",
    "between", "by", "can", "candidate", "company", "could", "do", "does",
    "during", "each", "experience", "for", "from", "have", "in", "including",
    "intern", "internship", "into", "is", "it", "its", "job", "looking", "may",
    "more", "most", "not", "of", "on", "or", "other", "our", "preferred",
    "qualification", "requirements", "responsibilities", "role", "should",
    "skill", "skills", "such", "than", "that", "the", "their", "them", "they",
    "this", "through", "to", "using", "we", "who", "will", "with", "within",
    "work", "you", "your",
}

PHRASES = {
    "artificial intelligence": "ai",
    "computer vision": "computer-vision",
    "deep learning": "deep-learning",
    "full stack": "full-stack",
    "machine learning": "machine-learning",
    "natural language processing": "nlp",
    "reinforcement learning": "reinforcement-learning",
    "robot operating system": "ros",
    "software developer": "software-engineering",
    "software engineering": "software-engineering",
}

ALIASES = {
    "ai": "ai",
    "artificial-intelligence": "ai",
    "cv": "computer-vision",
    "developer": "software-engineering",
    "developers": "software-engineering",
    "engineer": "engineering",
    "engineers": "engineering",
    "ml": "machine-learning",
    "nlp": "nlp",
    "robot": "robotics",
    "robotic": "robotics",
    "robots": "robotics",
    "ros2": "ros",
    "swe": "software-engineering",
}


def _word(value: str) -> str:
    value = value.lower().strip(".")
    if value in ALIASES:
        return ALIASES[value]
    if len(value) > 4 and value.endswith("ies"):
        value = value[:-3] + "y"
    elif len(value) > 4 and value.endswith("s") and not value.endswith("ss"):
        value = value[:-1]
    return ALIASES.get(value, value)


def concepts(value: str) -> set[str]:
    """Return deterministic, normalized concepts used only for ranking."""
    lowered = re.sub(r"[/_]", " ", (value or "").lower())
    found = {
        _word(token)
        for token in re.findall(r"[a-z][a-z0-9+#.-]{1,}", lowered)
        if _word(token) not in STOP
    }
    for phrase, canonical in PHRASES.items():
        if re.search(r"(?<![a-z])" + re.escape(phrase) + r"(?![a-z])", lowered):
            for component in phrase.split():
                found.discard(_word(component))
            found.add(canonical)
    return found


def tokens(value: str) -> set[str]:
    """Backwards-compatible public alias for the ranking vocabulary."""
    return concepts(value)


@dataclass(frozen=True)
class EvidenceLink:
    fact_id: str
    source_path: str
    source_ref: str
    text: str
    score: int
    selection_rank: int
    matched_title_terms: tuple[str, ...]
    matched_description_terms: tuple[str, ...]
    matched_tags: tuple[str, ...]


@dataclass
class TailoredResume:
    header: dict[str, Any]
    summary: str
    skills: list[str]
    education: list[dict[str, Any]]
    sections: list[dict[str, Any]]
    selected_fact_ids: list[str]
    evidence_links: list[EvidenceLink] = field(default_factory=list)
    selection_audit: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class _Candidate:
    fact_id: str
    text: str
    score: int
    section_index: int
    entry_index: int
    bullet_index: int
    source_path: str
    source_ref: str
    matched_title_terms: tuple[str, ...]
    matched_description_terms: tuple[str, ...]
    matched_tags: tuple[str, ...]

    @property
    def entry_key(self) -> tuple[int, int]:
        return self.section_index, self.entry_index


def _score_candidate(
    *,
    text: str,
    tags: list[Any],
    context: str,
    title_terms: set[str],
    description_terms: set[str],
    target_text: str,
    source_ref: str,
) -> tuple[int, tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    text_terms = concepts(text)
    context_terms = concepts(context)
    tag_terms: set[str] = set()
    matched_tag_phrases: set[str] = set()
    normalized_target = target_text.lower()
    for tag in tags:
        raw = str(tag).strip()
        if not raw:
            continue
        tag_terms.update(concepts(raw))
        if re.search(r"(?<![a-z])" + re.escape(raw.lower()) + r"(?![a-z])", normalized_target):
            matched_tag_phrases.add(raw.lower())

    title_matches = text_terms & title_terms
    description_matches = text_terms & description_terms
    tag_title_matches = tag_terms & title_terms
    tag_description_matches = tag_terms & description_terms
    context_title_matches = context_terms & title_terms
    context_description_matches = context_terms & description_terms

    direct_score = (
        7 * len(tag_title_matches)
        + 5 * len(title_matches)
        + 4 * len(matched_tag_phrases)
        + 3 * len(tag_description_matches)
        + 2 * len(description_matches)
    )
    score = direct_score
    if direct_score:
        score += (
            2 * len(context_title_matches)
            + len(context_description_matches)
        )
    if score and re.search(r"\b\d+(?:[.,]\d+)?%?\b", text):
        score += 1
    if score and source_ref:
        score += 1
    return (
        score,
        tuple(sorted(title_matches | tag_title_matches)),
        tuple(sorted(description_matches | tag_description_matches)),
        tuple(sorted(matched_tag_phrases | tag_title_matches | tag_description_matches)),
    )


def _rank_skills(
    skills: list[Any],
    title_terms: set[str],
    description_terms: set[str],
    maximum: int,
) -> list[str]:
    ranked: list[tuple[int, int, str]] = []
    seen: set[str] = set()
    for index, skill in enumerate(skills):
        text = str(skill).strip()
        canonical = text.casefold()
        if not text or canonical in seen:
            continue
        seen.add(canonical)
        terms = concepts(text)
        score = 5 * len(terms & title_terms) + 2 * len(terms & description_terms)
        if score:
            ranked.append((-score, index, text))
    ranked.sort()
    return [text for _score, _index, text in ranked[:maximum]]


def tailor_resume(
    job: Job,
    profile: dict[str, Any],
    facts: dict[str, Any],
    *,
    max_bullets: int = MAX_BULLETS,
    max_bullets_per_entry: int = MAX_BULLETS_PER_ENTRY,
    max_entries: int = MAX_ENTRIES,
    max_skills: int = MAX_SKILLS,
) -> TailoredResume:
    """Select concise, relevant, verbatim facts with a deterministic audit trail."""
    if min(max_bullets, max_bullets_per_entry, max_entries, max_skills) < 0:
        raise ValueError("Tailoring limits cannot be negative")

    title_terms = concepts(job.role)
    description_terms = concepts(job.description)
    target_text = f"{job.role} {job.description}"
    candidates: list[_Candidate] = []
    known_ids: dict[str, str] = {}
    missing_id_count = 0

    sections = facts.get("sections", [])
    for section_index, section in enumerate(sections):
        for entry_index, entry in enumerate(section.get("entries", [])):
            context = " ".join(
                str(entry.get(key, ""))
                for key in ("title", "organization")
                if entry.get(key)
            )
            for bullet_index, bullet in enumerate(entry.get("bullets", [])):
                fact_id = str(bullet.get("id", "")).strip()
                text = str(bullet.get("text", "")).strip()
                if not fact_id or not text:
                    missing_id_count += 1
                    continue
                previous = known_ids.get(fact_id)
                if previous is not None:
                    if previous != text:
                        raise ValueError(f"Evidence id {fact_id!r} maps to conflicting facts")
                    continue
                known_ids[fact_id] = text
                source_ref = str(
                    bullet.get("evidence")
                    or bullet.get("source")
                    or bullet.get("url")
                    or ""
                ).strip()
                raw_tags = bullet.get("tags", [])
                tags = [raw_tags] if isinstance(raw_tags, str) else list(raw_tags or [])
                score, title_hits, description_hits, tag_hits = _score_candidate(
                    text=text,
                    tags=tags,
                    context=context,
                    title_terms=title_terms,
                    description_terms=description_terms,
                    target_text=target_text,
                    source_ref=source_ref,
                )
                section_name = str(section.get("name", "")).strip().casefold()
                if score:
                    # Prefer evidence from work/projects when relevance is
                    # otherwise similar. Awards can support a CV, but should not
                    # crowd out technical evidence merely because a posting uses
                    # generic words such as "communication" or "English".
                    score = max(
                        0,
                        score
                        + {"experience": 3, "projects": 2, "awards": -8}.get(
                            section_name, 0
                        ),
                    )
                candidates.append(
                    _Candidate(
                        fact_id=fact_id,
                        text=text,
                        score=score,
                        section_index=section_index,
                        entry_index=entry_index,
                        bullet_index=bullet_index,
                        source_path=(
                            f"sections[{section_index}].entries[{entry_index}]"
                            f".bullets[{bullet_index}]"
                        ),
                        source_ref=source_ref,
                        matched_title_terms=title_hits,
                        matched_description_terms=description_hits,
                        matched_tags=tag_hits,
                    )
                )

    ranked = sorted(
        (candidate for candidate in candidates if candidate.score > 0),
        key=lambda item: (
            -item.score,
            item.section_index,
            item.entry_index,
            item.bullet_index,
            item.fact_id,
        ),
    )
    selected: list[_Candidate] = []
    entry_counts: Counter[tuple[int, int]] = Counter()
    selected_entries: set[tuple[int, int]] = set()
    for candidate in ranked:
        if len(selected) >= max_bullets:
            break
        section_name = str(
            sections[candidate.section_index].get("name", "")
        ).strip().casefold()
        per_entry_limit = 1 if section_name == "awards" else max_bullets_per_entry
        if entry_counts[candidate.entry_key] >= per_entry_limit:
            continue
        if candidate.entry_key not in selected_entries and len(selected_entries) >= max_entries:
            continue
        selected.append(candidate)
        selected_entries.add(candidate.entry_key)
        entry_counts[candidate.entry_key] += 1

    selection_rank = {candidate.fact_id: index + 1 for index, candidate in enumerate(selected)}
    by_entry: dict[tuple[int, int], list[_Candidate]] = defaultdict(list)
    for candidate in selected:
        by_entry[candidate.entry_key].append(candidate)
    for values in by_entry.values():
        values.sort(key=lambda item: selection_rank[item.fact_id])

    ordered_entries = sorted(
        by_entry,
        key=lambda key: min(selection_rank[item.fact_id] for item in by_entry[key]),
    )
    section_order: list[int] = []
    entries_by_section: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for section_index, entry_index in ordered_entries:
        if section_index not in section_order:
            section_order.append(section_index)
        source_entry = sections[section_index]["entries"][entry_index]
        copied = {key: value for key, value in source_entry.items() if key != "bullets"}
        copied["bullets"] = [candidate.text for candidate in by_entry[(section_index, entry_index)]]
        copied["evidence_ids"] = [
            candidate.fact_id for candidate in by_entry[(section_index, entry_index)]
        ]
        entries_by_section[section_index].append(copied)
    tailored_sections = [
        {
            "name": sections[index].get("name", ""),
            "entries": entries_by_section[index],
        }
        for index in section_order
    ]

    evidence_links = [
        EvidenceLink(
            fact_id=candidate.fact_id,
            source_path=candidate.source_path,
            source_ref=candidate.source_ref,
            text=candidate.text,
            score=candidate.score,
            selection_rank=selection_rank[candidate.fact_id],
            matched_title_terms=candidate.matched_title_terms,
            matched_description_terms=candidate.matched_description_terms,
            matched_tags=candidate.matched_tags,
        )
        for candidate in selected
    ]
    identity = profile.get("identity", {})
    contact = profile.get("contact", {})
    return TailoredResume(
        header={
            "name": f"{identity.get('first_name', '')} {identity.get('last_name', '')}".strip(),
            "email": contact.get("email", ""),
            "phone": contact.get("phone", ""),
            "location": contact.get("location", ""),
            "links": [
                contact.get("linkedin", ""),
                contact.get("github", ""),
                contact.get("website", ""),
            ],
        },
        summary=str(facts.get("summary", "")).strip(),
        skills=_rank_skills(
            list(facts.get("skills", [])), title_terms, description_terms, max_skills
        ),
        education=[dict(item) for item in facts.get("education", [])],
        sections=tailored_sections,
        selected_fact_ids=[candidate.fact_id for candidate in selected],
        evidence_links=evidence_links,
        selection_audit={
            "algorithm": "verified-concept-ranker-v2",
            "title_terms": sorted(title_terms),
            "description_terms": sorted(description_terms),
            "considered_fact_count": len(candidates),
            "relevant_fact_count": len(ranked),
            "selected_fact_count": len(selected),
            "excluded_missing_id_or_text_count": missing_id_count,
            "limits": {
                "max_bullets": max_bullets,
                "max_bullets_per_entry": max_bullets_per_entry,
                "max_entries": max_entries,
                "max_skills": max_skills,
            },
        },
    )
