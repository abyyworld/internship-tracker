// ==UserScript==
// @name         Internship Tracker: Generate CV + Apply
// @namespace    internship-watcher.local
// @version      1.1.0
// @description  Generate a private role-specific CV locally, then open the employer page for Simplify.
// @match        https://github.com/*/internship-tracker*
// @match        https://abyyworld.github.io/internship-tracker/*
// @grant        GM_download
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// @run-at       document-idle
// ==/UserScript==

(function () {
  "use strict";

  const BRIDGE = "http://127.0.0.1:8765";
  const TOKEN_KEY = "autoapply_bridge_token_v1";
  const BUTTON_CLASS = "autoapply-cv-apply";
  const ATS_HOST_SUFFIXES = ["greenhouse.io", "lever.co", "ashbyhq.com"];

  function toast(message, error = false) {
    let node = document.getElementById("autoapply-toast");
    if (!node) {
      node = document.createElement("div");
      node.id = "autoapply-toast";
      Object.assign(node.style, {
        position: "fixed", right: "18px", bottom: "18px", zIndex: "2147483647",
        maxWidth: "430px", padding: "12px 14px", borderRadius: "9px",
        color: "#fff", font: "13px/1.4 -apple-system,BlinkMacSystemFont,sans-serif",
        boxShadow: "0 6px 24px rgba(0,0,0,.28)"
      });
      document.body.appendChild(node);
    }
    node.style.background = error ? "#b42318" : "#176f3a";
    node.textContent = message;
    node.hidden = false;
    window.setTimeout(() => { node.hidden = true; }, error ? 9000 : 5000);
  }

  async function bridgeToken(force = false) {
    let token = force ? "" : await GM_getValue(TOKEN_KEY, "");
    if (!token) {
      token = window.prompt(
        "Paste the private bridge token from private/bridge.token. " +
        "The background helper should already be running:"
      ) || "";
      token = token.trim();
      if (token) await GM_setValue(TOKEN_KEY, token);
    }
    return token;
  }

  function requestPrepare(url, token) {
    return new Promise((resolve, reject) => {
      GM_xmlhttpRequest({
        method: "POST",
        url: `${BRIDGE}/prepare`,
        headers: {
          "Content-Type": "application/json",
          "X-Autoapply-Token": token
        },
        data: JSON.stringify({url}),
        timeout: 120000,
        onload(response) {
          let value = {};
          try { value = JSON.parse(response.responseText || "{}"); } catch (_error) {}
          if (response.status === 401) {
            GM_setValue(TOKEN_KEY, "");
          }
          if (response.status < 200 || response.status >= 300) {
            reject(new Error(value.error || `Bridge returned HTTP ${response.status}`));
            return;
          }
          resolve(value);
        },
        onerror() {
          reject(new Error(
            "Local CV helper is not reachable. Open start-autoapply.command " +
            "from the internship watcher folder."
          ));
        },
        ontimeout() {
          reject(new Error("CV generation timed out. Check the bridge terminal."));
        }
      });
    });
  }

  async function generateAndApply(event, anchor, button) {
    event.preventDefault();
    event.stopPropagation();
    const applyTab = window.open("about:blank", "_blank");
    const oldText = button.textContent;
    button.disabled = true;
    button.textContent = "Generating CV…";
    try {
      const token = await bridgeToken();
      if (!token) throw new Error("Bridge token was not entered.");
      const result = await requestPrepare(anchor.href, token);
      GM_download({
        url: result.resume_download_url,
        name: `${result.company}-${result.role}.pdf`.replace(/[^A-Za-z0-9._-]+/g, "-"),
        saveAs: false,
        onerror() {
          toast("CV was generated, but the automatic download failed.", true);
        }
      });
      if (applyTab) {
        applyTab.location.replace(result.application_url);
      } else {
        window.open(result.application_url, "_blank", "noopener");
      }
      toast(
        `Tailored CV downloaded for ${result.company}. ` +
        `Simplify can now autofill the opened form; select the new PDF and review it.`
      );
      button.textContent = "CV ready ✓";
    } catch (error) {
      if (applyTab) applyTab.close();
      toast(error.message || String(error), true);
      button.textContent = oldText;
      button.disabled = false;
    }
  }

  function eligibleLink(anchor) {
    if (
      !anchor.href ||
      anchor.dataset.autoapplyEnhanced === "1" ||
      anchor.dataset.noAutoapply === "1"
    ) return false;
    let parsed;
    try { parsed = new URL(anchor.href); } catch (_error) { return false; }
    if (
      parsed.protocol !== "https:" ||
      !ATS_HOST_SUFFIXES.some(
        suffix => parsed.hostname === suffix || parsed.hostname.endsWith(`.${suffix}`)
      )
    ) return false;
    return Boolean(
      anchor.closest(
        "article.markdown-body, [data-testid='readme'], [data-autoapply-dashboard]"
      )
    );
  }

  function enhance() {
    document.querySelectorAll("a[href]").forEach(anchor => {
      if (!eligibleLink(anchor)) return;
      anchor.dataset.autoapplyEnhanced = "1";
      const button = document.createElement("button");
      button.type = "button";
      button.className = BUTTON_CLASS;
      button.textContent = "⚡ Generate CV + Apply";
      Object.assign(button.style, {
        marginLeft: "7px", padding: "2px 7px", border: "1px solid #1f883d",
        borderRadius: "6px", background: "#dafbe1", color: "#116329",
        cursor: "pointer", fontSize: "11px", fontWeight: "600"
      });
      button.addEventListener("click", event => generateAndApply(event, anchor, button));
      anchor.insertAdjacentElement("afterend", button);
    });
  }

  enhance();
  new MutationObserver(enhance).observe(document.documentElement, {
    childList: true, subtree: true
  });
})();
