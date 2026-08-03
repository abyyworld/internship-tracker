"""The editing surface: alternatives, added and removed lines, answers."""

import unittest

from autoapply.cv_editor import (
    MAX_VARIANTS,
    facts_from_document,
    master_document,
    normalize_draft,
    ordered_sections,
    resume_from_document,
)


PROFILE = {
    "identity": {"first_name": "Ada", "last_name": "Lovelace"},
    "contact": {"email": "ada@invalid.test"},
}
FACTS = {
    "summary": "Engineer with verified project work.",
    "skills": ["Python"],
    "education": [],
    "sections": [
        {
            "name": "Projects",
            "layout": "entries",
            "entries": [
                {
                    "title": "Engine",
                    "bullets": [
                        {"id": "lead", "text": "It computes.", "style": "lead"},
                        {"id": "body", "text": "Built the analytical engine routines."},
                    ],
                },
                {
                    "title": "Notes",
                    "bullets": [{"id": "notes", "text": "Wrote the first algorithm."}],
                },
            ],
        }
    ],
}


class VariantTests(unittest.TestCase):
    def setUp(self):
        self.document = master_document(PROFILE, FACTS)

    def _draft(self, patch):
        return normalize_draft(self.document, "job-1", {"bullets": {"body": patch}})

    def test_alternative_phrasings_survive_a_save(self):
        draft = self._draft({
            "id": "body",
            "proposal": "Built the analytical engine routines end to end.",
            "variants": [
                "Built the analytical engine routines end to end.",
                "Wrote the routines that drive the analytical engine.",
            ],
        })
        self.assertEqual(len(draft["bullets"]["body"]["variants"]), 2)

    def test_the_selected_proposal_is_always_among_the_options(self):
        draft = self._draft({
            "id": "body",
            "proposal": "Built the analytical engine routines end to end.",
            "variants": ["Wrote the routines that drive the analytical engine."],
        })
        patch = draft["bullets"]["body"]
        self.assertIn(patch["proposal"], patch["variants"])

    def test_the_number_of_options_is_capped(self):
        draft = self._draft({
            "id": "body",
            "proposal": "Built the analytical engine routines end to end.",
            "variants": [f"Alternative phrasing number {n} of the routines." for n in range(9)],
        })
        self.assertLessEqual(len(draft["bullets"]["body"]["variants"]), MAX_VARIANTS)


class AddedAndRemovedLineTests(unittest.TestCase):
    def setUp(self):
        self.document = master_document(PROFILE, FACTS)

    def _draft(self, incoming):
        return normalize_draft(self.document, "job-1", incoming)

    def test_a_removed_line_leaves_this_jobs_cv_only(self):
        draft = self._draft({"removed": ["lead"]})
        bullets = [
            bullet["id"]
            for section in ordered_sections(self.document, draft)
            for entry in section["entries"]
            for bullet in entry["bullets"]
        ]
        self.assertNotIn("lead", bullets)
        self.assertIn("body", bullets)
        # The fact bank is untouched: the master document still has both.
        self.assertEqual(len(self.document["sections"][0]["entries"][0]["bullets"]), 2)

    def test_an_entry_whose_every_line_is_removed_leaves_the_cv(self):
        draft = self._draft({"removed": ["notes"]})
        titles = [
            entry["title"]
            for section in ordered_sections(self.document, draft)
            for entry in section["entries"]
        ]
        self.assertNotIn("Notes", titles)

    def test_an_accepted_added_line_prints_and_a_pending_one_does_not(self):
        draft = self._draft({
            "added": {
                "s0e0": [
                    {"id": "s0e0-new0", "text": "Also proved the routines terminate.",
                     "status": "accepted", "source": "manual"},
                    {"id": "s0e0-new1", "text": "Not accepted yet.",
                     "status": "pending", "source": "ai"},
                ]
            }
        })
        texts = [
            bullet["text"]
            for section in ordered_sections(self.document, draft)
            for entry in section["entries"]
            for bullet in entry["bullets"]
        ]
        self.assertIn("Also proved the routines terminate.", texts)
        self.assertNotIn("Not accepted yet.", texts)

    def test_added_lines_reach_the_exported_cv_and_a_saved_copy(self):
        draft = self._draft({
            "added": {
                "s0e1": [{"id": "s0e1-new0", "text": "Published the notes.",
                          "status": "accepted", "source": "manual"}]
            },
            "removed": ["lead"],
        })
        resume = resume_from_document(self.document, draft)
        rendered = [
            bullet["text"]
            for section in resume.sections
            for entry in section["entries"]
            for bullet in entry["bullets"]
        ]
        self.assertIn("Published the notes.", rendered)
        self.assertNotIn("It computes.", rendered)
        saved = facts_from_document(self.document, draft)
        kept = [
            bullet["text"]
            for section in saved["sections"]
            for entry in section["entries"]
            for bullet in entry["bullets"]
        ]
        self.assertIn("Published the notes.", kept)

    def test_a_line_id_that_is_not_in_the_document_is_ignored(self):
        draft = self._draft({"removed": ["nonexistent"], "added": {"nope": []}})
        self.assertEqual(draft["removed"], [])
        self.assertEqual(draft["added"], {})

    def test_an_added_line_source_must_be_declared(self):
        with self.assertRaises(ValueError):
            self._draft({
                "added": {"s0e0": [{"text": "x" * 50, "source": "elsewhere"}]}
            })


class AnswerDraftTests(unittest.TestCase):
    def setUp(self):
        self.document = master_document(PROFILE, FACTS)

    def test_questions_and_letters_round_trip(self):
        draft = normalize_draft(self.document, "job-1", {
            "questions": [
                {"id": "q0", "question": "Why us?", "answer": "Because.",
                 "word_limit": 200, "source": "posting"},
                {"question": "", "answer": "dropped"},
            ],
            "cover_letter": {"text": "Dear team,"},
            "keywords": [{"term": "Python", "status": "covered", "importance": "high"}],
            "match_score": 71,
        })
        self.assertEqual(len(draft["questions"]), 1)
        self.assertEqual(draft["questions"][0]["word_limit"], 200)
        self.assertEqual(draft["cover_letter"]["text"], "Dear team,")
        self.assertEqual(draft["keywords"][0]["status"], "covered")
        self.assertEqual(draft["match_score"], 71)

    def test_an_empty_letter_is_stored_as_absent(self):
        draft = normalize_draft(
            self.document, "job-1", {"cover_letter": {"text": "   "}}
        )
        self.assertIsNone(draft["cover_letter"])

    def test_a_keyword_status_outside_the_pair_is_treated_as_missing(self):
        draft = normalize_draft(
            self.document, "job-1", {"keywords": [{"term": "Rust", "status": "maybe"}]}
        )
        self.assertEqual(draft["keywords"][0]["status"], "missing")


class KeywordCoverageTests(unittest.TestCase):
    def test_claimed_coverage_is_checked_against_the_cv(self):
        from autoapply.tailoring import concepts

        cv_terms = concepts("Built analytical engine routines in Python.")
        self.assertTrue(concepts("Python") <= cv_terms)
        self.assertFalse(concepts("Kubernetes") <= cv_terms)


if __name__ == "__main__":
    unittest.main()
