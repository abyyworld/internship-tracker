from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from html import escape
import json
from pathlib import Path

from .tailoring import TailoredResume


def file_sha256(path: Path) -> str:
    value = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            value.update(chunk)
    return value.hexdigest()


def render_resume(resume: TailoredResume, destination: Path) -> str:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer
    except ImportError as exc:
        raise RuntimeError("ReportLab is required: pip install reportlab") from exc

    destination.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    normal = ParagraphStyle(
        "ResumeBody", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=9, leading=11, spaceAfter=2,
    )
    header = ParagraphStyle(
        "ResumeHeader", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=17, leading=20, alignment=TA_CENTER, spaceAfter=2,
    )
    contact = ParagraphStyle(
        "ResumeContact", parent=normal, alignment=TA_CENTER, fontSize=8.5, leading=10,
    )
    section = ParagraphStyle(
        "ResumeSection", parent=normal, fontName="Helvetica-Bold", fontSize=10,
        leading=12, textColor=colors.HexColor("#1f2937"), spaceBefore=5, spaceAfter=2,
        borderWidth=0, borderPadding=0,
    )
    entry_title = ParagraphStyle(
        "ResumeEntry", parent=normal, fontName="Helvetica-Bold", fontSize=9.2,
    )
    bullet = ParagraphStyle(
        "ResumeBullet", parent=normal, leftIndent=10, firstLineIndent=-7, bulletIndent=0,
    )
    doc = SimpleDocTemplate(
        str(destination), pagesize=A4, rightMargin=15 * mm, leftMargin=15 * mm,
        topMargin=12 * mm, bottomMargin=12 * mm,
        title=f"{resume.header.get('name', '')} Resume",
    )
    story = [Paragraph(escape(resume.header.get("name", "")), header)]
    contact_parts = [
        resume.header.get("email", ""),
        resume.header.get("phone", ""),
        resume.header.get("location", ""),
        *resume.header.get("links", []),
    ]
    story.append(
        Paragraph(" &nbsp; | &nbsp; ".join(escape(x) for x in contact_parts if x), contact)
    )
    if resume.summary:
        story.extend(
            [Paragraph("SUMMARY", section), Paragraph(escape(resume.summary), normal)]
        )
    if resume.skills:
        story.extend(
            [
                Paragraph("SKILLS", section),
                Paragraph(escape(" • ".join(resume.skills)), normal),
            ]
        )
    if resume.education:
        story.append(Paragraph("EDUCATION", section))
        for item in resume.education:
            title = " | ".join(
                str(item.get(key, "")) for key in ("institution", "degree") if item.get(key)
            )
            details = " | ".join(
                str(item.get(key, "")) for key in ("location", "dates") if item.get(key)
            )
            story.append(KeepTogether([
                Paragraph(escape(title), entry_title),
                Paragraph(escape(details), normal) if details else Spacer(1, 0),
            ]))
    for resume_section in resume.sections:
        story.append(Paragraph(escape(str(resume_section.get("name", "")).upper()), section))
        for item in resume_section.get("entries", []):
            title = " | ".join(
                str(item.get(key, "")) for key in ("title", "organization") if item.get(key)
            )
            meta = " | ".join(
                str(item.get(key, "")) for key in ("location", "dates") if item.get(key)
            )
            block = [Paragraph(escape(title), entry_title)]
            if meta:
                block.append(Paragraph(escape(meta), normal))
            for text in item.get("bullets", []):
                block.append(Paragraph(f"• {escape(str(text))}", bullet))
            story.append(KeepTogether(block))
    def invariant_canvas(*args, **kwargs):
        kwargs["invariant"] = 1
        return Canvas(*args, **kwargs)

    doc.build(story, canvasmaker=invariant_canvas)
    if not destination.exists() or destination.stat().st_size == 0:
        raise RuntimeError("Resume renderer produced an empty file")
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
