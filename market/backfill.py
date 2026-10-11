"""Replay every committed tracker.csv into a DuckDB warehouse.

The daily watcher commits tracker.csv once a day, so the repository's own
history is already a daily snapshot archive. This module reads one version per
day out of git (the last commit that day, so a manual rerun replaces the
scheduled one rather than counting as a second day), keeps it as a plain CSV
under market/.cache/snapshots/, and loads them all into raw.snapshot.

Nothing here is ever committed: the warehouse can always be rebuilt from git.

Run:   python -m market.backfill            # incremental
       python -m market.backfill --rebuild  # re-extract every day
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKER = "tracker.csv"
CACHE_DIR = ROOT / "market" / ".cache" / "snapshots"
WAREHOUSE = ROOT / "market" / "warehouse.duckdb"
MODELS = ROOT / "market" / "models.sql"
# tracker.csv columns that models.sql reads.
STAGED_COLUMNS = (
    "id", "url", "company", "role", "category", "region", "company_type",
    "elite_tier", "role_type", "term", "level", "sponsorship", "citizenship",
    "work_mode", "sources", "source_status", "record_kind", "first_seen", "deadline",
)
# Code that decides which roles reach tracker.csv. A change to any of these
# can surface roles that were already live, so the day it first reaches the
# tracker is a coverage change, not a day of postings.
SCRAPER_FILES = (
    "internship_watcher.py", "board_discovery.py", "board_harvest.py",
    "uk_listings.py", "config",
)


def git(*args, cwd=ROOT):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True,
        env={**os.environ, "TZ": "UTC"},
    ).stdout


def daily_commits(cwd=ROOT, path=TRACKER):
    """Return [(date, sha)] oldest first, one commit per UTC day.

    git log lists newest first, so the first commit seen for a date is the
    last one made that day — the state the tracker ended the day in.
    """
    out = git(
        "log", "--format=%H %ad", "--date=format-local:%Y-%m-%d",
        "--", path, cwd=cwd,
    ).decode()
    by_day = {}
    for line in out.splitlines():
        sha, day = line.split()
        by_day.setdefault(day, sha)
    return sorted((day, sha) for day, sha in by_day.items())


def coverage_changes(commits, cwd=ROOT):
    """Return sorted snapshot dates that first reflect a scraper code change.

    commits is daily_commits() output. A code change is any commit to
    SCRAPER_FILES other than the bot's daily "watcher: update"; it takes effect
    in the first daily snapshot committed at or after it.
    """
    out = git("log", "--format=%H %ct %s", "--", *SCRAPER_FILES, cwd=cwd).decode()
    changes = []
    for line in out.splitlines():
        _, stamp, subject = (line.split(maxsplit=2) + [""])[:3]
        if not subject.startswith("watcher: update"):
            changes.append(int(stamp))
    stamps = [(int(git("show", "-s", "--format=%ct", sha, cwd=cwd)), day)
              for day, sha in commits]
    days = set()
    for t in changes:
        later = [day for stamp, day in stamps if stamp >= t]
        if later:
            days.add(later[0])
    return sorted(days)


def extract(commits, cache_dir=CACHE_DIR, cwd=ROOT, path=TRACKER, rebuild=False):
    """Write each day's tracker.csv to cache_dir/<date>.csv. Returns new dates."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    manifest = cache_dir / "manifest.tsv"
    known = {}
    if manifest.exists() and not rebuild:
        for line in manifest.read_text().splitlines():
            day, sha = line.split("\t")
            known[day] = sha
    written = []
    for day, sha in commits:
        target = cache_dir / f"{day}.csv"
        if known.get(day) == sha and target.exists():
            continue
        target.write_bytes(git("show", f"{sha}:{path}", cwd=cwd))
        known[day] = sha
        written.append(day)
    manifest.write_text("".join(f"{d}\t{s}\n" for d, s in sorted(known.items())))
    (cache_dir / "coverage_changes.txt").write_text(
        "".join(f"{d}\n" for d in coverage_changes(commits, cwd=cwd)))
    return written


def load(con, cache_dir=CACHE_DIR, models=MODELS):
    """(Re)load raw.snapshot from the cached CSVs and rebuild the models.

    The tracker gained columns over the summer (record_kind, last_healthy_miss,
    …), so the files are read by name and every value is kept as text; the
    staging model is where types are decided.
    """
    pattern = str(cache_dir / "*.csv").replace("'", "''")
    manifest = str(cache_dir / "manifest.tsv").replace("'", "''")
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")
    con.execute(f"""
        CREATE OR REPLACE TABLE raw.snapshot AS
        SELECT CAST(regexp_extract(filename, '(\\d{{4}}-\\d{{2}}-\\d{{2}})\\.csv$', 1)
                    AS DATE) AS snapshot_date,
               * EXCLUDE (filename)
        FROM read_csv('{pattern}', union_by_name = true, all_varchar = true,
                      filename = true, header = true)
    """)
    # A column the tracker has not written yet (or wrote only later) still
    # exists, empty, so the staging model never has to guess.
    for column in STAGED_COLUMNS:
        con.execute(f'ALTER TABLE raw.snapshot ADD COLUMN IF NOT EXISTS "{column}" VARCHAR')
    con.execute(f"""
        CREATE OR REPLACE TABLE raw.snapshot_manifest AS
        SELECT CAST(column0 AS DATE) AS snapshot_date, column1 AS commit_sha
        FROM read_csv('{manifest}', delim = '\t', header = false,
                      columns = {{'column0': 'VARCHAR', 'column1': 'VARCHAR'}})
    """)
    changes = cache_dir / "coverage_changes.txt"
    days = changes.read_text().split() if changes.exists() else []
    con.execute("CREATE OR REPLACE TABLE raw.coverage_change (snapshot_date DATE)")
    if days:
        con.executemany("INSERT INTO raw.coverage_change VALUES (?)", [[d] for d in days])
    con.execute(Path(models).read_text())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--rebuild", action="store_true",
                        help="re-extract every day from git")
    parser.add_argument("--db", default=str(WAREHOUSE))
    args = parser.parse_args(argv)

    import duckdb

    if git("rev-parse", "--is-shallow-repository").strip() == b"true":
        sys.exit("This clone is shallow; run `git fetch --unshallow` first so "
                 "every daily tracker.csv is available.")
    commits = daily_commits()
    written = extract(commits, rebuild=args.rebuild)
    con = duckdb.connect(args.db)
    load(con)
    days, rows = con.execute(
        "SELECT count(DISTINCT snapshot_date), count(*) FROM raw.snapshot"
    ).fetchone()
    roles = con.execute("SELECT count(*) FROM mart.role").fetchone()[0]
    print(f"{len(written)} new day(s) extracted; warehouse holds {days} days, "
          f"{rows} snapshot rows, {roles} roles -> {args.db}")


if __name__ == "__main__":
    main()
