// Hash-chained JSONL timeline (Layer 5). Each line carries sha256 of the previous line's exact bytes.
import { createHash } from 'node:crypto';
import { appendFileSync, readFileSync, writeFileSync } from 'node:fs';
import { EVENTS, TIERS } from './policy.mjs';

export const sha256 = (s) => createHash('sha256').update(s).digest('hex');
const GENESIS = sha256('');
const KNOWN = new Set(EVENTS);

export class Timeline {
  constructor(path, { strict = true } = {}) {
    this.path = path;
    this.seq = 0;
    this.prev = GENESIS;
    this.strict = strict;
    this.listeners = [];
    writeFileSync(path, '');
  }

  onEvent(fn) { this.listeners.push(fn); }

  /** Appends one event. tier: 0 observe, 1 interact, 2 human, null = bookkeeping. */
  append(event, data = {}, tier = null) {
    if (this.strict && !KNOWN.has(event)) throw new Error(`Unknown timeline event: ${event}`);
    if (tier !== null && !Object.values(TIERS).includes(tier)) throw new Error(`Bad tier: ${tier}`);
    const rec = { seq: ++this.seq, ts: new Date().toISOString(), event, tier, data, prev_sha256: this.prev };
    const line = JSON.stringify(rec);
    appendFileSync(this.path, line + '\n');
    this.prev = sha256(line);
    for (const fn of this.listeners) { try { fn(rec); } catch { /* listeners never break the chain */ } }
    return rec;
  }

  head() { return this.prev; }
}

/** Recomputes the chain. Returns { ok, events, head } or { ok:false, broken_at, reason }. */
export function verifyChain(path) {
  const lines = readFileSync(path, 'utf8').split(/\r?\n/).filter((l) => l.length);
  let prev = GENESIS;
  for (let i = 0; i < lines.length; i++) {
    let rec;
    try { rec = JSON.parse(lines[i]); } catch { return { ok: false, broken_at: i + 1, reason: 'unparsable line' }; }
    if (rec.prev_sha256 !== prev) return { ok: false, broken_at: i + 1, reason: 'prev_sha256 mismatch' };
    if (rec.seq !== i + 1) return { ok: false, broken_at: i + 1, reason: 'seq gap' };
    prev = sha256(lines[i]);
  }
  return { ok: true, events: lines.length, head: prev };
}

export function readTimeline(path) {
  return readFileSync(path, 'utf8').split(/\r?\n/).filter((l) => l.length).map((l) => JSON.parse(l));
}
