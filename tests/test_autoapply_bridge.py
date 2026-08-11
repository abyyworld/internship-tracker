import http.client
import json
from pathlib import Path
import stat
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.parse import quote

from autoapply.bridge import BridgeServer, load_or_create_bridge_token
from autoapply.models import Job
from autoapply.store import Store


class BridgeTests(unittest.TestCase):
    def test_bridge_token_is_private_and_stable(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            token = load_or_create_bridge_token(home)
            self.assertGreaterEqual(len(token), 32)
            self.assertEqual(load_or_create_bridge_token(home), token)
            self.assertEqual(
                stat.S_IMODE((home / "bridge.token").stat().st_mode), 0o600
            )

    def test_clicked_url_generates_one_time_pdf_download(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            generated = home / "generated" / "job"
            generated.mkdir(parents=True)
            pdf = generated / "resume.pdf"
            pdf.write_bytes(b"%PDF-safe-test")
            database = home / "autoapply.sqlite3"
            job = Job(
                "job",
                "Robot Co",
                "Robotics Intern",
                "https://jobs.ashbyhq.com/robot/"
                "12345678-1234-1234-1234-123456789abc",
                ats="ashby",
                external_id="12345678-1234-1234-1234-123456789abc",
                source_status="open",
            )
            with Store(database) as store:
                store.upsert_job(job)
            tracker = home / "tracker.csv"
            tracker.write_text("", encoding="utf-8")
            server = BridgeServer(
                ("127.0.0.1", 0),
                home=home,
                tracker=tracker,
                token="private-test-token-with-more-than-32-characters",
            )
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            port = server.server_address[1]
            try:
                connection = http.client.HTTPConnection("127.0.0.1", port)
                connection.request("GET", "/connect")
                connect_page = connection.getresponse()
                self.assertEqual(connect_page.status, 200)
                self.assertIn(
                    b"autoapply_bridge_token_v1", connect_page.read()
                )
                connection.request(
                    "GET", f"/tailor?url={quote(job.url, safe='')}"
                )
                tailor_page = connection.getresponse()
                self.assertEqual(tailor_page.status, 200)
                self.assertIn(b"Local Qwen CV editor", tailor_page.read())
                result = {
                    "resume_path": str(pdf),
                    "resume_hash": "hash",
                    "selected_fact_ids": ["robot"],
                    "tailoring": {"provider": "ollama-local"},
                }
                with patch("autoapply.bridge.prepare", return_value=result):
                    connection.request(
                        "POST",
                        "/prepare",
                        body=json.dumps({"url": job.url}),
                        headers={
                            "Content-Type": "application/json",
                            "X-Autoapply-Token": server.token,
                        },
                    )
                    response = connection.getresponse()
                    payload = json.loads(response.read())
                    self.assertEqual(response.status, 200)
                    self.assertEqual(
                        payload["application_url"], job.url + "/application"
                    )
                    self.assertEqual(
                        payload["tailoring"]["provider"], "ollama-local"
                    )
                    self.assertEqual(
                        payload["description_source"], ""
                    )
                    path = payload["resume_download_url"].split(str(port), 1)[1]
                    connection.request("GET", path)
                    download = connection.getresponse()
                    self.assertEqual(download.status, 200)
                    self.assertEqual(download.read(), b"%PDF-safe-test")
                    connection.request("GET", path)
                    reused = connection.getresponse()
                    self.assertEqual(reused.status, 404)
                    reused.read()
                    connection.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

    def test_switching_provider_asks_for_that_providers_own_key(self):
        """The failure this covers: choosing Google, then being told the OpenAI
        key already on disk is configured, and getting an authentication error
        from Google on every request."""
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            tracker = home / "tracker.csv"
            tracker.write_text("", encoding="utf-8")
            server = BridgeServer(
                ("127.0.0.1", 0),
                home=home,
                tracker=tracker,
                token="private-test-token-with-more-than-32-characters",
            )
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            port = server.server_address[1]
            connection = http.client.HTTPConnection("127.0.0.1", port)

            def post(path, body):
                connection.request(
                    "POST", path, body=json.dumps(body),
                    headers={
                        "Content-Type": "application/json",
                        "X-Autoapply-Token": server.token,
                    },
                )
                response = connection.getresponse()
                return response.status, json.loads(response.read())

            try:
                # An OpenAI key is already saved, as it would be for anyone who
                # used the editor before switching provider.
                status, _ = post(
                    "/api/settings/key",
                    {"api_key": "sk-test-key-with-at-least-twenty-characters"},
                )
                self.assertEqual(status, 200)
                # No key means the endpoint cannot be asked for a model list.
                with patch(
                    "autoapply.openai_tailoring.available_models",
                    side_effect=RuntimeError("no listing without a key"),
                ):
                    status, switched = post("/api/settings/endpoint", {
                        "base_url":
                            "https://generativelanguage.googleapis.com/v1beta/openai",
                    })
                self.assertEqual(status, 200)
                self.assertEqual(switched["provider"]["id"], "gemini")
                self.assertEqual(switched["provider"]["label"], "Google AI Studio")
                self.assertFalse(switched["provider"]["configured"])
                self.assertEqual(switched["provider"]["key_hint"], "AIza…")
                # The provider's own recommendations still fill the picker.
                self.assertEqual(switched["models"][0], "gemini-2.5-flash")

                status, refused = post(
                    "/api/settings/key",
                    {"api_key": "sk-test-key-with-at-least-twenty-characters"},
                )
                self.assertEqual(status, 422)
                self.assertIn("OpenAI", refused["error"])
                self.assertIn("Google AI Studio", refused["error"])

                with patch(
                    "autoapply.openai_tailoring.available_models",
                    side_effect=RuntimeError("no listing in a test"),
                ):
                    status, saved = post(
                        "/api/settings/key",
                        {"api_key": "AIzaSyDummyGoogleKeyForTests-000000000"},
                    )
                self.assertEqual(status, 200)
                self.assertTrue(saved["provider"]["configured"])
                # Saving the key is what the model picker was waiting for.
                self.assertEqual(saved["models"][0], "gemini-2.5-flash")
                self.assertEqual(
                    (home / "gemini.key").read_text(encoding="utf-8").strip(),
                    "AIzaSyDummyGoogleKeyForTests-000000000",
                )
                self.assertEqual(
                    stat.S_IMODE((home / "gemini.key").stat().st_mode), 0o600
                )
                # The OpenAI key is neither overwritten nor sent to Google.
                self.assertTrue((home / "openai.key").exists())

                # A model named the way this provider lists it stays usable.
                status, model = post(
                    "/api/settings/model", {"model": "models/gemini-2.5-flash"}
                )
                self.assertEqual(status, 200)
                self.assertEqual(model["model"], "gemini-2.5-flash")
                connection.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

    def test_userscript_uses_private_local_bridge_then_opens_apply_page(self):
        script = Path("github-cv-apply.user.js").read_text(encoding="utf-8")
        self.assertIn("@connect      127.0.0.1", script)
        self.assertIn("X-Autoapply-Token", script)
        self.assertIn("GM_download", script)
        self.assertIn("Generate CV + Apply", script)
        self.assertIn("abyyworld.github.io/internship-tracker", script)
        self.assertIn("data-autoapply-dashboard", script)
        self.assertNotIn("submit(", script)


if __name__ == "__main__":
    unittest.main()
