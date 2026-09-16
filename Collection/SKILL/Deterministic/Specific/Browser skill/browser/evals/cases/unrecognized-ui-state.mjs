// Anything the classifier cannot place with evidence is UNKNOWN. No other branch exists.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { classify } from '../../scripts/lib/classify.mjs';
import { fromFixture } from '../../scripts/lib/observe.mjs';
import { STATES } from '../../scripts/lib/policy.mjs';
import { assertEq, assertTrue } from '../lib/assert.mjs';

export const name = 'unrecognized-ui-state';

export async function run(ctx) {
  const fx = (n) => fromFixture(JSON.parse(readFileSync(join(ctx.fixtures, 'observations', `${n}.json`), 'utf8')));
  let r = classify(fx('claude-unknown'), 'claude');
  assertEq('unknown.state', r.state, 'UNKNOWN');
  assertEq('unknown.blocking', r.blocking, true);
  assertTrue('unknown.evidence', r.evidence && r.evidence.text.length > 0, r.evidence?.text);

  r = classify(fx('claude-ambiguous'), 'claude');
  assertEq('ambiguous.state', r.state, 'UNKNOWN');
  assertEq('ambiguous.evidence', r.evidence.type, 'ambiguous');

  r = classify(fromFixture({ url: 'https://claude.ai/new?incognito=', title: '', aria_yaml: '' }), 'claude');
  assertEq('empty.state', r.state, 'UNKNOWN');

  r = classify(fromFixture({ url: 'https://claude.ai/new?incognito=', title: 'Claude', aria_yaml: '- textbox "prompt a"\n- textbox "prompt b"\n' }), 'claude');
  assertEq('two-composers.state', r.state, 'UNKNOWN');
  assertEq('two-composers.drift', r.drift, true);

  // every state the classifier can emit is in the enum
  for (const n of ['claude-ready', 'claude-login-required', 'claude-usage-limit', 'claude-unknown', 'claude-drift', 'claude-captcha', 'claude-ambiguous']) {
    const s = classify(fx(n), 'claude').state;
    assertTrue(`enum.${n}`, STATES.includes(s), s);
  }
}
