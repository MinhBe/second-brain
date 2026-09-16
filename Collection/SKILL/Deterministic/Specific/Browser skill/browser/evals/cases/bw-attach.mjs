// End-to-end: bw.mjs attach against a throwaway Chrome that stands in for the user's running
// browser (--remote-debugging-port on a temp user-data-dir, two pre-existing "user" tabs).
// Proves: the skill works only in tabs it opened, refuses the user's tabs (7), refuses
// state-save (7), close detaches without touching Chrome, and the user's tabs survive.
import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { assertEq, assertTrue } from '../lib/assert.mjs';
import { findChrome } from '../../scripts/lib/chrome.mjs';

export const name = 'bw-attach';
export const needsBrowser = true;
export const skip = findChrome() ? undefined : 'Google Chrome not installed';

const PORT = 9377;
const ENDPOINT = `http://127.0.0.1:${PORT}`;

async function devtools(path, method = 'GET') {
  const res = await fetch(`${ENDPOINT}${path}`, { method });
  const text = await res.text();
  try { return JSON.parse(text); } catch { return text; }
}

async function userTabs() {
  const list = await devtools('/json');
  return (Array.isArray(list) ? list : []).filter((t) => t.type === 'page' && /^data:/.test(t.url)).map((t) => t.title).sort();
}

export async function run(ctx) {
  const srv = await ctx.server();
  const chrome = findChrome();
  const ud = mkdtempSync(join(tmpdir(), 'bw-attach-'));
  const tabA = 'data:text/html,<title>user tab A</title>A';
  const child = spawn(chrome.path, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${ud}`, '--no-first-run', '--no-default-browser-check', tabA], { stdio: 'ignore', windowsHide: true });
  const S = 'bwattach';
  const env = { BROWSER_SKILL_CDP_ENDPOINT: ENDPOINT };
  const step = (id, args) => { const r = ctx.runScript('bw', args, { env }); ctx.checkLine(id, r); return r; };
  try {
    let up = false;
    for (let i = 0; i < 40 && !up; i++) { try { await devtools('/json/version'); up = true; } catch { await new Promise((r) => setTimeout(r, 250)); } }
    assertTrue('chrome.up', up, 'devtools endpoint answers');
    await devtools('/json/new?data:text/html,<title>user%20tab%20B</title>B', 'PUT');
    await new Promise((r) => setTimeout(r, 500));
    const before = await userTabs();
    assertEq('user-tabs.before', before.length, 2);

    ctx.runScript('bw', ['close', '-s', S], { env });
    let r = step('attach', ['attach', srv.url, '-s', S]);
    assertEq('attach.exit', r.status, 0);
    assertEq('attach.attached', r.json.attached, true);
    assertEq('attach.title', r.json.title, 'bw smoke fixture');
    assertEq('attach.baseline', r.json.baseline_tabs, 2);
    assertEq('attach.tab-index', r.json.tab_index, 2);

    r = step('open-busy', ['open', srv.url, '-s', S]);
    assertEq('open-busy.exit', r.status, 12);
    assertTrue('open-busy.next', /tabs -s bwattach --new/.test(r.json.next), r.json.next);

    r = step('tabs', ['tabs', '-s', S]);
    assertEq('tabs.count', r.json.tabs.length, 3);
    assertEq('tabs.owned', r.json.tabs.filter((t) => t.owned).length, 1);
    assertEq('tabs.user-redacted', r.json.tabs[0].url, null);

    r = step('select-user', ['tabs', '-s', S, '--select', '0']);
    assertEq('select-user.exit', r.status, 7);
    r = step('close-user', ['tabs', '-s', S, '--close', '1']);
    assertEq('close-user.exit', r.status, 7);
    r = step('state-save', ['state-save', 'attachx', '-s', S]);
    assertEq('state-save.exit', r.status, 7);

    r = step('goto', ['goto', `${srv.url}index.html#attach`, '-s', S]);
    assertEq('goto.exit', r.status, 0);
    r = step('extract', ['extract', '-s', S, '--mode', 'text', '--css', 'h1']);
    assertEq('extract.text', r.json.text, 'bw smoke fixture');

    r = step('tabs-new', ['tabs', '-s', S, '--new', srv.url]);
    assertEq('tabs-new.exit', r.status, 0);
    assertEq('tabs-new.owned', r.json.tabs.filter((t) => t.owned).length, 2);

    // The user closes the skill's tabs by hand: the guard must refuse to act on their tab.
    const pages = await devtools('/json');
    for (const p of pages.filter((t) => t.type === 'page' && t.url.startsWith(srv.url))) await devtools(`/json/close/${p.id}`);
    await new Promise((r) => setTimeout(r, 500));
    r = step('goto-after-user-closed', ['goto', srv.url, '-s', S]);
    assertEq('goto-after-user-closed.exit', r.status, 7);
    r = step('tabs-new-recover', ['tabs', '-s', S, '--new', srv.url]);
    assertEq('tabs-new-recover.exit', r.status, 0);

    r = step('close', ['close', '-s', S]);
    assertEq('close.exit', r.status, 0);
    assertEq('close.detached', r.json.detached, true);
    assertEq('close.closed-tabs', r.json.closed_tabs, 1);
    r = step('list', ['list']);
    assertTrue('list.gone', !r.json.sessions.some((s) => s.name === S), 'session detached');

    const after = await userTabs();
    assertEq('user-tabs.after', JSON.stringify(after), JSON.stringify(before));
    assertTrue('chrome.alive', child.exitCode === null, 'user Chrome still running');
  } finally {
    ctx.runScript('bw', ['close', '-s', S], { env });
    child.kill();
    await new Promise((r) => setTimeout(r, 500));
    try { rmSync(ud, { recursive: true, force: true }); } catch { /* locked; temp dir */ }
  }
}
