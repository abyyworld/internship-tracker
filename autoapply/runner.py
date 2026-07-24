from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
from typing import Any

from .adapters import get_adapter
from .browser import BrowserSession, assert_allowed_url, detect_captcha
from .config import facts_path, load_yaml, profile_path, reject_placeholders
from .eligibility import assess_eligibility
from .jobs import fetch_description
from .models import (
    FillAction,
    FillPlan,
    FormField,
    FormSnapshot,
    Job,
    UnresolvedField,
    digest,
    normalize_text,
)
from .policy import build_fill_plan, new_approval_token, token_hash
from .questions import classify
from .resume import file_sha256, render_resume
from .store import Store, TERMINAL_APPLICATION_STATES, now_iso
from .tailoring import tailor_resume


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value)[:80]


APPROVAL_TTL = timedelta(hours=24)


def _fetch_required_description(job: Job) -> str:
    description = (fetch_description(job) or "").strip()
    if not description:
        raise RuntimeError(
            "Could not fetch a non-empty job description; approval is fail-closed"
        )
    return description


def _verify_latest_description(store: Store, job: Job) -> None:
    latest = _fetch_required_description(job)
    if not job.description or normalize_text(latest) != normalize_text(job.description):
        store.update_description(job.id, latest)
        raise RuntimeError(
            "Job description changed or was unavailable during preparation; "
            "prepare, inspect, and approve again"
        )


def _eligibility_fingerprint(job: Job, profile: dict[str, Any], report: Any) -> str:
    education = profile.get("education", {})
    return digest(
        {
            "status": report.status,
            "reasons": list(report.reasons),
            "job": {
                "id": job.id,
                "role": job.role,
                "region": job.region,
                "location": job.location,
                "description_hash": job.description_hash,
            },
            "profile": {
                "citizenships": profile.get("citizenships", []),
                "work_authorization": profile.get("work_authorization", {}),
                "education_level": (
                    education.get("level", "")
                    if isinstance(education, dict)
                    else ""
                ),
            },
        }
    )


def _require_gate_eligibility(job: Job, profile: dict[str, Any]) -> str:
    report = assess_eligibility(job, profile)
    if report.status != "not_blocked":
        detail = "; ".join(report.reasons) or report.status
        raise RuntimeError(
            "Eligibility must be exactly 'not_blocked' before approval or "
            f"submission: {detail}"
        )
    return _eligibility_fingerprint(job, profile, report)


def _document_url(document: Any) -> str:
    value = getattr(document, "url", "")
    return str(value() if callable(value) else value or "")


def _application_view_url(page: Any, target: Any) -> str:
    target_url = _document_url(target)
    if target_url and target_url != "about:blank":
        return target_url
    return _document_url(page)


def _documents(page: Any) -> list[Any]:
    documents = [page]
    documents.extend(
        frame for frame in getattr(page, "frames", []) if frame != page.main_frame
    )
    return documents


def _capture_confirmation_states(
    adapter: Any, page: Any, required_documents: tuple[Any, ...] = ()
) -> dict[int, dict[str, Any] | None]:
    states: dict[int, dict[str, Any] | None] = {}
    for document in _documents(page):
        try:
            states[id(document)] = adapter.confirmation_state(document)
        except Exception:
            states[id(document)] = None
    for document in required_documents:
        if states.get(id(document)) is None:
            raise RuntimeError(
                "Submission confirmation baseline could not be observed; "
                "final click is prohibited"
            )
    return states


def _submission_confirmed(
    adapter: Any,
    page: Any,
    starting_states: dict[int, dict[str, Any] | None],
) -> bool:
    for document in _documents(page):
        identity = id(document)
        if identity in starting_states and starting_states[identity] is None:
            continue
        try:
            if adapter.confirmed(document, starting_states.get(identity)):
                return True
        except Exception:
            continue
    return False


def _field_identity(field: FormField) -> tuple[str, str]:
    return field.key, field.selector


def _action_identity(action: FillAction) -> tuple[str, str]:
    return action.field_key, action.selector


def _is_empty_observed(value: Any) -> bool:
    return value is None or value == "" or value == [] or value is False


def _expected_observed_value(action: FillAction) -> Any:
    if action.kind == "file":
        return [Path(str(action.value)).name]
    if action.kind == "checkbox":
        return action.value
    if action.kind == "checkbox-group":
        return [str(action.value)]
    return str(action.value)


def _observed_value_issues(
    snapshot: FormSnapshot,
    plan: FillPlan,
    *,
    after_fill: bool,
) -> list[tuple[FormField, str]]:
    actions: dict[tuple[str, str], FillAction] = {}
    for action in plan.actions:
        identity = _action_identity(action)
        if identity in actions:
            raise RuntimeError(
                f"Duplicate approved action identity for {action.prompt!r}"
            )
        actions[identity] = action

    seen: set[tuple[str, str]] = set()
    issues: list[tuple[FormField, str]] = []
    for field in snapshot.fields:
        identity = _field_identity(field)
        if identity in seen:
            raise RuntimeError(
                f"Duplicate observable field identity for {field.prompt!r}"
            )
        seen.add(identity)
        action = actions.get(identity)
        observed = field.current_value
        if not field.value_observable:
            issues.append((field, "field_value_could_not_be_observed"))
            continue
        if action is None:
            if not _is_empty_observed(observed):
                issues.append((field, "nonempty_value_was_not_approved"))
            continue
        expected = _expected_observed_value(action)
        if after_fill:
            if observed != expected:
                issues.append((field, "post_fill_value_does_not_match_approval"))
        elif not _is_empty_observed(observed) and observed != expected:
            issues.append((field, "initial_value_does_not_match_approval"))

    missing_actions = set(actions) - seen
    if missing_actions:
        raise RuntimeError("One or more approved fields are no longer observable")
    return issues


def _append_initial_value_blockers(
    snapshot: FormSnapshot, plan: FillPlan
) -> None:
    for field, reason in _observed_value_issues(
        snapshot, plan, after_fill=False
    ):
        plan.unresolved.append(
            UnresolvedField(
                field_key=field.key,
                prompt=field.prompt,
                required=True,
                reason=reason,
                category=classify(field).value,
            )
        )


def _assert_post_fill_invariants(
    approved_plan: FillPlan,
    snapshot: FormSnapshot,
    application_url: str,
    submit_fingerprint: str,
) -> None:
    if snapshot.form_hash != approved_plan.form_hash:
        raise RuntimeError(
            "Form fields or control state changed after filling; final click prohibited"
        )
    if application_url != approved_plan.application_url:
        raise RuntimeError(
            "Application-view URL changed after filling; final click prohibited"
        )
    if submit_fingerprint != approved_plan.submit_fingerprint:
        raise RuntimeError(
            "Visible submit control changed after filling; final click prohibited"
        )
    issues = _observed_value_issues(snapshot, approved_plan, after_fill=True)
    if issues:
        labels = [field.prompt or field.key for field, _reason in issues[:5]]
        raise RuntimeError(
            "Post-fill form contains missing, changed, or unapproved values: "
            + "; ".join(labels)
        )


def _approval_expiry() -> str:
    return (datetime.now(timezone.utc) + APPROVAL_TTL).isoformat(timespec="seconds")


def _approval_is_expired(value: str) -> bool:
    try:
        expires_at = datetime.fromisoformat(value)
        if expires_at.tzinfo is None:
            return True
    except (TypeError, ValueError):
        return True
    return expires_at <= datetime.now(timezone.utc)


def _ensure_not_terminal(store: Store, job_id: str) -> None:
    state = store.application(job_id)["state"]
    if state in TERMINAL_APPLICATION_STATES:
        raise RuntimeError(
            f"Application state is {state!r}; no automatic retry or reset is allowed"
        )


def prepare(store: Store, home: Path, job_id: str) -> dict[str, Any]:
    profile = load_yaml(profile_path(home))
    facts = load_yaml(facts_path(home))
    reject_placeholders(profile)
    reject_placeholders(facts)
    job = store.get_job(job_id)
    _ensure_not_terminal(store, job_id)
    assert_allowed_url(job.url, job.ats)
    description = _fetch_required_description(job)
    if description != job.description:
        store.update_description(job_id, description)
        job.description = description
    eligibility = assess_eligibility(job, profile)
    if eligibility.status == "blocked":
        message = "; ".join(eligibility.reasons)
        store.update_application(job_id, state="eligibility_blocked", last_error=message)
        store.event(job_id, "eligibility_blocked", {"reasons": eligibility.reasons})
        raise RuntimeError(message)
    tailored = tailor_resume(job, profile, facts)
    if not tailored.selected_fact_ids:
        message = (
            "No role-relevant verified evidence matched this job. "
            "Add truthful facts to resume_facts.yaml and review them before retrying."
        )
        store.update_application(job_id, state="needs_evidence", last_error=message)
        store.event(job_id, "needs_evidence", {"reason": message})
        raise RuntimeError(message)
    tailoring_config = profile.get("tailoring", {})
    if tailoring_config.get("provider", "deterministic") == "ollama":
        from .ai_tailoring import rewrite_with_ollama

        tailored = rewrite_with_ollama(
            tailored,
            job,
            model=str(tailoring_config.get("model", "")).strip(),
            endpoint=str(
                tailoring_config.get("endpoint", "http://127.0.0.1:11434")
            ).strip(),
        )
    output = home / "generated" / _safe_name(job_id) / "resume.pdf"
    resume_hash = render_resume(tailored, output)
    store.update_application(
        job_id,
        state="prepared",
        resume_path=str(output),
        resume_hash=resume_hash,
        last_error="",
    )
    result = {
        "job_id": job_id,
        "description_available": bool(job.description),
        "eligibility": eligibility.status,
        "eligibility_notes": eligibility.reasons,
        "resume_path": str(output),
        "resume_hash": resume_hash,
        "selected_fact_ids": tailored.selected_fact_ids,
        "tailoring": tailored.selection_audit.get(
            "ai_rewrite", {"provider": "verified-concept-ranker"}
        ),
    }
    store.event(job_id, "prepared", result)
    return result


def _application_target(page: Any, adapter: Any) -> Any:
    targets = [page, *[frame for frame in page.frames if frame != page.main_frame]]
    matches = []
    for target in targets:
        try:
            adapter.find_form(target)
            matches.append(target)
        except Exception:
            continue
    if len(matches) != 1:
        raise RuntimeError(f"Expected one application document, found {len(matches)}")
    return matches[0]


def _resume_details(store: Store, job_id: str) -> tuple[str, str]:
    application = store.application(job_id)
    path = Path(application.get("resume_path", ""))
    expected = application.get("resume_hash", "")
    if not path.is_file() or not expected:
        raise RuntimeError("Prepared resume is missing; run prepare first")
    actual = file_sha256(path)
    if actual != expected:
        raise RuntimeError("Prepared resume changed after preparation; run prepare again")
    return str(path), actual


def inspect_and_plan(
    store: Store,
    home: Path,
    job_id: str,
    *,
    headed: bool = False,
    execute: bool = False,
) -> FillPlan:
    profile = load_yaml(profile_path(home))
    reject_placeholders(profile)
    job = store.get_job(job_id)
    _ensure_not_terminal(store, job_id)
    assert_allowed_url(job.url, job.ats)
    if job.source_status != "open":
        raise RuntimeError(f"Job source status is {job.source_status!r}, not open")
    if not job.description.strip():
        raise RuntimeError("Prepared job description is empty; run prepare first")
    eligibility = assess_eligibility(job, profile)
    if eligibility.status == "blocked":
        raise RuntimeError("; ".join(eligibility.reasons))
    resume_path, resume_hash = _resume_details(store, job_id)
    adapter = get_adapter(job.ats)
    artifact_dir = home / "artifacts" / _safe_name(job_id)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    with BrowserSession(home / "browser-profile", headed=headed) as browser:
        page = browser.open(job.url, job.ats)
        adapter.prepare(page)
        assert_allowed_url(page.url, job.ats)
        captcha = detect_captcha(page)
        target = _application_target(page, adapter)
        application_url = _application_view_url(page, target)
        assert_allowed_url(application_url, job.ats)
        snapshot = adapter.inspect(target, application_url, captcha)
        plan = build_fill_plan(
            job, snapshot, profile, resume_path=resume_path, resume_hash=resume_hash
        )
        plan.application_url = application_url
        plan.eligibility_hash = _eligibility_fingerprint(job, profile, eligibility)
        plan.initial_state_hash = snapshot.state_hash
        plan.submit_fingerprint = adapter.submit_fingerprint(target)
        _append_initial_value_blockers(snapshot, plan)
        state = "blocked_captcha" if plan.captcha else (
            "needs_review" if plan.blocking else "planned"
        )
        store.save_plan(job_id, plan, state=state)
        if execute:
            if plan.captcha:
                raise RuntimeError("CAPTCHA detected; automation stopped without filling")
            adapter.fill(target, plan)
            screenshot = artifact_dir / "filled.png"
            page.screenshot(path=str(screenshot), full_page=True)
            screenshot.chmod(0o600)
            store.update_application(
                job_id,
                state="filled_needs_review" if plan.blocking else "filled",
            )
            store.event(job_id, "form_filled", {"screenshot": str(screenshot)})
        else:
            store.event(job_id, "dry_run", {"form_hash": plan.form_hash})
        return plan


def approve(store: Store, home: Path, job_id: str) -> tuple[str, str, str]:
    profile = load_yaml(profile_path(home))
    reject_placeholders(profile)
    job = store.get_job(job_id)
    _ensure_not_terminal(store, job_id)
    assert_allowed_url(job.url, job.ats)
    if job.source_status != "open":
        raise RuntimeError(f"Job source status is {job.source_status!r}, not open")
    _verify_latest_description(store, job)
    eligibility_hash = _require_gate_eligibility(job, profile)
    plan = store.load_plan(job_id)
    if plan.job_id != job.id:
        raise RuntimeError("Stored plan belongs to a different job")
    if not plan.application_url:
        raise RuntimeError("Stored plan lacks the actual application-view URL; inspect again")
    if not plan.initial_state_hash:
        raise RuntimeError("Stored plan lacks the inspected form state; inspect again")
    if not plan.submit_fingerprint:
        raise RuntimeError("Stored plan lacks the visible submit control; inspect again")
    assert_allowed_url(plan.application_url, job.ats)
    if plan.eligibility_hash != eligibility_hash:
        raise RuntimeError("Eligibility facts changed after inspection; inspect again")
    if not plan.safe_to_submit:
        reasons = [x.prompt or x.field_key for x in plan.blocking]
        if plan.captcha:
            reasons.append("CAPTCHA detected")
        raise RuntimeError("Cannot approve: " + "; ".join(reasons))
    resume = Path(plan.resume_path)
    if not resume.is_file() or file_sha256(resume) != plan.resume_hash:
        raise RuntimeError("Resume changed or disappeared; prepare and inspect again")
    bound = plan.approval_hash(job)
    token = new_approval_token()
    expires_at = _approval_expiry()
    store.update_application(
        job_id,
        state="approved",
        approval_token_hash=token_hash(token),
        approval_bound_hash=bound,
        approval_expires_at=expires_at,
        approval_used=0,
        last_error="",
    )
    store.event(
        job_id,
        "approved",
        {"approval_bound_hash": bound, "approval_expires_at": expires_at},
    )
    return token, bound, expires_at


def _handle_captcha(page: Any, headed: bool) -> None:
    if not detect_captcha(page):
        return
    if not headed:
        raise RuntimeError("CAPTCHA detected; rerun headed and complete it manually")
    input("CAPTCHA detected. Complete it manually in Edge, then press Enter here: ")
    if detect_captcha(page):
        raise RuntimeError("CAPTCHA is still present; submission stopped")


def submit(
    store: Store,
    home: Path,
    job_id: str,
    approval_token: str,
    *,
    headed: bool = True,
) -> str:
    if not headed:
        raise RuntimeError(
            "Headless final submission is prohibited; rerun with a visible browser"
        )
    profile = load_yaml(profile_path(home))
    reject_placeholders(profile)
    job = store.get_job(job_id)
    assert_allowed_url(job.url, job.ats)
    if job.source_status != "open":
        raise RuntimeError(f"Job source status is {job.source_status!r}, not open")
    _verify_latest_description(store, job)
    eligibility_hash = _require_gate_eligibility(job, profile)
    application = store.application(job_id)
    if application["state"] != "approved" or application["approval_used"]:
        raise RuntimeError("Application does not have an unused approval")
    if _approval_is_expired(application.get("approval_expires_at", "")):
        store.update_application(
            job_id,
            state="approval_expired",
            approval_token_hash="",
            approval_bound_hash="",
            approval_expires_at="",
        )
        raise RuntimeError("Approval expired; inspect and approve again")
    approved_plan = store.load_plan(job_id)
    if approved_plan.eligibility_hash != eligibility_hash:
        raise RuntimeError("Eligibility facts changed after approval")
    if not approved_plan.application_url:
        raise RuntimeError("Approved plan lacks the actual application-view URL")
    if not approved_plan.initial_state_hash:
        raise RuntimeError("Approved plan lacks the inspected form state")
    if not approved_plan.submit_fingerprint:
        raise RuntimeError("Approved plan lacks the visible submit control")
    assert_allowed_url(approved_plan.application_url, job.ats)
    approved_bound = approved_plan.approval_hash(job)
    if approved_bound != application["approval_bound_hash"]:
        raise RuntimeError("Stored application changed after approval")
    if token_hash(approval_token) != application["approval_token_hash"]:
        raise RuntimeError("Approval token is invalid")
    resume_path, resume_hash = _resume_details(store, job_id)
    adapter = get_adapter(job.ats)
    artifact_dir = home / "artifacts" / _safe_name(job_id)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    with BrowserSession(home / "browser-profile", headed=headed) as browser:
        page = browser.open(job.url, job.ats)
        adapter.prepare(page)
        assert_allowed_url(page.url, job.ats)
        _handle_captcha(page, headed)
        target = _application_target(page, adapter)
        application_url = _application_view_url(page, target)
        assert_allowed_url(application_url, job.ats)
        snapshot = adapter.inspect(target, application_url, captcha=False)
        current_plan = build_fill_plan(
            job, snapshot, profile, resume_path=resume_path, resume_hash=resume_hash
        )
        current_plan.application_url = application_url
        current_plan.eligibility_hash = eligibility_hash
        current_plan.initial_state_hash = snapshot.state_hash
        current_plan.submit_fingerprint = adapter.submit_fingerprint(target)
        _append_initial_value_blockers(snapshot, current_plan)
        if not current_plan.safe_to_submit:
            raise RuntimeError(
                "Current form contains CAPTCHA, unresolved fields, or "
                "unapproved prefilled values"
            )
        if current_plan.approval_hash(job) != approved_bound:
            raise RuntimeError("Form, answers, or resume changed; approval is stale")
        adapter.fill(target, current_plan)
        _handle_captcha(page, headed)
        page.wait_for_timeout(300)
        first_post_fill = adapter.inspect(target, application_url, captcha=False)
        first_url = _application_view_url(page, target)
        assert_allowed_url(first_url, job.ats)
        first_submit_fingerprint = adapter.submit_fingerprint(
            target, require_enabled=True
        )
        _assert_post_fill_invariants(
            approved_plan,
            first_post_fill,
            first_url,
            first_submit_fingerprint,
        )
        page.wait_for_timeout(250)
        final_post_fill = adapter.inspect(target, application_url, captcha=False)
        final_url = _application_view_url(page, target)
        assert_allowed_url(final_url, job.ats)
        final_submit_fingerprint = adapter.submit_fingerprint(
            target, require_enabled=True
        )
        if (
            final_post_fill.state_hash != first_post_fill.state_hash
            or final_url != first_url
            or final_submit_fingerprint != first_submit_fingerprint
        ):
            raise RuntimeError(
                "Post-fill form did not remain stable; final click prohibited"
            )
        _assert_post_fill_invariants(
            approved_plan,
            final_post_fill,
            final_url,
            final_submit_fingerprint,
        )
        if not adapter.native_form_valid(target):
            raise RuntimeError("Browser validation failed; submission stopped before click")
        starting_states = _capture_confirmation_states(
            adapter, page, (page, target)
        )
        submit_control = adapter.submit_control_for_click(
            target, approved_plan.submit_fingerprint
        )
        if not store.claim_approval(
            job_id, token_hash(approval_token), approved_bound
        ):
            raise RuntimeError("Approval was already used or changed")

        try:
            submit_control.click()
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                page.wait_for_timeout(2000)
            confirmed = _submission_confirmed(adapter, page, starting_states)
        except Exception as exc:
            message = (
                "The final click had an ambiguous browser outcome. Approval was "
                "consumed and the application will not be retried automatically. "
                f"Browser detail: {exc}"
            )
            store.update_application(job_id, state="unknown_outcome", last_error=message)
            store.event(job_id, "unknown_outcome", {"error": str(exc)})
            return "unknown_outcome"
        screenshot = artifact_dir / ("submitted.png" if confirmed else "unknown_outcome.png")
        try:
            page.screenshot(path=str(screenshot), full_page=True)
            screenshot.chmod(0o600)
        except Exception:
            pass
        if confirmed:
            store.update_application(
                job_id,
                state="submitted",
                submitted_at=now_iso(),
                last_error="",
            )
            store.event(job_id, "submitted", {"screenshot": str(screenshot)})
            return "submitted"
        state = "blocked_captcha_after_click" if detect_captcha(page) else "unknown_outcome"
        message = (
            "No reliable confirmation was detected. Approval was consumed and the "
            "application will not be retried automatically."
        )
        store.update_application(job_id, state=state, last_error=message)
        store.event(job_id, state, {"screenshot": str(screenshot)})
        return state
