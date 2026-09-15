// If the Fetch.requestPaused handler itself throws, the request is still failed (never allowed).
import { createFirewall } from '../../scripts/lib/firewall.mjs';
import { FakeCdp } from '../lib/fake-cdp.mjs';
import { assertEq, assertTrue } from '../lib/assert.mjs';

export const name = 'handler-exception-fails-closed';

export async function run() {
  // 1. host parser throws
  let cdp = new FakeCdp();
  let audit = [];
  let fw = createFirewall(cdp, (e) => audit.push(e), { hostOf: () => { throw new Error('boom'); } });
  await fw.enable();
  await cdp.pause('https://claude.ai/new');
  assertEq('throw.verdict', audit.at(-1).verdict, 'blocked');
  assertEq('throw.event', audit.at(-1).event, 'HANDLER_ERROR_BLOCKED');
  assertEq('throw.decision', cdp.sent.at(-1).method, 'Fetch.failRequest');
  assertEq('throw.no-continue', cdp.methods().includes('Fetch.continueRequest'), false);
  assertEq('throw.stats', fw.stats.handler_errors, 1);

  // 2. continueRequest itself fails on an allowlisted host -> fallback failRequest attempted
  cdp = new FakeCdp({ failOn: ['Fetch.continueRequest'] });
  audit = [];
  fw = createFirewall(cdp, (e) => audit.push(e));
  await cdp.pause('https://claude.ai/new');
  assertEq('continue-fail.verdict', audit.at(-1).verdict, 'blocked');
  assertEq('continue-fail.decision', cdp.sent.at(-1).method, 'Fetch.failRequest');

  // 3. audit sink throws -> enforcement unaffected
  cdp = new FakeCdp();
  fw = createFirewall(cdp, () => { throw new Error('audit down'); });
  await cdp.pause('https://evil.example/');
  assertEq('audit-throw.decision', cdp.sent.at(-1).method, 'Fetch.failRequest');
  await cdp.pause('https://claude.ai/');
  assertEq('audit-throw.allowed-still-works', cdp.sent.at(-1).method, 'Fetch.continueRequest');

  // 4. missing params -> blocked
  cdp = new FakeCdp();
  audit = [];
  fw = createFirewall(cdp, (e) => audit.push(e));
  const handlers = cdp.listeners('Fetch.requestPaused');
  await Promise.all(handlers.map((h) => h(undefined)));
  assertTrue('undefined-params', audit.at(-1).verdict === 'blocked', 'blocked');
}
