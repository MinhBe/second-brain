#!/usr/bin/env bash
set -Eeuo pipefail

# Keep ONE long-lived chrome-devtools-mcp process attached to the user's existing
# default Chrome profile, expose it to Hermes over localhost Streamable HTTP,
# then run a real ChatGPT send/readback test.
#
# This avoids a new CDP client connection on every Hermes turn. Chrome's live
# remote-debugging consent may still appear ONCE when this persistent bridge first
# attaches. Do not restart this service between tasks; subsequent Hermes turns use
# the same MCP child and should not create new Chrome consent prompts.
#
# The script never launches or restarts Chrome and never creates a Chrome profile.

TARGET_URL="${1:-}"
[[ "$TARGET_URL" =~ ^https://chatgpt\.com/c/[A-Za-z0-9-]+/?$ ]] || {
  echo "Usage: $0 'https://chatgpt.com/c/<conversation-id>'" >&2
  exit 2
}
TARGET_URL="${TARGET_URL%/}"

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CHROME_ROOT="$HOME/.config/google-chrome"
CONFIG="$HERMES_HOME/config.yaml"
BINDING="$HERMES_HOME/real-chrome-binding.json"

BIN_DIR="$HOME/.local/bin"
SERVICE_DIR="$HOME/.config/systemd/user"
LAUNCHER="$BIN_DIR/hermes-chrome-mcp-persistent"
SERVICE="$SERVICE_DIR/hermes-chrome-mcp.service"

MCP_PORT="${HERMES_CHROME_MCP_PORT:-8931}"
MCP_URL="http://127.0.0.1:$MCP_PORT/mcp"
HEALTH_URL="http://127.0.0.1:$MCP_PORT/healthz"
LOG="$HERMES_HOME/logs/chrome-mcp-persistent.log"
E2E_LOG="$HERMES_HOME/logs/chatgpt-web-e2e-last.log"

mkdir -p "$BIN_DIR" "$SERVICE_DIR" "$HERMES_HOME/logs"

banner() {
  echo
  echo "================================================================"
  echo "$1"
  echo "================================================================"
}

banner "1. VERIFY EXISTING REAL CHROME — NO NEW BROWSER"

REAL_PID="$(
python3 <<'PY'
from pathlib import Path
import os
uid=os.getuid()
rows=[]
for p in Path("/proc").iterdir():
    if not p.name.isdigit():
        continue
    try:
        if p.stat().st_uid != uid:
            continue
        exe=os.readlink(p/"exe")
        if not exe.endswith("/chrome"):
            continue
        cmd=(p/"cmdline").read_bytes().replace(b"\0",b" ").decode(errors="replace")
    except Exception:
        continue
    if "--type=" in cmd or ".hermes/chrome-real-profile" in cmd:
        continue
    rows.append((int(p.name),cmd))
if rows:
    rows.sort()
    print(rows[0][0])
PY
)"

[[ -n "$REAL_PID" ]] || {
  echo "[FAIL] Existing normal Chrome process not found."
  exit 1
}

echo "[PASS] Existing Chrome PID: $REAL_PID"
echo "[PASS] Chrome data root: $CHROME_ROOT"
echo "[PASS] Profile locked: Default"

python3 - "$CHROME_ROOT" <<'PY'
from pathlib import Path
import json,sys
root=Path(sys.argv[1])
st=json.loads((root/"Local State").read_text(encoding="utf-8",errors="replace"))
info=((st.get("profile") or {}).get("info_cache") or {}).get("Default") or {}
print("[PASS] Chrome profile name:",info.get("name"))
print("[PASS] Chrome account:",info.get("user_name"))
print("[PASS] Google name:",info.get("gaia_name"))
PY

banner "2. REFRESH THE EXISTING CHROME DEVTOOLS ENDPOINT"

python3 - "$CHROME_ROOT" "$REAL_PID" "$BINDING" <<'PY'
from pathlib import Path
from datetime import datetime,timezone
import json,sys,re,subprocess

root=Path(sys.argv[1]); real_pid=sys.argv[2]; out=Path(sys.argv[3])
f=root/"DevToolsActivePort"
if not f.is_file():
    raise SystemExit("[FAIL] Existing Chrome has no DevToolsActivePort. Browser was NOT restarted.")
lines=f.read_text(encoding="utf-8",errors="replace").splitlines()
if len(lines)<2 or not lines[0].isdigit() or not lines[1].startswith("/devtools/browser/"):
    raise SystemExit("[FAIL] Invalid DevToolsActivePort")
port=int(lines[0]); path=lines[1]
ss=subprocess.check_output(["ss","-ltnp"],text=True,errors="replace")
pat=rf"127\.0\.0\.1:{port}.*pid={re.escape(real_pid)},"
if not re.search(pat,ss):
    raise SystemExit(f"[FAIL] CDP port {port} is not owned by existing Chrome PID {real_pid}")
ws=f"ws://127.0.0.1:{port}{path}"
data={
  "browser":"google-chrome",
  "pid":int(real_pid),
  "user_data_dir":str(root),
  "profile_directory":"Default",
  "cdp_port":port,
  "ws_endpoint":ws,
  "saved_at":datetime.now(timezone.utc).isoformat(),
  "policy":{
    "reuse_existing_browser":True,
    "allow_new_browser":False,
    "allow_random_profile":False,
    "profile_locked":True
  }
}
out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
out.chmod(0o600)
print("[PASS] Existing CDP port:",port)
print("[PASS] Existing browser WebSocket:",ws)
print("[PASS] Binding refreshed:",out)
PY

banner "3. INSTALL PERSISTENT MCP RELAY"

cat >"$LAUNCHER" <<'LAUNCHER'
#!/usr/bin/env bash
set -Eeuo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
BINDING="$HERMES_HOME/real-chrome-binding.json"
PORT="${HERMES_CHROME_MCP_PORT:-8931}"

WS="$(
python3 - "$BINDING" <<'PY'
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))
print(d["ws_endpoint"])
PY
)"

# One persistent chrome-devtools-mcp child for all future Hermes sessions.
# The child keeps its Chrome CDP connection open instead of reconnecting per turn.
exec npx -y supergateway \
  --stdio "npx -y chrome-devtools-mcp@latest --wsEndpoint=$WS --no-usage-statistics" \
  --outputTransport streamableHttp \
  --stateful \
  --sessionTimeout 86400000 \
  --port "$PORT" \
  --streamableHttpPath /mcp \
  --healthEndpoint /healthz \
  --logLevel info
LAUNCHER
chmod 700 "$LAUNCHER"

cat >"$SERVICE" <<EOF
[Unit]
Description=Hermes Persistent MCP Bridge to Existing Chrome
After=network.target

[Service]
Type=simple
Environment=HERMES_HOME=$HERMES_HOME
Environment=HERMES_CHROME_MCP_PORT=$MCP_PORT
ExecStart=$LAUNCHER
Restart=on-failure
RestartSec=5
TimeoutStopSec=15
StandardOutput=append:$LOG
StandardError=append:$LOG

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable hermes-chrome-mcp.service >/dev/null

# Intentionally restart ONLY this relay during installation so it reads the fresh
# current DevToolsActivePort. Do not restart Chrome.
systemctl --user restart hermes-chrome-mcp.service

echo "[PASS] Persistent bridge service installed:"
echo "       hermes-chrome-mcp.service"
echo "[PASS] It does NOT launch Chrome."

READY=0
for _ in $(seq 1 45); do
  if curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 1
done

if [[ "$READY" != "1" ]]; then
  echo "[FAIL] Persistent MCP relay did not become healthy."
  tail -n 120 "$LOG" || true
  exit 1
fi

echo "[PASS] Relay HTTP layer is live: $MCP_URL"

banner "4. POINT HERMES chrome-real TO THE PERSISTENT RELAY"

python3 - "$CONFIG" "$MCP_URL" <<'PY'
from pathlib import Path
import sys,yaml
p=Path(sys.argv[1]); url=sys.argv[2]
cfg=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
servers=cfg.setdefault("mcp_servers",{})
old=servers.get("chrome-real") or {}
servers["chrome-real"]={
  "url":url,
  "enabled":True,
  "timeout":180,
  "connect_timeout":30,
  "protocol":"auto",
  "keepalive_interval":30,
  "supports_parallel_tool_calls":False,
  "trust":"full",
}
p.write_text(yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False),encoding="utf-8")
print("[PASS] chrome-real is now HTTP:",url)
print("[PASS] Removed per-turn stdio Chrome spawning:",bool(old.get("command") or old.get("args")))
PY

hermes config check >/dev/null
echo "[PASS] Hermes config valid"

banner "5. FORCE THE ONE PERSISTENT CHROME ATTACH"

echo "The current Chrome live-debugging flow may show ONE consent dialog now."
echo "If it appears, click Allow ONCE."
echo
echo "After this bridge is attached, DO NOT restart hermes-chrome-mcp.service between tasks."
echo "Hermes gateway/model sessions will talk to the relay, not reconnect directly to Chrome."
echo

# First MCP test initializes the persistent child. It may not force CDP until a tool call,
# so the subsequent E2E run is the definitive attach test.
timeout 90s hermes mcp test chrome-real || {
  echo "[WARN] MCP discovery did not complete yet."
  echo "If Chrome is showing Allow remote debugging, click Allow once, then press ENTER."
  read -r -p "Press ENTER to retry... " _
  timeout 90s hermes mcp test chrome-real
}

banner "6. RESTART ONLY HERMES GATEWAY — KEEP CHROME RELAY ALIVE"

export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"

systemctl --user restart hermes-gateway.service 2>/dev/null || true
sleep 4

systemctl --user is-active hermes-chrome-mcp.service
systemctl --user is-active hermes-gateway.service || true

banner "7. SEND A REAL MESSAGE TO CHATGPT WEB AND READ THE RESPONSE"

MARKER="HERMES-WEB-E2E-$(date +%s)"
EXPECTED="WEB-REPLY-$MARKER"

echo "Target conversation:"
echo "$TARGET_URL"
echo
echo "Message Hermes will visibly send:"
echo "Reply with exactly: $EXPECTED"
echo

rm -f "$E2E_LOG"

set +e
timeout 420s hermes chat \
  --oneshot \
  --max-turns 35 \
  -s chatgpt-thread-controller \
  -q "Use chatgpt-thread-controller and chrome-real only.

chrome-real is a persistent HTTP MCP relay attached to my already-running real Chrome Default profile.
Never launch Chrome.
Never use autoConnect.
Never select or create another Chrome profile.

Target exactly this existing ChatGPT conversation:
$TARGET_URL

If that URL is not already open, open ONE new tab to that exact URL in the existing Chrome.
Bring that exact thread to the foreground.

Take a fresh snapshot and verify ChatGPT is authenticated.

Send exactly this message:
Reply with exactly: $EXPECTED

Verify from a new snapshot that my message appears in the conversation.
Wait for ChatGPT to finish responding.
Take another fresh snapshot.
Read the assistant response immediately following my new message.

Return the exact response you observed.
Leave the ChatGPT tab open.

End with exactly one of:
HERMES_WEB_E2E_PASS
HERMES_WEB_E2E_FAIL" 2>&1 | tee "$E2E_LOG"
HERMES_RC=${PIPESTATUS[0]}
set -e

# Avoid the old false-positive bug: inspect only the rendered Hermes final-answer box.
FINAL="$(
awk '
  /╭─ ☤ Hermes/ {inside=1; next}
  inside && /╰─/ {inside=0}
  inside {print}
' "$E2E_LOG" |
sed -E 's/^[[:space:]│┃|]+//; s/[[:space:]│┃|]+$//'
)"

if printf '%s\n' "$FINAL" | grep -Fxq 'HERMES_WEB_E2E_PASS'; then
  banner "PASS — HERMES SENT TO CHATGPT WEB AND READ THE RESPONSE"
  echo "Expected ChatGPT text: $EXPECTED"
  echo "Persistent relay: $MCP_URL"
  echo "Service remains running: hermes-chrome-mcp.service"
  echo
  echo "Future Hermes tasks should reuse this service without a new Chrome CDP connection."
  exit 0
fi

banner "E2E DID NOT PASS"
echo "Hermes exit code: $HERMES_RC"
echo "Persistent relay status:"
systemctl --user is-active hermes-chrome-mcp.service || true
echo
echo "Last relay log:"
tail -n 80 "$LOG" || true
echo
echo "Last Hermes E2E log:"
tail -n 140 "$E2E_LOG" || true
exit 1
