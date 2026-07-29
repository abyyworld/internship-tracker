"""Multiple saved CVs.

The fact bank at ``private/resume_facts.yaml`` is the master CV. Additional
saved CVs live in ``private/cv-library/<id>.yaml`` and use the same schema, so
any of them can be opened in the editor, tailored for a job, and saved back as
a new CV without touching the master.
"""

from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
import re
from typing import Any

import yaml

from .config import facts_path, load_yaml


MASTER_CV_ID = "master"
LIBRARY_DIRECTORY = "cv-library"
MAX_LABEL_CHARS = 80


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def safe_cv_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value or "")).strip(".-")
    return cleaned[:64]


def library_directory(home: Path) -> Path:
    return home / LIBRARY_DIRECTORY


def cv_path(home: Path, cv_id: str) -> Path:
    """Resolve a CV id to its file, refusing anything outside the library."""
    identifier = safe_cv_id(cv_id) or MASTER_CV_ID
    if identifier == MASTER_CV_ID:
        return facts_path(home)
    directory = library_directory(home).resolve()
    candidate = (directory / f"{identifier}.yaml").resolve()
    if candidate.parent != directory:
        raise ValueError("Invalid CV id")
    return candidate


def _label_of(value: dict[str, Any], fallback: str) -> str:
    label = str(value.get("label", "")).strip()
    return (label or fallback)[:MAX_LABEL_CHARS]


def list_cvs(home: Path) -> list[dict[str, Any]]:
    """Return every saved CV, master first, then the library newest-first."""
    entries: list[dict[str, Any]] = []
    master = facts_path(home)
    if master.exists():
        try:
            loaded = load_yaml(master)
        except (OSError, ValueError):
            loaded = {}
        entries.append(
            {
                "id": MASTER_CV_ID,
                "label": _label_of(loaded, "Master CV"),
                "is_master": True,
                "updated_at": str(loaded.get("saved_at", "")),
            }
        )
    directory = library_directory(home)
    if directory.is_dir():
        saved: list[dict[str, Any]] = []
        for path in sorted(directory.glob("*.yaml")):
            if path.is_symlink() or not path.is_file():
                continue
            try:
                loaded = load_yaml(path)
            except (OSError, ValueError):
                continue
            saved.append(
                {
                    "id": path.stem,
                    "label": _label_of(loaded, path.stem),
                    "is_master": False,
                    "updated_at": str(loaded.get("saved_at", "")),
                }
            )
        saved.sort(key=lambda item: item["updated_at"], reverse=True)
        entries.extend(saved)
    return entries


def load_cv(home: Path, cv_id: str) -> dict[str, Any]:
    path = cv_path(home, cv_id)
    if not path.exists():
        raise FileNotFoundError(f"Saved CV '{safe_cv_id(cv_id)}' does not exist")
    return load_yaml(path)


def save_cv(
    home: Path,
    cv_id: str,
    label: str,
    facts: dict[str, Any],
) -> dict[str, Any]:
    """Write a CV into the library as a private mode-0600 file.

    The master CV is never overwritten here; saving always targets the library
    so the immutable fact bank stays the single reviewed source of truth.
    """
    identifier = safe_cv_id(cv_id)
    if not identifier or identifier == MASTER_CV_ID:
        raise ValueError("Choose a name for the saved CV")
    if not isinstance(facts, dict) or not facts.get("sections"):
        raise ValueError("A saved CV needs at least one section")

    payload = dict(facts)
    payload["label"] = str(label or identifier).strip()[:MAX_LABEL_CHARS]
    payload["saved_at"] = _now_iso()

    path = cv_path(home, identifier)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.parent.chmod(0o700)
    if path.exists() and path.is_symlink():
        raise RuntimeError("Refusing a symbolic-link CV file")

    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(temporary, flags, 0o600)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = -1
            yaml.safe_dump(payload, handle, allow_unicode=True, sort_keys=False)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    os.replace(temporary, path)
    path.chmod(0o600)
    return {"id": identifier, "label": payload["label"], "is_master": False}
