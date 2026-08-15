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
# A login service is the one that survives every other attempt: killing the
# process just makes launchd start the same old copy again.
{ launchctl list 2>/dev/null || true; } | awk '/autoapply|internship/ {print $3}' \
  | while read -r LABEL; do
  [ -z "$LABEL" ] && continue
  line "Stopping: login service $LABEL"
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null \
    || launchctl unload "$HOME/Library/LaunchAgents/$LABEL.plist" 2>/dev/null \
    || true
done
pkill -f "autoapply bridge" 2>/dev/null || true
PIDS="$(lsof -ti "tcp:$PORT" 2>/dev/null || true)"
if [[ -n "$PIDS" ]]; then
  line "Stopping: process on port $PORT"
  printf '%s\n' "$PIDS" | while read -r PID; do kill "$PID" 2>/dev/null || true; done
fi
for _ in 1 2 3 4 5 6 7 8 9 10; do
  lsof -ti "tcp:$PORT" >/dev/null 2>&1 || break
  sleep 1
done

line ""
line "Starting the helper from this folder. Keep this window open."
line "If a login service was stopped above, this window is now the helper —"
line "closing it stops the CV editor until you run this again."
line ""
exec "./start-autoapply.command"
