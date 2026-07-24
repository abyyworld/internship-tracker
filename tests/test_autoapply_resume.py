import json
import tempfile
from pathlib import Path
import unittest

from autoapply.models import Job
from autoapply.resume import render_resume
from autoapply.tailoring import tailor_resume


def applicant():
    return {
        "identity": {"first_name": "Ada", "last_name": "Lovelace"},
        "contact": {"email": "ada@invalid.test", "location": "London"},
    }


def entry(title, bullets):
    return {"title": title, "organization": "Verified Org", "bullets": bullets}


class ResumeTests(unittest.TestCase):
    def test_only_relevant_verbatim_facts_are_selected_and_linked(self):
        job = Job(
            "robotics",
            "Robotics Co",
            "Robotics Perception Intern",
            "https://invalid.test",
            description="Python computer vision perception for autonomous robots",
        )
        facts = {
            "summary": "Verified summary.",
            "skills": ["Writing", "Python", "Computer Vision"],
            "education": [
                {"institution": "Example University", "degree": "BSc Computer Science"}
            ],
            "sections": [
                {
                    "name": "Projects",
                    "entries": [
                        entry(
                            "Projects",
                            [
                                {
                                    "id": "robot",
                                    "text": "Built a Python perception prototype.",
                                    "tags": ["robotics", "perception", "python"],
                                    "evidence": "https://github.invalid/verified-robot",
                                },
                                {
                                    "id": "writing",
                                    "text": "Edited a student magazine.",
                                    "tags": ["writing"],
                                },
                            ],
                        )
                    ],
                }
            ],
        }
        tailored = tailor_resume(job, applicant(), facts)

        bullets = tailored.sections[0]["entries"][0]["bullets"]
        self.assertEqual(bullets, ["Built a Python perception prototype."])
        self.assertEqual(tailored.selected_fact_ids, ["robot"])
        self.assertEqual(tailored.skills, ["Python", "Computer Vision"])
        self.assertEqual(tailored.sections[0]["entries"][0]["evidence_ids"], ["robot"])

        link = tailored.evidence_links[0]
        self.assertEqual(link.fact_id, "robot")
        self.assertEqual(link.text, facts["sections"][0]["entries"][0]["bullets"][0]["text"])
        self.assertEqual(link.source_path, "sections[0].entries[0].bullets[0]")
        self.assertEqual(link.source_ref, "https://github.invalid/verified-robot")
        self.assertGreater(link.score, 0)
        self.assertEqual(tailored.selection_audit["selected_fact_count"], 1)

    def test_title_relevance_outweighs_equal_description_only_evidence(self):
        job = Job(
            "rank",
            "Acme",
            "Robotics Intern",
            "https://invalid.test",
            description="Python perception",
        )
        facts = {
            "skills": [],
            "education": [],
            "sections": [
                {
                    "name": "Projects",
                    "entries": [
                        entry(
                            "Projects",
                            [
                                {
                                    "id": "description-match",
                                    "text": "Used Python perception tooling.",
                                    "tags": [],
                                },
                                {
                                    "id": "title-match",
                                    "text": "Built a robotics system.",
                                    "tags": [],
                                },
                            ],
                        )
                    ],
                }
            ],
        }
        tailored = tailor_resume(job, applicant(), facts)
        self.assertEqual(tailored.selected_fact_ids[0], "title-match")

    def test_global_limits_and_tie_breaking_are_deterministic(self):
        job = Job(
            "limits",
            "Acme",
            "Robotics Software Intern",
            "https://invalid.test",
            description="Python robotics software",
        )
        facts = {
            "skills": ["Python", "Robotics", "Writing", "Python"],
            "education": [],
            "sections": [
                {
                    "name": "Experience",
                    "entries": [
                        entry(
                            "Robotics",
                            [
                                {"id": f"a-{index}", "text": f"Built robotics module {index}.", "tags": ["robotics"]}
                                for index in range(4)
                            ],
                        ),
                        entry(
                            "Software",
                            [
                                {"id": f"b-{index}", "text": f"Built Python service {index}.", "tags": ["python"]}
                                for index in range(4)
                            ],
                        ),
                    ],
                }
            ],
        }
        first = tailor_resume(
            job,
            applicant(),
            facts,
            max_bullets=3,
            max_bullets_per_entry=2,
            max_entries=2,
            max_skills=2,
        )
        second = tailor_resume(
            job,
            applicant(),
            facts,
            max_bullets=3,
            max_bullets_per_entry=2,
            max_entries=2,
            max_skills=2,
        )
        self.assertEqual(first.selected_fact_ids, second.selected_fact_ids)
        self.assertEqual(first.evidence_links, second.evidence_links)
        self.assertEqual(first.selection_audit, second.selection_audit)
        self.assertEqual(len(first.selected_fact_ids), 3)
        self.assertLessEqual(
            max(len(item["bullets"]) for item in first.sections[0]["entries"]), 2
        )
        self.assertEqual(first.skills, ["Robotics", "Python"])

    def test_missing_ids_are_excluded_and_conflicting_ids_fail(self):
        job = Job(
            "integrity",
            "Acme",
            "Robotics Intern",
            "https://invalid.test",
            description="robotics",
        )
        missing = {
            "skills": [],
            "education": [],
            "sections": [
                {
                    "name": "Projects",
                    "entries": [
                        entry(
                            "Robotics",
                            [
                                {"text": "Untraceable robotics claim.", "tags": ["robotics"]},
                                {
                                    "id": "verified",
                                    "text": "Verified robotics claim.",
                                    "tags": ["robotics"],
                                },
                            ],
                        )
                    ],
                }
            ],
        }
        tailored = tailor_resume(job, applicant(), missing)
        self.assertEqual(tailored.selected_fact_ids, ["verified"])
        self.assertEqual(
            tailored.selection_audit["excluded_missing_id_or_text_count"], 1
        )

        conflicting = {
            "skills": [],
            "education": [],
            "sections": [
                {
                    "name": "Projects",
                    "entries": [
                        entry(
                            "Robotics",
                            [
                                {"id": "same", "text": "First fact.", "tags": ["robotics"]},
                                {"id": "same", "text": "Different fact.", "tags": ["robotics"]},
                            ],
                        )
                    ],
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "conflicting facts"):
            tailor_resume(job, applicant(), conflicting)

    def test_entry_context_cannot_make_an_irrelevant_claim_eligible(self):
        job = Job(
            "no-laundering",
            "Acme",
            "Robotics Intern",
            "https://invalid.test",
            description="robot perception",
        )
        facts = {
            "skills": ["Writing"],
            "education": [],
            "sections": [
                {
                    "name": "Projects",
                    "entries": [
                        entry(
                            "Robotics Research",
                            [
                                {
                                    "id": "irrelevant",
                                    "text": "Edited a student magazine.",
                                    "tags": ["writing"],
                                }
                            ],
                        )
                    ],
                }
            ],
        }
        tailored = tailor_resume(job, applicant(), facts)
        self.assertEqual(tailored.selected_fact_ids, [])
        self.assertEqual(tailored.sections, [])
        self.assertEqual(tailored.skills, [])
        self.assertEqual(tailored.selection_audit["relevant_fact_count"], 0)

    def test_generic_language_and_awards_do_not_crowd_out_technical_evidence(self):
        job = Job(
            "technical-first",
            "Robot Co",
            "Electrical Engineering Intern",
            "https://invalid.test",
            description=(
                "Build robotics systems in Python. Strong communication and "
                "English are required."
            ),
        )
        facts = {
            "skills": ["Python", "Robotics", "English"],
            "education": [],
            "sections": [
                {
                    "name": "Experience",
                    "entries": [
                        entry(
                            "Drone Engineering",
                            [
                                {
                                    "id": "technical",
                                    "text": "Built a Python robotics prototype.",
                                    "tags": ["python", "robotics"],
                                }
                            ],
                        )
                    ],
                },
                {
                    "name": "Projects",
                    "entries": [
                        entry(
                            "Systems Project",
                            [
                                {
                                    "id": "systems",
                                    "text": "Implemented a software system.",
                                    "tags": ["software", "systems"],
                                }
                            ],
                        )
                    ],
                },
                {
                    "name": "Awards",
                    "entries": [
                        entry(
                            "Awards",
                            [
                                {
                                    "id": "english-one",
                                    "text": "Earned an English award.",
                                    "tags": ["english", "communication"],
                                },
                                {
                                    "id": "english-two",
                                    "text": "Earned another English award.",
                                    "tags": ["english", "communication"],
                                },
                            ],
                        )
                    ],
                },
            ],
        }
        tailored = tailor_resume(job, applicant(), facts)
        self.assertEqual(tailored.selected_fact_ids[0], "technical")
        self.assertLessEqual(
            len(
                [
                    fact_id
                    for fact_id in tailored.selected_fact_ids
                    if fact_id.startswith("english-")
                ]
            ),
            1,
        )

    def test_pdf_and_evidence_sidecar_are_deterministic_and_private(self):
        job = Job(
            "render",
            "Acme",
            "Python Intern",
            "https://invalid.test",
            description="Python",
        )
        facts = {
            "summary": "Verified summary.",
            "skills": ["Python"],
            "education": [],
            "sections": [
                {
                    "name": "Projects",
                    "entries": [
                        entry(
                            "Python Project",
                            [
                                {
                                    "id": "python-fact",
                                    "text": "Built a verified Python project.",
                                    "tags": ["python"],
                                }
                            ],
                        )
                    ],
                }
            ],
        }
        tailored = tailor_resume(job, applicant(), facts)
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.pdf"
            second = Path(directory) / "second.pdf"
            first_hash = render_resume(tailored, first)
            second_hash = render_resume(tailored, second)

            self.assertTrue(first.read_bytes().startswith(b"%PDF"))
            self.assertEqual(first_hash, second_hash)
            self.assertEqual(len(first_hash), 64)
            evidence = json.loads(
                first.with_name("first.evidence.json").read_text(encoding="utf-8")
            )
            self.assertEqual(evidence["resume_sha256"], first_hash)
            self.assertEqual(evidence["selected_fact_ids"], ["python-fact"])
            self.assertEqual(
                evidence["evidence_links"][0]["source_path"],
                "sections[0].entries[0].bullets[0]",
            )
            self.assertEqual(first.stat().st_mode & 0o777, 0o600)
            self.assertEqual(
                first.with_name("first.evidence.json").stat().st_mode & 0o777,
                0o600,
            )


if __name__ == "__main__":
    unittest.main()
