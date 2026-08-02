import unittest
from urllib.parse import unquote_plus

from universities import (
    ACADEMIC_POSITION_TYPES,
    _index,
    annotate,
    load_universities,
    match_university,
    research_terms,
    supervisor_links,
)


class DatasetTests(unittest.TestCase):
    def setUp(self):
        self.universities = load_universities()

    def test_the_dataset_covers_a_hundred_institutions(self):
        self.assertEqual(len(self.universities), 100)

    def test_every_entry_carries_a_domain_and_country(self):
        for entry in self.universities:
            self.assertTrue(entry["domain"], entry["name"])
            self.assertTrue(entry.get("country"), entry["name"])
            self.assertNotIn(" ", entry["domain"], entry["name"])

    def test_names_and_aliases_are_unique(self):
        keys = [key for key, _ in _index(self.universities)]
        duplicates = {key for key in keys if keys.count(key) > 1}
        self.assertEqual(duplicates, set())


class MatchingTests(unittest.TestCase):
    def setUp(self):
        self.index = _index(load_universities())

    def test_a_university_employer_is_matched(self):
        matched = match_university("University of Birmingham", self.index)
        self.assertEqual(matched["domain"], "bham.ac.uk")

    def test_an_alias_inside_a_longer_name_is_matched(self):
        self.assertEqual(
            match_university("MIT CSAIL", self.index)["name"],
            "Massachusetts Institute of Technology",
        )

    def test_the_longest_matching_name_wins(self):
        # "berkeley" alone must not beat the full institution name.
        matched = match_university("University of California, Berkeley", self.index)
        self.assertEqual(matched["domain"], "berkeley.edu")

    def test_a_non_university_employer_is_not_matched(self):
        self.assertIsNone(match_university("Jane Street", self.index))
        self.assertIsNone(match_university("", self.index))


class SearchTermTests(unittest.TestCase):
    def test_employment_words_are_not_treated_as_research_topics(self):
        terms = research_terms("PhD Studentship in Robot Learning", "")
        self.assertNotIn("phd", terms)
        self.assertNotIn("studentship", terms)
        self.assertIn("robot", terms)
        self.assertIn("learning", terms)

    def test_focus_tags_contribute_terms(self):
        terms = research_terms("Research Assistant", "computer-vision,perception")
        self.assertIn("computer", terms)

    def test_terms_are_capped(self):
        self.assertLessEqual(len(research_terms("a b c d e f g h robotics vision nlp llm hci")), 4)


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.entry = {"name": "University of Oxford", "domain": "ox.ac.uk"}

    def test_the_scholar_search_is_scoped_to_the_institutional_domain(self):
        links = supervisor_links(self.entry, ["robot", "learning"])
        self.assertIn("ox.ac.uk", unquote_plus(links["scholar"]))
        self.assertIn("robot learning", unquote_plus(links["scholar"]))

    def test_every_link_is_https(self):
        for url in supervisor_links(self.entry, ["vision"]).values():
            self.assertTrue(url.startswith("https://"), url)

    def test_links_work_without_any_research_terms(self):
        for url in supervisor_links(self.entry, []).values():
            self.assertTrue(url.startswith("https://"), url)


class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.index = _index(load_universities())

    def test_a_university_posting_is_annotated(self):
        job = {"company": "ETH Zurich", "role": "PhD in Robot Learning",
               "focus": "robotics", "position_type": "phd-fellowship"}
        annotate(job, self.index)
        self.assertEqual(job["university"]["domain"], "ethz.ch")
        self.assertTrue(job["university"]["research_track"])

    def test_a_university_internship_is_annotated_but_not_flagged_research(self):
        job = {"company": "Pennsylvania State University", "role": "R&D Engineer Intern",
               "focus": "", "position_type": "intern"}
        annotate(job, self.index)
        self.assertIn("university", job)
        self.assertFalse(job["university"]["research_track"])

    def test_a_company_posting_is_left_alone(self):
        job = {"company": "Citadel", "role": "Software Engineer Intern",
               "focus": "", "position_type": "intern"}
        annotate(job, self.index)
        self.assertNotIn("university", job)

    def test_the_research_track_set_matches_the_dashboard_chips(self):
        self.assertIn("postdoc", ACADEMIC_POSITION_TYPES)
        self.assertIn("phd-fellowship", ACADEMIC_POSITION_TYPES)


if __name__ == "__main__":
    unittest.main()
