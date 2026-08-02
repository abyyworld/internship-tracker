import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from autoapply.ai_tailoring import _length_bounds, _validate_rewrite
from autoapply.cv_render import (
    A4_HEIGHT,
    A4_WIDTH,
    CONTENT_W,
    _bullet_html,
    _entry_links,
    build_story,
    render_pdf,
    track,
)


PROSE = (
    "Seven-stage pipeline taking raw teleoperation sessions to a trained, "
    "traceable policy: ingest, validate, score, dataset, train, evaluate, "
    "report. Each session receives a score and a gold, silver, or reject "
    "grade, and rejects never reach training, so a poor demonstration is "
    "identified from the numbers alone with no video review at any point."
)

RESUME = SimpleNamespace(
    header={
        "name": "Ada Lovelace",
        "tagline": "Analytical Engine Researcher · Numerical Methods",
        "contact_line": ["London, UK", "ada@invalid.test", "example.invalid"],
    },
    summary="Researcher and engineer working on analytical engines.",
    sections=[
        {
            "name": "Research",
            "layout": "entries",
            "entries": [
                {
                    "title": "Note G",
                    "organization": "Independent research · first published algorithm",
                    "url": "https://example.invalid/note-g",
                    "link_text": "GitHub",
                    "bullets": [
                        {"id": "lead", "text": "The engine can do more than arithmetic.", "style": "lead"},
                        {"id": "body", "text": PROSE},
                    ],
                }
            ],
        },
        {
            "name": "Honours",
            "layout": "notes",
            "entries": [
                {"bullets": [{"id": "award", "text": "Recognised for the first algorithm."}]}
            ],
        },
        {
            "name": "Skills & Languages",
            "layout": "skills",
            "entries": [
                {"title": "Mathematics", "bullets": [{"id": "maths", "text": "Analysis, Number Theory"}]}
            ],
        },
    ],
)


class TrackingTests(unittest.TestCase):
    def test_letterspacing_matches_the_master_design(self):
        self.assertEqual(track("AB CD", gap=" ", wordgap=3), "A B&nbsp;&nbsp;&nbsp;C D")

    def test_ampersands_survive_as_markup_entities(self):
        self.assertIn("&amp;", track("R&D"))


class BulletMarkupTests(unittest.TestCase):
    def test_a_lead_bullet_prints_bold_ahead_of_its_body(self):
        html = _bullet_html(
            [{"id": "a", "text": "Claim.", "style": "lead"}, {"id": "b", "text": "Body."}]
        )
        self.assertEqual(html, "<b>Claim.</b> Body.")

    def test_plain_strings_still_render(self):
        self.assertEqual(_bullet_html(["Body."]), "Body.")

    def test_angle_brackets_cannot_inject_markup(self):
        self.assertNotIn("<i>", _bullet_html([{"id": "a", "text": "<i>x</i>"}]))

    def test_links_print_in_the_order_the_master_cv_uses(self):
        html = _entry_links({
            "url": "https://example.invalid/repo",
            "link_text": "GitHub",
            "link_extra_url": "https://example.invalid/site",
            "link_extra_text": "Dashboard",
        })
        self.assertLess(html.index("Dashboard"), html.index("GitHub"))


class RenderTests(unittest.TestCase):
    def test_a_long_cv_renders_to_a_multi_page_a4_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "cv.pdf"
            long_resume = SimpleNamespace(
                header=RESUME.header,
                summary=RESUME.summary,
                sections=RESUME.sections * 12,
            )
            render_pdf(long_resume, destination)
            body = destination.read_bytes()
            self.assertGreater(destination.stat().st_size, 0)
            # More content than one page fits must paginate, not overflow.
            self.assertGreater(body.count(b"/Type /Page\n"), 1)

    def test_every_section_layout_produces_flowables(self):
        from reportlab.lib.styles import ParagraphStyle

        from autoapply.cv_render import _styles

        story = build_story(RESUME, _styles())
        self.assertTrue(story)

        def texts(items):
            for item in items:
                # Section heads are grouped so a heading never ends a page alone.
                yield from texts(getattr(item, "_content", []) or [])
                yield getattr(item, "text", "")

        rendered = " ".join(texts(story))
        self.assertIn("R E S E A R C H", rendered)
        self.assertIn("H O N O U R S", rendered)
        self.assertIsInstance(_styles()["body"], ParagraphStyle)

    def test_the_page_geometry_is_the_master_design(self):
        self.assertAlmostEqual(A4_WIDTH, 595.2755905511812)
        self.assertAlmostEqual(A4_HEIGHT, 841.8897637795277)
        self.assertAlmostEqual(CONTENT_W, 510.2355905511812)


class RewriteLengthTests(unittest.TestCase):
    def test_a_prose_entry_may_be_rewritten_as_prose(self):
        rewrite = PROSE.replace("Seven-stage pipeline", "Seven-stage system")
        self.assertEqual(_validate_rewrite(PROSE, rewrite), rewrite)

    def test_a_paragraph_cannot_be_replaced_by_a_sentence(self):
        with self.assertRaises(ValueError):
            _validate_rewrite(PROSE, "Built a pipeline for teleoperation data.")

    def test_short_bullets_keep_their_original_bounds(self):
        self.assertEqual(_length_bounds("Built a controller."), (24, 360))


if __name__ == "__main__":
    unittest.main()
