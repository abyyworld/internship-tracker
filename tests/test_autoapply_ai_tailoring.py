import json
import unittest
from unittest.mock import Mock, patch

from autoapply.ai_tailoring import rewrite_with_ollama
from autoapply.models import Job
from autoapply.tailoring import EvidenceLink, TailoredResume


def resume():
    links = [
        EvidenceLink(
            fact_id="robot",
            source_path="sections[0].entries[0].bullets[0]",
            source_ref="",
            text="Built a Python robot controller and reduced latency by 20%.",
            score=10,
            selection_rank=1,
            matched_title_terms=("robotics",),
            matched_description_terms=("python",),
            matched_tags=("robotics",),
        ),
        EvidenceLink(
            fact_id="vision",
            source_path="sections[0].entries[0].bullets[1]",
            source_ref="",
            text="Tested a computer vision prototype on recorded images.",
            score=8,
            selection_rank=2,
            matched_title_terms=("computer-vision",),
            matched_description_terms=(),
            matched_tags=("computer-vision",),
        ),
    ]
    return TailoredResume(
        header={},
        summary="Student building verified robotics projects.",
        skills=["Python"],
        education=[],
        sections=[
            {
                "name": "Projects",
                "entries": [
                    {
                        "title": "Robot",
                        "evidence_ids": ["robot", "vision"],
                        "bullets": [link.text for link in links],
                    }
                ],
            }
        ],
        selected_fact_ids=["robot", "vision"],
        evidence_links=links,
        selection_audit={},
    )


class LocalAiTailoringTests(unittest.TestCase):
    def test_rewrites_safe_bullet_and_rejects_new_metric(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "message": {
                "content": json.dumps(
                    {
                        "summary": "Student building verified robotics projects.",
                        "bullets": {
                            "robot": (
                                "Developed a Python robot controller, reducing "
                                "latency by 20%."
                            ),
                            "vision": (
                                "Tested a computer vision prototype on recorded "
                                "images with 50% higher accuracy."
                            ),
                        },
                    }
                )
            }
        }
        job = Job(
            "job", "Robot Co", "Robotics Intern", "https://invalid.test",
            description="Python robotics and computer vision",
        )
        with patch("autoapply.ai_tailoring.requests.post", return_value=response):
            tailored = rewrite_with_ollama(
                resume(), job, model="qwen3:1.7b"
            )
        bullets = tailored.sections[0]["entries"][0]["bullets"]
        self.assertTrue(bullets[0].startswith("Developed"))
        self.assertEqual(
            bullets[1],
            "Tested a computer vision prototype on recorded images.",
        )
        audit = tailored.selection_audit["ai_rewrite"]
        self.assertEqual(audit["accepted_fact_ids"], ["robot"])
        self.assertEqual(audit["rejected_fact_ids"]["vision"], "new_numeric_claim")
        self.assertEqual(audit["summary"], "accepted")
        self.assertTrue(audit["review_required"])

    def test_private_facts_cannot_be_sent_to_remote_endpoint(self):
        with self.assertRaisesRegex(ValueError, "loopback"):
            rewrite_with_ollama(
                resume(),
                Job("job", "A", "Intern", "https://invalid.test"),
                model="model",
                endpoint="https://example.com",
            )


if __name__ == "__main__":
    unittest.main()
