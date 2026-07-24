import http.client
import json
from pathlib import Path
import stat
import tempfile
import threading
import unittest
from unittest.mock import patch

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
                result = {
                    "resume_path": str(pdf),
                    "resume_hash": "hash",
                    "selected_fact_ids": ["robot"],
                    "tailoring": {"provider": "ollama-local"},
                }
                with patch("autoapply.bridge.prepare", return_value=result):
                    connection = http.client.HTTPConnection("127.0.0.1", port)
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
