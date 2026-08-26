"""Nothing in this repository may be a credential.

This is a public repository that exists to help people apply for jobs with
their own API keys. The keys live in two places by design — a mode-0600 file
under private/ on the machine running the helper, and this browser's own
storage for the studio — and neither is here. That is a property somebody has
to keep true on every commit, so it is checked on every commit rather than
remembered.

What it scans is exactly what the public can read: the files git is tracking.
The patterns are the shapes real credentials have, written tightly enough that
a job-board URL cannot match one — the earlier version of this check flagged
"...Risk-Analytics-and-Decision-Sciences--RADS-PhD..." because "sk-" appears
inside "Risk-".
"""

from pathlib import Path
import re
import secrets
import subprocess
import unittest


ROOT = Path(__file__).resolve().parent.parent

# Each pattern is anchored so the prefix cannot be the tail of an ordinary
# word, and the body excludes the hyphen wherever the real credential does —
# which is what keeps hyphenated URLs and job titles out of the results.
CREDENTIALS = {
    "OpenAI key": r"(?<![A-Za-z0-9])sk-(?:proj-)?[A-Za-z0-9_]{24,}",
    "OpenRouter key": r"(?<![A-Za-z0-9])sk-or-v1-[A-Za-z0-9]{24,}",
    "Anthropic key": r"(?<![A-Za-z0-9])sk-ant-[A-Za-z0-9_-]{24,}",
    "Google AI Studio key": r"(?<![A-Za-z0-9])AIza[A-Za-z0-9_-]{30,}",
    "Groq key": r"(?<![A-Za-z0-9])gsk_[A-Za-z0-9]{40,}",
    "GitHub token": r"(?<![A-Za-z0-9])gh[posru]_[A-Za-z0-9]{30,}",
    "GitHub fine-grained token": r"(?<![A-Za-z0-9])github_pat_[A-Za-z0-9_]{50,}",
    "AWS access key id": r"(?<![A-Za-z0-9])AKIA[A-Z0-9]{16}(?![A-Za-z0-9])",
    "Slack token": r"(?<![A-Za-z0-9])xox[baprs]-[A-Za-z0-9-]{20,}",
    "private key file": r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----",
}

# The bridge's bearer token is secrets.token_urlsafe(32) — no vendor prefix, so
# nothing above could ever match it, which is exactly how a credential gets
# past a scanner. What gives that kind away is not its shape but the name it is
# assigned to, so the name is what is looked for.
OPAQUE_SECRET = re.compile(
    r"(?i)[a-z0-9_]*(?:token|secret|passwd|password|bearer|credential|api_?key)"
    r"\"?\s*[:=]\s*\"?([A-Za-z0-9_\-]{32,})"
)

# Files whose whole purpose is to describe the shape of a key. A placeholder
# has to be recognisable as one, so these are allowed to talk about prefixes.
DOCUMENTATION = {"tests/test_no_secrets.py"}

# A test needs something key-shaped to pass to the code under test, and that
# is not a leak — but "it is in a test file" is the wrong exemption, because a
# real key pasted into a test is exactly as public as one pasted anywhere
# else. What makes a fixture safe is that it says so, or that it has no
# entropy: no issued credential is a run of zeros.
INVENTED_WORDS = ("dummy", "example", "sample", "fake", "test", "placeholder",
                  "redacted", "notreal", "changeme", "yourkey", "xxxx")


def looks_invented(value: str) -> bool:
    lowered = value.lower()
    if any(word in lowered for word in INVENTED_WORDS):
        return True
    if re.search(r"(.)\1{7,}", value):          # 00000000, aaaaaaaa
        return True
    body = re.sub(r"^[A-Za-z_]+[-_]?(?:v1-|proj-)?", "", value)
    return len(set(body)) < 8                    # too few distinct characters


def _is_a_name(value: str) -> bool:
    """A long identifier is not a credential: no issued token spells words."""
    return bool(re.fullmatch(r"[a-z][a-z0-9]*(?:[_-][a-z0-9]+)+", value))


def tracked_files() -> list[str]:
    """What the public can read: everything git is tracking, and nothing else."""
    listed = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    return [name for name in listed.stdout.split("\0") if name]


class NoCredentialIsPublished(unittest.TestCase):
    def test_no_tracked_file_contains_anything_shaped_like_a_key(self):
        found = []
        for name in tracked_files():
            if name in DOCUMENTATION:
                continue
            path = ROOT / name
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:                      # unreadable is not a leak
                continue
            for label, pattern in CREDENTIALS.items():
                match = re.search(pattern, text)
                if not match:
                    continue
                if looks_invented(match.group(0)):
                    continue
                line = text[:match.start()].count("\n") + 1
                found.append(f"{name}:{line} looks like a {label}: "
                             f"{match.group(0)[:12]}…")
        self.assertEqual(found, [], "a credential appears to be committed:\n"
                                    + "\n".join(found))

    def test_no_tracked_file_assigns_an_opaque_secret(self):
        """The kind of credential no prefix can find.

        The bridge writes secrets.token_urlsafe(32) and every route trusts it.
        It looks like nothing in particular, so the only handle on it is the
        name it is written under.
        """
        found = []
        for name in tracked_files():
            if name in DOCUMENTATION:
                continue
            path = ROOT / name
            if not path.is_file() or path.suffix in {".csv", ".html", ".json"}:
                continue                         # data files, not source
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for match in OPAQUE_SECRET.finditer(text):
                value = match.group(1)
                if looks_invented(value) or _is_a_name(value):
                    continue
                line = text[:match.start()].count("\n") + 1
                found.append(f"{name}:{line} assigns {value[:10]}… to a secret")
        self.assertEqual(found, [], "an opaque secret appears to be committed:\n"
                                    + "\n".join(found))

    def test_the_private_directory_is_not_tracked(self):
        # The helper writes every provider's key, the fact bank and generated
        # CVs here. One `git add -A` from the repository root is all it would
        # take, so the ignore rule is the thing standing between a key and the
        # internet — and it is checked, not assumed.
        offenders = [name for name in tracked_files()
                     if name.startswith("private/") or name.startswith(".private/")
                     or name.endswith(".key") or name.endswith(".token")
                     or name == ".env"
                     or name.endswith("/.env") or name.endswith(".pem")
                     or name.endswith(".p12") or name.endswith(".sqlite3")]
        self.assertEqual(offenders, [], f"these should never be tracked: {offenders}")

    def test_the_ignore_rules_that_hold_that_true_are_still_there(self):
        ignored = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for rule in ("private/", "*.key", "*.token", "*.sqlite3"):
            self.assertIn(rule, ignored, f".gitignore no longer protects {rule}")

    def test_a_key_would_actually_be_caught(self):
        """The check is worth having only if it fires on the real shapes.

        Invented strings of the right form — none of these is a key, and none
        of them has ever been one.
        """
        samples = [
            "sk-" + "A1b2C3d4E5f6G7h8I9j0K1l2",
            "sk-or-v1-" + "0a1b2c3d4e5f60718293a4b5",
            "AIza" + "SyA0b1c2d3e4f5g6h7i8j9k0l1m2n3o4p5q",
            "gsk_" + "0123456789abcdef0123456789abcdef01234567",
            "ghp_" + "0123456789abcdef0123456789abcdef0123",
            "AKIA" + "ABCDEFGHIJKLMNOP",
        ]
        for sample in samples:
            self.assertTrue(
                any(re.search(pattern, sample) for pattern in CREDENTIALS.values()),
                f"nothing would catch {sample[:10]}…")

    def test_a_bridge_token_would_be_caught(self):
        """The case the prefix patterns cannot see.

        secrets.token_urlsafe(32) is what the bridge writes, and every route
        trusts it. It has no prefix, so only the name it is assigned to gives
        it away — and a value with real entropy must not be waved through as a
        fixture.
        """
        issued = secrets.token_urlsafe(32)
        for line in (f'BRIDGE_TOKEN = "{issued}"',
                     f'bridge_token: {issued}',
                     f'"authToken": "{issued}"',
                     f'api_key={issued}'):
            match = OPAQUE_SECRET.search(line)
            self.assertIsNotNone(match, f"nothing would catch {line[:20]}…")
            self.assertFalse(looks_invented(match.group(1)))
            self.assertFalse(_is_a_name(match.group(1)))

    def test_ordinary_code_is_not_an_opaque_secret(self):
        for line in ('max_tokens: 2000,',
                     'token = tokenize(line)',
                     'SECRET_HEADER = "x-autoapply-approval-token"',
                     'password_field = "the_one_labelled_password_on_the_form"',
                     'api_key = os.environ.get("OPENAI_API_KEY", "")'):
            match = OPAQUE_SECRET.search(line)
            if match is None:
                continue
            self.assertTrue(looks_invented(match.group(1)) or _is_a_name(match.group(1)),
                            f"{line} reads as a committed secret")

    def test_a_fixture_is_told_apart_from_a_credential(self):
        # The test suite has to hand key-shaped strings to the code under
        # test. Those are safe because they say what they are, or because
        # nothing issued looks like that.
        for invented in ["AIzaSyDummyGoogleKeyForTests-000000000",
                         "sk-or-v1-0000000000000000000000000000",
                         "sk-example-key-for-the-readme-000000",
                         "ghp_testtesttesttesttesttesttesttest"]:
            self.assertTrue(looks_invented(invented), f"{invented} reads as real")
        # And one with the entropy of an issued key does not get the benefit.
        for real_shaped in ["AIzaSyB7q2XmR9pL4vN0kT8sD3fH6jW1cZ5aY2e",
                            "sk-or-v1-9f3a7c1e5b8d2046a1c9e7f30b5d8264"]:
            self.assertFalse(looks_invented(real_shaped),
                             f"{real_shaped[:12]}… would be waved through")

    def test_what_a_job_board_url_looks_like_is_not_a_key(self):
        """The false positives that made the first version of this useless."""
        innocent = [
            "https://wd1.myworkdaysite.com/recruiting/wf/Jobs/job/CHARLOTTE-NC/"
            "XMLNAME-2027-Quantitative-Analytics-Summer-Internship-Risk-Analytics-"
            "and-Decision-Sciences--RADS-PhD----Early-Careers_R-569912",
            "Paste your key (AIza…)",           # the placeholder the studio shows
            "sk-…",                              # and the one in its provider table
            "gsk_…",
            "Risk-Management-Graduate-Intern---Quantitative-Summer-2027_JR17553",
        ]
        for text in innocent:
            hits = [label for label, pattern in CREDENTIALS.items() if re.search(pattern, text)]
            self.assertEqual(hits, [], f"{hits} matched something innocent: {text[:60]}")


if __name__ == "__main__":
    unittest.main()
