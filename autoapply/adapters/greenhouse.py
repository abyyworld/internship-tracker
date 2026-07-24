from .base import BaseAdapter


class GreenhouseAdapter(BaseAdapter):
    ats = "greenhouse"
    form_selectors = (
        "form#application_form",
        'form[action*="/applications"]',
        'form:has(input[name="first_name"]):has(input[type="email"])',
        "form",
    )
    submit_selectors = (
        "#submit_app",
        'button[type="submit"]',
        'input[type="submit"]',
    )
