// A usage-limit banner is classified USAGE_EXHAUSTED with raw text kept and reset time parsed.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { classify } from '../../scripts/lib/classify.mjs';
import { fromFixture } from '../../scripts/lib/observe.mjs';
import { parseResetTime, nextLocalTime } from '../../scripts/lib/providers/claude.mjs';
import { assertEq, assertTrue, assertMatch } from '../lib/assert.mjs';

export const name = 'usage-limit';

export async function run(ctx) {
  const o = fromFixture(JSON.parse(readFileSync(join(ctx.fixtures, 'observations', 'claude-usage-limit.json'), 'utf8')));
  const r = classify(o, 'claude');
  assertEq('state', r.state, 'USAGE_EXHAUSTED');
  assertEq('blocking', r.blocking, true);
  assertMatch('evidence-raw', r.evidence.text, /out of free messages/i);
  const reset = parseResetTime(o.alerts[0]);
  assertEq('reset.time', reset.time, '05:40');
  assertEq('reset.raw', reset.raw, 'until 5:40 AM');
  const until = nextLocalTime(reset.time, new Date('2026-09-11T07:20:23Z'));
  assertTrue('reset.future', Date.parse(until) > Date.parse('2026-09-11T07:20:23Z'), until);
  assertEq('pm-parse', parseResetTime('You are out of messages until 11:05 PM').time, '23:05');
  assertEq('noon-parse', parseResetTime('until 12 PM').time, '12:00');
  assertEq('none', parseResetTime('no time here'), null);
}
