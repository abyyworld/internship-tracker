import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import Mock, patch

from autoapply.cv_editor import master_document
from autoapply.openai_tailoring import (
    OPENAI_MODEL_DEFAULT,
    generate_suggestions,
    load_openai_key,
    openai_key_configured,
    save_openai_key,
)
from autoapply.models import Job


class OpenAiTailoringTests(unittest.TestCase):
    def setUp(self):
        self.document = master_document(
            {
                "identity": {"first_name": "Ada", "last_name": "Lovelace"},
                "contact": {"email": "ada@invalid.test"},
            },
            {
                "summary": "Student building verified robotics projects.",
                "skills": ["Python"],
                "education": [],
                "sections": [
                    {
                        "name": "Projects",
                        "entries": [
                            {
                                "title": "Robot",
                                "bullets": [
                                    {
                                        "id": "robot",
                                        "text": (
                                            "Built a Python robot controller and "
                                            "reduced latency by 20%."
                                        ),
                                    },
                                    {
                                        "id": "vision",
                                        "text": (
                                            "Tested a computer vision prototype "
                                            "on recorded images."
                                        ),
                                    },
                                ],
                            }
                        ],
                    }
                ],
            },
        )
        self.job = Job(
            "job",
            "Robot Co",
            "Robotics Intern",
            "https://invalid.test",
            description="Python robotics and computer vision",
        )

    def test_key_is_private_and_stable(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self.assertFalse(openai_key_configured(home))
            save_openai_key(home, "sk-test-key-with-at-least-twenty-characters")
            self.assertEqual(
                load_openai_key(home),
                "sk-test-key-with-at-least-twenty-characters",
            )
            self.assertTrue(openai_key_configured(home))
            self.assertEqual(
                stat.S_IMODE((home / "openai.key").stat().st_mode),
                0o600,
            )

    def test_environment_key_is_used_when_present(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            with patch.dict(
                os.environ,
                {"OPENAI_API_KEY": "sk-env-key-with-at-least-twenty-chars"},
            ):
                self.assertEqual(
                    load_openai_key(home),
                    "sk-env-key-with-at-least-twenty-chars",
                )

    def test_safe_patch_is_returned_and_new_metric_is_discarded(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "summary": None,
                                "bullets": [
                                    {
                                        "fact_id": "robot",
                                        "proposal": (
                                            "Developed a Python robot controller, "
                                            "reducing latency by 20%."
                                        ),
                                        "rationale": "Stronger action verb.",
                                        "keywords": ["Python", "robotics"],
                                    },
                                    {
                                        "fact_id": "vision",
                                        "proposal": (
                                            "Tested a computer vision prototype "
                                            "with 50% higher accuracy."
                                        ),
                                        "rationale": "Unsupported metric.",
                                        "keywords": [],
                                    },
                                ],
                                "advice": ["Keep the application focused."],
                            }
                        )
                    }
                }
            ]
        }
        with patch(
            "autoapply.openai_tailoring.requests.post",
            return_value=response,
        ) as request:
            draft = generate_suggestions(
                self.job,
                self.document,
                api_key="private-api-key",
            )
        self.assertEqual(list(draft["bullets"]), ["robot"])
        self.assertEqual(
            draft["rejected_by_validator"]["vision"],
            "new_numeric_claim",
        )
        sent = request.call_args
        self.assertEqual(
            sent.kwargs["headers"]["Authorization"],
            "Bearer private-api-key",
        )
        self.assertEqual(sent.kwargs["json"]["model"], OPENAI_MODEL_DEFAULT)
        self.assertNotIn("private-api-key", json.dumps(sent.kwargs["json"]))

    def test_endpoint_is_openai(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "summary": None,
                                "bullets": [
                                    {
                                        "fact_id": "robot",
                                        "proposal": (
                                            "Developed a Python robot controller, "
                                            "reducing latency by 20%."
                                        ),
                                        "rationale": "Stronger action verb.",
                                        "keywords": ["Python"],
                                    }
                                ],
                                "advice": [],
                            }
                        )
                    }
                }
            ]
        }
        with patch(
            "autoapply.openai_tailoring.requests.post",
            return_value=response,
        ) as request:
            generate_suggestions(
                self.job,
                self.document,
                api_key="private-api-key",
            )
        self.assertEqual(
            request.call_args.args[0],
            "https://api.openai.com/v1/chat/completions",
        )

    def test_empty_model_response_is_rejected(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {"summary": None, "bullets": [], "advice": []}
                        )
                    }
                }
            ]
        }
        with patch(
            "autoapply.openai_tailoring.requests.post",
            return_value=response,
        ):
            with self.assertRaises(RuntimeError):
                generate_suggestions(
                    self.job,
                    self.document,
                    api_key="private-api-key",
                )


if __name__ == "__main__":
    unittest.main()
