from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
import json
import re
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    raw = value if isinstance(value, str) else canonical_json(value)
    return sha256(raw.encode("utf-8")).hexdigest()


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


@dataclass
class Job:
    id: str
    company: str
    role: str
    url: str
    ats: str = "unknown"
    external_id: str = ""
    location: str = ""
    region: str = ""
    description: str = ""
    source_status: str = "open"

    @property
    def description_hash(self) -> str:
        return digest(normalize_text(self.description))


@dataclass
class FormField:
    key: str
    prompt: str
    kind: str
    required: bool = False
    options: list[str] = field(default_factory=list)
    selector: str = ""
    option_selectors: dict[str, str] = field(default_factory=dict)
    current_value: Any = ""
    value_observable: bool = True

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "FormField":
        return cls(
            key=str(value.get("key", "")),
            prompt=str(value.get("prompt", "")),
            kind=str(value.get("kind", "text")),
            required=bool(value.get("required", False)),
            options=[str(x) for x in value.get("options", [])],
            selector=str(value.get("selector", "")),
            option_selectors={
                str(k): str(v) for k, v in value.get("option_selectors", {}).items()
            },
            current_value=value.get("current_value", ""),
            value_observable=bool(value.get("value_observable", False)),
        )


@dataclass
class FormSnapshot:
    ats: str
    url: str
    fields: list[FormField]
    captcha: bool = False

    @property
    def form_hash(self) -> str:
        stable = [
            {
                "key": f.key,
                "prompt": normalize_text(f.prompt),
                "kind": f.kind,
                "required": f.required,
                "options": [normalize_text(x) for x in f.options],
                "selector": f.selector,
                "value_observable": f.value_observable,
                "option_selectors": {
                    normalize_text(k): v
                    for k, v in sorted(f.option_selectors.items())
                },
            }
            for f in self.fields
        ]
        return digest({"ats": self.ats, "fields": stable})

    @property
    def state_hash(self) -> str:
        return digest(
            {
                "form_hash": self.form_hash,
                "values": [
                    {
                        "key": field.key,
                        "selector": field.selector,
                        "current_value": field.current_value,
                        "value_observable": field.value_observable,
                    }
                    for field in self.fields
                ],
            }
        )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["form_hash"] = self.form_hash
        return value

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "FormSnapshot":
        return cls(
            ats=str(value["ats"]),
            url=str(value["url"]),
            fields=[FormField.from_dict(x) for x in value.get("fields", [])],
            captcha=bool(value.get("captcha", False)),
        )


@dataclass
class FillAction:
    field_key: str
    prompt: str
    kind: str
    selector: str
    value: Any
    source: str
    option_selector: str = ""


@dataclass
class UnresolvedField:
    field_key: str
    prompt: str
    required: bool
    reason: str
    category: str


@dataclass
class FillPlan:
    job_id: str
    form_hash: str
    resume_path: str
    resume_hash: str
    actions: list[FillAction] = field(default_factory=list)
    unresolved: list[UnresolvedField] = field(default_factory=list)
    captcha: bool = False
    application_url: str = ""
    eligibility_hash: str = ""
    initial_state_hash: str = ""
    submit_fingerprint: str = ""

    @property
    def blocking(self) -> list[UnresolvedField]:
        return [x for x in self.unresolved if x.required]

    @property
    def safe_to_submit(self) -> bool:
        return not self.captcha and not self.blocking

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["safe_to_submit"] = self.safe_to_submit
        return value

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "FillPlan":
        return cls(
            job_id=str(value["job_id"]),
            form_hash=str(value["form_hash"]),
            resume_path=str(value.get("resume_path", "")),
            resume_hash=str(value.get("resume_hash", "")),
            actions=[FillAction(**x) for x in value.get("actions", [])],
            unresolved=[UnresolvedField(**x) for x in value.get("unresolved", [])],
            captcha=bool(value.get("captcha", False)),
            application_url=str(value.get("application_url", "")),
            eligibility_hash=str(value.get("eligibility_hash", "")),
            initial_state_hash=str(value.get("initial_state_hash", "")),
            submit_fingerprint=str(value.get("submit_fingerprint", "")),
        )

    def approval_hash(self, job: Job) -> str:
        actions = [
            {
                "field_key": x.field_key,
                "prompt": normalize_text(x.prompt),
                "kind": x.kind,
                "value": x.value,
                "source": x.source,
                "selector": x.selector,
                "option_selector": x.option_selector,
            }
            for x in self.actions
        ]
        return digest(
            {
                "job_id": job.id,
                "url": job.url,
                "application_url": self.application_url,
                "description_hash": job.description_hash,
                "eligibility_hash": self.eligibility_hash,
                "initial_state_hash": self.initial_state_hash,
                "submit_fingerprint": self.submit_fingerprint,
                "form_hash": self.form_hash,
                "resume_hash": self.resume_hash,
                "actions": actions,
                "unresolved": [asdict(x) for x in self.unresolved],
                "captcha": self.captcha,
            }
        )
