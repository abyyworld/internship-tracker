#!/usr/bin/env python3
"""
copilot.py  -  Application co-pilot cockpit
============================================
Reads tracker.csv (produced by internship_watcher.py), calculates title relevance,
and generates a self-contained 3-tab review cockpit:

  Tab 1  APPROVED QUEUE    - roles you explicitly reviewed or marked eligible.
  Tab 2  REVIEW NEEDED     - open postings whose application facts still need review.
  Tab 3  NOT ELIGIBLE      - unsafe links or known term, degree, or citizenship blocks.

The cockpit opens application pages but never fills or submits them.

No em-dashes are used in any generated application text.

Run:   python3 copilot.py
Then:  open apply_cockpit.html   (double-click it)

Requires: nothing but Python 3.8+ (standard library only).
"""

import csv, html, json, os, re
from datetime import date
from urllib.parse import urlsplit

TRACKER_FILE = "tracker.csv"
OUT_HTML     = "apply_cockpit.html"

# ─────────────────────────────────────────────────────────────────────────────
# Generic target-area signals. Personal evidence belongs only in the ignored
# private/resume_facts.yaml used by the local autoapply tailor.
# ─────────────────────────────────────────────────────────────────────────────
TARGET = {
    "primary": [
        "machine learning", "computer vision", "deep learning", "pytorch", "nlp",
        "ai", "artificial intelligence", "research", "hci", "vr", "xr", "unity",
        "c#", "full stack", "full-stack", "python", "model", "perception",
    ],
    "secondary": [
        "software", "engineer", "developer", "backend", "frontend", "systems",
        "platform", "infrastructure", "data", "java", "docker", "api", "applied",
        "robotics",
    ],
    "specialist": [
        "c++", "low latency", "low-latency", "fpga", "hardware", "kernel",
        "options", "derivatives", "market making", "market maker",
    ],
}

# Fit thresholds (0..100)
READY_MIN      = 52
NEEDSWORK_MIN  = 30


def load_rows():
    if not os.path.exists(TRACKER_FILE):
        raise SystemExit("tracker.csv not found. Run internship_watcher.py first.")
    with open(TRACKER_FILE, newline="", encoding="utf-8") as f:
        return [
            r for r in csv.DictReader(f)
            if r.get("source_status") == "open"
            and r.get("record_kind", "posting") == "posting"
        ]


def has(word, text):
    return re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", text) is not None


def score_role(r):
    """Return title relevance plus an independently gated readiness tab."""
    title = " ".join(
        r.get(key, "")
        for key in ("role", "company", "category", "focus_tags", "robotics_focus")
    ).lower()
    reasons = []
    fit = 45  # baseline for an in-lane early-career role

    if not safe_application_url(r.get("url", "")):
        return 0, ["Missing or unsafe application URL"], "not_ready"
    citizenship = r.get("citizenship", "").lower()
    if citizenship == "us only" or "required" in citizenship:
        return 0, [
            "A citizenship or US-person requirement is listed; confirm before applying"
        ], "not_ready"
    if r.get("level") in ("PhD", "MSc", "Masters", "Advanced/unknown"):
        return 15, [
            f"Degree gate is {r.get('level')}; verify before applying as an undergraduate"
        ], "not_ready"
    if r.get("role_type") in ("graduate", "new-grad", "campus", "other"):
        return 20, [
            f"Role type is {r.get('role_type')}; it is not a confirmed internship"
        ], "not_ready"
    if r.get("term") == "Summer 2026" and date.today() >= date(2026, 7, 1):
        return 20, ["Summer 2026 is already in progress; verify it still accepts applications"], "not_ready"

    # Strengths
    s_hits = [w for w in TARGET["primary"] if has(w, title)]
    e_hits = [w for w in TARGET["secondary"] if has(w, title)]
    g_hits = [w for w in TARGET["specialist"] if has(w, title)]
    fit += min(len(s_hits), 4) * 12
    fit += min(len(e_hits), 3) * 6
    if r.get("role_type") in ("intern", "new-grad", "graduate", "placement",
                              "campus", "summer-analyst"):
        fit += 3  # a clean in-lane early-career posting
    if s_hits:
        reasons.append("Target-area signals: " + ", ".join(sorted(set(s_hits))[:4]))
    if g_hits:
        reasons.append(
            "Specialist requirements to verify: "
            + ", ".join(sorted(set(g_hits))[:3])
        )

    # Elite quant/HFT are high bar and OA-heavy
    quant = any(has(w, title) for w in ["quant", "quantitative", "trading", "trader"])
    if quant and r.get("elite_tier") == "elite":
        fit -= 6
        reasons.append("Top quant firm: expect a demanding timed technical assessment")

    # Sponsorship information is a review note, never an inferred eligibility answer.
    if r.get("sponsorship") in ("no sponsorship", "unavailable"):
        reasons.append("No visa sponsorship is indicated; confirm local work authorisation")

    fit = max(0, min(100, fit))

    verified = r.get("eligibility") == "verified eligible"
    if fit < NEEDSWORK_MIN:
        tab = "not_ready"
    elif verified:
        tab = "ready"
    else:
        tab = "needs_work"
        reasons.append("Application facts and eligibility still need your review")
    if not reasons:
        reasons.append("General match to the configured software/AI target areas")
    return fit, reasons, tab


def suggestions_for(r):
    """Rule-based CV tailoring notes. No em-dashes."""
    title = (r.get("role", "") + " " + r.get("company", "")).lower()
    tips = []
    if any(has(w, title) for w in ["hci", "human-computer", "interaction", "ux"]):
        tips.append("Lead with your strongest verified HCI or user-research evidence.")
    if any(has(w, title) for w in ["quant", "quantitative", "trading", "trader"]):
        tips.append(
            "Lead with verified quantitative/programming evidence and prepare "
            "for timed problem-solving."
        )
    if any(has(w, title) for w in ["machine", "ml", "ai", "vision", "deep", "research", "scientist"]):
        tips.append(
            "Put the most relevant verified ML/research evidence first and "
            "quantify outcomes only when the fact bank supports them."
        )
    if has("c++", title):
        tips.append(
            "This role leans C++; include only evidence-backed systems, "
            "performance, or C++ experience."
        )
    if any(has(w, title) for w in ["backend", "systems", "platform", "infrastructure"]):
        tips.append(
            "Prioritise verified backend, systems, deployment, or infrastructure "
            "evidence from the private fact bank."
        )
    if r.get("region") == "UK":
        tips.append("For this UK-based role, state only your verified current location "
                    "and answer work-authorisation questions from your private profile.")
    if not tips:
        tips.append("Tailor the top third of your CV to the words in this job title, "
                    "and put your most relevant project first.")
    return tips


def esc(s):
    return html.escape(str(s), quote=True)


def safe_application_url(value):
    candidate = (value or "").strip()
    try:
        parsed = urlsplit(candidate)
    except ValueError:
        return ""
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return ""
    return candidate


def build(rows):
    cards = []
    for r in rows:
        fit, reasons, tab = score_role(r)
        cards.append({
            "id": r.get("id", ""),
            "company": r.get("company", ""),
            "role": r.get("role", ""),
            "category": r.get("category", ""),
            "focus": r.get("robotics_focus", "") or r.get("focus_tags", ""),
            "company_type": r.get("company_type", "unknown"),
            "equity_signal": r.get("equity_signal", "unknown"),
            "eligibility": r.get("eligibility", "review required"),
            "region": r.get("region", ""),
            "location": r.get("location", ""),
            "term": r.get("term", ""),
            "level": r.get("level", "Any"),
            "tier": r.get("elite_tier", "") if r.get("elite_tier") in ("elite", "high") else "",
            "deadline": r.get("deadline", ""),
            "url": safe_application_url(r.get("url", "")),
            "fit": fit,
            "reasons": reasons,
            "tips": suggestions_for(r),
            "tab": tab,
        })
    # sort each tab by tier then fit
    tier_rank = {"elite": 0, "high": 1, "": 2}
    cards.sort(key=lambda c: (tier_rank.get(c["tier"], 2), -c["fit"]))

    counts = {t: sum(1 for c in cards if c["tab"] == t)
              for t in ("ready", "needs_work", "not_ready")}
    data = json.dumps(cards, ensure_ascii=True)
    data = data.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")

    page = HTML_TEMPLATE.replace("__DATA__", data)\
                        .replace("__DATE__", date.today().isoformat())\
                        .replace("__READY__", str(counts["ready"]))\
                        .replace("__NEEDS__", str(counts["needs_work"]))\
                        .replace("__NOTREADY__", str(counts["not_ready"]))
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(page)
    return counts


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Application Cockpit</title>
<style>
  :root{
    --bg:#0f1115; --card:#1a1d24; --line:#2a2f3a; --tx:#e8eaed; --mut:#9aa3b2;
    --acc:#4f8cff; --ok:#33c27f; --warn:#f2b544; --bad:#f2685c;
  }
  @media (prefers-color-scheme: light){
    :root{--bg:#f5f6f8; --card:#fff; --line:#e3e6ea; --tx:#1a1d24; --mut:#5a6472;}
  }
  *{box-sizing:border-box}
  body{margin:0;font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
       background:var(--bg);color:var(--tx)}
  header{padding:20px 22px 8px}
  h1{margin:0 0 2px;font-size:20px}
  .sub{color:var(--mut);font-size:13px}
  .tabs{display:flex;gap:6px;padding:12px 22px 0;flex-wrap:wrap;position:sticky;top:0;
        background:var(--bg);z-index:5}
  .tab{padding:9px 14px;border:1px solid var(--line);border-bottom:none;border-radius:9px 9px 0 0;
       background:transparent;color:var(--mut);cursor:pointer;font-weight:600;font-size:14px}
  .tab.active{background:var(--card);color:var(--tx)}
  .tab .n{display:inline-block;min-width:20px;text-align:center;margin-left:6px;
          padding:1px 6px;border-radius:10px;background:var(--line);font-size:12px}
  .bar{display:flex;gap:10px;align-items:center;padding:12px 22px;flex-wrap:wrap;
       border-top:1px solid var(--line)}
  button.act{background:var(--acc);color:#fff;border:none;padding:9px 14px;border-radius:8px;
             font-weight:600;cursor:pointer;font-size:14px}
  button.ghost{background:transparent;color:var(--tx);border:1px solid var(--line);
               padding:8px 12px;border-radius:8px;cursor:pointer;font-size:13px}
  .wrap{padding:6px 22px 60px;max-width:1000px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:12px;
        padding:14px 16px;margin:12px 0}
  .top{display:flex;gap:12px;align-items:flex-start}
  .chk{width:18px;height:18px;margin-top:3px;flex:none}
  .co{font-weight:700}
  .role{color:var(--tx)}
  .meta{color:var(--mut);font-size:12.5px;margin-top:3px}
  .pill{display:inline-block;padding:1px 8px;border-radius:10px;font-size:11.5px;
        border:1px solid var(--line);margin-right:5px}
  .pill.elite{color:var(--acc);border-color:var(--acc)}
  .pill.high{color:var(--ok);border-color:var(--ok)}
  .fit{margin-left:auto;text-align:right;flex:none}
  .fit .num{font-size:20px;font-weight:800}
  .fit.ok .num{color:var(--ok)} .fit.warn .num{color:var(--warn)} .fit.bad .num{color:var(--bad)}
  .why{margin:10px 0 0;padding:0;list-style:none;font-size:13px;color:var(--mut)}
  .why li:before{content:"• ";color:var(--acc)}
  .tips{margin-top:10px;background:rgba(127,127,127,.08);border-radius:9px;padding:10px 12px}
  .tips h4{margin:0 0 6px;font-size:12px;text-transform:uppercase;letter-spacing:.4px;color:var(--mut)}
  .tips ul{margin:0;padding-left:18px;font-size:13.5px}
  .row{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
  a.apply{background:var(--acc);color:#fff;text-decoration:none;padding:8px 13px;border-radius:8px;
          font-weight:600;font-size:13px}
  .hide{display:none}
  .empty{color:var(--mut);padding:30px 0;text-align:center}
  .note{font-size:12px;color:var(--mut);padding:0 22px 10px}
</style>
</head>
<body>
<header>
  <h1>Application Cockpit</h1>
  <div class="sub">Generated __DATE__ from open posting rows in tracker.csv. The number is title relevance, not an eligibility decision or a tailored CV score.</div>
</header>

<div class="tabs">
  <button class="tab" data-tab="ready">Approved queue <span class="n">__READY__</span></button>
  <button class="tab active" data-tab="needs_work">Review needed <span class="n">__NEEDS__</span></button>
  <button class="tab" data-tab="not_ready">Not eligible / defer <span class="n">__NOTREADY__</span></button>
</div>

<div class="bar">
  <button class="act" id="openTicked">Open selected apply pages</button>
  <button class="ghost" id="tickAll">Tick all shown</button>
  <button class="ghost" id="untickAll">Untick all</button>
  <span class="sub" id="tickInfo"></span>
</div>
<div class="note">Selections and manual review marks persist in this browser. For local CV tailoring, uploads, guarded form filling, and one-time approved submission, use <code>python -m autoapply</code>. Unknown legal or work-authorisation answers remain blocked.</div>

<div class="wrap" id="wrap"></div>

<script>
const CARDS = __DATA__;
const STORE_KEY = "internship-cockpit-v2";
let memoryState = {selected:{}, overrides:{}, current:"needs_work"};
try {
  const saved = JSON.parse(localStorage.getItem(STORE_KEY) || "null");
  if(saved && typeof saved==="object") memoryState = {
    selected: saved.selected || {}, overrides: saved.overrides || {},
    current: ["ready","needs_work","not_ready"].includes(saved.current) ? saved.current : "needs_work"
  };
} catch(_e) {}
CARDS.forEach(c=>{ if(memoryState.overrides[c.id]) c.tab=memoryState.overrides[c.id]; });
let current = memoryState.current;

function fitClass(f){ return f>=58?"ok":(f>=32?"warn":"bad"); }
function esc(s){ const d=document.createElement("div"); d.textContent=s??""; return d.innerHTML; }
function persist(){ try{ localStorage.setItem(STORE_KEY, JSON.stringify(memoryState)); }catch(_e){} }
function selected(c){
  return Object.prototype.hasOwnProperty.call(memoryState.selected,c.id)
    ? !!memoryState.selected[c.id] : c.tab==="ready";
}

function cardHTML(c, i){
  const pills = [];
  if(c.tier) pills.push(`<span class="pill ${c.tier}">${c.tier}</span>`);
  if(c.category) pills.push(`<span class="pill">${esc(c.category)}</span>`);
  pills.push(`<span class="pill">${esc(c.region)}</span>`);
  pills.push(`<span class="pill">${esc(c.term)}</span>`);
  if(c.level) pills.push(`<span class="pill">${esc(c.level)}</span>`);
  if(c.company_type && c.company_type!=="unknown") pills.push(`<span class="pill">${esc(c.company_type)}</span>`);
  if(c.deadline) pills.push(`<span class="pill">due ${esc(c.deadline)}</span>`);
  const why = c.reasons.map(r=>`<li>${esc(r)}</li>`).join("");
  const tips = c.tips.map(t=>`<li>${esc(t)}</li>`).join("");
  const moveBtn = (c.tab==="needs_work")
    ? `<button class="ghost" onclick="moveToReady(${i})">Mark reviewed as approved</button>` : "";
  const applyBtn = c.url
    ? `<a class="apply" href="${esc(c.url)}" target="_blank" rel="noopener">Open apply page</a>` : "";
  return `<div class="card" data-i="${i}">
    <div class="top">
      <input class="chk" type="checkbox" data-i="${i}" ${selected(c)?"checked":""}>
      <div>
        <div><span class="co">${esc(c.company)}</span> &nbsp;<span class="role">${esc(c.role)}</span></div>
        <div class="meta">${esc(c.location)} · ${esc(c.eligibility)}</div>
        <div class="meta" style="margin-top:6px">${pills.join(" ")}</div>
      </div>
      <div class="fit ${fitClass(c.fit)}"><div class="num">${c.fit}</div><div class="meta">relevance</div></div>
    </div>
    <ul class="why">${why}</ul>
    <div class="tips"><h4>Suggested CV tweaks</h4><ul>${tips}</ul></div>
    <div class="row">${applyBtn}${moveBtn}</div>
  </div>`;
}

function render(){
  const wrap = document.getElementById("wrap");
  const shown = CARDS.map((c,i)=>[c,i]).filter(([c])=>c.tab===current);
  wrap.innerHTML = shown.length
    ? shown.map(([c,i])=>cardHTML(c,i)).join("")
    : `<div class="empty">Nothing in this tab right now.</div>`;
  updateTickInfo();
}
function updateTickInfo(){
  const n = CARDS.filter(selected).length;
  document.getElementById("tickInfo").textContent = n+" selected across all tabs";
}
function moveToReady(i){
  CARDS[i].tab="ready";
  memoryState.overrides[CARDS[i].id]="ready";
  if(!Object.prototype.hasOwnProperty.call(memoryState.selected,CARDS[i].id))
    memoryState.selected[CARDS[i].id]=true;
  persist(); recount(); render();
}
function recount(){
  const c={ready:0,needs_work:0,not_ready:0};
  CARDS.forEach(x=>c[x.tab]++);
  document.querySelectorAll(".tab").forEach(t=>{
    const k=t.dataset.tab; t.querySelector(".n").textContent=c[k];
  });
}
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
  t.classList.add("active"); current=t.dataset.tab; memoryState.current=current; persist(); render();
});
document.addEventListener("change", e=>{
  if(e.target.classList.contains("chk")){
    const card=CARDS[+e.target.dataset.i];
    memoryState.selected[card.id]=e.target.checked; persist(); updateTickInfo();
  }
});
document.getElementById("tickAll").onclick=()=>{
  CARDS.filter(c=>c.tab===current).forEach(c=>memoryState.selected[c.id]=true);
  persist(); render();
};
document.getElementById("untickAll").onclick=()=>{
  CARDS.forEach(c=>memoryState.selected[c.id]=false);
  persist(); render();
};
document.getElementById("openTicked").onclick=()=>{
  const urls=CARDS.filter(c=>selected(c)).map(c=>c.url).filter(Boolean);
  if(!urls.length){ alert("Nothing selected."); return; }
  if(urls.length>8 && !confirm(`Open ${urls.length} application pages in new tabs?`)) return;
  urls.forEach((u,k)=>setTimeout(()=>window.open(u,"_blank","noopener"), k*350));
};
document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("active",t.dataset.tab===current));
render();
</script>
</body>
</html>"""


if __name__ == "__main__":
    rows = load_rows()
    counts = build(rows)
    print(f"\napply cockpit built -> {OUT_HTML}")
    print(f"  Reviewed queue : {counts['ready']}")
    print(f"  Needs work     : {counts['needs_work']}")
    print(f"  Defer / gated  : {counts['not_ready']}")
    print(f"\n  open it:  open {OUT_HTML}\n")
