# The internship market, measured

The daily watcher commits `tracker.csv` every morning, so the repository's git
history is already a daily snapshot of every role it tracks. This package
replays that history into a DuckDB warehouse, models it in SQL, and measures
how long roles stay open, when firms post them, and whether you can tell which
will close first.

The published write-up is [`docs/market.html`](../docs/market.html)
([live](https://abyyworld.github.io/internship-tracker/market.html)). It is
rebuilt after every daily watch by `.github/workflows/market.yml`.

## Run it

```bash
git fetch --unshallow                      # every day's tracker.csv, not just today's
pip install -r requirements-market.txt
python -m market.backfill                  # git history -> market/warehouse.duckdb
python -m market.analysis                  # -> market/results.json
python -m market.report                    # -> docs/market.html
python -m unittest tests.test_market       # the model tests (DuckDB needed)
```

The warehouse and the per-day extracts under `market/.cache/` are not
committed; they rebuild from git in seconds. `results.json` and the report are.

## The warehouse

| Table | Grain | What it holds |
|--|--|--|
| `raw.snapshot` | role × day | every committed `tracker.csv`, as text, one per UTC day (the last commit that day) |
| `raw.coverage_change` | day | snapshots that first reflect a change to the scraper code |
| `stg.snapshot` | role × day | typed postings only; watchlists and July's personal columns dropped; `status` = open / closed / stale |
| `int.id_alias` | watcher id | retitled roles stitched to their first id by URL |
| `int.source_start` | source | the first day each board or list was watched |
| `mart.role_day` | role × day | **the daily table**: one row per role per day it was listed |
| `mart.role` | role | company, sector, tier, region, sponsorship, `opened_on`, `closed_on`, `duration_days`, `closed`, `fresh` |
| `mart.daily_market` | day × sector | open, new and closed counts |

Decisions the SQL makes (each one has a test in `tests/test_market.py`):

- **Closed** means the tracker confirmed the role gone on two healthy runs and
  it never came back. The close date is the first morning it was missing.
- A role whose source was **failing** is never closed. It, and anything still
  open, is censored at the last day it was seen open.
- **Fresh** roles appeared on a source that was already being watched, on a day
  the scraper code did not change. Only for those is the first-listed date a
  posting date, so only those enter the duration, timing and forecast
  analysis. The rest were already open when the tracker started looking.

## The analysis

- **Survival.** Kaplan–Meier curves by sector, role type, company size,
  prestige tier, listing source and region, with log-rank tests; a Cox model
  with all of them together, with a proportional-hazards check per factor.
- **Timing.** New roles per week and weekday on a fixed panel of sources
  watched from the start, so boards added later do not read as new postings.
  The weekday is shifted one day back because the watcher runs at 07:00 UTC.
- **Sponsorship.** What the postings say, by sector, and how little of it
  there is.
- **Forecast.** P(closes within 14 days) from what an advert says on its first
  day. Training labels come from a warehouse rebuilt from only the snapshots
  that existed on the cutoff day; the test set is the roles posted after it.
  Base rate, logistic regression, gradient boosting and a Cox model compete on
  AUC, Brier score and log loss.

## Limits worth stating

- Coverage is mostly US; UK roles are about 5% of the dated ones.
- A community list closing a role means the listing went away, which is close
  to, but not always the same as, the employer closing applications.
- Sponsorship is stated on about 1% of postings, so it is reported as a
  coverage figure, not compared across sectors.
