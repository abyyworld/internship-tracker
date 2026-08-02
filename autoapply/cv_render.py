"""Render a CV to PDF in the exact design of the master document.

The layout constants below are the design spec of ``my cv and the tool/build_cv.py``:
A4, 15 mm left/right margins, Times body, letterspaced Helvetica-Bold section
heads, accent #14324F, #9DB2C2 rules, right-aligned Helvetica-Bold dates. That
file renders one hard-coded CV; this module renders any fact bank through the
same spec, so a tailored export is visually indistinguishable from the original.

Content longer than a page flows onto further pages automatically — the frame is
a single full-height column and ReportLab paginates it.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any


A4_WIDTH = 595.2755905511812
A4_HEIGHT = 841.8897637795277

L_MARGIN = 42.52
TOP_MARGIN = 36.0
BOTTOM_MARGIN = 40.0
CONTENT_W = A4_WIDTH - 2 * L_MARGIN
DATE_COLUMN_W = 150.0
SKILL_LABEL_W = 86.8

INK = "#111111"
ACCENT = "#14324F"
DATE_CLR = "#2B3A47"
SUB_CLR = "#3D4A56"
META_CLR = "#6B6B6B"
RULE_CLR = "#9DB2C2"
HAIR_CLR = "#D8E0E6"

# Layouts a section may declare in resume_facts.yaml.
LAYOUT_ENTRIES = "entries"
LAYOUT_NOTES = "notes"
LAYOUT_SKILLS = "skills"


def track(value: str, gap: str = " ", wordgap: int = 4) -> str:
    """Letterspace a string for a section head.

    Word gaps use ``&nbsp;`` because ReportLab collapses runs of ordinary
    spaces inside a Paragraph.
    """
    separator = "\x00"
    spaced = separator.join(gap.join(word) for word in str(value).split(" "))
    return spaced.replace("&", "&amp;").replace(separator, "&nbsp;" * wordgap)


def _link(url: str, text: str) -> str:
    return f'<link href="{escape(url, quote=True)}" color="{ACCENT}"><b>{escape(text)}</b></link>'


def _entry_links(entry: dict[str, Any]) -> str:
    """Trailing links for an entry, in the order the master CV prints them."""
    parts: list[str] = []
    extra_url = str(entry.get("link_extra_url", "")).strip()
    if extra_url:
        parts.append(_link(extra_url, str(entry.get("link_extra_text", "")).strip() or "Link"))
    url = str(entry.get("url", "")).strip()
    if url:
        parts.append(_link(url, str(entry.get("link_text", "")).strip() or "GitHub"))
    if not parts:
        return ""
    prefix = str(entry.get("link_prefix", "")).strip()
    if prefix:
        return f" {escape(prefix)} " + " · ".join(parts) + "."
    return " " + " · ".join(parts)


def _bullet_html(bullets: Any) -> str:
    """Join an entry's bullets into one printed paragraph.

    A bullet marked ``lead`` prints bold and runs straight into the body that
    follows it, which is how every entry in the master CV opens. Plain strings
    are accepted so the automatic tailoring path, which flattens bullets before
    it gets here, still renders.
    """
    pieces: list[str] = []
    for bullet in bullets or []:
        if isinstance(bullet, str):
            text, style = escape(bullet.strip()), ""
        else:
            text = escape(str(bullet.get("text", "")).strip())
            style = str(bullet.get("style", ""))
        if not text:
            continue
        pieces.append(f"<b>{text}</b>" if style == "lead" else text)
    return " ".join(pieces)


def _styles():
    from reportlab.lib.colors import HexColor
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.styles import ParagraphStyle

    def style(name: str, **kwargs: Any) -> ParagraphStyle:
        return ParagraphStyle(name, **kwargs)

    return {
        "name": style(
            "name", fontName="Times-Bold", fontSize=24, leading=27,
            alignment=TA_CENTER, textColor=HexColor(INK),
        ),
        "tagline": style(
            "tagline", fontName="Times-Italic", fontSize=11.5, leading=14,
            alignment=TA_CENTER, textColor=HexColor(ACCENT), spaceBefore=6,
        ),
        "contact": style(
            "contact", fontName="Helvetica", fontSize=8.3, leading=11,
            alignment=TA_CENTER, textColor=HexColor(META_CLR), spaceBefore=5,
        ),
        "summary": style(
            "summary", fontName="Times-Roman", fontSize=10, leading=13.2,
            alignment=TA_CENTER, textColor=HexColor(INK),
        ),
        "section": style(
            "section", fontName="Helvetica-Bold", fontSize=10, leading=12,
            alignment=TA_LEFT, textColor=HexColor(ACCENT),
        ),
        "title": style(
            "title", fontName="Times-Bold", fontSize=10.8, leading=13,
            alignment=TA_LEFT, textColor=HexColor(INK),
        ),
        "date": style(
            "date", fontName="Helvetica-Bold", fontSize=8.4, leading=13,
            alignment=TA_RIGHT, textColor=HexColor(DATE_CLR),
        ),
        "sub": style(
            "sub", fontName="Times-Italic", fontSize=9.8, leading=13.5,
            alignment=TA_LEFT, textColor=HexColor(SUB_CLR), spaceBefore=1,
        ),
        "body": style(
            "body", fontName="Times-Roman", fontSize=9.7, leading=12.1,
            alignment=TA_LEFT, textColor=HexColor(INK), spaceBefore=2.5,
        ),
        "skilllabel": style(
            "skilllabel", fontName="Helvetica-Bold", fontSize=8.4, leading=12,
            alignment=TA_LEFT, textColor=HexColor(ACCENT),
        ),
        "skillval": style(
            "skillval", fontName="Times-Roman", fontSize=9.6, leading=12,
            alignment=TA_LEFT, textColor=HexColor(INK),
        ),
    }


def build_story(resume: Any, styles: dict[str, Any]) -> list[Any]:
    """Compose the flowables for one CV.

    ``resume`` is anything exposing ``header``, ``summary``, and ``sections``
    with the master-document shape.
    """
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (
        HRFlowable, KeepTogether, Paragraph, Spacer, Table, TableStyle,
    )

    def section_head(label: str) -> Any:
        return KeepTogether([
            Spacer(1, 13),
            Paragraph(track(label.upper()), styles["section"]),
            HRFlowable(
                width="100%", thickness=1.0, color=HexColor(RULE_CLR),
                spaceBefore=5, spaceAfter=7,
            ),
        ])

    def entry_block(title: str, dates: str, sub: str, body: str) -> list[Any]:
        if dates:
            head: Any = Table(
                [[Paragraph(title, styles["title"]), Paragraph(dates, styles["date"])]],
                colWidths=[CONTENT_W - DATE_COLUMN_W, DATE_COLUMN_W],
            )
            head.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))
        else:
            head = Paragraph(title, styles["title"])
        block: list[Any] = [head]
        if sub:
            block.append(Paragraph(sub, styles["sub"]))
        out: list[Any] = [KeepTogether(block)]
        if body:
            out.append(Paragraph(body, styles["body"]))
        out.append(Spacer(1, 5))
        return out

    def skills_table(rows: list[tuple[str, str]]) -> Any:
        data = [
            [
                Paragraph(track(label.upper(), gap="", wordgap=1), styles["skilllabel"]),
                Paragraph(value, styles["skillval"]),
            ]
            for label, value in rows
        ]
        table = Table(data, colWidths=[SKILL_LABEL_W, CONTENT_W - SKILL_LABEL_W])
        table.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, -2), 0.4, HexColor(HAIR_CLR)),
        ]))
        return table

    header = dict(resume.header or {})
    story: list[Any] = []

    name = str(header.get("name", "")).strip()
    if name:
        story.append(Paragraph(track(name.upper(), gap=" ", wordgap=3), styles["name"]))
    tagline = str(header.get("tagline", "")).strip()
    if tagline:
        story.append(
            Paragraph(escape(tagline).replace("·", "&nbsp;·&nbsp;"), styles["tagline"])
        )
    contact_parts = [str(part).strip() for part in header.get("contact_line", []) if str(part).strip()]
    if contact_parts:
        story.append(
            Paragraph(
                "&nbsp;|&nbsp; ".join(escape(part) for part in contact_parts),
                styles["contact"],
            )
        )
    story.append(
        HRFlowable(
            width="100%", thickness=1.6, color=HexColor(ACCENT),
            spaceBefore=8, spaceAfter=10,
        )
    )
    if resume.summary:
        story.append(Paragraph(escape(str(resume.summary).strip()), styles["summary"]))

    for section in resume.sections or []:
        heading = str(section.get("name", "")).strip()
        entries = list(section.get("entries", []))
        if not heading or not entries:
            continue
        layout = str(section.get("layout", "") or LAYOUT_ENTRIES)

        if layout == LAYOUT_SKILLS:
            rows = [
                (str(entry.get("title", "")).strip(), _bullet_html(entry.get("bullets", [])))
                for entry in entries
                if str(entry.get("title", "")).strip()
            ]
            if not rows:
                continue
            story.append(KeepTogether([
                Spacer(1, 13),
                Paragraph(track(heading.upper()), styles["section"]),
                HRFlowable(
                    width="100%", thickness=1.0, color=HexColor(RULE_CLR),
                    spaceBefore=5, spaceAfter=7,
                ),
                skills_table(rows),
            ]))
            continue

        story.append(section_head(heading))

        if layout == LAYOUT_NOTES:
            for entry in entries:
                body = _bullet_html(entry.get("bullets", [])) + _entry_links(entry)
                if not body.strip():
                    continue
                story.append(Paragraph(body, styles["body"]))
                story.append(Spacer(1, 5))
            continue

        for entry in entries:
            story.extend(entry_block(
                escape(str(entry.get("title", "")).strip()),
                escape(str(entry.get("dates", "")).strip()),
                escape(str(entry.get("organization", "")).strip()),
                _bullet_html(entry.get("bullets", [])) + _entry_links(entry),
            ))

    return story


def render_pdf(resume: Any, destination: Path, *, title: str = "") -> None:
    """Write ``resume`` to ``destination`` as a PDF in the master CV's design."""
    try:
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
    except ImportError as exc:  # pragma: no cover - depends on the environment
        raise RuntimeError("ReportLab is required: pip install reportlab") from exc

    destination.parent.mkdir(parents=True, exist_ok=True)
    author = str((resume.header or {}).get("name", "")).strip()
    document = BaseDocTemplate(
        str(destination),
        pagesize=(A4_WIDTH, A4_HEIGHT),
        leftMargin=L_MARGIN,
        rightMargin=L_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title=title or (f"{author} - CV" if author else "CV"),
        author=author,
        subject="Curriculum Vitae",
    )
    frame = Frame(
        L_MARGIN, BOTTOM_MARGIN, CONTENT_W,
        A4_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN,
        id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    document.addPageTemplates([PageTemplate(id="all", frames=[frame])])

    def invariant_canvas(*args: Any, **kwargs: Any) -> Canvas:
        kwargs["invariant"] = 1
        return Canvas(*args, **kwargs)

    document.build(build_story(resume, _styles()), canvasmaker=invariant_canvas)
    if not destination.exists() or destination.stat().st_size == 0:
        raise RuntimeError("CV renderer produced an empty file")
