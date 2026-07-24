from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ALLOWED_HOST_SUFFIXES = {
    "greenhouse": ("greenhouse.io",),
    "lever": ("lever.co",),
    "ashby": ("ashbyhq.com",),
}

CAPTCHA_SELECTORS = (
    # Invisible score/anchor widgets are routinely preloaded by ATS pages. Only
    # challenge frames/dialogs count as an active block.
    'iframe[src*="recaptcha"][src*="bframe"]',
    'iframe[src*="hcaptcha"][title*="challenge" i]',
    'iframe[src*="challenges.cloudflare.com"][title*="challenge" i]',
    'iframe[title*="recaptcha challenge" i]',
    '[role="dialog"] iframe[src*="captcha"]',
    'input[name*="captcha" i]',
)


def assert_allowed_url(url: str, ats: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme.lower() != "https":
        raise RuntimeError("Refusing browser automation over non-HTTPS transport")
    host = (parsed.hostname or "").lower()
    suffixes = ALLOWED_HOST_SUFFIXES.get(ats, ())
    if not suffixes or not any(host == suffix or host.endswith("." + suffix) for suffix in suffixes):
        raise RuntimeError(f"Refusing browser automation on unapproved host: {host}")


def detect_captcha(page: Any) -> bool:
    for selector in CAPTCHA_SELECTORS:
        locator = page.locator(selector)
        for index in range(locator.count()):
            try:
                if locator.nth(index).is_visible():
                    return True
            except Exception:
                return True
    # ATS pages commonly preload dormant, invisible CAPTCHA frames. The visible
    # selectors above catch an active challenge; a frame URL alone is not proof
    # that the applicant is being challenged.
    try:
        text = page.locator("body").inner_text(timeout=2000)
        if any(
            phrase in text.lower()
            for phrase in ("verify you are human", "complete the captcha", "security check")
        ):
            return True
    except Exception:
        pass
    return False


class BrowserSession:
    def __init__(self, profile_dir: Path, headed: bool = False):
        self.profile_dir = profile_dir
        self.headed = headed
        self._playwright = None
        self.context = None
        self.page = None

    def __enter__(self) -> "BrowserSession":
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError(
                "Playwright is not installed. Run: pip install -r requirements-autoapply.txt"
            ) from exc
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self._playwright = sync_playwright().start()
        self.context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_dir),
            channel="msedge",
            headless=not self.headed,
            viewport={"width": 1365, "height": 900},
        )
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self.page.set_default_timeout(10000)
        return self

    def open(self, url: str, ats: str) -> Any:
        assert_allowed_url(url, ats)
        self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        assert_allowed_url(self.page.url, ats)
        return self.page

    def __exit__(self, *_args: object) -> None:
        if self.context is not None:
            self.context.close()
        if self._playwright is not None:
            self._playwright.stop()
