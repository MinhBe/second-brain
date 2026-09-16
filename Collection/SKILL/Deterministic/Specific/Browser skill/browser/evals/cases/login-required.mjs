// LOGIN_REQUIRED and CAPTCHA are recognized with evidence and never lead to typing.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { classify } from '../../scripts/lib/classify.mjs';
import { fromFixture } from '../../scripts/lib/observe.mjs';
import { assertEq, assertTrue } from '../lib/assert.mjs';

export const name = 'login-required';

export async function run(ctx) {
  const fx = (n) => fromFixture(JSON.parse(readFileSync(join(ctx.fixtures, 'observations', `${n}.json`), 'utf8')));
  let r = classify(fx('claude-login-required'), 'claude');
  assertEq('login.state', r.state, 'LOGIN_REQUIRED');
  assertEq('login.blocking', r.blocking, true);
  assertTrue('login.evidence', ['url', 'visible_text'].includes(r.evidence.type) && r.evidence.text.length > 0, `${r.evidence.type}: ${r.evidence.text}`);
  r = classify(fx('claude-captcha'), 'claude');
  assertEq('captcha.state', r.state, 'CAPTCHA');
  assertEq('captcha.evidence', r.evidence.type, 'iframe');
  // real Cloudflare interstitial captured live on 2026-09-11
  r = classify(fx('claude-cf-interstitial'), 'claude');
  assertEq('cf-interstitial.state', r.state, 'CAPTCHA');
  assertEq('cf-interstitial.rule', r.evidence.rule, 'cf-interstitial');
  r = classify(fx('claude-ready'), 'claude');
  assertEq('ready.state', r.state, 'READY');
  assertEq('ready.blocking', r.blocking, false);
}
