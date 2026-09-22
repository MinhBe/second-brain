#!/usr/bin/env bash
set -Eeuo pipefail

TARGET_URL="${1:-}"
[[ "$TARGET_URL" =~ ^https://chatgpt\.com/c/[A-Za-z0-9-]+/?$ ]] || {
  echo "Usage: $0 'https://chatgpt.com/c/<conversation-id>'" >&2
  exit 2
}
TARGET_URL="${TARGET_URL%/}"

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CONFIG="$HERMES_HOME/config.yaml"
RELAY_SERVICE="hermes-chrome-mcp.service"
OLD_BROWSER_SERVICE="hermes-chrome-real.service"
MCP_URL="http://127.0.0.1:8931/mcp"
SKILL_DIR="$HERMES_HOME/skills/chatgpt-thread-controller"
SKILL_URL="https://raw.githubusercontent.com/MinhBe/second-brain/main/Collection/SKILL/chatgpt-thread-controller/SKILL.md"
TEST_LOG="$HERMES_HOME/logs/chatgpt-fast-path-last.log"

mkdir -p "$SKILL_DIR" "$HERMES_HOME/logs"

banner() {
  echo
  echo "================================================================"
  echo "$1"
  echo "================================================================"
}

banner "1. REMOVE THE OLD BLANK-CHROME LAUNCHER"

# This obsolete unit was created by the earlier dedicated-profile design.
# Stop/remove only that unit and only Chrome processes using its user-data-dir.
systemctl --user disable --now "$OLD_BROWSER_SERVICE" 2>/dev/null || true
rm -f "$HOME/.config/systemd/user/$OLD_BROWSER_SERVICE"
systemctl --user daemon-reload

pkill -u "$(id -u)" -f '[c]hrome.*--user-data-dir=/home/ubuntu/.hermes/chrome-real-profile' 2>/dev/null || true
pkill -u "$(id -u)" -f '[g]oogle-chrome.*--user-data-dir=/home/ubuntu/.hermes/chrome-real-profile' 2>/dev/null || true

echo "[PASS] Old Hermes blank-profile Chrome launcher removed."
echo "[PASS] Existing normal Chrome was not touched."

banner "2. REQUIRE THE EXISTING PERSISTENT RELAY — DO NOT RESTART IT"

if ! systemctl --user is-active --quiet "$RELAY_SERVICE"; then
  echo "[FAIL] $RELAY_SERVICE is not active."
  echo "Not restarting it automatically because a new CDP attach can trigger Chrome's Allow prompt."
  exit 1
fi

RELAY_MAIN_PID="$(systemctl --user show -p MainPID --value "$RELAY_SERVICE")"
RELAY_STARTED="$(systemctl --user show -p ActiveEnterTimestampMonotonic --value "$RELAY_SERVICE")"

echo "[PASS] Persistent relay active."
echo "       main PID: $RELAY_MAIN_PID"
echo "       active-since-monotonic: $RELAY_STARTED"

curl -fsS "http://127.0.0.1:8931/healthz" >/dev/null
echo "[PASS] Relay health endpoint OK."

banner "3. HARD-LIMIT chrome-real TO THE FAST TOOLSET"

python3 - "$CONFIG" "$MCP_URL" <<'PY'
from pathlib import Path
import sys,yaml

p=Path(sys.argv[1]); url=sys.argv[2]
cfg=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
servers=cfg.setdefault("mcp_servers",{})
s=servers.setdefault("chrome-real",{})

# Keep the persistent HTTP transport. Never put command/args back here.
for k in ("command","args","env"):
    s.pop(k,None)

s["url"]=url
s["enabled"]=True
s["timeout"]=120
s["connect_timeout"]=15
s["protocol"]="auto"
s["keepalive_interval"]=30
s["supports_parallel_tool_calls"]=False
s["trust"]="full"

# Deliberately omit new_page and close_page so the model cannot create/close tabs.
s["tools"]={
    "include":[
        "list_pages",
        "select_page",
        "navigate_page",
        "evaluate_script",
        "type_text",
        "take_snapshot",
        "fill",
        "press_key",
        "wait_for"
    ],
    "resources":False,
    "prompts":False
}

p.write_text(
    yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False),
    encoding="utf-8"
)
print("[PASS] chrome-real hard-limited to existing-page tools.")
print("[PASS] new_page is NOT exposed.")
print("[PASS] close_page is NOT exposed.")
PY

hermes config check >/dev/null
echo "[PASS] Hermes config valid."

banner "4. INSTALL THE HARD FAST-PATH SKILL"

curl -fsSL "$SKILL_URL" -o "$SKILL_DIR/SKILL.md"
echo "[PASS] Latest fast-path skill installed."

banner "5. RESTART ONLY HERMES GATEWAY"

export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"

systemctl --user restart hermes-gateway.service
sleep 3

systemctl --user is-active --quiet "$RELAY_SERVICE" || {
  echo "[FAIL] Persistent relay died unexpectedly."
  exit 1
}

RELAY_MAIN_PID_AFTER="$(systemctl --user show -p MainPID --value "$RELAY_SERVICE")"
RELAY_STARTED_AFTER="$(systemctl --user show -p ActiveEnterTimestampMonotonic --value "$RELAY_SERVICE")"

if [[ "$RELAY_MAIN_PID_AFTER" != "$RELAY_MAIN_PID" || "$RELAY_STARTED_AFTER" != "$RELAY_STARTED" ]]; then
  echo "[FAIL] Relay restarted; refusing to continue because that can trigger a new Chrome Allow prompt."
  exit 1
fi

echo "[PASS] Relay stayed alive through gateway restart."
echo "[PASS] No new Chrome CDP attachment was created."

banner "6. FAST END-TO-END TEST — REUSE EXISTING TAB ONLY"

MARKER="FAST-WEB-$(date +%s)"
EXPECTED="FAST-REPLY-$MARKER"

echo "Target: $TARGET_URL"
echo "Expected response: $EXPECTED"
echo
echo "Hard rule: NO new_page tool exists in this test."

rm -f "$TEST_LOG"

set +e
timeout 180s hermes chat \
  --oneshot \
  --max-turns 18 \
  -s chatgpt-thread-controller \
  -q "FAST PATH ONLY.

Use chrome-real only.
Do not search for tools.
Do not use terminal.
Do not use snapshots unless semantic composer focus fails.

Target exactly:
$TARGET_URL

Hard constraints:
- list_pages takes NO arguments.
- new_page is forbidden and unavailable.
- Never create a browser or tab.
- Never change Chrome profile.
- Reuse the exact target page if present.
- If exact target is absent, navigate an already-open chatgpt.com page to it.
- If no ChatGPT page exists, fail instead of creating one.
- Bring the chosen page to front.

Send exactly:
Reply with exactly: $EXPECTED

Use the mandatory fast-path sequence from chatgpt-thread-controller:
list_pages -> select/reuse -> evaluate_script focus+baseline -> type_text with submitKey Enter -> one async evaluate_script to wait for and return the stable latest assistant response.

Do not repeatedly take snapshots while waiting.

Report:
target_page_reused: yes/no
new_page_created: yes/no
submission_observed: yes/no
latest_response: <text>

PASS only when:
- target_page_reused=yes
- new_page_created=no
- submission_observed=yes
- latest_response is exactly $EXPECTED

End with exactly:
HERMES_FAST_WEB_PASS
or
HERMES_FAST_WEB_FAIL" 2>&1 | tee "$TEST_LOG"
RC=${PIPESTATUS[0]}
set -e

FINAL="$(
awk '
  /╭─ ☤ Hermes/ {inside=1; next}
  inside && /╰─/ {inside=0}
  inside {print}
' "$TEST_LOG" |
sed -E 's/^[[:space:]│┃|]+//; s/[[:space:]│┃|]+$//'
)"

if printf '%s\n' "$FINAL" | grep -Fxq 'HERMES_FAST_WEB_PASS'; then
  banner "PASS — FAST EXISTING-TAB CHATGPT PATH"
  echo "[PASS] No blank Hermes Chrome service."
  echo "[PASS] Persistent relay was not restarted."
  echo "[PASS] No new_page tool exposed."
  echo "[PASS] Message sent and response read."
  echo
  echo "Relay PID still: $(systemctl --user show -p MainPID --value "$RELAY_SERVICE")"
  exit 0
fi

banner "FAST TEST FAILED"
echo "Hermes exit code: $RC"
echo "Relay remains active: $(systemctl --user is-active "$RELAY_SERVICE" 2>/dev/null || true)"
echo
tail -n 120 "$TEST_LOG" || true
exit 1
