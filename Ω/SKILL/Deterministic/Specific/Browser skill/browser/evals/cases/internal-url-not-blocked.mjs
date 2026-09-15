// Internal browser URLs pass Layer 0 without a host check; everything off-allowlist is failed.
import { createFirewall } from '../../scripts/lib/firewall.mjs';
import { FakeCdp } from '../lib/fake-cdp.mjs';
import { assertEq, assertTrue } from '../lib/assert.mjs';

export const name = 'internal-url-not-blocked';

export async function run() {
  const cdp = new FakeCdp();
  const audit = [];
  const fw = createFirewall(cdp, (e) => audit.push(e));
  await fw.enable();
  assertEq('fetch-enable-first', cdp.methods()[0], 'Fetch.enable');
  assertEq('fetch-enable-pattern', cdp.sent[0].params.patterns[0].urlPattern, '*');
  const internal = ['about:blank', 'chrome://newtab/', 'devtools://devtools/bundled/inspector.html', 'data:text/html,<h1>x</h1>', 'blob:https://claude.ai/123'];
  for (const u of internal) await cdp.pause(u);
  const verdicts = audit.map((a) => a.verdict);
  assertTrue('all-internal-allowed', verdicts.every((v) => v === 'allowed'), verdicts.join(','));
  assertEq('no-fail-yet', cdp.methods().filter((m) => m === 'Fetch.failRequest').length, 0);
  assertEq('internal-count', fw.stats.internal, internal.length);
  // allowlisted host passes, case-insensitively
  await cdp.pause('https://CLAUDE.ai/new');
  assertEq('allowlist-case', audit.at(-1).verdict, 'allowed');
  // off-allowlist fails with BlockedByClient
  await cdp.pause('https://evil.example/x');
  assertEq('evil-blocked', audit.at(-1).verdict, 'blocked');
  assertEq('evil-decision', cdp.sent.at(-1).method, 'Fetch.failRequest');
  assertEq('evil-reason', cdp.sent.at(-1).params.errorReason, 'BlockedByClient');
  // redirect target on another host is a fresh pause -> blocked
  await cdp.pause('https://www.claude.ai/', { resourceType: 'Document' });
  assertEq('www-not-stripped', audit.at(-1).verdict, 'blocked');
  // malformed URL -> handler error -> blocked
  await cdp.pause('not a url');
  assertEq('malformed-blocked', audit.at(-1).verdict, 'blocked');
  assertEq('malformed-flagged', audit.at(-1).event, 'HANDLER_ERROR_BLOCKED');
}
