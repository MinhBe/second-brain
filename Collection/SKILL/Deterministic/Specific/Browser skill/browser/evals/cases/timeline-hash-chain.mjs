// Timeline lines are hash-chained; tampering is detected; unknown events are rejected.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { Timeline, verifyChain, sha256 } from '../../scripts/lib/timeline.mjs';
import { assertEq, assertTrue, assertThrows } from '../lib/assert.mjs';

export const name = 'timeline-hash-chain';

export async function run(ctx) {
  mkdirSync(ctx.evalsDir, { recursive: true });
  const p = join(ctx.evalsDir, `timeline-${Date.now()}.jsonl`);
  const t = new Timeline(p);
  t.append('RUN_STARTED', { run_id: 'x' });
  t.append('PAGE_OPENED', { url: 'https://claude.ai/new' }, 1);
  t.append('AUTH_VERIFIED', {}, 0);
  t.append('PROMPT_SUBMITTED', { chars: 4 }, 1);
  t.append('RUN_COMPLETED', {}, null);
  const v = verifyChain(p);
  assertEq('verify.ok', v.ok, true);
  assertEq('verify.events', v.events, 5);
  assertEq('head-matches', v.head, t.head());
  const lines = readFileSync(p, 'utf8').split('\n');
  assertEq('genesis', JSON.parse(lines[0]).prev_sha256, sha256(''));
  // tamper with line 3
  lines[2] = lines[2].replace('"tier":0', '"tier":2');
  writeFileSync(p, lines.join('\n'));
  const bad = verifyChain(p);
  assertEq('tamper.detected', bad.ok, false);
  assertEq('tamper.line', bad.broken_at, 4);
  // deleting a line also breaks
  writeFileSync(p, lines.filter((_, i) => i !== 1).join('\n'));
  assertEq('delete.detected', verifyChain(p).ok, false);
  await assertThrows('unknown-event', () => t.append('MAKE_IT_SO'), /Unknown timeline event/);
  await assertThrows('bad-tier', () => t.append('RUN_FAILED', {}, 7), /Bad tier/);
  assertTrue('done', true, 'chain semantics hold');
}
