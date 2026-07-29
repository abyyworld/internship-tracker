import stat
import tempfile
import unittest
from pathlib import Path

import yaml

from autoapply.cv_editor import (
    draft_path,
    facts_from_document,
    master_document,
    normalize_draft,
)
from autoapply.cv_library import (
    MASTER_CV_ID,
    cv_path,
    list_cvs,
    load_cv,
    safe_cv_id,
    save_cv,
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
            "entries": [
                {
                    "title": "Robot",
                    "bullets": [
                        {"id": "robot", "text": "Built a controller."},
                        {"id": "vision", "text": "Tested a prototype."},
                    ],
                }
            ],
        }
    ],
}


class CvLibraryTests(unittest.TestCase):
    def test_master_resolves_to_the_fact_bank(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self.assertEqual(cv_path(home, MASTER_CV_ID), home / "resume_facts.yaml")

    def test_saved_cv_is_private_and_listed(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            (home / "resume_facts.yaml").write_text(
                yaml.safe_dump(FACTS), encoding="utf-8"
            )
            save_cv(home, "ml-cv", "ML CV", FACTS)
            self.assertEqual(
                stat.S_IMODE((home / "cv-library" / "ml-cv.yaml").stat().st_mode),
                0o600,
            )
            listed = list_cvs(home)
            self.assertEqual(listed[0]["id"], MASTER_CV_ID)
            self.assertTrue(listed[0]["is_master"])
            self.assertIn("ml-cv", [item["id"] for item in listed])
            self.assertEqual(load_cv(home, "ml-cv")["label"], "ML CV")

    def test_saving_cannot_overwrite_the_master_fact_bank(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            with self.assertRaises(ValueError):
                save_cv(home, MASTER_CV_ID, "Master", FACTS)

    def test_cv_id_cannot_escape_the_library_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            escaped = cv_path(home, "../../etc/passwd")
            self.assertEqual(escaped.parent, (home / "cv-library").resolve())
            self.assertEqual(safe_cv_id("../../etc/passwd"), "etc-passwd")

    def test_drafts_are_scoped_per_cv(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self.assertNotEqual(
                draft_path(home, "job-1", MASTER_CV_ID),
                draft_path(home, "job-1", "ml-cv"),
            )
            # The master keeps its original unsuffixed filename.
            self.assertEqual(
                draft_path(home, "job-1", MASTER_CV_ID),
                draft_path(home, "job-1"),
            )


class PatchSourceTests(unittest.TestCase):
    def setUp(self):
        self.document = master_document(PROFILE, FACTS)

    def _draft(self, source):
        return normalize_draft(
            self.document,
            "job-1",
            {
                "bullets": {
                    "robot": {
                        "id": "robot",
                        "proposal": "Engineered a controller.",
                        "status": "accepted",
                        "source": source,
                    }
                }
            },
        )

    def test_manual_and_ai_patches_stay_distinguishable(self):
        self.assertEqual(self._draft("manual")["bullets"]["robot"]["source"], "manual")
        self.assertEqual(self._draft("ai")["bullets"]["robot"]["source"], "ai")

    def test_unknown_source_is_rejected(self):
        with self.assertRaises(ValueError):
            self._draft("somewhere-else")

    def test_patch_without_source_defaults_to_ai(self):
        draft = normalize_draft(
            self.document,
            "job-1",
            {
                "bullets": {
                    "robot": {"id": "robot", "proposal": "Engineered a controller."}
                }
            },
        )
        self.assertEqual(draft["bullets"]["robot"]["source"], "ai")

    def test_facts_from_document_applies_accepted_patches_only(self):
        draft = normalize_draft(
            self.document,
            "job-1",
            {
                "bullets": {
                    "robot": {
                        "id": "robot",
                        "proposal": "Engineered a controller.",
                        "status": "accepted",
                        "source": "manual",
                    },
                    "vision": {
                        "id": "vision",
                        "proposal": "Should not be applied.",
                        "status": "pending",
                        "source": "ai",
                    },
                }
            },
        )
        facts = facts_from_document(self.document, draft)
        bullets = {
            bullet["id"]: bullet["text"]
            for section in facts["sections"]
            for entry in section["entries"]
            for bullet in entry["bullets"]
        }
        self.assertEqual(bullets["robot"], "Engineered a controller.")
        self.assertEqual(bullets["vision"], "Tested a prototype.")
        # A saved CV must stay reopenable: every fact id survives.
        self.assertEqual(set(bullets), {"robot", "vision"})


if __name__ == "__main__":
    unittest.main()
