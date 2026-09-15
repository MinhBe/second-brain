#!/usr/bin/env node
// doctor.mjs — environment, pins, dirs, ACL, policy hash, playwright-cli health.
import { existsSync, readFileSync, writeFileSync, readdirSync, unlinkSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { connect } from 'node:net';
import { parseArgs } from './lib/args.mjs';
import { EXIT } from './lib/exit-codes.mjs';
import { emit, main, helpLine, log } from './lib/out.mjs';
import { DIRS, FILES, CANONICAL, ensureDirs, tsForFile, fwd, NODE_MODULES } from './lib/paths.mjs';
import { cliVersion, PINNED_CLI_VERSION, runCli } from './lib/pwcli.mjs';
import { policySha256 } from './lib/policy.mjs';
import { isOwnerOnly, restrict } from './lib/acl.mjs';
import { findChrome, chromeDevToolsPort } from './lib/chrome.mjs';

const PORTS = [3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010, 4200, 5173, 5174, 8000, 8080, 8888];

async function run() {
  const { flags } = parseArgs(process.argv.slice(2), { flags: { fix: { type: 'bool' }, ports: { type: 'bool' }, help: { type: 'bool' } } }, `Usage: node ${CANONICAL}/scripts/doctor.mjs [--fix] [--ports]`);
  if (flags.help) return helpLine('doctor', ['(no verbs) [--fix] [--ports]']);
  ensureDirs();
  const checks = {};
  const details = [];
  const add = (name, status, detail) => { checks[name] = status; details.push(`[${status.toUpperCase()}] ${name}: ${detail}`); };

  // node
  const major = Number(process.versions.node.split('.')[0]);
  add('node', major >= 20 ? 'ok' : 'fail', `node ${process.versions.node} (need >= 20)`);

  // pins
  const pkg = JSON.parse(readFileSync(FILES.packageJson, 'utf8'));
  const wantCli = pkg.dependencies['@playwright/cli'];
  const haveCli = cliVersion();
  add('pwcli', haveCli === wantCli && haveCli === PINNED_CLI_VERSION ? 'ok' : 'fail', `@playwright/cli installed=${haveCli ?? 'missing'} pinned=${wantCli}`);
  let havePw = null;
  try { havePw = JSON.parse(readFileSync(join(NODE_MODULES, 'playwright', 'package.json'), 'utf8')).version; } catch { /* missing */ }
  add('playwright', havePw === pkg.dependencies.playwright ? 'ok' : 'fail', `playwright installed=${havePw ?? 'missing'} pinned=${pkg.dependencies.playwright}`);

  // browser
  const channel = (process.env.BROWSER_SKILL_CHANNEL ?? 'chrome').toLowerCase();
  let chrome_version = null;
  if (channel === 'chrome') {
    const c = findChrome();
    chrome_version = c?.version ?? null;
    add('chrome', c ? 'ok' : 'fail', c ? `${c.path} (${c.version ?? 'version unknown'})` : 'Google Chrome not found; install Chrome or set BROWSER_SKILL_CHANNEL=chromium after npx playwright install chromium');
  } else {
    try {
      const { chromium } = await import('playwright');
      const p = chromium.executablePath();
      add('chrome', existsSync(p) ? 'ok' : 'fail', `bundled chromium ${p}`);
    } catch (e) { add('chrome', 'fail', `cannot resolve bundled chromium: ${e.message}`); }
  }

  // user's running Chrome accepting DevTools connections (needed only by bw.mjs attach; never a failure)
  const dbg = await chromeDevToolsPort();
  add('chrome_remote_debugging', dbg.open ? 'ok' : 'warn', dbg.open
    ? `user Chrome accepts DevTools on 127.0.0.1:${dbg.port}; bw.mjs attach is available`
    : `off (${dbg.port ? `port ${dbg.port} closed` : 'DevToolsActivePort missing'}); bw.mjs attach needs the human to tick "Allow remote debugging" at chrome://inspect/#remote-debugging`);

  // dirs writable
  let dirsOk = true; const bad = [];
  for (const [k, d] of Object.entries(DIRS)) {
    try { mkdirSync(d, { recursive: true }); const t = join(d, `.doctor-${process.pid}`); writeFileSync(t, 'x'); unlinkSync(t); } catch { dirsOk = false; bad.push(k); }
  }
  add('dirs', dirsOk ? 'ok' : 'fail', dirsOk ? `all runtime dirs writable under ${fwd(DIRS.state)}/..` : `not writable: ${bad.join(', ')}`);

  // ACL on profiles/ and state/
  for (const [k, d] of [['acl_profiles', DIRS.profiles], ['acl_state', DIRS.state]]) {
    let a = isOwnerOnly(d);
    if (!a.ok && flags.fix) { const r = restrict(d); a = isOwnerOnly(d); a.fixed = r.ok; }
    add(k, a.ok ? 'ok' : 'warn', a.ok ? `${fwd(d)} restricted to owner/SYSTEM/Administrators${a.fixed ? ' (fixed)' : ''}` : `${fwd(d)} also grants: ${(a.extra ?? []).join(', ') || a.reason}; run doctor --fix`);
  }

  // policy hash
  let pinned = null;
  try { pinned = readFileSync(FILES.policyHash, 'utf8').trim(); } catch { /* missing */ }
  const actual = policySha256();
  add('policy', pinned && pinned === actual ? 'ok' : 'fail', pinned === actual ? `policy.mjs sha256 ${actual.slice(0, 12)} matches pin` : `policy.mjs sha256 ${actual.slice(0, 12)} != pinned ${(pinned ?? 'none').slice(0, 12)}; a policy change needs review + updating evals/fixtures/policy.sha256`);

  // registry sanity
  if (existsSync(FILES.registry)) {
    try {
      const reg = JSON.parse(readFileSync(FILES.registry, 'utf8'));
      const real = join(process.env.LOCALAPPDATA ?? '', 'Google', 'Chrome', 'User Data').toLowerCase();
      const offenders = (reg.profiles ?? []).filter((p) => String(p.automation_user_data_dir ?? '').toLowerCase().startsWith(real));
      add('registry', offenders.length ? 'fail' : 'ok', offenders.length ? `profiles point at the real Chrome User Data dir: ${offenders.map((p) => p.id).join(', ')}` : `${(reg.profiles ?? []).length} profile(s), none use the real Chrome User Data dir`);
    } catch (e) { add('registry', 'fail', `profiles.json unreadable: ${e.message}`); }
  } else {
    add('registry', 'ok', 'no profiles registered yet');
  }

  // runs git (Layer 5 lite)
  if (existsSync(join(DIRS.runs, '.git'))) {
    const r = spawnSync('git', ['-C', DIRS.runs, 'remote'], { encoding: 'utf8', windowsHide: true });
    const remotes = (r.stdout ?? '').trim().split(/\r?\n/).filter(Boolean);
    add('runs_git', remotes.length ? 'ok' : 'warn', remotes.length ? `runs/ repo pushes to ${remotes.join(', ')}` : 'runs/ is a git repo without a remote; audit push disabled');
  } else {
    add('runs_git', 'warn', 'runs/ is not a git repo; audit push disabled (hash chain still on)');
  }

  // playwright-cli responds
  try {
    const r = runCli(['list'], { json: true, timeoutMs: 60000 });
    writeFileSync(join(DIRS.doctor, 'pwcli-list.txt'), r.stdout + (r.stderr ? '\n[stderr]\n' + r.stderr : ''));
    add('pwcli_list', r.status === 0 ? 'ok' : 'fail', r.status === 0 ? `${(r.parsed?.browsers ?? []).length} session(s) open` : `playwright-cli list exited ${r.status}`);
  } catch (e) { add('pwcli_list', 'fail', e.message); }

  // console code page
  const cp = spawnSync('cmd.exe', ['/c', 'chcp'], { encoding: 'utf8', windowsHide: true });
  const cpn = Number((cp.stdout ?? '').match(/(\d+)/)?.[1] ?? 0);
  add('codepage', cpn === 65001 || cpn === 0 ? 'ok' : 'warn', cpn ? `console code page ${cpn}${cpn !== 65001 ? ' (non-ASCII paths may display oddly; harmless)' : ''}` : 'could not read code page');

  // optional ports
  let open_ports;
  if (flags.ports) {
    open_ports = (await Promise.all(PORTS.map((port) => new Promise((res) => {
      const s = connect({ host: '127.0.0.1', port, timeout: 400 });
      s.once('connect', () => { s.destroy(); res(port); }); s.once('error', () => res(null)); s.once('timeout', () => { s.destroy(); res(null); });
    })))).filter(Boolean);
    add('ports', 'ok', open_ports.length ? `local servers on ${open_ports.join(', ')}` : 'no local dev server');
  }

  const fail = Object.values(checks).filter((s) => s === 'fail').length;
  const warn = Object.values(checks).filter((s) => s === 'warn').length;
  const report = join(DIRS.doctor, `${tsForFile()}.txt`);
  writeFileSync(report, details.join('\n') + '\n');
  for (const d of details) log(d);
  const fields = { checks, fail, warn, chrome_version, channel, chrome_devtools_port: dbg.open ? dbg.port : null, report_path: fwd(report) };
  if (open_ports) fields.open_ports = open_ports;
  return emit('doctor', fail ? EXIT.PRECONDITION : EXIT.OK, fields,
    fail ? `Fix the [FAIL] items listed in report_path, then run doctor again` : `Environment OK. General browsing: node ${CANONICAL}/scripts/bw.mjs open <url> -s <name>. Observer: node ${CANONICAL}/scripts/profile.mjs list`);
}

main('doctor', run);
