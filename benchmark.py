#!/usr/bin/env python3
"""Measure what a model is actually worth for this job, on your own account.

Model choice is usually argued from benchmarks that have nothing to do with
rewriting a CV. This runs the real thing — a full tailoring of your CV against
a real posting — and reports what came back and what it cost in tokens, so a
free tier and a paid one can be compared on the same evidence.

Token counts are exact, taken from each provider's own usage field. Prices are
not hard-coded here because they change; multiply the tokens by whatever the
provider's page says today.

    python3 benchmark.py                      # the configured model
    python3 benchmark.py gpt-5.4 gpt-5.6-sol  # compare several
    python3 benchmark.py --job "Neuralink"    # pick the posting by name
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def main() -> int:
    import yaml

    from autoapply import openai_tailoring as ai
    from autoapply.config import database_path
    from autoapply.cv_editor import master_document, ordered_sections
    from autoapply.store import Store
    from dashboard import load_jobs

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("models", nargs="*", help="models to compare")
    parser.add_argument("--job", default="", help="match a posting by company or role")
    parser.add_argument("--mode", default="full",
                        choices=("targeted", "full", "aggressive"))
    parser.add_argument("--instructions", default="")
    parser.add_argument("--home", default=str(ROOT / "private"))
    args = parser.parse_args()

    home = Path(args.home)
    base_url = ai.load_base_url(home)
    try:
        api_key = ai.load_key_for(home)
    except FileNotFoundError:
        print("No key configured for", base_url)
        return 1

    jobs = load_jobs()
    wanted = args.job.lower()
    matches = [
        job for job in jobs
        if not wanted or wanted in f"{job['company']} {job['role']}".lower()
    ]
    if not matches:
        print(f"No posting matches {args.job!r}")
        return 1
    posting = matches[0]

    profile = yaml.safe_load((home / "profile.yaml").read_text(encoding="utf-8"))
    facts = yaml.safe_load((home / "resume_facts.yaml").read_text(encoding="utf-8"))
    document = master_document(profile, facts)
    total_lines = len(document["fact_ids"])

    with Store(database_path(home)) as store:
        job = store.find_job_by_url(posting["url"])

    models = args.models or [ai.load_model(home)]
    print(f"posting  : {posting['company']} — {posting['role']}")
    print(f"endpoint : {base_url}")
    print(f"CV       : {total_lines} lines, mode {args.mode}\n")
    header = (
        f"{'model':22}{'time':>7}{'rewritten':>12}{'summary':>9}"
        f"{'in tok':>10}{'out tok':>10}  order"
    )
    print(header)
    print("-" * len(header))

    for model in models:
        started = time.time()
        try:
            with ai.track_usage() as usage:
                draft = ai.generate_suggestions(
                    job, document,
                    api_key=api_key, model=model, mode=args.mode,
                    instructions=args.instructions, timeout=300,
                    base_url=base_url,
                )
                counted = usage()
        except Exception as exc:  # a provider that cannot do the job is a result
            print(f"{model:22}{time.time() - started:6.0f}s  failed: {str(exc)[:60]}")
            continue
        order = " → ".join(
            section["name"] for section in ordered_sections(document, draft)
        )
        print(
            f"{model:22}{time.time() - started:6.0f}s"
            f"{len(draft['bullets']):>8}/{total_lines:<3}"
            f"{'yes' if draft['summary'] else 'no':>9}"
            f"{counted.get('input', 0):>10,}{counted.get('output', 0):>10,}"
            f"  {order[:44]}"
        )
    print(
        "\nMultiply the token columns by your provider's per-million price to "
        "get the cost of one tailoring."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
