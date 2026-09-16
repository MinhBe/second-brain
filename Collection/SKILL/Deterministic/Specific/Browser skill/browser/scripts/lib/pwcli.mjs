// Strict wrapper around the pinned playwright-cli binary.
// - always spawns node_modules/@playwright/cli/playwright-cli.js with cwd = state/pwcli
//   (so sessions, snapshots and .playwright-cli/ never touch the user's project)
// - appends raw stdout/stderr to state/logs/pwcli-<session>.log
// - parses the documented text output (### sections) and maps errors to exit codes
// All knowledge about playwright-cli's output shape lives here and is tested by
// evals/cases/pwcli-parser.mjs against evals/fixtures/pwcli/*.txt.
import { spawnSync } from 'node:child_process';
import { existsSync, appendFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, resolve, isAbsolute } from 'node:path';
import { EXIT, SkillError } from './exit-codes.mjs';
import { DIRS, FILES, NODE_MODULES, ensureDirs, fwd } from './paths.mjs';

export const PINNED_CLI_VERSION = '0.1.19';
export const SESSION_RE = /^[a-z0-9][a-z0-9-]{0,23}$/;
/** Agent-facing instruction when the user's Chrome does not accept DevTools connections. */
export const ATTACH_HOWTO = 'Ask the user: in their running Chrome open chrome://inspect/#remote-debugging, tick "Allow remote debugging for this browser instance", keep Chrome open, then run this command once more';

export function cliBinPath() {
  const p = join(NODE_MODULES, '@playwright', 'cli', 'playwright-cli.js');
  if (!existsSync(p)) {
    throw new SkillError(EXIT.PRECONDITION, 'playwright-cli is not installed in the skill folder',
      'Run: npm install (inside the skill folder), then node <skill>/scripts/doctor.mjs');
  }
  return p;
}

export function cliVersion() {
  try {
    return JSON.parse(readFileSync(join(NODE_MODULES, '@playwright', 'cli', 'package.json'), 'utf8')).version;
  } catch { return null; }
}

export function assertSession(name) {
  if (!name || !SESSION_RE.test(name)) {
    throw new SkillError(EXIT.USAGE, `Session name must match ${SESSION_RE} (got ${JSON.stringify(name ?? '')})`,
      'Add -s <name> using only lowercase letters, digits and dashes, e.g. -s dash');
  }
  return name;
}

/** Writes state/pwcli/<session>.config.json from config/pwcli.template.json. Returns the absolute path. */
export function writeSessionConfig(session, { headless = false, userDataDir = null } = {}) {
  ensureDirs();
  const tpl = JSON.parse(readFileSync(FILES.pwcliTemplate, 'utf8'));
  delete tpl._comment;
  tpl.browser = tpl.browser ?? {};
  tpl.browser.launchOptions = { ...(tpl.browser.launchOptions ?? {}), headless: !!headless };
  const channel = (process.env.BROWSER_SKILL_CHANNEL ?? 'chrome').toLowerCase();
  if (channel === 'chromium') delete tpl.browser.launchOptions.channel; else tpl.browser.launchOptions.channel = channel;
  if (userDataDir) tpl.browser.userDataDir = fwd(userDataDir); else delete tpl.browser.userDataDir;
  tpl.outputDir = fwd(join(DIRS.pwcli, `out-${session}`));
  mkdirSync(tpl.outputDir, { recursive: true });
  const p = join(DIRS.pwcli, `${session}.config.json`);
  writeFileSync(p, JSON.stringify(tpl, null, 2));
  return p;
}

/**
 * Runs playwright-cli. Returns { status, stdout, stderr, parsed }.
 * opts: { session, json, raw, timeoutMs, config }
 */
export function runCli(args, opts = {}) {
  const bin = cliBinPath();
  ensureDirs();
  const argv = [bin];
  if (opts.session) argv.push(`-s=${opts.session}`);
  if (opts.config) argv.push(`--config=${opts.config}`);
  if (opts.json) argv.push('--json');
  if (opts.raw) argv.push('--raw');
  argv.push(...args);
  const started = Date.now();
  const r = spawnSync(process.execPath, argv, {
    cwd: DIRS.pwcli,
    encoding: 'utf8',
    timeout: opts.timeoutMs ?? 120000,
    windowsHide: true,
    env: { ...process.env, MSYS_NO_PATHCONV: '1' },
    maxBuffer: 32 * 1024 * 1024,
  });
  const stdout = r.stdout ?? '';
  const stderr = r.stderr ?? '';
  const logName = `pwcli-${opts.session ?? 'global'}.log`;
  try {
    const shown = (opts.logArgs ?? argv.slice(1)).map(redactArg).join(' ');
    appendFileSync(join(DIRS.logs, logName),
      `\n=== ${new Date().toISOString()} (${Date.now() - started}ms, exit ${r.status}) playwright-cli ${shown}\n${stripAnsi(stdout)}${stderr ? '[stderr]\n' + stripAnsi(stderr) : ''}`);
  } catch { /* logging must never break a verb */ }
  if (r.error && r.error.code === 'ETIMEDOUT') {
    throw new SkillError(EXIT.TIMEOUT, `playwright-cli did not finish within ${opts.timeoutMs ?? 120000} ms`,
      'Run: node <skill>/scripts/bw.mjs kill-all, then node <skill>/scripts/doctor.mjs');
  }
  if (r.error) {
    throw new SkillError(EXIT.TOOL, `Could not start playwright-cli: ${r.error.message}`,
      'Run: node <skill>/scripts/doctor.mjs');
  }
  const parsed = opts.json ? parseJson(stdout) : (opts.raw ? { raw: stdout } : parseText(stdout));
  return { status: r.status ?? 1, stdout, stderr, parsed };
}

function redactArg(a) {
  return a.length > 200 ? a.slice(0, 200) + '…' : a;
}

export function stripAnsi(s) {
  return String(s ?? '').replace(/\x1b\[[0-9;]*m/g, '').replace(/\[(?:2|22)m/g, '');
}

function parseJson(stdout) {
  try { return JSON.parse(stdout); } catch { return { parseError: true, text: stdout }; }
}

/**
 * Parses the text output. Sections start with "### Name". Returns:
 * { sections, opened:{session,pid}, url, title, console:{errors,warnings}, snapshotFile, snapshotInline, error, modal, result, events }
 */
export function parseText(stdout) {
  const out = { sections: {}, opened: null, attached: null, url: null, title: null, console: null, snapshotFile: null, snapshotInline: null, error: null, modal: null, result: null, events: null };
  const lines = String(stdout ?? '').split(/\r?\n/);
  let current = null;
  const bodies = {};
  for (const line of lines) {
    const h = line.match(/^###\s+(.*)$/);
    if (h) {
      const title = h[1].trim();
      const op = title.match(/^Browser `([^`]+)` opened with pid (\d+)\.?$/);
      if (op) { out.opened = { session: op[1], pid: Number(op[2]) }; current = null; continue; }
      // attach --cdp: "### Session `x` created, attached to `chrome`." then a "Run commands with:" line (ignored)
      const at = title.match(/^Session `([^`]+)` created, attached to `([^`]+)`\.?$/);
      if (at) { out.attached = { session: at[1], endpoint: at[2] }; current = null; continue; }
      current = title;
      bodies[current] = bodies[current] ?? [];
      continue;
    }
    if (current) bodies[current].push(line);
  }
  for (const [k, v] of Object.entries(bodies)) out.sections[k] = v.join('\n').trim();
  const page = out.sections['Page'] ?? '';
  const u = page.match(/^- Page URL:\s*(.*)$/m); if (u) out.url = u[1].trim();
  const t = page.match(/^- Page Title:\s*(.*)$/m); if (t) out.title = t[1].trim();
  const c = page.match(/^- Console:\s*(\d+) errors?,\s*(\d+) warnings?/m); if (c) out.console = { errors: Number(c[1]), warnings: Number(c[2]) };
  const snap = out.sections['Snapshot'] ?? '';
  const sf = snap.match(/\[Snapshot\]\(([^)]+)\)/); if (sf) out.snapshotFile = sf[1].trim();
  const yaml = snap.match(/```yaml\r?\n([\s\S]*?)```/); if (yaml) out.snapshotInline = yaml[1];
  if (out.sections['Error'] !== undefined) {
    const firstLine = stripAnsi(out.sections['Error']).split(/\r?\n/).map((l) => l.trim()).filter(Boolean)[0] ?? '';
    out.error = firstLine.replace(/^(Error|TimeoutError):\s*/, '').trim() || 'unknown error';
  }
  if (out.sections['Modal state'] !== undefined) out.modal = out.sections['Modal state'];
  if (out.sections['Result'] !== undefined) out.result = out.sections['Result'];
  if (out.sections['Events'] !== undefined) out.events = out.sections['Events'];
  // bare-text outputs like "Browser 'cap' closed" or "(no browsers)"
  if (!Object.keys(bodies).length && !out.opened && !out.attached) out.result = String(stdout ?? '').trim();
  return out;
}

/** Resolves a path printed by playwright-cli (relative to its cwd) to an absolute forward-slash path. */
export function resolveCliPath(p) {
  if (!p) return null;
  const clean = String(p).trim();
  return fwd(isAbsolute(clean) ? clean : resolve(DIRS.pwcli, clean));
}

/** Maps a playwright-cli error message to a SkillError with the right exit code and next step. */
export function mapError(message, verb, session) {
  const m = String(message ?? '');
  const s = session ? `-s ${session}` : '';
  if (/Ref e\d+ not found|does not match any elements|strict mode violation|resolved to \d+ elements|not an? (editable|checkbox|select)|Element is not/i.test(m)) {
    return new SkillError(EXIT.TARGET, m, `Run: node <skill>/scripts/bw.mjs snapshot ${s} (or find ${s} --pattern "<text>"), then retry ${verb} once with the new ref`);
  }
  if (/Timeout \d+ms exceeded|Timed out|waiting for/i.test(m) && /locator|getBy|selector|element/i.test(m)) {
    return new SkillError(EXIT.TARGET, m, `Element not found in time. Run: node <skill>/scripts/bw.mjs snapshot ${s}, then retry once`);
  }
  if (/Timeout \d+ms exceeded|Navigation timeout|net::ERR_|ERR_NAME_NOT_RESOLVED|ERR_CONNECTION/i.test(m)) {
    return new SkillError(EXIT.TIMEOUT, m, 'The page did not load. Check the URL with the user; do not retry more than once');
  }
  // attach: the user's Chrome is not accepting DevTools connections (checked before the generic "not found" rule)
  if (/Could not connect to \w+|DevToolsActivePort|ECONNREFUSED 127\.0\.0\.1:\d+/i.test(m)) {
    return new SkillError(EXIT.PRECONDITION, m, ATTACH_HOWTO);
  }
  if (/was not attached|is not attached/i.test(m)) {
    return new SkillError(EXIT.NOT_FOUND, m, `Run: node <skill>/scripts/bw.mjs list (the session is not an attached one)`);
  }
  if (/No (open )?browser|not (found|open|running)|is not open|does not exist|Unknown session|no session/i.test(m)) {
    return new SkillError(EXIT.NOT_FOUND, m, `Run: node <skill>/scripts/bw.mjs open <url> ${s} first (or bw.mjs list to see sessions)`);
  }
  if (/already (open|running|exists)/i.test(m)) {
    return new SkillError(EXIT.BUSY, m, `Session ${session} is already open. Use goto instead of open, or close it first`);
  }
  if (/dialog|Modal state/i.test(m)) {
    return new SkillError(EXIT.TARGET, m, `A dialog is open. Run: node <skill>/scripts/bw.mjs dialog ${s} --accept (or --dismiss), then retry`);
  }
  return new SkillError(EXIT.TOOL, m, `Run: node <skill>/scripts/bw.mjs kill-all, then node <skill>/scripts/doctor.mjs`);
}

/** Convenience: run + throw mapped error when playwright-cli failed. */
export function runOrThrow(args, opts, verb) {
  const r = runCli(args, opts);
  const err = opts.json ? (r.parsed?.isError ? r.parsed.error : null) : r.parsed?.error;
  if (r.status !== 0 || err) {
    // A daemon crash prints a Node stack on stderr; the useful line is "[PlaywrightError: ...".
    const pwe = stripAnsi(r.stderr || '').match(/PlaywrightError: ([^\r\n]+)/);
    const msg = err || pwe?.[1] || (r.stderr || r.stdout || '').trim().split(/\r?\n/).filter(Boolean).slice(0, 3).join(' | ') || `playwright-cli exited ${r.status}`;
    throw mapError(msg, verb, opts.session);
  }
  return r;
}

/** Counts refs in a snapshot file (or inline yaml). */
export function countRefs(snapshotFileOrText, inline = false) {
  try {
    const text = inline ? snapshotFileOrText : readFileSync(snapshotFileOrText, 'utf8');
    return { refs: (text.match(/\[ref=e\d+\]/g) ?? []).length, bytes: Buffer.byteLength(text, 'utf8') };
  } catch { return { refs: null, bytes: null }; }
}
