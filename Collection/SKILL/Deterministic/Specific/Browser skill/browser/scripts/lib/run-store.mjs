// Run directory layout (SPEC-1 Storage Layout) + helpers.
// runs/YYYY-MM-DD/run_<YYYYMMDDTHHMMSSZ>_<4hex>/{run.json,timeline.jsonl,firewall.jsonl,response.md,
//   notifications.json,browser-state.json,observation.json,report.md,screenshots/,artifacts/}
import { createHash, randomBytes } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync, appendFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { DIRS, fwd } from './paths.mjs';

export const sha256File = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');
export const sha256Text = (s) => createHash('sha256').update(String(s)).digest('hex');

export function newRunId(now = new Date()) {
  const stamp = now.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}Z$/, 'Z');
  return `run_${stamp}_${randomBytes(2).toString('hex')}`;
}

export function createRunDir(runId, now = new Date()) {
  const day = now.toISOString().slice(0, 10);
  const dir = join(DIRS.runs, day, runId);
  mkdirSync(join(dir, 'screenshots'), { recursive: true });
  mkdirSync(join(dir, 'artifacts'), { recursive: true });
  return dir;
}

export function findRunDir(runId) {
  if (!existsSync(DIRS.runs)) return null;
  for (const day of readdirSync(DIRS.runs)) {
    const d = join(DIRS.runs, day, runId);
    if (/^\d{4}-\d{2}-\d{2}$/.test(day) && existsSync(d)) return d;
  }
  return null;
}

export function listRuns(limit = 50) {
  if (!existsSync(DIRS.runs)) return [];
  const out = [];
  for (const day of readdirSync(DIRS.runs).filter((d) => /^\d{4}-\d{2}-\d{2}$/.test(d)).sort().reverse()) {
    for (const r of readdirSync(join(DIRS.runs, day)).filter((r) => r.startsWith('run_')).sort().reverse()) {
      out.push({ run_id: r, day, dir: fwd(join(DIRS.runs, day, r)) });
      if (out.length >= limit) return out;
    }
  }
  return out;
}

export class RunStore {
  constructor(dir, runId) {
    this.dir = dir;
    this.runId = runId;
    this.paths = {
      run: join(dir, 'run.json'),
      timeline: join(dir, 'timeline.jsonl'),
      firewall: join(dir, 'firewall.jsonl'),
      response: join(dir, 'response.md'),
      notifications: join(dir, 'notifications.json'),
      browserState: join(dir, 'browser-state.json'),
      observation: join(dir, 'observation.json'),
      report: join(dir, 'report.md'),
      screenshots: join(dir, 'screenshots'),
      artifacts: join(dir, 'artifacts'),
    };
    this.shotSeq = 0;
    this.screenshots = [];
    if (!existsSync(this.paths.firewall)) writeFileSync(this.paths.firewall, '');
  }

  static open(runId) {
    const dir = findRunDir(runId);
    if (!dir) return null;
    const s = new RunStore(dir, runId);
    try { s.screenshots = s.readRun()?.screenshots ?? []; } catch { /* ignore */ }
    return s;
  }

  writeRun(obj) { writeFileSync(this.paths.run, JSON.stringify(obj, null, 2) + '\n'); }
  readRun() { return existsSync(this.paths.run) ? JSON.parse(readFileSync(this.paths.run, 'utf8')) : null; }
  appendFirewall(entry) { appendFileSync(this.paths.firewall, JSON.stringify(entry) + '\n'); }
  writeResponse(text) { writeFileSync(this.paths.response, String(text ?? '')); return { chars: String(text ?? '').length, sha256: sha256Text(text ?? '') }; }
  writeNotifications(arr) { writeFileSync(this.paths.notifications, JSON.stringify(arr, null, 2) + '\n'); }
  writeBrowserState(obj) { writeFileSync(this.paths.browserState, JSON.stringify(obj, null, 2) + '\n'); }
  writeObservation(o) { writeFileSync(this.paths.observation, JSON.stringify(o, null, 2) + '\n'); }

  /** Takes a screenshot named NNN-<slug>.png; returns { file, sha256, event }. Never throws. */
  async screenshot(page, slug, event = 'SCREENSHOT_CAPTURED') {
    const n = String(++this.shotSeq).padStart(3, '0');
    const file = join(this.paths.screenshots, `${n}-${slug.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.png`);
    try {
      await page.screenshot({ path: file, fullPage: false, timeout: 10000 });
      const rec = { file: `screenshots/${n}-${slug.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.png`, sha256: sha256File(file), event, path: fwd(file) };
      this.screenshots.push(rec);
      return rec;
    } catch (e) {
      const rec = { file: null, sha256: null, event, error: String(e?.message ?? e) };
      this.screenshots.push(rec);
      return rec;
    }
  }

  firewallSummary() {
    const s = { allowed: 0, blocked: 0, handler_errors: 0, blocked_hosts: [] };
    const hosts = new Set();
    if (!existsSync(this.paths.firewall)) return s;
    for (const line of readFileSync(this.paths.firewall, 'utf8').split(/\r?\n/)) {
      if (!line) continue;
      let e; try { e = JSON.parse(line); } catch { continue; }
      if (e.event === 'HANDLER_ERROR_BLOCKED') s.handler_errors++;
      else if (e.verdict === 'blocked') { s.blocked++; if (e.host) hosts.add(e.host); }
      else if (e.verdict === 'allowed') s.allowed++;
    }
    s.blocked_hosts = [...hosts].slice(0, 50);
    return s;
  }

  sizeBytes() {
    let total = 0;
    const walk = (d) => { for (const f of readdirSync(d)) { const p = join(d, f); const st = statSync(p); if (st.isDirectory()) walk(p); else total += st.size; } };
    walk(this.dir);
    return total;
  }
}
