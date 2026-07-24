from __future__ import annotations

import argparse
from importlib.util import find_spec
import json
import os
from pathlib import Path
import platform
import re
import stat
import sys
from typing import Any

from .config import (
    database_path,
    default_home,
    ensure_home,
    facts_path,
    load_yaml,
    profile_path,
    reject_placeholders,
)
from .jobs import jobs_from_tracker
from .models import digest
from .runner import approve, inspect_and_plan, prepare, submit
from .store import Store


def _print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def plan_for_output(plan: Any, *, show_values: bool) -> dict[str, Any]:
    """Redact personal form values from stdout unless explicitly requested."""
    value = plan.to_dict()
    if show_values:
        return value
    value["resume_path"] = "[private]"
    for action in value.get("actions", []):
        action["value"] = "[redacted]"
    value["output_note"] = (
        "Personal action values are redacted. Rerun with --show-values only in "
        "a private terminal when reviewing the plan."
    )
    return value


def approval_token_path(home: Path, job_id: str) -> Path:
    prefix = re.sub(r"[^a-zA-Z0-9_.-]+", "_", job_id).strip("._")[:48] or "job"
    return home / "approvals" / f"{prefix}-{digest(job_id)[:12]}.token"


def resolve_approval_token_path(
    home: Path, job_id: str, requested: Path | None
) -> Path:
    """Keep approval secrets inside one dedicated directory under private home."""
    approval_dir = (home / "approvals").resolve()
    if requested is None:
        return approval_token_path(home, job_id).resolve()
    path = requested.expanduser().resolve()
    if path.parent != approval_dir:
        raise RuntimeError(
            "Approval token files must be direct children of "
            f"{approval_dir}; arbitrary shared paths are refused"
        )
    return path


def write_approval_token(path: Path, token: str) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    parent_mode = stat.S_IMODE(path.parent.stat().st_mode)
    if parent_mode & 0o077:
        raise RuntimeError("Approval token directory must not be group/world accessible")
    if path.is_symlink():
        raise RuntimeError("Refusing to overwrite a symbolic-link approval token")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, 0o600)
    except OSError as exc:
        raise RuntimeError(f"Could not create approval token file: {exc}") from exc
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = -1
            handle.write(token + "\n")
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    path.chmod(0o600)


def read_approval_token(path: Path) -> str:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise RuntimeError(f"Could not read approval token file: {exc}") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise RuntimeError("Approval token path must be a regular file")
        if stat.S_IMODE(metadata.st_mode) != 0o600:
            raise RuntimeError("Approval token file must have mode 0600")
        with os.fdopen(descriptor, encoding="utf-8") as handle:
            descriptor = -1
            token = handle.read().strip()
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if not token:
        raise RuntimeError("Approval token file is empty")
    return token


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m autoapply",
        description="Local, dry-run-first ATS application assistant.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=default_home(),
        help="Private data directory (default: %(default)s)",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Check local dependencies and private configuration")

    importer = commands.add_parser(
        "import-tracker",
        help="Import jobs from tracker.csv",
        allow_abbrev=False,
    )
    importer.add_argument("--tracker", type=Path, default=Path("tracker.csv"))

    job_commands: dict[str, argparse.ArgumentParser] = {}
    for name in ("prepare", "inspect", "fill", "approve"):
        command = commands.add_parser(name, allow_abbrev=False)
        job_commands[name] = command
        command.add_argument("job_id")
        if name in {"inspect", "fill"}:
            command.add_argument("--headed", action="store_true")
            command.add_argument(
                "--show-values",
                action="store_true",
                help="Print personal planned values to this terminal (redacted by default).",
            )
        if name == "fill":
            command.add_argument(
                "--execute",
                action="store_true",
                help="Actually fill the live form. Without this flag, only a plan is produced.",
            )
    job_commands["approve"].add_argument(
        "--approval-file",
        type=Path,
        help="Private output file for the one-time token (default: under AUTOAPPLY_HOME)",
    )

    submit_command = commands.add_parser("submit", allow_abbrev=False)
    submit_command.add_argument("job_id")
    submit_command.add_argument(
        "--approval-file",
        type=Path,
        help="Mode-0600 token file created by approve (default: under AUTOAPPLY_HOME)",
    )

    status = commands.add_parser("status", allow_abbrev=False)
    status.add_argument("--job-id")

    bridge = commands.add_parser(
        "bridge",
        help="Serve the private click-to-tailor bridge on localhost",
        allow_abbrev=False,
    )
    bridge.add_argument("--tracker", type=Path, default=Path("tracker.csv"))
    bridge.add_argument("--port", type=int, default=8765)
    return parser


def doctor(home: Path) -> tuple[dict[str, Any], bool]:
    edge = Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge")
    configs_ok = True
    config_error = ""
    profile: dict[str, Any] = {}
    try:
        profile = load_yaml(profile_path(home))
        reject_placeholders(profile)
        reject_placeholders(load_yaml(facts_path(home)))
    except (FileNotFoundError, ValueError) as exc:
        configs_ok = False
        config_error = str(exc)
    required_profile_values = {
        "identity.first_name": profile.get("identity", {}).get("first_name"),
        "identity.last_name": profile.get("identity", {}).get("last_name"),
        "contact.email": profile.get("contact", {}).get("email"),
        "contact.phone": profile.get("contact", {}).get("phone"),
        "contact.phone_country": profile.get("contact", {}).get("phone_country"),
        "contact.location": profile.get("contact", {}).get("location"),
        "education.institution": profile.get("education", {}).get("institution"),
        "education.degree": profile.get("education", {}).get("degree"),
        "education.field_of_study": profile.get("education", {}).get("field_of_study"),
        "education.level": profile.get("education", {}).get("level"),
        "education.graduation_date": profile.get("education", {}).get(
            "graduation_date"
        ),
    }
    missing_profile_values = sorted(
        key for key, value in required_profile_values.items()
        if value is None or not str(value).strip()
    )
    work_auth = profile.get("work_authorization", {})
    unknown_jurisdictions = sorted(
        str(code)
        for code, values in work_auth.items()
        if not isinstance(values, dict)
        or values.get("authorized_now", "unknown") == "unknown"
        or values.get("requires_sponsorship_now_or_future", "unknown") == "unknown"
    )
    application_profile_ok = (
        configs_ok
        and not missing_profile_values
        and bool(profile.get("citizenships"))
        and any(
            isinstance(values, dict)
            and values.get("authorized_now", "unknown") != "unknown"
            and values.get("requires_sponsorship_now_or_future", "unknown")
            != "unknown"
            for values in work_auth.values()
        )
    )
    private_mode = stat.S_IMODE(home.stat().st_mode)
    sensitive_modes = {
        str(path): stat.S_IMODE(path.stat().st_mode)
        for path in (profile_path(home), facts_path(home), database_path(home))
        if path.exists()
    }
    tailoring = profile.get("tailoring", {})
    tailoring_provider = tailoring.get("provider", "deterministic")
    local_ai_check: dict[str, Any] = {
        "ok": True,
        "provider": tailoring_provider,
    }
    if configs_ok and tailoring_provider == "ollama":
        model = str(tailoring.get("model", "")).strip()
        endpoint = str(
            tailoring.get("endpoint", "http://127.0.0.1:11434")
        ).strip()
        try:
            from .ai_tailoring import ollama_models

            models = ollama_models(endpoint)
            local_ai_check = {
                "ok": bool(model) and model in models,
                "provider": "ollama",
                "model": model,
                "endpoint": endpoint,
                "available_models": sorted(models),
                "error": (
                    "" if model in models else "Configured model is not installed"
                ),
            }
        except Exception as exc:
            local_ai_check = {
                "ok": False,
                "provider": "ollama",
                "model": model,
                "endpoint": endpoint,
                "available_models": [],
                "error": str(exc),
            }
    checks = {
        "python": {
            "ok": sys.version_info >= (3, 11),
            "value": platform.python_version(),
        },
        "pyyaml": {"ok": find_spec("yaml") is not None},
        "reportlab": {"ok": find_spec("reportlab") is not None},
        "requests": {"ok": find_spec("requests") is not None},
        "playwright": {"ok": find_spec("playwright") is not None},
        "microsoft_edge": {"ok": edge.exists(), "path": str(edge)},
        "profile": {"ok": profile_path(home).is_file(), "path": str(profile_path(home))},
        "resume_facts": {"ok": facts_path(home).is_file(), "path": str(facts_path(home))},
        "configuration": {"ok": configs_ok, "error": config_error},
        "local_ai_tailoring": local_ai_check,
        "application_profile": {
            "ok": application_profile_ok,
            "missing_required_values": missing_profile_values,
            "citizenships_confirmed": bool(profile.get("citizenships")),
            "jurisdictions_still_unknown": unknown_jurisdictions,
            "note": (
                "Unknown values are safe and intentional, but approval remains "
                "blocked for forms that require them."
            ),
        },
        "private_home": {
            "ok": private_mode & 0o077 == 0,
            "path": str(home),
            "mode": oct(private_mode),
        },
        "sensitive_file_permissions": {
            "ok": all(mode & 0o077 == 0 for mode in sensitive_modes.values()),
            "modes": {path: oct(mode) for path, mode in sensitive_modes.items()},
        },
    }
    ok = all(item["ok"] for item in checks.values())
    return {"ok": ok, "checks": checks}, ok


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    home = ensure_home(args.home.expanduser().resolve())
    if args.command == "doctor":
        result, ok = doctor(home)
        _print(result)
        return 0 if ok else 1
    if args.command == "bridge":
        from .bridge import run_bridge

        try:
            run_bridge(home, args.tracker, args.port)
        except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
            print(f"autoapply: {exc}", file=sys.stderr)
            return 2
        return 0

    try:
        with Store(database_path(home)) as store:
            if args.command == "import-tracker":
                jobs = jobs_from_tracker(args.tracker)
                count = store.import_jobs(jobs)
                _print({"imported": count, "database": str(store.path)})
            elif args.command == "prepare":
                _print(prepare(store, home, args.job_id))
            elif args.command == "inspect":
                plan = inspect_and_plan(
                    store, home, args.job_id, headed=args.headed, execute=False
                )
                _print(plan_for_output(plan, show_values=args.show_values))
            elif args.command == "fill":
                plan = inspect_and_plan(
                    store,
                    home,
                    args.job_id,
                    headed=args.headed,
                    execute=args.execute,
                )
                _print(plan_for_output(plan, show_values=args.show_values))
            elif args.command == "approve":
                token, bound, expires_at = approve(store, home, args.job_id)
                token_file = resolve_approval_token_path(
                    home, args.job_id, args.approval_file
                )
                write_approval_token(token_file, token)
                _print(
                    {
                        "job_id": args.job_id,
                        "approval_file": str(token_file),
                        "approval_bound_hash": bound,
                        "approval_expires_at": expires_at,
                        "warning": "The mode-0600 token file is valid for one submit click.",
                    }
                )
            elif args.command == "submit":
                token_file = resolve_approval_token_path(
                    home, args.job_id, args.approval_file
                )
                approval_token = read_approval_token(token_file)
                try:
                    outcome = submit(
                        store,
                        home,
                        args.job_id,
                        approval_token,
                        headed=True,
                    )
                finally:
                    application = store.application(args.job_id)
                    if application["approval_used"] or application["state"] == "approval_expired":
                        token_file.unlink(missing_ok=True)
                _print({"job_id": args.job_id, "outcome": outcome})
            elif args.command == "status":
                values = store.statuses()
                if args.job_id:
                    values = [value for value in values if value["id"] == args.job_id]
                _print(values)
    except (FileNotFoundError, KeyError, OSError, RuntimeError, ValueError) as exc:
        print(f"autoapply: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
