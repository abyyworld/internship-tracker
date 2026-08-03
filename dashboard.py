#!/usr/bin/env python3
"""Build the public, filterable GitHub Pages job dashboard."""

from __future__ import annotations

import csv
from datetime import date
import json
from pathlib import Path
from urllib.parse import urlsplit

import scorecard
from funding import load_schemes
from source_health import alerts as health_alerts, summary as health_summary
from universities import _index, annotate, load_universities


ROOT = Path(__file__).resolve().parent
TRACKER = ROOT / "tracker.csv"
OUTPUT = ROOT / "docs" / "index.html"
ATS_SUFFIXES = ("greenhouse.io", "lever.co", "ashbyhq.com")

# Categories the dashboard chips can filter on. Must stay in sync with
# CATEGORY_ORDER in the page template and category_of() in the watcher.
KNOWN_CATEGORIES = {
    "AI / ML",
    "Software Engineering",
    "Quant / Finance",
    "Robotics & Embodied AI",
    "Security",
    "Data",
    "Systems & Infra",
    "Hardware / EE",
    "HCI / XR",
    "Computational Science",
}

# Rows scraped before the category rename keep their old label. Without this
# map their chip never matches and the jobs become unreachable by any filter.
LEGACY_CATEGORIES = {
    "Quant": "Quant / Finance",
    "HCI": "HCI / XR",
    "Robotics": "Robotics & Embodied AI",
    "Bioinformatics": "Computational Science",
    "Systems": "Systems & Infra",
    "Hardware": "Hardware / EE",
}


def normalize_tier(company: str, stored: str) -> str:
    """Recompute a row's tier from the current watchlists.

    Tier is written when a row is scraped, so a row discovered before the
    tiers were rebalanced keeps its old value — which is how every FAANG
    posting stayed on "high" while smaller firms showed as "elite".
    """
    try:
        from internship_watcher import tier_of
    except Exception:
        return (stored or "").strip()
    return tier_of(company or "") or ""


def normalize_category(stored: str, company: str, role: str) -> str:
    """Map a tracker row onto a current chip label.

    Rows keep whatever category the watcher assigned when it scraped them, so
    after a rename or a new category is added the stored value can be stale.
    Renames are mapped directly; anything still unrecognised is reclassified
    with the watcher's own classifier so there is a single source of truth.
    """
    value = (stored or "").strip()
    if value in KNOWN_CATEGORIES:
        return value
    if value in LEGACY_CATEGORIES:
        return LEGACY_CATEGORIES[value]
    try:
        from internship_watcher import category_of
    except Exception:
        return value or "Software Engineering"
    return category_of(company, role)


def safe_url(value: str) -> str:
    candidate = (value or "").strip()
    try:
        parsed = urlsplit(candidate)
    except ValueError:
        return ""
    if parsed.scheme != "https" or not parsed.hostname:
        return ""
    return candidate


def ats_supported(value: str) -> bool:
    hostname = (urlsplit(value).hostname or "").lower()
    return any(
        hostname == suffix or hostname.endswith(f".{suffix}")
        for suffix in ATS_SUFFIXES
    )


def load_jobs() -> list[dict[str, object]]:
    with TRACKER.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row.get("record_kind", "posting") == "posting"
            and row.get("source_status") == "open"
        ]
    # Academic postings rarely name a supervisor, so match the institution once
    # and let each such job carry links to its real, current faculty.
    index = _index(load_universities())
    campuses = scorecard.index()
    jobs: list[dict[str, object]] = []
    for row in rows:
        url = safe_url(row.get("url", ""))
        jobs.append(
            {
                "id": row.get("id", ""),
                "company": row.get("company", ""),
                "role": row.get("role", ""),
                "category": normalize_category(
                    row.get("category", ""),
                    row.get("company", ""),
                    row.get("role", ""),
                ),
                "position_type": row.get("role_type", ""),
                "region": row.get("region", "Unknown"),
                "location": row.get("location", ""),
                "term": row.get("term", "Unknown"),
                "level": row.get("level", "Unknown"),
                "work_mode": row.get("work_mode", "unspecified"),
                "tier": normalize_tier(
                    row.get("company", ""), row.get("elite_tier", "")
                ),
                "focus": row.get("focus_tags", ""),
                "company_type": row.get("company_type", "unknown"),
                "company_signal": row.get("company_signal", ""),
                "equity_signal": row.get("equity_signal", "unknown"),
                "eligibility": row.get("eligibility", "review required"),
                "deadline": row.get("deadline", ""),
                "first_seen": row.get("first_seen", ""),
                "last_seen": row.get("last_seen", ""),
                # fix: column is "NEW" (all-caps), not "discovered_new"
                "new": row.get("NEW", "").upper() == "YES",
                "url": url,
                "tailor": bool(url),
                "official_ats": bool(url and ats_supported(url)),
            }
        )
        annotate(jobs[-1], index)
        university = jobs[-1].get("university")
        if university and university.get("country") == "United States":
            figures = scorecard.lookup(university["name"], campuses)
            if figures:
                university["scorecard"] = {
                    "admission_rate": figures.get("admission_rate"),
                    "students": figures.get("students"),
                    "tuition": figures.get("tuition_out_of_state"),
                    "earnings": figures.get("earnings_10yr_median"),
                    "summary": scorecard.describe(figures),
                }
    return jobs


def json_for_script(value: object) -> str:
    return (
        json.dumps(value, ensure_ascii=True, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def build() -> int:
    jobs = load_jobs()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    # Reliability is published deliberately. A job dataset nobody audits is
    # worth nothing, and the failures here are the kind that hide.
    health = {"summary": health_summary(), "alerts": health_alerts()[:8]}
    # Funding is listed for everyone rather than matched here: matching needs
    # the private profile, and this page is public.
    schemes = [
        {
            key: value for key, value in scheme.items()
            if key in {"id", "name", "funder", "country", "levels", "eligibility",
                       "covers", "cycle", "url"}
        }
        for scheme in load_schemes()
    ]
    page = (
        TEMPLATE.replace("__JOBS__", json_for_script(jobs))
        .replace("__HEALTH__", json_for_script(health))
        .replace("__FUNDING__", json_for_script(schemes))
        .replace("__GENERATED__", date.today().isoformat())
    )
    OUTPUT.write_text(page, encoding="utf-8")
    return len(jobs)


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Filter internships, research positions, PhD fellowships, and new-grad roles worldwide. Review AI-tailored CV edits locally, then apply.">
<title>Role Radar · Internships · Research · PhD · New Grad</title>
<style>
:root{
  color-scheme:dark;
  --bg:#07110f;--panel:#0e1b18;--panel2:#13231f;--line:#284139;
  --text:#f1f8f5;--muted:#9bb1a9;--green:#70efad;--green2:#25b875;
  --amber:#f5c86b;--blue:#79b8ff;--red:#ff8b82;--purple:#c4a0ff;
  --shadow:0 18px 55px #0007;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:
  radial-gradient(circle at 12% -5%,#164c3860 0,transparent 33rem),
  radial-gradient(circle at 92% 12%,#173c5860 0,transparent 31rem),var(--bg);
  color:var(--text);font:15px/1.45 Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
button,input,select{font:inherit}
button,a{outline-offset:3px}
.shell{width:min(1420px,calc(100% - 36px));margin:auto}
header{padding:38px 0 20px}
.eyebrow{display:flex;align-items:center;gap:9px;color:var(--green);font-weight:800;
  text-transform:uppercase;letter-spacing:.15em;font-size:11px}
.pulse{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 18px var(--green)}
.hero{display:flex;justify-content:space-between;gap:30px;align-items:flex-end;margin-top:14px}
h1{font-size:clamp(34px,6vw,68px);line-height:.95;letter-spacing:-.055em;margin:0;max-width:780px}
h1 span{color:var(--green)}
.intro{max-width:520px;color:var(--muted);font-size:16px;margin:0 0 4px}
.statusbar{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:28px 0 20px}
.stat{background:linear-gradient(145deg,#13241fdd,#0b1714dd);border:1px solid var(--line);
  border-radius:16px;padding:16px 18px;box-shadow:var(--shadow)}
.stat strong{font-size:27px;display:block;letter-spacing:-.04em}.stat span{color:var(--muted);font-size:12px}
.helper{display:flex;align-items:center;justify-content:space-between;gap:15px;padding:14px 16px;
  border:1px solid #396b55;border-radius:14px;background:#102b20;margin:0 0 14px}
.helper strong{color:var(--green)}.helper p{margin:2px 0;color:var(--muted);font-size:13px}
.helper a{white-space:nowrap}
.filters{position:sticky;top:0;z-index:20;background:#0b1714ee;backdrop-filter:blur(18px);
  border:1px solid var(--line);border-radius:18px;padding:14px;box-shadow:var(--shadow)}
.searchrow{display:grid;grid-template-columns:minmax(240px,1.8fr) repeat(5,minmax(125px,.7fr));gap:10px}
.control{height:43px;width:100%;border:1px solid var(--line);border-radius:10px;
  color:var(--text);background:#09130f;padding:0 12px}
.control:focus{border-color:var(--green2);box-shadow:0 0 0 3px #25b87522;outline:none}
.quick{display:flex;gap:8px;flex-wrap:wrap;margin-top:11px;align-items:center}
.chip{border:1px solid var(--line);border-radius:999px;background:transparent;color:var(--muted);
  padding:7px 11px;cursor:pointer;font-size:12px;font-weight:700}
.chip:hover,.chip.active{border-color:var(--green2);color:var(--green);background:#173327}
.chip.type-chip:hover,.chip.type-chip.active{border-color:var(--purple);color:var(--purple);background:#1d1530}
.quick-label{font-size:11px;color:var(--muted);font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;white-space:nowrap}
.quick-divider{width:1px;height:24px;background:var(--line);margin:0 4px}
.spacer{flex:1}.toggle{display:flex;align-items:center;gap:7px;color:var(--muted);font-size:12px;cursor:pointer}
.toggle input{accent-color:var(--green2);width:17px;height:17px}
.resultbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:24px 2px 8px}
.resultbar strong{font-size:21px}.resultbar span{color:var(--muted)}
.sort{width:auto;min-width:185px}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:13px;padding-bottom:20px}
.card{position:relative;display:flex;flex-direction:column;min-height:300px;background:
  linear-gradient(155deg,#13251f 0,#0c1714 78%);border:1px solid var(--line);
  border-radius:17px;padding:18px;transition:transform .18s,border-color .18s,box-shadow .18s}
.card:hover{transform:translateY(-3px);border-color:#41705c;box-shadow:0 18px 50px #0006}
.cardhead{display:flex;gap:12px;align-items:flex-start}
.logo{width:42px;height:42px;display:grid;place-items:center;flex:0 0 42px;border-radius:11px;
  background:#1a372c;border:1px solid #315a49;color:var(--green);font-weight:900;font-size:15px}
.company{color:var(--muted);font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.08em}
h2{font-size:17px;line-height:1.25;margin:3px 0 0;letter-spacing:-.018em}
.badges{display:flex;gap:6px;flex-wrap:wrap;margin:15px 0 10px}
.badge{border:1px solid var(--line);border-radius:999px;padding:4px 8px;color:var(--muted);font-size:11px}
.badge.research{border-color:#5a3e8a;color:var(--purple);background:#1a1028}
.badge.phd{border-color:#7a4a9a;color:var(--purple);background:#1a1028}
.badge.elite{border-color:#526d91;color:var(--blue)}.badge.new{border-color:#876f39;color:var(--amber)}
.badge.security{border-color:#6b3a3a;color:var(--red);background:#1a0f0f}
.badge.ai{border-color:#2b7b58;color:var(--green);background:#102b1e}
.meta{display:grid;gap:7px;color:var(--muted);font-size:12px;margin-top:3px}
.meta div{display:flex;gap:8px}.meta b{color:#cfddd8;font-weight:700;min-width:58px}
.focus{margin:13px 0;color:#b9cbc4;font-size:12px}
.health{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:12px 15px;
  margin:0 0 12px;border:1px solid var(--line);border-radius:14px;background:#0d1a17;font-size:12.5px}
.health .dot{width:9px;height:9px;border-radius:50%;flex:0 0 9px}
.health .dot.ok{background:var(--green);box-shadow:0 0 12px var(--green)}
.health .dot.bad{background:var(--red);box-shadow:0 0 12px var(--red)}
.health b{font-size:13px}
.health .muted{color:var(--muted)}
.health details{color:var(--muted)}
.health summary{cursor:pointer;color:var(--blue)}
.health ul{margin:8px 0 0;padding-left:18px}
.health li{margin:3px 0}
.fitbar{display:none;align-items:center;gap:10px;flex-wrap:wrap;padding:11px 14px;margin:0 0 12px;
  border:1px solid #396b55;border-radius:14px;background:#102b20;font-size:13px}
.fitbar.show{display:flex}
.fitbar b{color:var(--green)}
.fitchip{border:1px solid var(--line);border-radius:999px;background:transparent;color:var(--muted);
  padding:6px 11px;cursor:pointer;font-size:12px;font-weight:700}
.fitchip.active{border-color:var(--green2);color:var(--green);background:#173327}
.badge.fit-apply{border-color:#2b7b58;color:var(--green);background:#102b1e}
.badge.fit-sponsor{border-color:#876f39;color:var(--amber);background:#241d10}
.badge.fit-mismatch{border-color:#6b3a3a;color:var(--red);background:#1a0f0f}
.whyfit{margin:10px 0 0;font-size:11.5px;color:var(--muted);line-height:1.45}
.whyfit b{color:#cfddd8;font-weight:700}
.card.dim{opacity:.55}
.supervisors{margin:12px 0 2px;padding:11px 12px;border:1px solid #5a3e8a;border-radius:12px;
  background:#170f24}
.supervisors b{display:block;color:var(--purple);font-size:11px;letter-spacing:.05em;
  text-transform:uppercase}
.supervisors span{display:block;color:var(--muted);font-size:11.5px;margin:4px 0 7px}
.suplinks{display:flex;flex-wrap:wrap;gap:6px}
.suplinks a{border:1px solid #4a356f;border-radius:999px;padding:4px 9px;font-size:11px;
  color:#d9c8ff;text-decoration:none;font-weight:700}
.suplinks a:hover{border-color:var(--purple);background:#20143a}
.scfacts{display:block;color:#cbb8f5;font-size:11px;margin:4px 0 0}
.funding{margin:26px 0 8px;border:1px solid var(--line);border-radius:18px;
  background:linear-gradient(155deg,#141f2e 0,#0c1418 78%);padding:20px 22px}
.funding h3{margin:0;font-size:19px;letter-spacing:-.02em}
.funding>p{color:var(--muted);font-size:13px;margin:6px 0 14px;max-width:70ch}
.fundgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}
.fund{border:1px solid var(--line);border-radius:13px;padding:12px 13px;background:#0d1620}
.fund b{display:block;font-size:13.5px;margin-bottom:2px}
.fund .who{color:var(--muted);font-size:11.5px}
.fund .cyc{color:var(--amber);font-size:11.5px;margin-top:6px}
.fund .lv{display:flex;gap:4px;flex-wrap:wrap;margin-top:7px}
.fund .lv i{font-style:normal;border:1px solid #3a5a7a;border-radius:99px;padding:2px 7px;
  font-size:10px;color:var(--blue)}
.fund a{display:inline-block;margin-top:8px;color:var(--blue);font-size:11.5px;font-weight:700}
.actions{display:flex;gap:8px;margin-top:auto;padding-top:16px}
.btn{display:inline-flex;justify-content:center;align-items:center;min-height:40px;border-radius:10px;
  padding:0 12px;text-decoration:none;border:1px solid var(--line);font-weight:800;font-size:12px;cursor:pointer}
.btn.primary{background:var(--green2);border-color:var(--green2);color:#03130c;flex:1}
.btn.secondary{color:var(--text);background:#13241f}
.autoapply-cv-apply{flex:1!important;margin:0!important;padding:0 12px!important;font-size:12px!important}
.empty{grid-column:1/-1;text-align:center;border:1px dashed var(--line);border-radius:18px;
  color:var(--muted);padding:70px 20px}
.load{display:block;margin:10px auto 45px;background:transparent;color:var(--green);
  border:1px solid #3b6b56;border-radius:11px;padding:11px 20px;font-weight:800;cursor:pointer}
footer{border-top:1px solid var(--line);color:var(--muted);padding:25px 0 45px;font-size:12px}
footer a{color:var(--green)}
@media(max-width:1050px){.searchrow{grid-template-columns:repeat(3,1fr)}.searchrow .search{grid-column:1/-1}.cards{grid-template-columns:repeat(2,1fr)}}
@media(max-width:720px){.shell{width:min(100% - 22px,1420px)}header{padding-top:24px}.hero{display:block}.intro{margin-top:16px}
  .statusbar{grid-template-columns:repeat(2,1fr)}.filters{position:relative}.searchrow{grid-template-columns:1fr 1fr}
  .searchrow .search{grid-column:1/-1}.cards{grid-template-columns:1fr}.helper{align-items:flex-start;flex-direction:column}
  .resultbar{align-items:flex-end}.sort{min-width:150px}.card{min-height:280px}}
</style>
</head>
<body>
<div class="shell" data-autoapply-dashboard>
<header>
  <div class="eyebrow"><i class="pulse"></i>verified role intelligence · updated __GENERATED__</div>
  <div class="hero">
    <h1>Find the role.<br><span>Tailor. Apply.</span></h1>
    <p class="intro">Internships, research assistantships, PhD fellowships, postdocs, and new-grad roles — worldwide, across every CS and STEM domain. AI-tailored CV editing built in.</p>
  </div>
</header>
<section class="statusbar" aria-label="Tracker totals">
  <div class="stat"><strong id="totalStat">0</strong><span>verified-open roles</span></div>
  <div class="stat"><strong id="researchStat">0</strong><span>research / PhD / postdoc</span></div>
  <div class="stat"><strong id="newStat">0</strong><span>new since last run</span></div>
  <div class="stat"><strong id="tailorStat">0</strong><span>AI CV editor ready</span></div>
</section>
<section class="helper">
  <div><strong>⚡ Local AI CV Studio</strong><p>Every role opens your complete CV with reviewable AI suggestions. Accept, reject, directly edit, then export — nothing is silently removed.</p></div>
  <a class="btn primary" href="http://127.0.0.1:8765/connect" target="_blank">Check local connection</a>
</section>
<section class="filters" aria-label="Job filters">
  <div class="searchrow">
    <input id="search" class="control search" type="search" placeholder="Search role, company, location or focus…" autocomplete="off">
    <select id="region" class="control"><option value="">All regions</option></select>
    <select id="term" class="control"><option value="">All terms</option></select>
    <select id="level" class="control"><option value="">All degree levels</option></select>
    <select id="tier" class="control"><option value="">All tiers</option><option value="elite">Elite</option><option value="high">High</option><option value="standard">Standard</option></select>
    <select id="companyType" class="control" title="Company stage, from the tracker's curated watchlist"><option value="">All company stages</option></select>
  </div>
  <div class="quick" style="margin-top:11px">
    <span class="quick-label">Category</span>
    <div id="categoryChips" style="display:contents"></div>
    <span class="quick-divider"></span>
    <span class="quick-label">Type</span>
    <div id="typeChips" style="display:contents"></div>
  </div>
  <div class="quick">
    <label class="toggle"><input id="newOnly" type="checkbox"> New roles</label>
    <label class="toggle"><input id="officialOnly" type="checkbox"> Official ATS feed</label>
    <label class="toggle"><input id="remoteOnly" type="checkbox"> Remote</label>
    <label class="toggle"><input id="startupOnly" type="checkbox"> Startups</label>
    <label class="toggle"><input id="academicOnly" type="checkbox"> Top-100 universities</label>
    <span class="spacer"></span>
    <button class="chip" id="clear">Clear filters</button>
  </div>
</section>
<div class="health" id="health"></div>
<div class="fitbar" id="fitOffer">
  <b>Check these against your own profile</b>
  <span class="muted" style="font-size:12px">Your local helper can mark which of these
  you can actually apply to, by work authorisation and graduation date. It stays on your machine.</span>
  <span class="spacer"></span>
  <a class="btn primary" href="http://127.0.0.1:8765/dashboard">Open my local tracker</a>
</div>
<div class="fitbar" id="fitbar">
  <b id="fitSummary"></b>
  <span class="muted" style="font-size:12px">Checked on your machine against your profile — never published.</span>
  <span class="spacer"></span>
  <button class="fitchip" data-fit="apply">Can apply now</button>
  <button class="fitchip" data-fit="sponsor">Needs sponsorship</button>
  <button class="fitchip" data-fit="hide-mismatch">Hide date mismatches</button>
</div>
<div class="resultbar">
  <div><strong id="resultCount">0 roles</strong> <span id="context"></span></div>
  <select id="sort" class="control sort">
    <option value="recommended">Recommended</option>
    <option value="newest">Newest first</option>
    <option value="company">Company A–Z</option>
    <option value="elite">Elite tier first</option>
  </select>
</div>
<main class="cards" id="cards"></main>
<section class="funding" id="funding" hidden>
  <h3>Funding for study and research</h3>
  <p>Scholarships, studentships and fellowships that fund a degree or a research post,
  with who may apply and when the cycle usually opens. Deadlines move every year, so each
  one links to the page that actually governs it. Your local helper can mark which are open
  to you now.</p>
  <div class="fundgrid" id="fundgrid"></div>
</section>
<button class="load" id="loadMore" hidden>Show more roles</button>
<footer>Public job metadata only. Eligibility remains review-required unless personally verified. CV editing happens through the private localhost helper and never submits an application. <a href="https://github.com/abyyworld/internship-tracker">View source on GitHub</a>.</footer>
</div>
<script>
const JOBS=__JOBS__;
const HEALTH=__HEALTH__;
const FUNDING=__FUNDING__;
const PAGE=48;
const CATEGORY_ORDER=["All","AI / ML","Software Engineering","Quant / Finance","Robotics & Embodied AI","Security","Data","Systems & Infra","Hardware / EE","HCI / XR","Computational Science"];
const TYPE_ORDER=["All types","intern","research-assistant","new-grad","phd-fellowship","postdoc","co-op","placement","fellowship","masters-research"];
const TYPE_LABELS={"intern":"Internship","research-assistant":"Research Assistant","new-grad":"New Grad","phd-fellowship":"PhD Fellowship","postdoc":"Postdoc","co-op":"Co-op","placement":"Placement","fellowship":"Fellowship","masters-research":"Masters Research"};
// Company stage comes from a curated watchlist. "Not classified" is honest: the
// employer is simply not on it, which is different from being a large company.
const COMPANY_TYPE_LABELS={"emerging-startup":"Early-stage startup","startup":"Startup",
  "private-scaleup":"Private scale-up","scaleup":"Scale-up","established":"Established company",
  "unknown":"Not classified"};
const COMPANY_TYPE_ORDER=["emerging-startup","startup","private-scaleup","scaleup","established","unknown"];
const prettyType=v=>COMPANY_TYPE_LABELS[v]||v;
// "Unknown" is stored when the posting never states the field. Say that.
const LEVEL_LABELS={"Unknown":"Degree not stated","Advanced/unknown":"Advanced or not stated"};
const TERM_LABELS={"Unknown":"Term not stated","Ambiguous":"Term ambiguous"};
const REGION_LABELS={"Unknown":"Region not stated"};
const prettyLevel=v=>LEVEL_LABELS[v]||v;
const prettyTerm=v=>TERM_LABELS[v]||v;
const prettyRegion=v=>REGION_LABELS[v]||v;
let category="All", posType="All types", visible=PAGE;
// Personal fit verdicts, fetched from the local helper when it is running.
// They are never baked into this page: it is public.
let FIT={}, fitFilter="";
const FIT_LABELS={apply:"you can apply",sponsor:"needs sponsorship",mismatch:"date mismatch"};
const $=id=>document.getElementById(id);
const esc=value=>{const d=document.createElement("div");d.textContent=value??"";return d.innerHTML};
const norm=value=>(value||"").toString().toLowerCase();
const unique=key=>[...new Set(JOBS.map(j=>j[key]).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
const isResearch=j=>["research-assistant","phd-fellowship","postdoc","masters-research","fellowship"].includes(j.position_type);
const isStartup=j=>["emerging-startup","startup","private-scaleup","scaleup"].includes(j.company_type);
const rank=j=>({elite:0,high:1}[j.tier]??2);
function optionize(id,key,label,pretty,order){
  let values=unique(key);
  if(order)values=order.filter(v=>values.includes(v));
  values.forEach(value=>$(id).insertAdjacentHTML("beforeend",
    `<option value="${esc(value)}">${esc((pretty?pretty(value):value)||label)}</option>`));
}
function initials(name){return (name||"?").split(/\s+/).slice(0,2).map(x=>x[0]).join("").toUpperCase()}
function posTypeBadge(pt){
  if(!pt||pt==="other")return "";
  const cls=["research-assistant","phd-fellowship","postdoc","masters-research","fellowship"].includes(pt)?"research phd"
    :pt==="new-grad"?"ai":pt==="intern"?"":"";
  const label=TYPE_LABELS[pt]||pt;
  return `<span class="badge ${cls}">${esc(label)}</span>`;
}
function categoryBadge(cat){
  const cls=cat==="Security"?"security":cat==="AI / ML"?"ai":"";
  return `<span class="badge ${cls}">${esc(cat)}</span>`;
}
// Academic postings are decided by a supervisor the advert never names. These
// links go to the institution's own current faculty, not to a stored list of
// people and addresses that would be out of date within a term.
function supervisors(j){
  const u=j.university;
  if(!u)return "";
  const topic=(u.terms||[]).join(", ");
  const sc=u.scorecard&&u.scorecard.summary
    ?`<span class="scfacts">${esc(u.scorecard.summary)}</span>`:"";
  return `<div class="supervisors">
    <b>Supervisors · ${esc(u.name)}${u.rank?` · THE #${esc(u.rank)}`:""}</b>${sc}
    <span>${topic?`Search its faculty for ${esc(topic)}:`:"Search its faculty:"}</span>
    <div class="suplinks">
      <a href="${esc(u.scholar)}" target="_blank" rel="noopener">Academics &amp; contacts ↗</a>
      <a href="${esc(u.openalex)}" target="_blank" rel="noopener">Recent papers ↗</a>
      <a href="${esc(u.directory)}" target="_blank" rel="noopener">Department directory ↗</a>
    </div>
  </div>`;
}
const fitOf=j=>FIT[j.url]||null;
function whyFit(j){
  const f=fitOf(j);
  if(!f||!f.reasons||!f.reasons.length)return "";
  return `<p class="whyfit"><b>${esc(FIT_LABELS[f.status]||f.status)}:</b> ${esc(f.reasons[0])}</p>`;
}
function card(j){
  const badges=[
    categoryBadge(j.category),
    posTypeBadge(j.position_type),
    j.tier?`<span class="badge ${esc(j.tier)}">${esc(j.tier)}</span>`:"",
    j.new?`<span class="badge new">new</span>`:"",
    j.tailor?`<span class="badge ai">AI CV editor</span>`:"",
    j.university?`<span class="badge phd">supervisors listed</span>`:"",
    fitOf(j)&&FIT_LABELS[fitOf(j).status]
      ?`<span class="badge fit-${esc(fitOf(j).status)}">${esc(FIT_LABELS[fitOf(j).status])}</span>`:""
  ].filter(Boolean).join("");
  const focus=j.focus?`<p class="focus">${esc(j.focus.replaceAll(",",", "))}</p>`:"";
  const localUrl=`http://127.0.0.1:8765/editor?url=${encodeURIComponent(j.url)}`;
  const f=fitOf(j);
  return `<article class="card${f&&f.status==="mismatch"?" dim":""}">
    <div class="cardhead"><div class="logo">${esc(initials(j.company))}</div><div>
      <div class="company">${esc(j.company)}</div><h2>${esc(j.role)}</h2></div></div>
    <div class="badges">${badges}</div>
    <div class="meta">
      <div><b>Location</b><span>${esc(j.location||prettyRegion(j.region)||"Not stated")}</span></div>
      <div><b>Term</b><span>${esc(prettyTerm(j.term)||"Not stated")} · ${esc(j.work_mode||"unspecified")}</span></div>
      <div><b>Degree</b><span>${esc(prettyLevel(j.level)||"Not stated")}</span></div>
      ${j.company_type&&j.company_type!=="unknown"?`<div><b>Company</b><span>${esc(prettyType(j.company_type))}</span></div>`:""}
    </div>${whyFit(j)}${focus}${supervisors(j)}
    <div class="actions">
      <a class="btn primary" href="${esc(localUrl)}" target="_blank" rel="noopener">✦ Edit CV for this job</a>
      <a class="btn secondary job-link" data-no-autoapply="1" href="${esc(j.url)}" target="_blank" rel="noopener">Open only</a>
    </div>
  </article>`;
}
function state(){
  return {q:$("search").value.trim(),region:$("region").value,term:$("term").value,
    level:$("level").value,tier:$("tier").value,companyType:$("companyType").value,
    newOnly:$("newOnly").checked,officialOnly:$("officialOnly").checked,
    remoteOnly:$("remoteOnly").checked,startupOnly:$("startupOnly").checked,
    academicOnly:$("academicOnly").checked,
    sort:$("sort").value,category,posType,fit:fitFilter};
}
function matches(j,s){
  const hay=norm([j.company,j.role,j.location,j.region,j.focus,j.category,j.position_type].join(" "));
  const typeMatch=s.posType==="All types"||j.position_type===s.posType;
  return (!s.q||hay.includes(norm(s.q)))&&(!s.region||j.region===s.region)&&
    (!s.term||j.term===s.term)&&(!s.level||j.level===s.level)&&
    (!s.companyType||j.company_type===s.companyType)&&
    (!s.tier||(s.tier==="standard"?!j.tier:j.tier===s.tier))&&
    (s.category==="All"||j.category===s.category)&&typeMatch&&(!s.newOnly||j.new)&&
    (!s.officialOnly||j.official_ats)&&(!s.remoteOnly||j.work_mode==="remote")&&
    (!s.startupOnly||isStartup(j))&&(!s.academicOnly||!!j.university)&&matchesFit(j,s.fit);
}
function matchesFit(j,mode){
  if(!mode)return true;
  const f=fitOf(j);
  if(mode==="hide-mismatch")return !f||f.status!=="mismatch";
  return !!f&&f.status===mode;
}
const LOCAL=location.port==="8765";
async function loadFit(){
  const token=localStorage.getItem("autoapply_bridge_token_v1")||"";
  // Verdicts need the local helper. Served from it, this is a same-origin
  // request; on the public page it is not, and browsers now gate loopback
  // requests from public sites behind a permission prompt, so the page offers
  // a link to the local copy instead of failing quietly.
  if(token.length<32)return;
  if(!LOCAL){$("fitOffer").classList.add("show");return}
  try{
    const r=await fetch("/api/fit",{headers:{"X-Autoapply-Token":token}});
    if(!r.ok)return;
    const result=await r.json();
    FIT=result.fit||{};
    const c=result.counts||{};
    $("fitSummary").textContent=
      `${c.apply||0} you can apply to · ${c.sponsor||0} need sponsorship · ${c.mismatch||0} ruled out by date`;
    $("fitbar").classList.add("show");
    render();
  }catch(e){/* the helper is not running; the page stays as it is */}
}
function sorted(list,mode){
  return [...list].sort((a,b)=>{
    if(mode==="company")return a.company.localeCompare(b.company)||a.role.localeCompare(b.role);
    if(mode==="newest")return norm(b.first_seen).localeCompare(norm(a.first_seen))||rank(a)-rank(b);
    if(mode==="elite")return rank(a)-rank(b)||Number(b.new)-Number(a.new)||a.company.localeCompare(b.company);
    return Number(b.new)-Number(a.new)||rank(a)-rank(b)||Number(isStartup(b))-Number(isStartup(a))||a.company.localeCompare(b.company);
  });
}
function syncUrl(s){
  const p=new URLSearchParams();
  Object.entries(s).forEach(([k,v])=>{if(v&&v!=="All"&&v!=="All types"&&v!=="recommended")p.set(k,String(v))});
  history.replaceState(null,"",`${location.pathname}${p.size?`?${p}`:""}`);
}
function render(){
  const s=state(), filtered=sorted(JOBS.filter(j=>matches(j,s)),s.sort);
  $("resultCount").textContent=`${filtered.length} role${filtered.length===1?"":"s"}`;
  $("context").textContent=filtered.length===JOBS.length?"across the live tracker":"matching your filters";
  $("cards").innerHTML=filtered.length?filtered.slice(0,visible).map(card).join(""):`<div class="empty"><strong>No matching roles.</strong><br>Try clearing one or two filters.</div>`;
  $("loadMore").hidden=visible>=filtered.length;
  document.querySelectorAll("#categoryChips .chip").forEach(x=>x.classList.toggle("active",x.dataset.category===category));
  document.querySelectorAll("#typeChips .chip").forEach(x=>x.classList.toggle("active",x.dataset.postype===posType));
  syncUrl(s);
}
function restore(){
  const p=new URLSearchParams(location.search);
  ["search","region","term","level","tier","companyType","sort"].forEach(id=>{const v=p.get(id==="search"?"q":id);if(v)$(id).value=v});
  ["newOnly","officialOnly","remoteOnly","startupOnly","academicOnly"].forEach(id=>$(id).checked=p.get(id)==="true");
  if(CATEGORY_ORDER.includes(p.get("category")))category=p.get("category");
  if(TYPE_ORDER.includes(p.get("posType")))posType=p.get("posType");
}
function renderHealth(){
  const s=HEALTH.summary||{}, a=HEALTH.alerts||[];
  if(!s.sources)return;
  const clean=!a.some(x=>x.severity==="broken");
  const rate=s.description_rate==null?"":
    ` · ${Math.round(s.description_rate*100)}% of sampled adverts still readable`;
  let html=`<span class="dot ${clean?"ok":"bad"}"></span>`+
    `<b>${s.healthy}/${s.sources} sources healthy</b>`+
    `<span class="muted">${s.rows} rows on ${esc(s.date||"the last run")}${rate}</span>`;
  if(a.length){
    html+=`<details><summary>${a.length} issue${a.length===1?"":"s"} being tracked</summary><ul>`+
      a.map(x=>`<li><b>${esc(x.source)}</b> — ${esc(x.detail)}</li>`).join("")+`</ul></details>`;
  }
  $("health").innerHTML=html;
}
const LEVEL_NAMES={undergraduate:"Undergrad",masters:"Masters",phd:"PhD",
  postdoc:"Postdoc",research:"Research"};
function renderFunding(){
  if(!FUNDING.length)return;
  $("funding").hidden=false;
  $("fundgrid").innerHTML=FUNDING.map(f=>`<article class="fund">
    <b>${esc(f.name)}</b>
    <span class="who">${esc(f.funder)}</span>
    <div class="lv">${(f.levels||[]).map(l=>`<i>${esc(LEVEL_NAMES[l]||l)}</i>`).join("")}</div>
    <div class="cyc">${esc(f.cycle||"")}</div>
    <a href="${esc(f.url)}" target="_blank" rel="noopener">Eligibility &amp; deadline ↗</a>
  </article>`).join("");
}
renderFunding();
renderHealth();
$("totalStat").textContent=JOBS.length;
$("researchStat").textContent=JOBS.filter(isResearch).length;
$("newStat").textContent=JOBS.filter(j=>j.new).length;
$("tailorStat").textContent=JOBS.filter(j=>j.tailor).length;
optionize("region","region","Not stated",prettyRegion);
optionize("term","term","Not stated",prettyTerm);
optionize("level","level","Not stated",prettyLevel);
optionize("companyType","company_type","Not classified",prettyType,COMPANY_TYPE_ORDER);
$("categoryChips").innerHTML=CATEGORY_ORDER.map(x=>`<button class="chip" data-category="${esc(x)}">${esc(x)}</button>`).join("");
$("typeChips").innerHTML=TYPE_ORDER.map(x=>`<button class="chip type-chip" data-postype="${esc(x)}">${esc(TYPE_LABELS[x]||x)}</button>`).join("");
$("categoryChips").onclick=e=>{if(e.target.dataset.category){category=e.target.dataset.category;visible=PAGE;render()}};
$("typeChips").onclick=e=>{if(e.target.dataset.postype){posType=e.target.dataset.postype;visible=PAGE;render()}};
document.querySelector(".filters").addEventListener("input",()=>{visible=PAGE;render()});
$("sort").addEventListener("change",()=>{visible=PAGE;render()});
$("loadMore").onclick=()=>{visible+=PAGE;render()};
$("clear").onclick=()=>{document.querySelectorAll(".filters input").forEach(x=>{x.type==="checkbox"?x.checked=false:x.value=""});
  document.querySelectorAll(".filters select").forEach(x=>x.value="");$("sort").value="recommended";category="All";posType="All types";visible=PAGE;render()};
$("fitbar").onclick=e=>{
  const want=e.target.dataset.fit;
  if(!want)return;
  fitFilter=fitFilter===want?"":want;
  document.querySelectorAll(".fitchip").forEach(x=>
    x.classList.toggle("active",x.dataset.fit===fitFilter));
  visible=PAGE;render();
};
restore();render();loadFit();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    count = build()
    print(f"dashboard built: {OUTPUT} ({count} jobs)")
