#!/usr/bin/env python3
"""
internship_watcher.py v2 — elite global edition
=================================================
Profile: Akbar Juraev | AI/CS Year 2, University of Birmingham
         HCI researcher · ML/CV · SWE · quant-adjacent
Target:  Elite summer internships (Summer 2027) + UK spring weeks / term-time

SOURCES AUTO-SCRAPED EVERY RUN:
  GitHub community repos  — SimplifyJobs, vanshb03, sndsh404
  Greenhouse JSON API     — Jump Trading, IMC, Virtu, Akuna, Anthropic,
                            Waymo, Cloudflare, Stripe, Databricks, Figma,
                            Scale AI, Brex, Together AI, xAI, Jane Street +12 more
  (Lever API tested — all timed out; skipped.)

CURATED ELITE WATCHLIST (manual-check, always in tracker):
  Jane Street, DE Shaw, Two Sigma, Citadel, Optiver, HRT, Five Rings, SIG,
  Google/DeepMind, Meta, Apple, Amazon, Microsoft Research, OpenAI, ARM,
  Netflix, Palantir

UK SPRING WEEKS (hardcoded, always in tracker):
  Jane Street FOCUS, Citadel Discover, Goldman Sachs, Morgan Stanley,
  JP Morgan, Two Sigma Discovery, Optiver/IMC insight days, Barclays

Run:   python3 internship_watcher.py
Needs: Python 3.8+ stdlib only.
"""

import csv, html, json, os, re, ssl, sys, urllib.request
from datetime import date
from urllib.error import HTTPError, URLError

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
TRACKER_FILE   = "tracker.csv"
MANUAL_FILE    = "manual_checks.md"
TODAY          = date.today().isoformat()
DROP_CLOSED    = True
USER_COLS      = ["my_status", "priority", "applied_date", "notes"]

# Role title keyword filter — broad. Elite filter done via tier scoring.
KEYWORDS = [
    "software", "engineer", "developer", "swe", "backend", "frontend",
    "full stack", "full-stack", "systems", "platform", "infrastructure",
    "machine learning", " ml", "ml ", " ai", "ai ", "artificial intelligence",
    "data", "quant", "research", "scientist", "applied", "hci", "human",
    "computer vision", "nlp", "intern", "residency", "campus", "co-op", "coop",
    "fpga", "algorithmic", "trading", "quantitative",
]

# Elite tier — used to auto-set priority column (user can override)
TIER_1 = {
    "jane street", "de shaw", "two sigma", "hudson river trading", "hrt",
    "citadel", "citadel securities", "optiver", "imc trading", "imc",
    "five rings", "susquehanna", "sig", "akuna capital", "akuna",
    "openai", "anthropic", "google deepmind", "deepmind", "xai", "x.ai",
    "microsoft research", "meta ai", "fair", "jump trading", "jump",
    "virtu", "virtu financial",
}
TIER_2 = {
    "palantir", "google", "alphabet", "meta", "facebook", "apple",
    "amazon", "microsoft", "netflix", "stripe", "waymo", "databricks",
    "scale ai", "figma", "hugging face", "cohere", "mistral", "together ai",
    "drw", "arm", "graphcore", "wayve", "isomorphic labs",
    "cloudflare", "brex", "verkada", "nuro",
}

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# ─────────────────────────────────────────────────────────────────────────────
# SOURCE DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

GITHUB_SOURCES = [
    {
        "name": "Simplify2027",
        "url":  "https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships/dev/README.md",
        "fmt":  "html",
        "term": "Summer 2027",
    },
    {
        "name": "Simplify2026",
        "url":  "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md",
        "fmt":  "html",
        "term": "Summer 2026",
    },
    {
        "name": "vanshb03_2027",
        "url":  "https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/dev/README.md",
        "fmt":  "md_href",
        "term": "Summer 2027",
    },
    {
        "name": "sndsh404_2027",
        "url":  "https://raw.githubusercontent.com/sndsh404/summer-2027-internships/main/README.md",
        "fmt":  "md_link",
        "term": "Summer 2027",
    },
]

# Verified via API test — these slugs return real data.
# Slugs that returned 404/timeout are NOT listed here (they'd just fail every run).
GREENHOUSE_BOARDS = [
    # slug              display name          preferred term
    ("jumptrading",     "Jump Trading",       "Summer 2027"),   # AI/research intern roles LIVE
    ("imc",             "IMC Trading",        "Summer 2027"),   # quant intern roles LIVE
    ("akunacapital",    "Akuna Capital",      "Summer 2027"),   # SWE+quant intern LIVE
    ("virtu",           "Virtu Financial",    "Summer 2027"),   # quant intern Dublin LIVE
    ("anthropic",       "Anthropic",          "Summer 2027"),   # watching (no current intern)
    ("janestreet",      "Jane Street",        "Summer 2027"),   # watching (roles post Aug-Oct)
    ("xai",             "xAI",               "Summer 2027"),   # Musk's AI lab
    ("waymo",           "Waymo",             "Summer 2027"),
    ("cloudflare",      "Cloudflare",         "Summer 2027"),
    ("stripe",          "Stripe",             "Summer 2027"),
    ("databricks",      "Databricks",         "Summer 2027"),
    ("scaleai",         "Scale AI",           "Summer 2027"),
    ("brex",            "Brex",              "Summer 2027"),
    ("figma",           "Figma",             "Summer 2027"),
    ("togetherai",      "Together AI",        "Summer 2027"),   # research intern roles LIVE
    ("verkada",         "Verkada",            "Summer 2027"),
    ("coreweave",       "CoreWeave",          "Summer 2027"),   # GPU cloud, ML infra
    ("nuro",            "Nuro",              "Summer 2027"),
    ("mercury",         "Mercury",            "Summer 2027"),
    ("wayve",           "Wayve",             "Summer 2027"),   # UK autonomous driving
    ("deepmind",        "DeepMind",           "Summer 2027"),   # watching
]

# ─────────────────────────────────────────────────────────────────────────────
# CURATED ELITE WATCHLIST  (JS-heavy or own ATS — cannot auto-scrape)
# These rows are always present in the tracker. Check the URL manually.
# ─────────────────────────────────────────────────────────────────────────────
ELITE_WATCHLIST = [
    # company                role                              location                url                                                          term           tier
    ("Jane Street",          "Software Engineer Intern",       "New York / London",    "https://www.janestreet.com/join-jane-street/open-roles/",   "Summer 2027", "elite"),
    ("Jane Street",          "Quantitative Trading Intern",    "New York / London",    "https://www.janestreet.com/join-jane-street/open-roles/",   "Summer 2027", "elite"),
    ("DE Shaw",              "SWE / Quant Research Intern",    "New York / London",    "https://www.deshaw.com/careers/internships",                "Summer 2027", "elite"),
    ("Two Sigma",            "SWE / Quant Research Intern",   "New York",             "https://careers.twosigma.com/careers/jobListings",          "Summer 2027", "elite"),
    ("Citadel",              "SWE / Quant Research Intern",   "Chicago / London / NY","https://www.citadel.com/careers/",                          "Summer 2027", "elite"),
    ("Citadel Securities",   "SWE / Trading Intern",          "Chicago / London / NY","https://www.citadelsecurities.com/careers/",                "Summer 2027", "elite"),
    ("Optiver",              "Software Engineer Intern",       "Amsterdam/Chicago",    "https://optiver.com/working-at-optiver/career-opportunities/","Summer 2027","elite"),
    ("Optiver",              "Trader Intern",                  "Amsterdam/Chicago",    "https://optiver.com/working-at-optiver/career-opportunities/","Summer 2027","elite"),
    ("Hudson River Trading", "SWE / Algo Dev Intern",         "New York / London",    "https://www.hudsonrivertrading.com/careers/",               "Summer 2027", "elite"),
    ("Five Rings",           "Software / Quant Research Intern","New York",           "https://fiverings.com/careers/",                            "Summer 2027", "elite"),
    ("Susquehanna (SIG)",    "Technology / Quant Intern",     "Philadelphia / Dublin","https://careers.sig.com/",                                  "Summer 2027", "elite"),
    ("Google",               "Software Engineering Intern",   "Global (incl London)", "https://careers.google.com/",                               "Summer 2027", "elite"),
    ("Google DeepMind",      "Research Intern (AI/ML)",       "London / Mountain View","https://deepmind.google/careers/",                         "Summer 2027", "elite"),
    ("Meta",                 "SWE Intern / Research Intern",  "Global (incl London)", "https://www.metacareers.com/",                              "Summer 2027", "elite"),
    ("Meta AI (FAIR)",       "Research Intern",               "London / Menlo Park",  "https://ai.meta.com/join-us/",                              "Summer 2027", "elite"),
    ("Apple",                "SWE / ML Research Intern",      "Cupertino / Cambridge","https://jobs.apple.com/",                                   "Summer 2027", "elite"),
    ("Microsoft Research",   "Research Intern",               "Cambridge UK / Redmond","https://www.microsoft.com/en-us/research/careers/",        "Summer 2027", "elite"),
    ("Amazon",               "SDE Intern / Applied Sci Intern","Global (incl London)","https://www.amazon.jobs/",                                 "Summer 2027", "elite"),
    ("Netflix",              "SWE Intern",                    "Los Gatos / Remote",   "https://jobs.netflix.com/",                                 "Summer 2027", "high"),
    ("OpenAI",               "SWE / Research Intern",        "San Francisco",        "https://openai.com/careers/",                               "Summer 2027", "elite"),
    ("Palantir",             "Forward Deployed SWE Intern",   "London / New York",    "https://www.palantir.com/careers/",                         "Summer 2027", "high"),
    ("ARM",                  "SWE / ML Intern",               "Cambridge, UK",        "https://careers.arm.com/",                                  "Summer 2027", "high"),
    ("DRW",                  "SWE / Quant Research Intern",   "Chicago / London",     "https://drw.com/work-at-drw/",                              "Summer 2027", "elite"),
    ("Graphcore",            "ML / SWE Intern",               "Bristol, UK",          "https://www.graphcore.ai/careers",                          "Summer 2027", "high"),
    ("Isomorphic Labs",      "Research Intern",               "London, UK",           "https://www.isomorphiclabs.com/join",                       "Summer 2027", "high"),
]

# ─────────────────────────────────────────────────────────────────────────────
# UK SPRING WEEKS & TERM-TIME PROGRAMS
# Applications open ~Sept–Nov 2026; programs run Spring/Easter 2027
# ─────────────────────────────────────────────────────────────────────────────
SPRING_WEEKS = [
    # company            role/program                       location      url                                                               deadline           tier
    ("Jane Street",      "FOCUS (First-Year Insight)",      "London/NY",  "https://www.janestreet.com/join-jane-street/open-roles/",        "Oct–Nov 2026",    "elite"),
    ("Two Sigma",        "Discovery Program",               "London/NY",  "https://careers.twosigma.com/careers/jobListings",               "Oct–Jan 2027",    "elite"),
    ("Citadel",          "Discover Citadel (Spring Week)",  "London",     "https://www.citadel.com/careers/",                               "Oct–Nov 2026",    "elite"),
    ("Optiver",          "Insight Day / Spring Program",    "Amsterdam",  "https://optiver.com/working-at-optiver/career-opportunities/",   "Rolling Oct–Feb", "elite"),
    ("IMC Trading",      "Insight Day",                     "Amsterdam",  "https://www.imc.com/eu/careers/",                                "Rolling Oct–Feb", "elite"),
    ("Goldman Sachs",    "Engineering Spring Insight (UK)", "London",     "https://www.goldmansachs.com/careers/",                          "Oct–Dec 2026",    "high"),
    ("Morgan Stanley",   "Technology Spring Insight (UK)",  "London",     "https://www.morganstanley.com/people-opportunities/",            "Oct–Dec 2026",    "high"),
    ("JP Morgan",        "Technology Spring Week (UK)",     "London",     "https://careers.jpmorgan.com/",                                  "Oct–Nov 2026",    "high"),
    ("Barclays",         "Technology Spring Intern (UK)",   "London",     "https://home.barclays/careers/",                                 "Nov–Jan 2027",    "medium"),
    ("Hudson River Trading","Insight Day / Campus Event",   "London/NY",  "https://www.hudsonrivertrading.com/careers/",                    "Rolling",         "elite"),
    ("Susquehanna (SIG)","Quant Finance Insight Days",      "Dublin",     "https://careers.sig.com/",                                       "Rolling",         "elite"),
    ("Five Rings",       "Summer Smash / Insight Event",    "New York",   "https://fiverings.com/careers/",                                 "Rolling",         "elite"),
]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "internship-watcher/2"})
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as r:
        return r.read().decode("utf-8", "replace")


def first_url(cell):
    for m in re.finditer(r'href="([^"]+)"', cell):
        u = m.group(1)
        if "i.imgur.com" in u:
            continue
        if "simplify.jobs" not in u:
            return html.unescape(u)
    m = re.search(r"\]\((https?://[^)]+)\)", cell)
    if m:
        return html.unescape(m.group(1))
    m = re.search(r'href="([^"]+)"', cell)
    return html.unescape(m.group(1)) if m else ""


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def clean_loc(s):
    s = s.replace("</br>", " / ").replace("<br>", " / ").replace("<br/>", " / ")
    return strip_html(s).strip(" /")


US_ST = set(("al ak az ar ca co ct de fl ga hi id il in ia ks ky la me md ma mi "
             "mn ms mo mt ne nv nh nj nm ny nc nd oh ok or pa ri sc sd tn tx ut "
             "vt va wa wv wi wy dc").split())

def region_of(loc):
    l = loc.lower()
    if re.search(r"\buk\b|\bu\.k\.|united kingdom|england|scotland|wales|\blondon\b|"
                 r"\bedinburgh\b|\bcardiff\b|\bcambridge\b|\bbristol\b|\bbirmingham\b|"
                 r"\bmanchester\b|\bsouthampton\b", l):
        return "UK"
    if "ireland" in l or "dublin" in l:
        return "Ireland"
    if "amsterdam" in l or "netherlands" in l:
        return "Netherlands"
    if "canada" in l or re.search(r",\s*(on|bc|qc|ab)\b", l):
        return "Canada"
    if "remote" in l:
        return "Remote"
    if re.search(r",\s*(" + "|".join(US_ST) + r")\b", l):
        return "US"
    if re.search(r"\b(nyc|sf|la\b|san francisco|new york|seattle|boston|austin|"
                 r"chicago|palo alto|menlo park|redmond|sunnyvale|santa clara|"
                 r"bay area|silicon valley|united states|usa|mountain view)\b", l):
        return "US"
    if any(c in l for c in ("global", "worldwide")):
        return "Global"
    return "Other"


def norm_role(role):
    r = role.lower()
    r = re.sub(r"\(.*?\)|\[.*?\]", "", r)
    r = re.sub(r"summer\s*20\d\d|co-?op|intern(ship)?|campus|20\d\d", "", r)
    r = re.sub(r"[^a-z ]", " ", r)
    r = re.sub(r"\s+", " ", r).strip()
    r = r.replace("engineering", "engineer").replace("developer", "engineer")
    return r


def make_id(company, role, loc):
    city = loc.split("/")[0].split(",")[0].strip().lower()
    key = f"{company.lower().strip()}|{norm_role(role)}|{city}"
    return re.sub(r"[^a-z0-9]", "", key)[:64]


def tier_of(company):
    c = company.lower()
    # Use word-boundary matching to avoid "sig" matching "design", etc.
    def wbmatch(pattern, text):
        return bool(re.search(r"(?<![a-z])" + re.escape(pattern) + r"(?![a-z])", text))
    for t1 in TIER_1:
        if wbmatch(t1, c):
            return "elite"
    for t2 in TIER_2:
        if wbmatch(t2, c):
            return "high"
    return ""


def emoji_flags(text):
    f = []
    if "🛂" in text: f.append("NO-SPONSORSHIP")
    if "🇺🇸" in text: f.append("US-CITIZEN-ONLY")
    if "🎓" in text: f.append("ADV-DEGREE")
    if "🔥" in text: f.append("HOT")
    return f


INTERN_SIGNALS = [
    "intern", "co-op", "coop", "campus", "residency",
    "sneak peek", "challenge", "insight", "discovery",
]

def keep(company, role, closed, require_intern_signal=False):
    if not company or not role:
        return False
    if DROP_CLOSED and closed:
        return False
    t = role.lower()
    if require_intern_signal and not any(k in t for k in INTERN_SIGNALS):
        return False
    return any(k in t for k in KEYWORDS)


# ─────────────────────────────────────────────────────────────────────────────
# PARSERS
# ─────────────────────────────────────────────────────────────────────────────
def parse_html_table(text, term):
    rows, last = [], ""
    for tr in re.findall(r"<tr>(.*?)</tr>", text, re.S):
        tds = re.findall(r"<td.*?>(.*?)</td>", tr, re.S)
        if len(tds) < 4:
            continue
        raw_co = tds[0]
        company = strip_html(raw_co)
        if company in ("↳", ""):
            company = last
        else:
            last = company
        role = strip_html(tds[1])
        loc  = clean_loc(tds[2])
        url  = first_url(tds[3])
        closed = "🔒" in tr
        if not keep(company, role, closed):
            continue
        rows.append(dict(company=company, role=role, location=loc, url=url,
                         term=term, flags=emoji_flags(raw_co + role + tr)))
    return rows


def parse_md_pipe(text, term):
    rows, last = [], ""
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        if cells[0].lower() in ("company", "") or set(cells[0]) <= set("- :"):
            continue
        raw_co = cells[0]
        company = strip_html(raw_co)
        if company in ("↳", ""):
            company = last
        else:
            last = company
        role   = strip_html(cells[1])
        loc    = clean_loc(cells[2])
        apply  = cells[3] if len(cells) > 3 else ""
        closed = "🔒" in apply or "🔒" in line
        url    = "" if closed else first_url(apply)
        if not keep(company, role, closed):
            continue
        rows.append(dict(company=company, role=role, location=loc, url=url,
                         term=term, flags=emoji_flags(line)))
    return rows


def parse_greenhouse(slug, display_name, term):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        data = json.loads(fetch(url, timeout=15))
    except Exception as e:
        return None, str(e)
    rows = []
    for j in data.get("jobs", []):
        role = j.get("title", "")
        if not keep(display_name, role, False, require_intern_signal=True):
            continue
        loc_raw = j.get("location", {})
        loc = loc_raw.get("name", "") if isinstance(loc_raw, dict) else str(loc_raw)
        apply_url = j.get("absolute_url", "")
        rows.append(dict(company=display_name, role=role, location=loc,
                         url=apply_url, term=term, flags=[]))
    return rows, None


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
def gather():
    merged = {}    # id -> record
    failed = []

    def add(r, source):
        rid = make_id(r["company"], r["role"], r["location"])
        if rid in merged:
            if source not in merged[rid]["sources"]:
                merged[rid]["sources"].append(source)
            if not merged[rid]["url"] and r.get("url"):
                merged[rid]["url"] = r["url"]
        else:
            merged[rid] = dict(
                id=rid,
                company=r["company"],
                role=r["role"],
                location=r["location"],
                region=region_of(r["location"]),
                url=r.get("url", ""),
                term=r.get("term", "Summer 2027"),
                sources=[source],
                flags=r.get("flags", []),
                elite_tier=tier_of(r["company"]),
            )

    # — GitHub repos —
    for src in GITHUB_SOURCES:
        try:
            text = fetch(src["url"])
        except Exception as e:
            failed.append((src["name"], str(e)))
            print(f"  {src['name']:<20} SKIP  {str(e)[:55]}", file=sys.stderr)
            continue
        if src["fmt"] == "html":
            rows = parse_html_table(text, src["term"])
        else:
            rows = parse_md_pipe(text, src["term"])
        for r in rows:
            add(r, src["name"])
        print(f"  {src['name']:<20} {len(rows):>4} roles")

    # — Greenhouse boards —
    gh_ok = gh_fail = 0
    for slug, name, term in GREENHOUSE_BOARDS:
        rows, err = parse_greenhouse(slug, name, term)
        if rows is None:
            gh_fail += 1
            failed.append((name, err))
        else:
            gh_ok += 1
            for r in rows:
                add(r, f"Greenhouse/{slug}")
    print(f"  Greenhouse          {gh_ok}/{gh_ok+gh_fail} boards OK, "
          f"{sum(1 for r in merged.values() if 'Greenhouse' in ','.join(r['sources']))} roles")

    # — Curated elite watchlist (always present) —
    for (company, role, loc, url, term, tier) in ELITE_WATCHLIST:
        rid = make_id(company, role, loc)
        if rid not in merged:
            merged[rid] = dict(
                id=rid, company=company, role=role, location=loc,
                region=region_of(loc), url=url, term=term,
                sources=["elite_watchlist"], flags=[], elite_tier=tier,
            )
        else:
            if "elite_watchlist" not in merged[rid]["sources"]:
                merged[rid]["sources"].append("elite_watchlist")

    # — Spring weeks —
    for (company, role, loc, url, deadline, tier) in SPRING_WEEKS:
        role_full = f"{role} [deadline: {deadline}]"
        rid = make_id(company, role_full, loc)
        if rid not in merged:
            merged[rid] = dict(
                id=rid, company=company, role=role_full, location=loc,
                region=region_of(loc), url=url, term="Spring Week 2027",
                sources=["spring_weeks"], flags=[], elite_tier=tier,
            )

    return merged, failed


def load_existing(path):
    if not os.path.exists(path):
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {row["id"]: row for row in csv.DictReader(f) if row.get("id")}


def write_manual_checks(failed):
    lines = [f"# Manual Check List — {TODAY}\n",
             "These companies use JS-heavy or private ATS — check their career pages directly.\n",
             "Set `my_status` in tracker.csv once you've applied or decided to skip.\n\n"]

    lines.append("## Elite Manual Checks\n")
    lines.append("| Company | Role | Location | Term | Link |\n")
    lines.append("|---------|------|----------|------|------|\n")
    for (company, role, loc, url, term, _tier) in ELITE_WATCHLIST:
        lines.append(f"| {company} | {role} | {loc} | {term} | [Apply]({url}) |\n")

    lines.append("\n## UK Spring Weeks (apply NOW — deadlines Oct–Jan)\n")
    lines.append("| Company | Program | Location | Deadline | Link |\n")
    lines.append("|---------|---------|----------|----------|------|\n")
    for (company, role, loc, url, deadline, _tier) in SPRING_WEEKS:
        lines.append(f"| {company} | {role} | {loc} | {deadline} | [Apply]({url}) |\n")

    if failed:
        lines.append("\n## Sources that failed this run\n")
        for name, err in failed:
            lines.append(f"- **{name}**: {err}\n")

    with open(MANUAL_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD  — the shareable README.md front page (regenerated every run)
# ─────────────────────────────────────────────────────────────────────────────
def _cell(s):
    """Make a string safe for a markdown table cell."""
    return str(s).replace("|", "/").replace("\n", " ").strip()


def _role_row(r, cols=("company", "role", "region", "term")):
    url = r.get("url", "")
    company = _cell(r.get("company", ""))
    role = _cell(r.get("role", ""))
    if url:
        role = f"[{role}]({url})"
    flag = ""
    if r.get("block") == "BLOCKED":
        flag = " 🚫"
    elif "NO-SPONSORSHIP" in r.get("flags", ""):
        flag = " 🛂"
    cells = {
        "company": f"**{company}**",
        "role": role + flag,
        "region": _cell(r.get("region", "")),
        "term": _cell(r.get("term", "")),
        "location": _cell(r.get("location", "")),
    }
    return "| " + " | ".join(cells[c] for c in cols) + " |"


def build_dashboard(rows_out, new_ids, current):
    live = [r for r in rows_out if r.get("source_status") == "open"]
    elite = [r for r in live if r.get("elite_tier") == "elite"]
    high  = [r for r in live if r.get("elite_tier") == "high"]
    new_rows = [r for r in rows_out if r.get("NEW") == "YES"]
    spring = [r for r in live if r.get("term") == "Spring Week 2027"]

    from collections import Counter
    region_counts = Counter(r.get("region", "?") for r in live)

    L = []
    L.append("# 🎯 Elite Internship Tracker — Summer 2027 + UK Spring Weeks\n")
    L.append(f"> **Auto-updated daily** by GitHub Actions · Last run: **{TODAY}** · "
             f"**{len(live)} live roles** tracked\n")
    L.append("\nCurated for **AI/ML · SWE · Quant/HFT · HCI research**. "
             "Scrapes 3 community boards + 21 company Greenhouse APIs every day, "
             "merges + de-dupes, and flags what newly opened.\n")
    L.append("\n🚫 = US-citizen-only (blocked)   🛂 = no visa sponsorship\n")

    # At a glance
    L.append("\n## 📊 At a glance\n")
    L.append("| Metric | Count |\n|--------|------:|\n")
    L.append(f"| Total live roles | {len(live)} |\n")
    L.append(f"| 🏆 Elite tier | {len(elite)} |\n")
    L.append(f"| ⭐ High tier | {len(high)} |\n")
    L.append(f"| 🆕 New this run | {len(new_ids)} |\n")
    reg_str = " · ".join(f"{k} {v}" for k, v in region_counts.most_common())
    L.append(f"\n**By region:** {reg_str}\n")

    # NEW roles
    if new_rows:
        elite_new = [r for r in new_rows if r.get("elite_tier") in ("elite", "high")]
        L.append(f"\n## 🆕 Newly opened ({len(new_rows)})\n")
        shown = elite_new if elite_new else new_rows
        L.append("| Company | Role | Region | Term |\n|--|--|--|--|\n")
        for r in shown[:40]:
            L.append(_role_row(r) + "\n")
        if len(shown) > 40:
            L.append(f"\n_…and {len(shown)-40} more — see [tracker.csv](tracker.csv)_\n")

    # Elite roles by region (collapsible)
    L.append(f"\n## 🏆 Elite roles — live & auto-scraped ({len(elite)})\n")
    by_region = {}
    for r in elite:
        by_region.setdefault(r.get("region", "Other"), []).append(r)
    order = ["UK", "US", "Netherlands", "Ireland", "Canada", "Remote", "Global", "Other"]
    for reg in sorted(by_region, key=lambda x: order.index(x) if x in order else 99):
        rs = sorted(by_region[reg], key=lambda r: r.get("company", ""))
        L.append(f"\n<details><summary><b>{reg}</b> — {len(rs)} roles</summary>\n\n")
        L.append("| Company | Role | Term |\n|--|--|--|\n")
        for r in rs:
            L.append(_role_row(r, cols=("company", "role", "term")) + "\n")
        L.append("\n</details>\n")

    # Spring weeks — urgent
    if spring:
        L.append("\n## 🇬🇧 UK Spring Weeks & Insight Days — APPLY OCT–NOV 2026\n")
        L.append("First-year/early insight programs that feed directly into summer offers. "
                 "**These deadlines come first — don't miss them.**\n\n")
        L.append("| Company | Program | Location | Link |\n|--|--|--|--|\n")
        for r in sorted(spring, key=lambda r: r.get("company", "")):
            url = r.get("url", "")
            link = f"[Apply]({url})" if url else ""
            L.append(f"| **{_cell(r['company'])}** | {_cell(r['role'])} | "
                     f"{_cell(r.get('location',''))} | {link} |\n")

    # High tier (collapsible, compact)
    if high:
        L.append(f"\n## ⭐ High-tier roles ({len(high)})\n")
        L.append("<details><summary>Show all</summary>\n\n")
        L.append("| Company | Role | Region | Term |\n|--|--|--|--|\n")
        for r in sorted(high, key=lambda r: (r.get("region",""), r.get("company",""))):
            L.append(_role_row(r) + "\n")
        L.append("\n</details>\n")

    # Manual-check elites
    L.append("\n## 📋 Elite companies — check these career pages directly\n")
    L.append("_These firms use private application systems that can't be auto-scraped. "
             "They're your highest-priority targets — check weekly._\n\n")
    L.append("| Company | Role | Location | Link |\n|--|--|--|--|\n")
    for (company, role, loc, url, term, _t) in ELITE_WATCHLIST:
        L.append(f"| **{_cell(company)}** | {_cell(role)} | {_cell(loc)} | [Open]({url}) |\n")

    # Footer
    L.append("\n---\n")
    L.append("\n## ⚙️ How this works\n")
    L.append("- A Python scraper (`internship_watcher.py`) runs **every morning via "
             "GitHub Actions** — no server, no computer needed.\n")
    L.append("- It pulls [SimplifyJobs](https://github.com/SimplifyJobs), "
             "[vanshb03](https://github.com/vanshb03/Summer2027-Internships), "
             "sndsh404, and 21 companies' Greenhouse job APIs.\n")
    L.append("- Full data (with your own status/notes columns) lives in "
             "[tracker.csv](tracker.csv). Manual-check links in "
             "[manual_checks.md](manual_checks.md).\n")
    L.append("- Want your own copy? Fork this repo and enable Actions. "
             "Zero dependencies — Python stdlib only.\n")
    L.append(f"\n_Built for and by [@abyyworld](https://github.com/abyyworld). "
             f"Data is community-sourced; verify before applying._\n")

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(L)


def run():
    print(f"\ninternship watcher v2 — {TODAY}")
    print("=" * 56)

    current, failed = gather()
    existing = load_existing(TRACKER_FILE)

    new_ids, rows_out = [], []

    for rid, rec in current.items():
        blocked = "BLOCKED" if "US-CITIZEN-ONLY" in rec["flags"] else ""
        prev = existing.get(rid)
        if prev:
            first_seen = prev.get("first_seen", TODAY)
            user = {c: prev.get(c, "") for c in USER_COLS}
            is_new = False
        else:
            first_seen = TODAY
            user = {c: "" for c in USER_COLS}
            new_ids.append(rid)
            is_new = True

        row = dict(
            id=rid,
            NEW="YES" if is_new else "",
            company=rec["company"],
            role=rec["role"],
            region=rec["region"],
            location=rec["location"],
            term=rec.get("term", ""),
            elite_tier=rec.get("elite_tier", ""),
            source_status="open",
            block=blocked,
            flags=",".join(rec["flags"]),
            sources=",".join(rec["sources"]),
            url=rec["url"],
            first_seen=first_seen,
            last_seen=TODAY,
            **user,
        )
        rows_out.append(row)

    # Preserve roles you've applied to even if they vanished from sources
    for rid, prev in existing.items():
        if rid in current:
            continue
        prev["source_status"] = "gone/closed?"
        prev["NEW"] = ""
        rows_out.append(prev)

    # Sort: NEW first, then elite_tier, then company
    tier_rank = {"elite": 0, "high": 1, "": 2}
    rows_out.sort(key=lambda r: (
        r.get("NEW") != "YES",
        tier_rank.get(r.get("elite_tier", ""), 2),
        r.get("company", ""),
    ))

    FIELDS = ["NEW", "company", "role", "region", "location", "term",
              "elite_tier", "source_status", "block", "flags", "sources",
              "url", "first_seen", "last_seen", *USER_COLS, "id"]

    with open(TRACKER_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows_out:
            w.writerow(r)

    # New-roles digest
    if new_ids:
        fn = f"new_roles_{TODAY}.md"
        with open(fn, "w", encoding="utf-8") as f:
            f.write(f"# {len(new_ids)} new roles — {TODAY}\n\n")
            for rid in new_ids:
                rec = current[rid]
                tier = f" **[{rec['elite_tier'].upper()}]**" if rec.get("elite_tier") else ""
                blk  = " _(US citizen only — blocked)_" if "US-CITIZEN-ONLY" in rec["flags"] else ""
                f.write(f"- **{rec['company']}**{tier} — {rec['role']} "
                        f"[{rec['region']}, {rec.get('term','')}]{blk}\n"
                        f"  {rec['url']}\n")

    write_manual_checks(failed)
    build_dashboard(rows_out, new_ids, current)

    # Summary
    total_elite = sum(1 for r in rows_out if r.get("elite_tier") == "elite")
    total_high  = sum(1 for r in rows_out if r.get("elite_tier") == "high")
    print(f"\n  tracked roles       : {len(rows_out)}")
    print(f"  elite tier          : {total_elite}")
    print(f"  high tier           : {total_high}")
    print(f"  NEW this run        : {len(new_ids)}")

    elite_new = [rid for rid in new_ids if current[rid].get("elite_tier")]
    if elite_new:
        print(f"\n  NEW elite/high roles ({len(elite_new)}):")
        for rid in elite_new[:15]:
            rec = current[rid]
            print(f"    [{rec['elite_tier'].upper():5}] {rec['company']} — {rec['role'][:55]} [{rec['region']}]")
    elif new_ids:
        print(f"\n  sample new roles:")
        for rid in new_ids[:8]:
            rec = current[rid]
            print(f"    {rec['company']} — {rec['role'][:60]} [{rec['region']}]")

    print(f"\n  tracker  -> {TRACKER_FILE}")
    print(f"  manual   -> {MANUAL_FILE}")
    if new_ids:
        print(f"  new digest -> new_roles_{TODAY}.md")
    print()


if __name__ == "__main__":
    run()
