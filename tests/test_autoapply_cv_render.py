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
        self.assertEqual(_length_bounds("Built a controller."), (19, 360))

    def test_the_floor_never_exceeds_the_line_being_rewritten(self):
        # "SAT: 1500 (Dec 2023):" is 21 characters; a 24-character floor would
        # reject every possible rewrite of it.
        for original in ("SAT: 1500 (Dec 2023):", "IELTS: 8.0 (Apr 2024):"):
            low, high = _length_bounds(original, strict=False)
            self.assertLessEqual(low, len(original), original)
            self.assertGreater(high, len(original), original)


if __name__ == "__main__":
    unittest.main()


class FabricationGuardTests(unittest.TestCase):
    """The rewrite is unrestricted; the claims inside it are not."""

    ORIGINAL = "Built a controller for a mobile robot and evaluated it in simulation."
    # The fact bank names PhD only as a category of posting the tracker watches.
    CV = ORIGINAL + " Tracks research, PhD, and postdoc positions across Python tooling."

    def _rewrite(self, candidate, **kwargs):
        from autoapply.ai_tailoring import _validate_rewrite

        return _validate_rewrite(
            self.ORIGINAL, candidate, strict=False, evidence=self.CV, **kwargs
        )

    def test_a_faithful_rewrite_is_accepted(self):
        value = self._rewrite(
            "Developed a controller for a mobile robot and evaluated it in simulation."
        )
        self.assertTrue(value.startswith("Developed"))

    def test_a_degree_cannot_be_awarded_by_a_rewrite(self):
        with self.assertRaises(ValueError) as caught:
            self._rewrite(
                "Holds a PhD and built a controller for a mobile robot, "
                "evaluated in simulation."
            )
        self.assertEqual(str(caught.exception), "new_credential_claim")

    def test_a_summary_cannot_award_a_degree_named_elsewhere_in_the_cv(self):
        from autoapply.ai_tailoring import _validate_summary

        original = (
            "Researcher and engineer reading Artificial Intelligence at Birmingham, "
            "building robot controllers and evaluating them in simulation."
        )
        with self.assertRaises(ValueError) as caught:
            _validate_summary(
                original + " Tracks research, PhD, and postdoc positions.",
                "Researcher and engineer with a PhD in Artificial Intelligence, "
                "building robot controllers and evaluating them in simulation.",
                strict=False,
                original=original,
            )
        self.assertEqual(str(caught.exception), "new_credential_claim")

    def test_an_employer_cannot_be_smuggled_in_at_the_start_of_a_sentence(self):
        """A capitalised opener used to be exempt from the entity check."""
        with self.assertRaises(ValueError) as caught:
            self._rewrite(
                "Neuralink work: built a controller for a mobile robot, "
                "evaluated in simulation."
            )
        self.assertEqual(str(caught.exception), "new_named_technology_or_entity")

    def test_an_institution_cannot_be_smuggled_in_at_the_start_of_a_sentence(self):
        with self.assertRaises(ValueError) as caught:
            self._rewrite(
                "Stanford research: built a controller for a mobile robot, "
                "evaluated in simulation."
            )
        self.assertEqual(str(caught.exception), "new_named_technology_or_entity")

    def test_ordinary_verbs_may_still_open_a_rewrite(self):
        """The opener check must not reject plain English."""
        for opener in ("Developed", "Delivered", "Builds", "Led", "Rebuilt a"):
            with self.subTest(opener=opener):
                value = self._rewrite(
                    f"{opener} controller for a mobile robot and evaluated it "
                    "in simulation."
                )
                self.assertTrue(value.startswith(opener.split()[0]))

    def test_a_metric_from_another_entry_cannot_be_attached_to_this_one(self):
        """A number is a claim about one piece of work, not about the CV."""
        entry = "Robotics project. " + self.ORIGINAL
        document = entry + " Sales role: grew revenue by 40% across 12 markets."
        from autoapply.ai_tailoring import _validate_rewrite

        with self.assertRaises(ValueError) as caught:
            _validate_rewrite(
                self.ORIGINAL,
                "Built a controller for a mobile robot, raising task success "
                "by 40% over 12 simulated runs.",
                strict=False,
                evidence=document,
                local_evidence=entry,
            )
        self.assertEqual(str(caught.exception), "new_numeric_claim")

    def test_a_metric_from_this_entry_may_be_restated(self):
        entry = self.ORIGINAL + " The controller cut settling time by 30%."
        from autoapply.ai_tailoring import _validate_rewrite

        value = _validate_rewrite(
            self.ORIGINAL,
            "Built a controller for a mobile robot, cutting settling time by "
            "30% in simulation.",
            strict=False,
            evidence=entry,
            local_evidence=entry,
        )
        self.assertIn("30%", value)

    def test_a_requirement_the_cv_never_mentions_cannot_be_echoed_back(self):
        from autoapply.ai_tailoring import borrowed_terms

        forbidden = borrowed_terms(
            ["Strong background in neuroscience and neural decoding"], self.CV
        )
        self.assertIn("neuroscience", forbidden)
        with self.assertRaises(ValueError) as caught:
            self._rewrite(
                "Built a neuroscience controller for a mobile robot, "
                "evaluated in simulation.",
                forbidden=forbidden,
            )
        self.assertEqual(str(caught.exception), "borrowed_requirement_not_in_cv")

    def test_generic_requirement_words_are_not_barred(self):
        from autoapply.ai_tailoring import borrowed_terms

        forbidden = borrowed_terms(
            ["Demonstrated ability and strong communication over several years"],
            self.CV,
        )
        self.assertEqual(forbidden & {"ability", "communication", "years"}, set())

    def test_a_technology_the_cv_names_elsewhere_may_move_into_a_line(self):
        # Python is in the CV, so a rewrite may bring it to where it answers
        # the posting. That is tailoring, not invention.
        self.assertTrue(
            self._rewrite(
                "Built a Python controller for a mobile robot, evaluated in simulation."
            )
        )

    def test_a_technology_absent_from_the_whole_cv_is_rejected(self):
        with self.assertRaises(ValueError) as caught:
            self._rewrite(
                "Built a Kubernetes controller for a mobile robot, "
                "evaluated in simulation."
            )
        self.assertEqual(str(caught.exception), "new_named_technology_or_entity")


class TruncatedResponseTests(unittest.TestCase):
    def test_a_response_cut_off_mid_value_keeps_its_finished_entries(self):
        from autoapply.openai_tailoring import _json_object

        whole = (
            '{"bullets":[{"fact_id":"a","proposal":"one"},'
            '{"fact_id":"b","proposal":"two"}]}'
        )
        salvaged = _json_object(whole[:52])
        self.assertEqual(salvaged["bullets"], [{"fact_id": "a", "proposal": "one"}])

    def test_an_intact_response_is_parsed_whole(self):
        from autoapply.openai_tailoring import _json_object

        whole = '{"bullets":[{"fact_id":"a","proposal":"one"}],"advice":[]}'
        self.assertEqual(len(_json_object(whole)["bullets"]), 1)
