"""The deterministic half of tailoring: what can be counted is not asserted.

Nothing here touches a network. Every function under test is a pure function
of text, which is the point of having them.
"""

import unittest

from autoapply.suggestion_quality import (
    MIN_SCORABLE_TERMS,
    covers,
    coverage_score,
    evidence_gaps,
    is_screening_term,
    keyword_panel,
    normalise_importance,
    posting_vocabulary,
    significant_parts,
    terms_gained,
)
from autoapply.tailoring import concepts


CV = (
    "Built a data processing pipeline in Python. "
    "Studied algorithms and data structures. Wrote unit tests."
)


class ScreeningTermTests(unittest.TestCase):
    def test_boilerplate_is_stripped_before_matching(self):
        self.assertEqual(significant_parts("Strong Python proficiency"), {"python"})

    def test_a_term_that_is_only_boilerplate_is_not_a_screening_term(self):
        for term in ("strong communication skills", "excellent team player"):
            with self.subTest(term=term):
                self.assertFalse(is_screening_term(term))

    def test_a_sentence_is_not_a_screening_term(self):
        self.assertFalse(
            is_screening_term(
                "The candidate should have experience with distributed systems"
            )
        )

    def test_a_date_is_not_a_screening_term(self):
        self.assertFalse(is_screening_term("starting June 2026"))

    def test_a_named_technology_is_a_screening_term(self):
        for term in ("Python", "Kubernetes", "distributed training"):
            with self.subTest(term=term):
                self.assertTrue(is_screening_term(term))


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.cv_terms = concepts(CV)

    def test_a_term_the_cv_evidences_is_covered(self):
        self.assertTrue(covers("Python", self.cv_terms))
        self.assertTrue(covers("data processing", self.cv_terms))

    def test_a_partial_match_is_a_gap_not_a_match(self):
        """The bug this replaces: two words of three counted as covered."""
        self.assertFalse(covers("distributed data processing", self.cv_terms))

    def test_boilerplate_around_a_covered_term_does_not_block_it(self):
        self.assertTrue(covers("strong Python proficiency", self.cv_terms))

    def test_a_term_the_cv_never_mentions_is_missing(self):
        self.assertFalse(covers("Kubernetes", self.cv_terms))


class KeywordPanelTests(unittest.TestCase):
    RAW = [
        {"term": "Python", "status": "missing", "importance": "high"},
        {"term": "Kubernetes", "status": "covered", "importance": "high"},
        {"term": "distributed data processing", "importance": "high"},
        {"term": "data processing", "importance": "medium"},
        {"term": "strong communication skills", "importance": "low"},
        {"term": "starting in 2026", "importance": "low"},
        {"term": "python", "importance": "low"},
    ]

    def setUp(self):
        self.panel = keyword_panel(self.RAW, CV)
        self.by_term = {k["term"]: k for k in self.panel}

    def test_the_models_claim_about_coverage_is_recomputed(self):
        """It said Python was missing and Kubernetes covered. Both were wrong."""
        self.assertEqual(self.by_term["Python"]["status"], "covered")
        self.assertEqual(self.by_term["Kubernetes"]["status"], "missing")

    def test_padding_is_dropped_rather_than_carried(self):
        self.assertNotIn("strong communication skills", self.by_term)
        self.assertNotIn("starting in 2026", self.by_term)

    def test_a_repeated_term_is_listed_once(self):
        self.assertEqual(len([k for k in self.panel if k["term"].lower() == "python"]), 1)

    def test_importance_is_normalised(self):
        self.assertEqual(normalise_importance("HIGH"), "high")
        self.assertEqual(normalise_importance("critical"), "medium")
        self.assertEqual(normalise_importance(None), "medium")

    def test_a_junk_entry_does_not_break_the_panel(self):
        self.assertEqual(keyword_panel([None, 7, {}, {"term": ""}], CV), [])


class CoverageScoreTests(unittest.TestCase):
    def test_the_score_agrees_with_the_panel_beside_it(self):
        panel = [
            {"term": "a", "status": "covered", "importance": "high"},
            {"term": "b", "status": "covered", "importance": "high"},
            {"term": "c", "status": "missing", "importance": "high"},
            {"term": "d", "status": "missing", "importance": "high"},
        ]
        self.assertEqual(coverage_score(panel), 50)

    def test_a_missing_high_importance_term_costs_more_than_a_low_one(self):
        high_gap = [
            {"term": "a", "status": "missing", "importance": "high"},
            {"term": "b", "status": "covered", "importance": "low"},
            {"term": "c", "status": "covered", "importance": "low"},
            {"term": "d", "status": "covered", "importance": "low"},
        ]
        low_gap = [
            {"term": "a", "status": "covered", "importance": "high"},
            {"term": "b", "status": "missing", "importance": "low"},
            {"term": "c", "status": "covered", "importance": "low"},
            {"term": "d", "status": "covered", "importance": "low"},
        ]
        self.assertLess(coverage_score(high_gap), coverage_score(low_gap))

    def test_too_few_terms_means_no_figure_rather_than_a_flattering_one(self):
        panel = [{"term": "a", "status": "covered", "importance": "high"}]
        self.assertLess(len(panel), MIN_SCORABLE_TERMS)
        self.assertIsNone(coverage_score(panel))

    def test_an_empty_panel_scores_nothing(self):
        self.assertIsNone(coverage_score([]))


class GapTests(unittest.TestCase):
    def test_the_gaps_are_named_and_ordered_by_importance(self):
        panel = [
            {"term": "Rust", "status": "missing", "importance": "low"},
            {"term": "Kubernetes", "status": "missing", "importance": "high"},
            {"term": "Python", "status": "covered", "importance": "high"},
        ]
        gaps = evidence_gaps(panel)
        self.assertEqual(len(gaps), 2)
        self.assertIn("Kubernetes", gaps[0])
        self.assertIn("Rust", gaps[1])

    def test_a_gap_never_invites_the_applicant_to_invent_one(self):
        panel = [{"term": "Kubernetes", "status": "missing", "importance": "high"}]
        self.assertIn("only if you have genuinely done it", evidence_gaps(panel)[0])

    def test_a_cv_with_no_gaps_reports_none(self):
        panel = [{"term": "Python", "status": "covered", "importance": "high"}]
        self.assertEqual(evidence_gaps(panel), [])


class TermsGainedTests(unittest.TestCase):
    def test_a_rewrite_reports_the_posting_words_it_brings_in(self):
        gained = terms_gained(
            "Worked on a training pipeline.",
            "Built a distributed training pipeline.",
            {"distributed", "training", "kubernete"},
        )
        self.assertEqual(gained, ["distributed"])

    def test_a_rephrasing_that_gains_nothing_says_so(self):
        self.assertEqual(
            terms_gained(
                "Built a distributed training pipeline.",
                "Developed a distributed training pipeline.",
                {"distributed", "training"},
            ),
            [],
        )

    def test_words_the_posting_never_asked_for_are_not_counted_as_gains(self):
        self.assertEqual(
            terms_gained("Built a pipeline.", "Built a Rust pipeline.", {"python"}),
            [],
        )

    def test_the_posting_vocabulary_comes_from_requirements_and_terms(self):
        vocabulary = posting_vocabulary(
            ["Strong experience with distributed training"],
            [{"term": "Kubernetes"}],
        )
        self.assertIn("distributed", vocabulary)
        self.assertIn("kubernete", vocabulary)
        # Boilerplate the posting phrases itself in is not vocabulary.
        self.assertNotIn("experience", vocabulary)
        self.assertNotIn("strong", vocabulary)


if __name__ == "__main__":
    unittest.main()
