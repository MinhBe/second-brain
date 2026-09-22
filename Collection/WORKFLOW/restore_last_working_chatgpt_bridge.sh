#!/usr/bin/env bash
set -Eeuo pipefail

TARGET_URL="${1:-}"
[[ "$TARGET_URL" =~ ^https://chatgpt\.com/c/[A-Za-z0-9-]+/?$ ]] || {
  echo "Usage: $0 'https://chatgpt.com/c/<conversation-id>'" >&2
  exit 2
}
TARGET_URL="${TARGET_URL%/}"

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
REPO="${SECOND_BRAIN_REPO:-$HOME/second-brain}"
OLD_FLOW="$REPO/Collection/WORKFLOW/persist_real_chrome_mcp_and_test_chatgpt.sh"

echo "================================================================"
echo "ROLL BACK TO LAST KNOWN-WORKING CHATGPT BRIDGE"
echo "================================================================"

# 1) Remove the failed direct-bridge experiment only.
systemctl --user disable --now hermes-chatgpt-direct.service 2>/dev/null || true
rm -f "$HOME/.config/systemd/user/hermes-chatgpt-direct.service"
systemctl --user daemon-reload
systemctl --user reset-failed hermes-chatgpt-direct.service 2>/dev/null || true

echo "[PASS] Broken direct bridge disabled."

# 2) Ensure the known-working workflow exists locally.
if [[ ! -f "$OLD_FLOW" ]]; then
  mkdir -p "$(dirname "$OLD_FLOW")"
  curl -fsSL \
    "https://raw.githubusercontent.com/MinhBe/second-brain/main/Collection/WORKFLOW/persist_real_chrome_mcp_and_test_chatgpt.sh" \
    -o "$OLD_FLOW"
fi
chmod +x "$OLD_FLOW"

# 3) Restore the last known-working supergateway -> chrome-devtools-mcp -> real Chrome path.
# This recreates hermes-chrome-mcp.service, points chrome-real back to 127.0.0.1:8931/mcp,
# validates MCP discovery, restarts only Hermes gateway, and performs the same E2E test
# that previously succeeded.
bash "$OLD_FLOW" "$TARGET_URL"
