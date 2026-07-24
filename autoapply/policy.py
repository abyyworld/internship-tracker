from __future__ import annotations

from hashlib import sha256
import re
import secrets
from typing import Any

from .eligibility import explicit_jurisdictions, jurisdiction_for
from .models import (
    FillAction,
    FillPlan,
    FormField,
    FormSnapshot,
    Job,
    UnresolvedField,
    normalize_text,
)
from .questions import Category, classify


IDENTITY_PATHS: dict[Category, tuple[str, str]] = {
    Category.FIRST_NAME: ("identity", "first_name"),
    Category.PREFERRED_NAME: ("identity", "preferred_name"),
    Category.LAST_NAME: ("identity", "last_name"),
    Category.EMAIL: ("contact", "email"),
    Category.PHONE: ("contact", "phone"),
    Category.PHONE_COUNTRY: ("contact", "phone_country"),
    Category.LOCATION: ("contact", "location"),
    Category.LINKEDIN: ("contact", "linkedin"),
    Category.GITHUB: ("contact", "github"),
    Category.WEBSITE: ("contact", "website"),
    Category.SCHOOL: ("education", "institution"),
    Category.DEGREE: ("education", "degree"),
    Category.FIELD_OF_STUDY: ("education", "field_of_study"),
    Category.GRAD_MONTH: ("education", "graduation_month"),
    Category.GRAD_YEAR: ("education", "graduation_year"),
    Category.GRAD_DATE: ("education", "graduation_date"),
}

MANUAL_ONLY = {
    Category.CITIZENSHIP,
    Category.LEGAL,
    Category.CONSENT,
    Category.SALARY,
    Category.CRIMINAL,
    Category.CLEARANCE,
}


def token_hash(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def new_approval_token() -> str:
    return secrets.token_urlsafe(24)


def _nested(profile: dict[str, Any], path: tuple[str, str]) -> Any:
    return profile.get(path[0], {}).get(path[1], "")


def _full_name(profile: dict[str, Any]) -> str:
    identity = profile.get("identity", {})
    return f"{identity.get('first_name', '')} {identity.get('last_name', '')}".strip()


def _reviewed_answer(
    profile: dict[str, Any],
    job: Job,
    form_hash: str,
    field: FormField,
) -> Any:
    """Return only an answer reviewed for this exact job and form revision."""
    per_job = profile.get("reviewed_answers", {}).get(job.id, {})
    if not isinstance(per_job, dict):
        return None
    wanted = normalize_text(f"{form_hash} :: {field.key} :: {field.prompt}")
    for key, value in per_job.items():
        if normalize_text(str(key)) == wanted:
            return value
    return None


def _question_jurisdiction(prompt: str, job: Job) -> str:
    text = normalize_text(prompt)
    explicit = explicit_jurisdictions(prompt)
    if len(explicit) == 1:
        return next(iter(explicit))
    if len(explicit) > 1:
        return ""
    # A prompt that syntactically names a place we do not recognise must not
    # inherit the job's country. Generic references to "this job/country" may
    # use the unambiguous job jurisdiction.
    work_location_clause = re.search(
        r"\b(?:work|working|employed|employment)\b.{0,60}"
        r"\b(?:in|within|for)\s+([^?.,;:]{2,80})",
        text,
    )
    generic_location = re.search(
        r"\b(?:this|the|that)\s+(?:country|jurisdiction|location|region|"
        r"job|role|position|office)\b|"
        r"\bcountry (?:where|in which)\b|"
        r"\b(?:job|role|position|office) (?:is )?(?:based|located)\b",
        text,
    )
    if work_location_clause and not generic_location:
        return ""
    return jurisdiction_for(job)


def _match_option(
    field: FormField, desired: Any
) -> tuple[Any, str] | None:
    if field.kind == "checkbox":
        if isinstance(desired, bool):
            return desired, ""
        normalized = normalize_text(str(desired))
        if normalized in {"yes", "true", "checked", "agree", "i agree"}:
            return True, ""
        if normalized in {"no", "false", "unchecked", "disagree", "i disagree"}:
            return False, ""
        return None
    if field.kind not in {"select", "radio", "combobox", "checkbox-group"}:
        return desired, ""
    if isinstance(desired, bool):
        desired = "Yes" if desired else "No"
    wanted = normalize_text(str(desired))
    exact = [option for option in field.options if normalize_text(option) == wanted]
    candidates = exact
    if not candidates and wanted in {"yes", "no"}:
        candidates = [
            option
            for option in field.options
            if normalize_text(option).startswith(wanted + " ")
            or normalize_text(option).startswith(wanted + ",")
        ]
    if len(candidates) != 1:
        return None
    displayed = candidates[0]
    return displayed, field.option_selectors.get(displayed, "")


def _resolve(
    field: FormField,
    category: Category,
    profile: dict[str, Any],
    job: Job,
    form_hash: str,
    resume_path: str,
) -> tuple[Any, str] | tuple[None, str]:
    if category == Category.RESUME:
        return (resume_path, "tailored_resume") if resume_path else (None, "resume_missing")
    if category == Category.FULL_NAME:
        value = _full_name(profile)
        return (value, "profile.identity") if value else (None, "profile_value_missing")
    if category in IDENTITY_PATHS:
        if field.kind in {"select", "radio", "combobox", "checkbox-group"}:
            reviewed = _reviewed_answer(profile, job, form_hash, field)
            if reviewed is not None:
                return reviewed, "profile.reviewed_answers.exact_prompt"
        value = _nested(profile, IDENTITY_PATHS[category])
        return (value, f"profile.{'.'.join(IDENTITY_PATHS[category])}") if value else (
            None,
            "profile_value_missing",
        )
    if category in {Category.WORK_AUTH, Category.SPONSORSHIP}:
        if field.kind not in {"select", "radio", "combobox"}:
            return None, "sensitive_answer_requires_an_exact_choice_control"
        prompt = normalize_text(field.prompt)
        nuanced = (
            category == Category.WORK_AUTH
            and re.search(
                r"\beligible to apply\b|\bapply for (?:a )?(?:visa|permit)\b|"
                r"\b(?:visa|permit) (?:type|status|details?)\b|"
                r"\bwhat (?:type|kind) of (?:visa|permit)\b",
                prompt,
            )
        ) or (
            category == Category.SPONSORSHIP
            and re.search(
                r"\b(?:visa|permit) (?:type|status|details?)\b|"
                r"\bwhat (?:type|kind) of (?:visa|permit|sponsorship)\b",
                prompt,
            )
        )
        if nuanced:
            reviewed = _reviewed_answer(profile, job, form_hash, field)
            if reviewed is not None:
                return reviewed, "profile.reviewed_answers.exact_prompt"
            return None, "nuanced_immigration_question_requires_exact_review"
        jurisdiction = _question_jurisdiction(field.prompt, job)
        if not jurisdiction:
            return None, "job_jurisdiction_unknown"
        auth = profile.get("work_authorization", {}).get(jurisdiction, {})
        key = (
            "authorized_now"
            if category == Category.WORK_AUTH
            else "requires_sponsorship_now_or_future"
        )
        value = auth.get(key, "unknown")
        if value == "unknown" or value is None:
            return None, f"profile.work_authorization.{jurisdiction}.{key}_unknown"
        return value, f"profile.work_authorization.{jurisdiction}.{key}"
    if category == Category.EEO:
        mode = profile.get("preferences", {}).get("eeo", "manual")
        if mode == "decline_if_available":
            decline = [
                option
                for option in field.options
                if any(
                    phrase in normalize_text(option)
                    for phrase in ("decline", "prefer not", "do not wish", "not disclose")
                )
            ]
            if len(decline) == 1:
                return decline[0], "profile.preferences.eeo"
        reviewed = _reviewed_answer(profile, job, form_hash, field)
        if reviewed is not None:
            return reviewed, "profile.reviewed_answers.exact_prompt"
        return None, "protected_information_manual_only"
    if category in MANUAL_ONLY:
        reviewed = _reviewed_answer(profile, job, form_hash, field)
        if reviewed is not None:
            return reviewed, "profile.reviewed_answers.exact_prompt"
        return None, f"{category.value}_manual_only"
    if category == Category.UNKNOWN:
        reviewed = _reviewed_answer(profile, job, form_hash, field)
        if reviewed is not None:
            return reviewed, "profile.reviewed_answers"
        return None, "unrecognized_question"
    return None, "no_safe_rule"


def build_fill_plan(
    job: Job,
    snapshot: FormSnapshot,
    profile: dict[str, Any],
    resume_path: str,
    resume_hash: str,
) -> FillPlan:
    actions: list[FillAction] = []
    unresolved: list[UnresolvedField] = []
    for field in snapshot.fields:
        category = classify(field)
        value, source = _resolve(
            field,
            category,
            profile,
            job,
            snapshot.form_hash,
            resume_path,
        )
        if value is None:
            unresolved.append(
                UnresolvedField(
                    field_key=field.key,
                    prompt=field.prompt,
                    required=field.required,
                    reason=source,
                    category=category.value,
                )
            )
            continue
        matched = _match_option(field, value)
        if matched is None:
            unresolved.append(
                UnresolvedField(
                    field_key=field.key,
                    prompt=field.prompt,
                    required=field.required,
                    reason="configured_answer_does_not_match_one_exact_option",
                    category=category.value,
                )
            )
            continue
        displayed, option_selector = matched
        if field.kind == "checkbox" and field.required and displayed is False:
            unresolved.append(
                UnresolvedField(
                    field_key=field.key,
                    prompt=field.prompt,
                    required=True,
                    reason="required_checkbox_was_explicitly_declined",
                    category=category.value,
                )
            )
            continue
        actions.append(
            FillAction(
                field_key=field.key,
                prompt=field.prompt,
                kind=field.kind,
                selector=field.selector,
                value=displayed,
                source=source,
                option_selector=option_selector,
            )
        )
    return FillPlan(
        job_id=job.id,
        form_hash=snapshot.form_hash,
        resume_path=resume_path,
        resume_hash=resume_hash,
        actions=actions,
        unresolved=unresolved,
        captcha=snapshot.captcha,
    )
