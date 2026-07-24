from .base import BaseAdapter


class AshbyAdapter(BaseAdapter):
    ats = "ashby"
    form_selectors = (
        '#form[role="tabpanel"]',
        'form:has(input[name="_systemfield_email"])',
        'form:has(input[type="email"]):has(input[type="file"])',
        "form",
    )
    submit_selectors = (
        'button[type="submit"]',
        'button:has-text("Submit application")',
        'button:has-text("Submit Application")',
    )

    def prepare(self, page):
        if (
            page.locator('#form[role="tabpanel"]').count() == 0
            and not page.url.rstrip("/").endswith("/application")
        ):
            page.goto(page.url.rstrip("/") + "/application", wait_until="domcontentloaded")
        page.locator(
            'input[name="_systemfield_email"], #form[role="tabpanel"] input[type="email"]'
        ).first.wait_for(state="visible", timeout=15000)
