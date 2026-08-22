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

# A bridge is started once and left running for weeks while the checkout moves
# on, so "already running" was quietly answering the editor from code that is no
# longer on disk — and every symptom then belonged to a version nobody has. The
# build it reports is compared with the build in the working copy, and a stale
# process is replaced rather than reused.
if [[ -f "private/bridge.token" ]]; then
  BRIDGE_TOKEN="$(<private/bridge.token)"
  HEALTH="$(curl -fsS -H "X-Autoapply-Token: $BRIDGE_TOKEN" \
      "http://127.0.0.1:8765/health" 2>/dev/null || true)"
  if [[ -n "$HEALTH" ]]; then
    RUNNING_BUILD="$(printf '%s' "$HEALTH" | sed -n 's/.*"build": *"\([^"]*\)".*/\1/p')"
    CHECKOUT_BUILD="$(".venv/bin/python" -c \
      'from autoapply.openai_tailoring import BUILD; print(BUILD)' 2>/dev/null || true)"
    if [[ -n "$RUNNING_BUILD" && "$RUNNING_BUILD" == "$CHECKOUT_BUILD" ]]; then
      print -rn -- "$BRIDGE_TOKEN" | pbcopy
      open "http://127.0.0.1:8765/connect#$BRIDGE_TOKEN"
      echo "Autoapply is already running (build $RUNNING_BUILD)."
      echo "The dashboard is opening and the private token is on your clipboard."
      sleep 2
      exit 0
    fi
    echo "The running helper is out of date:"
    echo "  running  : ${RUNNING_BUILD:-unknown (a version from before this check)}"
    echo "  on disk  : ${CHECKOUT_BUILD:-unknown}"
    echo "Stopping it so this window serves the current code…"
    # Only this project's bridge, and only if it is ours to stop.
    pkill -f "python -m autoapply bridge" 2>/dev/null || true
    pkill -f "autoapply/__main__.py bridge" 2>/dev/null || true
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      curl -fsS -H "X-Autoapply-Token: $BRIDGE_TOKEN" \
        "http://127.0.0.1:8765/health" >/dev/null 2>&1 || break
      sleep 1
    done
  fi
fi

# Left as a window, the helper dies with the window — which is why the CV
# editor stopped working the moment this was closed. Unless a window is asked
# for explicitly, hand over to the installer: it puts the helper behind a login
# service that starts itself and survives a reboot, and this window can go.
WANT_WINDOW=""
for ARG in "$@"; do
  [[ "$ARG" == "--window" || "$ARG" == "-w" ]] && WANT_WINDOW="yes"
done

if [[ -z "$WANT_WINDOW" && -x "./install-login-service.command" ]]; then
  echo "Setting the CV helper up to start by itself, so this does not have to be"
  echo "done again. Run this with --window for a one-off helper in a window."
  echo ""
  exec "./install-login-service.command"
fi

echo "Starting the private CV helper…"
echo "Keep this window open while applying. Press Control-C to stop."
if [[ -z "$WANT_WINDOW" ]]; then
  echo "(install-login-service.command is not in this folder, so it cannot be"
  echo " installed as a background service yet.)"
fi
(sleep 2; [[ -f "private/bridge.token" ]] && BRIDGE_TOKEN="$(<private/bridge.token)" && print -rn -- "$BRIDGE_TOKEN" | pbcopy && open "http://127.0.0.1:8765/connect#$BRIDGE_TOKEN") &
exec ".venv/bin/python" -m autoapply bridge
