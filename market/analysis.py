"""Measure the market held in the warehouse and write market/results.json.

  1. How long roles stay open   Kaplan–Meier curves, log-rank tests, Cox model
  2. When firms post            new roles per week and weekday, on a fixed panel
  3. Sponsorship                what the sources actually say, by sector
  4. Forecast                   P(closes within N days), trained on the past
                                and scored on later roles it never saw

Only "fresh" roles enter 1, 2 and 4: roles that appeared on a source the
tracker was already watching, on a day the scraper code did not change. For
those, the day first seen is (to within a day) the day posted. Everything else
was already open when the tracker started looking and its age is unknown.

Run:   python -m market.analysis   (after python -m market.backfill)
"""

import argparse
import json
import math
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from market.backfill import MODELS, WAREHOUSE
from market.report import RESULTS
HORIZON = 14            # forecast: closes within this many days
MIN_GROUP = 100         # smaller categories fold into "Other" (8 series at most)
KM_DAYS = 60            # curves are reported out to this many days
MIN_AT_RISK = 50        # ...or until fewer roles than this are still at risk

ROLE_GROUP = {
    "intern": "Internship", "internship": "Internship", "co-op": "Internship",
    "new-grad": "New grad", "entry-level": "New grad", "graduate": "New grad",
    "phd-fellowship": "Research / PhD", "research-assistant": "Research / PhD",
    "fellowship": "Research / PhD", "postdoc": "Research / PhD",
}


# ── data ────────────────────────────────────────────────────────────────────
def roles(con):
    df = con.execute("""
        SELECT role_key, company, title, category, region, elite_tier, role_type,
               term, sponsorship, source_family, company_roles, opened_on,
               closed_on, closed, duration_days, fresh, deadline
        FROM mart.role
    """).df()
    return prepare(df)


def prepare(df):
    df = df.copy()
    df["opened_on"] = pd.to_datetime(df["opened_on"])
    df["closed"] = df["closed"].astype(bool)
    df["fresh"] = df["fresh"].astype(bool)
    # role_type "other" is nearly all "Software Engineer 1" / "Junior …"
    # adverts from the new-grad list that the watcher did not tag new-grad.
    df["role_group"] = df["role_type"].map(ROLE_GROUP).fillna("Junior full-time")
    df["region_group"] = np.select(
        [df["region"].str.startswith("US"), df["region"].str.contains("UK"),
         df["region"] == "Canada"],
        ["US", "UK", "Canada"], "Elsewhere / unknown")
    df["tier"] = df["elite_tier"].map(
        {"elite": "Elite", "high": "High"}).fillna("Unranked")
    df["company_size"] = pd.cut(
        df["company_roles"], [0, 4, 19, math.inf],
        labels=["1–4 roles", "5–19 roles", "20+ roles"]).astype(str)
    df["term_group"] = np.select(
        [df["term"].str.contains("2027"), df["term"].str.contains("New Grad")],
        ["2027 start", "New grad 2026"], "Other / unstated")
    # The watcher runs at 07:00 UTC, so a role first listed on day d went up
    # during day d-1 in the Americas, where most of these employers are.
    df["posted_weekday"] = (df["opened_on"] - pd.Timedelta(days=1)).dt.day_name()
    return df


def fold_categories(df, column="category", min_group=MIN_GROUP):
    counts = df[column].value_counts()
    keep = counts[counts >= min_group].index
    return df[column].where(df[column].isin(keep), "Other")


# ── 1. survival ─────────────────────────────────────────────────────────────
def km_curve(durations, events, label):
    from lifelines import KaplanMeierFitter

    kmf = KaplanMeierFitter().fit(durations, events, label=label)
    sf = kmf.survival_function_.iloc[:, 0]
    ci = kmf.confidence_interval_survival_function_
    points = []
    for t in range(0, KM_DAYS + 1):
        # past this point a handful of old roles move the curve by whole steps
        at_risk = int((durations >= t).sum())
        if at_risk < MIN_AT_RISK:
            break
        i = sf.index[sf.index <= t].max()
        points.append({"t": t, "s": round(float(sf[i]), 4),
                       "lo": round(float(ci.iloc[:, 0][i]), 4),
                       "hi": round(float(ci.iloc[:, 1][i]), 4),
                       "at_risk": at_risk})
    median = kmf.median_survival_time_
    horizon = points[-1]["t"]
    if median > horizon:
        median = math.inf
    return {
        "label": label, "n": int(len(durations)), "events": int(events.sum()),
        "median_days": None if math.isinf(median) else float(median),
        "open_after_14": surv_at(sf, 14, horizon), "open_after_30": surv_at(sf, 30, horizon),
        "points": points,
    }


def surv_at(sf, t, horizon):
    if horizon < t:
        return None
    return round(float(sf[sf.index[sf.index <= t].max()]), 4)


def km_by(df, column, order=None):
    from lifelines.statistics import multivariate_logrank_test

    groups = order or df[column].value_counts().index.tolist()
    curves = [km_curve(df.loc[df[column] == g, "duration_days"],
                       df.loc[df[column] == g, "closed"], str(g))
              for g in groups if (df[column] == g).sum() >= 20]
    test = multivariate_logrank_test(df["duration_days"], df[column], df["closed"])
    return {"by": column, "curves": curves,
            "logrank_p": float(test.p_value), "logrank_chi2": float(test.test_statistic)}


COX_COVARIATES = {
    # column: reference level
    "category_group": "Software Engineering",
    "role_group": "Internship",
    "region_group": "US",
    "tier": "Unranked",
    "company_size": "1–4 roles",
    "source_family": "community list",
}


def design(df, columns=COX_COVARIATES, levels=None):
    """One-hot encode with fixed reference levels; returns (X, levels)."""
    levels = levels or {c: sorted(set(df[c]) - {ref}) for c, ref in columns.items()}
    X = pd.DataFrame(index=df.index)
    for column, values in levels.items():
        for value in values:
            X[f"{column}={value}"] = (df[column] == value).astype(float)
    return X, levels


def cox(df):
    from lifelines import CoxPHFitter
    from lifelines.statistics import proportional_hazard_test

    X, _ = design(df)
    X = X.loc[:, X.sum() >= 15]          # too few roles to estimate a hazard
    data = X.assign(duration=df["duration_days"], event=df["closed"].astype(int))
    fit = CoxPHFitter(penalizer=0.01).fit(data, "duration", "event")
    summary = fit.summary
    ph = proportional_hazard_test(fit, data, time_transform="rank").summary
    rows = []
    for name in summary.index:
        column, value = name.split("=", 1)
        rows.append({
            "covariate": column, "level": value,
            "reference": COX_COVARIATES[column],
            "n": int(X[name].sum()),
            "hr": round(float(summary.loc[name, "exp(coef)"]), 3),
            "lo": round(float(summary.loc[name, "exp(coef) lower 95%"]), 3),
            "hi": round(float(summary.loc[name, "exp(coef) upper 95%"]), 3),
            "p": float(summary.loc[name, "p"]),
            "ph_p": float(ph.loc[name, "p"]),
        })
    return {"rows": rows, "concordance": round(float(fit.concordance_index_), 3),
            "n": int(len(data)), "events": int(data["event"].sum()),
            "penalizer": 0.01}


# ── 2. timing ───────────────────────────────────────────────────────────────
def timing(con, df):
    """New roles per ISO week, on sources watched since the panel start.

    The tracker added sources all summer, so raw weekly counts mostly measure
    the tracker. Holding the source panel fixed leaves the market.
    """
    first_day = df["opened_on"].min()
    panel_start = (first_day + pd.Timedelta(days=14)).date()
    panel = con.execute("""
        SELECT DISTINCT r.role_key
        FROM mart.role r, unnest(string_split(r.all_sources, ',')) AS t(source)
        JOIN int.source_start s ON s.source = trim(t.source)
        WHERE s.first_watched <= ?
    """, [panel_start]).df()["role_key"]
    p = df[df["fresh"] & df["role_key"].isin(panel)
           & (df["opened_on"].dt.date > panel_start)].copy()
    p["week"] = p["opened_on"].dt.to_period("W-SUN").dt.start_time
    p["category_group"] = fold_categories(p)
    last = df["opened_on"].max()
    complete = p["week"] + pd.Timedelta(days=6) <= last
    weekly = (p[complete].groupby(["week", "category_group"]).size()
              .unstack(fill_value=0).sort_index())
    order = weekly.sum().sort_values(ascending=False).index.tolist()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday"]
    by_day = p["posted_weekday"].value_counts().reindex(weekdays, fill_value=0)
    # which sectors open first: the date by which each had posted half of its
    # panel roles for 2027 starts
    half = {}
    for cat, g in p[p["term_group"] == "2027 start"].groupby("category_group"):
        if len(g) >= 20:
            d = g["opened_on"].sort_values().iloc[len(g) // 2]
            half[cat] = {"n": int(len(g)), "half_posted_by": d.date().isoformat()}
    return {
        "panel_start": panel_start.isoformat(),
        "panel_roles": int(len(p)),
        "weeks": [w.date().isoformat() for w in weekly.index],
        "series": [{"label": c, "values": [int(v) for v in weekly[c]]} for c in order],
        "weekday": [{"day": d, "roles": int(by_day[d])} for d in weekdays],
        "half_posted": dict(sorted(half.items(), key=lambda kv: kv[1]["half_posted_by"])),
    }


# ── 3. sponsorship ──────────────────────────────────────────────────────────
def sponsorship(con):
    rows = con.execute("""
        SELECT category,
               count(*)                                         AS roles,
               count(*) FILTER (WHERE sponsorship = 'yes')      AS sponsors,
               count(*) FILTER (WHERE sponsorship IN ('no', 'unavailable')) AS no_sponsorship,
               count(*) FILTER (WHERE sponsorship = 'unknown')  AS unknown,
               count(*) FILTER (WHERE citizenship <> 'unknown') AS citizenship_required
        FROM (SELECT r.category, r.sponsorship,
                     (SELECT arg_max(citizenship, snapshot_date) FROM mart.role_day d
                      WHERE d.role_key = r.role_key) AS citizenship
              FROM mart.role r)
        GROUP BY 1 ORDER BY roles DESC
    """).df()
    total = rows[["roles", "sponsors", "no_sponsorship", "unknown",
                  "citizenship_required"]].sum()
    return {
        "rows": rows.to_dict("records"),
        "total": {k: int(v) for k, v in total.items()},
        "known_share": round(float(1 - total["unknown"] / total["roles"]), 4),
    }


# ── 4. forecast ─────────────────────────────────────────────────────────────
def as_of(warehouse_con, cutoff):
    """A warehouse rebuilt from only the snapshots up to cutoff (inclusive).

    Training labels must be what was knowable on the cutoff day: a role that
    looked closed then may have come back since.
    """
    import duckdb

    con = duckdb.connect()
    con.execute("CREATE SCHEMA raw")
    for table in ("snapshot", "coverage_change"):
        frame = warehouse_con.execute(
            f"SELECT * FROM raw.{table} WHERE snapshot_date <= ?", [cutoff]).df()
        con.register("frame", frame)
        con.execute(f"CREATE TABLE raw.{table} AS SELECT * FROM frame")
        con.unregister("frame")
    con.execute(Path(MODELS).read_text())
    return con


def label(df, horizon, last_day):
    """1 closed within horizon days, 0 seen open past it, NaN not yet known."""
    closed_in_time = df["closed"] & (df["duration_days"] <= horizon)
    survived = df["duration_days"] > horizon
    known = df["opened_on"] + pd.Timedelta(days=horizon) <= pd.Timestamp(last_day)
    y = pd.Series(np.nan, index=df.index)
    y[known & survived] = 0.0
    y[closed_in_time] = 1.0
    y[~known & ~closed_in_time] = np.nan
    return y


def features(df, history):
    """Posting-time features only. Company volume counts earlier openings."""
    out = df.copy()
    out["category_group"] = out["category"].where(
        out["category"].isin(history["category_group_levels"]), "Other")
    prior = history["openings"]
    out["company_prior_roles"] = [
        int(((prior["company"] == c) & (prior["opened_on"] < d)).sum())
        for c, d in zip(out["company"], out["opened_on"])]
    out["log_company_prior"] = np.log1p(out["company_prior_roles"])
    out["opened_weekend"] = out["opened_on"].dt.dayofweek >= 5
    out["has_deadline"] = out["deadline"].notna()
    return out


FORECAST_COLUMNS = {
    "category_group": "Software Engineering", "role_group": "Internship",
    "region_group": "US", "tier": "Unranked", "source_family": "community list",
    "term_group": "2027 start",
}


def matrix(df, levels=None):
    X, levels = design(df, FORECAST_COLUMNS, levels)
    X["log_company_prior"] = df["log_company_prior"]
    X["opened_weekend"] = df["opened_weekend"].astype(float)
    X["has_deadline"] = df["has_deadline"].astype(float)
    return X, levels


def forecast(warehouse_con, full, horizon=HORIZON):
    from lifelines import CoxPHFitter
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score

    last_day = full["opened_on"].max().date()
    # Test roles need horizon days of follow-up before the last snapshot;
    # the cutoff leaves the last four weeks of openings for testing.
    test_end = last_day - timedelta(days=horizon)
    cutoff = test_end - timedelta(days=14)

    known = prepare(roles(as_of(warehouse_con, cutoff)))
    past = known[known["fresh"]].copy()
    train = past[past["opened_on"].dt.date <= cutoff - timedelta(days=horizon)].copy()
    train["y"] = label(train, horizon, cutoff)
    train = train.dropna(subset=["y"])

    test = full[full["fresh"] & (full["opened_on"].dt.date > cutoff)
                & (full["opened_on"].dt.date <= test_end)].copy()
    test["y"] = label(test, horizon, last_day)
    test = test.dropna(subset=["y"])

    counts = train["category"].value_counts()
    # company volume counts every role listed earlier, fresh or not, in both
    history_train = {"openings": known[["company", "opened_on"]],
                     "category_group_levels": set(counts[counts >= 30].index)}
    history_test = {"openings": full[["company", "opened_on"]],
                    "category_group_levels": history_train["category_group_levels"]}
    train = features(train, history_train)
    test = features(test, history_test)
    Xtr, levels = matrix(train)
    Xte, _ = matrix(test, levels)
    keep = Xtr.columns[Xtr.std() > 0]
    Xtr, Xte = Xtr[keep], Xte[keep]
    ytr, yte = train["y"].astype(int), test["y"].astype(int)

    preds = {"Base rate": np.full(len(test), ytr.mean())}
    logit = LogisticRegression(C=1.0, max_iter=2000).fit(Xtr, ytr)
    preds["Logistic regression"] = logit.predict_proba(Xte)[:, 1]
    gbm = HistGradientBoostingClassifier(
        max_depth=3, learning_rate=0.05, max_iter=300, random_state=0).fit(Xtr, ytr)
    preds["Gradient boosting"] = gbm.predict_proba(Xte)[:, 1]
    # Cox is fitted on every fresh role known at the cutoff, censoring included —
    # the survival model's advantage is that it uses roles still open.
    past = features(past, history_train)
    Xpast, _ = matrix(past, levels)
    data = Xpast[keep].assign(duration=past["duration_days"],
                              event=past["closed"].astype(int))
    data = data.loc[:, (data != 0).any()]
    coxfit = CoxPHFitter(penalizer=0.05).fit(data, "duration", "event")
    sf = coxfit.predict_survival_function(Xte[data.columns.drop(["duration", "event"])],
                                          times=[horizon])
    preds["Cox model"] = 1 - sf.iloc[0].to_numpy()

    metrics = []
    for name, p in preds.items():
        p = np.clip(p, 1e-4, 1 - 1e-4)
        metrics.append({
            "model": name,
            "auc": None if name == "Base rate" else round(float(roc_auc_score(yte, p)), 3),
            "brier": round(float(brier_score_loss(yte, p)), 4),
            "log_loss": round(float(log_loss(yte, p)), 4),
        })
    best = min((m for m in metrics if m["model"] != "Base rate"),
               key=lambda m: m["brier"])["model"]
    p = preds[best]
    bins = np.clip((p * 10).astype(int), 0, 9)
    calibration = []
    for b in range(10):
        mask = bins == b
        if mask.sum() >= 10:
            calibration.append({"predicted": round(float(p[mask].mean()), 3),
                                "observed": round(float(yte[mask].mean()), 3),
                                "n": int(mask.sum())})
    return {
        "horizon_days": horizon, "cutoff": cutoff.isoformat(),
        "train": {"opened_through": (cutoff - timedelta(days=horizon)).isoformat(),
                  "labelled_as_of": cutoff.isoformat(), "n": int(len(train)),
                  "closed_share": round(float(ytr.mean()), 3)},
        "test": {"opened_from": (cutoff + timedelta(days=1)).isoformat(),
                 "opened_through": test_end.isoformat(),
                 "labelled_as_of": last_day.isoformat(), "n": int(len(test)),
                 "closed_share": round(float(yte.mean()), 3)},
        "metrics": metrics, "best": best, "calibration": calibration,
    }


# ── put together ────────────────────────────────────────────────────────────
def analyse(con):
    df = roles(con)
    fresh = df[df["fresh"]].copy()
    fresh["category_group"] = fold_categories(fresh)
    meta = con.execute("""
        SELECT min(snapshot_date), max(snapshot_date), count(DISTINCT snapshot_date),
               count(*) FROM raw.snapshot
    """).fetchone()
    overall = km_curve(fresh["duration_days"], fresh["closed"], "All fresh roles")
    category_order = (fresh["category_group"].value_counts()
                      .drop("Other", errors="ignore").index.tolist() + ["Other"])
    return {
        "meta": {
            "built": date.today().isoformat(),
            "first_snapshot": meta[0].isoformat(), "last_snapshot": meta[1].isoformat(),
            "snapshots": int(meta[2]), "snapshot_rows": int(meta[3]),
            "roles": int(len(df)), "fresh_roles": int(len(fresh)),
            "fresh_closed": int(fresh["closed"].sum()),
            "closed_roles": int(df["closed"].sum()),
            "stitched_ids": int(con.execute(
                "SELECT count(*) FROM int.id_alias WHERE watcher_id <> role_key"
            ).fetchone()[0]),
            "coverage_change_days": [d.isoformat() for (d,) in con.execute(
                "SELECT snapshot_date FROM raw.coverage_change ORDER BY 1").fetchall()],
        },
        "survival": {
            "overall": overall,
            "by_category": km_by(fresh, "category_group", category_order),
            "by_role_group": km_by(fresh, "role_group"),
            "by_tier": km_by(fresh, "tier", ["Elite", "High", "Unranked"]),
            "by_company_size": km_by(fresh, "company_size",
                                     ["1–4 roles", "5–19 roles", "20+ roles"]),
            "by_source_family": km_by(fresh, "source_family"),
            "by_region": km_by(fresh, "region_group"),
        },
        # the forest plot has no colour budget, so it keeps sectors down to 60
        "cox": cox(fresh.assign(category_group=fold_categories(fresh, min_group=60))),
        "timing": timing(con, df),
        "sponsorship": sponsorship(con),
        "forecast": forecast(con, df),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--db", default=str(WAREHOUSE))
    parser.add_argument("--out", default=str(RESULTS))
    args = parser.parse_args(argv)

    import duckdb

    con = duckdb.connect(args.db, read_only=True)
    results = analyse(con)
    Path(args.out).write_text(json.dumps(results, indent=1, default=str) + "\n")
    s = results["survival"]["overall"]
    f = results["forecast"]
    print(f"{results['meta']['fresh_roles']} fresh roles, median open "
          f"{s['median_days']} days; best {f['horizon_days']}-day forecast: {f['best']} "
          f"-> {args.out}")


if __name__ == "__main__":
    main()
