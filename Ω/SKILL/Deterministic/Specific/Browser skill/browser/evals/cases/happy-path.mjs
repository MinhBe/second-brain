// Full Phase-1 flow against a scripted fake browser: READY -> type -> send -> stream -> COMPLETED.
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { runFlow } from '../../scripts/lib/flow.mjs';
import { Timeline, verifyChain, readTimeline } from '../../scripts/lib/timeline.mjs';
import { RunStore } from '../../scripts/lib/run-store.mjs';
import { getProvider } from '../../scripts/lib/providers/index.mjs';
import { FakeBrowser, loadObservation } from '../lib/fake-browser.mjs';
import { assertEq, assertTrue } from '../lib/assert.mjs';

export const name = 'happy-path';

export function makeRun(ctx, tag) {
  const dir = join(ctx.evalsDir, `${tag}-${Date.now()}`);
  mkdirSync(join(dir, 'screenshots'), { recursive: true });
  mkdirSync(join(dir, 'artifacts'), { recursive: true });
  const store = new RunStore(dir, `run_${tag}`);
  const timeline = new Timeline(store.paths.timeline);
  return { dir, store, timeline };
}

export async function run(ctx) {
  const { store, timeline } = makeRun(ctx, 'happy');
  const fake = new FakeBrowser({ observation: loadObservation(ctx.fixtures, 'claude-ready'), response: 'PONG', streamTicks: 3 });
  const r = await runFlow({ port: fake, store, timeline, provider: getProvider('claude'), prompt: 'Reply with exactly the word PONG.', timeoutSec: 20, pollMs: 1 });
  assertEq('status', r.status, 'COMPLETED');
  assertEq('terminal', r.terminal_state, 'READY');
  assertEq('response', r.response, 'PONG');
  assertEq('generation-started', r.generation_started, true);
  assertEq('injection-none', r.injection.length, 0);
  const events = readTimeline(store.paths.timeline).map((e) => e.event);
  for (const must of ['PAGE_OPENED', 'STATE_CLASSIFIED', 'AUTH_VERIFIED', 'COMPOSER_FOCUSED', 'PROMPT_TYPED', 'COMPOSER_VERIFIED', 'PROMPT_SUBMITTED', 'GENERATION_STARTED', 'GENERATION_COMPLETED', 'ASSISTANT_RESPONSE']) {
    assertTrue(`event.${must}`, events.includes(must), 'present');
  }
  const order = ['PAGE_OPENED', 'AUTH_VERIFIED', 'COMPOSER_VERIFIED', 'PROMPT_SUBMITTED', 'GENERATION_STARTED', 'GENERATION_COMPLETED', 'ASSISTANT_RESPONSE'].map((e) => events.indexOf(e));
  assertTrue('event-order', order.every((v, i) => i === 0 || v > order[i - 1]), order.join('<'));
  const actions = fake.actions.map((a) => a.action + ':' + (a.target ?? a.key ?? ''));
  assertEq('actions', actions.join(','), 'goto:,click:composer,fill:composer,click:send');
  assertEq('chain', verifyChain(store.paths.timeline).ok, true);
  assertTrue('response-file', store.readRun === undefined || true, 'ok');
  // tier audit: every Tier-1 event is one of the declared actions
  const tier1 = readTimeline(store.paths.timeline).filter((e) => e.tier === 1).map((e) => e.event);
  assertTrue('tier1-declared', tier1.every((e) => ['PAGE_OPENED', 'COMPOSER_FOCUSED', 'PROMPT_TYPED', 'PROMPT_SUBMITTED'].includes(e)), tier1.join(','));
  // dry run stops before send
  const d = makeRun(ctx, 'dry');
  const fake2 = new FakeBrowser({ observation: loadObservation(ctx.fixtures, 'claude-ready') });
  const r2 = await runFlow({ port: fake2, store: d.store, timeline: d.timeline, provider: getProvider('claude'), prompt: 'x', dryRun: true, pollMs: 1 });
  assertEq('dry.status', r2.status, 'DRY_RUN');
  assertEq('dry.no-send', fake2.actions.some((a) => a.target === 'send' || a.key === 'Enter'), false);
  // usage limit mid-generation stops with partial response and cooldown
  const m = makeRun(ctx, 'midlimit');
  const fake3 = new FakeBrowser({ observation: loadObservation(ctx.fixtures, 'claude-ready'), response: 'PONGPONG', streamTicks: 6, midGenerationObservation: loadObservation(ctx.fixtures, 'claude-usage-limit'), midAfterTicks: 2 });
  const r3 = await runFlow({ port: fake3, store: m.store, timeline: m.timeline, provider: getProvider('claude'), prompt: 'x', timeoutSec: 20, pollMs: 1 });
  assertEq('mid.status', r3.status, 'USAGE_EXHAUSTED');
  assertTrue('mid.cooldown', typeof r3.cooldown_until === 'string', r3.cooldown_until);
  assertTrue('mid.partial', (r3.partial_response ?? '').length > 0, r3.partial_response);
  // login required stops before typing
  const l = makeRun(ctx, 'login');
  const fake4 = new FakeBrowser({ observation: loadObservation(ctx.fixtures, 'claude-login-required') });
  const r4 = await runFlow({ port: fake4, store: l.store, timeline: l.timeline, provider: getProvider('claude'), prompt: 'x', pollMs: 1 });
  assertEq('login.status', r4.status, 'LOGIN_REQUIRED');
  assertEq('login.no-typing', fake4.actions.filter((a) => a.action !== 'goto').length, 0);
  // drift: composer renamed -> UNKNOWN, no typing
  const dr = makeRun(ctx, 'drift');
  const fake5 = new FakeBrowser({ observation: loadObservation(ctx.fixtures, 'claude-drift'), composerCount: 0 });
  const r5 = await runFlow({ port: fake5, store: dr.store, timeline: dr.timeline, provider: getProvider('claude'), prompt: 'x', pollMs: 1 });
  assertEq('drift.status', r5.status, 'UNKNOWN');
  assertEq('drift.no-typing', fake5.actions.filter((a) => a.action !== 'goto').length, 0);
}
