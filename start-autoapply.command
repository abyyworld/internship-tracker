#!/bin/zsh
set -euo pipefail

PROJECT_DIR="${0:A:h}"
cd "$PROJECT_DIR"

if [[ ! -x ".venv/bin/python" ]]; then
  echo "The local Python environment is missing at:"
  echo "  $PROJECT_DIR/.venv"
  echo ""
  read "?Press Return to close."
  exit 1
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

if command -v brew >/dev/null 2>&1; then
  brew services start ollama >/dev/null 2>&1 || true
fi

echo "Starting the private CV helper…"
echo "Keep this window open while applying. Press Control-C to stop."
(sleep 2; [[ -f "private/bridge.token" ]] && BRIDGE_TOKEN="$(<private/bridge.token)" && print -rn -- "$BRIDGE_TOKEN" | pbcopy && open "http://127.0.0.1:8765/connect#$BRIDGE_TOKEN") &
exec ".venv/bin/python" -m autoapply bridge
