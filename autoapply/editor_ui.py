from __future__ import annotations


EDITOR_PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CV Patch Studio</title>
<style>
:root{color-scheme:dark;--bg:#07110f;--panel:#0d1b17;--panel2:#13251f;
--line:#29473d;--text:#f3f8f6;--muted:#9fb5ad;--green:#71efae;
--green2:#27bd79;--blue:#7db6ff;--red:#ff938b;--amber:#ffcf70}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 18% -10%,#15533a77,
transparent 38rem),var(--bg);color:var(--text);font:14px/1.5 -apple-system,
BlinkMacSystemFont,"Segoe UI",sans-serif}button,input,textarea{font:inherit}
button,a.button{border:1px solid var(--line);border-radius:10px;min-height:40px;padding:0 14px;
font-weight:800;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;
justify-content:center}.primary{background:var(--green2);color:#03130c}.secondary{background:#152821;
color:var(--text)}.ghost{background:transparent;color:var(--muted)}button:disabled{opacity:.45;
cursor:not-allowed}.shell{min-height:100vh;display:grid;grid-template-rows:auto 1fr}
header{position:sticky;z-index:5;top:0;background:#07110fe8;backdrop-filter:blur(14px);
border-bottom:1px solid var(--line);padding:14px 20px;display:flex;align-items:center;gap:16px}
.brand{font-size:20px;font-weight:950;letter-spacing:-.04em}.brand b{color:var(--green)}
.job{min-width:0;flex:1}.job strong,.job span{display:block;white-space:nowrap;overflow:hidden;
text-overflow:ellipsis}.job span{color:var(--muted);font-size:12px}
.layout{display:grid;grid-template-columns:minmax(0,1fr) 390px;gap:16px;padding:16px;
max-width:1500px;width:100%;margin:auto}.card{background:linear-gradient(145deg,var(--panel2),
var(--panel));border:1px solid var(--line);border-radius:16px;padding:18px}
.toolbar{display:flex;justify-content:space-between;gap:12px;align-items:start;margin-bottom:16px}
.eyebrow{color:var(--green);font-size:10px;font-weight:950;letter-spacing:.14em;
text-transform:uppercase}h1,h2,h3,p{margin-top:0}h1{font-size:27px;letter-spacing:-.04em;
margin:4px 0 5px}h2{font-size:19px}.muted{color:var(--muted)}
.stats{display:flex;flex-wrap:wrap;gap:7px}.pill{border:1px solid var(--line);border-radius:99px;
padding:4px 9px;color:var(--muted);font-size:11px}.pill.ok{border-color:#2a7455;color:var(--green)}
.notice{border:1px solid #66552b;background:#2b2414;padding:12px;border-radius:11px;
color:#ffe1a1;margin-bottom:14px}.notice.error{border-color:#6f3430;background:#2a1715;
color:var(--red)}.notice.ok{border-color:#285f49;background:#10271e;color:var(--green)}
.suggestion{border:1px solid var(--line);background:#091410;border-radius:14px;padding:15px;
margin-top:12px}.suggestion.accepted{border-color:#2f8c64}.suggestion.rejected{opacity:.7}
.suggestion-head{display:flex;justify-content:space-between;gap:10px}.label{font-size:11px;
font-weight:900;color:var(--blue);letter-spacing:.08em;text-transform:uppercase}
.diff{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}.diff>div{min-width:0}
.diff small{display:block;color:var(--muted);font-weight:800;margin-bottom:5px}
.original,.proposal{width:100%;min-height:118px;border:1px solid var(--line);
border-radius:9px;padding:10px;color:var(--text);background:#07100d;resize:vertical}
.original{color:#b6c6c0}.proposal{border-color:#376455}.rationale{color:var(--muted);
font-size:12px}.keywords{display:flex;gap:5px;flex-wrap:wrap;margin:8px 0}
.keywords i{font-style:normal;border-radius:99px;background:#172c25;padding:2px 7px;
font-size:10px;color:var(--green)}.actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}
.choice.active{border-color:var(--green);color:var(--green)}
.choice.keep.active{border-color:var(--amber);color:var(--amber)}
.empty{text-align:center;padding:54px 22px;color:var(--muted);border:1px dashed var(--line);
border-radius:14px}.side{display:flex;flex-direction:column;gap:16px}.side .card{position:relative}
textarea.instruction,input.key{width:100%;border:1px solid var(--line);background:#07100d;
color:var(--text);padding:11px;border-radius:10px}.instruction{min-height:105px;resize:vertical}
.hint{font-size:11px;color:var(--muted);margin:7px 0}.full-cv{max-height:45vh;overflow:auto;
padding-right:5px}.cv-section{margin-top:13px}.cv-section h3{font-size:11px;color:var(--green);
letter-spacing:.1em}.cv-entry{margin-bottom:12px}.cv-entry strong{font-size:12px}
.cv-entry ul{margin:5px 0;padding-left:18px;color:#c6d5d0;font-size:11px}
.cv-entry li{margin:5px 0}.mini-edit{min-height:24px;padding:0 7px;margin-left:6px;
font-size:9px;background:transparent;color:var(--green)}
.busy{display:none;align-items:center;gap:8px;color:var(--green)}.busy.show{display:flex}
.spinner{width:16px;height:16px;border:2px solid #35604f;border-top-color:var(--green);
border-radius:50%;animation:spin .75s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
#toast{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);background:#172c25;
border:1px solid var(--line);padding:10px 15px;border-radius:9px;display:none;z-index:10}
@media(max-width:900px){.layout{grid-template-columns:1fr}.side{grid-row:1}.full-cv{max-height:320px}}
@media(max-width:650px){header{align-items:flex-start;flex-wrap:wrap}.diff{grid-template-columns:1fr}
.layout{padding:9px}.card{padding:14px}}
</style></head>
<body><div class="shell">
<header><div class="brand"><b>CV</b> Patch Studio</div>
<div class="job"><strong id="jobTitle">Loading role…</strong><span id="jobMeta">Private localhost editor</span></div>
<a class="button ghost" href="https://abyyworld.github.io/internship-tracker/">Dashboard</a>
<a class="button primary" id="applyTop" target="_blank" rel="noopener">Open application</a>
</header>
<div class="layout">
<main class="card">
  <div class="toolbar"><div><div class="eyebrow">Non-destructive MiniMax M3 tailoring</div>
  <h1>Review suggested edits</h1><p class="muted">Nothing changes unless you accept it.
  Export always retains the complete master CV.</p></div>
  <div class="stats"><span class="pill" id="factCount">— facts</span>
  <span class="pill ok">full CV locked</span></div></div>
  <div id="notice"></div><div id="suggestions"><div class="empty">
  Open a job and press <b>Generate suggestions</b>. M3 will propose a few targeted edits
  while every other line stays untouched.</div></div>
</main>
<aside class="side">
  <section class="card"><div class="eyebrow">Direct M3 instructions</div>
  <h2>What should improve?</h2>
  <textarea class="instruction" id="instructions" maxlength="4000"
  placeholder="Example: Emphasise robotics software and C++ evidence. Keep my technical tone and do not change the awards."></textarea>
  <p class="hint">Generating replaces only the pending suggestion set. Your master CV is never overwritten.</p>
  <p class="hint">Pressing Generate sends the job description and master CV text to
  MiniMax M3 through your API account. It is never sent to GitHub.</p>
  <div class="actions"><button class="primary" id="generate">Generate suggestions</button>
  <button class="secondary" id="acceptAll" disabled>Accept all safe</button></div>
  <div class="busy" id="busy"><span class="spinner"></span><span>M3 is comparing the full CV…</span></div>
  </section>
  <section class="card" id="keyCard"><div class="eyebrow">Private API setup</div>
  <h2>MiniMax M3 key</h2><p class="muted" id="keyStatus">Checking local configuration…</p>
  <input class="key" id="keyInput" type="password" autocomplete="off"
  placeholder="Paste MiniMax API key"><div class="actions">
  <button class="secondary" id="saveKey">Save key locally</button></div>
  <p class="hint">Stored only in <code>private/minimax.key</code> with macOS mode 0600.
  It never enters GitHub or this page’s URL.</p></section>
  <section class="card"><div class="eyebrow">Export</div><h2>Build the complete PDF</h2>
  <p class="muted" id="exportNote">Pending and rejected edits use the original wording.</p>
  <div class="actions"><button class="primary" id="exportPdf">Export accepted PDF</button>
  <a class="button secondary" id="applySide" target="_blank" rel="noopener">Apply with Simplify</a></div>
  </section>
  <section class="card"><div class="eyebrow">Immutable master</div><h2>Full CV contents</h2>
  <div class="full-cv" id="fullCv">Loading…</div></section>
</aside></div></div><div id="toast"></div>
<script>
const token=localStorage.getItem("autoapply_bridge_token_v1")||"";
const params=new URLSearchParams(location.search);
const jobUrl=params.get("url")||"";
let state=null;
const $=id=>document.getElementById(id);
function text(tag,value,cls=""){const node=document.createElement(tag);node.textContent=value;
 if(cls)node.className=cls;return node}
function toast(message){$("toast").textContent=message;$("toast").style.display="block";
 setTimeout(()=>$("toast").style.display="none",2400)}
function notice(message,type=""){const box=$("notice");box.replaceChildren();
 if(!message)return;box.append(text("div",message,"notice "+type))}
async function api(path,options={}){
 const response=await fetch(path,{...options,headers:{"Content-Type":"application/json",
 "X-Autoapply-Token":token,...(options.headers||{})}});
 const result=await response.json();if(!response.ok)throw new Error(result.error||`Local helper returned ${response.status}`);
 return result
}
function renderMaster(){
 const doc=state.document,root=$("fullCv");root.replaceChildren();
 const summary=document.createElement("p");summary.className="muted";
 summary.append(document.createTextNode(doc.summary||"No summary"));
 const summaryEdit=text("button","edit","mini-edit");
 summaryEdit.onclick=()=>addManualPatch("summary",doc.summary);summary.append(summaryEdit);root.append(summary);
 for(const section of doc.sections){const wrap=document.createElement("div");wrap.className="cv-section";
  wrap.append(text("h3",section.name));
  for(const entry of section.entries){const block=document.createElement("div");block.className="cv-entry";
   block.append(text("strong",[entry.title,entry.organization].filter(Boolean).join(" · ")));
   const ul=document.createElement("ul");for(const bullet of entry.bullets){const li=document.createElement("li");
    li.append(document.createTextNode(bullet.text));const edit=text("button","edit","mini-edit");
    edit.onclick=()=>addManualPatch(bullet.id,bullet.text);li.append(edit);ul.append(li)}
   block.append(ul);wrap.append(block)}root.append(wrap)}
}
function addManualPatch(id,original){
 if(id==="summary"){
  state.draft.summary=state.draft.summary||{id,original,proposal:original,rationale:"Manual edit",keywords:[],status:"pending"};
 }else{
  state.draft.bullets=state.draft.bullets||{};
  state.draft.bullets[id]=state.draft.bullets[id]||{id,original,proposal:original,rationale:"Manual edit",keywords:[],status:"pending"};
 }
 renderSuggestions();saveDraft();window.scrollTo({top:0,behavior:"smooth"});toast("Editable patch added");
}
function patchCard(patch,label){
 const card=document.createElement("article");card.className="suggestion "+(patch.status||"pending");
 const head=document.createElement("div");head.className="suggestion-head";
 head.append(text("span",label,"label"),text("span",patch.id==="summary"?"Summary":patch.id,"pill"));card.append(head);
 const diff=document.createElement("div");diff.className="diff";
 const before=document.createElement("div");before.append(text("small","Original"));
 const original=document.createElement("textarea");original.className="original";original.readOnly=true;
 original.value=patch.original;before.append(original);
 const after=document.createElement("div");after.append(text("small","M3 suggestion — directly editable"));
 const proposal=document.createElement("textarea");proposal.className="proposal";proposal.value=patch.proposal;
 proposal.maxLength=600;proposal.addEventListener("change",()=>{patch.proposal=proposal.value;saveDraft()});
 after.append(proposal);diff.append(before,after);card.append(diff);
 if(patch.rationale)card.append(text("p",patch.rationale,"rationale"));
 if(patch.keywords?.length){const keys=document.createElement("div");keys.className="keywords";
  for(const keyword of patch.keywords)keys.append(text("i",keyword));card.append(keys)}
 const actions=document.createElement("div");actions.className="actions";
 const accept=text("button","Accept edit","secondary choice");accept.classList.toggle("active",patch.status==="accepted");
 const keep=text("button","Keep original","ghost choice keep");keep.classList.toggle("active",patch.status==="rejected");
 accept.onclick=()=>{patch.status="accepted";renderSuggestions();saveDraft()};
 keep.onclick=()=>{patch.status="rejected";renderSuggestions();saveDraft()};
 actions.append(accept,keep);card.append(actions);return card
}
function renderSuggestions(){
 const root=$("suggestions");root.replaceChildren();const draft=state.draft||{};
 const values=[];if(draft.summary)values.push([draft.summary,"Profile summary"]);
 for(const patch of Object.values(draft.bullets||{}))values.push([patch,"Experience bullet"]);
 if(!values.length){root.append(text("div","No suggestions yet. Add an instruction if you want, then ask M3 to compare the role against your full CV.","empty"));
  $("acceptAll").disabled=true;return}
 for(const [patch,label] of values)root.append(patchCard(patch,label));
 $("acceptAll").disabled=false;
 const accepted=values.filter(([p])=>p.status==="accepted").length;
 $("exportNote").textContent=`${accepted} accepted edit${accepted===1?"":"s"} will be applied. Everything else remains original.`;
 const rejected=Object.keys(draft.rejected_by_validator||{}).length;
 notice(rejected?`${rejected} unsafe or unsupported model suggestion${rejected===1?" was":"s were"} automatically discarded.`:"");
}
async function saveDraft(){
 try{state.draft.instructions=$("instructions").value;
  const result=await api("/api/draft",{method:"POST",body:JSON.stringify({url:jobUrl,draft:state.draft})});
  state.draft=result.draft}catch(error){notice(error.message,"error")}
}
async function generate(){
 $("generate").disabled=true;$("busy").classList.add("show");notice("");
 try{const result=await api("/api/suggest",{method:"POST",body:JSON.stringify({
  url:jobUrl,instructions:$("instructions").value})});state.draft=result.draft;
  $("instructions").value=state.draft.instructions||"";renderSuggestions();toast("New safe suggestions are ready")}
 catch(error){notice(error.message,"error")}finally{$("generate").disabled=false;$("busy").classList.remove("show")}
}
async function saveKey(){
 const key=$("keyInput").value;try{await api("/api/settings/minimax",{method:"POST",
  body:JSON.stringify({api_key:key})});$("keyInput").value="";state.minimax_configured=true;
  renderKey();toast("MiniMax key saved privately")}catch(error){notice(error.message,"error")}
}
function renderKey(){
 $("keyStatus").textContent=state.minimax_configured?
 "Configured ✓ Paste a new key below only if you need to replace it.":"Not configured. Paste your key once.";
 $("keyStatus").className=state.minimax_configured?"ok":"muted";
 $("keyInput").placeholder=state.minimax_configured?"Paste replacement MiniMax key":"Paste MiniMax API key";
 $("saveKey").textContent=state.minimax_configured?"Replace saved key":"Save key locally";
}
async function exportPdf(){
 $("exportPdf").disabled=true;try{await saveDraft();
  const result=await api("/api/export",{method:"POST",body:JSON.stringify({url:jobUrl})});
  const link=document.createElement("a");link.href=result.resume_download_url;link.download="";
  document.body.append(link);link.click();link.remove();toast(`Full CV exported with ${result.accepted_patch_count} accepted edits`)}
 catch(error){notice(error.message,"error")}finally{$("exportPdf").disabled=false}
}
async function init(){
 if(token.length<32){notice("Browser connection missing. Open start-autoapply.command once, then retry.","error");return}
 if(!jobUrl){notice("No job URL was supplied.","error");return}
 try{state=await api(`/api/editor?url=${encodeURIComponent(jobUrl)}`);
  $("jobTitle").textContent=`${state.job.role} · ${state.job.company}`;
  $("jobMeta").textContent=[state.job.location,state.job.description?"job description ready":"description loads when M3 runs"].filter(Boolean).join(" · ");
  $("factCount").textContent=`${state.document.fact_ids.length} verified facts`;
  $("applyTop").href=$("applySide").href=state.job.application_url;
  $("instructions").value=state.draft.instructions||"";renderKey();renderMaster();renderSuggestions()}
 catch(error){notice(error.message,"error")}
}
$("generate").onclick=generate;$("saveKey").onclick=saveKey;$("exportPdf").onclick=exportPdf;
$("acceptAll").onclick=()=>{if(state.draft.summary)state.draft.summary.status="accepted";
 for(const patch of Object.values(state.draft.bullets||{}))patch.status="accepted";
 renderSuggestions();saveDraft()};
init();
</script></body></html>"""
