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


class ProviderEndpointTests(unittest.TestCase):
    """Any OpenAI-compatible endpoint, including one on this machine."""

    def setUp(self):
        from autoapply.openai_tailoring import PROVIDERS

        self.providers = PROVIDERS

    def test_every_provider_is_https_or_loopback(self):
        from urllib.parse import urlparse

        for key, provider in self.providers.items():
            parsed = urlparse(provider["base"])
            if parsed.scheme == "http":
                self.assertIn(parsed.hostname, {"127.0.0.1", "localhost"}, key)
            else:
                self.assertEqual(parsed.scheme, "https", key)

    def test_a_remote_endpoint_must_be_https(self):
        from autoapply.openai_tailoring import save_base_url

        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                save_base_url(Path(directory), "http://example.invalid/v1")

    def test_a_local_endpoint_is_allowed_and_needs_no_key(self):
        from autoapply.openai_tailoring import (
            is_local,
            load_key_for,
            openai_key_configured,
            save_base_url,
        )

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            url = save_base_url(home, "http://127.0.0.1:11434/v1")
            self.assertTrue(is_local(url))
            self.assertEqual(load_key_for(home), "")
            # A local runtime has no account, so it counts as configured.
            self.assertTrue(openai_key_configured(home))

    def test_the_endpoint_file_is_private(self):
        from autoapply.openai_tailoring import base_url_path, save_base_url

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_base_url(home, "https://api.groq.com/openai/v1")
            self.assertEqual(
                stat.S_IMODE(base_url_path(home).stat().st_mode), 0o600
            )

    def test_the_default_endpoint_is_openai(self):
        from autoapply.openai_tailoring import OPENAI_BASE_DEFAULT, load_base_url

        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_base_url(Path(directory)), OPENAI_BASE_DEFAULT)

    def test_a_provider_without_a_model_listing_is_seeded(self):
        from autoapply.openai_tailoring import PROVIDERS, models_for

        gemini = PROVIDERS["gemini"]
        self.assertTrue(gemini["models"])
        with patch(
            "autoapply.openai_tailoring.available_models",
            side_effect=RuntimeError("no listing"),
        ):
            self.assertEqual(models_for(gemini["base"], "k"), gemini["models"])

    def test_the_request_goes_to_the_configured_endpoint(self):
        from autoapply.openai_tailoring import _ask_once

        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [{"message": {"content": '{"ok":true}'}}]
        }
        with patch(
            "autoapply.openai_tailoring.requests.post", return_value=response
        ) as request:
            _ask_once("s", "u", api_key="", model="m", max_tokens=10, timeout=5,
                      base_url="http://127.0.0.1:11434/v1")
        self.assertEqual(
            request.call_args.args[0],
            "http://127.0.0.1:11434/v1/chat/completions",
        )
        # A local runtime has no account, so no bearer token is sent.
        self.assertNotIn("Authorization", request.call_args.kwargs["headers"])


class ProviderCompatibilityTests(unittest.TestCase):
    """Third-party endpoints accept a different subset of the same API."""

    def _body(self):
        from autoapply.openai_tailoring import _request_body

        return _request_body("s", "u", model="gpt-4o-mini", max_tokens=100)

    def test_an_endpoint_wanting_the_older_token_field_gets_it(self):
        from autoapply.openai_tailoring import _without_rejected

        response = Mock()
        response.json.return_value = {
            "error": {"message": "Unsupported parameter: 'max_completion_tokens'"}
        }
        reduced = _without_rejected(self._body(), response)
        self.assertIn("max_tokens", reduced)
        self.assertNotIn("max_completion_tokens", reduced)
        self.assertEqual(reduced["max_tokens"], 100)

    def test_an_endpoint_without_json_mode_still_gets_a_request(self):
        from autoapply.openai_tailoring import _without_rejected

        response = Mock()
        response.json.return_value = {
            "error": {"message": "'response_format' is not supported"}
        }
        reduced = _without_rejected(self._body(), response)
        self.assertNotIn("response_format", reduced)
        self.assertIn("messages", reduced)

    def test_an_unrelated_error_is_not_papered_over(self):
        from autoapply.openai_tailoring import _without_rejected

        response = Mock()
        response.json.return_value = {"error": {"message": "invalid model"}}
        self.assertIsNone(_without_rejected(self._body(), response))

    def test_fixed_temperature_models_do_not_send_one(self):
        from autoapply.openai_tailoring import _request_body

        self.assertNotIn(
            "temperature",
            _request_body("s", "u", model="gpt-5.5", max_tokens=10),
        )


class UsageAccountingTests(unittest.TestCase):
    def test_tokens_are_totalled_across_calls(self):
        from autoapply.openai_tailoring import _ask_once, track_usage

        response = Mock()
        response.status_code = 200
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [{"message": {"content": '{"ok":true}'}}],
            "usage": {"prompt_tokens": 120, "completion_tokens": 45},
        }
        with patch("autoapply.openai_tailoring.requests.post", return_value=response):
            with track_usage() as usage:
                for _ in range(3):
                    _ask_once("s", "u", api_key="k", model="m",
                              max_tokens=10, timeout=5)
                counted = usage()
        self.assertEqual(counted, {"input": 360, "output": 135, "calls": 3})

    def test_usage_outside_a_tracked_block_is_not_collected(self):
        from autoapply.openai_tailoring import _ask_once, track_usage

        response = Mock()
        response.status_code = 200
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [{"message": {"content": '{"ok":true}'}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        }
        with patch("autoapply.openai_tailoring.requests.post", return_value=response):
            _ask_once("s", "u", api_key="k", model="m", max_tokens=10, timeout=5)
            with track_usage() as usage:
                counted = usage()
        self.assertEqual(counted["calls"], 0)
