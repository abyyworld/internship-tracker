#!/bin/zsh
# Make the running helper match this folder, and prove which code is serving.
#
# A bridge is started once and left running for weeks. The checkout moves on,
# a login service quietly respawns the old process, and the editor keeps being
# answered by code that is no longer on disk — so a fix that is pushed, pulled
# and tested still does not reach the browser. This does every step of that in
# one go and then says, out loud, which build ended up serving.
#
#   ./update-autoapply.command                 update the current branch
#   ./update-autoapply.command some-branch     switch to that branch first
#
# Nothing here discards work: local edits are parked with git stash and the
# command to bring them back is printed.

set -euo pipefail

PROJECT_DIR="${0:A:h}"
cd "$PROJECT_DIR"
BRANCH="${1:-}"
PORT=8765

line() { printf '%s\n' "$1"; }
line ""
line "Project : $PROJECT_DIR"

# ── What is answering right now, before anything changes ─────────────────────
if [[ -f "private/bridge.token" ]]; then
  RUNNING="$(curl -fsS -H "X-Autoapply-Token: $(<private/bridge.token)" \
    "http://127.0.0.1:$PORT/health" 2>/dev/null || true)"
  if [[ -n "$RUNNING" ]]; then
    RUNNING_BUILD="$(printf '%s' "$RUNNING" | sed -n 's/.*"build": *"\([^"]*\)".*/\1/p')"
    line "Serving : ${RUNNING_BUILD:-a build from before this check existed}"
  else
    line "Serving : nothing is listening on 127.0.0.1:$PORT"
  fi
fi

# ── Update the checkout, without destroying what the watcher has written ─────
line "Branch  : $(git rev-parse --abbrev-ref HEAD 2>/dev/null || print unknown)"
if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
  STAMP="autoapply update $(date +%Y-%m-%dT%H:%M:%S)"
  git stash push -u -m "$STAMP" >/dev/null
  line "Parked  : local changes stashed — restore them with  git stash pop"
fi
git fetch origin --quiet || line "Warning : could not reach GitHub; using what is already here"
if [[ -n "$BRANCH" ]]; then
  git checkout -B "$BRANCH" "origin/$BRANCH" \
    || line "Warning : GitHub has no branch called $BRANCH; staying on this one"
else
  git pull --ff-only --quiet \
    || line "Warning : could not fast-forward this branch; resolve it with git pull"
fi
line "Now at  : $(git log --oneline -1)"
ON_DISK="$(".venv/bin/python" -c \
  'from autoapply.openai_tailoring import BUILD; print(BUILD)' 2>/dev/null || true)"
line "On disk : ${ON_DISK:-unknown (the virtual environment may need rebuilding)}"

# ── Stop everything that could keep serving the old code ─────────────────────
# The helper is a background service, so updating it means restarting that
# service — not holding a terminal window open. Anything else claiming port
# 8765 is stopped first, including an older service pointing at a stale copy.
LABEL="com.autoapply.bridge"
DOMAIN="gui/$(id -u)"
INSTALLED=""
{ launchctl list 2>/dev/null || true; } | awk '/autoapply|internship/ {print $3}' \
  | while read -r OTHER; do
      [ -z "$OTHER" ] && continue
      [ "$OTHER" = "$LABEL" ] && continue
      line "Stopping: the older login service $OTHER"
      launchctl bootout "$DOMAIN/$OTHER" 2>/dev/null \
        || launchctl unload "$HOME/Library/LaunchAgents/$OTHER.plist" 2>/dev/null || true
    done
if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
  INSTALLED="yes"
fi

if [[ -z "$INSTALLED" ]]; then
  line ""
  line "The CV editor is not installed as a background service yet, so it only"
  line "runs while a window is open. Installing it now — after this you will not"
  line "need a terminal again."
  if [[ -x "./install-login-service.command" ]]; then
    exec "./install-login-service.command"
  fi
  line "install-login-service.command is not in this folder, so the helper will"
  line "run in this window instead. Keep it open."
  exec "./start-autoapply.command"
fi

pkill -f "autoapply bridge" 2>/dev/null || true
line "Restarting the background service with the code in this folder…"
launchctl kickstart -k "$DOMAIN/$LABEL" 2>/dev/null || {
  launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
  launchctl bootstrap "$DOMAIN" "$HOME/Library/LaunchAgents/$LABEL.plist" 2>/dev/null || true
}

SERVING=""
for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  if [[ -f "private/bridge.token" ]]; then
    HEALTH="$(curl -fsS -H "X-Autoapply-Token: $(<private/bridge.token)" \
      "http://127.0.0.1:$PORT/health" 2>/dev/null || true)"
    if [[ -n "$HEALTH" ]]; then
      SERVING="$(printf '%s' "$HEALTH" | sed -n 's/.*"build": *"\([^"]*\)".*/\1/p')"
      [[ -n "$SERVING" ]] && break
    fi
  fi
  sleep 1
done

line ""
if [[ -n "$SERVING" ]]; then
  line "Serving : $SERVING   ← the editor is now answering from this folder"
  BRIDGE_TOKEN="$(<private/bridge.token)"
  printf '%s' "$BRIDGE_TOKEN" | pbcopy 2>/dev/null || true
  open "http://127.0.0.1:$PORT/connect#$BRIDGE_TOKEN" 2>/dev/null || true
  line "The editor keeps running without this window. You can close it."
else
  line "The service did not answer. Its output is in private/bridge.log:"
  tail -n 12 "private/bridge.log" 2>/dev/null || true
fi
sleep 3
