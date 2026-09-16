#!/usr/bin/env node
// bwp daemon — keeps ONE Playwright connection to the user's running Chrome and executes
// bwp verbs for the CLI over a loopback TCP socket. Chrome 144+ asks the human to allow
// every new DevTools client, so a single long-lived connection means one "Allow" per
// Chrome session instead of one per command. Exits after IDLE_MS without requests.
import { createServer } from 'node:net';
import { writeFileSync, unlinkSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { randomBytes } from 'node:crypto';
import { SkillError, EXIT } from './exit-codes.mjs';
import { connectBrowser } from './cdp-attach.mjs';
import { execVerb, DIR } from './bwp-core.mjs';

const IDLE_MS = Number(process.env.BROWSER_SKILL_BWP_IDLE_MS ?? 60 * 60 * 1000);
const FILE = join(DIR, 'daemon.json');
const token = randomBytes(16).toString('hex');
let browser = null;
let busy = Promise.resolve();
let idleTimer = null;

async function getBrowser() {
  if (browser && browser.isConnected()) return browser;
  browser = await connectBrowser();
  browser.once('disconnected', () => { browser = null; });
  return browser;
}
async function reconnect() {
  if (browser) await browser.close().catch(() => {});
  browser = null;
  return getBrowser();
}
const ctx = { browser: getBrowser, reconnect, daemonInfo: () => ({ pid: process.pid, connected: !!(browser && browser.isConnected()) }) };

function armIdle() { clearTimeout(idleTimer); idleTimer = setTimeout(() => shutdown('idle'), IDLE_MS); idleTimer.unref(); }
async function shutdown(reason) {
  try { unlinkSync(FILE); } catch { /* none */ }
  if (browser) await browser.close().catch(() => {});
  process.stderr.write(`bwp-daemon exit (${reason})\n`);
  process.exit(0);
}

const server = createServer((sock) => {
  let buf = '';
  sock.setEncoding('utf8');
  sock.on('data', (d) => {
    buf += d;
    const i = buf.indexOf('\n');
    if (i < 0) return;
    const line = buf.slice(0, i); buf = buf.slice(i + 1);
    let req;
    try { req = JSON.parse(line); } catch { sock.end(JSON.stringify({ exit: EXIT.USAGE, code: 'USAGE', error: 'bad request' }) + '\n'); return; }
    if (req.token !== token) { sock.end(JSON.stringify({ exit: EXIT.POLICY, code: 'POLICY', error: 'bad token' }) + '\n'); return; }
    armIdle();
    // Verbs run one at a time: the browser connection is shared.
    busy = busy.then(async () => {
      let out;
      if (req.verb === 'daemon') {
        out = { exit: EXIT.OK, verb: 'daemon', fields: ctx.daemonInfo(), next: 'Daemon running' };
        if (req.rest?.includes('--stop')) { sock.end(JSON.stringify({ ...out, fields: { ...out.fields, stopping: true } }) + '\n'); await shutdown('stop'); return; }
      } else {
        try {
          const r = await execVerb(req.verb, req.rest ?? [], { ...ctx, stdin: req.stdin ?? '' });
          out = { exit: EXIT.OK, verb: r.verb, fields: r.fields, next: r.next };
        } catch (e) {
          out = e instanceof SkillError
            ? { exit: e.exit, code: e.code, verb: req.verb, error: e.message, next: e.next, fields: e.extra ?? {} }
            : { exit: EXIT.INTERNAL, code: 'INTERNAL', verb: req.verb, error: String(e?.stack ?? e).split('\n').slice(0, 3).join(' | '), next: 'Report this error' };
        }
      }
      sock.end(JSON.stringify(out) + '\n');
    }).catch(() => {});
  });
});

mkdirSync(DIR, { recursive: true });
server.listen(0, '127.0.0.1', () => {
  writeFileSync(FILE, JSON.stringify({ port: server.address().port, token, pid: process.pid, started_at: new Date().toISOString() }));
  armIdle();
});
process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
