#!/usr/bin/env python3
"""Build the public, filterable GitHub Pages job dashboard."""

from __future__ import annotations

import csv
from datetime import date
import json
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
TRACKER = ROOT / "tracker.csv"
OUTPUT = ROOT / "docs" / "index.html"
ATS_SUFFIXES = ("greenhouse.io", "lever.co", "ashbyhq.com")


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
    jobs: list[dict[str, object]] = []
    for row in rows:
        url = safe_url(row.get("url", ""))
        jobs.append(
            {
                "id": row.get("id", ""),
                "company": row.get("company", ""),
                "role": row.get("role", ""),
                "category": row.get("category", "Unknown"),
                "region": row.get("region", "Unknown"),
                "location": row.get("location", ""),
                "term": row.get("term", "Unknown"),
                "level": row.get("level", "Unknown"),
                "work_mode": row.get("work_mode", "unspecified"),
                "tier": row.get("elite_tier", ""),
                "focus": row.get("robotics_focus", "")
                or row.get("focus_tags", ""),
                "company_type": row.get("company_type", "unknown"),
                "company_signal": row.get("company_signal", ""),
                "equity_signal": row.get("equity_signal", "unknown"),
                "eligibility": row.get("eligibility", "review required"),
                "deadline": row.get("deadline", ""),
                "first_seen": row.get("first_seen", ""),
                "last_seen": row.get("last_seen", ""),
                "new": row.get("discovered_new", "").upper() == "YES",
                "url": url,
                "tailor": bool(url),
                "official_ats": bool(url and ats_supported(url)),
            }
        )
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
    page = TEMPLATE.replace("__JOBS__", json_for_script(jobs)).replace(
        "__GENERATED__", date.today().isoformat()
    )
    OUTPUT.write_text(page, encoding="utf-8")
    return len(jobs)


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Filter verified internships and robotics roles, generate a tailored CV locally, then apply.">
<title>Role Radar · Internship & Robotics Jobs</title>
<style>
:root{
  color-scheme:dark;
  --bg:#07110f;--panel:#0e1b18;--panel2:#13231f;--line:#284139;
  --text:#f1f8f5;--muted:#9bb1a9;--green:#70efad;--green2:#25b875;
  --amber:#f5c86b;--blue:#79b8ff;--red:#ff8b82;--shadow:0 18px 55px #0007;
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
.badge.robotics{border-color:#2b7b58;color:var(--green);background:#173126}
.badge.elite{border-color:#526d91;color:var(--blue)}.badge.new{border-color:#876f39;color:var(--amber)}
.meta{display:grid;gap:7px;color:var(--muted);font-size:12px;margin-top:3px}
.meta div{display:flex;gap:8px}.meta b{color:#cfddd8;font-weight:700;min-width:58px}
.focus{margin:13px 0;color:#b9cbc4;font-size:12px}
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
  <div class="eyebrow"><i class="pulse"></i>verified job intelligence · updated __GENERATED__</div>
  <div class="hero">
    <h1>Find the role.<br><span>Tailor. Apply.</span></h1>
    <p class="intro">Search live internships worldwide, isolate robotics startups and top technical roles, then generate an evidence-checked CV on your Mac before Simplify fills the application.</p>
  </div>
</header>
<section class="statusbar" aria-label="Tracker totals">
  <div class="stat"><strong id="totalStat">0</strong><span>verified-open roles</span></div>
  <div class="stat"><strong id="roboticsStat">0</strong><span>robotics / embodied AI</span></div>
  <div class="stat"><strong id="startupStat">0</strong><span>robotics startups / scaleups</span></div>
  <div class="stat"><strong id="tailorStat">0</strong><span>local CV generation</span></div>
</section>
<section class="helper">
  <div><strong>⚡ Local CV helper</strong><p>Every role can generate a private edited CV on your Mac. No CV facts are sent to this website.</p></div>
  <a class="btn primary" href="http://127.0.0.1:8765/connect" target="_blank">Check local connection</a>
</section>
<section class="filters" aria-label="Job filters">
  <div class="searchrow">
    <input id="search" class="control search" type="search" placeholder="Search role, company, location or focus…" autocomplete="off">
    <select id="region" class="control"><option value="">All regions</option></select>
    <select id="term" class="control"><option value="">All terms</option></select>
    <select id="level" class="control"><option value="">All degrees</option></select>
    <select id="tier" class="control"><option value="">All tiers</option><option value="elite">Elite</option><option value="high">High</option><option value="standard">Standard</option></select>
    <select id="companyType" class="control"><option value="">All company types</option></select>
  </div>
  <div class="quick" id="categoryChips"></div>
  <div class="quick">
    <label class="toggle"><input id="newOnly" type="checkbox"> New roles</label>
    <label class="toggle"><input id="officialOnly" type="checkbox"> Official ATS feed</label>
    <label class="toggle"><input id="remoteOnly" type="checkbox"> Remote</label>
    <label class="toggle"><input id="startupOnly" type="checkbox"> Robotics startups</label>
    <span class="spacer"></span>
    <button class="chip" id="clear">Clear filters</button>
  </div>
</section>
<div class="resultbar">
  <div><strong id="resultCount">0 roles</strong> <span id="context"></span></div>
  <select id="sort" class="control sort">
    <option value="recommended">Recommended</option>
    <option value="newest">Newest first</option>
    <option value="company">Company A–Z</option>
    <option value="robotics">Robotics first</option>
  </select>
</div>
<main class="cards" id="cards"></main>
<button class="load" id="loadMore" hidden>Show more roles</button>
<footer>Public job metadata only. Eligibility remains review-required unless personally verified. CV generation happens locally and never submits an application. <a href="https://github.com/abyyworld/internship-tracker">View source on GitHub</a>.</footer>
</div>
<script>
const JOBS=__JOBS__;
const PAGE=48;
const CATEGORY_ORDER=["All","Robotics & Embodied AI","AI / ML","Software Engineering","Quant","Data"];
let category="All", visible=PAGE;
const $=id=>document.getElementById(id);
const esc=value=>{const d=document.createElement("div");d.textContent=value??"";return d.innerHTML};
const norm=value=>(value||"").toString().toLowerCase();
const unique=key=>[...new Set(JOBS.map(j=>j[key]).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
const isRobotics=j=>j.category==="Robotics & Embodied AI";
const isStartup=j=>isRobotics(j)&&["emerging-startup","startup","private-scaleup","scaleup"].includes(j.company_type);
const rank=j=>({elite:0,high:1}[j.tier]??2);
function optionize(id,key,label){
  unique(key).forEach(value=>$(id).insertAdjacentHTML("beforeend",`<option value="${esc(value)}">${esc(value||label)}</option>`));
}
function initials(name){return (name||"?").split(/\s+/).slice(0,2).map(x=>x[0]).join("").toUpperCase()}
function card(j){
  const badges=[
    `<span class="badge ${isRobotics(j)?"robotics":""}">${esc(j.category)}</span>`,
    j.tier?`<span class="badge ${esc(j.tier)}">${esc(j.tier)}</span>`:"",
    j.new?`<span class="badge new">new</span>`:"",
    j.tailor?`<span class="badge robotics">local AI CV</span>`:""
  ].join("");
  const focus=j.focus?`<p class="focus">${esc(j.focus.replaceAll(",",", "))}</p>`:"";
  const localUrl=`http://127.0.0.1:8765/tailor?url=${encodeURIComponent(j.url)}`;
  return `<article class="card">
    <div class="cardhead"><div class="logo">${esc(initials(j.company))}</div><div>
      <div class="company">${esc(j.company)}</div><h2>${esc(j.role)}</h2></div></div>
    <div class="badges">${badges}</div>
    <div class="meta">
      <div><b>Location</b><span>${esc(j.location||j.region||"Unknown")}</span></div>
      <div><b>Term</b><span>${esc(j.term||"Unknown")} · ${esc(j.work_mode||"unspecified")}</span></div>
      <div><b>Degree</b><span>${esc(j.level||"Unknown")}</span></div>
      ${j.company_type&&j.company_type!=="unknown"?`<div><b>Company</b><span>${esc(j.company_type)}</span></div>`:""}
    </div>${focus}
    <div class="actions">
      <a class="btn primary" href="${esc(localUrl)}" target="_blank" rel="noopener">⚡ Tailor CV + Apply</a>
      <a class="btn secondary job-link" data-no-autoapply="1" href="${esc(j.url)}" target="_blank" rel="noopener">Open only</a>
    </div>
  </article>`;
}
function state(){
  return {q:$("search").value.trim(),region:$("region").value,term:$("term").value,
    level:$("level").value,tier:$("tier").value,companyType:$("companyType").value,
    newOnly:$("newOnly").checked,officialOnly:$("officialOnly").checked,
    remoteOnly:$("remoteOnly").checked,startupOnly:$("startupOnly").checked,
    sort:$("sort").value,category};
}
function matches(j,s){
  const hay=norm([j.company,j.role,j.location,j.region,j.focus,j.category].join(" "));
  return (!s.q||hay.includes(norm(s.q)))&&(!s.region||j.region===s.region)&&
    (!s.term||j.term===s.term)&&(!s.level||j.level===s.level)&&
    (!s.companyType||j.company_type===s.companyType)&&
    (!s.tier||(s.tier==="standard"?!j.tier:j.tier===s.tier))&&
    (s.category==="All"||j.category===s.category)&&(!s.newOnly||j.new)&&
    (!s.officialOnly||j.official_ats)&&(!s.remoteOnly||j.work_mode==="remote")&&
    (!s.startupOnly||isStartup(j));
}
function sorted(list,mode){
  return [...list].sort((a,b)=>{
    if(mode==="company")return a.company.localeCompare(b.company)||a.role.localeCompare(b.role);
    if(mode==="newest")return norm(b.first_seen).localeCompare(norm(a.first_seen))||rank(a)-rank(b);
    if(mode==="robotics")return Number(isRobotics(b))-Number(isRobotics(a))||Number(isStartup(b))-Number(isStartup(a))||rank(a)-rank(b);
    return Number(b.new)-Number(a.new)||rank(a)-rank(b)||Number(isStartup(b))-Number(isStartup(a))||a.company.localeCompare(b.company);
  });
}
function syncUrl(s){
  const p=new URLSearchParams();
  Object.entries(s).forEach(([k,v])=>{if(v&&v!=="All"&&v!=="recommended")p.set(k,String(v))});
  history.replaceState(null,"",`${location.pathname}${p.size?`?${p}`:""}`);
}
function render(){
  const s=state(), filtered=sorted(JOBS.filter(j=>matches(j,s)),s.sort);
  $("resultCount").textContent=`${filtered.length} role${filtered.length===1?"":"s"}`;
  $("context").textContent=filtered.length===JOBS.length?"across the live tracker":"matching your filters";
  $("cards").innerHTML=filtered.length?filtered.slice(0,visible).map(card).join(""):`<div class="empty"><strong>No matching roles.</strong><br>Try clearing one or two filters.</div>`;
  $("loadMore").hidden=visible>=filtered.length;
  document.querySelectorAll("#categoryChips .chip").forEach(x=>x.classList.toggle("active",x.dataset.category===category));
  syncUrl(s);
}
function restore(){
  const p=new URLSearchParams(location.search);
  ["search","region","term","level","tier","companyType","sort"].forEach(id=>{const v=p.get(id==="search"?"q":id);if(v)$(id).value=v});
  ["newOnly","officialOnly","remoteOnly","startupOnly"].forEach(id=>$(id).checked=p.get(id)==="true");
  if(CATEGORY_ORDER.includes(p.get("category")))category=p.get("category");
}
$("totalStat").textContent=JOBS.length;
$("roboticsStat").textContent=JOBS.filter(isRobotics).length;
$("startupStat").textContent=JOBS.filter(isStartup).length;
$("tailorStat").textContent=JOBS.filter(j=>j.tailor).length;
optionize("region","region","Unknown");optionize("term","term","Unknown");
optionize("level","level","Unknown");optionize("companyType","company_type","Unknown");
$("categoryChips").innerHTML=CATEGORY_ORDER.map(x=>`<button class="chip" data-category="${esc(x)}">${esc(x)}</button>`).join("");
$("categoryChips").onclick=e=>{if(e.target.dataset.category){category=e.target.dataset.category;visible=PAGE;render()}};
document.querySelector(".filters").addEventListener("input",()=>{visible=PAGE;render()});
$("sort").addEventListener("change",()=>{visible=PAGE;render()});
$("loadMore").onclick=()=>{visible+=PAGE;render()};
$("clear").onclick=()=>{document.querySelectorAll(".filters input").forEach(x=>{x.type==="checkbox"?x.checked=false:x.value=""});
  document.querySelectorAll(".filters select").forEach(x=>x.value="");$("sort").value="recommended";category="All";visible=PAGE;render()};
restore();render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    count = build()
    print(f"dashboard built: {OUTPUT} ({count} jobs)")
