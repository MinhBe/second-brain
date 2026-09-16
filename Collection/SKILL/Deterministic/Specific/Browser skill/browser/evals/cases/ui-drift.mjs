// A redesigned composer (no ladder step matches) is ADAPTER_DRIFT -> UNKNOWN, with zero actions.
// The flow-level half (fake browser, no click/type/send) is added by the happy-path/flow evals in Phase C.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { classify, findComposerInAria } from '../../scripts/lib/classify.mjs';
import { fromFixture } from '../../scripts/lib/observe.mjs';
import { assertEq, assertTrue } from '../lib/assert.mjs';

export const name = 'ui-drift';

export async function run(ctx) {
  const o = fromFixture(JSON.parse(readFileSync(join(ctx.fixtures, 'observations', 'claude-drift.json'), 'utf8')));
  const c = findComposerInAria(o, 'claude');
  assertEq('composer.found', c.found, 0);
  const r = classify(o, 'claude');
  assertEq('state', r.state, 'UNKNOWN');
  assertEq('drift', r.drift, true);
  assertTrue('evidence', /no composer candidate/.test(r.evidence.text), r.evidence.text);
}
