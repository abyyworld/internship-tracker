// ==UserScript==
// @name         Legacy Basic Application Autofill Template
// @namespace    internship-watcher.local
// @version      1.1
// @description  Fills basic contact and education text fields only. It never answers screening/EEO questions or submits an application.
// @match        *://boards.greenhouse.io/*
// @match        *://job-boards.greenhouse.io/*
// @match        *://*.greenhouse.io/*
// @match        *://jobs.lever.co/*
// @match        *://jobs.ashbyhq.com/*
// @match        *://*.ashbyhq.com/*
// @grant        none
// @run-at       document-idle
// ==/UserScript==

/*
  LEGACY TEMPLATE

  The guarded `python -m autoapply` workflow is recommended for supported ATS
  sites. This small userscript remains available for basic contact fields only.

  HOW TO USE:
  1. Install the free "Tampermonkey" extension (Chrome/Edge/Firefox/Safari).
  2. Copy this file to `autofill.local.user.js`. That filename is gitignored.
  3. Edit the PROFILE block in the private copy, then paste that copy into a new
     Tampermonkey script.
  4. Open any Greenhouse / Lever / Ashby application page. A blue "Autofill" button
     appears bottom-right. Click it. Review every field. Attach your CV (browsers
     block auto-attaching files for security). Click the site's own Submit.

  It intentionally does not fill dropdowns, radio buttons, checkboxes, work
  authorisation, sponsorship, citizenship, legal, salary, consent, demographic,
  disability, veteran, or other EEO fields. It never clicks Submit.
*/

const PROFILE = {
  firstName:  "",
  preferredName: "",
  lastName:   "",
  fullName:   "",
  email:      "",
  phone:      "",
  linkedin:   "",
  github:     "",
  website:    "",
  location:   "",
  city:       "",
  school:     "",
  degree:     "",
  discipline: "",
  gradMonth:  "",
  gradYear:   "",
};

// Narrow label patterns only. First match wins, including an intentionally
// blank value, so a broader rule cannot fill the wrong field.
const RULES = [
  [/^preferred name\b/, PROFILE.preferredName],
  [/^(first|given|legal first)\s*name\b/, PROFILE.firstName],
  [/^(last|family|legal last|surname)\s*name\b|^surname\b/, PROFILE.lastName],
  [/^(full |legal )?name\b|^candidate name\b/, PROFILE.fullName],
  [/^(email|e-mail)\b/, PROFILE.email],
  [/^(phone|mobile|telephone)\s+(country|region|code)\b/, ""],
  [/^(phone|mobile|telephone)\b/, PROFILE.phone],
  [/\blinkedin\b/, PROFILE.linkedin],
  [/\bgithub\b|\bgit hub\b/, PROFILE.github],
  [/^(portfolio|website|personal website|personal site)\b/, PROFILE.website],
  [/^city\b/, PROFILE.city],
  [/^(location|current location|where are you based)\b/, PROFILE.location],
  [/^(school|university|college|institution)( name)?\b/, PROFILE.school],
  [/^(degree|degree type|qualification)\b/, PROFILE.degree],
  [/^(discipline|major|field of study|course of study)\b/, PROFILE.discipline],
  [/^(expected )?(graduation|graduate).*\bmonth\b.*\byear\b/,
    (PROFILE.gradMonth + " " + PROFILE.gradYear).trim()],
  [/^(expected )?(graduation|graduate).*\bmonth\b/, PROFILE.gradMonth],
  [/^(expected )?(graduation|graduate).*\byear\b/, PROFILE.gradYear],
];

// Never autofill these even when an ATS renders them as text inputs.
const SENSITIVE_LABELS = [
  "authorized to work", "authorised to work", "right to work",
  "eligible to work", "sponsorship", "visa", "immigration",
  "citizen", "citizenship", "nationality", "export control", "clearance",
  "gender", "sex", "sexual orientation", "pronoun", "race", "ethnic",
  "hispanic", "latino", "veteran", "disability", "demographic",
  "religion", "date of birth", "age", "salary", "compensation",
  "criminal", "conviction", "consent", "signature",
];

function labelText(el) {
  let t = "";
  if (el.id) {
    const lab = document.querySelector('label[for="' + CSS.escape(el.id) + '"]');
    if (lab) t += " " + lab.textContent;
  }
  if (el.getAttribute("aria-label")) t += " " + el.getAttribute("aria-label");
  if (el.placeholder) t += " " + el.placeholder;
  if (el.name) t += " " + el.name;
  // climb to a wrapping label or nearby label/legend
  let p = el.closest("label, .field, .application-field, div");
  if (p) {
    const l = p.querySelector("label, legend, .label");
    if (l) t += " " + l.textContent;
  }
  return t.toLowerCase().replace(/\s+/g, " ").trim();
}

function setNativeValue(el, value) {
  const proto = el.tagName === "TEXTAREA"
    ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
  const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
  setter.call(el, value);
  el.dispatchEvent(new Event("input", { bubbles: true }));
  el.dispatchEvent(new Event("change", { bubbles: true }));
}

function fillText(el) {
  if (!el.value && el.type !== "hidden" && !el.disabled) {
    const lab = labelText(el);
    if (SENSITIVE_LABELS.some(key => lab.includes(key))) return false;
    for (const [pattern, val] of RULES) {
      if (pattern.test(lab)) {
        if (val) { setNativeValue(el, val); return true; }
        return false;
      }
    }
  }
  return false;
}

function run() {
  let n = 0;
  document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], input[type="url"], input:not([type]), textarea')
    .forEach(el => { if (fillText(el)) n++; });
  toast(n ? ("Filled " + n + " fields. Review, attach your CV, then submit.")
          : "No matching fields found on this page. Fill manually.");
}

function toast(msg) {
  let t = document.getElementById("__af_toast");
  if (!t) {
    t = document.createElement("div"); t.id = "__af_toast";
    t.style.cssText = "position:fixed;bottom:78px;right:20px;z-index:2147483647;" +
      "background:#111;color:#fff;padding:10px 14px;border-radius:8px;font:13px sans-serif;" +
      "max-width:280px;box-shadow:0 4px 14px rgba(0,0,0,.3)";
    document.body.appendChild(t);
  }
  t.textContent = msg;
  clearTimeout(t._h); t._h = setTimeout(() => t.remove(), 6000);
}

function addButton() {
  if (document.getElementById("__af_btn")) return;
  const b = document.createElement("button");
  b.id = "__af_btn"; b.textContent = "Autofill";
  b.style.cssText = "position:fixed;bottom:20px;right:20px;z-index:2147483647;" +
    "background:#4f8cff;color:#fff;border:none;padding:12px 18px;border-radius:10px;" +
    "font:600 14px sans-serif;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.3)";
  b.onclick = run;
  document.body.appendChild(b);
}

addButton();
new MutationObserver(addButton).observe(document.documentElement, { childList: true, subtree: true });
