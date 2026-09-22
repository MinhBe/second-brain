#!/usr/bin/env bash
set -Eeuo pipefail

# Canonical browser setup for Hermes on Ubuntu.
# Goal:
# - one persistent Chrome user-data-dir for ChatGPT auth/session state
# - one fixed profile directory (Default), never a random/no-account profile
# - one fixed local CDP port
# - chrome-real always connects with --browser-url (never --autoConnect)
# - no recurring "Allow remote debugging?" consent dialog
# - automatic Chrome restart through a user systemd service
#
# Usage:
#   bash install_persistent_chatgpt_browser.sh 'https://chatgpt.com/c/<conversation-id>'
#
# The only unavoidable manual action is the FIRST ChatGPT login in this dedicated
# Chrome profile. After that, cookies/local storage/session data persist in
# ~/.hermes/chrome-real-profile until ChatGPT itself expires/revokes the session.

TARGET_URL="${1:-https://chatgpt.com/}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CONFIG="$HERMES_HOME/config.yaml"
PROFILE_ROOT="$HERMES_HOME/chrome-real-profile"
PROFILE_DIR="Default"
PORT="${HERMES_CHROME_CDP_PORT:-9222}"
CDP_URL="http://127.0.0.1:$PORT"
BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/hermes-chrome-real"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE="$SERVICE_DIR/hermes-chrome-real.service"

mkdir -p "$HERMES_HOME/logs" "$BIN_DIR" "$SERVICE_DIR"

say() {
  echo
  echo "================================================================"
  echo "$1"
  echo "================================================================"
}

say "HERMES PERSISTENT CHATGPT BROWSER"

CHROME_BIN=""
for b in google-chrome google-chrome-stable chromium chromium-browser; do
  if command -v "$b" >/dev/null 2>&1; then
    CHROME_BIN="$(command -v "$b")"
    break
  fi
done
[[ -n "$CHROME_BIN" ]] || { echo "[FAIL] Chrome/Chromium not found"; exit 1; }
echo "[PASS] Chrome: $CHROME_BIN"

cat >"$LAUNCHER" <<'LAUNCHER'
#!/usr/bin/env bash
set -Eeuo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
PROFILE_ROOT="$HERMES_HOME/chrome-real-profile"
PROFILE_DIR="Default"
PORT="${HERMES_CHROME_CDP_PORT:-9222}"
CDP_URL="http://127.0.0.1:$PORT"
START_URL="${HERMES_CHROME_START_URL:-https://chatgpt.com/}"
LOG="$HERMES_HOME/logs/chrome-real-service.log"

mkdir -p "$PROFILE_ROOT" "$HERMES_HOME/logs"

CHROME_BIN=""
for b in google-chrome google-chrome-stable chromium chromium-browser; do
  if command -v "$b" >/dev/null 2>&1; then
    CHROME_BIN="$(command -v "$b")"
    break
  fi
done
[[ -n "$CHROME_BIN" ]] || exit 127

cdp_live() {
  python3 - "$CDP_URL" >/dev/null 2>&1 <<'PY'
import json, sys, urllib.request
with urllib.request.urlopen(sys.argv[1] + "/json/version", timeout=2) as r:
    j=json.load(r)
assert j.get("webSocketDebuggerUrl")
PY
}

# If the dedicated browser already exists, keep this service alive as its watchdog.
if cdp_live; then
  while cdp_live; do sleep 10; done
  exit 1
fi

# Never inherit an SSH/MobaXterm forwarded DISPLAY. Resolve the real desktop session.
GUI_PID=""
for _ in $(seq 1 120); do
  for proc in gnome-shell plasmashell; do
    GUI_PID="$(pgrep -u "$(id -u)" -n "$proc" 2>/dev/null || true)"
    [[ -n "$GUI_PID" ]] && break 2
  done
  sleep 1
done
[[ -n "$GUI_PID" ]] || { echo "No graphical session" >>"$LOG"; exit 1; }

ENV_FILE="/proc/$GUI_PID/environ"
[[ -r "$ENV_FILE" ]] || exit 1
getenv_gui() {
  tr '\0' '\n' < "$ENV_FILE" 2>/dev/null | sed -n "s/^$1=//p" | head -n 1
}

REAL_DISPLAY="$(getenv_gui DISPLAY)"
REAL_WAYLAND="$(getenv_gui WAYLAND_DISPLAY)"
REAL_XDG="$(getenv_gui XDG_RUNTIME_DIR)"
REAL_DBUS="$(getenv_gui DBUS_SESSION_BUS_ADDRESS)"
REAL_XAUTH="$(getenv_gui XAUTHORITY)"

if [[ -z "$REAL_XAUTH" ]]; then
  REAL_XAUTH="$(find "/run/user/$(id -u)" -maxdepth 1 -type f -name '.mutter-Xwaylandauth*' 2>/dev/null | head -n1 || true)"
fi

[[ -n "$REAL_DISPLAY" ]] || exit 1

export DISPLAY="$REAL_DISPLAY"
[[ -n "$REAL_WAYLAND" ]] && export WAYLAND_DISPLAY="$REAL_WAYLAND"
export XDG_RUNTIME_DIR="${REAL_XDG:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${REAL_DBUS:-unix:path=$XDG_RUNTIME_DIR/bus}"
[[ -n "$REAL_XAUTH" ]] && export XAUTHORITY="$REAL_XAUTH"

# IMPORTANT:
# - fixed non-default user-data-dir => Chrome permits remote-debugging-port
# - fixed profile-directory=Default => never falls into another/no-account profile
# - same directory every launch => ChatGPT cookies/session/local storage persist
exec "$CHROME_BIN" \
  --ozone-platform=x11 \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port="$PORT" \
  --user-data-dir="$PROFILE_ROOT" \
  --profile-directory="$PROFILE_DIR" \
  --no-first-run \
  --no-default-browser-check \
  --disable-session-crashed-bubble \
  --restore-last-session \
  "$START_URL" \
  >>"$LOG" 2>&1
LAUNCHER
chmod 700 "$LAUNCHER"

cat >"$SERVICE" <<EOF
[Unit]
Description=Hermes Persistent Authenticated Chrome
After=graphical-session.target

[Service]
Type=simple
Environment=HERMES_HOME=$HERMES_HOME
Environment=HERMES_CHROME_CDP_PORT=$PORT
Environment=HERMES_CHROME_START_URL=https://chatgpt.com/
ExecStart=$LAUNCHER
Restart=always
RestartSec=5
TimeoutStopSec=15

[Install]
WantedBy=default.target
EOF

echo "[PASS] Persistent launcher installed: $LAUNCHER"
echo "[PASS] User service installed: $SERVICE"
echo "[PASS] Persistent Chrome profile: $PROFILE_ROOT/$PROFILE_DIR"

# Permanently remove --autoConnect from chrome-real.
python3 - "$CONFIG" "$CDP_URL" <<'PY'
from pathlib import Path
import sys, yaml
p=Path(sys.argv[1]); cdp=sys.argv[2]
cfg=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
servers=cfg.setdefault("mcp_servers", {})
server=servers.get("chrome-real")
if not isinstance(server, dict):
    raise SystemExit("[FAIL] mcp_servers.chrome-real is missing")
args=server.get("args") or []
if not isinstance(args,list):
    raise SystemExit("[FAIL] chrome-real.args must be a list")
out=[]; i=0
while i < len(args):
    a=str(args[i]); lo=a.lower()
    if lo in ("--autoconnect","--auto-connect"):
        i+=1; continue
    if lo in ("--browser-url","--browserurl","--ws-endpoint","--wsendpoint"):
        i+=2; continue
    if lo.startswith(("--autoconnect=","--auto-connect=","--browser-url=","--browserurl=","--ws-endpoint=","--wsendpoint=")):
        i+=1; continue
    out.append(args[i]); i+=1
out.append("--browser-url="+cdp)
server["args"]=out
server["enabled"]=True
p.write_text(yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False),encoding="utf-8")
print("[PASS] chrome-real permanently uses", "--browser-url="+cdp)
PY

hermes config check >/dev/null
echo "[PASS] Hermes config valid"

# Stop only the dedicated browser from older ad-hoc runs, then let systemd own it.
systemctl --user stop hermes-chrome-real.service 2>/dev/null || true
pkill -u "$(id -u)" -f '[g]oogle-chrome.*chrome-real-profile' 2>/dev/null || true
pkill -u "$(id -u)" -f '[c]hromium.*chrome-real-profile' 2>/dev/null || true
sleep 2

systemctl --user daemon-reload
systemctl --user enable --now hermes-chrome-real.service

READY=0
for _ in $(seq 1 45); do
  if python3 - "$CDP_URL" >/dev/null 2>&1 <<'PY'
import json, sys, urllib.request
with urllib.request.urlopen(sys.argv[1]+"/json/version",timeout=2) as r:
    j=json.load(r)
assert j.get("webSocketDebuggerUrl")
PY
  then READY=1; break; fi
  sleep 1
done

if [[ "$READY" != "1" ]]; then
  echo "[FAIL] Persistent Chrome did not expose CDP"
  systemctl --user status hermes-chrome-real.service --no-pager -l || true
  tail -n 100 "$HERMES_HOME/logs/chrome-real-service.log" || true
  exit 1
fi

echo "[PASS] Persistent Chrome CDP is live: $CDP_URL"

# Open the exact requested thread through CDP without starting another profile/browser.
python3 - "$CDP_URL" "$TARGET_URL" <<'PY'
import json, sys, urllib.request, urllib.parse, time
base,target=sys.argv[1],sys.argv[2]
tid=target.rstrip("/").split("/")[-1] if "/c/" in target else ""
def pages():
    with urllib.request.urlopen(base+"/json/list",timeout=5) as r:
        return json.load(r)
if tid and any(tid in str(p.get("url","")) for p in pages() if isinstance(p,dict)):
    print("[PASS] Target ChatGPT thread already open")
    raise SystemExit(0)
req=urllib.request.Request(base+"/json/new?"+urllib.parse.quote(target,safe=":/"),method="PUT")
with urllib.request.urlopen(req,timeout=8) as r: r.read()
time.sleep(2)
print("[PASS] Requested ChatGPT page opened in persistent profile")
PY

say "ONE-TIME LOGIN CHECK"
echo "Look at the Chrome window on the Ubuntu desktop."
echo
echo "This is now the ONLY Chrome profile Hermes will control:"
echo "  $PROFILE_ROOT/$PROFILE_DIR"
echo
echo "If ChatGPT is already logged in, do nothing."
echo "If it is not logged in, log in ONCE in this window."
echo "Chrome will keep the session/cookies/local storage in this persistent profile."
echo
echo "You should NOT get the recurring 'Allow remote debugging?' consent dialog"
echo "because chrome-real no longer uses --autoConnect."
echo
read -r -p "When the target ChatGPT conversation is visible and logged in, press ENTER once... " _

say "RUNTIME VALIDATION"

python3 - "$CDP_URL" "$TARGET_URL" <<'PY'
import json,sys,urllib.request
base,target=sys.argv[1],sys.argv[2]
tid=target.rstrip("/").split("/")[-1] if "/c/" in target else ""
with urllib.request.urlopen(base+"/json/list",timeout=5) as r:
    pages=json.load(r)
print("[PASS] CDP pages:",len(pages))
if tid:
    matches=[p for p in pages if tid in str(p.get("url",""))]
    print("[PASS] Exact target thread tabs:",len(matches))
    if not matches:
        raise SystemExit("[FAIL] Exact target thread is not open")
PY

timeout 60s hermes mcp test chrome-real

echo
echo "[PASS] Persistent browser infrastructure is ready."
echo "[PASS] Service: hermes-chrome-real.service"
echo "[PASS] Profile: $PROFILE_ROOT/$PROFILE_DIR"
echo "[PASS] chrome-real: $CDP_URL"
echo
echo "The Chrome banner 'Chrome is being controlled by automated test software' is normal."
echo "It is NOT an authorization prompt and requires no action."
