from .base import BaseAdapter


class LeverAdapter(BaseAdapter):
    ats = "lever"
    form_selectors = (
        "form.application-form",
        'form[action*="/apply"]',
        'form:has(input[name="name"]):has(input[name="email"])',
    )
    submit_selectors = (
        ".application-submit button",
        'button[type="submit"]',
        'input[type="submit"]',
    )

    def prepare(self, page):
        if page.locator("form").count() == 0 and not page.url.rstrip("/").endswith("/apply"):
            page.goto(page.url.rstrip("/") + "/apply", wait_until="domcontentloaded")
        page.locator(
            'form.application-form, form[action*="/apply"], '
            'form:has(input[name="email"])'
        ).first.wait_for(state="visible", timeout=15000)
