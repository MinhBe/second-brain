#!/usr/bin/env bash
set -Eeuo pipefail

TARGET_URL="${1:-}"
[[ "$TARGET_URL" =~ ^https://chatgpt\.com/c/[A-Za-z0-9-]+/?$ ]] || {
  echo "Usage: $0 'https://chatgpt.com/c/<conversation-id>'" >&2
  exit 2
}
TARGET_URL="${TARGET_URL%/}"

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CHROME_ROOT="$HOME/.config/google-chrome"
APP_DIR="$HOME/.local/lib/hermes-chatgpt-bridge"
BIN_DIR="$HOME/.local/bin"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE="$SERVICE_DIR/hermes-chatgpt-direct.service"
SERVER="$APP_DIR/server.mjs"
CLI="$BIN_DIR/chatgpt-web-exchange"
LOG="$HERMES_HOME/logs/chatgpt-direct-bridge.log"
PORT="${HERMES_CHATGPT_DIRECT_PORT:-8940}"
BASE="http://127.0.0.1:$PORT"

mkdir -p "$APP_DIR" "$BIN_DIR" "$SERVICE_DIR" "$HERMES_HOME/logs"

NODE_BIN="$(command -v node || true)"
[[ -n "$NODE_BIN" ]] || { echo "[FAIL] node not found"; exit 1; }
NODE_WS_FLAG=""
if ! "$NODE_BIN" -e 'process.exit(typeof WebSocket === "function" ? 0 : 1)' >/dev/null 2>&1; then
  if "$NODE_BIN" --experimental-websocket -e 'process.exit(typeof WebSocket === "function" ? 0 : 1)' >/dev/null 2>&1; then
    NODE_WS_FLAG="--experimental-websocket"
  else
    echo "[FAIL] This Node runtime has no WebSocket support."
    exit 1
  fi
fi

banner() {
  echo
  echo "================================================================"
  echo "$1"
  echo "================================================================"
}

banner "1. REQUIRE THE EXISTING REAL CHROME"

REAL_PID="$(
python3 <<'PY'
from pathlib import Path
import os
uid=os.getuid()
rows=[]
for p in Path("/proc").iterdir():
    if not p.name.isdigit(): continue
    try:
        if p.stat().st_uid != uid: continue
        exe=os.readlink(p/"exe")
        if not exe.endswith("/chrome"): continue
        cmd=(p/"cmdline").read_bytes().replace(b"\0",b" ").decode(errors="replace")
    except Exception:
        continue
    if "--type=" in cmd or ".hermes/chrome-real-profile" in cmd: continue
    rows.append((int(p.name),cmd))
if rows:
    rows.sort()
    print(rows[0][0])
PY
)"

[[ -n "$REAL_PID" ]] || { echo "[FAIL] Existing normal Chrome not found"; exit 1; }
echo "[PASS] Existing Chrome PID: $REAL_PID"
echo "[PASS] No Chrome will be launched or restarted."

python3 - "$CHROME_ROOT" <<'PY'
from pathlib import Path
import json,sys
root=Path(sys.argv[1])
s=json.loads((root/"Local State").read_text(encoding="utf-8",errors="replace"))
i=((s.get("profile") or {}).get("info_cache") or {}).get("Default") or {}
print("[PASS] Profile: Default")
print("[PASS] Chrome account:",i.get("user_name"))
print("[PASS] Google name:",i.get("gaia_name"))
PY

banner "2. RETIRE THE SUPERGATEWAY RELAY"

# Supergateway stateful mode owns one stdio child per HTTP MCP session.
# That means separate Hermes MCP sessions can create separate Chrome CDP connections.
# Retire it; do not touch Chrome.
systemctl --user disable --now hermes-chrome-mcp.service 2>/dev/null || true
rm -f "$HOME/.config/systemd/user/hermes-chrome-mcp.service"
systemctl --user daemon-reload

echo "[PASS] Old supergateway relay stopped."
echo "[PASS] Existing Chrome remains running."

banner "3. INSTALL ONE TRUE PERSISTENT CDP OWNER"

TMP_SERVER="$APP_DIR/server.new.mjs"
rm -f "$TMP_SERVER"
cat >"$TMP_SERVER" <<'NODE'
import http from 'node:http';
import fs from 'node:fs';

const HOME = process.env.HOME;
const CHROME_ROOT = process.env.CHROME_ROOT || HOME + '/.config/google-chrome';
const PORT = Number(process.env.HERMES_CHATGPT_DIRECT_PORT || '8940');

let ws = null;
let wsEndpoint = null;
let nextId = 1;
const pending = new Map();
let connecting = null;

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function readEndpoint() {
  const p = CHROME_ROOT + '/DevToolsActivePort';
  const lines = fs.readFileSync(p, 'utf8').trim().split(/\r?\n/);
  if (!/^\d+$/.test(lines[0] || '') || !(lines[1] || '').startsWith('/devtools/browser/')) {
    throw new Error('invalid DevToolsActivePort');
  }
  return `ws://127.0.0.1:${lines[0]}${lines[1]}`;
}

async function ensureConnected() {
  if (ws && ws.readyState === WebSocket.OPEN) return;
  if (connecting) return connecting;

  connecting = new Promise((resolve, reject) => {
    try {
      wsEndpoint = readEndpoint();
      const sock = new WebSocket(wsEndpoint);

      const timer = setTimeout(() => {
        try { sock.close(); } catch {}
        reject(new Error('Chrome CDP connect timeout'));
      }, 60000);

      sock.onopen = () => {
        clearTimeout(timer);
        ws = sock;

        ws.onmessage = (event) => {
          let msg;
          try { msg = JSON.parse(event.data); } catch { return; }
          if (msg.id && pending.has(msg.id)) {
            const {resolve, reject, timer} = pending.get(msg.id);
            pending.delete(msg.id);
            clearTimeout(timer);
            if (msg.error) reject(new Error(JSON.stringify(msg.error)));
            else resolve(msg.result);
          }
        };

        ws.onclose = () => {
          ws = null;
          for (const [id,p] of pending) {
            clearTimeout(p.timer);
            p.reject(new Error('Chrome CDP disconnected'));
          }
          pending.clear();
        };

        ws.onerror = () => {};
        resolve();
      };

      sock.onerror = () => {
        clearTimeout(timer);
        reject(new Error('Chrome CDP websocket error'));
      };
    } catch (e) {
      reject(e);
    }
  }).finally(() => { connecting = null; });

  return connecting;
}

async function cdp(method, params={}, sessionId=undefined, timeout=30000) {
  await ensureConnected();
  const id = nextId++;
  const payload = {id, method, params};
  if (sessionId) payload.sessionId = sessionId;

  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      pending.delete(id);
      reject(new Error(`${method} timeout`));
    }, timeout);
    pending.set(id, {resolve, reject, timer});
    ws.send(JSON.stringify(payload));
  });
}

async function getPages() {
  const r = await cdp('Target.getTargets');
  return (r.targetInfos || []).filter(x => x.type === 'page');
}

async function attach(targetId) {
  const r = await cdp('Target.attachToTarget', {targetId, flatten:true});
  return r.sessionId;
}

async function evalJs(sessionId, expression, timeout=30000) {
  const r = await cdp('Runtime.evaluate', {
    expression,
    awaitPromise:true,
    returnByValue:true,
    userGesture:true
  }, sessionId, timeout);
  if (r.exceptionDetails) {
    throw new Error('Runtime.evaluate exception: ' + JSON.stringify(r.exceptionDetails));
  }
  return r.result?.value;
}

async function chooseTarget(targetUrl) {
  let pages = await getPages();
  let exact = pages.find(p => (p.url || '').replace(/\/$/,'') === targetUrl.replace(/\/$/,''));

  if (exact) return {target:exact, reused:true, navigated:false};

  const chat = pages.find(p => (p.url || '').startsWith('https://chatgpt.com/'));
  if (!chat) throw new Error('No existing ChatGPT tab; refusing to create a new tab');

  const sid = await attach(chat.targetId);
  await cdp('Page.enable', {}, sid);
  await cdp('Page.navigate', {url:targetUrl}, sid, 30000);

  for (let i=0; i<60; i++) {
    await sleep(250);
    pages = await getPages();
    exact = pages.find(p => (p.url || '').replace(/\/$/,'') === targetUrl.replace(/\/$/,''));
    if (exact) return {target:exact, reused:true, navigated:true};
  }

  throw new Error('Existing ChatGPT tab did not reach target URL');
}

function jsString(x) {
  return JSON.stringify(String(x));
}

async function exchange(targetUrl, prompt) {
  const chosen = await chooseTarget(targetUrl);
  const target = chosen.target;

  await cdp('Target.activateTarget', {targetId:target.targetId});
  const sid = await attach(target.targetId);
  await cdp('Runtime.enable', {}, sid);
  await cdp('Page.enable', {}, sid);

  const baseline = await evalJs(sid, `(() => {
    const users=[...document.querySelectorAll('[data-message-author-role="user"]')];
    const assistants=[...document.querySelectorAll('[data-message-author-role="assistant"]')];
    const composer=
      document.querySelector('#prompt-textarea') ||
      document.querySelector('textarea[placeholder]') ||
      document.querySelector('[contenteditable="true"][data-virtualkeyboard]') ||
      document.querySelector('div[contenteditable="true"]');
    if (!composer) return {ok:false,reason:'composer_not_found',url:location.href};
    composer.focus();
    return {
      ok:true,
      url:location.href,
      userCount:users.length,
      assistantCount:assistants.length,
      lastAssistant:assistants.at(-1)?.innerText?.trim() || ''
    };
  })()`);

  if (!baseline?.ok) throw new Error(JSON.stringify(baseline));

  // Clear composer with real key events, then insert text through CDP so React sees it.
  await cdp('Input.dispatchKeyEvent', {type:'keyDown', key:'a', code:'KeyA', modifiers:2}, sid);
  await cdp('Input.dispatchKeyEvent', {type:'keyUp', key:'a', code:'KeyA', modifiers:2}, sid);
  await cdp('Input.dispatchKeyEvent', {type:'keyDown', key:'Backspace', code:'Backspace'}, sid);
  await cdp('Input.dispatchKeyEvent', {type:'keyUp', key:'Backspace', code:'Backspace'}, sid);
  await cdp('Input.insertText', {text:prompt}, sid);

  // Verify exact text made it into composer before sending.
  const composerText = await evalJs(sid, `(() => {
    const el =
      document.querySelector('#prompt-textarea') ||
      document.querySelector('textarea[placeholder]') ||
      document.querySelector('[contenteditable="true"][data-virtualkeyboard]') ||
      document.querySelector('div[contenteditable="true"]');
    return el ? ((el.value ?? el.innerText ?? el.textContent ?? '').trim()) : null;
  })()`);

  if (composerText !== prompt.trim()) {
    throw new Error('composer_text_mismatch: ' + JSON.stringify(composerText));
  }

  // Explicitly click ChatGPT's send button. Do not rely on Enter semantics.
  let clickResult = await evalJs(sid, `(() => {
    const selectors = [
      'button[data-testid="send-button"]',
      'button[aria-label="Send prompt"]',
      'button[aria-label^="Send"]',
      'button[type="submit"]'
    ];
    const btn = selectors.map(s => document.querySelector(s)).find(Boolean);
    if (!btn) return {ok:false,reason:'send_button_not_found'};
    const disabled = !!btn.disabled || btn.getAttribute('aria-disabled') === 'true';
    if (disabled) return {ok:false,reason:'send_button_disabled'};
    btn.click();
    return {ok:true,selector:selectors.find(s=>document.querySelector(s)===btn)};
  })()`);

  if (!clickResult?.ok) {
    throw new Error('send_click_failed: ' + JSON.stringify(clickResult));
  }

  // Require a NEW user turn containing this exact prompt. If absent, sending failed.
  let submitted = false;
  for (let i=0; i<40; i++) {
    await sleep(250);
    const x = await evalJs(sid, `(() => {
      const users=[...document.querySelectorAll('[data-message-author-role="user"]')];
      return {
        count:users.length,
        last:(users.at(-1)?.innerText || '').trim()
      };
    })()`);
    if (x && x.count > baseline.userCount && x.last.includes(prompt.trim())) {
      submitted = true;
      break;
    }
  }
  if (!submitted) throw new Error('submission_not_observed_after_send_click');

  // Wait for assistant count to increase. A previous last assistant is never accepted.
  let stableText = '';
  let stableSamples = 0;
  let lastSeen = '';
  const deadline = Date.now() + 150000;

  while (Date.now() < deadline) {
    await sleep(500);
    const x = await evalJs(sid, `(() => {
      const assistants=[...document.querySelectorAll('[data-message-author-role="assistant"]')];
      const text=(assistants.at(-1)?.innerText || '').trim();
      const stop=!!(
        document.querySelector('button[data-testid="stop-button"]') ||
        document.querySelector('button[aria-label*="Stop"]')
      );
      return {count:assistants.length,text,stop};
    })()`);

    if (!x || x.count <= baseline.assistantCount || !x.text) {
      stableSamples = 0;
      continue;
    }

    if (x.text === lastSeen) stableSamples += 1;
    else {
      lastSeen = x.text;
      stableSamples = 1;
    }

    if (!x.stop && stableSamples >= 3) {
      stableText = x.text;
      break;
    }
  }

  if (!stableText) throw new Error('new_assistant_response_timeout');

  return {
    ok:true,
    target_url:targetUrl,
    target_id:target.targetId,
    target_page_reused:true,
    new_page_created:false,
    navigated_existing_chatgpt_tab:chosen.navigated,
    submitted:true,
    response:stableText
  };
}

async function bodyJson(req) {
  const chunks=[];
  for await (const c of req) chunks.push(c);
  return JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
}

const server = http.createServer(async (req,res) => {
  res.setHeader('Content-Type','application/json; charset=utf-8');

  if (req.method === 'GET' && req.url === '/health') {
    try {
      await ensureConnected();
      const v = await cdp('Browser.getVersion');
      res.end(JSON.stringify({ok:true,connected:true,browser:v.product,ws_endpoint:wsEndpoint}));
    } catch (e) {
      res.statusCode=503;
      res.end(JSON.stringify({ok:false,connected:false,error:String(e)}));
    }
    return;
  }

  if (req.method === 'GET' && req.url === '/pages') {
    try {
      const pages=await getPages();
      res.end(JSON.stringify({ok:true,pages:pages.map(p=>({id:p.targetId,title:p.title,url:p.url}))}));
    } catch (e) {
      res.statusCode=500;
      res.end(JSON.stringify({ok:false,error:String(e)}));
    }
    return;
  }

  if (req.method === 'POST' && req.url === '/exchange') {
    try {
      const body=await bodyJson(req);
      if (typeof body.target_url !== 'string' || typeof body.prompt !== 'string') {
        throw new Error('target_url and prompt are required strings');
      }
      const result=await exchange(body.target_url.replace(/\/$/,''),body.prompt);
      res.end(JSON.stringify(result));
    } catch (e) {
      res.statusCode=500;
      res.end(JSON.stringify({ok:false,error:String(e)}));
    }
    return;
  }

  res.statusCode=404;
  res.end(JSON.stringify({ok:false,error:'not found'}));
});

server.listen(PORT,'127.0.0.1', async () => {
  console.log(`direct bridge listening on http://127.0.0.1:${PORT}`);
  try {
    await ensureConnected();
    console.log(`connected to ${wsEndpoint}`);
  } catch (e) {
    console.error(String(e));
  }
});
NODE

echo "[CHECK] Validating direct bridge JavaScript before installation..."
if ! "$NODE_BIN" --check "$TMP_SERVER"; then
  echo "[FAIL] Generated direct bridge JavaScript is invalid."
  rm -f "$TMP_SERVER"
  exit 1
fi
mv -f "$TMP_SERVER" "$SERVER"
echo "[PASS] Direct bridge JavaScript syntax valid."

cat >"$CLI" <<'SH'
#!/usr/bin/env bash
set -Eeuo pipefail
TARGET="${1:?target URL required}"
PROMPT="${2:?prompt required}"
PORT="${HERMES_CHATGPT_DIRECT_PORT:-8940}"

python3 - "$TARGET" "$PROMPT" "$PORT" <<'PY'
import json,sys,urllib.request
target,prompt,port=sys.argv[1:]
body=json.dumps({"target_url":target,"prompt":prompt}).encode()
req=urllib.request.Request(
    f"http://127.0.0.1:{port}/exchange",
    data=body,
    headers={"Content-Type":"application/json"},
    method="POST"
)
with urllib.request.urlopen(req,timeout=180) as r:
    result=json.load(r)
print(json.dumps(result,ensure_ascii=False))
if not result.get("ok"):
    raise SystemExit(1)
PY
SH
chmod 700 "$CLI"

cat >"$SERVICE" <<EOF
[Unit]
Description=Hermes Direct Persistent ChatGPT Browser Bridge
After=default.target

[Service]
Type=simple
Environment=HOME=$HOME
Environment=CHROME_ROOT=$CHROME_ROOT
Environment=HERMES_CHATGPT_DIRECT_PORT=$PORT
ExecStart=$NODE_BIN $NODE_WS_FLAG $SERVER
Restart=on-failure
RestartSec=5
StandardOutput=append:$LOG
StandardError=append:$LOG

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable hermes-chatgpt-direct.service >/dev/null

if systemctl --user is-active --quiet hermes-chatgpt-direct.service \
   && curl -fsS "$BASE/health" >/dev/null 2>&1; then
  echo "[PASS] Healthy direct bridge already active; NOT restarting it."
else
  systemctl --user stop hermes-chatgpt-direct.service 2>/dev/null || true
  systemctl --user reset-failed hermes-chatgpt-direct.service 2>/dev/null || true
  systemctl --user start hermes-chatgpt-direct.service
  echo
  echo "Chrome may show ONE final 'Allow remote debugging' prompt now."
  echo "Click Allow once. After this, keep hermes-chatgpt-direct.service running."
fi

READY=0
for _ in $(seq 1 90); do
  if curl -fsS "$BASE/health" >/tmp/chatgpt-direct-health.json 2>/dev/null; then
    READY=1
    break
  fi
  sleep 1
done

if [[ "$READY" != "1" ]]; then
  echo "[FAIL] Direct bridge did not attach."
  tail -n 100 "$LOG" || true
  exit 1
fi

echo "[PASS] Direct bridge health:"
cat /tmp/chatgpt-direct-health.json
echo
echo "[PASS] One long-lived CDP owner is now active."

PID_BEFORE="$(systemctl --user show -p MainPID --value hermes-chatgpt-direct.service)"
START_BEFORE="$(systemctl --user show -p ActiveEnterTimestampMonotonic --value hermes-chatgpt-direct.service)"

banner "4. LIST EXISTING TABS THROUGH THE SAME PERSISTENT CONNECTION"

curl -fsS "$BASE/pages" | python3 -m json.tool

banner "5. DETERMINISTIC SEND + CLICK + RESPONSE TEST"

MARKER="DIRECT-FAST-$(date +%s)"
EXPECTED="DIRECT-REPLY-$MARKER"
PROMPT="Reply with exactly: $EXPECTED"

echo "Sending:"
echo "$PROMPT"

RESULT="$("$CLI" "$TARGET_URL" "$PROMPT")"
printf '%s\n' "$RESULT" | python3 -m json.tool

python3 - "$EXPECTED" "$RESULT" <<'PY'
import json,sys
expected=sys.argv[1]
r=json.loads(sys.argv[2])
assert r.get("ok") is True, r
assert r.get("new_page_created") is False, r
assert r.get("submitted") is True, r
assert (r.get("response") or "").strip() == expected, r
print("[PASS] Exact new assistant response matched:",expected)
PY

PID_AFTER="$(systemctl --user show -p MainPID --value hermes-chatgpt-direct.service)"
START_AFTER="$(systemctl --user show -p ActiveEnterTimestampMonotonic --value hermes-chatgpt-direct.service)"

[[ "$PID_BEFORE" == "$PID_AFTER" && "$START_BEFORE" == "$START_AFTER" ]] || {
  echo "[FAIL] Direct bridge restarted during the test."
  exit 1
}

banner "PASS — ONE CHROME / ONE CDP CONNECTION / EXPLICIT SEND CLICK"

echo "[PASS] Existing Chrome reused."
echo "[PASS] No new Chrome opened."
echo "[PASS] No new tab created."
echo "[PASS] Send button was explicitly clicked."
echo "[PASS] New user turn was verified before waiting for response."
echo "[PASS] Only a NEW assistant turn was accepted."
echo "[PASS] Bridge PID remained $PID_AFTER."
echo
echo "CLI for Hermes:"
echo "  $CLI '<chatgpt-thread-url>' '<prompt>'"
echo
echo "Keep hermes-chatgpt-direct.service running."
echo "Do not restart it between tasks."
