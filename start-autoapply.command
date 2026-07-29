#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h}"
cd "$PROJECT_DIR"

# Recreate the venv if it is missing or broken (e.g. after moving the project folder).
if [[ ! -x ".venv/bin/python" ]] || ! ".venv/bin/python" -c "import yaml, requests" 2>/dev/null; then
  echo "Setting up the local Python environment (this is a one-time step)…"
  python3 -m venv .venv --clear
  ".venv/bin/pip" install --quiet --upgrade pip
  ".venv/bin/pip" install --quiet -r requirements-autoapply.txt
  echo "Done."
fi

if [[ -f "private/bridge.token" ]]; then
  BRIDGE_TOKEN="$(<private/bridge.token)"
  if curl -fsS -H "X-Autoapply-Token: $BRIDGE_TOKEN" \
      "http://127.0.0.1:8765/health" >/dev/null 2>&1; then
    print -rn -- "$BRIDGE_TOKEN" | pbcopy
    open "http://127.0.0.1:8765/connect#$BRIDGE_TOKEN"
    echo "Autoapply is already running."
    echo "The dashboard is opening and the private token is on your clipboard."
    sleep 2
    exit 0
  fi
fi

echo "Starting the private CV helper…"
echo "Keep this window open while applying. Press Control-C to stop."
(sleep 2; [[ -f "private/bridge.token" ]] && BRIDGE_TOKEN="$(<private/bridge.token)" && print -rn -- "$BRIDGE_TOKEN" | pbcopy && open "http://127.0.0.1:8765/connect#$BRIDGE_TOKEN") &
exec ".venv/bin/python" -m autoapply bridge
