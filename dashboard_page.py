"""The public page: one box, every kind of opportunity, in either theme.

Kept apart from dashboard.py because it is a front end, not a data pipeline —
and because the two change for completely different reasons. dashboard.py
decides what is true; this decides what it looks like.
"""

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Radar — internships, PhD positions, funding and the people behind them</title>
<meta name="description" content="Every opportunity worth applying for — internships, new-grad roles, PhD and research positions, accelerators and scholarships — matched to what you say you want.">
<link rel="icon" href="./favicon.svg" type="image/svg+xml">
<style>
/* ── Palette ───────────────────────────────────────────────────────────────
   Light is the default because most people read this in daylight on a phone.
   Every colour is a token so the dark set is a swap, not a second stylesheet,
   and the reader's own choice always beats the system's. */
:root{
  --bg:#f7f8fa; --raise:#ffffff; --sunk:#eef1f5;
  --ink:#0f1419; --ink-2:#39434e; --muted:#6b7684; --faint:#95a0ad;
  --line:#e2e6ec; --line-2:#cfd6df;
  --accent:#1a56db; --accent-ink:#ffffff; --accent-soft:#e8eefc;
  --good:#0f7b4f; --good-soft:#e3f6ec;
  --warn:#8a5300; --warn-soft:#fdf1de;
  --bad:#b42318; --bad-soft:#fdece9;
  --shadow:0 1px 2px rgba(15,20,25,.05), 0 2px 8px rgba(15,20,25,.06);
  --shadow-lift:0 4px 12px rgba(15,20,25,.10), 0 12px 28px rgba(15,20,25,.10);
  --radius:14px; --radius-s:10px;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#0d1117; --raise:#151b23; --sunk:#1c232c;
    --ink:#e9eef5; --ink-2:#c2ccd8; --muted:#8b98a8; --faint:#6b7889;
    --line:#242c37; --line-2:#333d4b;
    --accent:#5b8cff; --accent-ink:#08101f; --accent-soft:#182742;
    --good:#4ed49a; --good-soft:#12291f;
    --warn:#e3b341; --warn-soft:#2a2113;
    --bad:#ff8b82; --bad-soft:#2c1715;
    --shadow:0 1px 2px rgba(0,0,0,.4); --shadow-lift:0 8px 26px rgba(0,0,0,.55);
  }
}
:root[data-theme="dark"]{
  --bg:#0d1117; --raise:#151b23; --sunk:#1c232c;
  --ink:#e9eef5; --ink-2:#c2ccd8; --muted:#8b98a8; --faint:#6b7889;
  --line:#242c37; --line-2:#333d4b;
  --accent:#5b8cff; --accent-ink:#08101f; --accent-soft:#182742;
  --good:#4ed49a; --good-soft:#12291f;
  --warn:#e3b341; --warn-soft:#2a2113;
  --bad:#ff8b82; --bad-soft:#2c1715;
  --shadow:0 1px 2px rgba(0,0,0,.4); --shadow-lift:0 8px 26px rgba(0,0,0,.55);
}

*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto,
       "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing:antialiased;
}
a{color:var(--accent); text-decoration:none}
a:hover{text-decoration:underline}
button,input,select,textarea{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--accent); outline-offset:2px; border-radius:6px}
.wrap{max-width:1180px;margin:0 auto;padding:0 18px}
h1,h2,h3{margin:0;line-height:1.25;letter-spacing:-.01em}

/* ── Top bar ─────────────────────────────────────────────────────────────── */
header.top{
  position:sticky; top:0; z-index:40; background:var(--raise);
  border-bottom:1px solid var(--line);
}
.topin{display:flex;align-items:center;gap:14px;padding:11px 0}
.brand{display:flex;align-items:center;gap:9px;font-weight:800;letter-spacing:-.02em;
  font-size:17px;color:var(--ink);white-space:nowrap}
.brand:hover{text-decoration:none}
.dot{width:22px;height:22px;border-radius:7px;background:var(--accent);
  display:grid;place-items:center;color:var(--accent-ink);font-size:12px;font-weight:900}
.ask{flex:1;position:relative;min-width:0}
.ask input{
  width:100%;padding:11px 42px 11px 38px;border-radius:999px;
  border:1px solid var(--line-2);background:var(--sunk);color:var(--ink);
}
.ask input::placeholder{color:var(--faint)}
.ask input:focus{background:var(--raise);border-color:var(--accent);outline:none;
  box-shadow:0 0 0 3px var(--accent-soft)}
.ask .mag{position:absolute;left:13px;top:50%;transform:translateY(-50%);color:var(--faint);
  font-size:14px;pointer-events:none}
.ask .go{position:absolute;right:5px;top:50%;transform:translateY(-50%);
  border:0;background:var(--accent);color:var(--accent-ink);border-radius:999px;
  padding:6px 13px;font-size:13px;font-weight:700;cursor:pointer}
.iconbtn{border:1px solid var(--line-2);background:var(--raise);color:var(--ink-2);
  border-radius:10px;padding:8px 10px;cursor:pointer;line-height:1;white-space:nowrap}
.iconbtn:hover{border-color:var(--accent);color:var(--accent)}
.iconbtn .n{font-weight:700;color:var(--ink)}
@media (max-width:640px){
  .topin{flex-wrap:wrap;gap:10px}
  .brand{flex:1}
  .ask{order:3;flex:1 0 100%}
  nav.lenses{top:104px}
  aside.facets{top:auto}
  .resulthead{align-items:flex-start}
  .resulthead select.control{max-width:60vw}
}

/* ── Lenses ──────────────────────────────────────────────────────────────── */
nav.lenses{background:var(--raise);border-bottom:1px solid var(--line);
  position:sticky;top:57px;z-index:30}
.lensrow{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none}
.lensrow::-webkit-scrollbar{display:none}
.lens{border:0;background:none;padding:11px 13px;cursor:pointer;color:var(--muted);
  font-weight:600;font-size:14px;border-bottom:2px solid transparent;white-space:nowrap}
.lens:hover{color:var(--ink)}
.lens.on{color:var(--accent);border-bottom-color:var(--accent)}
.lens i{font-style:normal;color:var(--faint);font-weight:600;margin-left:6px;font-size:12px}
.lens.on i{color:var(--accent)}

/* ── Frame ───────────────────────────────────────────────────────────────── */
.frame{display:grid;grid-template-columns:250px 1fr;gap:22px;padding:20px 0 60px;align-items:start}
@media (max-width:900px){
  .frame{grid-template-columns:1fr}
  aside.facets{position:static;max-height:none}
  aside.facets:not(.open) .facetbody{display:none}
}
aside.facets{position:sticky;top:110px;background:var(--raise);border:1px solid var(--line);
  border-radius:var(--radius);padding:14px;box-shadow:var(--shadow)}
.facethead{display:flex;align-items:center;justify-content:space-between;gap:8px}
.facethead h2{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
#facetToggle{display:none}
@media (max-width:900px){ #facetToggle{display:inline} }
.facet{margin-top:14px}
.facet > label{display:block;font-size:12px;font-weight:700;color:var(--muted);
  text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
select.control, input.control{
  width:100%;padding:8px 10px;border-radius:var(--radius-s);
  border:1px solid var(--line-2);background:var(--sunk);color:var(--ink)}
select.control:focus,input.control:focus{border-color:var(--accent);outline:none}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{border:1px solid var(--line-2);background:var(--raise);color:var(--ink-2);
  border-radius:999px;padding:5px 11px;font-size:12.5px;cursor:pointer}
.chip:hover{border-color:var(--accent);color:var(--accent)}
.chip.on{background:var(--accent);border-color:var(--accent);color:var(--accent-ink);font-weight:600}
.switch{display:flex;align-items:center;gap:8px;font-size:13.5px;color:var(--ink-2);
  padding:5px 0;cursor:pointer}
.switch input{accent-color:var(--accent);width:15px;height:15px}
.linkish{border:0;background:none;color:var(--accent);cursor:pointer;padding:0;font-size:13px}

/* ── Results ─────────────────────────────────────────────────────────────── */
.resulthead{display:flex;align-items:baseline;justify-content:space-between;gap:12px;
  margin-bottom:12px;flex-wrap:wrap}
.resulthead .count{font-weight:700}
.resulthead .sub{color:var(--muted);font-size:13.5px}
.cards{display:flex;flex-direction:column;gap:12px}
.card{background:var(--raise);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px;box-shadow:var(--shadow);transition:box-shadow .15s, border-color .15s, transform .15s}
.card:hover{box-shadow:var(--shadow-lift);border-color:var(--line-2)}
.cardtop{display:flex;gap:12px;align-items:flex-start}
.mono{width:42px;height:42px;flex:0 0 42px;border-radius:11px;background:var(--sunk);
  color:var(--ink-2);display:grid;place-items:center;font-weight:800;font-size:14px;
  border:1px solid var(--line)}
.cardtop h3{font-size:16.5px;font-weight:700}
.cardtop h3 a{color:var(--ink)}
.org{color:var(--muted);font-size:13.5px;margin-top:1px}
.spacer{flex:1}
.save{border:1px solid var(--line-2);background:var(--raise);color:var(--muted);
  border-radius:9px;padding:6px 9px;cursor:pointer;font-size:13px;line-height:1}
.save:hover{color:var(--accent);border-color:var(--accent)}
.save.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);font-weight:700}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:11px}
.tag{font-size:12px;padding:3px 9px;border-radius:999px;background:var(--sunk);
  color:var(--ink-2);border:1px solid var(--line)}
.tag.kind{background:var(--accent-soft);color:var(--accent);border-color:transparent;font-weight:700}
.tag.new{background:var(--good-soft);color:var(--good);border-color:transparent;font-weight:700}
.tag.warn{background:var(--warn-soft);color:var(--warn);border-color:transparent}
.facts{display:flex;flex-wrap:wrap;gap:14px;margin-top:11px;font-size:13.5px}
.facts div{color:var(--muted)}
.facts b{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.06em;
  color:var(--faint);font-weight:700}
.facts span{color:var(--ink-2)}
.why{margin-top:11px;padding:8px 11px;border-radius:var(--radius-s);
  background:var(--good-soft);color:var(--good);font-size:13px;font-weight:600}
.why.plain{background:none;padding:8px 0 0;color:var(--muted);font-weight:500;
  border-top:1px solid var(--line);border-radius:0}
.note{margin-top:10px;color:var(--muted);font-size:13px}
.actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:13px}
.btn{border-radius:10px;padding:8px 13px;font-size:13.5px;font-weight:600;cursor:pointer;
  border:1px solid var(--line-2);background:var(--raise);color:var(--ink)}
.btn:hover{text-decoration:none;border-color:var(--accent);color:var(--accent)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.btn.primary:hover{filter:brightness(1.07);color:var(--accent-ink)}
.more{width:100%;margin-top:16px;padding:12px;border-radius:var(--radius);
  border:1px dashed var(--line-2);background:none;color:var(--ink-2);cursor:pointer}
.more:hover{border-color:var(--accent);color:var(--accent)}
.empty{background:var(--raise);border:1px solid var(--line);border-radius:var(--radius);
  padding:34px 22px;text-align:center;color:var(--muted)}
.empty b{display:block;color:var(--ink);font-size:16px;margin-bottom:6px}

/* ── Strips ──────────────────────────────────────────────────────────────── */
.strip{background:var(--raise);border:1px solid var(--line);border-radius:var(--radius);
  padding:13px 15px;margin-bottom:12px;box-shadow:var(--shadow)}
.strip.warn{background:var(--warn-soft);border-color:transparent;color:var(--warn)}
.strip h3{font-size:14px;margin-bottom:4px}
.strip p{margin:0;color:var(--muted);font-size:13.5px}
.strip.warn p{color:inherit}
.stats{display:flex;gap:18px;flex-wrap:wrap;margin:0 0 14px}
.stat{background:var(--raise);border:1px solid var(--line);border-radius:var(--radius);
  padding:11px 15px;box-shadow:var(--shadow);flex:1;min-width:130px}
.stat b{display:block;font-size:22px;letter-spacing:-.02em}
.stat span{color:var(--muted);font-size:12.5px}
footer{border-top:1px solid var(--line);padding:22px 0 40px;color:var(--muted);font-size:13px}
.hidden{display:none !important}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
</style>
</head>
<body>
<div class="shell" data-autoapply-dashboard>

<header class="top">
  <div class="wrap topin">
    <a class="brand" href="./"><span class="dot">R</span> Radar</a>
    <form class="ask" id="askForm" role="search">
      <span class="mag">⌕</span>
      <input id="ask" type="search" autocomplete="off" spellcheck="false"
             placeholder="Say what you are looking for — “robotics PhD in the UK that funds international students”">
      <button class="go" type="submit">Match</button>
    </form>
    <button class="iconbtn" id="savedBtn" type="button" title="What you kept">★ <span class="n" id="savedCount">0</span></button>
    <button class="iconbtn" id="themeBtn" type="button" title="Light, dark or whatever this device uses">◐</button>
  </div>
</header>

<nav class="lenses" aria-label="Kind of opportunity">
  <div class="wrap lensrow" id="lensRow">
    <button class="lens on" data-lens="match" type="button">Best matches</button>
    <button class="lens" data-lens="roles" type="button">Internships &amp; jobs<i id="nRoles"></i></button>
    <button class="lens" data-lens="research" type="button">PhD &amp; research<i id="nResearch"></i></button>
    <button class="lens" data-lens="ventures" type="button">Ventures<i id="nVentures"></i></button>
    <button class="lens" data-lens="funding" type="button">Funding<i id="nFunding"></i></button>
    <button class="lens" data-lens="universities" type="button">Universities<i id="nUnis"></i></button>
  </div>
</nav>

<div class="wrap frame">
  <aside class="facets" id="facets">
    <div class="facethead">
      <h2 id="facetTitle">Narrow it down</h2>
      <button class="linkish" id="facetToggle" type="button">Show</button>
    </div>
    <div class="facetbody" id="facetBody">
      <div class="facet" id="facetKinds">
        <label>Kind</label>
        <div class="chips" id="kindChips"></div>
      </div>
      <div class="facet" id="facetRegion">
        <label for="region">Where</label>
        <select class="control" id="region"><option value="">Anywhere</option></select>
      </div>
      <div class="facet" id="facetTerm">
        <label for="term">When it starts</label>
        <select class="control" id="term"><option value="">Any term</option></select>
      </div>
      <div class="facet" id="facetLevel">
        <label for="level">Your level</label>
        <select class="control" id="level"><option value="">Any level</option></select>
      </div>
      <div class="facet" id="facetField">
        <label>Field</label>
        <div class="chips" id="fieldChips"></div>
      </div>
      <div class="facet hidden" id="facetUni">
        <label for="country">Country</label>
        <select class="control" id="country"><option value="">Anywhere</option></select>
        <label class="switch" style="margin-top:8px"><input type="checkbox" id="fOpen">
          Only where something is open</label>
      </div>
      <div class="facet hidden" id="facetFunding">
        <label>Study level</label>
        <div class="chips" id="fundLevelChips"></div>
        <label style="margin-top:12px" for="fundCountry">Open to</label>
        <select class="control" id="fundCountry"><option value="">Anywhere</option></select>
      </div>
      <div class="facet hidden" id="facetVenture">
        <label>Kind</label>
        <div class="chips" id="ventureKindChips"></div>
        <label class="switch" style="margin-top:10px"><input type="checkbox" id="fNoEquity">
          Takes no equity</label>
        <label class="switch"><input type="checkbox" id="fVRemote"> Can be done remotely</label>
      </div>
      <div class="facet" id="facetFlags">
        <label>Only show</label>
        <label class="switch"><input type="checkbox" id="fNew"> New since the last run</label>
        <label class="switch"><input type="checkbox" id="fRemote"> Remote</label>
        <label class="switch"><input type="checkbox" id="fAcademic"> At a top-100 university</label>
        <label class="switch"><input type="checkbox" id="fOfficial"> Straight from the employer</label>
        <label class="switch"><input type="checkbox" id="fSaved"> Kept by me</label>
      </div>
      <div class="facet">
        <button class="chip" id="clearAll" type="button">Clear everything</button>
      </div>
    </div>
  </aside>

  <main>
    <div id="stats" class="stats"></div>
    <div id="strips"></div>
    <div class="resulthead">
      <div>
        <span class="count" id="count">—</span>
        <span class="sub" id="countSub"></span>
      </div>
      <div>
        <label class="sr" for="sort">Order</label>
        <select class="control" id="sort" style="width:auto">
          <option value="match">Best match first</option>
          <option value="new">Newest first</option>
          <option value="deadline">Closing soonest</option>
          <option value="company">By organisation</option>
        </select>
      </div>
    </div>
    <div class="cards" id="cards"></div>
    <button class="more hidden" id="more" type="button">Show more</button>
  </main>
</div>

<footer>
  <div class="wrap">
    <p>Checked __GENERATED__. <strong>Radar</strong> watches community boards and official Greenhouse, Ashby and Lever
    feeds, then keeps only what is still open. Verified on __GENERATED__.
    Work authorisation is marked <em>review required</em> when the posting does not say — never
    assumed. <a href="./studio.html">Tailor your CV in the browser</a> ·
    <a href="https://github.com/abyyworld/internship-tracker">How this is built</a></p>
  </div>
</footer>
</div>
<script>
"use strict";
const JOBS = __JOBS__;
const VENTURES = __VENTURES__;
const FUNDING = __FUNDING__;
const UNIS = __UNIVERSITIES__;
const HEALTH = __HEALTH__;
const GENERATED = "__GENERATED__";

const $ = id => document.getElementById(id);
const plain = value => String(value == null ? "" : value)
  .replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE00}-\u{FE0F}\u{2B00}-\u{2BFF}]/gu, "")
  .replace(/\s{2,}/g, " ").trim();
const esc = value => String(value == null ? "" : value)
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
  .replace(/"/g, "&quot;");
const norm = value => String(value == null ? "" : value).toLowerCase();
const uniq = list => [...new Set(list.filter(Boolean))];

/* ── The theme ─────────────────────────────────────────────────────────────
   Three states, not two: whatever this device does, or light, or dark. The
   third is what a reader picks when their device is wrong about them. */
const THEMES = ["system", "light", "dark"];
const THEME_MARK = {system: "Auto", light: "Light", dark: "Dark"};
const THEME_SAYS = {system: "Following this device", light: "Light", dark: "Dark"};
let theme = "system";
function applyTheme() {
  if (theme === "system") document.documentElement.removeAttribute("data-theme");
  else document.documentElement.setAttribute("data-theme", theme);
  $("themeBtn").textContent = THEME_MARK[theme];
  $("themeBtn").title = `${THEME_SAYS[theme]} — press for the next`;
}
try { theme = THEMES.includes(localStorage.getItem("radar.theme")) ? localStorage.getItem("radar.theme") : "system"; }
catch (error) { theme = "system"; }
applyTheme();

/* ── What is kept ──────────────────────────────────────────────────────── */
let saved = new Set();
try { saved = new Set(JSON.parse(localStorage.getItem("radar.saved") || "[]")); }
catch (error) { saved = new Set(); }
function keep(id) {
  if (saved.has(id)) saved.delete(id); else saved.add(id);
  try { localStorage.setItem("radar.saved", JSON.stringify([...saved])); } catch (error) { /* private */ }
  $("savedCount").textContent = String(saved.size);
  render();
}

/* ── One shape for every kind of opportunity ───────────────────────────────
   A PhD position, an accelerator and a scholarship are different things, but
   the question asked of them is the same: does this fit me? So they are all
   reduced to the same handful of fields, and each keeps its own record for
   the parts of the card that differ. */
const PRETTY_REGION = {"US": "United States", "UK": "United Kingdom"};
const PRETTY_COUNTRY = {GB: "United Kingdom", US: "United States", EU: "European Union",
  INTL: "Anywhere in the world", DE: "Germany", CA: "Canada", FR: "France", CH: "Switzerland",
  CN: "China", JP: "Japan", NL: "Netherlands", SE: "Sweden", AU: "Australia", IE: "Ireland"};
const prettyCountry = value => PRETTY_COUNTRY[value] || value || "";
const prettyRegion = value => PRETTY_REGION[value] || value || "";
const RESEARCH_WORDS = /\b(phd|doctoral|postdoc|post-doc|research assistant|research fellow|dphil)\b/i;
function isResearch(job) {
  return job.level === "PhD"
    || ["phd-fellowship", "postdoc", "fellowship"].includes(job.position_type)
    || RESEARCH_WORDS.test(job.role || "");
}

const ITEMS = [];
for (const job of JOBS) {
  ITEMS.push({
    kind: isResearch(job) ? "research" : "role",
    id: `job:${job.id}`,
    title: job.role,
    org: job.company,
    place: job.location || prettyRegion(job.region),
    region: job.region,
    when: job.term,
    level: job.level,
    field: job.category,
    type: job.position_type,
    url: job.url,
    fresh: !!job.new,
    remote: job.work_mode === "remote",
    official: !!job.official_ats,
    academic: !!job.university,
    deadline: job.deadline || "",
    tags: uniq([job.category, job.position_type, job.tier === "elite" ? "elite" : ""]),
    text: norm([job.company, job.role, job.location, prettyRegion(job.region), job.focus,
                job.category, job.position_type, job.level, job.term].join(" ")),
    job,
  });
}
for (const venture of VENTURES) {
  ITEMS.push({
    kind: "venture",
    id: `venture:${venture.id}`,
    title: venture.name,
    org: venture.organisation || venture.name,
    place: venture.geography || venture.location || "",
    region: "",
    when: venture.duration || "",
    level: "",
    field: venture.kind || "",
    url: venture.url || venture.apply || "",
    tags: uniq([venture.kind, ...(venture.stage || [])]),
    text: norm([venture.name, venture.organisation, venture.kind, (venture.stage || []).join(" "),
                venture.who_for, venture.gives, venture.geography, venture.format].join(" ")),
    venture,
  });
}
for (const scheme of FUNDING) {
  ITEMS.push({
    kind: "funding",
    id: `funding:${scheme.id}`,
    title: scheme.name,
    org: scheme.funder || "",
    place: prettyCountry(scheme.country),
    region: "",
    when: scheme.cycle || "",
    level: (scheme.levels || []).join(", "),
    field: "funding",
    url: scheme.url || "",
    tags: uniq([...(scheme.levels || []), ...(scheme.covers || [])]),
    text: norm([scheme.name, scheme.funder, scheme.country, prettyCountry(scheme.country),
                (scheme.levels || []).join(" "),
                scheme.eligibility, (scheme.covers || []).join(" ")].join(" ")),
    scheme,
  });
}
for (const uni of UNIS) {
  ITEMS.push({
    kind: "university",
    id: `uni:${uni.name}`,
    title: uni.name,
    org: uni.country || "",
    place: uni.country || "",
    region: "",
    when: "",
    level: "",
    field: "university",
    url: uni.links ? uni.links.directory : "",
    tags: uniq([uni.country, uni.rank ? `world #${uni.rank}` : "",
                uni.openings ? `${uni.openings} open here` : ""]),
    text: norm([uni.name, uni.country, uni.domain, (uni.aliases || []).join(" ")].join(" ")),
    uni,
  });
}

/* ── Reading what someone typed ────────────────────────────────────────────
   Not an AI: a vocabulary built out of the data itself, so it stays true as
   the data changes, and so the page works with no key and no network. What
   it recognises, it says out loud on every card it returns. */
const VOCAB = {region: new Map(), term: new Map(), level: new Map(), field: new Map()};
const alias = (map, phrase, value) => { if (phrase && value) map.set(norm(phrase), value); };
for (const job of JOBS) {
  alias(VOCAB.region, job.region, job.region);
  alias(VOCAB.region, prettyRegion(job.region), job.region);
  alias(VOCAB.term, job.term, job.term);
  alias(VOCAB.level, job.level, job.level);
  alias(VOCAB.field, job.category, job.category);
}
for (const [phrase, value] of [["uk", "UK"], ["britain", "UK"], ["england", "UK"],
    ["united kingdom", "UK"], ["us", "US"], ["usa", "US"], ["states", "US"],
    ["america", "US"], ["european", "Europe"]]) {
  if ([...VOCAB.region.values()].includes(value)) alias(VOCAB.region, phrase, value);
}
for (const [phrase, value] of [["robotics", "Robotics & Embodied AI"], ["robot", "Robotics & Embodied AI"],
    ["ml", "AI / ML"], ["machine learning", "AI / ML"], ["ai", "AI / ML"],
    ["quant", "Quant / Finance"], ["trading", "Quant / Finance"],
    ["software", "Software Engineering"], ["swe", "Software Engineering"],
    ["hardware", "Hardware / EE"], ["security", "Security"], ["data", "Data"]]) {
  if ([...VOCAB.field.values()].includes(value)) alias(VOCAB.field, phrase, value);
}
const KIND_WORDS = [
  [/\b(phd|doctoral|dphil|postdoc|post-doc|research)\b/, "research"],
  [/\b(intern|internship|placement|summer|new grad|graduate scheme|job|role)\b/, "role"],
  [/\b(accelerator|incubator|fellowship programme|founder|startup programme|venture)\b/, "venture"],
  [/\b(fund|funding|scholarship|grant|stipend|bursary|tuition)\b/, "funding"],
  [/\b(university|universities|uni|school|campus|supervisor|professor|prof|lab)\b/, "university"],
];
const STOP = new Set(("a an and are as at be but by for from how i im in is it me my of on or "
  + "that the to want with you your looking need would like get find role roles position "
  + "positions opportunity opportunities apply please can").split(" "));

function readQuery(text) {
  const raw = norm(text).replace(/[^a-z0-9+#/ .-]/g, " ").replace(/\s+/g, " ").trim();
  const query = {raw, words: [], region: "", term: "", level: "", fields: [], kinds: [],
                 remote: false, funded: false};
  if (!raw) return query;
  const eat = (map, longestFirst) => {
    for (const phrase of longestFirst) {
      if (phrase && raw.includes(phrase)) return map.get(phrase);
    }
    return "";
  };
  const byLength = map => [...map.keys()].sort((a, b) => b.length - a.length);
  query.region = eat(VOCAB.region, byLength(VOCAB.region));
  query.term = eat(VOCAB.term, byLength(VOCAB.term));
  query.level = eat(VOCAB.level, byLength(VOCAB.level));
  for (const phrase of byLength(VOCAB.field)) {
    if (raw.includes(phrase)) query.fields.push(VOCAB.field.get(phrase));
  }
  query.fields = uniq(query.fields);
  for (const [pattern, kind] of KIND_WORDS) if (pattern.test(raw)) query.kinds.push(kind);
  query.kinds = uniq(query.kinds);
  query.remote = /\bremote\b|\bfrom home\b/.test(raw);
  query.funded = /\bfunded\b|\bfully funded\b|\bstipend\b|\bpaid\b|\bscholarship\b/.test(raw);
  query.words = uniq(raw.split(" ").filter(word => word.length > 2 && !STOP.has(word)));
  return query;
}

/* What matched, and why — the "why" is the part a filter box can never give. */
// Saying "in the UK" is not a hint to weigh — it is a condition. Ranking alone
// put Sunnyvale above London for "robotics PhD in the UK", which is not what
// anybody means. The narrowing is dropped only when it would leave nothing.
function insisted(item, query) {
  if (!query.region) return true;
  if (!["role", "research"].includes(item.kind)) return true;
  return item.region === query.region || norm(item.place).includes(norm(prettyRegion(query.region)));
}

function scoreItem(item, query) {
  if (!query.raw) return {score: 0, why: []};
  let score = 0;
  const why = [];
  if (query.region && item.region === query.region) { score += 8; why.push(prettyRegion(query.region)); }
  if (query.term && item.when === query.term) { score += 6; why.push(query.term); }
  if (query.level && item.level === query.level) { score += 6; why.push(query.level); }
  for (const field of query.fields) {
    if (item.field === field) { score += 7; why.push(field); }
    else if (item.text.includes(norm(field))) score += 2;
  }
  if (query.kinds.length) {
    // The lens already says what kind these are; repeating it is not a reason.
    if (query.kinds.includes(item.kind)) score += 5;
    else score -= 3;
  }
  if (query.remote && item.remote) { score += 4; why.push("remote"); }
  if (query.funded && (item.kind === "funding" || /stipend|funded/.test(item.text))) {
    score += 3;
    why.push("funded");
  }
  let hits = 0;
  const spare = [];
  for (const word of query.words) {
    if (!item.text.includes(word)) continue;
    score += 2;
    hits += 1;
    // A word already named by a chip above adds nothing by being repeated.
    if (!why.some(said => norm(said).includes(word))) spare.push(word);
  }
  if (spare.length) why.push(spare.slice(0, 3).join(", "));
  if (item.fresh) score += 0.6;
  if (item.official) score += 0.4;
  return {score, why: uniq(why).slice(0, 4)};
}

const KIND_LABEL = {role: "Internship or job", research: "PhD & research",
                    venture: "Venture programme", funding: "Funding", university: "University"};

/* ── The cards ─────────────────────────────────────────────────────────── */
const mono = name => (plain(name) || "?").split(/\s+/).slice(0, 2)
  .map(word => word[0] || "").join("").toUpperCase();
const tagHtml = (list, extra = "") => list.filter(Boolean)
  .map(tag => `<span class="tag ${extra}">${esc(tag)}</span>`).join("");

function factsHtml(pairs) {
  const cells = pairs.filter(pair => pair[1])
    .map(pair => `<div><b>${esc(pair[0])}</b><span>${esc(pair[1])}</span></div>`).join("");
  return cells ? `<div class="facts">${cells}</div>` : "";
}

function whyHtml(item, why, reason) {
  if (reason) return `<div class="why">${esc(reason)}</div>`;
  if (why && why.length) return `<div class="why plain">Matches ${esc(why.join(" · "))}</div>`;
  return "";
}

function tailorUrl(job) {
  // Never a direct link to 127.0.0.1: when the helper is not running that is a
  // dead end, and the opener decides between the local editor and the studio.
  return "./open.html?url=" + encodeURIComponent(job.url)
    + "&role=" + encodeURIComponent(job.role || "")
    + "&company=" + encodeURIComponent(job.company || "")
    + (job.location ? "&location=" + encodeURIComponent(job.location) : "")
    + (job.focus ? "&tags=" + encodeURIComponent(job.focus) : "");
}

function supervisorHtml(job) {
  const uni = job.university;
  if (!uni) return "";
  const figures = uni.scorecard && uni.scorecard.summary ? ` · ${esc(uni.scorecard.summary)}` : "";
  const topics = (uni.terms || []).join(", ");
  return `<div class="note"><b>${esc(uni.name)}</b>${uni.rank ? ` · world #${esc(uni.rank)}` : ""}${figures}<br>
    ${topics ? `Who takes students for ${esc(topics)}: ` : "Who takes students: "}
    <a href="${esc(uni.scholar)}" target="_blank" rel="noopener">academics</a> ·
    <a href="${esc(uni.openalex)}" target="_blank" rel="noopener">recent papers</a> ·
    <a href="${esc(uni.directory)}" target="_blank" rel="noopener">department directory</a></div>`;
}

function cardHtml(item, why, reason) {
  const kept = saved.has(item.id);
  const star = `<button class="save${kept ? " on" : ""}" data-keep="${esc(item.id)}"
    title="${kept ? "Kept" : "Keep this"}" type="button">${kept ? "★" : "☆"}</button>`;
  const head = (rawTitle, rawOrg, href) => {
    const title = plain(rawTitle), org = plain(rawOrg);
    return `<div class="cardtop">
      <div class="mono">${esc(mono(org || title))}</div>
      <div><h3>${href ? `<a href="${esc(href)}" target="_blank" rel="noopener">${esc(title)}</a>`
                       : esc(title)}</h3>
        <div class="org">${esc(org)}</div></div>
      <div class="spacer"></div>${star}</div>`;
  };

  if (item.kind === "role" || item.kind === "research") {
    const job = item.job;
    const tags = tagHtml([KIND_LABEL[item.kind]], "kind")
      + (job.new ? `<span class="tag new">new</span>` : "")
      + tagHtml(item.tags)
      + (job.eligibility && job.eligibility !== "eligible"
         ? `<span class="tag warn">${esc(job.eligibility)}</span>` : "");
    return `<article class="card">${head(job.role, job.company, job.url)}
      <div class="tags">${tags}</div>
      ${factsHtml([["Where", item.place],
                   ["Term", job.term && !["Unknown", "Ambiguous"].includes(job.term) ? job.term : ""],
                   ["Level", job.level && job.level !== "Unknown" ? job.level : ""],
                   ["How", job.work_mode && job.work_mode !== "unspecified" ? job.work_mode : ""]])}
      ${whyHtml(item, why, reason)}
      ${job.focus ? `<div class="note">${esc(job.focus.replaceAll(",", ", "))}</div>` : ""}
      ${supervisorHtml(job)}
      <div class="actions">
        <a class="btn primary" href="${esc(tailorUrl(job))}" target="_blank" rel="noopener">✦ Edit CV for this job</a>
        <a class="btn job-link" data-no-autoapply="1" href="${esc(job.url)}" target="_blank" rel="noopener">Open posting</a>
      </div></article>`;
  }

  if (item.kind === "venture") {
    const venture = item.venture;
    return `<article class="card">${head(venture.name, venture.organisation || "", venture.url)}
      <div class="tags">${tagHtml([KIND_LABEL.venture], "kind")}${tagHtml(item.tags)}</div>
      ${factsHtml([["Gives", venture.gives || ""], ["Equity", venture.equity || ""],
                   ["Format", venture.format || ""], ["Runs for", venture.duration || ""]])}
      ${whyHtml(item, why, reason)}
      ${venture.who_for ? `<div class="note">${esc(venture.who_for)}</div>` : ""}
      <div class="actions">
        ${venture.url ? `<a class="btn primary" href="${esc(venture.url)}" target="_blank" rel="noopener">Open programme</a>` : ""}
      </div></article>`;
  }

  if (item.kind === "funding") {
    const scheme = item.scheme;
    return `<article class="card">${head(scheme.name, scheme.funder || "", scheme.url)}
      <div class="tags">${tagHtml([KIND_LABEL.funding], "kind")}${tagHtml(item.tags)}</div>
      ${factsHtml([["Open to", prettyCountry(scheme.country)], ["Covers", (scheme.covers || []).join(", ")],
                   ["Level", (scheme.levels || []).join(", ")], ["Cycle", scheme.cycle || ""]])}
      ${whyHtml(item, why, reason)}
      ${scheme.eligibility ? `<div class="note">${esc(scheme.eligibility)}</div>` : ""}
      <div class="actions">
        ${scheme.url ? `<a class="btn primary" href="${esc(scheme.url)}" target="_blank" rel="noopener">Open the scheme</a>` : ""}
      </div></article>`;
  }

  const uni = item.uni;
  const card = uni.scorecard || {};
  const initials = mono(uni.name);
  const money = value => value ? "$" + Number(value).toLocaleString("en-US") : "";
  const percent = value => value || value === 0 ? Math.round(value * 100) + "%" : "";
  return `<article class="card">${head(uni.name, uni.country || "", uni.links && uni.links.directory)
      .replace(`<div class="mono">${esc(mono(uni.country || uni.name))}</div>`,
               `<div class="mono">${esc(initials)}</div>`)}
    <div class="tags">${tagHtml([KIND_LABEL.university], "kind")}${tagHtml(item.tags)}</div>
    ${factsHtml([["Admits", percent(card.admission_rate)],
                 ["Students", card.students ? Number(card.students).toLocaleString("en-US") : ""],
                 ["Tuition", money(card.tuition)],
                 ["Earnings after 10y", money(card.earnings)]])}
    ${whyHtml(item, why, reason)}
    ${uni.openings ? `<div class="note">${uni.openings} open ${uni.openings === 1 ? "position" : "positions"} here right now.</div>` : ""}
    <div class="actions">
      ${uni.openings ? `<button class="btn primary" data-uni="${esc(uni.name)}" type="button">See its positions</button>` : ""}
      ${uni.links ? `<a class="btn" href="${esc(uni.links.directory)}" target="_blank" rel="noopener">Faculty directory</a>` : ""}
      ${uni.links ? `<a class="btn" href="${esc(uni.links.openalex)}" target="_blank" rel="noopener">What they publish</a>` : ""}
    </div></article>`;
}

/* ── State ─────────────────────────────────────────────────────────────── */
const KINDS_IN_LENS = {
  match: ["role", "research", "venture", "funding", "university"],
  roles: ["role"], research: ["research"], ventures: ["venture"],
  funding: ["funding"], universities: ["university"],
};
let lens = "match";
let query = readQuery("");
let kindPicks = new Set();
let fieldPicks = new Set();
let fundPicks = new Set();
let venturePicks = new Set();
let shown = 25;
let ranked = null;          // what the model said, when it was asked

function facetsFor(lens) {
  const showsJobs = ["match", "roles", "research"].includes(lens);
  $("facetUni").classList.toggle("hidden", lens !== "universities");
  $("facetFunding").classList.toggle("hidden", lens !== "funding");
  $("facetVenture").classList.toggle("hidden", lens !== "ventures");
  // Sorting by a deadline means nothing to a university, and sorting by rank
  // means nothing to a job.
  const options = lens === "universities"
    ? [["match", "Best match first"], ["rank", "World rank"], ["openings", "Most open positions"],
       ["admits", "Hardest to get into"]]
    : [["match", "Best match first"], ["new", "Newest first"],
       ["deadline", "Closing soonest"], ["company", "By organisation"]];
  const sort = $("sort");
  if (sort.dataset.shape !== lens) {
    const wanted = sort.value;
    sort.replaceChildren();
    for (const [value, label] of options) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      option.selected = value === wanted;
      sort.append(option);
    }
    if (!options.some(pair => pair[0] === sort.value)) sort.value = "match";
    sort.dataset.shape = lens;
  }
  $("facetRegion").classList.toggle("hidden", !showsJobs);
  $("facetTerm").classList.toggle("hidden", !showsJobs);
  $("facetLevel").classList.toggle("hidden", !showsJobs);
  $("facetField").classList.toggle("hidden", !showsJobs);
  $("facetKinds").classList.toggle("hidden", lens !== "match");
  $("facetFlags").classList.toggle("hidden", lens === "universities" || lens === "funding");
}

function pool() {
  const kinds = KINDS_IN_LENS[lens];
  let list = ITEMS.filter(item => kinds.includes(item.kind));
  if (lens === "match" && kindPicks.size) list = list.filter(item => kindPicks.has(item.kind));
  const region = $("region").value, term = $("term").value, level = $("level").value;
  if (region) list = list.filter(item => item.region === region || item.kind === "university");
  if (term) list = list.filter(item => item.when === term || !["role", "research"].includes(item.kind));
  if (level) list = list.filter(item => item.level === level || !["role", "research"].includes(item.kind));
  if (fieldPicks.size) {
    list = list.filter(item => fieldPicks.has(item.field) || !["role", "research"].includes(item.kind));
  }
  if ($("fNew").checked) list = list.filter(item => item.fresh);
  if ($("fRemote").checked) list = list.filter(item => item.remote);
  if ($("fAcademic").checked) list = list.filter(item => item.academic || item.kind === "university");
  if ($("fOfficial").checked) list = list.filter(item => item.official);
  if ($("fSaved").checked) list = list.filter(item => saved.has(item.id));
  if (lens === "funding") {
    const country = $("fundCountry").value;
    if (country) list = list.filter(item => item.scheme.country === country);
    if (fundPicks.size) {
      list = list.filter(item => (item.scheme.levels || []).some(level => fundPicks.has(level)));
    }
  }
  if (lens === "ventures") {
    if (venturePicks.size) list = list.filter(item => venturePicks.has(item.venture.kind));
    // "None while you are still forming" is still none.
    if ($("fNoEquity").checked) {
      list = list.filter(item => /^none/i.test(String(item.venture.equity || "").trim()));
    }
    if ($("fVRemote").checked) list = list.filter(item => item.venture.remote);
  }
  if (lens === "universities") {
    const country = $("country").value;
    if (country) list = list.filter(item => item.uni.country === country);
    if ($("fOpen").checked) list = list.filter(item => item.uni.openings > 0);
  }
  return list;
}

function ordered(list) {
  const scored = list.map(item => ({item, ...scoreItem(item, query)}));
  const mode = $("sort").value;
  const asked = ranked && ranked.order;
  if (asked) {
    scored.forEach(row => {
      const at = asked.indexOf(row.item.id);
      row.aiRank = at < 0 ? 999 : at;
      row.reason = ranked.why[row.item.id] || "";
    });
    scored.sort((a, b) => a.aiRank - b.aiRank || b.score - a.score);
    return scored;
  }
  if (query.raw) scored.sort((a, b) => b.score - a.score || String(a.item.org).localeCompare(b.item.org));
  if (mode === "new") scored.sort((a, b) => Number(b.item.fresh) - Number(a.item.fresh));
  else if (mode === "company") scored.sort((a, b) => String(a.item.org).localeCompare(String(b.item.org)));
  else if (mode === "deadline") {
    scored.sort((a, b) => (a.item.deadline || "9999").localeCompare(b.item.deadline || "9999"));
  } else if (mode === "rank" || (!query.raw && lens === "universities")) {
    scored.sort((a, b) => (a.item.uni.rank || 999) - (b.item.uni.rank || 999));
  } else if (mode === "openings") {
    scored.sort((a, b) => (b.item.uni.openings || 0) - (a.item.uni.openings || 0));
  } else if (mode === "admits") {
    const rate = row => (row.item.uni.scorecard || {}).admission_rate;
    scored.sort((a, b) => (rate(a) == null ? 9 : rate(a)) - (rate(b) == null ? 9 : rate(b)));
  }
  return scored;
}

function render() {
  facetsFor(lens);
  let list = ordered(pool());
  let loosened = "";
  // With something typed, anything that answers none of it is noise.
  if (query.raw && !ranked) {
    const kept = list.filter(row => row.score > 0);
    const insistedOn = kept.filter(row => insisted(row.item, query));
    if (query.region && insistedOn.length >= 3) list = insistedOn;
    else {
      list = kept;
      if (query.region && insistedOn.length < kept.length) {
        loosened = `Only ${insistedOn.length} in ${prettyRegion(query.region)}, so the rest are shown too.`;
      }
    }
  }
  const cards = $("cards");
  const page = list.slice(0, shown);
  cards.innerHTML = page.map(row => cardHtml(row.item, row.why, row.reason)).join("")
    || `<div class="empty"><b>Nothing here answers that yet.</b>
        ${query.raw ? "Try fewer words, or a different lens — funding and universities are "
                    + "listed separately from jobs." : "Clear a filter or two."}</div>`;
  $("more").classList.toggle("hidden", list.length <= shown);
  $("more").textContent = `Show more — ${list.length - shown} left`;
  const NAMED = {match: ["match", "matches"], roles: ["job", "jobs"],
                 research: ["PhD & research post", "PhD & research posts"],
                 ventures: ["venture programme", "venture programmes"],
                 funding: ["funding scheme", "funding schemes"],
                 universities: ["university", "universities"]};
  const named = NAMED[lens] || ["result", "results"];
  $("count").textContent = `${list.length.toLocaleString("en-US")} `
    + (list.length === 1 ? named[0] : named[1]);
  $("countSub").textContent = ranked
    ? `ranked by ${ranked.model}`
    : (query.raw ? `for “${query.raw}”${loosened ? ` — ${loosened}` : ""}` : "");
  for (const button of cards.querySelectorAll("[data-keep]")) {
    button.onclick = () => keep(button.dataset.keep);
  }
  for (const button of cards.querySelectorAll("[data-uni]")) {
    button.onclick = () => {
      $("ask").value = button.dataset.uni;
      query = readQuery(button.dataset.uni);
      setLens("research");
    };
  }
  syncUrl();
}

function setLens(next) {
  lens = next;
  ranked = null;
  shown = 25;
  for (const button of $("lensRow").querySelectorAll(".lens")) {
    button.classList.toggle("on", button.dataset.lens === lens);
  }
  render();
  window.scrollTo({top: 0, behavior: "smooth"});
}

function syncUrl() {
  const params = new URLSearchParams();
  if (query.raw) params.set("q", $("ask").value.trim());
  if (lens !== "match") params.set("lens", lens);
  if ($("region").value) params.set("region", $("region").value);
  const next = params.toString();
  history.replaceState(null, "", next ? `?${next}` : location.pathname);
}

/* ── Asking a model to rank what the page already found ────────────────────
   Optional, and never the only way through: the list above is complete and
   ordered before this is pressed. The key is the one already stored for the
   CV studio on this device — nothing new to set up, and nothing sent anywhere
   the reader has not already chosen. */
const PROVIDERS = {
  gemini: "https://generativelanguage.googleapis.com/v1beta/openai",
  openrouter: "https://openrouter.ai/api/v1",
  groq: "https://api.groq.com/openai/v1",
  openai: "https://api.openai.com/v1",
};
function storedProvider() {
  let id = "gemini", base = "", key = "", model = "";
  try {
    id = localStorage.getItem("studio.provider") || "gemini";
    base = id === "custom" ? (localStorage.getItem("studio.base") || "") : (PROVIDERS[id] || "");
    key = localStorage.getItem(`studio.key.${id}`) || "";
    model = localStorage.getItem(`studio.model.${id}`) || "gemini-2.5-flash-lite";
  } catch (error) { /* private mode */ }
  return {id, base, key, model};
}

async function rankWithModel() {
  const {base, key, model} = storedProvider();
  const button = $("rankBtn");
  if (!base || !key) {
    $("rankNote").innerHTML = 'No key on this device yet — set one once in the '
      + '<a href="./studio.html">CV studio</a> and this page can use it too.';
    return;
  }
  const candidates = ordered(pool()).filter(row => !query.raw || row.score > 0).slice(0, 40);
  if (!candidates.length) { $("rankNote").textContent = "Nothing to rank yet."; return; }
  button.disabled = true;
  const was = button.textContent;
  button.textContent = "Reading them…";
  $("rankNote").textContent = `Asking ${model} to read ${candidates.length} of them.`;
  const lines = candidates.map(row => {
    const item = row.item;
    return `${item.id} | ${KIND_LABEL[item.kind]} | ${item.title} | ${item.org} | `
      + `${item.place} | ${item.when} | ${item.level} | ${item.tags.join(", ")}`;
  }).join("\n");
  const prompt = [
    `Someone is looking for: ${$("ask").value.trim() || "anything worth applying for"}`,
    "",
    "Here are opportunities already found for them. Each line is:",
    "id | kind | title | organisation | where | when | level | tags",
    lines,
    "",
    "Return the ones actually worth their time, best first, at most 12, as JSON only:",
    '{"picks":[{"id":"job:abc","why":"one sentence on why this one, in plain words"}]}',
    "Leave out anything that does not fit what they asked for. Never invent an id.",
  ].join("\n");
  try {
    const response = await fetch(base.replace(/\/+$/, "") + "/chat/completions", {
      method: "POST",
      headers: {"Content-Type": "application/json", "Authorization": `Bearer ${key}`},
      body: JSON.stringify({
        model,
        messages: [
          {role: "system", content: "You match people to opportunities. You never invent one, "
            + "and you say plainly why each is worth their time."},
          {role: "user", content: prompt},
        ],
        temperature: 0.2,
        max_tokens: 2000,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      const said = (Array.isArray(payload) ? payload[0] : payload) || {};
      throw new Error((said.error && said.error.message) || `${response.status}`);
    }
    const content = payload.choices && payload.choices[0] && payload.choices[0].message
      && payload.choices[0].message.content;
    const text = String(content || "").replace(/```(?:json)?/g, "");
    const parsed = JSON.parse(text.slice(text.indexOf("{"), text.lastIndexOf("}") + 1));
    const picks = (parsed.picks || []).filter(pick => pick && pick.id);
    if (!picks.length) throw new Error("it found nothing here worth ranking");
    ranked = {model, order: picks.map(pick => pick.id), why: {}};
    for (const pick of picks) ranked.why[pick.id] = String(pick.why || "");
    shown = Math.max(shown, picks.length);
    $("rankNote").textContent = `${picks.length} picked out by ${model}. Press again after changing what you asked for.`;
    render();
  } catch (error) {
    $("rankNote").textContent = `${model} could not rank these: ${error.message}. `
      + "The list below is still complete and ordered.";
  } finally {
    button.disabled = false;
    button.textContent = was;
  }
}

/* ── Setting the page up ───────────────────────────────────────────────── */
function countBy(list, get) {
  const counts = new Map();
  for (const item of list) {
    const value = get(item);
    if (value && value !== "Unknown" && value !== "unspecified") {
      counts.set(value, (counts.get(value) || 0) + 1);
    }
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1]);
}

function fillSelect(id, pairs, pretty = value => value) {
  const select = $(id);
  const first = select.options[0];
  select.replaceChildren(first);
  for (const [value, count] of pairs) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = `${pretty(value)} (${count})`;
    select.append(option);
  }
}

function chipRow(id, values, picks) {
  const box = $(id);
  box.replaceChildren();
  for (const [value, label] of values) {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "chip" + (picks.has(value) ? " on" : "");
    chip.textContent = label;
    chip.onclick = () => {
      if (picks.has(value)) picks.delete(value); else picks.add(value);
      chip.classList.toggle("on");
      shown = 25;
      render();
    };
    box.append(chip);
  }
}

const jobs = ITEMS.filter(item => item.kind === "role" || item.kind === "research");
fillSelect("region", countBy(jobs, item => item.region), prettyRegion);
fillSelect("term", countBy(jobs, item => item.when));
fillSelect("level", countBy(jobs, item => item.level));
fillSelect("country", countBy(ITEMS.filter(item => item.kind === "university"),
                              item => item.uni.country));
chipRow("fieldChips", countBy(jobs, item => item.field).slice(0, 10).map(([value]) => [value, value]),
        fieldPicks);
chipRow("kindChips", Object.entries(KIND_LABEL).map(([value, label]) => [value, label]), kindPicks);
chipRow("fundLevelChips",
        countBy(FUNDING.flatMap(scheme => scheme.levels || []), level => level)
          .map(([value]) => [value, value]), fundPicks);
chipRow("ventureKindChips", countBy(VENTURES, venture => venture.kind).map(([value]) => [value, value]),
        venturePicks);
fillSelect("fundCountry", countBy(FUNDING, scheme => scheme.country), prettyCountry);

const counts = {
  role: ITEMS.filter(item => item.kind === "role").length,
  research: ITEMS.filter(item => item.kind === "research").length,
  venture: VENTURES.length, funding: FUNDING.length, university: UNIS.length,
};
$("nRoles").textContent = counts.role.toLocaleString("en-US");
$("nResearch").textContent = counts.research;
$("nVentures").textContent = counts.venture;
$("nFunding").textContent = counts.funding;
$("nUnis").textContent = counts.university;
$("savedCount").textContent = String(saved.size);

$("stats").innerHTML = [
  [counts.role + counts.research, "open positions"],
  [counts.research, "PhD, postdoc and research posts"],
  [jobs.filter(item => item.fresh).length, "new since the last run"],
  [counts.venture + counts.funding, "programmes and funding schemes"],
].map(([number, label]) =>
  `<div class="stat"><b>${Number(number).toLocaleString("en-US")}</b><span>${esc(label)}</span></div>`).join("");

function renderStrips() {
  const parts = [];
  parts.push(`<div class="strip"><h3>Say it in your own words</h3>
    <p>“robotics internship in the UK for summer 2027”, “fully funded PhD in machine learning”,
    “accelerator that takes no equity”. Every card says which part of that it answers.
    Nothing you type leaves this page unless you press the button below.</p>
    <div class="actions">
      <button class="btn" id="rankBtn" type="button">Rank these with your own AI key</button>
      <span class="note" id="rankNote" style="margin:0;align-self:center"></span>
    </div></div>`);
  const alerts = (HEALTH && HEALTH.alerts) || [];
  if (alerts.length) {
    const said = alerts.slice(0, 3).map(alert => typeof alert === "string" ? alert
      : `${alert.source || "a source"}: ${alert.detail || alert.kind || "did not answer"}`);
    parts.push(`<div class="strip warn"><h3>${alerts.length} source${alerts.length === 1 ? "" : "s"} to watch</h3>
      <p>${esc(said.join(" · "))}. Roles from those sources are kept and marked,
      never silently closed.</p></div>`);
  }
  $("strips").innerHTML = parts.join("");
  $("rankBtn").onclick = rankWithModel;
}
renderStrips();

/* ── Events ────────────────────────────────────────────────────────────── */
let typing = null;
$("askForm").onsubmit = event => {
  event.preventDefault();
  clearTimeout(typing);
  query = readQuery($("ask").value);
  ranked = null;
  shown = 25;
  if (query.kinds.length === 1 && lens === "match") {
    const only = query.kinds[0];
    const lensFor = {role: "roles", research: "research", venture: "ventures",
                     funding: "funding", university: "universities"};
    if (lensFor[only]) { setLens(lensFor[only]); return; }
  }
  render();
};
$("ask").oninput = () => {
  clearTimeout(typing);
  typing = setTimeout(() => {
    query = readQuery($("ask").value);
    ranked = null;
    shown = 25;
    render();
  }, 220);
};
for (const button of $("lensRow").querySelectorAll(".lens")) {
  button.onclick = () => setLens(button.dataset.lens);
}
for (const id of ["region", "term", "level", "sort", "country", "fundCountry"]) {
  $(id).onchange = () => { shown = 25; render(); };
}
for (const id of ["fNew", "fRemote", "fAcademic", "fOfficial", "fSaved", "fOpen",
                  "fNoEquity", "fVRemote"]) {
  $(id).onchange = () => { shown = 25; render(); };
}
$("more").onclick = () => { shown += 25; render(); };
$("clearAll").onclick = () => {
  $("ask").value = "";
  query = readQuery("");
  for (const id of ["region", "term", "level"]) $(id).value = "";
  for (const id of ["fNew", "fRemote", "fAcademic", "fOfficial", "fSaved"]) $(id).checked = false;
  kindPicks.clear();
  fieldPicks.clear();
  fundPicks.clear();
  venturePicks.clear();
  for (const chip of document.querySelectorAll(".chips .chip.on")) chip.classList.remove("on");
  for (const id of ["country", "fundCountry"]) $(id).value = "";
  for (const id of ["fOpen", "fNoEquity", "fVRemote"]) $(id).checked = false;
  chipRow("fieldChips", countBy(jobs, item => item.field).slice(0, 10).map(([value]) => [value, value]), fieldPicks);
  chipRow("kindChips", Object.entries(KIND_LABEL).map(([value, label]) => [value, label]), kindPicks);
  ranked = null;
  shown = 25;
  render();
};
$("savedBtn").onclick = () => {
  $("fSaved").checked = !$("fSaved").checked;
  shown = 25;
  render();
};
$("themeBtn").onclick = () => {
  theme = THEMES[(THEMES.indexOf(theme) + 1) % THEMES.length];
  try { localStorage.setItem("radar.theme", theme); } catch (error) { /* private mode */ }
  applyTheme();
};
$("facetToggle").onclick = () => {
  const open = $("facets").classList.toggle("open");
  $("facetToggle").textContent = open ? "Hide" : "Show";
};

/* Whatever the link said, before anything is drawn. */
const opened = new URLSearchParams(location.search);
if (opened.get("q")) { $("ask").value = opened.get("q"); query = readQuery(opened.get("q")); }
if (opened.get("region")) $("region").value = opened.get("region");
if (KINDS_IN_LENS[opened.get("lens")]) lens = opened.get("lens");
for (const button of $("lensRow").querySelectorAll(".lens")) {
  button.classList.toggle("on", button.dataset.lens === lens);
}
render();
</script>
</body>
</html>
"""
