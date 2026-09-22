#!/usr/bin/env bash
set -Eeuo pipefail

# One-pass repair + validation for Hermes authenticated ChatGPT browser control.
# Usage:
#   bash Collection/WORKFLOW/repair_and_test_chatgpt_browser.sh \
#     'https://chatgpt.com/c/<conversation-id>'
#
# This script:
#   1) attaches to the real Ubuntu graphical session,
#   2) starts/reuses a dedicated persistent Chrome profile with CDP,
#   3) patches chrome-real to a fixed --browser-url,
#   4) ensures the exact ChatGPT thread is open,
#   5) installs the latest chatgpt-thread-controller skill,
#   6) runs one end-to-end Hermes test,
#   7) restores the gateway on exit.
#
# It intentionally does not expose the user's normal Chrome profile to CDP.

TARGET_URL="${1:-}"
if [[ ! "$TARGET_URL" =~ ^https://chatgpt\.com/c/[A-Za-z0-9-]+/?$ ]]; then
  echo "Usage: $0 'https://chatgpt.com/c/<conversation-id>'" >&2
  exit 2
fi
TARGET_URL="${TARGET_URL%/}"

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
CONFIG="$HERMES_HOME/config.yaml"
SKILL_SRC="$REPO_ROOT/Collection/SKILL/chatgpt-thread-controller"
SKILL_DST="$HERMES_HOME/skills/chatgpt-thread-controller"
CHROME_PROFILE="$HERMES_HOME/chrome-real-profile"
CHROME_LOG="$HERMES_HOME/logs/chrome-real.log"
CDP_PORT="${HERMES_CHATGPT_CDP_PORT:-9222}"
CDP_URL="http://127.0.0.1:$CDP_PORT"
TEST_LOG="$HERMES_HOME/logs/chatgpt-bridge-last-test.log"

mkdir -p "$HERMES_HOME/logs" "$HERMES_HOME/backups" "$HERMES_HOME/skills"

banner() {
  echo
  echo "================================================================"
  echo "$1"
  echo "================================================================"
}

restore_gateway() {
  banner "RESTORE HERMES GATEWAY"
  systemctl --user start hermes-gateway.service 2>/dev/null || true
  sleep 3
  systemctl --user is-active hermes-gateway.service 2>/dev/null || true
}
trap restore_gateway EXIT

banner "HERMES CHATGPT BROWSER — REPAIR + END-TO-END TEST"

# 1. Chrome binary
CHROME_BIN=""
for b in google-chrome google-chrome-stable chromium chromium-browser; do
  if command -v "$b" >/dev/null 2>&1; then
    CHROME_BIN="$(command -v "$b")"
    break
  fi
done
[[ -n "$CHROME_BIN" ]] || { echo "[FAIL] Chrome/Chromium not found"; exit 1; }
echo "[PASS] Chrome: $CHROME_BIN"

# 2. Real GUI environment, not SSH/MoTTY X11 forwarding.
GUI_PID=""
GUI_PROCESS=""
for proc in gnome-shell plasmashell; do
  GUI_PID="$(pgrep -u "$(id -u)" -n "$proc" 2>/dev/null || true)"
  if [[ -n "$GUI_PID" ]]; then GUI_PROCESS="$proc"; break; fi
done
[[ -n "$GUI_PID" ]] || { echo "[FAIL] No active Ubuntu desktop session"; exit 1; }
ENV_FILE="/proc/$GUI_PID/environ"
[[ -r "$ENV_FILE" ]] || { echo "[FAIL] Cannot read $ENV_FILE"; exit 1; }

get_gui_env() {
  tr '\0' '\n' < "$ENV_FILE" 2>/dev/null | sed -n "s/^$1=//p" | head -n 1
}
REAL_DISPLAY="$(get_gui_env DISPLAY)"
REAL_WAYLAND="$(get_gui_env WAYLAND_DISPLAY)"
REAL_XDG_RUNTIME="$(get_gui_env XDG_RUNTIME_DIR)"
REAL_DBUS="$(get_gui_env DBUS_SESSION_BUS_ADDRESS)"
REAL_XAUTH="$(get_gui_env XAUTHORITY)"

if [[ -z "$REAL_XAUTH" ]]; then
  for x in "/run/user/$(id -u)/gdm/Xauthority" "$HOME/.Xauthority"; do
    [[ -f "$x" ]] && { REAL_XAUTH="$x"; break; }
  done
fi
if [[ -z "$REAL_XAUTH" ]]; then
  REAL_XAUTH="$(find "/run/user/$(id -u)" -maxdepth 1 -type f -name '.mutter-Xwaylandauth*' 2>/dev/null | head -n 1 || true)"
fi

[[ -n "$REAL_DISPLAY" ]] || { echo "[FAIL] Could not resolve desktop DISPLAY"; exit 1; }
export DISPLAY="$REAL_DISPLAY"
[[ -n "$REAL_WAYLAND" ]] && export WAYLAND_DISPLAY="$REAL_WAYLAND"
export XDG_RUNTIME_DIR="${REAL_XDG_RUNTIME:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${REAL_DBUS:-unix:path=$XDG_RUNTIME_DIR/bus}"
if [[ -n "$REAL_XAUTH" ]]; then export XAUTHORITY="$REAL_XAUTH"; else unset XAUTHORITY || true; fi

echo "[PASS] Desktop: $GUI_PROCESS pid=$GUI_PID DISPLAY=$DISPLAY"
if command -v xdpyinfo >/dev/null 2>&1; then
  xdpyinfo -display "$DISPLAY" >/dev/null 2>&1 || { echo "[FAIL] X11 authorization"; exit 1; }
  echo "[PASS] X11 authorization"
fi

# 3. Latest skill into Anna.
[[ -f "$SKILL_SRC/SKILL.md" ]] || { echo "[FAIL] Missing $SKILL_SRC/SKILL.md"; exit 1; }
if [[ -e "$SKILL_DST" ]]; then
  cp -a "$SKILL_DST" "$HERMES_HOME/backups/chatgpt-thread-controller-$(date +%Y%m%d-%H%M%S)"
fi
rm -rf "$SKILL_DST"
mkdir -p "$SKILL_DST"
cp -a "$SKILL_SRC/." "$SKILL_DST/"
echo "[PASS] Latest chatgpt-thread-controller installed"

# 4. Stop competing gateway/MCP clients during repair/test.
systemctl --user stop hermes-gateway.service 2>/dev/null || true
sleep 3
pkill -u "$(id -u)" -f '[c]hrome-devtools-mcp' 2>/dev/null || true
sleep 2
echo "[PASS] Gateway stopped; stale MCP clients reaped"

# 5. Start/reuse dedicated Chrome CDP.
cdp_ok() {
  python3 - "$CDP_URL" >/dev/null 2>&1 <<'PY'
import json, sys, urllib.request
with urllib.request.urlopen(sys.argv[1] + "/json/version", timeout=2) as r:
    j=json.load(r)
assert j.get("webSocketDebuggerUrl")
PY
}

if ! cdp_ok; then
  pkill -u "$(id -u)" -f '[c]hrome.*chrome-real-profile' 2>/dev/null || true
  sleep 2
  mkdir -p "$CHROME_PROFILE"
  rm -f "$CHROME_PROFILE/SingletonLock" "$CHROME_PROFILE/SingletonSocket" "$CHROME_PROFILE/SingletonCookie" 2>/dev/null || true

  nohup env \
    DISPLAY="$DISPLAY" \
    XAUTHORITY="${XAUTHORITY:-}" \
    XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" \
    DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" \
    "$CHROME_BIN" \
      --ozone-platform=x11 \
      --remote-debugging-address=127.0.0.1 \
      --remote-debugging-port="$CDP_PORT" \
      --user-data-dir="$CHROME_PROFILE" \
      --no-first-run \
      --no-default-browser-check \
      --new-window \
      "$TARGET_URL" \
      >"$CHROME_LOG" 2>&1 &

  READY=0
  for _ in $(seq 1 30); do
    if cdp_ok; then READY=1; break; fi
    sleep 1
  done
  if [[ "$READY" != "1" ]]; then
    echo "[FAIL] Chrome CDP did not start"
    tail -n 100 "$CHROME_LOG" || true
    exit 1
  fi
fi
echo "[PASS] Chrome CDP live at $CDP_URL"

# 6. Patch chrome-real to fixed browser-url.
python3 - "$CONFIG" "$CDP_URL" <<'PY'
from pathlib import Path
from datetime import datetime
import shutil, sys, yaml
p=Path(sys.argv[1]); cdp=sys.argv[2]
cfg=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
server=(cfg.setdefault("mcp_servers", {})).get("chrome-real")
if not isinstance(server, dict):
    raise SystemExit("[FAIL] mcp_servers.chrome-real missing")
args=server.get("args") or []
if not isinstance(args, list):
    raise SystemExit("[FAIL] chrome-real args must be a list")
backup=p.with_name("config.yaml.before-chatgpt-onepass-"+datetime.now().strftime("%Y%m%d-%H%M%S"))
shutil.copy2(p, backup)
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
p.write_text(yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")
print("[PASS] chrome-real ->", "--browser-url="+cdp)
print("[PASS] Config backup:", backup)
PY

hermes config check >/dev/null
echo "[PASS] Hermes config valid"

# 7. Ensure exact thread is open. Use direct CDP instead of relying on model navigation.
python3 - "$CDP_URL" "$TARGET_URL" <<'PY'
import json, sys, urllib.request, urllib.parse, time
base, target=sys.argv[1],sys.argv[2]
tid=target.rstrip("/").split("/")[-1]
def pages():
    with urllib.request.urlopen(base+"/json/list", timeout=5) as r:
        return json.load(r)
def found():
    return any(tid in str(p.get("url","")) for p in pages() if isinstance(p,dict))
if not found():
    req=urllib.request.Request(base+"/json/new?"+urllib.parse.quote(target, safe=":/"), method="PUT")
    with urllib.request.urlopen(req, timeout=8) as r:
        r.read()
    for _ in range(15):
        if found():
            break
        time.sleep(1)
print("[INFO] Exact target currently open:", found())
raise SystemExit(0 if found() else 3)
PY
OPEN_RC=$?

if [[ "$OPEN_RC" != "0" ]]; then
  banner "LOGIN CHECKPOINT"
  echo "Chrome is visible on the Ubuntu desktop."
  echo "If ChatGPT requires login, log in now."
  echo "The persistent profile is: $CHROME_PROFILE"
  echo
  read -r -p "After login is complete, press ENTER once; the script will reopen and test the exact thread automatically... " _

  python3 - "$CDP_URL" "$TARGET_URL" <<'PY'
import json, sys, urllib.request, urllib.parse, time
base,target=sys.argv[1],sys.argv[2]
tid=target.rstrip("/").split("/")[-1]
req=urllib.request.Request(base+"/json/new?"+urllib.parse.quote(target, safe=":/"), method="PUT")
with urllib.request.urlopen(req, timeout=8) as r: r.read()
for _ in range(25):
    with urllib.request.urlopen(base+"/json/list", timeout=5) as r:
        ps=json.load(r)
    if any(tid in str(p.get("url","")) for p in ps if isinstance(p,dict)):
        print("[PASS] Exact ChatGPT thread is open")
        raise SystemExit(0)
    time.sleep(1)
raise SystemExit("[FAIL] Exact ChatGPT thread still not open after login")
PY
else
  echo "[PASS] Exact ChatGPT thread is open"
fi

# 8. MCP init check.
timeout 60s hermes mcp test chrome-real >/tmp/hermes-chatgpt-mcp-test.log 2>&1 || {
  cat /tmp/hermes-chatgpt-mcp-test.log
  exit 1
}
grep -q 'Tools discovered: 29' /tmp/hermes-chatgpt-mcp-test.log || {
  cat /tmp/hermes-chatgpt-mcp-test.log
  echo "[FAIL] Unexpected MCP tool discovery result"
  exit 1
}
echo "[PASS] chrome-real MCP initialized with 29 tools"

# 9. One end-to-end Hermes run: list -> select -> snapshot -> send -> verify -> wait -> read.
MARKER="CHATGPT-BRIDGE-TEST-$(date +%s)"
banner "END-TO-END HERMES TEST"
echo "Marker: $MARKER"

set +e
timeout 600s hermes chat \
  --oneshot \
  --max-turns 40 \
  -s chatgpt-thread-controller \
  -q "Use the chatgpt-thread-controller skill and chrome-real only.

Target exactly:
$TARGET_URL

The exact thread is already open in the visible authenticated Chrome.

Call list_pages with NO arguments.
Select the exact thread and bring it to the foreground.
Take a fresh snapshot.

Send exactly:
$MARKER

Take a NEW snapshot and verify that $MARKER appears as the newest user turn.
Wait until ChatGPT finishes.
Take another fresh snapshot.
Read the newest assistant response immediately following $MARKER.
Leave the tab open.

If and only if all of those observations succeed, end your answer with exactly:
CHATGPT_BRIDGE_PASS

Otherwise end with exactly:
CHATGPT_BRIDGE_FAIL" 2>&1 | tee "$TEST_LOG"
HERMES_RC=${PIPESTATUS[0]}
set -e

if grep -q 'CHATGPT_BRIDGE_PASS' "$TEST_LOG"; then
  banner "PASS — CHATGPT BROWSER BRIDGE WORKS"
  echo "Target: $TARGET_URL"
  echo "Chrome profile: $CHROME_PROFILE"
  echo "CDP: $CDP_URL"
  echo "Test log: $TEST_LOG"
  exit 0
fi

banner "FAIL — END-TO-END TEST DID NOT COMPLETE"
echo "Hermes exit code: $HERMES_RC"
echo "Log: $TEST_LOG"
tail -n 120 "$TEST_LOG" || true
exit 1
