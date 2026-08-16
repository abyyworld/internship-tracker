import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests

from autoapply.cv_editor import master_document
from autoapply.openai_tailoring import (
    OPENAI_MODEL_DEFAULT,
    generate_suggestions,
    key_configured,
    load_key,
    save_key,
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
            self.assertFalse(key_configured(home))
            save_key(home, "sk-test-key-with-at-least-twenty-characters")
            self.assertEqual(
                load_key(home),
                "sk-test-key-with-at-least-twenty-characters",
            )
            self.assertTrue(key_configured(home))
            self.assertEqual(
                stat.S_IMODE((home / "openai.key").stat().st_mode),
                0o600,
            )

    def test_environment_key_is_used_when_no_file_is_saved(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            with patch.dict(
                os.environ,
                {"OPENAI_API_KEY": "sk-env-key-with-at-least-twenty-chars"},
            ):
                self.assertEqual(
                    load_key(home),
                    "sk-env-key-with-at-least-twenty-chars",
                )

    def test_the_pasted_key_outranks_the_environment(self):
        # The key in the editor is the one the applicant chose; a variable left
        # in the shell is a fallback for a run with no file at all.
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_key(home, "sk-pasted-key-with-at-least-twenty-chars")
            with patch.dict(
                os.environ,
                {"OPENAI_API_KEY": "sk-env-key-with-at-least-twenty-chars"},
            ):
                self.assertEqual(
                    load_key(home), "sk-pasted-key-with-at-least-twenty-chars"
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

    def _draft_from(self, payload):
        """Run the whole pipeline against one canned model response."""
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [{"message": {"content": json.dumps(payload)}}]
        }
        with patch("autoapply.openai_tailoring.requests.post", return_value=response):
            return generate_suggestions(
                self.job, self.document, api_key="private-api-key"
            )

    def test_an_invented_employer_is_rejected_end_to_end(self):
        """The CV names no employer. A rewrite may not introduce one."""
        draft = self._draft_from({
            "bullets": [
                {
                    "fact_id": "robot",
                    "proposal": (
                        "Neuralink internship: built a Python robot controller "
                        "and reduced latency by 20%."
                    ),
                    "rationale": "Leads with the employer.",
                },
                {
                    "fact_id": "vision",
                    "proposal": (
                        "Evaluated a computer vision prototype on recorded images."
                    ),
                    "rationale": "Stronger verb.",
                },
            ],
        })
        self.assertNotIn("robot", draft["bullets"])
        self.assertEqual(
            draft["rejected_by_validator"]["robot"],
            "new_named_technology_or_entity",
        )

    def test_a_metric_from_another_entry_is_rejected_end_to_end(self):
        """20% was earned by the robot entry, not by the essay entry."""
        self.document["sections"].append({
            "id": "s1",
            "name": "Writing",
            "layout": "entries",
            "entries": [{
                "id": "s1e0",
                "title": "Essay",
                "organization": "",
                "bullets": [{
                    "id": "essay",
                    "text": "Wrote an essay on autonomous systems for a seminar.",
                }],
            }],
        })
        draft = self._draft_from({
            "bullets": [
                {
                    "fact_id": "essay",
                    "proposal": (
                        "Wrote an essay on autonomous systems for a seminar, "
                        "cutting latency by 20%."
                    ),
                    "rationale": "Borrows another entry's number.",
                },
                {
                    "fact_id": "robot",
                    "proposal": (
                        "Developed a Python robot controller, reducing latency "
                        "by 20%."
                    ),
                    "rationale": "Stronger verb.",
                },
            ],
        })
        self.assertEqual(
            draft["rejected_by_validator"]["essay"], "new_numeric_claim"
        )
        self.assertIn("robot", draft["bullets"])

    def test_a_metric_may_be_restated_within_the_entry_that_earned_it(self):
        """Sibling lines describe one piece of work and share its evidence."""
        draft = self._draft_from({
            "bullets": [
                {
                    "fact_id": "vision",
                    "proposal": (
                        "Tested a computer vision prototype on recorded images "
                        "from the same 20% latency work."
                    ),
                    "rationale": "Restates a sibling's number.",
                },
            ],
        })
        self.assertIn("vision", draft["bullets"])

    def test_coverage_is_counted_from_the_cv_not_taken_on_trust(self):
        draft = self._draft_from({
            "keywords": [
                {"term": "Python", "status": "missing", "importance": "high"},
                {"term": "Kubernetes", "status": "covered", "importance": "high"},
                {"term": "computer vision", "status": "missing", "importance": "high"},
                {"term": "excellent team player", "status": "covered",
                 "importance": "low"},
                {"term": "Rust", "status": "covered", "importance": "high"},
            ],
            "bullets": [
                {
                    "fact_id": "robot",
                    "proposal": (
                        "Developed a Python robot controller, reducing latency "
                        "by 20%."
                    ),
                    "rationale": "Stronger verb.",
                },
            ],
        })
        status = {k["term"]: k["status"] for k in draft["keywords"]}
        # The model called Python missing and Kubernetes covered; the CV says
        # the opposite, and the CV is the fact.
        self.assertEqual(status["Python"], "covered")
        self.assertEqual(status["Kubernetes"], "missing")
        self.assertEqual(status["computer vision"], "covered")
        self.assertNotIn("excellent team player", status)
        self.assertEqual(status["Rust"], "missing")
        # The figure is derived from the panel, so the two cannot disagree.
        covered = sum(1 for value in status.values() if value == "covered")
        self.assertEqual(covered, 2)
        # Python and computer vision covered, Kubernetes and Rust missing, all
        # four high importance: (3 + 3) / (3 + 3 + 3 + 3).
        self.assertEqual(draft["match_score"], 50)

    def test_an_unevidenced_requirement_is_reported_as_a_gap(self):
        draft = self._draft_from({
            "keywords": [
                {"term": "Python", "status": "covered", "importance": "high"},
                {"term": "Kubernetes", "status": "missing", "importance": "high"},
                {"term": "computer vision", "status": "covered", "importance": "low"},
                {"term": "Rust", "status": "missing", "importance": "low"},
            ],
            "bullets": [
                {
                    "fact_id": "robot",
                    "proposal": (
                        "Developed a Python robot controller, reducing latency "
                        "by 20%."
                    ),
                    "rationale": "Stronger verb.",
                },
            ],
        })
        self.assertTrue(any("Kubernetes" in gap for gap in draft["gaps"]))
        self.assertTrue(any("Kubernetes" in line for line in draft["advice"]))
        # A gap is never an invitation to invent the evidence.
        self.assertTrue(
            all("only if you have genuinely done it" in gap for gap in draft["gaps"])
        )

    def test_a_rewrite_records_the_screening_terms_it_actually_adds(self):
        draft = self._draft_from({
            "requirements": ["Experience with computer vision and Python"],
            "bullets": [
                {
                    "fact_id": "robot",
                    "proposal": (
                        "Built a Python robot controller for computer vision "
                        "work and reduced latency by 20%."
                    ),
                    "rationale": "Answers the vision requirement.",
                },
            ],
        })
        self.assertEqual(
            draft["bullets"]["robot"]["adds_keywords"], ["computer-vision"]
        )

    def test_a_rationale_that_explains_nothing_is_dropped(self):
        draft = self._draft_from({
            "requirements": ["Experience with computer vision"],
            "bullets": [
                {
                    "fact_id": "robot",
                    "proposal": (
                        "Developed a Python robot controller, reducing latency "
                        "by 20%."
                    ),
                    "rationale": "Stronger action verb and clearer wording.",
                },
                {
                    "fact_id": "vision",
                    "proposal": (
                        "Evaluated a computer vision prototype on recorded images."
                    ),
                    "rationale": "Answers the computer vision requirement.",
                },
            ],
        })
        self.assertEqual(draft["bullets"]["robot"]["rationale"], "")
        self.assertEqual(
            draft["bullets"]["vision"]["rationale"],
            "Answers the computer vision requirement.",
        )

    def test_the_rewrite_prompt_asks_for_a_checkable_rationale(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [{"message": {"content": json.dumps({"bullets": []})}}]
        }
        with patch(
            "autoapply.openai_tailoring.requests.post", return_value=response
        ) as request:
            with self.assertRaises(RuntimeError):
                generate_suggestions(
                    self.job, self.document, api_key="private-api-key"
                )
        prompts = " ".join(
            message["content"]
            for call in request.call_args_list
            for message in call.kwargs["json"]["messages"]
        )
        self.assertIn("RATIONALE", prompts)
        self.assertIn("would be true of any rewrite", prompts)
        self.assertIn("Never suggest claiming something they have not done", prompts)

    def test_an_added_line_is_held_to_the_same_standard_as_a_rewrite(self):
        draft = self._draft_from({
            "requirements": ["Experience with computer vision"],
            "bullets": [],
            "add": [
                {
                    "entry_id": "s0e0",
                    "text": (
                        "Evaluated the computer vision prototype on recorded "
                        "images before integrating it with the controller."
                    ),
                    "rationale": "Makes the entry stronger and clearer.",
                },
            ],
        })
        line = draft["added"]["s0e0"][0]
        # The rationale would be true of any added line, so it is dropped.
        self.assertEqual(line["rationale"], "")
        # What it adds is measured instead.
        self.assertIn("computer-vision", line["adds_keywords"])

    def test_an_added_line_may_not_invent_evidence(self):
        draft = self._draft_from({
            "bullets": [
                {
                    "fact_id": "robot",
                    "proposal": (
                        "Developed a Python robot controller, reducing latency "
                        "by 20%."
                    ),
                    "rationale": "Answers the Python requirement.",
                },
            ],
            "add": [
                {
                    "entry_id": "s0e0",
                    "text": (
                        "Deployed the controller to a fleet of 40 robots "
                        "across three sites for a full season."
                    ),
                    "rationale": "Adds scale.",
                },
            ],
        })
        self.assertEqual(draft["added"], {})
        self.assertEqual(
            draft["rejected_by_validator"]["add:s0e0"], "new_numeric_claim"
        )

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
            key_configured,
            load_key_for,
            save_base_url,
        )

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            url = save_base_url(home, "http://127.0.0.1:11434/v1")
            self.assertTrue(is_local(url))
            self.assertEqual(load_key_for(home), "")
            # A local runtime has no account, so it counts as configured.
            self.assertTrue(key_configured(home))

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


class ProviderKeyTests(unittest.TestCase):
    """A key belongs to the account that issued it, and to no other provider."""

    GOOGLE_KEY = "AIzaSyDummyGoogleKeyForTests-000000000"
    OPENAI_KEY = "sk-test-key-with-at-least-twenty-characters"

    def test_each_provider_keeps_its_own_key(self):
        from autoapply.openai_tailoring import (
            key_configured,
            key_path,
            load_key_for,
            save_base_url,
        )

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_key(home, self.OPENAI_KEY)
            gemini = save_base_url(
                home, "https://generativelanguage.googleapis.com/v1beta/openai"
            )
            # Switching provider must not report the previous provider's key as
            # this one's: it would be sent to Google and rejected.
            self.assertFalse(key_configured(home))
            with self.assertRaises(FileNotFoundError):
                load_key_for(home)
            save_key(home, self.GOOGLE_KEY)
            self.assertEqual(key_path(home, gemini).name, "gemini.key")
            self.assertEqual(load_key_for(home), self.GOOGLE_KEY)
            self.assertEqual(
                stat.S_IMODE(key_path(home, gemini).stat().st_mode), 0o600
            )
            # And the OpenAI key is still there, untouched, for switching back.
            save_base_url(home, "https://api.openai.com/v1")
            self.assertEqual(load_key_for(home), self.OPENAI_KEY)

    def test_an_openai_variable_is_not_sent_to_another_provider(self):
        from autoapply.openai_tailoring import load_key, save_base_url

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_base_url(
                home, "https://generativelanguage.googleapis.com/v1beta/openai"
            )
            with patch.dict(os.environ, {"OPENAI_API_KEY": self.OPENAI_KEY}):
                with self.assertRaises(FileNotFoundError):
                    load_key(home)

    def test_a_provider_reads_its_own_environment_variable(self):
        from autoapply.openai_tailoring import load_key, save_base_url

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_base_url(
                home, "https://generativelanguage.googleapis.com/v1beta/openai"
            )
            with patch.dict(os.environ, {"GEMINI_API_KEY": self.GOOGLE_KEY}):
                self.assertEqual(load_key(home), self.GOOGLE_KEY)

    def test_a_key_belonging_to_another_provider_is_refused_with_both_names(self):
        from autoapply.openai_tailoring import save_base_url

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_base_url(
                home, "https://generativelanguage.googleapis.com/v1beta/openai"
            )
            with self.assertRaises(ValueError) as caught:
                save_key(home, self.OPENAI_KEY)
            self.assertIn("OpenAI", str(caught.exception))
            self.assertIn("Google AI Studio", str(caught.exception))

    def test_an_openrouter_key_is_not_mistaken_for_an_openai_one(self):
        from autoapply.openai_tailoring import load_key_for, save_base_url

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_base_url(home, "https://openrouter.ai/api/v1")
            # OpenRouter's keys are `sk-or-...`, which is also a valid `sk-`.
            save_key(home, "sk-or-v1-0000000000000000000000000000")
            self.assertEqual(
                load_key_for(home), "sk-or-v1-0000000000000000000000000000"
            )

    def test_an_endpoint_of_your_own_gets_a_file_of_its_own(self):
        from autoapply.openai_tailoring import key_path

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self.assertEqual(
                key_path(home, "https://llm.example.test/v1").name,
                "custom-llm-example-test.key",
            )

    def test_a_key_saved_under_the_old_shared_name_is_filed_by_its_prefix(self):
        from autoapply.openai_tailoring import (
            load_key_for, migrate_legacy_key, save_base_url
        )

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            # What the editor wrote when every provider shared one file.
            (home / "openai.key").write_text(self.GOOGLE_KEY + "\n", encoding="utf-8")
            (home / "openai.key").chmod(0o600)
            self.assertEqual(migrate_legacy_key(home), "gemini")
            self.assertFalse((home / "openai.key").exists())
            save_base_url(
                home, "https://generativelanguage.googleapis.com/v1beta/openai"
            )
            self.assertEqual(load_key_for(home), self.GOOGLE_KEY)

    def test_an_openai_key_under_its_own_name_is_left_alone(self):
        from autoapply.openai_tailoring import load_key_for, migrate_legacy_key

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_key(home, self.OPENAI_KEY)
            self.assertEqual(migrate_legacy_key(home), "")
            self.assertEqual(load_key_for(home), self.OPENAI_KEY)

    def test_a_migration_never_overwrites_a_key_already_filed(self):
        from autoapply.openai_tailoring import migrate_legacy_key, save_base_url

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            gemini = "https://generativelanguage.googleapis.com/v1beta/openai"
            save_base_url(home, gemini)
            save_key(home, self.GOOGLE_KEY)
            other = "AIzaSyAnotherGoogleKeyForTests-11111111"
            (home / "openai.key").write_text(other + "\n", encoding="utf-8")
            (home / "openai.key").chmod(0o600)
            self.assertEqual(migrate_legacy_key(home), "")
            self.assertEqual(
                (home / "gemini.key").read_text(encoding="utf-8").strip(),
                self.GOOGLE_KEY,
            )

    def test_a_missing_key_names_the_provider_that_needs_one(self):
        from autoapply.openai_tailoring import load_key, save_base_url

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_base_url(home, "https://api.groq.com/openai/v1")
            with self.assertRaises(FileNotFoundError) as caught:
                load_key(home)
            self.assertIn("Groq", str(caught.exception))


class ModelNameTests(unittest.TestCase):
    """A model id is what the endpoint calls it, slashes and suffixes included."""

    def test_a_vendor_qualified_name_survives_being_saved(self):
        from autoapply.openai_tailoring import load_model, save_model

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            for name in (
                "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                "openai/gpt-oss-120b:free",
            ):
                self.assertEqual(save_model(home, name), name)
                self.assertEqual(load_model(home), name)

    def test_googles_listing_prefix_is_stripped(self):
        from autoapply.openai_tailoring import save_model

        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(
                save_model(Path(directory), "models/gemini-2.5-flash"),
                "gemini-2.5-flash",
            )

    def _listing(self, ids):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"data": [{"id": name} for name in ids]}
        return patch(
            "autoapply.openai_tailoring.requests.get", return_value=response
        )

    def test_a_discovered_google_model_is_offered_as_the_chat_api_spells_it(self):
        from autoapply.openai_tailoring import PROVIDERS, models_for

        with self._listing([
            "models/gemini-2.0-flash",
            "models/gemini-2.5-flash",
            "models/gemini-embedding-001",
        ]):
            offered = models_for(PROVIDERS["gemini"]["base"], "AIza-key")
        self.assertIn("gemini-2.5-flash", offered)
        self.assertNotIn("models/gemini-2.5-flash", offered)
        # An embedding model cannot answer a chat request.
        self.assertNotIn("gemini-embedding-001", offered)

    def test_the_recommendation_is_the_providers_own_order(self):
        from autoapply.openai_tailoring import PROVIDERS, models_for

        with self._listing([
            "models/gemini-2.0-flash",
            "models/gemini-2.5-pro",
            "models/gemini-2.5-flash",
        ]):
            offered = models_for(PROVIDERS["gemini"]["base"], "AIza-key")
        # Ranked by OpenAI's model names, the picker recommended whichever
        # Gemini happened to sort first.
        self.assertEqual(offered[0], "gemini-2.5-flash")


class ModelBelongsToItsProviderTests(unittest.TestCase):
    """A model id is only meaningful to the endpoint that serves it."""

    GEMINI = "https://generativelanguage.googleapis.com/v1beta/openai"

    def test_each_provider_remembers_its_own_model(self):
        from autoapply.openai_tailoring import (
            load_model, model_path, save_base_url, save_model
        )

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_model(home, "gpt-4o-mini")
            self.assertEqual(model_path(home).name, "openai-model.txt")
            save_base_url(home, self.GEMINI)
            # Not the OpenAI model, and not an OpenAI default either.
            self.assertEqual(load_model(home), "gemini-2.5-flash")
            save_model(home, "gemini-2.5-flash-lite")
            self.assertEqual(model_path(home).name, "gemini-model.txt")
            save_base_url(home, "https://api.openai.com/v1")
            self.assertEqual(load_model(home), "gpt-4o-mini")
            save_base_url(home, self.GEMINI)
            self.assertEqual(load_model(home), "gemini-2.5-flash-lite")

    def test_an_endpoint_with_no_choice_gets_its_own_default(self):
        from autoapply.openai_tailoring import (
            OPENAI_MODEL_DEFAULT, default_model, load_model, save_base_url
        )

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_base_url(home, self.GEMINI)
            # Falling back to an OpenAI id is how a Google endpoint was asked
            # for gpt-5.4 and answered with a bad request.
            self.assertEqual(load_model(home), "gemini-2.5-flash")
            self.assertEqual(default_model("https://llm.example.test/v1"),
                             OPENAI_MODEL_DEFAULT)

    def test_a_model_from_the_shared_era_is_refiled(self):
        from autoapply.openai_tailoring import (
            load_model, migrate_legacy_model, model_path, save_base_url
        )

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            # What the single-file era left behind: a Gemini id under OpenAI's
            # name, which OpenAI answers with a bad request.
            (home / "openai-model.txt").write_text("gemini-2.5-flash\n", encoding="utf-8")
            self.assertEqual(migrate_legacy_model(home), "gemini")
            self.assertFalse((home / "openai-model.txt").exists())
            save_base_url(home, self.GEMINI)
            self.assertEqual(load_model(home), "gemini-2.5-flash")
            self.assertEqual(model_path(home).name, "gemini-model.txt")

    def test_an_openai_model_is_left_where_it_is(self):
        from autoapply.openai_tailoring import migrate_legacy_model, save_model

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            save_model(home, "gpt-4o-mini")
            self.assertEqual(migrate_legacy_model(home), "")
            self.assertTrue((home / "openai-model.txt").exists())

    def test_a_model_the_endpoint_does_not_offer_is_refused(self):
        from autoapply.openai_tailoring import save_model

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            with self.assertRaises(ValueError) as caught:
                save_model(home, "gemini-2.5-flash", offered=["gpt-4o", "gpt-4o-mini"])
            self.assertIn("does not offer", str(caught.exception))
            # Nothing to compare against means anything is allowed: a keyless or
            # custom endpoint must still be configurable.
            self.assertEqual(save_model(home, "gpt-4o", offered=[]), "gpt-4o")


class ProviderProbeTests(unittest.TestCase):
    """One cheap round trip, reported exactly as it came back."""

    def test_a_working_endpoint_is_reported_as_working(self):
        from autoapply.openai_tailoring import probe

        answer = Mock(status_code=200, ok=True)
        answer.json.return_value = {"choices": [{"message": {"content": "{}"}}]}
        listing = Mock(status_code=200, ok=True)
        listing.json.return_value = {"data": [{"id": "gpt-4o"}, {"id": "gpt-4o-mini"}]}
        with patch("autoapply.openai_tailoring.requests.post", return_value=answer):
            with patch("autoapply.openai_tailoring.requests.get", return_value=listing):
                report = probe("https://api.openai.com/v1", "sk-key", "gpt-4o")
        self.assertTrue(report["ok"])
        self.assertEqual(report["status"], 200)
        self.assertEqual(report["provider"], "OpenAI")
        self.assertIn("gpt-4o", report["models"])
        self.assertEqual(report["problem"], "")

    def test_a_rejected_key_stops_looking_like_a_working_one(self):
        from autoapply.openai_tailoring import PROVIDERS, probe

        refused = Mock(status_code=400, ok=False)
        refused.json.return_value = [
            {"error": {"code": 400, "message": "Please pass a valid API key"}}
        ]
        with patch("autoapply.openai_tailoring.requests.post", return_value=refused):
            with patch("autoapply.openai_tailoring.requests.get", return_value=refused):
                report = probe(PROVIDERS["gemini"]["base"], "sk-wrong", "gemini-2.5-flash")
        self.assertFalse(report["ok"])
        self.assertIn("rejected the API key", report["problem"])
        self.assertEqual(report["detail"], "Please pass a valid API key")
        # A key rejection is not a payload problem, so nothing is stripped.
        self.assertEqual(report["dropped"], [])

    def test_every_refused_parameter_is_named_not_just_the_last(self):
        from autoapply.openai_tailoring import probe

        refusals = []
        for field in ("max_completion_tokens", "reasoning_effort"):
            refused = Mock(status_code=400, ok=False)
            refused.json.return_value = {
                "error": {"message": f'Unknown name "{field}": Cannot find field.'}
            }
            refusals.append(refused)
        accepted = Mock(status_code=200, ok=True)
        accepted.json.return_value = {"choices": [{"message": {"content": "{}"}}]}
        listing = Mock(status_code=200, ok=True)
        listing.json.return_value = {"data": []}
        with patch("autoapply.openai_tailoring.requests.post",
                   side_effect=[*refusals, accepted]):
            with patch("autoapply.openai_tailoring.requests.get", return_value=listing):
                report = probe("https://x.test/v1", "k" * 24, "gemini-2.5-flash")
        self.assertTrue(report["ok"])
        self.assertEqual(
            report["dropped"], ["max_completion_tokens", "reasoning_effort"]
        )

    def test_an_unreachable_endpoint_says_so(self):
        from autoapply.openai_tailoring import probe

        with patch("autoapply.openai_tailoring.requests.post",
                   side_effect=requests.ConnectionError("refused")):
            report = probe("http://127.0.0.1:1/v1", "", "any")
        self.assertFalse(report["ok"])
        self.assertIn("could not be reached", report["problem"])


class EndpointFileTests(unittest.TestCase):
    def test_a_symlinked_endpoint_file_is_refused_rather_than_followed(self):
        from autoapply.openai_tailoring import base_url_path, save_base_url

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            home.mkdir(parents=True, exist_ok=True)
            target = home / "elsewhere.txt"
            target.write_text("https://api.openai.com/v1\n", encoding="utf-8")
            base_url_path(home).symlink_to(target)
            # Saved through the link and refused on load, the endpoint reverted
            # to OpenAI while the editor still showed the provider chosen.
            with self.assertRaises(RuntimeError):
                save_base_url(home, "https://api.groq.com/openai/v1")

    def test_an_ignored_endpoint_file_is_explained(self):
        from autoapply.openai_tailoring import (
            OPENAI_BASE_DEFAULT, base_url_path, endpoint_problem, load_base_url
        )

        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            base_url_path(home).write_text("ftp://nope.test/v1\n", encoding="utf-8")
            self.assertEqual(load_base_url(home), OPENAI_BASE_DEFAULT)
            self.assertIn("not an HTTPS or local address", endpoint_problem(home))

    def test_an_endpoint_with_no_host_is_refused(self):
        from autoapply.openai_tailoring import save_base_url

        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                save_base_url(Path(directory), "https://")


class ChatModelFilterTests(unittest.TestCase):
    """The picker must offer what a chat completion can actually use."""

    def test_instruction_tuned_models_are_kept(self):
        from autoapply.openai_tailoring import is_chat_model

        # These are the free chat models the free providers actually serve.
        for name in (
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            "mistralai/mistral-7b-instruct:free",
            "moonshotai/kimi-k2-instruct-0905",
            "gemini-2.5-flash-lite",
            "openai/gpt-4.1",
        ):
            self.assertTrue(is_chat_model(name), name)

    def test_models_that_cannot_answer_a_chat_call_are_dropped(self):
        from autoapply.openai_tailoring import is_chat_model

        for name in (
            "gemini-embedding-001", "text-embedding-3-large", "whisper-1",
            "dall-e-3", "veo-3.1-generate-preview", "imagen-4.0-generate-001",
            "aqa", "gemini-2.5-flash-live-preview", "tts-1",
            "meta-llama/Llama-Guard-4-12B", "gpt-4o-realtime-preview",
        ):
            self.assertFalse(is_chat_model(name), name)

    def test_the_filter_does_not_depend_on_capitalisation(self):
        from autoapply.openai_tailoring import is_chat_model

        # Matching the raw id let Together's capitalised ids through a filter
        # that removed Groq's identical lowercase ones.
        self.assertEqual(
            is_chat_model("BAAI/bge-large-EN-Embedding"),
            is_chat_model("baai/bge-large-en-embedding"),
        )

    def test_a_filtered_model_can_never_be_recommended(self):
        from autoapply.openai_tailoring import available_models

        listing = Mock(status_code=200, ok=True)
        listing.json.return_value = {"data": [
            {"id": "text-embedding-3-large"}, {"id": "gpt-4o"},
        ]}
        with patch("autoapply.openai_tailoring.requests.get", return_value=listing):
            offered = available_models("k", base_url="https://api.openai.com/v1")
        self.assertEqual(offered, ["gpt-4o"])

    def test_a_catalog_that_answers_with_a_bare_array_is_read(self):
        from autoapply.openai_tailoring import PROVIDERS, available_models, catalog_url

        # GitHub Models serves its catalogue off the account host, as an array.
        self.assertEqual(
            catalog_url(PROVIDERS["github"]["base"]),
            "https://models.github.ai/catalog/models",
        )
        listing = Mock(status_code=200, ok=True)
        listing.json.return_value = [
            {"id": "openai/gpt-4o-mini"}, {"id": "openai/text-embedding-3-small"},
        ]
        with patch("autoapply.openai_tailoring.requests.get", return_value=listing):
            offered = available_models("ghp_x", base_url=PROVIDERS["github"]["base"])
        self.assertEqual(offered, ["openai/gpt-4o-mini"])

    def test_a_vendor_prefixed_thinking_model_is_still_told_not_to_think(self):
        from autoapply.openai_tailoring import _request_body

        # Ids are vendor-qualified on OpenRouter and Together, so a table keyed
        # on the bare family stopped applying exactly where it was needed.
        for model in ("google/gemini-2.5-flash", "google/gemini-2.5-flash:free"):
            self.assertEqual(
                _request_body("s", "u", model=model, max_tokens=10)["reasoning_effort"],
                "none", model,
            )

    def test_a_vendor_prefixed_fixed_temperature_model_sends_no_temperature(self):
        from autoapply.openai_tailoring import _request_body

        self.assertNotIn(
            "temperature",
            _request_body("s", "u", model="openai/gpt-5-mini", max_tokens=10),
        )


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

    def test_a_complaint_naming_no_parameter_still_gets_one_plain_attempt(self):
        from autoapply.openai_tailoring import OPTIONAL_PARAMS, _without_rejected

        # Most 400s name no parameter at all. Rather than report one while still
        # holding a payload the endpoint may not understand, everything optional
        # comes off at once — and then the reduction is finished, so this cannot
        # loop.
        response = Mock()
        response.json.return_value = {"error": {"message": "invalid request"}}
        plain = _without_rejected(self._body(), response)
        for name in OPTIONAL_PARAMS:
            self.assertNotIn(name, plain)
        self.assertIn("messages", plain)
        self.assertEqual(plain["max_tokens"], 100)
        self.assertIsNone(_without_rejected(plain, response))

    def test_a_google_error_array_is_read_rather_than_swallowed(self):
        from autoapply.openai_tailoring import (
            _error_message, _is_auth_error, _without_rejected
        )

        # Google's chat endpoint wraps its error object in a JSON array. Reading
        # `.get` off the list raised, both callers swallowed it, and every Google
        # failure was classified as if the body had been empty.
        response = Mock(status_code=400)
        response.json.return_value = [
            {"error": {"code": 400, "message": "Please pass a valid API key",
                       "status": "INVALID_ARGUMENT"}}
        ]
        self.assertEqual(_error_message(response), "Please pass a valid API key")
        self.assertTrue(_is_auth_error(response))

        from autoapply.openai_tailoring import _request_body

        rejected = Mock(status_code=400)
        rejected.json.return_value = [
            {"error": {"code": 400, "message":
                       'Invalid JSON payload received. Unknown name '
                       '"reasoning_effort": Cannot find field.'}}
        ]
        # A Gemini payload is the one that carries reasoning_effort.
        body = _request_body("s", "u", model="gemini-2.5-flash", max_tokens=100)
        reduced = _without_rejected(body, rejected)
        self.assertNotIn("reasoning_effort", reduced)
        # Only the named parameter comes off: the rest of the payload survives.
        self.assertIn("response_format", reduced)
        self.assertIn("max_completion_tokens", reduced)

    def test_an_error_body_with_no_error_wrapper_is_read(self):
        from autoapply.openai_tailoring import _error_message, _is_auth_error

        # Cerebras and GitHub Models put the message at the top level.
        response = Mock(status_code=401)
        response.json.return_value = {
            "message": "Unauthorized. Access token is missing or invalid.",
            "code": "unauthorized",
        }
        self.assertIn("Unauthorized", _error_message(response))
        self.assertTrue(_is_auth_error(response))

    def test_a_parameter_named_only_in_param_is_still_dropped(self):
        from autoapply.openai_tailoring import _without_rejected

        response = Mock(status_code=400)
        response.json.return_value = {
            "message": "Unsupported value.", "param": "response_format",
        }
        reduced = _without_rejected(self._body(), response)
        self.assertNotIn("response_format", reduced)
        self.assertIn("temperature", reduced)

    def test_the_key_is_never_echoed_back_in_a_message(self):
        from autoapply.openai_tailoring import _error_message

        response = Mock(status_code=400)
        response.json.return_value = {
            "error": {"message": "API key sk-secret-key-000000000000 is invalid"}
        }
        said = _error_message(response, "sk-secret-key-000000000000")
        self.assertNotIn("sk-secret-key-000000000000", said)
        self.assertIn("…", said)

    def test_fixed_temperature_models_do_not_send_one(self):
        from autoapply.openai_tailoring import _request_body

        self.assertNotIn(
            "temperature",
            _request_body("s", "u", model="gpt-5.5", max_tokens=10),
        )

    def test_a_thinking_model_is_told_not_to_spend_the_reply_on_thinking(self):
        from autoapply.openai_tailoring import _request_body

        body = _request_body("s", "u", model="gemini-2.5-flash", max_tokens=2600)
        self.assertEqual(body["reasoning_effort"], "none")

    def test_a_thinking_model_that_cannot_stop_is_asked_to_be_brief(self):
        from autoapply.openai_tailoring import _request_body

        body = _request_body("s", "u", model="gemini-2.5-pro", max_tokens=2600)
        self.assertEqual(body["reasoning_effort"], "low")

    def test_openais_own_reasoning_default_is_left_alone(self):
        from autoapply.openai_tailoring import _request_body

        # The measured quality of this pipeline was measured at OpenAI's
        # default; changing it here would silently invalidate that.
        for model in ("gpt-5.4", "gpt-5.6", "gpt-4o-mini"):
            self.assertNotIn(
                "reasoning_effort",
                _request_body("s", "u", model=model, max_tokens=10),
            )

    def test_a_payload_rejected_twice_is_reduced_twice(self):
        from autoapply.openai_tailoring import PROVIDERS, _ask_once

        # Google reports one unknown field per answer, so a payload it dislikes
        # in two ways needs two reductions to get through.
        rejects = {
            "max_completion_tokens": Mock(status_code=400),
            "reasoning_effort": Mock(status_code=400),
        }
        for name, response in rejects.items():
            response.json.return_value = {
                "error": {"message": f'Unknown name "{name}": Cannot find field.'}
            }
        accepted = Mock(status_code=200)
        accepted.raise_for_status.return_value = None
        accepted.json.return_value = {
            "choices": [{"message": {"content": '{"ok":true}'}}]
        }
        answers = [
            rejects["reasoning_effort"], rejects["max_completion_tokens"], accepted
        ]
        with patch(
            "autoapply.openai_tailoring.requests.post", side_effect=answers
        ) as request:
            self.assertEqual(
                _ask_once(
                    "s", "u", api_key="k", model="gemini-2.5-flash",
                    max_tokens=10, timeout=5,
                    base_url=PROVIDERS["gemini"]["base"],
                ),
                {"ok": True},
            )
        sent = request.call_args.kwargs["json"]
        self.assertNotIn("reasoning_effort", sent)
        self.assertNotIn("max_completion_tokens", sent)
        self.assertEqual(sent["max_tokens"], 10)

    def test_an_error_names_the_provider_actually_being_called(self):
        from autoapply.openai_tailoring import PROVIDERS, _ask_once

        response = Mock()
        response.status_code = 401
        response.json.return_value = {"error": {"message": "bad key"}}
        response.raise_for_status.side_effect = requests.HTTPError(response=response)
        with patch("autoapply.openai_tailoring.requests.post", return_value=response):
            with self.assertRaises(RuntimeError) as caught:
                _ask_once(
                    "s", "u", api_key="k", model="gemini-2.5-flash",
                    max_tokens=10, timeout=5,
                    base_url=PROVIDERS["gemini"]["base"],
                )
        self.assertIn("Google AI Studio", str(caught.exception))
        self.assertNotIn("OpenAI", str(caught.exception))

    def test_a_missing_key_reported_as_a_400_is_still_a_key_problem(self):
        from autoapply.openai_tailoring import PROVIDERS, _ask_once

        # Google answers a missing key with 400, not 401.
        response = Mock()
        response.status_code = 400
        response.json.return_value = {
            "error": {"message": "Missing or invalid Authorization header."}
        }
        response.raise_for_status.side_effect = requests.HTTPError(response=response)
        with patch("autoapply.openai_tailoring.requests.post", return_value=response):
            with self.assertRaises(RuntimeError) as caught:
                _ask_once(
                    "s", "u", api_key="", model="gemini-2.5-flash",
                    max_tokens=10, timeout=5,
                    base_url=PROVIDERS["gemini"]["base"],
                )
        self.assertIn("key", str(caught.exception).lower())

    def test_an_endpoint_rejecting_reasoning_effort_still_gets_a_request(self):
        from autoapply.openai_tailoring import _request_body, _without_rejected

        response = Mock()
        response.json.return_value = {
            "error": {"message": "Unrecognized request argument: reasoning_effort"}
        }
        body = _request_body("s", "u", model="gemini-2.5-flash", max_tokens=10)
        reduced = _without_rejected(body, response)
        self.assertNotIn("reasoning_effort", reduced)
        self.assertIn("messages", reduced)


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
