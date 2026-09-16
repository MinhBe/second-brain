#!/usr/bin/env node
// evals/run.mjs — runs evals/cases/*.mjs. No LLM in the loop.
//   node evals/run.mjs [--browser] [--only <name>] [--token-check]
// Each case exports { name, needsBrowser?, skip?, run(ctx) }.
// stderr: STEP_PASS|<case>|<evidence> / STEP_FAIL|<case>|<expected> -> <actual>|<artifact>
// stdout: one JSON line.
import { readdirSync, writeFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { spawnSync, spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { parseArgs } from '../scripts/lib/args.mjs';
import { EXIT } from '../scripts/lib/exit-codes.mjs';
import { emit, main, log, MAX_STDOUT_BYTES } from '../scripts/lib/out.mjs';
import { SKILL_ROOT, DIRS, ensureDirs, tsForFile, fwd } from '../scripts/lib/paths.mjs';
import { EvalFailure, stepFail, stepPass } from './lib/assert.mjs';

const CASES_DIR = join(SKILL_ROOT, 'evals', 'cases');

function runScript(script, args = [], opts = {}) {
  const file = script.endsWith('.mjs') ? resolve(SKILL_ROOT, script) : join(SKILL_ROOT, 'scripts', `${script}.mjs`);
  const r = spawnSync(process.execPath, [file, ...args], {
    encoding: 'utf8', cwd: opts.cwd ?? SKILL_ROOT, input: opts.input, timeout: opts.timeoutMs ?? 180000, windowsHide: true,
    env: { ...process.env, ...(opts.env ?? {}) },
  });
  const stdout = r.stdout ?? '';
  const lines = stdout.split(/\r?\n/).filter((l) => l.length);
  let json = null;
  try { json = JSON.parse(lines[lines.length - 1] ?? ''); } catch { /* not json */ }
  return { status: r.status, stdout, stderr: r.stderr ?? '', lines, json, bytes: Buffer.byteLength(lines[lines.length - 1] ?? '', 'utf8') };
}

async function run() {
  const { flags } = parseArgs(process.argv.slice(2), { flags: { browser: { type: 'bool' }, only: { type: 'string' }, 'token-check': { type: 'bool' }, online: { type: 'bool' } } }, 'Usage: node evals/run.mjs [--browser] [--only <case>] [--token-check] [--online]');
  ensureDirs();
  mkdirSync(DIRS.evals, { recursive: true });
  const files = readdirSync(CASES_DIR).filter((f) => f.endsWith('.mjs')).sort();
  const results = [];
  let server = null;
  const ctx = {
    skillRoot: SKILL_ROOT,
    runScript,
    browser: !!flags.browser,
    online: !!flags.online,
    tokenCheck: !!flags['token-check'],
    maxBytes: MAX_STDOUT_BYTES,
    evalsDir: DIRS.evals,
    fixtures: join(SKILL_ROOT, 'evals', 'fixtures'),
    log,
    // The fixture server runs in a CHILD process: runScript() blocks this process
    // synchronously, so an in-process server could never answer Chrome.
    async server() {
      if (server) return server;
      const hitsFile = join(DIRS.evals, `hits-${tsForFile()}.jsonl`);
      writeFileSync(hitsFile, '');
      const child = spawn(process.execPath, [join(SKILL_ROOT, 'evals', 'lib', 'static-server.mjs'), '--port', '0', '--hits-file', hitsFile], { stdio: ['ignore', 'pipe', 'inherit'], windowsHide: true });
      const first = await new Promise((res, rej) => {
        let buf = '';
        child.stdout.on('data', (d) => { buf += d; const i = buf.indexOf('\n'); if (i >= 0) res(buf.slice(0, i)); });
        child.once('exit', (c) => rej(new Error(`static server exited ${c}`)));
        setTimeout(() => rej(new Error('static server did not start in 10 s')), 10000).unref();
      });
      const info = JSON.parse(first);
      server = {
        port: info.port,
        url: info.url,
        hits: () => readFileSync(hitsFile, 'utf8').split(/\r?\n/).filter(Boolean).map((l) => JSON.parse(l)),
        close: () => new Promise((res) => { child.once('exit', () => res()); child.kill(); setTimeout(res, 3000).unref(); }),
      };
      return server;
    },
    checkLine(id, r) {
      if (!ctx.tokenCheck) return;
      if (r.lines.length !== 1) throw new EvalFailure(`${id}.one-line`, '1 stdout line', `${r.lines.length} lines`);
      if (r.bytes > MAX_STDOUT_BYTES) throw new EvalFailure(`${id}.bytes`, `<= ${MAX_STDOUT_BYTES}`, `${r.bytes}`);
      stepPass(`${id}.token`, `${r.bytes} bytes`);
    },
  };
  for (const f of files) {
    const name = f.replace(/\.mjs$/, '');
    if (flags.only && flags.only !== name) continue;
    let mod;
    try { mod = await import(pathToFileURL(join(CASES_DIR, f)).href); } catch (e) { results.push({ name, status: 'failed', detail: `import: ${e.message}` }); stepFail(name, 'import ok', e.message); continue; }
    if (mod.skip) { results.push({ name, status: 'skipped', detail: mod.skip }); log(`SKIP|${name}|${mod.skip}`); continue; }
    if (mod.needsBrowser && !flags.browser) { results.push({ name, status: 'skipped', detail: 'needs --browser' }); log(`SKIP|${name}|needs --browser`); continue; }
    if (mod.needsOnline && !flags.online) { results.push({ name, status: 'skipped', detail: 'needs --online' }); log(`SKIP|${name}|needs --online`); continue; }
    const started = Date.now();
    try {
      await mod.run(ctx);
      results.push({ name, status: 'passed', ms: Date.now() - started });
      stepPass(name, `passed in ${Date.now() - started} ms`);
    } catch (e) {
      const detail = e instanceof EvalFailure ? `${e.id}: expected ${e.expected}, got ${e.actual}` : String(e?.stack ?? e);
      results.push({ name, status: 'failed', detail, ms: Date.now() - started });
      stepFail(e instanceof EvalFailure ? `${name}:${e.id}` : name, e instanceof EvalFailure ? e.expected : 'no throw', e instanceof EvalFailure ? e.actual : String(e?.message ?? e), e?.artifact ?? '');
    }
  }
  if (server) await server.close();
  const passed = results.filter((r) => r.status === 'passed').length;
  const failed = results.filter((r) => r.status === 'failed').length;
  const skipped = results.filter((r) => r.status === 'skipped').length;
  const report = join(DIRS.logs, `evals-${tsForFile()}.txt`);
  writeFileSync(report, results.map((r) => `${r.status.toUpperCase().padEnd(7)} ${r.name}${r.ms ? ` (${r.ms} ms)` : ''}${r.detail ? `\n        ${r.detail}` : ''}`).join('\n') + '\n');
  const failedNames = results.filter((r) => r.status === 'failed').map((r) => r.name);
  return emit('evals', failed ? EXIT.PRECONDITION : EXIT.OK, { passed, failed, skipped, browser: !!flags.browser, token_check: !!flags['token-check'], failed_cases: failedNames, report_path: fwd(report) },
    failed ? `Read report_path for the failing cases` : 'All evals green');
}

main('evals', run);
