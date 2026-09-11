"""Workday adapter.

Workday runs a large share of graduate and internship hiring, PIMCO and G-Research
among the postings this pipeline already tracks, and every one of them was previously
refused at the host allowlist. That was the single biggest coverage gap.

Three things make Workday different from Greenhouse, Lever and Ashby, and all three
are handled here rather than left to the generic path:

1. It is a single-page application. Fields are identified by `data-automation-id`
   rather than by name or label, and querying too early finds nothing because the
   form has not rendered yet.
2. Applying requires an account on that employer's tenant. There is no anonymous
   apply. The persistent browser context means the human signs in once per tenant by
   hand and the session is reused; this adapter never creates an account and never
   types a credential.
3. The apply flow is multi-step, and the button that reads "Next" on step one reads
   "Submit" on the last. Treating every primary button as a submit control would
   click through an application before it was reviewed, so the submit selectors here
   deliberately match only the final control.
"""

from __future__ import annotations

from .base import BaseAdapter


class WorkdayAdapter(BaseAdapter):
    ats = "workday"

    # data-automation-id is Workday's stable hook. Class names are generated and
    # change between tenant versions, so matching on them would break per employer.
    form_selectors = (
        '[data-automation-id="applyManually"]',
        'form[data-automation-id="jobApplicationForm"]',
        '[data-automation-id="jobApplicationPage"]',
        'form:has([data-automation-id="legalNameSection_firstName"])',
        'form:has([data-automation-id="email"])',
        "form",
    )

    # Only the terminal control. "Next" and "Save and Continue" advance the wizard and
    # must not be mistaken for submission: the pipeline treats a click on a submit
    # control as the point of no return.
    submit_selectors = (
        '[data-automation-id="bottom-navigation-next-button"]:has-text("Submit")',
        'button[data-automation-id="wd-CommandButton_uic_okButton"]:has-text("Submit")',
        'button:has-text("Submit Application")',
        'button[aria-label="Submit"]',
    )

    # Steps that are not the application itself. Landing on one of these means the
    # session is not signed in, and stopping with a clear message beats filling a
    # login form.
    auth_markers = (
        '[data-automation-id="signInFormo"]',
        '[data-automation-id="createAccountCheckbox"]',
        '[data-automation-id="signInSubmitButton"]',
        '[data-automation-id="createAccountSubmitButton"]',
    )

    def prepare(self, page) -> None:
        url = page.url.split("?")[0].rstrip("/")

        # A posting URL is not an application URL. Workday exposes the form at
        # /apply/applyManually, and going there directly skips the autofill-with-resume
        # step, which produces a half-populated form that is harder to verify than an
        # empty one.
        if not url.endswith("/applyManually"):
            target = url + "/apply/applyManually" if not url.endswith("/apply") \
                else url + "/applyManually"
            try:
                page.goto(target, wait_until="domcontentloaded", timeout=30000)
            except Exception:
                # Some tenants route differently. Fall back to whatever the posting
                # page offers rather than failing outright.
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                for label in ("Apply Manually", "Apply", "Autofill with Resume"):
                    control = page.get_by_role("button", name=label, exact=False)
                    if control.count():
                        control.first.click()
                        break

        for marker in self.auth_markers:
            if page.locator(marker).count():
                raise RuntimeError(
                    "Workday wants a signed-in account for this employer's tenant "
                    f"({page.url.split('/')[2]}). Workday has no anonymous apply. Sign in "
                    "or create the account yourself in this window, then run this job "
                    "again. Nothing here will type a credential for you."
                )

        # The SPA renders the form after the route settles. Waiting on a field that
        # only exists on the real application avoids matching the shell.
        page.locator(
            '[data-automation-id="legalNameSection_firstName"], '
            '[data-automation-id="email"], '
            '[data-automation-id="applyManually"]'
        ).first.wait_for(state="visible", timeout=25000)

    def native_form_valid(self, page) -> bool:
        """Workday marks required-but-empty fields with an error automation id.

        The generic check looks for HTML5 validity, which a React-controlled input
        reports as valid even when Workday itself considers it incomplete.
        """
        if page.locator('[data-automation-id="errorMessage"]:visible').count():
            return False
        return super().native_form_valid(page)
