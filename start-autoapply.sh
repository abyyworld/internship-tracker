#!/usr/bin/env bash
# Linux: install the CV helper so it starts with your session, and open it.
#
# The same idea as start-autoapply.command on macOS. It installs a systemd user
# service (or an autostart entry where systemd is absent), so the helper comes
# back at every login and this window can be closed.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"
PORT=8765

if [[ ! -x ".venv/bin/python" ]] || ! ".venv/bin/python" -c "import yaml, requests" 2>/dev/null; then
  echo "Setting up the local Python environment (this is a one-time step)…"
  python3 -m venv .venv --clear
  ".venv/bin/pip" install --quiet --upgrade pip
  ".venv/bin/pip" install --quiet -r requirements-autoapply.txt
fi

# Nothing else may hold the port the service is about to bind.
pkill -f "autoapply bridge" 2>/dev/null || true
sleep 1

# This also brings the checkout up to date before installing: a service pointed
# at stale code is the failure the whole thing exists to end.
echo "Updating the code and installing the CV helper as a background service…"
".venv/bin/python" -m autoapply install-service --human

for _ in $(seq 1 15); do
  if [[ -f "private/bridge.token" ]]; then
    TOKEN="$(cat private/bridge.token)"
    if curl -fsS -H "X-Autoapply-Token: $TOKEN" "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
      command -v xdg-open >/dev/null 2>&1 && xdg-open "http://127.0.0.1:$PORT/connect#$TOKEN" >/dev/null 2>&1 || true
      command -v xclip >/dev/null 2>&1 && printf '%s' "$TOKEN" | xclip -selection clipboard 2>/dev/null || true
      command -v wl-copy >/dev/null 2>&1 && printf '%s' "$TOKEN" | wl-copy 2>/dev/null || true
      echo ""
      echo "Done. The CV editor is running and will start with your session."
      echo "Open it at http://127.0.0.1:$PORT/connect#$TOKEN"
      echo "You can close this window — the editor keeps running without it."
      exit 0
    fi
  fi
  sleep 1
done

echo "The service did not answer. Its output is in private/bridge.log:"
tail -n 12 private/bridge.log 2>/dev/null || true
exit 1
