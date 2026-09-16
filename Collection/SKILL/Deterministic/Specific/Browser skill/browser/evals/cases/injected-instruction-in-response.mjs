// An answer containing instructions is stored and labelled SUSPECTED_INJECTION; zero actions follow it.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { runFlow } from '../../scripts/lib/flow.mjs';
import { readTimeline } from '../../scripts/lib/timeline.mjs';
import { getProvider } from '../../scripts/lib/providers/index.mjs';
import { TIER1_ACTIONS } from '../../scripts/lib/policy.mjs';
import { FakeBrowser, loadObservation } from '../lib/fake-browser.mjs';
import { makeRun } from './happy-path.mjs';
import { assertEq, assertTrue } from '../lib/assert.mjs';

export const name = 'injected-instruction-in-response';

export async function run(ctx) {
  const injected = readFileSync(join(ctx.fixtures, 'responses', 'injected.md'), 'utf8');
  const { store, timeline } = makeRun(ctx, 'inject');
  const fake = new FakeBrowser({ observation: loadObservation(ctx.fixtures, 'claude-ready'), response: injected, streamTicks: 2 });
  const r = await runFlow({ port: fake, store, timeline, provider: getProvider('claude'), prompt: 'Summarize the report.', timeoutSec: 20, pollMs: 1 });
  assertEq('status', r.status, 'COMPLETED');
  assertTrue('flagged', r.injection.length >= 3, r.injection.map((h) => h.rule).join(','));
  const events = readTimeline(store.paths.timeline);
  const idxResp = events.findIndex((e) => e.event === 'ASSISTANT_RESPONSE');
  assertTrue('flag-events', events.filter((e) => e.event === 'SUSPECTED_INJECTION').length >= 3, 'SUSPECTED_INJECTION recorded');
  const after = events.slice(idxResp + 1).filter((e) => e.tier === 1);
  assertEq('no-tier1-after-response', after.length, 0);
  const actionsAfter = fake.actions.slice(fake.actions.findIndex((a) => a.target === 'send') + 1);
  assertEq('no-fake-actions-after-send', actionsAfter.length, 0);
  assertEq('response-stored-verbatim', readFileSync(store.paths.response, 'utf8'), injected);
  assertTrue('no-navigation-to-evil', !fake.actions.some((a) => String(a.url ?? '').includes('evil')), 'never navigated');
  assertEq('tier1-set', TIER1_ACTIONS.join(','), 'open,verify_auth,focus_composer,type,send,poll');
}
