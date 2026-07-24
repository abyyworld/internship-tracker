from __future__ import annotations

from enum import Enum
import re

from .models import FormField, normalize_text


class Category(str, Enum):
    FIRST_NAME = "first_name"
    PREFERRED_NAME = "preferred_name"
    LAST_NAME = "last_name"
    FULL_NAME = "full_name"
    EMAIL = "email"
    PHONE = "phone"
    PHONE_COUNTRY = "phone_country"
    LOCATION = "location"
    LINKEDIN = "linkedin"
    GITHUB = "github"
    WEBSITE = "website"
    SCHOOL = "school"
    DEGREE = "degree"
    FIELD_OF_STUDY = "field_of_study"
    GRAD_MONTH = "graduation_month"
    GRAD_YEAR = "graduation_year"
    GRAD_DATE = "graduation_date"
    RESUME = "resume"
    WORK_AUTH = "work_authorization"
    SPONSORSHIP = "sponsorship"
    CITIZENSHIP = "citizenship"
    EEO = "eeo"
    LEGAL = "legal"
    CONSENT = "consent"
    SALARY = "salary"
    CRIMINAL = "criminal_history"
    CLEARANCE = "clearance_export_control"
    UNKNOWN = "unknown"


def _has(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.I) is not None


def classify(field: FormField) -> Category:
    prompt = normalize_text(field.prompt)
    key = normalize_text(field.key)
    text = normalize_text(f"{prompt} {key}")
    if field.kind == "file" and _has(text, r"\b(resume|résumé|cv)\b"):
        return Category.RESUME
    if _has(text, r"\b(date of birth|birth date|disability|disabled|veteran|gender|sex|sexual orientation|"
                      r"pronouns?|transgender|ethnic|race|hispanic|latino|age|"
                      r"marital status|religion)\b"):
        return Category.EEO
    if _has(text, r"\b(criminal|conviction|convicted|arrest|felony)\b"):
        return Category.CRIMINAL
    if _has(text, r"\b(clearance|export control|itar|government eligibility)\b"):
        return Category.CLEARANCE
    if _has(text, r"\b(citizen|citizenship|nationality)\b"):
        return Category.CITIZENSHIP
    if _has(text, r"\b(sponsor|sponsorship|immigration support|visa support)\b"):
        return Category.SPONSORSHIP
    if _has(text, r"\b(authori[sz]ed|eligible|right)\b.*\b(work|employment)\b"):
        return Category.WORK_AUTH
    if _has(text, r"\b(salary|compensation|pay expectation|desired pay)\b"):
        return Category.SALARY
    if _has(text, r"\b(consent|privacy policy|data processing|marketing communications)\b"):
        return Category.CONSENT
    if _has(text, r"\b(certify|attest|signature|legally binding|terms and conditions|"
                         r"non.?compete|conflict of interest)\b"):
        return Category.LEGAL
    if _has(prompt, r"^preferred name\b") or key in {"preferred_name", "preferred-name"}:
        return Category.PREFERRED_NAME
    if (_has(prompt, r"^(first|given|legal first)\s*name\b")
            or key in {"first_name", "_systemfield_first_name"}):
        return Category.FIRST_NAME
    if (_has(prompt, r"^(last|family|legal last|surname)\s*name\b|^surname\b")
            or key in {"last_name", "_systemfield_last_name"}):
        return Category.LAST_NAME
    if _has(prompt, r"^(email|e-mail)\b") or key in {"email", "_systemfield_email"}:
        return Category.EMAIL
    if _has(prompt, r"^(phone|mobile|telephone)\s+(country|region|code)\b"):
        return Category.PHONE_COUNTRY
    if _has(prompt, r"^(phone|mobile|telephone)\b") or key in {
        "phone", "_systemfield_phone"
    }:
        return Category.PHONE
    if _has(text, r"\blinkedin\b"):
        return Category.LINKEDIN
    if _has(text, r"\bgithub\b"):
        return Category.GITHUB
    if _has(prompt, r"^(portfolio|website|personal website|website url|personal site)\b"):
        return Category.WEBSITE
    if _has(prompt, r"^(expected )?(graduation|graduate).*\bmonth\b.*\byear\b"):
        return Category.GRAD_DATE
    if _has(prompt, r"^(expected )?(graduation|graduate).*\bmonth\b"):
        return Category.GRAD_MONTH
    if _has(prompt, r"^(expected )?(graduation|graduate).*\byear\b"):
        return Category.GRAD_YEAR
    if _has(prompt, r"^(school|university|college|institution)( name)?\b"):
        return Category.SCHOOL
    if _has(prompt, r"^(field of study|discipline|major|course of study)\b"):
        return Category.FIELD_OF_STUDY
    if _has(prompt, r"^(degree|degree type|qualification)\b"):
        return Category.DEGREE
    if _has(text, r"^location\b|\b(current location|home location|city|address|where are you based)\b"):
        return Category.LOCATION
    if _has(prompt, r"^(full |legal )?name\b|^candidate name\b"):
        return Category.FULL_NAME
    return Category.UNKNOWN
