// Every script prints exactly one JSON line with the envelope, for --help and for errors.
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { assertEq, assertTrue } from '../lib/assert.mjs';

export const name = 'output-contract';

export async function run(ctx) {
  const scripts = ['doctor', 'discover-profiles', 'profile', 'bw', 'aiweb'].filter((s) => existsSync(join(ctx.skillRoot, 'scripts', `${s}.mjs`)));
  assertTrue('scripts-present', scripts.includes('bw') && scripts.includes('doctor'), scripts.join(','));
  for (const s of scripts) {
    const r = ctx.runScript(s, ['--help']);
    assertEq(`${s}.help.lines`, r.lines.length, 1);
    assertTrue(`${s}.help.json`, r.json && r.json.ok === true && typeof r.json.verb === 'string' && typeof r.json.next === 'string', JSON.stringify(r.json)?.slice(0, 100));
    assertTrue(`${s}.help.bytes`, r.bytes <= ctx.maxBytes, `${r.bytes}`);
  }
  // errors are also one JSON line with the right exit code
  let r = ctx.runScript('bw', ['bogus-verb']);
  assertEq('bw.unknown-verb.exit', r.status, 2);
  assertEq('bw.unknown-verb.code', r.json?.code, 'USAGE');
  r = ctx.runScript('bw', ['open', 'https://example.com']);
  assertEq('bw.missing-session.exit', r.status, 2);
  r = ctx.runScript('bw', ['open', 'notaurl', '-s', 'x']);
  assertEq('bw.bad-url.exit', r.status, 2);
  r = ctx.runScript('bw', ['open', 'https://claude.ai/new', '-s', 'x']);
  assertEq('bw.reserved-host.exit', r.status, 7);
  assertEq('bw.reserved-host.code', r.json?.code, 'POLICY');
  r = ctx.runScript('bw', ['open', 'https://chat.chatgpt.com/', '-s', 'x']);
  assertEq('bw.reserved-subdomain.exit', r.status, 7);
  // attach: URL validation runs before the DevTools probe, so these never touch Chrome.
  // R4 relaxed (temporary): provider hosts are allowed in attached sessions, so this reaches the probe (3), not 7.
  r = ctx.runScript('bw', ['attach', 'https://claude.ai/', '-s', 'x'], { env: { BROWSER_SKILL_CDP_ENDPOINT: 'http://127.0.0.1:1' } });
  assertEq('bw.attach-provider-host-allowed.exit', r.status, 3);
  r = ctx.runScript('bw', ['attach', 'notaurl', '-s', 'x']);
  assertEq('bw.attach-bad-url.exit', r.status, 2);
  r = ctx.runScript('bw', ['attach', 'https://example.com/']);
  assertEq('bw.attach-missing-session.exit', r.status, 2);
  r = ctx.runScript('bw', ['attach', 'https://example.com/', '-s', 'x'], { env: { BROWSER_SKILL_CDP_ENDPOINT: 'http://127.0.0.1:1' } });
  assertEq('bw.attach-no-devtools.exit', r.status, 3);
  assertTrue('bw.attach-no-devtools.next', /chrome:\/\/inspect/.test(r.json?.next ?? ''), r.json?.next);
  r = ctx.runScript('bw', ['find', '-s', 'x']);
  assertEq('bw.find-missing-pattern.exit', r.status, 2);
  r = ctx.runScript('bw', ['click', 'e1', '-s', 'BAD NAME']);
  assertEq('bw.bad-session-name.exit', r.status, 2);
  r = ctx.runScript('bw', ['extract', '-s', 'x', '--mode', 'html']);
  assertEq('bw.bad-mode.exit', r.status, 2);
  r = ctx.runScript('bw', ['press', 'Control+Alt+Delete+X', '-s', 'x']);
  assertEq('bw.bad-key.exit', r.status, 2);
  // secrets never echo: redaction in the envelope
  r = ctx.runScript('bw', ['fill', 'e1', '--secret', 'C:/definitely/missing.env:KEY', '-s', 'x']);
  assertEq('bw.secret-missing.exit', r.status, 4);
  assertTrue('bw.secret-missing.no-leak', !r.stdout.includes('KEY='), 'no key material');
}
