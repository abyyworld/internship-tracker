from __future__ import annotations


EDITOR_PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI CV Studio</title>
<style>
:root{color-scheme:dark;--bg:#07110f;--panel:#0d1b17;--panel2:#13251f;
--line:#29473d;--text:#f3f8f6;--muted:#9fb5ad;--green:#71efae;
--green2:#27bd79;--blue:#7db6ff;--red:#ff938b;--amber:#ffcf70;--purple:#c4a0ff}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 18% -10%,#15533a77,
transparent 38rem),var(--bg);color:var(--text);font:14px/1.5 -apple-system,
BlinkMacSystemFont,"Segoe UI",sans-serif}button,input,textarea,select{font:inherit}
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
/* 3-column layout */
.layout{display:grid;grid-template-columns:340px minmax(0,1.4fr) 300px;gap:0;height:calc(100vh - 57px);overflow:hidden}
.pane{height:100%;overflow-y:auto;display:flex;flex-direction:column}
.pane-header{position:sticky;top:0;z-index:5;background:#07110f;border-bottom:1px solid var(--line);
padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-shrink:0}
.pane-left{border-right:1px solid var(--line)}
.pane-right{border-left:1px solid var(--line)}
.pane-body{padding:14px 16px;flex:1}
.card{background:linear-gradient(145deg,var(--panel2),var(--panel));border:1px solid var(--line);
border-radius:14px;padding:16px;margin-bottom:12px}
.eyebrow{color:var(--green);font-size:10px;font-weight:950;letter-spacing:.14em;text-transform:uppercase}
.eyebrow.purple{color:var(--purple)}
h1,h2,h3,p{margin-top:0}h1{font-size:24px;letter-spacing:-.04em;margin:4px 0 5px}
h2{font-size:17px}h3{font-size:13px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.muted{color:var(--muted)}
.notice{border:1px solid #66552b;background:#2b2414;padding:11px 13px;border-radius:11px;
color:#ffe1a1;margin-bottom:12px}.notice.error{border-color:#6f3430;background:#2a1715;
color:var(--red)}.notice.ok{border-color:#285f49;background:#10271e;color:var(--green)}
.notice.info{border-color:#2d4a7a;background:#0e1f38;color:var(--blue)}
/* Suggestion cards */
.suggestion{border:1px solid var(--line);background:#091410;border-radius:13px;padding:13px;margin-top:10px}
.suggestion.accepted{border-color:#2f8c64}.suggestion.rejected{opacity:.65}
.suggestion-head{display:flex;justify-content:space-between;gap:8px;margin-bottom:8px}
.label{font-size:10px;font-weight:900;color:var(--blue);letter-spacing:.08em;text-transform:uppercase}
.rationale{color:var(--muted);font-size:11px;line-height:1.45;margin:8px 0}
.keywords{display:flex;gap:4px;flex-wrap:wrap;margin:6px 0}
.keywords i{font-style:normal;border-radius:99px;background:#172c25;padding:2px 6px;font-size:10px;color:var(--green)}
.diff{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0}
.diff small{display:block;color:var(--muted);font-weight:800;font-size:10px;margin-bottom:4px}
.original,.proposal{width:100%;min-height:90px;border:1px solid var(--line);
border-radius:8px;padding:9px;color:var(--text);background:#07100d;resize:vertical;font-size:12px}
.original{color:#b6c6c0}.proposal{border-color:#376455}
.choice-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.choice.active{border-color:var(--green);color:var(--green)}
.choice.keep.active{border-color:var(--amber);color:var(--amber)}
/* Editable CV pane */
.cv-section{margin-bottom:18px}
.cv-section-head{font-size:11px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;
color:var(--green);border-bottom:1px solid var(--line);padding-bottom:6px;margin-bottom:10px}
.cv-entry{margin-bottom:14px}
.cv-entry-head{display:flex;align-items:baseline;justify-content:space-between;gap:8px}
.cv-entry strong{font-size:13px;font-weight:800}
.cv-entry .dates{font-size:11px;color:var(--muted)}
.cv-bullet{display:flex;gap:8px;margin:5px 0;align-items:flex-start}
.cv-bullet::before{content:"·";color:var(--green);font-size:14px;flex-shrink:0;margin-top:1px}
.bullet-text{font-size:12px;color:#c6d5d0;flex:1;min-width:0;word-break:break-word}
.bullet-text.patched{color:var(--green);font-style:italic}
.bullet-text.accepted-patch{border-left:2px solid var(--green);padding-left:6px}
.bullet-edit{min-height:22px;padding:0 6px;font-size:10px;background:transparent;
color:var(--green);border-color:transparent}
.cv-summary{background:#0a1710;border:1px solid var(--line);border-radius:9px;padding:10px;
font-size:12px;color:#c6d5d0;margin-bottom:14px;cursor:pointer}
.cv-summary:hover{border-color:var(--green2)}
/* Gap analysis */
.gap-row{display:flex;align-items:baseline;gap:7px;padding:5px 0;border-bottom:1px solid #1a2e27}
.gap-row:last-child{border-bottom:none}
.gap-skill{font-size:12px;flex:1}
.gap-badge{font-size:10px;padding:2px 7px;border-radius:99px}
.gap-missing{background:#2a1715;color:var(--red);border:1px solid #6f3430}
.gap-partial{background:#2b2414;color:var(--amber);border:1px solid #66552b}
.gap-covered{background:#0f2318;color:var(--green);border:1px solid #2a7455}
/* Right pane */
.export-section{display:flex;flex-direction:column;gap:10px}
textarea.instruction{width:100%;border:1px solid var(--line);background:#07100d;
color:var(--text);padding:10px;border-radius:10px;min-height:90px;resize:vertical;font-size:13px}
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
font-size:13px;max-width:400px;text-align:center}
.empty-state{text-align:center;padding:40px 16px;color:var(--muted);border:1px dashed var(--line);
border-radius:13px;font-size:13px}
.advice-list{list-style:none;padding:0;margin:0}
.advice-list li{padding:6px 0;border-bottom:1px solid #1a2e27;font-size:12px;color:var(--muted)}
.advice-list li:last-child{border-bottom:none}
.advice-list li::before{content:"💡 "}
@media(max-width:1100px){.layout{grid-template-columns:290px minmax(0,1fr) 260px}}
@media(max-width:800px){.layout{grid-template-columns:1fr;height:auto;overflow:visible}
  .pane{height:auto;overflow-y:visible}.pane-left,.pane-right{border:none;border-top:1px solid var(--line)}}
</style></head>
<body><div class="shell">
<header>
  <div class="brand"><b>AI</b> CV Studio</div>
  <div class="job"><strong id="jobTitle">Loading…</strong><span id="jobMeta">Private localhost editor</span></div>
  <span class="fit-pill" id="fitPill" style="display:none"></span>
  <a class="button ghost" href="https://abyyworld.github.io/internship-tracker/" style="white-space:nowrap">Dashboard</a>
  <a class="button primary" id="applyTop" target="_blank" rel="noopener" style="white-space:nowrap">Open application</a>
</header>
<div class="layout">

<!-- LEFT: AI suggestions -->
<aside class="pane pane-left">
  <div class="pane-header">
    <div>
      <div class="eyebrow">AI suggestions</div>
      <div style="font-weight:800;font-size:15px">Suggested edits</div>
    </div>
    <div class="stats"><span class="pill" id="factCount">— facts</span>
    <span class="pill ok" id="acceptedCount" style="display:none"></span></div>
  </div>
  <div class="pane-body">
    <div id="notice"></div>
    <div id="suggestions">
      <div class="empty-state">Open a job, press <strong>Generate</strong> in the right panel.<br><br>
      AI will suggest a handful of targeted edits while your complete CV stays intact.</div>
    </div>
    <div id="adviceSection" style="display:none">
      <h3 style="margin-top:16px">Application advice</h3>
      <ul class="advice-list" id="adviceList"></ul>
    </div>
  </div>
</aside>

<!-- MIDDLE: Editable CV -->
<main class="pane">
  <div class="pane-header">
    <div>
      <div class="eyebrow">Your CV</div>
      <div style="font-weight:800;font-size:15px">Live document</div>
    </div>
    <div style="display:flex;gap:8px">
      <button class="secondary" id="acceptAll" disabled style="min-height:34px;font-size:12px">Accept all</button>
      <button class="secondary" id="resetAll" disabled style="min-height:34px;font-size:12px">Reset</button>
    </div>
  </div>
  <div class="pane-body">
    <div id="cvDoc"><div class="empty-state">Loading CV…</div></div>
  </div>
</main>

<!-- RIGHT: Controls + gap analysis + export -->
<aside class="pane pane-right">
  <div class="pane-header">
    <div class="eyebrow">Controls</div>
  </div>
  <div class="pane-body">

    <div class="card">
      <div class="eyebrow">Instructions</div>
      <textarea class="instruction" id="instructions" maxlength="4000"
        placeholder="Optional: e.g. Emphasise Python and systems programming. Keep my academic tone."></textarea>
      <p class="hint">Sending triggers an OpenAI call through your key — never via GitHub.</p>
      <div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">
        <button class="primary" id="generate">Generate suggestions</button>
      </div>
      <div class="busy" id="busy"><span class="spinner"></span><span id="busyText">AI is reviewing your CV…</span></div>
    </div>

    <div class="card" id="gapCard" style="display:none">
      <div class="eyebrow purple">Gap analysis</div>
      <p class="muted" style="font-size:12px;margin-bottom:8px">Keywords in the job not yet in your CV draft:</p>
      <div id="gapList"></div>
    </div>

    <div class="card">
      <div class="eyebrow">Export</div>
      <div class="export-section">
        <p class="muted" style="font-size:12px" id="exportNote">Accepted patches will be applied. Everything else stays original.</p>
        <button class="primary" id="exportPdf">Download tailored PDF</button>
        <a class="button secondary" id="applySide" target="_blank" rel="noopener">Apply with Simplify</a>
      </div>
    </div>

    <div class="card" id="keyCard">
      <div class="eyebrow">OpenAI key</div>
      <p class="muted" style="font-size:12px" id="keyStatus">Checking…</p>
      <input class="key" id="keyInput" type="password" autocomplete="off" placeholder="sk-…" style="margin:8px 0">
      <button class="secondary" id="saveKey" style="width:100%">Save key locally</button>
      <p class="hint">Stored in <code>private/openai.key</code> with mode 0600. Never enters GitHub.</p>
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
const $=id=>document.getElementById(id);
function esc(v){const d=document.createElement("div");d.textContent=v??"";return d.innerHTML}
function toast(msg){$("toast").textContent=msg;$("toast").style.display="block";setTimeout(()=>$("toast").style.display="none",2600)}
function notice(msg,type=""){const box=$("notice");box.replaceChildren();if(!msg)return;const d=document.createElement("div");d.className="notice "+type;d.textContent=msg;box.append(d)}
async function api(path,options={}){
  const r=await fetch(path,{...options,headers:{"Content-Type":"application/json","X-Autoapply-Token":token,...(options.headers||{})}});
  const result=await r.json();if(!r.ok)throw new Error(result.error||`Bridge returned ${r.status}`);return result
}

// ── Fit score ──────────────────────────────────────────────────────────────────
function computeFit(){
  if(!state)return null;
  const desc=((state.job&&state.job.raw_description)||"").toLowerCase();
  if(!desc)return null;
  const skills=(state.document.skills||[]).map(s=>s.toLowerCase());
  const bullets=[];
  for(const sec of state.document.sections||[])
    for(const ent of sec.entries||[])
      for(const b of ent.bullets||[])
        bullets.push((b.text||"").toLowerCase());
  const words=[...skills,...bullets].join(" ");
  const jobWords=desc.match(/\b[a-z][a-z0-9\+\#\.]{2,}\b/g)||[];
  const unique=[...new Set(jobWords)].filter(w=>w.length>3&&!["with","from","that","this","will","have","your","their","they","into","been","each","when","than","such","also","must","able","more","some","most","only","very","both","well","over","just","even","then","much","need","make","about","using","these","other","which","after","where"].includes(w));
  if(!unique.length)return null;
  const matched=unique.filter(w=>words.includes(w));
  return Math.round((matched.length/unique.length)*100);
}
function renderFitPill(){
  const score=computeFit();
  const pill=$("fitPill");
  if(score===null){pill.style.display="none";return}
  pill.style.display="";
  pill.textContent=`Fit: ${score}%`;
  pill.className="fit-pill "+(score>=70?"good":score>=45?"medium":"low");
}

// ── Gap analysis ───────────────────────────────────────────────────────────────
function computeGaps(){
  if(!state)return[];
  const desc=((state.job&&state.job.raw_description)||"").toLowerCase();
  if(!desc)return[];
  // Build current draft text (use accepted proposals where available)
  const draft=state.draft||{};
  const draftBullets=draft.bullets||{};
  const cvText=(state.document.skills||[]).join(" ")+" "+
    (state.document.sections||[]).flatMap(s=>s.entries||[]).flatMap(e=>{
      return(e.bullets||[]).map(b=>{
        const patch=draftBullets[b.id];
        return patch&&patch.status==="accepted"?patch.proposal:b.text;
      });
    }).join(" ");
  const lower=cvText.toLowerCase();
  // Extract technical keywords from job description
  const techPatterns=[
    /\b(python|java|javascript|typescript|c\+\+|c#|rust|go|golang|swift|kotlin|ruby|scala|r\b|matlab|julia)\b/gi,
    /\b(pytorch|tensorflow|keras|sklearn|numpy|pandas|jax|huggingface|transformers)\b/gi,
    /\b(react|vue|angular|node\.?js|express|django|flask|fastapi|spring)\b/gi,
    /\b(aws|gcp|azure|kubernetes|docker|terraform|kafka|spark|flink)\b/gi,
    /\b(machine learning|deep learning|computer vision|nlp|llm|rl|reinforcement)\b/gi,
    /\b(sql|postgresql|mysql|mongodb|redis|cassandra|elasticsearch)\b/gi,
    /\b(git|ci\/cd|devops|agile|scrum|rest api|grpc|graphql)\b/gi,
    /\b(ros|slam|perception|autonomy|control systems|mechatronics)\b/gi,
    /\b(fpga|vhdl|verilog|embedded|firmware|arm|rtos)\b/gi,
    /\b(linux|unix|bash|shell)\b/gi,
  ];
  const found=new Set();
  for(const pat of techPatterns){
    for(const m of desc.matchAll(pat)){found.add(m[0].toLowerCase().trim())}
  }
  const gaps=[];
  for(const kw of found){
    if(lower.includes(kw))gaps.push({kw,status:"covered"});
    else{
      const partial=kw.split(/\s+/).some(part=>part.length>3&&lower.includes(part));
      gaps.push({kw,status:partial?"partial":"missing"});
    }
  }
  gaps.sort((a,b)=>{const r={missing:0,partial:1,covered:2};return r[a.status]-r[b.status]||a.kw.localeCompare(b.kw)});
  return gaps.slice(0,24);
}
function renderGaps(){
  const gaps=computeGaps();
  const card=$("gapCard"),list=$("gapList");
  if(!gaps.length){card.style.display="none";return}
  card.style.display="";
  list.replaceChildren();
  for(const g of gaps){
    const row=document.createElement("div");row.className="gap-row";
    const skill=document.createElement("span");skill.className="gap-skill";skill.textContent=g.kw;
    const badge=document.createElement("span");
    badge.className="gap-badge gap-"+g.status;
    badge.textContent=g.status==="covered"?"✓ covered":g.status==="partial"?"~ partial":"✗ missing";
    row.append(skill,badge);list.append(row);
  }
}

// ── CV document renderer ───────────────────────────────────────────────────────
function activePatchText(bulletId){
  const draft=state&&state.draft||{};
  const patch=(draft.bullets||{})[bulletId];
  if(patch&&patch.status==="accepted")return{text:patch.proposal,accepted:true};
  return null;
}
function renderCV(){
  const doc=state.document,root=$("cvDoc");root.replaceChildren();
  // Summary
  const draft=state.draft||{};
  const sumPatch=draft.summary;
  const sumText=sumPatch&&sumPatch.status==="accepted"?sumPatch.proposal:doc.summary;
  if(sumText){
    const wrap=document.createElement("div");wrap.className="cv-section";
    const sh=document.createElement("div");sh.className="cv-section-head";sh.textContent="Summary";wrap.append(sh);
    const box=document.createElement("div");box.className="cv-summary";
    box.textContent=sumText;
    if(sumPatch&&sumPatch.status==="accepted")box.style.color="var(--green)";
    box.title="Click to create an editable patch";
    box.onclick=()=>addManualPatch("summary",doc.summary);
    wrap.append(box);root.append(wrap);
  }
  // Sections
  for(const sec of doc.sections||[]){
    const wrap=document.createElement("div");wrap.className="cv-section";
    const sh=document.createElement("div");sh.className="cv-section-head";sh.textContent=sec.name;wrap.append(sh);
    for(const entry of sec.entries||[]){
      const block=document.createElement("div");block.className="cv-entry";
      const head=document.createElement("div");head.className="cv-entry-head";
      const title=document.createElement("strong");
      title.textContent=[entry.title,entry.organization].filter(Boolean).join(" · ");
      const dates=document.createElement("span");dates.className="dates";dates.textContent=entry.dates||"";
      head.append(title,dates);block.append(head);
      // Supervisor / lab (academic fields)
      if(entry.supervisor){
        const sup=document.createElement("div");sup.style.cssText="font-size:11px;color:var(--muted);margin:3px 0";
        sup.textContent=`Supervisor: ${entry.supervisor}`;block.append(sup);
      }
      // Bullets
      for(const bullet of entry.bullets||[]){
        const patch=activePatchText(bullet.id);
        const text=patch?patch.text:bullet.text;
        const li=document.createElement("div");li.className="cv-bullet";
        const dot=document.createElement("span");dot.textContent="·";dot.style.cssText="color:var(--green);flex-shrink:0;padding-top:1px";
        const span=document.createElement("span");span.className="bullet-text"+(patch?" patched accepted-patch":"");
        span.textContent=text;
        const editBtn=document.createElement("button");editBtn.className="ghost bullet-edit";editBtn.textContent="edit";
        editBtn.onclick=()=>addManualPatch(bullet.id,bullet.text);
        li.append(dot,span,editBtn);block.append(li);
      }
      wrap.append(block);
    }
    root.append(wrap);
  }
}

// ── Suggestion cards ──────────────────────────────────────────────────────────
function patchCard(patch,label){
  const card=document.createElement("article");card.className="suggestion "+(patch.status||"pending");
  const head=document.createElement("div");head.className="suggestion-head";
  const lbl=document.createElement("span");lbl.className="label";lbl.textContent=label;
  const idPill=document.createElement("span");idPill.className="pill";
  idPill.textContent=patch.id==="summary"?"Summary":patch.id.replace(/-/g," ").slice(0,22);
  head.append(lbl,idPill);card.append(head);
  // Diff
  const diff=document.createElement("div");diff.className="diff";
  const before=document.createElement("div");before.innerHTML="<small>Original</small>";
  const origTA=document.createElement("textarea");origTA.className="original";origTA.readOnly=true;
  origTA.value=patch.original;before.append(origTA);
  const after=document.createElement("div");after.innerHTML="<small>AI suggestion — editable</small>";
  const propTA=document.createElement("textarea");propTA.className="proposal";propTA.value=patch.proposal;
  propTA.maxLength=600;
  propTA.addEventListener("change",()=>{patch.proposal=propTA.value;syncAndSave()});
  after.append(propTA);diff.append(before,after);card.append(diff);
  if(patch.rationale){const r=document.createElement("p");r.className="rationale";r.textContent=patch.rationale;card.append(r)}
  if(patch.keywords?.length){const kw=document.createElement("div");kw.className="keywords";for(const k of patch.keywords){const i=document.createElement("i");i.textContent=k;kw.append(i)}card.append(kw)}
  const actions=document.createElement("div");actions.className="choice-row";
  const accept=document.createElement("button");accept.className="secondary choice";accept.textContent="Accept";
  accept.classList.toggle("active",patch.status==="accepted");
  const keep=document.createElement("button");keep.className="ghost choice keep";keep.textContent="Keep original";
  keep.classList.toggle("active",patch.status==="rejected");
  accept.onclick=()=>{patch.status="accepted";renderSuggestions();syncAndSave()};
  keep.onclick=()=>{patch.status="rejected";renderSuggestions();syncAndSave()};
  actions.append(accept,keep);card.append(actions);return card;
}
function renderSuggestions(){
  const root=$("suggestions");root.replaceChildren();
  const draft=state&&state.draft||{};
  const items=[];
  if(draft.summary)items.push([draft.summary,"Profile summary"]);
  for(const p of Object.values(draft.bullets||{}))items.push([p,"Bullet"]);
  if(!items.length){
    root.innerHTML='<div class="empty-state">No suggestions yet.<br>Press <strong>Generate</strong> to analyse this role.</div>';
    $("acceptAll").disabled=$("resetAll").disabled=true;
    $("exportNote").textContent="Pending and rejected patches use the original wording.";
    return;
  }
  for(const [p,lbl] of items)root.append(patchCard(p,lbl));
  $("acceptAll").disabled=$("resetAll").disabled=false;
  const accepted=items.filter(([p])=>p.status==="accepted").length;
  $("acceptedCount").textContent=`${accepted} accepted`;
  $("acceptedCount").style.display=accepted?"":"none";
  $("exportNote").textContent=`${accepted} accepted edit${accepted===1?"":"s"} will be applied. Everything else stays original.`;
  const rejected=Object.keys(draft.rejected_by_validator||{}).length;
  if(rejected)notice(`${rejected} unsafe model suggestion${rejected===1?" was":"s were"} automatically discarded.`,"");
  // Advice
  const advice=(draft.advice||[]).filter(Boolean);
  if(advice.length){
    $("adviceSection").style.display="";
    const ul=$("adviceList");ul.replaceChildren();
    for(const a of advice){const li=document.createElement("li");li.textContent=a;ul.append(li)}
  }else $("adviceSection").style.display="none";
  renderCV();renderGaps();renderFitPill();
}

// ── Manual patches ────────────────────────────────────────────────────────────
function addManualPatch(id,original){
  if(id==="summary"){
    state.draft.summary=state.draft.summary||{id,original,proposal:original,rationale:"Manual edit",keywords:[],status:"pending"};
  }else{
    state.draft.bullets=state.draft.bullets||{};
    state.draft.bullets[id]=state.draft.bullets[id]||{id,original,proposal:original,rationale:"Manual edit",keywords:[],status:"pending"};
  }
  renderSuggestions();syncAndSave();
  toast("Editable patch created — scroll up to the suggestions panel");
}

// ── API helpers ───────────────────────────────────────────────────────────────
async function syncAndSave(){
  renderCV();renderGaps();renderFitPill();
  try{
    state.draft.instructions=$("instructions").value;
    const result=await api("/api/draft",{method:"POST",body:JSON.stringify({url:jobUrl,draft:state.draft})});
    state.draft=result.draft;
  }catch(err){notice(err.message,"error")}
}
async function generate(){
  $("generate").disabled=true;$("busy").classList.add("show");notice("");
  $("busyText").textContent="AI is comparing the role and your full CV…";
  try{
    const result=await api("/api/suggest",{method:"POST",body:JSON.stringify({url:jobUrl,instructions:$("instructions").value})});
    state.draft=result.draft;$("instructions").value=state.draft.instructions||"";
    renderSuggestions();toast("Suggestions ready — review each one below");
  }catch(err){notice(err.message,"error")}finally{$("generate").disabled=false;$("busy").classList.remove("show")}
}
async function saveKey(){
  const key=$("keyInput").value;
  try{await api("/api/settings/openai",{method:"POST",body:JSON.stringify({api_key:key})});
    $("keyInput").value="";state.ai_configured=true;renderKey();toast("OpenAI key saved privately")}
  catch(err){notice(err.message,"error")}
}
function renderKey(){
  $("keyStatus").textContent=state.ai_configured?
    "Configured ✓  Replace only if needed.":"Not configured — paste your OpenAI key.";
  $("keyStatus").className=state.ai_configured?"muted ok":"muted";
  $("keyInput").placeholder=state.ai_configured?"Paste replacement key (sk-…)":"sk-…";
  $("saveKey").textContent=state.ai_configured?"Replace key":"Save key locally";
}
async function exportPdf(){
  $("exportPdf").disabled=true;
  try{
    await syncAndSave();
    const result=await api("/api/export",{method:"POST",body:JSON.stringify({url:jobUrl})});
    const link=document.createElement("a");link.href=result.resume_download_url;link.download="";
    document.body.append(link);link.click();link.remove();
    toast(`Downloaded CV · ${result.accepted_patch_count} accepted edits applied`);
  }catch(err){notice(err.message,"error")}finally{$("exportPdf").disabled=false}
}

// ── Init ──────────────────────────────────────────────────────────────────────
function showInitError(msg){
  notice(msg,"error");
  $("jobTitle").textContent="Not connected";
  $("jobMeta").textContent="Bridge not running";
  $("cvDoc").innerHTML='<div class="empty-state" style="border-color:#6f3430;color:var(--red)">'+
    '<strong>CV not loaded</strong><br><br>'+msg+'<br><br>'+
    'Double-click <code>start-autoapply.command</code> in the project folder, then reload this page.</div>';
}
async function init(){
  if(token.length<32){showInitError("Browser connection missing — open start-autoapply.command once, then reload.");return}
  if(!jobUrl){showInitError("No job URL was supplied.");return}
  try{
    state=await api(`/api/editor?url=${encodeURIComponent(jobUrl)}`);
    $("jobTitle").textContent=`${state.job.role} · ${state.job.company}`;
    $("jobMeta").textContent=[state.job.location,state.job.description?"description ready":"description loads on Generate"].filter(Boolean).join(" · ");
    $("factCount").textContent=`${state.document.fact_ids.length} facts`;
    $("applyTop").href=$("applySide").href=state.job.application_url;
    $("instructions").value=state.draft.instructions||"";
    renderKey();renderCV();renderSuggestions();renderGaps();renderFitPill();
  }catch(err){showInitError(err.message)}
}
$("generate").onclick=generate;
$("saveKey").onclick=saveKey;
$("exportPdf").onclick=exportPdf;
$("acceptAll").onclick=()=>{
  if(state.draft.summary)state.draft.summary.status="accepted";
  for(const p of Object.values(state.draft.bullets||{}))p.status="accepted";
  renderSuggestions();syncAndSave();
};
$("resetAll").onclick=()=>{
  if(state.draft.summary)state.draft.summary.status="pending";
  for(const p of Object.values(state.draft.bullets||{}))p.status="pending";
  renderSuggestions();syncAndSave();
};
init();
</script></body></html>"""
