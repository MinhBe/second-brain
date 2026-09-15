#!/usr/bin/env node
// bwp.mjs — browse inside ONE tab of a chosen profile in the user's RUNNING Chrome.
// Same contract as bw.mjs (one verb, one JSON line). Thin client: verbs are executed by
// lib/bwp-daemon.mjs, which keeps a single DevTools connection open so the human answers
// Chrome's "allow remote debugging" prompt once per Chrome session, not once per command.
import { readFileSync, existsSync, unlinkSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { connect } from 'node:net';
import { spawn } from 'node:child_process';
import { takeVerb } from './lib/args.mjs';
import { EXIT, SkillError } from './lib/exit-codes.mjs';
import { ok, main, helpLine, emit } from './lib/out.mjs';
import { ensureDirs } from './lib/paths.mjs';
import { VERBS, DIR, S } from './lib/bwp-core.mjs';

const FILE = join(DIR, 'daemon.json');
const DAEMON = join(import.meta.dirname, 'lib', 'bwp-daemon.mjs');

function readDaemon() { try { return JSON.parse(readFileSync(FILE, 'utf8')); } catch { return null; } }

function request(info, payload, timeoutMs) {
  return new Promise((res, rej) => {
    const sock = connect({ host: '127.0.0.1', port: info.port });
    let buf = '';
    const t = setTimeout(() => { sock.destroy(); rej(new Error('daemon timeout')); }, timeoutMs);
    sock.setEncoding('utf8');
    sock.once('connect', () => sock.write(JSON.stringify({ token: info.token, ...payload }) + '\n'));
    sock.on('data', (d) => { buf += d; });
    sock.once('error', (e) => { clearTimeout(t); rej(e); });
    sock.once('close', () => { clearTimeout(t); try { res(JSON.parse(buf.trim())); } catch { rej(new Error('daemon closed without a reply')); } });
  });
}

async function ping(info) { try { return (await request(info, { verb: 'daemon', rest: [] }, 3000)).exit === EXIT.OK; } catch { return false; } }

async function ensureDaemon() {
  let info = readDaemon();
  if (info && await ping(info)) return info;
  try { unlinkSync(FILE); } catch { /* none */ }
  mkdirSync(DIR, { recursive: true });
  const child = spawn(process.execPath, [DAEMON], { detached: true, stdio: 'ignore', windowsHide: true, cwd: import.meta.dirname });
  child.unref();
  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, 300));
    info = readDaemon();
    if (info && info.pid === child.pid && await ping(info)) return info;
  }
  throw new SkillError(EXIT.TOOL, 'bwp daemon did not start', `Run: node ${DAEMON} in a terminal to see the error`);
}

async function run() {
  ensureDirs();
  const { verb, rest } = takeVerb(process.argv.slice(2));
  if (!verb || verb === '--help' || verb === 'help') return helpLine('bwp', VERBS, { canonical: `${S} <verb> -s <session> ...` });
  if (!VERBS.includes(verb)) throw new SkillError(EXIT.USAGE, `Unknown verb ${verb}`, `Verbs: ${VERBS.join(', ')}`);
  if (verb === 'daemon' && rest.includes('--stop')) {
    const info = readDaemon();
    if (!info || !(await ping(info))) { try { unlinkSync(FILE); } catch { /* none */ } return ok('daemon', { running: false }, 'No daemon was running'); }
    const r = await request(info, { verb: 'daemon', rest }, 10000).catch(() => null);
    return ok('daemon', { running: false, stopped: true, pid: info.pid, ...(r?.fields ?? {}) }, 'Daemon stopped; the next command starts a new one (Chrome will ask to allow once)');
  }
  const stdin = rest.includes('--stdin') ? readFileSync(0, 'utf8').replace(/\r?\n$/, '') : undefined;
  const info = await ensureDaemon();
  const r = await request(info, { verb, rest, stdin }, 240000);
  if (r.exit !== EXIT.OK) throw new SkillError(r.exit, r.error ?? 'error', r.next ?? '', r.fields ?? {});
  return emit(r.verb ?? verb, EXIT.OK, r.fields ?? {}, r.next ?? '');
}

main('bwp', async () => {
  const { verb } = takeVerb(process.argv.slice(2));
  try { await run(); } catch (e) { if (e instanceof SkillError && VERBS.includes(verb)) e.verb = verb; throw e; }
  finally { setTimeout(() => process.exit(process.exitCode ?? 0), 100).unref(); }
});
