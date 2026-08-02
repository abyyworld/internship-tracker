from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

from .cv_render import render_pdf
from .tailoring import TailoredResume


def file_sha256(path: Path) -> str:
    value = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            value.update(chunk)
    return value.hexdigest()


def render_resume(
    resume: TailoredResume,
    destination: Path,
    *,
    title: str = "",
) -> str:
    """Write the CV and its evidence file, and return the PDF hash.

    The PDF is laid out by :mod:`autoapply.cv_render`, which reproduces the
    master CV's design, so a tailored export looks like the original document
    rather than a generic resume template.
    """
    render_pdf(resume, destination, title=title)
    destination.chmod(0o600)
    pdf_hash = file_sha256(destination)
    evidence_path = destination.with_name(destination.stem + ".evidence.json")
    evidence_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "resume_pdf": destination.name,
                "resume_sha256": pdf_hash,
                "selected_fact_ids": resume.selected_fact_ids,
                "evidence_links": [asdict(link) for link in resume.evidence_links],
                "rendered_sections": resume.sections,
                "rendered_summary": resume.summary,
                "selection_audit": resume.selection_audit,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    evidence_path.chmod(0o600)
    return pdf_hash

