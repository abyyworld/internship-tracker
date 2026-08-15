// ==UserScript==
// @name         Tailor my CV: any job posting
// @namespace    internship-watcher.local
// @version      1.0.0
// @description  Read a job posting on any site and open it in the private local CV editor.
// @match        *://*/*
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_xmlhttpRequest
// @grant        GM_registerMenuCommand
// @connect      127.0.0.1
// @run-at       document-idle
// @noframes
// ==/UserScript==

// The tracker follows a few hundred boards. The job someone actually wants is
// routinely on none of them — a company careers page, a lab's own site, a link
// from a friend — and the editor only opened for postings the tracker already
// knew. This reads the posting off whatever page is open, hands it to the local
// helper, and opens the same editor for it.
//
// Nothing leaves the machine: the page text goes to 127.0.0.1 and nowhere else,
// and the button only appears on a page that reads like a job advert.

(function () {
  "use strict";

  const BRIDGE = "http://127.0.0.1:8765";
  const TOKEN_KEY = "autoapply_bridge_token_v1";
  const BUTTON_ID = "autoapply-tailor-anywhere";

  // Hosts that are always job pages, and words that make an ordinary page one.
  const ATS_HOSTS = [
    "greenhouse.io", "lever.co", "ashbyhq.com", "workday.com", "myworkdayjobs.com",
    "smartrecruiters.com", "workable.com", "jobvite.com", "icims.com", "teamtailor.com",
    "bamboohr.com", "recruitee.com", "personio.de", "join.com", "pinpointhq.com",
    "linkedin.com", "indeed.com", "glassdoor.com", "otta.com", "wellfound.com",
  ];
  const PATH_HINTS = [
    "/job", "/jobs/", "/career", "/careers", "/vacanc", "/opening", "/position",
    "/apply", "/opportunit", "/internship", "/graduate", "/phd", "/postdoc",
  ];
  const PAGE_WORDS = [
    "responsibilities", "qualifications", "what you'll do", "what you will do",
    "requirements", "about the role", "apply now", "job description",
    "who you are", "your profile", "we are looking for", "minimum qualifications",
  ];
  // Long enough that a listing page of one-line adverts does not qualify.
  const MIN_DESCRIPTION_CHARS = 600;

  function looksLikeAPosting() {
    const host = location.hostname.toLowerCase();
    if (ATS_HOSTS.some(suffix => host === suffix || host.endsWith(`.${suffix}`))) {
      return true;
    }
    const path = location.pathname.toLowerCase();
    const hinted = PATH_HINTS.some(hint => path.includes(hint));
    const text = (document.body ? document.body.innerText : "").toLowerCase();
    const words = PAGE_WORDS.filter(word => text.includes(word)).length;
    // A careers URL with advert language, or any page that reads like an advert
    // strongly enough that the URL does not matter.
    return (hinted && words >= 1) || words >= 3;
  }

  // ── Reading the posting ────────────────────────────────────────────────────

  function meta(...names) {
    for (const name of names) {
      const node =
        document.querySelector(`meta[property="${name}"]`) ||
        document.querySelector(`meta[name="${name}"]`);
      const value = node && node.content && node.content.trim();
      if (value) return value;
    }
    return "";
  }

  function fromJobPosting() {
    // Most boards publish schema.org/JobPosting, which is the posting as the
    // employer meant it rather than as the page happens to lay it out.
    for (const node of document.querySelectorAll('script[type="application/ld+json"]')) {
      let parsed;
      try { parsed = JSON.parse(node.textContent || "{}"); } catch (_error) { continue; }
      const items = Array.isArray(parsed) ? parsed : [parsed, ...(parsed["@graph"] || [])];
      for (const item of items) {
        if (!item || typeof item !== "object") continue;
        const type = item["@type"];
        const types = Array.isArray(type) ? type : [type];
        if (!types.includes("JobPosting")) continue;
        const location = item.jobLocation;
        const address =
          (Array.isArray(location) ? location[0] : location || {}).address || {};
        return {
          role: String(item.title || ""),
          company: String((item.hiringOrganization || {}).name || ""),
          location: [address.addressLocality, address.addressRegion, address.addressCountry]
            .filter(part => typeof part === "string" && part).join(", "),
          description: stripTags(String(item.description || "")),
        };
      }
    }
    return null;
  }

  function stripTags(html) {
    const holder = document.createElement("div");
    holder.innerHTML = html;
    return (holder.innerText || holder.textContent || "").trim();
  }

  function mainText() {
    // The densest block of prose on the page, which is the advert on every
    // layout tried, without needing a selector per employer.
    const candidates = [
      ...document.querySelectorAll(
        "article, main, [role='main'], #content, .content, .job, .job-description, " +
        "[class*='description' i], [class*='posting' i], [id*='description' i]"
      ),
    ];
    let best = "";
    for (const node of candidates) {
      const text = (node.innerText || "").trim();
      if (text.length > best.length) best = text;
    }
    const body = document.body ? (document.body.innerText || "").trim() : "";
    // A container that holds nearly the whole page is the page, not the advert;
    // but if nothing better exists, the page is what there is.
    return best.length >= MIN_DESCRIPTION_CHARS ? best : body;
  }

  function readPosting() {
    const structured = fromJobPosting();
    const heading = (document.querySelector("h1") || {}).innerText || "";
    const title = document.title || "";
    const role =
      (structured && structured.role) ||
      heading.trim() ||
      meta("og:title", "twitter:title") ||
      title.split(/[|·—–-]/)[0] ||
      "Role";
    const company =
      (structured && structured.company) ||
      meta("og:site_name") ||
      location.hostname.replace(/^www\./, "");
    const description =
      (structured && structured.description && structured.description.length >= MIN_DESCRIPTION_CHARS
        ? structured.description
        : mainText()) || "";
    return {
      url: location.href.split("#")[0],
      role: role.trim().slice(0, 200),
      company: company.trim().slice(0, 200),
      location: (structured && structured.location) || meta("og:locality") || "",
      description,
    };
  }

  // ── Talking to the local helper ────────────────────────────────────────────

  async function bridgeToken(force = false) {
    let token = force ? "" : await GM_getValue(TOKEN_KEY, "");
    if (!token) {
      token = (window.prompt(
        "Paste the private bridge token (private/bridge.token in the project " +
        "folder). It is stored in this browser only."
      ) || "").trim();
      if (token) await GM_setValue(TOKEN_KEY, token);
    }
    return token;
  }

  function post(path, body, token) {
    return new Promise((resolve, reject) => {
      GM_xmlhttpRequest({
        method: "POST",
        url: BRIDGE + path,
        headers: {"Content-Type": "application/json", "X-Autoapply-Token": token},
        data: JSON.stringify(body),
        timeout: 30000,
        onload(response) {
          let value = {};
          try { value = JSON.parse(response.responseText || "{}"); } catch (_error) {}
          if (response.status === 401) GM_setValue(TOKEN_KEY, "");
          if (response.status < 200 || response.status >= 300) {
            reject(new Error(value.error || `The helper returned HTTP ${response.status}`));
            return;
          }
          resolve(value);
        },
        onerror() {
          reject(new Error(
            "The local CV helper is not running. Double-click " +
            "start-autoapply.command in the project folder."
          ));
        },
        ontimeout() { reject(new Error("The local CV helper did not answer in time.")); },
      });
    });
  }

  // ── The button ─────────────────────────────────────────────────────────────

  function toast(message, isError) {
    let node = document.getElementById("autoapply-anywhere-toast");
    if (!node) {
      node = document.createElement("div");
      node.id = "autoapply-anywhere-toast";
      Object.assign(node.style, {
        position: "fixed", right: "18px", bottom: "70px", zIndex: "2147483647",
        maxWidth: "380px", padding: "11px 13px", borderRadius: "10px", color: "#fff",
        font: "13px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif",
        boxShadow: "0 8px 28px rgba(0,0,0,.3)",
      });
      document.body.appendChild(node);
    }
    node.style.background = isError ? "#b42318" : "#176f3a";
    node.textContent = message;
    node.hidden = false;
    window.setTimeout(() => { node.hidden = true; }, isError ? 9000 : 5000);
  }

  async function tailorThisPage(button) {
    const label = button ? button.textContent : "";
    if (button) { button.disabled = true; button.textContent = "Reading posting…"; }
    try {
      const posting = readPosting();
      if (!posting.url.startsWith("https://")) {
        throw new Error("Only pages served over HTTPS can be tailored for.");
      }
      const token = await bridgeToken();
      if (!token) throw new Error("No bridge token was entered.");
      const result = await post("/api/adopt", posting, token);
      window.open(result.editor_url, "_blank", "noopener");
      toast(
        `Opened the CV editor for ${result.job.role} at ${result.job.company} ` +
        `(${result.job.description_chars.toLocaleString()} characters of advert).`
      );
    } catch (error) {
      toast(error.message || String(error), true);
    } finally {
      if (button) { button.disabled = false; button.textContent = label; }
    }
  }

  function addButton() {
    if (document.getElementById(BUTTON_ID) || !document.body) return;
    const button = document.createElement("button");
    button.id = BUTTON_ID;
    button.type = "button";
    button.textContent = "✦ Tailor my CV";
    button.title = "Open this posting in the private local CV editor";
    Object.assign(button.style, {
      position: "fixed", right: "18px", bottom: "18px", zIndex: "2147483646",
      padding: "9px 14px", borderRadius: "999px", border: "1px solid #25b875",
      background: "#0c1714", color: "#70efad", cursor: "pointer",
      font: "600 13px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif",
      boxShadow: "0 6px 22px rgba(0,0,0,.34)", opacity: "0.92",
    });
    button.addEventListener("mouseenter", () => { button.style.opacity = "1"; });
    button.addEventListener("mouseleave", () => { button.style.opacity = "0.92"; });
    button.addEventListener("click", () => tailorThisPage(button));
    document.body.appendChild(button);
  }

  if (typeof GM_registerMenuCommand === "function") {
    // Always available, even when the page does not read like a posting.
    GM_registerMenuCommand("Tailor my CV for this page", () => tailorThisPage(null));
    GM_registerMenuCommand("Re-enter the bridge token", async () => {
      await bridgeToken(true);
    });
  }

  if (looksLikeAPosting()) addButton();
  // Job boards navigate without reloading, so the check is repeated when the
  // page changes rather than only at load.
  let lastUrl = location.href;
  new MutationObserver(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      const existing = document.getElementById(BUTTON_ID);
      if (existing) existing.remove();
      window.setTimeout(() => { if (looksLikeAPosting()) addButton(); }, 800);
    }
  }).observe(document.documentElement, {childList: true, subtree: true});
})();
