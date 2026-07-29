from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def default_home() -> Path:
    configured = os.environ.get("AUTOAPPLY_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path(__file__).resolve().parent.parent / "private").resolve()


def ensure_home(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.chmod(0o700)
    for child in ("generated", "artifacts", "browser-profile"):
        directory = path / child
        directory.mkdir(exist_ok=True, mode=0o700)
        directory.chmod(0o700)
    for sensitive in (profile_path(path), facts_path(path), database_path(path)):
        if sensitive.exists():
            sensitive.chmod(0o600)
    return path


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} does not exist. Copy the matching example from config/ and "
            "replace every placeholder with verified information."
        )
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle) or {}
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def profile_path(home: Path) -> Path:
    return home / "profile.yaml"


def facts_path(home: Path) -> Path:
    return home / "resume_facts.yaml"


def academic_path(home: Path) -> Path:
    return home / "academic_profile.yaml"


def database_path(home: Path) -> Path:
    return home / "autoapply.sqlite3"


def reject_placeholders(value: Any, path: str = "") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                location = path or "<root>"
                raise ValueError(
                    f"YAML mapping keys must be strings at {location}; "
                    "quote country codes such as \"NO\""
                )
            reject_placeholders(child, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_placeholders(child, f"{path}[{index}]")
    elif isinstance(value, str) and ("REPLACE_ME" in value or "example.com" in value):
        raise ValueError(f"Unresolved placeholder at {path}")
