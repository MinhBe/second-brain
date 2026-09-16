// The compiled-in policy cannot be mutated at runtime and matches its pinned hash.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { OBSERVER_ALLOWLIST, LOGIN_EXTRA_HOSTS, RESERVED_HOSTS, isReservedHost, policySha256 } from '../../scripts/lib/policy.mjs';
import { assertEq, assertTrue, assertThrows } from '../lib/assert.mjs';

export const name = 'allowlist-frozen';

export async function run(ctx) {
  await assertThrows('add-throws', () => OBSERVER_ALLOWLIST.add('evil.com'), /immutable/);
  await assertThrows('delete-throws', () => OBSERVER_ALLOWLIST.delete('claude.ai'), /immutable/);
  await assertThrows('clear-throws', () => OBSERVER_ALLOWLIST.clear(), /immutable/);
  await assertThrows('login-add-throws', () => LOGIN_EXTRA_HOSTS.add('evil.com'), /immutable/);
  assertEq('size', OBSERVER_ALLOWLIST.size, 5);
  assertTrue('exact-hosts', ['claude.ai', 'chatgpt.com', 'www.meta.ai', 'challenges.cloudflare.com', 'assets-proxy.anthropic.com'].every((h) => OBSERVER_ALLOWLIST.has(h)), 'claude.ai, chatgpt.com, www.meta.ai, challenges.cloudflare.com, assets-proxy.anthropic.com');
  assertEq('no-www-stripping', OBSERVER_ALLOWLIST.has('meta.ai'), false);
  assertEq('no-cloudflare-wildcard', OBSERVER_ALLOWLIST.has('cloudflare.com'), false);
  assertEq('reserved-subdomain', isReservedHost('chat.chatgpt.com'), true);
  assertEq('reserved-lookalike', isReservedHost('claude.ai.evil.com'), false);
  assertEq('reserved-suffix-trick', isReservedHost('notclaude.ai'), false);
  const pinned = readFileSync(join(ctx.skillRoot, 'evals', 'fixtures', 'policy.sha256'), 'utf8').trim();
  assertEq('policy-hash-pinned', policySha256(), pinned);
  assertTrue('reserved-covers-providers', ['claude.ai', 'chatgpt.com', 'www.meta.ai'].every((h) => isReservedHost(h)), 'every provider host is reserved for bw.mjs');
  assertEq('cloudflare-not-reserved', isReservedHost('challenges.cloudflare.com'), false);
  assertEq('reserved-count', RESERVED_HOSTS.size, 3);
}
