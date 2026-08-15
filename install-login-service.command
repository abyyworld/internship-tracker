#!/bin/zsh
# Double-click once. The CV editor then runs by itself, from now on.
#
# macOS starts the helper at login and restarts it if it ever stops, so there is
# no window to keep open and nothing to remember. Double-click this again after
# updating the code, or moving the project folder, and it re-points at the copy
# it is sitting in.

set -euo pipefail

PROJECT_DIR="${0:A:h}"
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
mkdir -p "$AGENTS" "private"
# & < > are legal in a folder name and would otherwise break the XML.
xml_escape() {
  printf '%s' "$1" | sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'
}
SAFE_DIR="$(xml_escape "$PROJECT_DIR")"
cat > "$PLIST" <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>$LABEL</string>
	<key>ProgramArguments</key>
	<array>
		<string>$SAFE_DIR/.venv/bin/python</string>
		<string>-m</string>
		<string>autoapply</string>
		<string>bridge</string>
	</array>
	<key>WorkingDirectory</key>
	<string>$SAFE_DIR</string>
	<key>RunAtLoad</key>
	<true/>
	<key>KeepAlive</key>
	<true/>
	<key>ProcessType</key>
	<string>Background</string>
	<key>StandardOutPath</key>
	<string>$SAFE_DIR/private/bridge.log</string>
	<key>StandardErrorPath</key>
	<string>$SAFE_DIR/private/bridge.log</string>
</dict>
</plist>
PLISTEOF

launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST" 2>/dev/null || launchctl load -w "$PLIST"
line "Installed: $PLIST"

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
