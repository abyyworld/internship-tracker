from pathlib import Path
import stat
import tempfile
import unittest

from autoapply.cv_editor import (
    load_draft,
    master_document,
    resume_from_document,
    save_draft,
)


def profile():
    return {
        "identity": {"first_name": "Ada", "last_name": "Lovelace"},
        "contact": {"email": "ada@invalid.test", "location": "London"},
    }


def facts():
    return {
        "summary": "Student building verified robotics projects.",
        "skills": ["Python", "C++", "Robotics"],
        "education": [{"institution": "University", "degree": "BSc"}],
        "sections": [
            {
                "name": "Projects",
                "entries": [
                    {
                        "title": "Robot",
                        "organization": "Lab",
                        "bullets": [
                            {
                                "id": "robot",
                                "text": (
                                    "Built a Python robot controller and reduced "
                                    "latency by 20%."
                                ),
                            },
                            {
                                "id": "vision",
                                "text": (
                                    "Tested a computer vision prototype on "
                                    "recorded images."
                                ),
                            },
                        ],
                    }
                ],
            }
        ],
    }


class CvEditorTests(unittest.TestCase):
    def test_export_retains_every_master_fact_and_only_applies_accepted_edits(self):
        document = master_document(profile(), facts())
        draft = {
            "bullets": {
                "robot": {
                    "id": "robot",
                    "proposal": (
                        "Developed a Python robot controller, reducing latency by 20%."
                    ),
                    "status": "accepted",
                },
                "vision": {
                    "id": "vision",
                    "proposal": (
                        "Evaluated a computer vision prototype on recorded images."
                    ),
                    "status": "rejected",
                },
            }
        }
        resume = resume_from_document(document, draft)
        bullets = resume.sections[0]["entries"][0]["bullets"]
        self.assertEqual(len(resume.selected_fact_ids), 2)
        self.assertEqual(len(bullets), 2)
        self.assertTrue(bullets[0].startswith("Developed"))
        self.assertEqual(bullets[1], facts()["sections"][0]["entries"][0]["bullets"][1]["text"])
        self.assertEqual(resume.skills, facts()["skills"])
        self.assertTrue(
            resume.selection_audit["untouched_content_preserved"]
        )

    def test_draft_is_private_and_unknown_fact_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            document = master_document(profile(), facts())
            incoming = {
                "instructions": "Emphasise robotics.",
                "bullets": {
                    "robot": {
                        "id": "robot",
                        "proposal": (
                            "Developed a Python robot controller, reducing "
                            "latency by 20%."
                        ),
                        "status": "pending",
                    }
                },
            }
            save_draft(home, document, "job", incoming)
            self.assertEqual(load_draft(home, "job")["instructions"], "Emphasise robotics.")
            path = home / "editor-drafts" / "job.json"
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            incoming["bullets"]["invented"] = {
                "proposal": "Invented unsupported evidence.",
            }
            with self.assertRaisesRegex(ValueError, "unknown fact"):
                save_draft(home, document, "job", incoming)


if __name__ == "__main__":
    unittest.main()
