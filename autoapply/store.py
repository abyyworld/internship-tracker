from __future__ import annotations

import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterable

from .models import FillPlan, Job, canonical_json


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    url TEXT NOT NULL,
    ats TEXT NOT NULL,
    external_id TEXT NOT NULL DEFAULT '',
    location TEXT NOT NULL DEFAULT '',
    region TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    source_status TEXT NOT NULL DEFAULT 'open',
    imported_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS applications (
    job_id TEXT PRIMARY KEY REFERENCES jobs(id),
    state TEXT NOT NULL DEFAULT 'discovered',
    resume_path TEXT NOT NULL DEFAULT '',
    resume_hash TEXT NOT NULL DEFAULT '',
    form_hash TEXT NOT NULL DEFAULT '',
    plan_json TEXT NOT NULL DEFAULT '',
    approval_token_hash TEXT NOT NULL DEFAULT '',
    approval_bound_hash TEXT NOT NULL DEFAULT '',
    approval_expires_at TEXT NOT NULL DEFAULT '',
    approval_used INTEGER NOT NULL DEFAULT 0,
    last_error TEXT NOT NULL DEFAULT '',
    submitted_at TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    at TEXT NOT NULL,
    event TEXT NOT NULL,
    detail_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS events_job_id_idx ON events(job_id, id);
CREATE UNIQUE INDEX IF NOT EXISTS jobs_url_unique_idx
    ON jobs(url) WHERE url != '';
CREATE UNIQUE INDEX IF NOT EXISTS jobs_ats_external_unique_idx
    ON jobs(ats, external_id)
    WHERE ats != 'unknown' AND external_id != '';
"""

TERMINAL_APPLICATION_STATES = {
    "submitted",
    "submitting",
    "unknown_outcome",
    "blocked_captcha_after_click",
}


class Store:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.db = sqlite3.connect(path)
        path.chmod(0o600)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)
        columns = {
            row["name"]
            for row in self.db.execute("PRAGMA table_info(applications)").fetchall()
        }
        if "approval_expires_at" not in columns:
            self.db.execute(
                "ALTER TABLE applications "
                "ADD COLUMN approval_expires_at TEXT NOT NULL DEFAULT ''"
            )
            self.db.commit()

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> "Store":
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()

    def upsert_job(self, job: Job, *, commit: bool = True) -> str:
        stamp = now_iso()
        exact = self.db.execute(
            "SELECT id FROM jobs WHERE id=?", (job.id,)
        ).fetchone()
        duplicate = self.db.execute(
            """
            SELECT id FROM jobs
            WHERE url=?
               OR (? != '' AND ats=? AND external_id=?)
            LIMIT 1
            """,
            (job.url, job.external_id, job.ats, job.external_id),
        ).fetchone()
        target_id = (
            exact["id"] if exact is not None
            else duplicate["id"] if duplicate is not None
            else job.id
        )
        self.db.execute(
            """
            INSERT INTO jobs
              (id, company, role, url, ats, external_id, location, region,
               description, source_status, imported_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              company=excluded.company, role=excluded.role, url=excluded.url,
              ats=excluded.ats, external_id=excluded.external_id,
              location=excluded.location, region=excluded.region,
              description=CASE WHEN excluded.description != ''
                               THEN excluded.description ELSE jobs.description END,
              source_status=excluded.source_status, updated_at=excluded.updated_at
            """,
            (
                target_id,
                job.company,
                job.role,
                job.url,
                job.ats,
                job.external_id,
                job.location,
                job.region,
                job.description,
                job.source_status,
                stamp,
                stamp,
            ),
        )
        self.db.execute(
            """
            INSERT INTO applications(job_id, state, updated_at)
            VALUES (?, 'discovered', ?)
            ON CONFLICT(job_id) DO NOTHING
            """,
            (target_id, stamp),
        )
        if commit:
            self.db.commit()
        return target_id

    def import_jobs(self, jobs: Iterable[Job]) -> int:
        """Atomically replace the latest supported-open tracker snapshot.

        Jobs absent from the latest import are retained for audit history, but
        they are made ineligible for preparation/approval/submission until they
        reappear as open in a later snapshot.
        """
        imported: set[str] = set()
        try:
            for job in jobs:
                imported.add(self.upsert_job(job, commit=False))
            stamp = now_iso()
            if imported:
                placeholders = ",".join("?" for _ in imported)
                self.db.execute(
                    f"""
                    UPDATE jobs
                    SET source_status='not_in_latest_import', updated_at=?
                    WHERE id NOT IN ({placeholders})
                    """,
                    (stamp, *sorted(imported)),
                )
            else:
                self.db.execute(
                    """
                    UPDATE jobs
                    SET source_status='not_in_latest_import', updated_at=?
                    """,
                    (stamp,),
                )
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        return len(imported)

    def get_job(self, job_id: str) -> Job:
        row = self.db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(f"Unknown job id: {job_id}")
        return Job(
            id=row["id"],
            company=row["company"],
            role=row["role"],
            url=row["url"],
            ats=row["ats"],
            external_id=row["external_id"],
            location=row["location"],
            region=row["region"],
            description=row["description"],
            source_status=row["source_status"],
        )

    def find_job_by_url(self, url: str) -> Job:
        """Resolve a clicked public ATS URL to exactly one imported job."""
        from .jobs import canonicalize_url, detect_ats, external_id

        canonical = canonicalize_url(url)
        ats = detect_ats(canonical)
        identifier = external_id(canonical, ats)
        row = None
        if ats != "unknown" and identifier:
            row = self.db.execute(
                "SELECT id FROM jobs WHERE ats=? AND external_id=? LIMIT 1",
                (ats, identifier),
            ).fetchone()
        if row is None:
            matches = [
                candidate["id"]
                for candidate in self.db.execute("SELECT id, url FROM jobs").fetchall()
                if canonicalize_url(candidate["url"]) == canonical
            ]
            if len(matches) == 1:
                row = {"id": matches[0]}
        if row is None:
            raise KeyError(
                "This link is not one of the currently imported open postings"
            )
        job = self.get_job(str(row["id"]))
        if job.source_status != "open":
            raise KeyError("This job is no longer open in the latest tracker import")
        return job

    def update_description(self, job_id: str, description: str) -> None:
        self.db.execute(
            "UPDATE jobs SET description=?, updated_at=? WHERE id=?",
            (description, now_iso(), job_id),
        )
        self.db.commit()

    def application(self, job_id: str) -> dict[str, Any]:
        row = self.db.execute(
            "SELECT * FROM applications WHERE job_id=?", (job_id,)
        ).fetchone()
        if row is None:
            raise KeyError(f"No application for job id: {job_id}")
        return dict(row)

    def update_application(self, job_id: str, **values: Any) -> None:
        allowed = {
            "state",
            "resume_path",
            "resume_hash",
            "form_hash",
            "plan_json",
            "approval_token_hash",
            "approval_bound_hash",
            "approval_expires_at",
            "approval_used",
            "last_error",
            "submitted_at",
        }
        unknown = set(values) - allowed
        if unknown:
            raise ValueError(f"Unsupported application columns: {sorted(unknown)}")
        values["updated_at"] = now_iso()
        assignments = ", ".join(f"{key}=?" for key in values)
        self.db.execute(
            f"UPDATE applications SET {assignments} WHERE job_id=?",
            (*values.values(), job_id),
        )
        self.db.commit()

    def save_plan(self, job_id: str, plan: FillPlan, state: str = "planned") -> None:
        if self.application(job_id)["state"] in TERMINAL_APPLICATION_STATES:
            raise RuntimeError(
                "Application is in a terminal or ambiguous post-click state; "
                "refusing to create a new plan"
            )
        self.update_application(
            job_id,
            state=state,
            form_hash=plan.form_hash,
            plan_json=canonical_json(plan.to_dict()),
            approval_token_hash="",
            approval_bound_hash="",
            approval_expires_at="",
            approval_used=0,
            last_error="",
        )
        self.event(
            job_id,
            "plan_saved",
            {
                "form_hash": plan.form_hash,
                "actions": len(plan.actions),
                "blocking": len(plan.blocking),
                "captcha": plan.captcha,
            },
        )

    def load_plan(self, job_id: str) -> FillPlan:
        raw = self.application(job_id).get("plan_json", "")
        if not raw:
            raise ValueError("No fill plan exists; run inspect or fill first")
        return FillPlan.from_dict(json.loads(raw))

    def claim_approval(
        self, job_id: str, supplied_token_hash: str, bound_hash: str
    ) -> bool:
        """Atomically consume an approval immediately before the final click."""
        stamp = now_iso()
        cursor = self.db.execute(
            """
            UPDATE applications
            SET approval_used=1, state='submitting', updated_at=?
            WHERE job_id=? AND approval_used=0
              AND approval_token_hash=? AND approval_bound_hash=?
              AND approval_expires_at > ?
              AND state='approved'
            """,
            (stamp, job_id, supplied_token_hash, bound_hash, stamp),
        )
        self.db.commit()
        return cursor.rowcount == 1

    def event(self, job_id: str, event: str, detail: Any | None = None) -> None:
        self.db.execute(
            "INSERT INTO events(job_id, at, event, detail_json) VALUES (?, ?, ?, ?)",
            (job_id, now_iso(), event, canonical_json(detail or {})),
        )
        self.db.commit()

    def statuses(self) -> list[dict[str, Any]]:
        rows = self.db.execute(
            """
            SELECT j.id, j.company, j.role, j.ats, j.source_status,
                   a.state, a.last_error, a.approval_expires_at, a.updated_at
            FROM jobs j JOIN applications a ON a.job_id=j.id
            ORDER BY a.updated_at DESC, j.company, j.role
            """
        ).fetchall()
        return [dict(row) for row in rows]
