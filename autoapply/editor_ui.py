from __future__ import annotations


# The middle pane is a live preview of the printed CV, not a second design.
# Every size below is the PDF's point size multiplied by 1.44 (the ratio of the
# 736px editable paper to the 510pt print column), and the colours, fonts, rules
# and letterspacing are the same constants autoapply/cv_render.py prints with,
# so what you edit is what the exported PDF looks like.
EDITOR_PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CV Studio</title>
<style>
:root{color-scheme:dark;--bg:#07110f;--panel:#0d1b17;--panel2:#13251f;
--line:#29473d;--text:#f3f8f6;--muted:#9fb5ad;--green:#71efae;
--green2:#27bd79;--blue:#7db6ff;--red:#ff938b;--amber:#ffcf70;--purple:#c4a0ff;
--ink:#111111;--accent:#14324F;--date:#2B3A47;--sub:#3D4A56;--meta:#6B6B6B;
--rule:#9DB2C2;--hair:#D8E0E6;--serif:"Times New Roman",Times,Georgia,serif;
--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 18% -10%,#15533a77,
transparent 38rem),var(--bg);color:var(--text);font:14px/1.5 var(--sans)}
button,input,textarea,select{font:inherit}
button,a.button{border:1px solid var(--line);border-radius:10px;min-height:40px;padding:0 14px;
font-weight:800;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;
justify-content:center}.primary{background:var(--green2);color:#03130c}.secondary{background:#152821;
color:var(--text)}.ghost{background:transparent;color:var(--muted)}button:disabled{opacity:.45;
cursor:not-allowed}.shell{min-height:100vh;display:grid;grid-template-rows:auto 1fr}
header{position:sticky;z-index:10;top:0;background:#07110fe8;backdrop-filter:blur(14px);
border-bottom:1px solid var(--line);padding:12px 18px;display:flex;align-items:center;gap:14px}
.brand{font-size:18px;font-weight:950;letter-spacing:-.04em;white-space:nowrap}.brand b{color:var(--green)}
.job{min-width:0;flex:1}.job strong,.job span{display:block;white-space:nowrap;overflow:hidden;
text-overflow:ellipsis}.job span{color:var(--muted);font-size:12px}
.fit-pill{border:1px solid var(--line);border-radius:99px;padding:4px 10px;font-size:12px;
font-weight:900;white-space:nowrap;color:var(--muted)}
.fit-pill.good{border-color:#2a7455;color:var(--green)}
.fit-pill.medium{border-color:#7a6030;color:var(--amber)}
.fit-pill.low{border-color:#6f3430;color:var(--red)}
.layout{display:grid;grid-template-columns:330px minmax(0,1.5fr) 300px;gap:0;
height:calc(100vh - 57px);overflow:hidden}
.pane{height:100%;overflow-y:auto;display:flex;flex-direction:column}
.pane-header{position:sticky;top:0;z-index:5;background:#07110f;border-bottom:1px solid var(--line);
padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-shrink:0}
.pane-left{border-right:1px solid var(--line)}
.pane-right{border-left:1px solid var(--line)}
.pane-body{padding:14px 16px;flex:1}
.pane-doc{background:#0a1210;padding:22px 16px 60px}
.card{background:linear-gradient(145deg,var(--panel2),var(--panel));border:1px solid var(--line);
border-radius:14px;padding:16px;margin-bottom:12px}
.eyebrow{color:var(--green);font-size:10px;font-weight:950;letter-spacing:.14em;text-transform:uppercase}
.eyebrow.purple{color:var(--purple)}.eyebrow.blue{color:var(--blue)}
h1,h2,h3,p{margin-top:0}h1{font-size:24px;letter-spacing:-.04em;margin:4px 0 5px}
h2{font-size:17px}h3{font-size:13px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.muted{color:var(--muted)}
.notice{border:1px solid #66552b;background:#2b2414;padding:11px 13px;border-radius:11px;
color:#ffe1a1;margin-bottom:12px}.notice.error{border-color:#6f3430;background:#2a1715;
color:var(--red)}.notice.ok{border-color:#285f49;background:#10271e;color:var(--green)}
.suggestion{border:1px solid var(--line);background:#091410;border-radius:13px;padding:13px;margin-top:10px}
.suggestion-head{display:flex;justify-content:space-between;gap:8px;margin-bottom:8px}
.label{font-size:10px;font-weight:900;color:var(--blue);letter-spacing:.08em;text-transform:uppercase}
.rationale{color:var(--muted);font-size:11.5px;line-height:1.5;margin:6px 0}
.choice-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}

/* ── The paper. Sizes are print points x 1.44, colours are the PDF's. ────── */
.cv-paper{background:#fff;color:var(--ink);font-family:var(--serif);
width:100%;max-width:840px;margin:0 auto;padding:50px 52px 60px;border-radius:4px;
box-shadow:0 24px 70px #000a,0 0 0 1px #ffffff14}
.cv-name{font:700 34.5px/1.15 var(--serif);text-align:center;letter-spacing:.2em;
text-transform:uppercase;padding-left:.2em}
.cv-tagline{font:italic 16.5px/1.25 var(--serif);text-align:center;color:var(--accent);margin-top:9px}
.cv-contact{font:12px/1.35 var(--sans);text-align:center;color:var(--meta);margin-top:7px}
.cv-rule-strong{height:2.3px;background:var(--accent);margin:12px 0 14px}
.cv-summary{font-size:14.4px;line-height:1.32;text-align:center}
.cv-section{margin-top:19px}
.cv-section-head{font:800 14.4px/1.2 var(--sans);letter-spacing:.36em;text-transform:uppercase;
color:var(--accent)}
.cv-section-rule{height:1.4px;background:var(--rule);margin:7px 0 10px}
.cv-entry{margin-bottom:7px}
.cv-entry-head{display:flex;align-items:baseline;justify-content:space-between;gap:14px}
.cv-entry-title{font-weight:700;font-size:15.5px;line-height:1.2}
.cv-entry-dates{font:700 12px/1.5 var(--sans);color:var(--date);white-space:nowrap}
.cv-entry-sub{font:italic 14px/1.35 var(--serif);color:var(--sub);margin-top:1px}
.cv-para{font-size:14px;line-height:1.26;margin:3px 0 0}
.cv-links{display:inline;font-size:14px}
.cv-links a{color:var(--accent);font-weight:700;text-decoration:none}
.cv-skills{display:grid;grid-template-columns:125px minmax(0,1fr);align-items:start;
column-gap:0;row-gap:0}
.cv-skills>div{padding:4.5px 0;border-bottom:1px solid var(--hair)}
.cv-skills>div:nth-last-child(-n+2){border-bottom:none}
.cv-skill-label{font:800 12px/1.35 var(--sans);letter-spacing:.05em;text-transform:uppercase;
color:var(--accent)}
/* Every editable line is a document line: click and type, no widgets. */
.eq{display:inline;font-size:14px;line-height:1.26;outline:none;border-radius:3px;
padding:1px 2px;margin:0 -2px;box-decoration-break:clone;-webkit-box-decoration-break:clone;
transition:background .12s}
.eq.lead{font-weight:700}
.eq:hover{background:#14324f0f}
.eq:focus{background:#14324f14;box-shadow:0 0 0 2px #14324f2e}
.eq.is-accepted{background:#27bd7924}
.eq.is-manual{background:#d99a2b26}
.cv-skills .eq{font-size:13.8px}
/* An AI proposal sits under the line it would change, inside the paper. */
.inline-ai{margin:7px 0 11px;border-left:3px solid var(--accent);background:#14324f0d;
border-radius:0 6px 6px 0;padding:9px 12px;font-family:var(--sans)}
.inline-ai .label{color:var(--accent)}
.inline-ai .prop{font:14px/1.3 var(--serif);color:var(--ink);margin:5px 0;outline:none;
border:1px solid #14324f26;border-radius:5px;padding:5px 7px;background:#fff;white-space:pre-wrap}
.inline-ai .why{font-size:11.5px;color:#4a5a68;line-height:1.45;margin-bottom:7px}
.inline-ai .row{display:flex;gap:6px;flex-wrap:wrap}
.inline-ai .mini.no{color:#4a5a68;border-color:#14324f33}
.mini{min-height:28px;padding:0 10px;font-size:11px;font-weight:800;border-radius:7px}
.mini.ok{background:var(--green2);color:#03130c;border-color:var(--green2)}
.mini.no{background:transparent;color:var(--muted)}
.entry-tools{display:flex;gap:4px;align-items:center;opacity:0;transition:opacity .12s}
.cv-entry:hover .entry-tools,.cv-section:hover .entry-tools{opacity:1}
.entry-tools button{min-height:20px;padding:0 6px;font-size:10px;font-weight:800;border-radius:5px;
border:1px solid #14324f33;background:#14324f0d;color:var(--accent);cursor:pointer}
.entry-tools button:hover{background:#14324f1f}
.entry-tools button.drop{color:#9c3a33;border-color:#9c3a3333}
.cv-section-head-row{display:flex;align-items:center;justify-content:space-between;gap:10px}
.left-out{margin-top:18px;border-top:1px dashed var(--rule);padding-top:11px}
.left-out h4{font:800 11px/1.3 var(--sans);letter-spacing:.16em;text-transform:uppercase;
color:var(--meta);margin:0 0 7px}
.left-out div{display:flex;align-items:center;justify-content:space-between;gap:10px;
padding:4px 0;font-size:13px;color:#7b8792}
.left-out button{min-height:22px;padding:0 8px;font-size:10px;font-weight:800;border-radius:5px;
border:1px solid #14324f33;background:transparent;color:var(--accent);cursor:pointer}
.modes{display:flex;gap:5px;margin:9px 0 4px}
.modes button{flex:1;min-height:32px;padding:0 6px;font-size:11px;font-weight:800;border-radius:8px;
background:#0b1712;color:var(--muted);border:1px solid var(--line)}
.modes button.on{border-color:var(--green2);color:var(--green);background:#12291f}
.mode-note{font-size:11px;color:var(--muted);margin:2px 0 0;min-height:30px}
.variants{display:flex;gap:4px;align-items:center;margin:5px 0 2px}
.variants b{font:800 10px/1 var(--sans);letter-spacing:.08em;text-transform:uppercase;
color:#4a5a68;margin-right:2px}
.variants button{min-height:22px;min-width:22px;padding:0 7px;font-size:11px;font-weight:800;
border-radius:5px;border:1px solid #14324f33;background:#fff;color:var(--accent);cursor:pointer}
.variants button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.inline-ai.added{border-left-color:#1f7a4d;background:#1f7a4d0f}
.inline-ai.added .label{color:#1f7a4d}
.line-x{font:700 10px/1 var(--sans);color:#9c3a33;border:1px solid transparent;background:none;
cursor:pointer;padding:0 3px;vertical-align:super;opacity:0;transition:opacity .12s}
.cv-para:hover .line-x{opacity:.75}
.line-x:hover{opacity:1;border-color:#9c3a3340;border-radius:4px}
.tabs{display:flex;gap:4px}
.tabs button{min-height:30px;padding:0 12px;font-size:12px;font-weight:800;border-radius:8px;
background:transparent;color:var(--muted);border:1px solid var(--line)}
.tabs button.on{border-color:var(--green2);color:var(--green);background:#12291f}
.qa{background:#fff;color:var(--ink);font-family:var(--serif);width:100%;max-width:840px;
margin:0 auto;padding:34px 38px 44px;border-radius:4px;box-shadow:0 24px 70px #000a}
.qa h3{font:800 13px/1.3 var(--sans);letter-spacing:.2em;text-transform:uppercase;
color:var(--accent);margin:0 0 4px}
.qa .rule{height:1.4px;background:var(--rule);margin:7px 0 14px}
.qa .q{font-weight:700;font-size:14.5px;margin:16px 0 3px}
.qa .limit{font:600 11px/1.4 var(--sans);color:var(--meta);margin-bottom:5px}
.qa .a{font-size:14px;line-height:1.4;white-space:pre-wrap;outline:none;border:1px solid #14324f26;
border-radius:6px;padding:9px 11px;min-height:64px;background:#fdfdfd}
.qa .a:focus{border-color:#14324f66;box-shadow:0 0 0 3px #14324f14}
.qa .count{font:600 11px/1.4 var(--sans);color:var(--meta);margin-top:4px;display:flex;
justify-content:space-between;gap:10px}
.qa .count.over{color:#9c3a33}
.qa .copy{min-height:24px;padding:0 9px;font:800 10px/1 var(--sans);border-radius:5px;
border:1px solid #14324f33;background:#fff;color:var(--accent);cursor:pointer}
.qa .empty{font:14px/1.5 var(--sans);color:var(--meta);text-align:center;padding:26px 10px}
.warn{border:1px solid #66552b;background:#2b2414;padding:10px 12px;border-radius:10px;
color:#ffe1a1;font-size:12px;margin-bottom:10px}
.kw{display:flex;flex-wrap:wrap;gap:5px}
.kw span{border-radius:99px;padding:3px 8px;font-size:11px;border:1px solid var(--line);
color:var(--muted)}
.kw span.missing{border-color:#6f3430;color:var(--red);background:#2a1715}
.kw span.covered{border-color:#2a7455;color:var(--green);background:#0f2318}
.kw span.high{font-weight:800}
.score{display:flex;align-items:baseline;gap:8px;margin:2px 0 10px}
.score b{font-size:26px;letter-spacing:-.03em}
.doc-toolbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.cv-picker select{background:#0b1712;color:var(--text);border:1px solid var(--line);
border-radius:9px;min-height:34px;padding:0 8px;max-width:200px}
.page-meta{max-width:840px;margin:0 auto 10px;display:flex;justify-content:space-between;
color:var(--muted);font-size:11px}
.gap-row{display:flex;align-items:baseline;gap:7px;padding:5px 0;border-bottom:1px solid #1a2e27}
.gap-row:last-child{border-bottom:none}
.gap-skill{font-size:12px;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}
.gap-badge{font-size:10px;padding:2px 7px;border-radius:99px;white-space:nowrap}
.gap-missing{background:#2a1715;color:var(--red);border:1px solid #6f3430}
.gap-partial{background:#2b2414;color:var(--amber);border:1px solid #66552b}
.gap-covered{background:#0f2318;color:var(--green);border:1px solid #2a7455}
.cv-row{display:flex;align-items:center;gap:6px;padding:6px 0;border-bottom:1px solid #1a2e27}
.cv-row:last-child{border-bottom:none}
.cv-row .name{flex:1;min-width:0;font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cv-row .file{display:block;font-size:10px;color:var(--muted);overflow:hidden;text-overflow:ellipsis}
.export-section{display:flex;flex-direction:column;gap:10px}
textarea.instruction{width:100%;border:1px solid var(--line);background:#07100d;
color:var(--text);padding:10px;border-radius:10px;min-height:80px;resize:vertical;font-size:13px}
input.key{width:100%;border:1px solid var(--line);background:#07100d;
color:var(--text);padding:10px;border-radius:10px;font-size:13px}
.hint{font-size:11px;color:var(--muted);margin:5px 0}
.stats{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.pill{border:1px solid var(--line);border-radius:99px;padding:3px 8px;color:var(--muted);font-size:11px}
.pill.ok{border-color:#2a7455;color:var(--green)}
.busy{display:none;align-items:center;gap:8px;color:var(--green);padding:6px 0}
.busy.show{display:flex}
.spinner{width:14px;height:14px;border:2px solid #35604f;border-top-color:var(--green);
border-radius:50%;animation:spin .75s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
#toast{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);background:#172c25;
border:1px solid var(--line);padding:10px 15px;border-radius:9px;display:none;z-index:20;
font-size:13px;max-width:420px;text-align:center}
.empty-state{text-align:center;padding:34px 16px;color:var(--muted);border:1px dashed var(--line);
border-radius:13px;font-size:13px}
.req-list,.advice-list{list-style:none;padding:0;margin:0}
.req-list li,.advice-list li{padding:6px 0;border-bottom:1px solid #1a2e27;font-size:12px;color:var(--muted)}
.req-list li:last-child,.advice-list li:last-child{border-bottom:none}
.req-list li::before{content:"◆ ";color:var(--blue)}
.reject-list{list-style:none;padding:0;margin:0}
.reject-list li{padding:6px 0;border-bottom:1px solid #1a2e27;font-size:12px;color:var(--muted)}
.reject-list li:last-child{border-bottom:none}
.reject-list li::before{content:"⊘ ";color:var(--amber)}
.advice-list li::before{content:"💡 "}
@media(max-width:1180px){.layout{grid-template-columns:290px minmax(0,1fr) 270px}
  .cv-paper{padding:38px 34px 46px}}
@media(max-width:900px){.layout{grid-template-columns:1fr;height:auto;overflow:visible}
  .pane{height:auto;overflow-y:visible}.pane-left,.pane-right{border:none;border-top:1px solid var(--line)}}
</style></head>
<body><div class="shell">
<header>
  <div class="brand"><b>CV</b> Studio</div>
  <div class="job"><strong id="jobTitle">Loading…</strong><span id="jobMeta">Private localhost editor</span></div>
  <span class="fit-pill" id="fitPill" style="display:none"></span>
  <a class="button ghost" href="https://abyyworld.github.io/internship-tracker/" style="white-space:nowrap">Dashboard</a>
  <a class="button primary" id="applyTop" target="_blank" rel="noopener" style="white-space:nowrap">Open application</a>
</header>
<div class="layout">

<!-- LEFT: what the posting asks for, and the AI patches answering it -->
<aside class="pane pane-left">
  <div class="pane-header">
    <div>
      <div class="eyebrow">Job match</div>
      <div style="font-weight:800;font-size:15px">Suggested edits</div>
    </div>
    <div class="stats"><span class="pill" id="factCount">— facts</span>
    <span class="pill ok" id="acceptedCount" style="display:none"></span></div>
  </div>
  <div class="pane-body">
    <div id="notice"></div>
    <div id="reqSection" style="display:none">
      <div class="eyebrow blue">Requirements read from this posting</div>
      <ul class="req-list" id="reqList"></ul>
    </div>
    <div id="suggestions">
      <div class="empty-state">Open a job, then press <strong>Generate</strong> on the right.<br><br>
      The model reads the posting's requirements first, then rewrites only the
      lines your CV already has evidence for.</div>
    </div>
    <div id="adviceSection" style="display:none">
      <h3 style="margin-top:16px">Gaps &amp; application advice</h3>
      <ul class="advice-list" id="adviceList"></ul>
    </div>
    <div id="rejectSection" style="display:none">
      <h3 style="margin-top:16px">Lines the model was not allowed to change</h3>
      <ul class="reject-list" id="rejectList"></ul>
    </div>
  </div>
</aside>

<!-- MIDDLE: the CV itself, laid out exactly as it prints -->
<main class="pane">
  <div class="pane-header">
    <div class="doc-toolbar cv-picker">
      <div class="tabs" id="tabs">
        <button data-tab="cv" class="on">CV</button>
        <button data-tab="answers">Answers</button>
      </div>
      <select id="cvSelect" title="Choose which saved CV to edit"></select>
      <span class="muted" id="savedFlag" style="font-size:11px">Saved</span>
    </div>
    <div style="display:flex;gap:6px">
      <button class="secondary mini" id="acceptAll" disabled>Accept all AI</button>
      <button class="secondary mini" id="resetAll" disabled>Revert all</button>
    </div>
  </div>
  <div class="pane-body pane-doc">
    <div class="page-meta">
      <span>Click any line and type — this is exactly how the PDF prints.</span>
      <span id="docMeta"></span>
    </div>
    <div id="cvDoc"><div class="empty-state">Loading CV…</div></div>
    <div id="answersDoc" style="display:none"></div>
  </div>
</main>

<!-- RIGHT: controls, saved CVs, gaps, export -->
<aside class="pane pane-right">
  <div class="pane-header">
    <div class="eyebrow">Controls</div>
  </div>
  <div class="pane-body">

    <div class="card">
      <div class="eyebrow">Instructions</div>
      <textarea class="instruction" id="instructions" maxlength="4000"
        placeholder="Optional: e.g. Lead with the robot-learning infrastructure work. Keep my academic tone."></textarea>
      <p class="hint" id="sendNote">Sends this posting and your CV to the provider below through your own key — never via GitHub.</p>
      <div class="modes">
        <button data-mode="targeted">Touch up</button>
        <button data-mode="full" class="on">Full rewrite</button>
        <button data-mode="aggressive">Go hard</button>
      </div>
      <p class="mode-note" id="modeNote"></p>
      <div style="display:flex;gap:8px;margin-top:6px;flex-wrap:wrap">
        <button class="primary" id="generate">Rewrite for this job</button>
      </div>
      <div class="busy" id="busy"><span class="spinner"></span><span id="busyText">Reading the posting…</span></div>
    </div>

    <div class="card">
      <div class="eyebrow">Saved CVs</div>
      <div id="cvList"></div>
      <div style="display:flex;gap:6px;margin-top:9px">
        <input class="key" id="newCvName" placeholder="Name this CV…" maxlength="80" style="flex:1">
        <button class="secondary mini" id="saveAsCv">Save</button>
      </div>
      <p class="hint">Named for this job by default — edit the name, then Save.
      Each CV is one private file in <code id="cvStorage">private/Saved CVs/</code></p>
    </div>

    <div class="card" id="answerCard">
      <div class="eyebrow blue">Application answers</div>
      <p class="hint" style="margin-top:4px">Finds the essay prompts and open-ended
      questions in the posting and drafts each one from your CV.</p>
      <label class="toggle" style="margin:6px 0"><input type="checkbox" id="wantCover" checked> Cover letter</label>
      <label class="toggle" style="margin-bottom:8px"><input type="checkbox" id="wantOutreach"> Recruiter note</label>
      <input class="key" id="ownQuestion" placeholder="Add your own question…" maxlength="500">
      <button class="secondary" id="writeAnswers" style="width:100%;margin-top:8px">Draft answers</button>
      <div class="busy" id="answerBusy"><span class="spinner"></span><span>Reading the posting…</span></div>
    </div>

    <div class="card" id="keywordCard" style="display:none">
      <div class="eyebrow purple">Keyword match</div>
      <div class="score" id="scoreBox" style="display:none"><b id="scoreValue">—</b>
        <span class="muted" style="font-size:11px">evidence match, judged against this posting</span></div>
      <p class="muted" style="font-size:12px;margin-bottom:8px" id="keywordNote"></p>
      <div class="kw" id="keywordList"></div>
    </div>

    <div class="card" id="gapCard" style="display:none">
      <div class="eyebrow purple">Technologies in the posting</div>
      <p class="muted" style="font-size:12px;margin-bottom:8px">Detected in the advert, against your current draft:</p>
      <div id="gapList"></div>
    </div>

    <div class="card">
      <div class="eyebrow">Export</div>
      <div class="export-section">
        <p class="muted" style="font-size:12px" id="exportNote">Accepted edits are applied. Everything else stays original.</p>
        <button class="primary" id="exportPdf">Download tailored PDF</button>
        <p class="hint" id="exportName"></p>
        <a class="button secondary" id="applySide" target="_blank" rel="noopener">Apply with Simplify</a>
      </div>
    </div>

    <div class="card" id="providerCard">
      <div class="eyebrow">Provider</div>
      <p class="hint" style="margin-top:4px">Anything speaking the OpenAI API
      works — including a model running on this Mac, which costs nothing and
      never leaves the machine.</p>
      <select id="providerSelect" class="key" style="margin-top:6px"></select>
      <p class="hint" id="providerNote"></p>
      <details id="customEndpoint" style="margin-top:6px">
        <summary class="hint" style="cursor:pointer">Use my own endpoint</summary>
        <p class="hint" style="margin-top:6px">Any OpenAI-compatible base URL —
        LM Studio, llama.cpp, a company proxy. HTTPS, or a local address.</p>
        <input class="key" id="customBase" autocomplete="off" spellcheck="false"
          placeholder="https://… or http://127.0.0.1:1234/v1" style="margin:6px 0">
        <button class="secondary" id="saveCustomBase" style="width:100%">Use this endpoint</button>
      </details>
      <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
        <button class="secondary" id="testProvider" style="flex:1">Test this provider</button>
      </div>
      <p class="hint" id="testNote"></p>
      <pre id="testReport" style="display:none;white-space:pre-wrap;word-break:break-word;
        margin:8px 0 0;padding:9px 10px;border-radius:9px;background:#0c1714;
        border:1px solid var(--line);font-size:11.5px;line-height:1.45;max-height:230px;overflow:auto"></pre>
    </div>

    <div class="card" id="modelCard">
      <div class="eyebrow">Model</div>
      <p class="hint" style="margin-top:4px">Default is the best value measured
      on your CV. Larger models rewrite one or two more lines for roughly
      double the wait and cost — worth it for a job you really want.</p>
      <select id="modelSelect" class="key" style="margin-top:6px"></select>
      <p class="hint" id="modelNote"></p>
    </div>

    <div class="card" id="keyCard">
      <div class="eyebrow" id="keyTitle">API key</div>
      <p class="muted" style="font-size:12px" id="keyStatus">Checking…</p>
      <input class="key" id="keyInput" type="password" autocomplete="off" style="margin:8px 0">
      <button class="secondary" id="saveKey" style="width:100%">Save key locally</button>
      <p class="hint" id="keyHint"></p>
    </div>

    <div class="card" id="helperCard">
      <div class="eyebrow">This helper</div>
      <p class="hint" id="buildNote" style="margin-top:4px"></p>
      <button class="secondary" id="updateHelper" style="width:100%;margin-top:8px">Check for an update</button>
      <p class="hint" id="updateNote"></p>
    </div>

  </div>
</aside>

</div></div>
<div id="toast"></div>
<script>
const token=localStorage.getItem("autoapply_bridge_token_v1")||"";
const params=new URLSearchParams(location.search);
const jobUrl=params.get("url")||"";
let state=null;
let cvId=params.get("cv")||"master";
let nameTouched=false;
let mode="full";
const MODE_NOTES={
  targeted:"A few wording patches on the lines that already answer this posting. Nothing moves.",
  full:"Rewrites every line for this posting, rewrites the summary, and reorders sections and entries so the most relevant work reads first.",
  aggressive:"Full rewrite, plus entries with nothing to say about this posting are left out of this job's CV. You can put any of them back."};
const $=id=>document.getElementById(id);
function toast(msg){$("toast").textContent=msg;$("toast").style.display="block";setTimeout(()=>$("toast").style.display="none",2800)}
function notice(msg,type=""){const box=$("notice");box.replaceChildren();if(!msg)return;
  const d=document.createElement("div");d.className="notice "+type;d.textContent=msg;box.append(d)}
async function api(path,options={}){
  const r=await fetch(path,{...options,headers:{"Content-Type":"application/json","X-Autoapply-Token":token,...(options.headers||{})}});
  const result=await r.json();if(!r.ok)throw new Error(result.error||`Bridge returned ${r.status}`);return result
}
// Mirrors cv_editor.ordered_sections: the draft decides the running order and
// what this job's CV leaves out; anything it does not mention keeps its master
// position and stays visible, so a partial order can never hide work silently.
function draftOrder(){
  state.draft=state.draft||{};
  state.draft.order=state.draft.order||{sections:[],entries:{}};
  state.draft.hidden=state.draft.hidden||[];
  return state.draft;
}
function orderedSections(){
  const d=draftOrder(),hidden=new Set(d.hidden);
  const rank=(ids,id,fallback)=>{const i=ids.indexOf(id);return i<0?[ids.length,fallback]:[i,0]};
  const all=state.document.sections||[];
  const secIds=d.order.sections||[];
  const sections=all.map((sec,i)=>({sec,key:rank(secIds,sec.id,i)}))
    .sort((a,b)=>a.key[0]-b.key[0]||a.key[1]-b.key[1]).map(x=>x.sec);
  const removed=new Set(d.removed||[]);
  const added=d.added||{};
  const out=[];
  for(const sec of sections){
    const wanted=(d.order.entries||{})[sec.id]||[];
    const kept=(sec.entries||[]).map((e,i)=>({e,key:rank(wanted,e.id,i)}))
      .filter(x=>!hidden.has(x.e.id))
      .sort((a,b)=>a.key[0]-b.key[0]||a.key[1]-b.key[1]).map(x=>x.e);
    const resolved=[];
    for(const e of kept){
      const bullets=(e.bullets||[]).filter(b=>!removed.has(b.id))
        .concat((added[e.id]||[]).filter(l=>l.status==="accepted"&&(l.text||"").trim())
          .map(l=>({id:l.id,text:l.text})));
      if(bullets.length)resolved.push({...e,bullets});
    }
    if(resolved.length)out.push({...sec,entries:resolved});
  }
  return out;
}
function draftLines(){
  const d=draftOrder();
  d.added=d.added||{};d.removed=d.removed||[];
  return d;
}
function setLineRemoved(factId,gone){
  const d=draftLines();
  const set=new Set(d.removed);
  gone?set.add(factId):set.delete(factId);
  d.removed=[...set];renderAll();queueSave();
}
function addedFor(entryId){return (draftLines().added||{})[entryId]||[]}
function addLine(entryId){
  const d=draftLines();
  const lines=(d.added[entryId]||[]).slice();
  if(lines.length>=3){toast("Three added lines per entry is the limit");return}
  lines.push({id:`${entryId}-new${lines.length}`,text:"New line — click to edit.",
    rationale:"Added by you",status:"accepted",source:"manual"});
  d.added={...d.added,[entryId]:lines};
  renderAll();queueSave();
  // Put the caret straight into the line that was just created.
  const el=document.querySelector(`[data-id="${lines[lines.length-1].id}"]`);
  if(el){el.focus();document.getSelection().selectAllChildren(el)}
}
function editAddedLine(entryId,lineId,text){
  const d=draftLines();
  const lines=(d.added[entryId]||[]).map(l=>l.id===lineId?{...l,text}:l)
    .filter(l=>(l.text||"").trim());
  d.added={...d.added,[entryId]:lines};
}
function findAddedLine(lineId){
  const d=draftLines();
  for(const [entryId,lines] of Object.entries(d.added||{}))
    for(const line of lines)if(line.id===lineId)return{entryId,line};
  return null;
}
function hiddenEntries(){
  const hidden=new Set(draftOrder().hidden);
  const out=[];
  for(const sec of state.document.sections||[])
    for(const e of sec.entries||[])
      if(hidden.has(e.id))out.push({section:sec.name,entry:e});
  return out;
}
function moveSection(id,delta){
  const d=draftOrder();
  const ids=orderedSections().map(s=>s.id);
  const from=ids.indexOf(id),to=from+delta;
  if(from<0||to<0||to>=ids.length)return;
  ids.splice(to,0,ids.splice(from,1)[0]);
  d.order.sections=ids;renderAll();queueSave();
}
function moveEntry(sectionId,entryId,delta){
  const d=draftOrder();
  const sec=orderedSections().find(s=>s.id===sectionId);
  if(!sec)return;
  const ids=sec.entries.map(e=>e.id);
  const from=ids.indexOf(entryId),to=from+delta;
  if(from<0||to<0||to>=ids.length)return;
  ids.splice(to,0,ids.splice(from,1)[0]);
  d.order.entries={...d.order.entries,[sectionId]:ids};
  renderAll();queueSave();
}
function setHidden(entryId,hide){
  const d=draftOrder();
  const set=new Set(d.hidden);
  hide?set.add(entryId):set.delete(entryId);
  d.hidden=[...set];renderAll();queueSave();
}
function allBullets(){
  const out=[];
  for(const sec of (state&&state.document.sections)||[])
    for(const ent of sec.entries||[])
      for(const b of ent.bullets||[])out.push(b);
  return out;
}

// ── Fit score ────────────────────────────────────────────────────────────────
function cvText(){
  const draftBullets=((state||{}).draft||{}).bullets||{};
  return allBullets().map(b=>{
    const patch=draftBullets[b.id];
    return patch&&patch.status==="accepted"?patch.proposal:b.text;
  }).join(" ").toLowerCase();
}
function computeFit(){
  if(!state)return null;
  const desc=((state.job&&state.job.raw_description)||"").toLowerCase();
  if(!desc)return null;
  const words=cvText();
  const jobWords=desc.match(/\b[a-z][a-z0-9\+\#\.]{2,}\b/g)||[];
  const stop=["with","from","that","this","will","have","your","their","they","into","been","each","when","than","such","also","must","able","more","some","most","only","very","both","well","over","just","even","then","much","need","make","about","using","these","other","which","after","where"];
  const unique=[...new Set(jobWords)].filter(w=>w.length>3&&!stop.includes(w));
  if(!unique.length)return null;
  return Math.round((unique.filter(w=>words.includes(w)).length/unique.length)*100);
}
function renderFitPill(){
  const score=computeFit(),pill=$("fitPill");
  if(score===null){pill.style.display="none";return}
  pill.style.display="";pill.textContent=`Fit: ${score}%`;
  pill.className="fit-pill "+(score>=70?"good":score>=45?"medium":"low");
}

// ── Gap analysis ─────────────────────────────────────────────────────────────
const TECH=[
  /\b(python|java|javascript|typescript|c\+\+|c#|rust|go|golang|swift|kotlin|ruby|scala|matlab|julia)\b/gi,
  /\b(pytorch|tensorflow|keras|sklearn|numpy|pandas|jax|huggingface|transformers)\b/gi,
  /\b(react|vue|angular|node\.?js|express|django|flask|fastapi|spring|unity|unreal)\b/gi,
  /\b(aws|gcp|azure|kubernetes|docker|terraform|kafka|spark|flink)\b/gi,
  /\b(machine learning|deep learning|computer vision|nlp|llm|reinforcement learning|imitation learning)\b/gi,
  /\b(sql|postgresql|mysql|mongodb|redis|cassandra|elasticsearch)\b/gi,
  /\b(git|ci\/cd|devops|agile|rest api|grpc|graphql)\b/gi,
  /\b(ros|slam|perception|autonomy|control systems|mechatronics|teleoperation)\b/gi,
  /\b(fpga|vhdl|verilog|embedded|firmware|rtos)\b/gi,
  /\b(hci|user study|eye tracking|vr|ar|xr|quest|openxr)\b/gi,
  /\b(linux|unix|bash|shell)\b/gi];
function computeGaps(){
  if(!state)return[];
  const desc=((state.job&&state.job.raw_description)||"").toLowerCase();
  if(!desc)return[];
  const lower=cvText();
  const found=new Set();
  for(const pat of TECH)for(const m of desc.matchAll(pat))found.add(m[0].toLowerCase().trim());
  const gaps=[...found].map(kw=>{
    if(lower.includes(kw))return{kw,status:"covered"};
    const partial=kw.split(/\s+/).some(part=>part.length>3&&lower.includes(part));
    return{kw,status:partial?"partial":"missing"};
  });
  const rank={missing:0,partial:1,covered:2};
  gaps.sort((a,b)=>rank[a.status]-rank[b.status]||a.kw.localeCompare(b.kw));
  return gaps.slice(0,24);
}
function renderGaps(){
  const gaps=computeGaps(),card=$("gapCard"),list=$("gapList");
  if(!gaps.length){card.style.display="none";return}
  card.style.display="";list.replaceChildren();
  for(const g of gaps){
    const row=document.createElement("div");row.className="gap-row";
    const skill=document.createElement("span");skill.className="gap-skill";skill.textContent=g.kw;
    const badge=document.createElement("span");badge.className="gap-badge gap-"+g.status;
    badge.textContent=g.status==="covered"?"✓ covered":g.status==="partial"?"~ partial":"✗ missing";
    row.append(skill,badge);list.append(row);
  }
}

// ── The paper ────────────────────────────────────────────────────────────────
function patchFor(id){return id==="summary"?(state.draft||{}).summary:((state.draft||{}).bullets||{})[id]}
function currentText(id,original){
  const p=patchFor(id);
  if(p&&(p.status==="accepted"||p.source==="manual"))return p.proposal;
  return original;
}
function setManualText(id,original,text){
  const clean=(text||"").replace(/\s+/g," ").trim();
  state.draft=state.draft||{};
  if(!clean||clean===original.replace(/\s+/g," ").trim()){
    // Back to the verified original — drop the patch rather than store a no-op.
    if(id==="summary")delete state.draft.summary;
    else if(state.draft.bullets)delete state.draft.bullets[id];
    return;
  }
  const patch={id,original,proposal:clean,rationale:"Edited by you",
    keywords:[],status:"accepted",source:"manual"};
  if(id==="summary")state.draft.summary=patch;
  else{state.draft.bullets=state.draft.bullets||{};state.draft.bullets[id]=patch}
}
// A span, not a block: the printed CV runs the bold opening claim straight into
// the body paragraph, and the editor has to break the line in the same places.
function editableLine(id,original,extraClass){
  const el=document.createElement("span");
  el.className="eq "+(extraClass||"");
  el.contentEditable="true";el.spellcheck=false;el.dataset.id=id;
  el.textContent=currentText(id,original);
  const p=patchFor(id);
  if(p&&p.status==="accepted")el.classList.add(p.source==="manual"?"is-manual":"is-accepted");
  el.addEventListener("blur",()=>{
    const owned=findAddedLine(id);
    if(owned){
      const text=(el.innerText||"").replace(/\s+/g," ").trim();
      if(text!==owned.line.text){
        editAddedLine(owned.entryId,id,text);renderAll();queueSave();
      }
      return;
    }
    const before=JSON.stringify(patchFor(id)||null);
    setManualText(id,original,el.innerText);
    if(JSON.stringify(patchFor(id)||null)!==before){renderAll();queueSave()}
  });
  el.addEventListener("keydown",ev=>{
    // One line here is one paragraph in print, so Enter commits rather than
    // splitting the element into markup the exporter would have to guess at.
    if(ev.key==="Enter"){ev.preventDefault();el.blur()}
    if(ev.key==="Escape"){el.textContent=currentText(id,original);el.blur()}
  });
  return el;
}
function pendingAiFor(id){
  const p=patchFor(id);
  return p&&p.source!=="manual"&&p.status==="pending"?p:null;
}
function inlineAiStrip(id){
  const p=pendingAiFor(id);
  if(!p)return null;
  const box=document.createElement("div");box.className="inline-ai";
  const lbl=document.createElement("div");lbl.className="label";lbl.textContent="AI suggests";
  box.append(lbl);
  const prop=document.createElement("div");prop.className="prop";prop.contentEditable="true";
  prop.spellcheck=false;prop.textContent=p.proposal;
  prop.addEventListener("blur",()=>{p.proposal=(prop.innerText||"").replace(/\s+/g," ").trim()||p.proposal});
  box.append(prop);
  // Alternative phrasings of the same line, so the choice is between real
  // options rather than take-it-or-leave-it.
  const opts=(p.variants||[]).filter(Boolean);
  if(opts.length>1){
    const row=document.createElement("div");row.className="variants";
    const cap=document.createElement("b");cap.textContent="Options";row.append(cap);
    opts.forEach((text,i)=>{
      const b=document.createElement("button");b.textContent=String(i+1);
      b.title=text.slice(0,160);
      if(text===p.proposal)b.classList.add("on");
      b.onclick=()=>{p.proposal=text;renderAll();queueSave()};
      row.append(b);
    });
    box.append(row);
  }
  if(p.rationale){const w=document.createElement("div");w.className="why";w.textContent=p.rationale;box.append(w)}
  // Counted rather than claimed: the posting vocabulary this rewrite actually
  // brings in. A rewrite that gains none is a rephrasing, and saying so lets
  // the reader skip it instead of reading two near-identical lines.
  const gained=(p.adds_keywords||[]).filter(Boolean);
  const gain=document.createElement("div");gain.className="why";
  gain.style.color=gained.length?"var(--green)":"var(--muted)";
  gain.textContent=gained.length
    ?"Adds screening terms: "+gained.join(", ")
    :"Adds no new screening term \u2014 wording only.";
  box.append(gain);
  const row=document.createElement("div");row.className="row";
  const ok=document.createElement("button");ok.className="mini ok";ok.textContent="Use this";
  ok.onclick=()=>{p.status="accepted";renderAll();queueSave()};
  const no=document.createElement("button");no.className="mini no";no.textContent="Dismiss";
  no.onclick=()=>{p.status="rejected";renderAll();queueSave()};
  row.append(ok,no);box.append(row);
  return box;
}
// A line the model proposes adding to an entry, drawn from that entry's own
// verified text. Accepting it prints it; it never touches the fact bank.
function addedStrips(entryId){
  const out=[];
  for(const line of addedFor(entryId)){
    if(line.status!=="pending")continue;
    const box=document.createElement("div");box.className="inline-ai added";
    const lbl=document.createElement("div");lbl.className="label";lbl.textContent="AI would add a line";
    box.append(lbl);
    const prop=document.createElement("div");prop.className="prop";prop.contentEditable="true";
    prop.spellcheck=false;prop.textContent=line.text;
    prop.addEventListener("blur",()=>{line.text=(prop.innerText||"").replace(/\s+/g," ").trim()||line.text});
    box.append(prop);
    if(line.rationale){const w=document.createElement("div");w.className="why";
      w.textContent=line.rationale;box.append(w)}
    const lg=(line.adds_keywords||[]).filter(Boolean);
    if(lg.length){const g=document.createElement("div");g.className="why";
      g.style.color="var(--green)";
      g.textContent="Adds screening terms: "+lg.join(", ");box.append(g)}
    const row=document.createElement("div");row.className="row";
    const ok=document.createElement("button");ok.className="mini ok";ok.textContent="Add this";
    ok.onclick=()=>{line.status="accepted";renderAll();queueSave()};
    const no=document.createElement("button");no.className="mini no";no.textContent="Dismiss";
    no.onclick=()=>{line.status="rejected";renderAll();queueSave()};
    row.append(ok,no);box.append(row);
    out.push(box);
  }
  return out;
}
function entryLinks(entry){
  const links=[];
  if(entry.link_extra_url)links.push([entry.link_extra_url,entry.link_extra_text||"Link"]);
  if(entry.url)links.push([entry.url,entry.link_text||"GitHub"]);
  if(!links.length)return null;
  const box=document.createElement("div");box.className="cv-links";
  if(entry.link_prefix)box.append(document.createTextNode(entry.link_prefix));
  links.forEach(([href,text],i)=>{
    if(i)box.append(document.createTextNode(" · "));
    const a=document.createElement("a");a.href=href;a.target="_blank";a.rel="noopener";
    a.textContent=text;box.append(a);
  });
  return box;
}
function toolButton(label,title,onclick,cls){
  const b=document.createElement("button");b.textContent=label;b.title=title;
  if(cls)b.className=cls;b.onclick=onclick;b.tabIndex=-1;return b;
}
function sectionShell(name,sectionId){
  const wrap=document.createElement("div");wrap.className="cv-section";
  const row=document.createElement("div");row.className="cv-section-head-row";
  const head=document.createElement("div");head.className="cv-section-head";head.textContent=name;
  const tools=document.createElement("div");tools.className="entry-tools";
  tools.append(
    toolButton("↑","Move this section up",()=>moveSection(sectionId,-1)),
    toolButton("↓","Move this section down",()=>moveSection(sectionId,1)));
  row.append(head,tools);
  const rule=document.createElement("div");rule.className="cv-section-rule";
  wrap.append(row,rule);
  return wrap;
}
function renderCV(){
  const doc=state.document,root=$("cvDoc");root.replaceChildren();
  const paper=document.createElement("div");paper.className="cv-paper";
  const head=doc.header||{};

  if(head.name){const n=document.createElement("div");n.className="cv-name";n.textContent=head.name;paper.append(n)}
  if(head.tagline){const t=document.createElement("div");t.className="cv-tagline";t.textContent=head.tagline;paper.append(t)}
  const contact=(head.contact_line||[]).filter(Boolean).join("  |  ");
  if(contact){const c=document.createElement("div");c.className="cv-contact";c.textContent=contact;paper.append(c)}
  const rule=document.createElement("div");rule.className="cv-rule-strong";paper.append(rule);

  if(doc.summary){
    const wrap=document.createElement("div");wrap.className="cv-summary";
    wrap.append(editableLine("summary",doc.summary));
    const strip=inlineAiStrip("summary");if(strip)wrap.append(strip);
    paper.append(wrap);
  }

  for(const sec of orderedSections()){
    const layout=sec.layout||"entries";
    const wrap=sectionShell(sec.name,sec.id);

    if(layout==="skills"){
      const grid=document.createElement("div");grid.className="cv-skills";
      for(const entry of sec.entries||[]){
        const label=document.createElement("div");label.className="cv-skill-label";
        label.textContent=entry.title||"";
        const value=document.createElement("div");
        for(const b of entry.bullets||[]){
          value.append(editableLine(b.id,b.text));
          const strip=inlineAiStrip(b.id);if(strip)value.append(strip);
        }
        grid.append(label,value);
      }
      wrap.append(grid);paper.append(wrap);continue;
    }

    for(const entry of sec.entries||[]){
      const block=document.createElement("div");block.className="cv-entry";
      if(layout!=="notes"&&(entry.title||entry.dates)){
        const hd=document.createElement("div");hd.className="cv-entry-head";
        const title=document.createElement("div");title.className="cv-entry-title";
        title.textContent=entry.title||"";
        const right=document.createElement("div");
        right.style.cssText="display:flex;align-items:baseline;gap:8px";
        const tools=document.createElement("div");tools.className="entry-tools";
        tools.append(
          toolButton("+ line","Write a new line for this entry",
            ()=>addLine(entry.id)),
          toolButton("↑","Move up",()=>moveEntry(sec.id,entry.id,-1)),
          toolButton("↓","Move down",()=>moveEntry(sec.id,entry.id,1)),
          toolButton("✕","Leave this entry out of this job's CV",
            ()=>setHidden(entry.id,true),"drop"));
        const dates=document.createElement("div");dates.className="cv-entry-dates";
        dates.textContent=entry.dates||"";
        right.append(tools,dates);
        hd.append(title,right);block.append(hd);
      }
      if(layout!=="notes"&&entry.organization){
        const sub=document.createElement("div");sub.className="cv-entry-sub";
        sub.textContent=entry.organization;block.append(sub);
      }
      // Lead and body print as one paragraph, so they sit in one here too, and
      // any AI proposals follow it rather than interrupting the prose.
      const para=document.createElement("p");para.className="cv-para";
      const strips=[];
      (entry.bullets||[]).forEach((b,i)=>{
        if(i)para.append(document.createTextNode(" "));
        para.append(editableLine(b.id,b.text,b.style==="lead"?"lead":""));
        const owned=findAddedLine(b.id);
        if(owned||((entry.bullets||[]).length>1)){
          const x=document.createElement("button");x.className="line-x";x.textContent="✕";
          x.title=owned?"Delete this added line":"Leave this line out of this job's CV";
          x.tabIndex=-1;
          x.onclick=()=>{
            if(!owned){setLineRemoved(b.id,true);return}
            editAddedLine(owned.entryId,b.id,"");renderAll();queueSave();
          };
          para.append(x);
        }
        const strip=inlineAiStrip(b.id);if(strip)strips.push(strip);
      });
      const links=entryLinks(entry);
      if(links){para.append(document.createTextNode(" "));para.append(links)}
      block.append(para);
      for(const strip of strips)block.append(strip);
      for(const strip of addedStrips(entry.id))block.append(strip);
      wrap.append(block);
    }
    paper.append(wrap);
  }

  const left=hiddenEntries();
  const removed=new Set(draftLines().removed);
  const lines=[];
  for(const sec of state.document.sections||[])
    for(const e of sec.entries||[])
      for(const bl of e.bullets||[])
        if(removed.has(bl.id))lines.push({entry:e,bullet:bl});
  if(left.length||lines.length){
    const box=document.createElement("div");box.className="left-out";
    const h=document.createElement("h4");
    h.textContent=`Left out of this job's CV (${left.length+lines.length})`;box.append(h);
    for(const {section,entry} of left){
      const row=document.createElement("div");
      const label=document.createElement("span");
      label.textContent=`${entry.title||"(untitled)"} · ${section}`;
      row.append(label,toolButton("Put back","Include this entry again",
        ()=>setHidden(entry.id,false)));
      box.append(row);
    }
    for(const {entry,bullet} of lines){
      const row=document.createElement("div");
      const label=document.createElement("span");
      label.textContent=`${(bullet.text||"").slice(0,70)}… · ${entry.title||""}`;
      row.append(label,toolButton("Put back","Include this line again",
        ()=>setLineRemoved(bullet.id,false)));
      box.append(row);
    }
    paper.append(box);
  }
  root.append(paper);
}

// ── Left pane ────────────────────────────────────────────────────────────────
function allPatches(){
  const d=(state&&state.draft)||{};
  const out=[];
  if(d.summary)out.push(d.summary);
  for(const p of Object.values(d.bullets||{}))out.push(p);
  return out;
}
// Why a line was left alone. "N suggestions discarded" reads like the tool is
// broken; naming the reason shows the guard doing its job on a specific line.
const REJECT_REASONS={
  new_named_technology_or_entity:"named a technology or employer your CV never claims",
  new_numeric_claim:"invented a number",
  new_credential_claim:"awarded you a degree or title you do not hold",
  new_unsupported_qualification:"claimed a qualification your CV cannot evidence",
  length:"came back too short or too long, twice",
  insufficient_evidence_overlap:"drifted off what that line is actually about",
  borrowed_requirement_not_in_cv:"echoed a requirement your CV never mentions back as a credential",
  unknown_fact_id:"referred to a line that does not exist"};
function renderRejected(){
  const rejected=(state.draft||{}).rejected_by_validator||{};
  const box=$("rejectSection"),list=$("rejectList");
  const groups={};
  for(const reason of Object.values(rejected))groups[reason]=(groups[reason]||0)+1;
  const keys=Object.keys(groups);
  if(!keys.length){box.style.display="none";return}
  box.style.display="";list.replaceChildren();
  for(const key of keys.sort((a,b)=>groups[b]-groups[a])){
    const li=document.createElement("li");
    li.textContent=`${groups[key]} rewrite${groups[key]===1?"":"s"} kept out: `+
      (REJECT_REASONS[key]||key);
    list.append(li);
  }
}
function renderRequirements(){
  const reqs=((state.draft||{}).requirements||[]).filter(Boolean);
  const box=$("reqSection"),list=$("reqList");
  if(!reqs.length){box.style.display="none";return}
  box.style.display="";list.replaceChildren();
  for(const r of reqs){const li=document.createElement("li");li.textContent=r;list.append(li)}
}
function renderSuggestions(){
  const root=$("suggestions");root.replaceChildren();
  const patches=allPatches();
  const ai=patches.filter(p=>p.source!=="manual");
  const pending=ai.filter(p=>p.status==="pending");
  const manual=patches.filter(p=>p.source==="manual");

  if(!ai.length){
    root.innerHTML='<div class="empty-state">No AI suggestions yet.<br><br>'+
      'Edit any line in the document directly, or press <strong>Generate</strong> '+
      'to have the model rewrite the lines that answer this posting.</div>';
  }else if(!pending.length){
    root.innerHTML='<div class="empty-state">All '+ai.length+' suggestion'+(ai.length===1?"":"s")+
      ' reviewed.<br><br>Accepted edits are marked in the document.</div>';
  }else{
    const note=document.createElement("p");note.className="hint";
    note.textContent=pending.length+" of "+state.document.fact_ids.length+
      " lines rewritten for this posting. Each is shown inline in the document; "+
      "press Accept all AI to take the whole rewrite.";
    root.append(note);
    for(const p of pending){
      const card=document.createElement("article");card.className="suggestion";
      const h=document.createElement("div");h.className="suggestion-head";
      const l=document.createElement("span");l.className="label";
      l.textContent=p.id==="summary"?"Summary":"CV line";
      h.append(l);card.append(h);
      const before=document.createElement("div");before.className="rationale";
      before.textContent="Now: "+p.original;card.append(before);
      const after=document.createElement("div");after.className="rationale";
      after.style.color="var(--blue)";after.textContent="AI: "+p.proposal;card.append(after);
      if(p.rationale){const why=document.createElement("div");why.className="rationale";
        why.style.color="var(--muted)";why.textContent="Why: "+p.rationale;card.append(why)}
      const row=document.createElement("div");row.className="choice-row";
      const ok=document.createElement("button");ok.className="mini ok";ok.textContent="Use this";
      ok.onclick=()=>{p.status="accepted";renderAll();queueSave()};
      const no=document.createElement("button");no.className="mini no";no.textContent="Dismiss";
      no.onclick=()=>{p.status="rejected";renderAll();queueSave()};
      row.append(ok,no);card.append(row);
      root.append(card);
    }
  }

  const acceptedAi=ai.filter(p=>p.status==="accepted").length;
  const total=acceptedAi+manual.length;
  $("acceptAll").disabled=!pending.length;
  $("resetAll").disabled=!patches.length;
  const rewritten=ai.length;
  $("acceptedCount").textContent=rewritten
    ?`${rewritten}/${state.document.fact_ids.length} rewritten`
    :total+" edit"+(total===1?"":"s");
  $("acceptedCount").style.display=(total||rewritten)?"":"none";
  const d=state.draft||{};
  const dropped=(d.hidden||[]).length;
  const cutLines=(d.removed||[]).length;
  const moved=((d.order||{}).sections||[]).length;
  const newLines=Object.values(d.added||{})
    .reduce((n,ls)=>n+ls.filter(l=>l.status==="accepted").length,0);
  const parts=[];
  if(manual.length)parts.push(`${manual.length} of your edits`);
  if(acceptedAi)parts.push(`${acceptedAi} AI rewrite${acceptedAi===1?"":"s"}`);
  if(newLines)parts.push(`${newLines} added line${newLines===1?"":"s"}`);
  if(moved)parts.push("a reordered running order");
  if(dropped)parts.push(`${dropped} entr${dropped===1?"y":"ies"} left out`);
  if(cutLines)parts.push(`${cutLines} line${cutLines===1?"":"s"} left out`);
  $("exportNote").textContent=parts.length
    ?parts.join(", ")+" will be applied. Everything else stays original."
    :"Your CV exports unchanged until you edit a line or accept a suggestion.";

  renderRejected();

  const advice=((state.draft||{}).advice||[]).filter(Boolean);
  if(advice.length){
    $("adviceSection").style.display="";
    const ul=$("adviceList");ul.replaceChildren();
    for(const a of advice){const li=document.createElement("li");li.textContent=a;ul.append(li)}
  }else $("adviceSection").style.display="none";
}
function renderKeywords(){
  const kws=((state.draft||{}).keywords||[]).filter(k=>k&&k.term);
  const card=$("keywordCard"),list=$("keywordList");
  const score=(state.draft||{}).match_score;
  if(!kws.length&&score==null){card.style.display="none";return}
  card.style.display="";
  $("scoreBox").style.display=score==null?"none":"";
  if(score!=null){
    $("scoreValue").textContent=score+"%";
    $("scoreValue").style.color=score>=70?"var(--green)":score>=45?"var(--amber)":"var(--red)";
  }
  const missing=kws.filter(k=>k.status==="missing").length;
  // The score is computed from these same checked statuses, so the two can no
  // longer disagree and the note no longer has to explain away a gap.
  $("keywordNote").textContent=kws.length
    ?`${missing} of ${kws.length} screening terms are not evidenced anywhere in `+
     `your CV. The score above is these terms, weighted by importance.`:"";
  list.replaceChildren();
  const order={high:0,medium:1,low:2};
  [...kws].sort((a,b)=>(a.status==="missing"?0:1)-(b.status==="missing"?0:1)
    ||(order[a.importance]??3)-(order[b.importance]??3))
    .forEach(k=>{
      const el=document.createElement("span");
      el.className=k.status+(k.importance==="high"?" high":"");
      el.textContent=(k.status==="covered"?"✓ ":"✗ ")+k.term;
      if(k.importance)el.title=k.importance+" importance";
      list.append(el);
    });
}
function renderFit(){
  // The checked keyword coverage, once a rewrite has been run. The word-overlap
  // number is only a fallback for before that.
  const score=(state.draft||{}).match_score;
  if(score==null){renderFitPill();return}
  const pill=$("fitPill");pill.style.display="";
  pill.textContent=`Match: ${score}%`;
  pill.className="fit-pill "+(score>=70?"good":score>=45?"medium":"low");
}
function renderAll(){
  renderCV();renderRequirements();renderSuggestions();renderGaps();
  renderKeywords();renderFit();renderAnswers();
}

// ── Application answers ──────────────────────────────────────────────────────
// Same document treatment as the CV: a page you type into, with the posting's
// own wording above each box and a live word count against its stated limit.
const words=t=>((t||"").trim().match(/\S+/g)||[]).length;
function answerBlock(label,text,onEdit,limit){
  const wrap=document.createElement("div");
  const q=document.createElement("div");q.className="q";q.textContent=label;wrap.append(q);
  if(limit){const l=document.createElement("div");l.className="limit";
    l.textContent=`Limit: ${limit} words`;wrap.append(l)}
  const a=document.createElement("div");a.className="a";a.contentEditable="true";
  a.spellcheck=true;a.textContent=text||"";
  const foot=document.createElement("div");foot.className="count";
  const n=document.createElement("span");
  const copy=document.createElement("button");copy.className="copy";copy.textContent="Copy";
  copy.onclick=async()=>{
    try{await navigator.clipboard.writeText(a.innerText);copy.textContent="Copied"}
    catch(e){copy.textContent="Select and copy"}
    setTimeout(()=>copy.textContent="Copy",1600);
  };
  const tally=()=>{
    const c=words(a.innerText);
    n.textContent=c+" word"+(c===1?"":"s");
    foot.classList.toggle("over",!!limit&&c>limit*1.1);
  };
  a.addEventListener("input",tally);
  a.addEventListener("blur",()=>{onEdit(a.innerText);queueSave()});
  foot.append(n,copy);wrap.append(a,foot);tally();
  return wrap;
}
function renderAnswers(){
  const root=$("answersDoc");root.replaceChildren();
  const d=state.draft||{};
  const questions=(d.questions||[]).filter(q=>q&&q.question);
  const page=document.createElement("div");page.className="qa";
  const h=document.createElement("h3");h.textContent="Application answers";page.append(h);
  const rule=document.createElement("div");rule.className="rule";page.append(rule);

  if(!questions.length&&!d.cover_letter&&!d.outreach_email){
    const empty=document.createElement("div");empty.className="empty";
    empty.innerHTML="Nothing drafted yet.<br><br>Press <strong>Draft answers</strong> on the right. "+
      "It reads the posting for essay prompts and open-ended questions, then writes each one "+
      "from the CV in the other tab.";
    page.append(empty);root.append(page);return;
  }
  for(const q of questions){
    page.append(answerBlock(q.question,q.answer,text=>{q.answer=text},q.word_limit));
  }
  if(d.cover_letter){
    page.append(answerBlock("Cover letter",d.cover_letter.text,
      text=>{d.cover_letter={...d.cover_letter,text}},300));
  }
  if(d.outreach_email){
    page.append(answerBlock("Note to a recruiter",d.outreach_email.text,
      text=>{d.outreach_email={...d.outreach_email,text}},0));
  }
  root.append(page);
}
async function writeAnswers(){
  $("writeAnswers").disabled=true;$("answerBusy").classList.add("show");notice("");
  try{
    const result=await api("/api/answers",{method:"POST",body:JSON.stringify({
      url:jobUrl,cv_id:cvId,question:$("ownQuestion").value.trim(),
      cover_letter:$("wantCover").checked,outreach:$("wantOutreach").checked,
      instructions:$("instructions").value})});
    state.draft=result.draft;$("ownQuestion").value="";
    showTab("answers");renderAll();
    const flagged=result.unverified_claims||[];
    if(flagged.length){
      notice("Check before sending — "+flagged.join("; "),"");
    }
    const n=(state.draft.questions||[]).length;
    toast(n?`${n} question${n===1?"":"s"} drafted`:"Cover letter drafted");
  }catch(err){notice(err.message,"error")}
  finally{$("writeAnswers").disabled=false;$("answerBusy").classList.remove("show")}
}
function showTab(name){
  const cv=name!=="answers";
  $("cvDoc").style.display=cv?"":"none";
  $("answersDoc").style.display=cv?"none":"";
  document.querySelectorAll("#tabs button").forEach(b=>
    b.classList.toggle("on",b.dataset.tab===(cv?"cv":"answers")));
  $("docMeta").textContent=cv
    ?`${state.document.fact_ids.length} editable lines`
    :`${((state.draft||{}).questions||[]).length} question(s)`;
}

// ── Saving ───────────────────────────────────────────────────────────────────
let saveTimer=null,saving=false;
function flag(text){$("savedFlag").textContent=text}
function queueSave(){flag("Saving…");clearTimeout(saveTimer);saveTimer=setTimeout(syncAndSave,500)}
async function syncAndSave(){
  if(saving){queueSave();return}
  saving=true;
  try{
    state.draft.instructions=$("instructions").value;
    state.draft.cv_id=cvId;
    state.draft.mode=mode;
    const result=await api("/api/draft",{method:"POST",
      body:JSON.stringify({url:jobUrl,cv_id:cvId,draft:state.draft})});
    state.draft=result.draft;flag("Saved");
  }catch(err){flag("Not saved");notice(err.message,"error")}
  finally{saving=false}
}
async function generate(){
  $("generate").disabled=true;$("busy").classList.add("show");notice("");
  $("busyText").textContent="Reading the posting…";
  const t1=setTimeout(()=>{$("busyText").textContent="Planning the running order…"},2500);
  const t2=setTimeout(()=>{$("busyText").textContent="Rewriting every section in parallel…"},7000);
  try{
    const result=await api("/api/suggest",{method:"POST",
      body:JSON.stringify({url:jobUrl,cv_id:cvId,mode,instructions:$("instructions").value})});
    state.draft=result.draft;$("instructions").value=state.draft.instructions||"";
    renderAll();
    const n=allPatches().filter(p=>p.source!=="manual"&&p.status==="pending").length;
    const dropped=(state.draft.hidden||[]).length;
    toast(n?`${n} of ${state.document.fact_ids.length} lines rewritten`+
      (dropped?`, ${dropped} entr${dropped===1?"y":"ies"} left out`:"")+" — review below"
      :"No new suggestions");
  }catch(err){notice(err.message,"error")}
  finally{clearTimeout(t1);clearTimeout(t2);$("generate").disabled=false;$("busy").classList.remove("show")}
}

// ── Saved CVs ────────────────────────────────────────────────────────────────
async function saveAsCv(){
  const label=$("newCvName").value.trim();
  if(!label){notice("Type a name for the CV first.","error");$("newCvName").focus();return}
  try{
    const result=await api("/api/cv/save",{method:"POST",
      body:JSON.stringify({url:jobUrl,cv_id:cvId,label})});
    state.cvs=result.cvs;nameTouched=false;
    renderCvPicker();renderCvList();
    toast(`Saved "${result.cv.label}" to ${result.cv.file}`);
  }catch(err){notice(err.message,"error")}
}
async function renameCv(cv){
  const label=prompt("Rename this CV (the file is renamed too)",cv.label);
  if(!label||label===cv.label)return;
  try{
    const result=await api("/api/cv/rename",{method:"POST",
      body:JSON.stringify({target:cv.id,label})});
    state.cvs=result.cvs;
    if(cvId===cv.id)await loadCv(result.cv.id);
    else{renderCvPicker();renderCvList()}
    toast("Renamed");
  }catch(err){notice(err.message,"error")}
}
async function deleteCv(cv){
  if(!confirm(`Delete the saved CV "${cv.label}"? This cannot be undone.`))return;
  try{
    const result=await api("/api/cv/delete",{method:"POST",body:JSON.stringify({target:cv.id})});
    state.cvs=result.cvs;
    if(cvId===cv.id)await loadCv("master");
    else{renderCvPicker();renderCvList()}
    toast("Deleted");
  }catch(err){notice(err.message,"error")}
}
function renderCvList(){
  const root=$("cvList");root.replaceChildren();
  for(const cv of state.cvs||[]){
    const row=document.createElement("div");row.className="cv-row";
    const name=document.createElement("span");name.className="name";
    name.textContent=cv.label;
    if(cv.id===cvId)name.style.color="var(--green)";
    const file=document.createElement("small");file.className="file";
    file.textContent=(cv.file||"").split("/").pop();
    name.append(file);row.append(name);
    if(cv.is_master){
      const b=document.createElement("span");b.className="gap-badge gap-covered";
      b.textContent="master";row.append(b);
    }else{
      const r=document.createElement("button");r.className="ghost mini";r.textContent="rename";
      r.onclick=()=>renameCv(cv);
      const d=document.createElement("button");d.className="ghost mini";d.textContent="delete";
      d.style.color="var(--red)";d.onclick=()=>deleteCv(cv);
      row.append(r,d);
    }
    root.append(row);
  }
}
function renderCvPicker(){
  const sel=$("cvSelect");sel.replaceChildren();
  for(const cv of state.cvs||[]){
    const o=document.createElement("option");o.value=cv.id;
    o.textContent=cv.label+(cv.is_master?" (master)":"");
    if(cv.id===cvId)o.selected=true;
    sel.append(o);
  }
}
async function saveKey(){
  try{
    const r=await api("/api/settings/key",{method:"POST",body:JSON.stringify({api_key:$("keyInput").value})});
    $("keyInput").value="";
    // The key belongs to the provider selected now, so the card's state comes
    // back from the bridge rather than being assumed here. The endpoint can be
    // asked what it runs as soon as it has a key, so the picker fills in too.
    if(r.provider)state.provider=r.provider;
    if((r.models||[]).length)state.models=r.models;
    renderProvider();renderKey();renderModel();
    toast(`${(state.provider||{}).label||"API"} key saved privately`);
  }
  catch(err){notice(err.message,"error")}
}
function renderProvider(){
  const sel=$("providerSelect");sel.replaceChildren();
  for(const p of state.providers||[]){
    const o=document.createElement("option");o.value=p.base;
    o.textContent=p.label;
    if(p.base===state.base_url)o.selected=true;
    sel.append(o);
  }
  const known=(state.providers||[]).some(p=>p.base===state.base_url);
  if(!known&&state.base_url){
    const o=document.createElement("option");o.value=state.base_url;
    o.textContent="Custom — "+state.base_url;o.selected=true;sel.append(o);
  }
  const provider=state.provider||{};
  const local=provider.local;
  const who=provider.label||"this provider";
  $("providerNote").textContent=local
    ?"Running locally. No key needed, no usage limit, nothing sent off this machine."
    :(provider.configured
      ?`Using your ${who} key. Free tiers exist for Groq, Google AI Studio, OpenRouter and GitHub Models.`
      :`Needs a key for ${who} below — each provider keeps its own. Free tiers exist for Groq, Google AI Studio, OpenRouter and GitHub Models.`);
  $("keyCard").style.display=local?"none":"";
  $("sendNote").textContent=local
    ?"Runs on this machine. Nothing is sent to any provider, and nothing to GitHub."
    :`Sends this posting and your CV to ${who} through your own key — never via GitHub.`;
}
async function saveProvider(url){
  try{
    const r=await api("/api/settings/endpoint",{method:"POST",
      body:JSON.stringify({base_url:url})});
    state.base_url=r.base_url;state.models=r.models||[];
    if(r.provider)state.provider=r.provider;
    // The model belongs to the provider that serves it, so it comes back with
    // the switch. Keeping the previous provider's model is how a Gemini id got
    // posted to OpenAI and came back as a bad request with no stated cause.
    if(r.model)state.model=r.model;
    if(state.models.length&&!state.models.includes(state.model)){
      await saveModel(state.models[0]);
    }
    // The key card follows the provider too: the previous provider's key is
    // still on disk, but it is not this provider's key and is never sent to it.
    hideTestReport();
    renderProvider();renderModel();renderKey();
    toast(state.provider&&state.provider.configured===false&&!state.provider.local
      ?`Provider set — paste a ${state.provider.label} key`:"Provider set");
  }catch(err){notice(err.message,"error")}
}
function hideTestReport(){
  $("testReport").style.display="none";$("testReport").textContent="";
  $("testNote").textContent="";
}
async function saveCustomBase(){
  const url=$("customBase").value.trim();
  if(!url){notice("Paste the base URL of an OpenAI-compatible endpoint.","error");return}
  await saveProvider(url);
  $("customBase").value="";
}
// One cheap round trip, reported exactly as it came back. Until this existed a
// rejected key and a working key looked identical, because a failed model
// listing falls back to the seeded recommendations without saying so.
async function testProvider(){
  const button=$("testProvider");button.disabled=true;
  const before=button.textContent;button.textContent="Testing…";
  $("testNote").textContent="";
  try{
    const r=await api("/api/settings/test",{method:"POST",body:JSON.stringify({})});
    const report=r.report||{};
    const lines=[
      `provider  ${report.provider||"?"}`,
      `endpoint  ${report.endpoint||"?"}`,
      `model     ${report.model||"?"}`,
      `status    ${report.status||"no answer"}${report.ok?"  ok":""}`,
    ];
    if((report.dropped||[]).length)
      lines.push(`dropped   ${report.dropped.join(", ")} (this endpoint refused them)`);
    if(report.detail)lines.push(`it said   ${report.detail}`);
    if(report.problem)lines.push(`problem   ${report.problem}`);
    if(report.note)lines.push(`note      ${report.note}`);
    if(report.listing_problem)lines.push(`listing   ${report.listing_problem}`);
    if((report.models||[]).length)
      lines.push(`offers    ${report.models.slice(0,12).join(", ")}`);
    const box=$("testReport");box.textContent=lines.join("\\n");box.style.display="";
    $("testNote").textContent=r.ok
      ?"This provider answered. Rewriting will work."
      :"This provider did not answer. The reason is above, in its own words.";
    // A working test proves the key, and the listing it returned is better than
    // the seeded guess the picker may be showing.
    if((report.models||[]).length){state.models=report.models;renderModel()}
  }catch(err){notice(err.message,"error")}
  finally{button.disabled=false;button.textContent=before}
}
// Every fix written for this project has to reach the copy of the code that is
// actually answering, and a background helper installed once can sit weeks
// behind the repository without anything looking wrong. This pulls, restarts,
// and waits for the new code to answer — so a fix never depends on someone
// opening a terminal to collect it.
async function updateHelper(){
  const button=$("updateHelper");button.disabled=true;
  const before=button.textContent;button.textContent="Checking…";
  const note=$("updateNote");note.textContent="";
  try{
    const r=await api("/api/update",{method:"POST",body:JSON.stringify({})});
    const report=r.report||{};
    const parked=report.stashed
      ?" Your own edits to the code were parked — git stash pop puts them back."
      :"";
    if(!report.updated){
      note.textContent=(report.reason
        ||`Already up to date${report.commit?` (${report.commit} on ${report.branch||"this branch"})`:""}.`)+parked;
      return;
    }
    if(!r.restarting){
      note.textContent=`Updated ${report.was} → ${report.commit}, but this helper could not`
        +` restart itself. Close it and start it again to run the new code.`+parked;
      return;
    }
    button.textContent="Restarting…";
    note.textContent=`Updated ${report.was} → ${report.commit}. Waiting for the new code to answer…`+parked;
    const health=await waitForRestart(report.commit_before,report.build_before);
    if(!health){
      note.textContent=`Updated ${report.was} → ${report.commit}, but the helper has not answered`
        +` yet. Give it a moment and reload this page.`+parked;
      return;
    }
    note.textContent=`Now running ${report.commit}. Reloading…`;
    setTimeout(()=>location.reload(),600);
  }catch(err){
    // A restart can close the socket before the answer lands. That is the
    // update working, not failing, so it is not reported as an error.
    note.textContent="";
    notice(err.message,"error");
  }
  finally{button.disabled=false;button.textContent=before}
}
// Answering again is not enough: the old process can serve a request or two
// before the service manager takes it away. A different commit, or a gap where
// nothing answered, is what proves the new code is the one talking.
async function waitForRestart(commitBefore,buildBefore,seconds=45){
  const deadline=Date.now()+seconds*1000;
  let wentQuiet=false;
  while(Date.now()<deadline){
    await new Promise(done=>setTimeout(done,900));
    try{
      const r=await fetch("/health",{headers:{"X-Autoapply-Token":token},cache:"no-store"});
      if(!r.ok){wentQuiet=true;continue}
      const health=await r.json();
      const moved=(commitBefore&&health.commit&&health.commit!==commitBefore)
        ||(buildBefore&&health.build&&health.build!==buildBefore);
      if(moved||wentQuiet)return health;
    }catch(err){wentQuiet=true}
  }
  return null;
}
function renderModel(){
  const sel=$("modelSelect");sel.replaceChildren();
  const list=state.models||[];
  if(!list.length){
    const provider=state.provider||{};
    $("modelNote").textContent=provider.local
      ?"No model is running on this machine yet."
      :`Add your ${provider.label?provider.label+" ":""}key to choose a model.`;
    sel.disabled=true;return;
  }
  sel.disabled=false;
  for(const name of list){
    const o=document.createElement("option");o.value=name;o.textContent=name;
    if(name===state.model)o.selected=true;
    sel.append(o);
  }
  $("modelNote").textContent=`Using ${state.model}. Recommended: ${list[0]}.`;
}
async function saveModel(name){
  try{
    const r=await api("/api/settings/model",{method:"POST",body:JSON.stringify({model:name})});
    state.model=r.model;renderModel();toast("Model set to "+r.model);
  }catch(err){notice(err.message,"error")}
}
function renderKey(){
  // Every label here names the provider actually selected. Reading "OpenAI key
  // — configured" while pointed at Google is how a key that cannot work looks
  // like one that does.
  const provider=state.provider||{};
  const shape=provider.key_hint||"";
  const named=provider.label?provider.label+" ":"";
  $("keyTitle").textContent=`${provider.label||"API"} key`;
  $("keyStatus").textContent=provider.configured
    ?"Configured ✓  Replace only if needed."
    :`Not configured — paste your ${named}key${shape?" ("+shape+")":""}.`;
  $("keyInput").placeholder=provider.configured
    ?"Paste replacement key"+(shape?" ("+shape+")":""):(shape||"Paste your key");
  $("saveKey").textContent=provider.configured?"Replace key":"Save key locally";
  const hint=$("keyHint");hint.replaceChildren();
  hint.append(document.createTextNode("Stored in "));
  const file=document.createElement("code");
  file.textContent=provider.key_file||"";hint.append(file);
  hint.append(document.createTextNode(
    " with mode 0600. Never enters GitHub. Each provider keeps its own key"
    +((provider.key_env||[]).length?`, and ${provider.key_env.join(" or ")} is used when no file is saved.`:".")));
  if(provider.key_page){
    hint.append(document.createTextNode(" "));
    const link=document.createElement("a");
    link.href=provider.key_page;link.target="_blank";link.rel="noopener";
    link.textContent=`Get a ${provider.label} key`;hint.append(link);
  }
  // The build serving this page. A bridge is started once and left running for
  // weeks, so the code answering a request can be many commits behind the
  // checkout — and then every symptom belongs to code that is no longer there.
  $("buildNote").textContent=
    `Running the code from ${provider.build||"an unknown build"}`
    +(provider.commit?` (${provider.commit})`:"")
    +(provider.auto_update
      ?" · checks for fixes by itself every few hours"
      :" · automatic updates are off")
    // "key from not configured" is what a prefix gets you; key_source is
    // already a phrase — a path, an environment variable, or a plain reason.
    +(provider.key_source?` · key: ${provider.key_source}`:"")
    +(provider.problem?` · ${provider.problem}`:"");
}
async function exportPdf(){
  $("exportPdf").disabled=true;
  try{
    clearTimeout(saveTimer);
    await syncAndSave();
    const result=await api("/api/export",{method:"POST",body:JSON.stringify({url:jobUrl,cv_id:cvId})});
    const link=document.createElement("a");link.href=result.resume_download_url;
    link.download=result.resume_filename||"";
    document.body.append(link);link.click();link.remove();
    toast(`Downloaded ${result.resume_filename||"CV"}`);
  }catch(err){notice(err.message,"error")}finally{$("exportPdf").disabled=false}
}

// ── Init ─────────────────────────────────────────────────────────────────────
// Whatever went wrong here, the reader still wants their CV tailored for this
// posting — and there is now a version of this editor that runs in the browser
// and cannot be affected by anything wrong with this machine. Offering it is
// better than leaving someone on an error with a chore to do.
function studioFor(){
  const carried=new URLSearchParams();
  if(jobUrl)carried.set("url",jobUrl);
  const job=(state&&state.job)||{};
  for(const field of ["company","role","location"])
    if(job[field])carried.set(field,job[field]);
  for(const field of ["company","role","location"])
    if(!carried.has(field)&&params.get(field))carried.set(field,params.get(field));
  return "https://abyyworld.github.io/internship-tracker/studio.html?"+carried.toString();
}
function showInitError(msg,reachable){
  notice(msg,"error");
  $("jobTitle").textContent=reachable?"Could not open this posting":"Not connected";
  $("jobMeta").textContent=reachable
    ?"The helper is running and answered — see the message below"
    :"Bridge not running";
  const box=document.createElement("div");
  box.className="empty-state";
  box.style.borderColor="#6f3430";box.style.color="var(--red)";
  const title=document.createElement("strong");
  title.textContent="CV not loaded";
  box.append(title,document.createElement("br"),document.createElement("br"),
             document.createTextNode(msg),
             document.createElement("br"),document.createElement("br"));
  const escape=document.createElement("a");
  escape.href=studioFor();
  escape.textContent="Tailor this CV in the browser instead";
  escape.style.color="var(--green)";
  box.append(escape);
  box.append(document.createTextNode(
    " — it needs nothing on this machine. Or double-click "));
  const file=document.createElement("code");
  file.textContent="install-login-service.command";
  box.append(file, document.createTextNode(
    " in the project folder, which repairs and updates the helper."));
  $("cvDoc").replaceChildren(box);
}
async function loadCv(id){
  cvId=id;
  try{localStorage.setItem("autoapply_last_cv",id)}catch(e){}
  state=await api(`/api/editor?url=${encodeURIComponent(jobUrl)}&cv=${encodeURIComponent(cvId)}`);
  cvId=state.cv_id||cvId;
  $("jobTitle").textContent=`${state.job.role} · ${state.job.company}`;
  $("jobMeta").textContent=[state.job.location,
    state.job.description?"description ready":"description loads on Generate"].filter(Boolean).join(" · ");
  $("factCount").textContent=`${state.document.fact_ids.length} lines`;
  $("docMeta").textContent=`${state.document.fact_ids.length} editable lines`;
  $("applyTop").href=$("applySide").href=state.job.application_url;
  $("instructions").value=state.draft.instructions||"";
  if(state.draft.mode&&MODE_NOTES[state.draft.mode]){mode=state.draft.mode;renderMode()}
  if(state.cv_storage)$("cvStorage").textContent=state.cv_storage;
  // Pre-name the CV after this job; the user edits it before pressing Save.
  if(!nameTouched)$("newCvName").value=state.suggested_cv_name||"";
  $("exportName").textContent=state.suggested_cv_name
    ?`Saves as “${(state.document.header.name||"").trim()} - ${state.suggested_cv_name} - CV.pdf”`:"";
  flag("Saved");
  renderCvPicker();renderCvList();renderKey();renderProvider();renderModel();renderAll();
}
async function init(){
  if(token.length<32){showInitError("Browser connection missing — open start-autoapply.command once, then reload.");return}
  if(!jobUrl){showInitError("No job URL was supplied.");return}
  let start="master";
  try{start=localStorage.getItem("autoapply_last_cv")||"master"}catch(e){}
  try{await loadCv(start)}
  catch(err){
    // A remembered CV may have been renamed or removed since last time.
    if(start!=="master"){try{await loadCv("master");return}catch(e){}}
    // An answer, even an error one, means the helper is alive: saying it is not
    // running sends someone to restart a thing that is already working.
    let reachable=false;
    try{await fetch("/health",{headers:{"X-Autoapply-Token":token}});reachable=true}
    catch(e){reachable=false}
    showInitError(err.message,reachable);
  }
}
$("generate").onclick=generate;
$("saveKey").onclick=saveKey;
$("exportPdf").onclick=exportPdf;
$("saveAsCv").onclick=saveAsCv;
$("newCvName").oninput=()=>{nameTouched=true};
$("writeAnswers").onclick=writeAnswers;
$("modelSelect").onchange=e=>saveModel(e.target.value);
$("providerSelect").onchange=e=>saveProvider(e.target.value);
$("testProvider").onclick=testProvider;
$("updateHelper").onclick=updateHelper;
$("saveCustomBase").onclick=saveCustomBase;
$("customBase").onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();saveCustomBase()}};
$("tabs").onclick=e=>{if(e.target.dataset.tab)showTab(e.target.dataset.tab)};
$("cvSelect").onchange=async e=>{
  try{await loadCv(e.target.value);toast("Switched CV")}
  catch(err){notice(err.message,"error")}
};
$("acceptAll").onclick=()=>{
  for(const p of allPatches())if(p.source!=="manual"&&p.status==="pending")p.status="accepted";
  renderAll();queueSave();
};
$("resetAll").onclick=()=>{
  if(!confirm("Discard every edit, rewrite, and reordering for this CV and job?"))return;
  state.draft.summary=null;state.draft.bullets={};
  state.draft.order={sections:[],entries:{}};state.draft.hidden=[];
  renderAll();queueSave();
};
function renderMode(){
  document.querySelectorAll(".modes button").forEach(b=>
    b.classList.toggle("on",b.dataset.mode===mode));
  $("modeNote").textContent=MODE_NOTES[mode]||"";
}
document.querySelector(".modes").onclick=e=>{
  if(!e.target.dataset.mode)return;
  mode=e.target.dataset.mode;
  try{localStorage.setItem("autoapply_mode",mode)}catch(err){}
  renderMode();
};
try{mode=localStorage.getItem("autoapply_mode")||"full"}catch(err){}
if(!MODE_NOTES[mode])mode="full";
renderMode();
init();
</script></body></html>"""
