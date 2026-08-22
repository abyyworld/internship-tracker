#!/bin/zsh
# Double-click once. The CV editor then runs by itself, from now on.
#
# macOS starts the helper at login and restarts it if it ever stops, so there is
# no window to keep open and nothing to remember. Double-click this again after
# updating the code, or moving the project folder, and it re-points at the copy
# it is sitting in.

set -euo pipefail

# Where the project actually is. Normally this file sits in it — but the whole
# point of a one-file installer is that it can be downloaded on its own, from a
# browser, by someone who does not want a terminal at all. Downloaded, it lands
# in ~/Downloads, so it goes looking for the checkout rather than installing a
# service that points at the Downloads folder.
find_project() {
  local here="${0:A:h}"
  local candidate
  if [[ -f "$here/autoapply/bridge.py" ]]; then
    print -r -- "$here"
    return 0
  fi
  for candidate in \
    "$HOME/Desktop/other projects/internship watcher" \
    "$HOME/Desktop/internship watcher" \
    "$HOME/Documents/internship watcher" \
    "$HOME/internship-tracker" \
    "$HOME/Desktop/internship-tracker"; do
    if [[ -f "$candidate/autoapply/bridge.py" ]]; then
      print -r -- "$candidate"
      return 0
    fi
  done
  candidate="$(find "$HOME/Desktop" "$HOME/Documents" "$HOME/Developer" "$HOME/Projects" \
    -maxdepth 4 -type f -path "*/autoapply/bridge.py" 2>/dev/null | head -1)"
  if [[ -n "$candidate" ]]; then
    print -r -- "${candidate:h:h}"
    return 0
  fi
  return 1
}

if ! PROJECT_DIR="$(find_project)"; then
  printf '%s\n' ""
  printf '%s\n' "Could not find the internship-watcher folder on this Mac."
  printf '%s\n' "Move this file into that folder and open it again."
  printf '%s\n' ""
  printf '%s\n' "Press Return to close this window."
  read -t 300 -r _ 2>/dev/null || true
  exit 1
fi
cd "$PROJECT_DIR"
LABEL="com.autoapply.bridge"
AGENTS="$HOME/Library/LaunchAgents"
PLIST="$AGENTS/$LABEL.plist"
PORT=8765
DOMAIN="gui/$(id -u)"

line() { printf '%s\n' "$1"; }
line ""
line "Installing the CV editor as a background service"
line "Project : $PROJECT_DIR"

# ── The code it will run ─────────────────────────────────────────────────────
# A service pointed at a stale checkout is the failure this whole file exists to
# end, so the checkout is brought up to date first. Nothing is discarded: local
# changes are parked with git stash and the command to restore them is printed.
if [[ -d ".git" ]] && command -v git >/dev/null 2>&1; then
  if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
    git stash push -u -m "autoapply install $(date +%Y-%m-%dT%H:%M:%S)" >/dev/null 2>&1 \
      && line "Parked  : local changes stashed — restore them with  git stash pop"
  fi
  if git fetch origin --quiet 2>/dev/null; then
    BEFORE="$(git rev-parse --short HEAD 2>/dev/null || true)"
    # Fast-forward what is checked out. Switching branches from a launcher would
    # move work out from under someone without asking.
    git pull --ff-only --quiet 2>/dev/null || true
    AFTER="$(git rev-parse --short HEAD 2>/dev/null || true)"
    if [[ "$BEFORE" != "$AFTER" ]]; then
      line "Updated : $BEFORE → $AFTER"
    else
      line "Code    : already current ($AFTER on $(git rev-parse --abbrev-ref HEAD 2>/dev/null))"
    fi
  else
    line "Offline : could not reach GitHub, installing the code already here"
  fi
fi

# ── The environment it will run in ───────────────────────────────────────────
if [[ ! -x ".venv/bin/python" ]] || ! ".venv/bin/python" -c "import yaml, requests" 2>/dev/null; then
  line "Setting up the local Python environment (this is a one-time step)…"
  python3 -m venv .venv --clear
  ".venv/bin/pip" install --quiet --upgrade pip
  ".venv/bin/pip" install --quiet -r requirements-autoapply.txt
fi

# ── Any older service, whatever it was called, stops owning port 8765 ────────
{ launchctl list 2>/dev/null || true; } | awk '/autoapply|internship/ {print $3}' \
  | while read -r OLD; do
      [ -z "$OLD" ] && continue
      [ "$OLD" = "$LABEL" ] && continue
      line "Removing : the older login service $OLD"
      launchctl bootout "$DOMAIN/$OLD" 2>/dev/null \
        || launchctl unload "$AGENTS/$OLD.plist" 2>/dev/null || true
      rm -f "$AGENTS/$OLD.plist"
    done

# ── Nothing else may hold the port the service is about to bind ─────────────
# A helper started by hand in a Terminal window owns 8765 just as firmly as a
# service does, and launchd would sit in a crash loop behind it.
pkill -f "autoapply bridge" 2>/dev/null || true
PIDS="$(lsof -ti "tcp:$PORT" 2>/dev/null || true)"
if [[ -n "$PIDS" ]]; then
  line "Stopping : the helper already running on port $PORT"
  printf '%s\n' "$PIDS" | while read -r PID; do kill "$PID" 2>/dev/null || true; done
fi
for _ in 1 2 3 4 5 6 7 8 9 10; do
  lsof -ti "tcp:$PORT" >/dev/null 2>&1 || break
  sleep 1
done

# ── The service itself ───────────────────────────────────────────────────────
# Written by autoapply's own installer, which knows how to do this on macOS,
# Linux and Windows. Keeping a second copy of the plist here is how the two
# drift apart.
mkdir -p "private"
INSTALLED_JSON="$(".venv/bin/python" -m autoapply install-service 2>&1)" || {
  line ""
  line "The service could not be installed:"
  printf '%s\n' "$INSTALLED_JSON"
  line ""
  line "Press Return to close this window."
  read -t 300 -r _ 2>/dev/null || true
  exit 1
}
line "Installed: $(printf '%s' "$INSTALLED_JSON" | sed -n 's/.*"file": *"\([^"]*\)".*/\1/p')"

# ── Prove it is answering, and pair the browser ──────────────────────────────
BUILD=""
for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  if [[ -f "private/bridge.token" ]]; then
    HEALTH="$(curl -fsS -H "X-Autoapply-Token: $(<private/bridge.token)" \
      "http://127.0.0.1:$PORT/health" 2>/dev/null || true)"
    if [[ -n "$HEALTH" ]]; then
      BUILD="$(printf '%s' "$HEALTH" | sed -n 's/.*"build": *"\([^"]*\)".*/\1/p')"
      break
    fi
  fi
  sleep 1
done

if [[ -z "$BUILD" ]]; then
  line ""
  line "The service did not answer within 15 seconds."
  line "Its output is in private/bridge.log — the last few lines:"
  tail -n 12 "private/bridge.log" 2>/dev/null || true
  line ""
  line "Press Return to close this window."
  read -t 300 -r _ 2>/dev/null || true
  exit 1
fi

BRIDGE_TOKEN="$(<private/bridge.token)"
printf '%s' "$BRIDGE_TOKEN" | pbcopy 2>/dev/null || true
open "http://127.0.0.1:$PORT/connect#$BRIDGE_TOKEN" 2>/dev/null || true

line ""
line "Done. The CV editor is running and will start itself at every login."
line "Build   : $BUILD"
line "Log     : $PROJECT_DIR/private/bridge.log"
line ""
line "You can close this window — the editor keeps running without it."
line "Nothing here needs a terminal again unless you move the project folder."
sleep 3
