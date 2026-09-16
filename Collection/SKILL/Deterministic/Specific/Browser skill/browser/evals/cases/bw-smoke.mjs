// End-to-end smoke of bw.mjs against the static fixture (needs --browser).
import { readFileSync } from 'node:fs';
import { assertEq, assertTrue, assertMatch } from '../lib/assert.mjs';

export const name = 'bw-smoke';
export const needsBrowser = true;

export async function run(ctx) {
  const srv = await ctx.server();
  const S = 'bwsmoke';
  const step = (id, args, input) => {
    const r = ctx.runScript('bw', args, { input });
    ctx.checkLine(id, r);
    return r;
  };
  try {
    // cleanup any stale session first
    ctx.runScript('bw', ['close', '-s', S]);

    let r = step('open', ['open', srv.url, '-s', S, '--headless']);
    assertEq('open.exit', r.status, 0);
    assertEq('open.title', r.json.title, 'bw smoke fixture');
    assertTrue('open.snapshot', typeof r.json.snapshot_path === 'string' && r.json.refs > 10, `refs=${r.json.refs}`);

    r = step('open-again', ['open', srv.url, '-s', S, '--headless']);
    assertEq('open-again.exit', r.status, 12);

    r = step('snapshot', ['snapshot', '-s', S]);
    assertEq('snapshot.exit', r.status, 0);
    assertTrue('snapshot.file', readFileSync(r.json.snapshot_path, 'utf8').includes('[ref=e'), 'refs in file');

    r = step('find', ['find', '-s', S, '--pattern', 'set state']);
    assertEq('find.exit', r.status, 0);
    assertTrue('find.match', r.json.matches.length >= 1 && /^e\d+$/.test(r.json.matches[0].ref), JSON.stringify(r.json.matches[0]));
    const setRef = r.json.matches[0].ref;

    r = step('click', ['click', setRef, '-s', S]);
    assertEq('click.exit', r.status, 0);

    r = step('extract-status', ['extract', '-s', S, '--mode', 'text', '--css', '#status']);
    assertEq('extract-status.exit', r.status, 0);
    assertEq('extract-status.text', r.json.text, 'clicked');

    r = step('find-name', ['find', '-s', S, '--pattern', 'textbox "Name"']);
    const nameRef = r.json.matches[0]?.ref;
    assertTrue('find-name.ref', /^e\d+$/.test(nameRef ?? ''), String(nameRef));

    r = step('fill', ['fill', nameRef, 'hello', '-s', S, '--submit']);
    assertEq('fill.exit', r.status, 0);
    assertEq('fill.chars', r.json.filled_chars, 5);
    assertTrue('fill.no-echo', !r.stdout.includes('hello'), 'value not echoed');

    r = step('wait-text', ['wait', '-s', S, '--text', 'submitted: hello']);
    assertEq('wait-text.exit', r.status, 0);
    assertEq('wait-text.matched', r.json.matched, true);

    r = step('wait-timeout', ['wait', '-s', S, '--text', 'NOPE-NOT-THERE', '--timeout', '1200']);
    assertEq('wait-timeout.exit', r.status, 6);

    r = step('select', ['select', '#color', 'green', '-s', S]);
    assertEq('select.exit', r.status, 0);
    r = step('check', ['check', '#agree', '-s', S]);
    assertEq('check.exit', r.status, 0);

    r = step('click-role', ['click', '--role', 'button', '--name', 'Ask confirm', '-s', S]);
    assertEq('click-role.exit', r.status, 0);
    assertMatch('click-role.modal', r.json.modal, /confirm/);
    r = step('dialog', ['dialog', '-s', S, '--accept']);
    assertEq('dialog.exit', r.status, 0);
    r = step('extract-dialog', ['extract', '-s', S, '--mode', 'text', '--css', '#dialog-result']);
    assertEq('extract-dialog.text', r.json.text, 'confirmed');

    r = step('extract-table', ['extract', '-s', S, '--mode', 'table']);
    assertEq('extract-table.exit', r.status, 0);
    assertEq('extract-table.rows', r.json.items[0].rows.length, 2);
    r = step('extract-links', ['extract', '-s', S, '--mode', 'links']);
    assertEq('extract-links.count', r.json.count, 3);
    r = step('extract-md', ['extract', '-s', S, '--mode', 'md']);
    assertEq('extract-md.exit', r.status, 0);
    assertTrue('extract-md.heading', (r.json.text ?? readFileSync(r.json.extract_path, 'utf8')).includes('# bw smoke fixture'), 'markdown heading');

    r = step('click-bad', ['click', 'e9999', '-s', S]);
    assertEq('click-bad.exit', r.status, 5);

    r = step('screenshot', ['screenshot', '-s', S]);
    assertEq('screenshot.exit', r.status, 0);
    assertTrue('screenshot.file', readFileSync(r.json.screenshot_path).length > 1000, 'png bytes');

    r = step('tabs', ['tabs', '-s', S]);
    assertEq('tabs.count', r.json.tabs.length, 1);

    r = step('state-save', ['state-save', 'smoke', '-s', S]);
    assertEq('state-save.exit', r.status, 0);
    assertTrue('state-save.cookies', r.json.cookies >= 1, `cookies=${r.json.cookies}`);
    assertTrue('state-save.no-cookie-values', !r.stdout.includes('smoke=1'), 'no cookie value in output');

    r = step('close', ['close', '-s', S]);
    assertEq('close.exit', r.status, 0);

    r = step('open-state', ['open', srv.url, '-s', S, '--headless', '--state', 'smoke']);
    assertEq('open-state.exit', r.status, 0);
    assertEq('open-state.loaded', r.json.state_loaded, true);
    r = step('extract-restored', ['extract', '-s', S, '--mode', 'text', '--css', '#status']);
    assertEq('extract-restored.text', r.json.text, 'restored');

    r = step('list', ['list']);
    assertTrue('list.has', r.json.sessions.some((s) => s.name === S), 'session listed');
  } finally {
    ctx.runScript('bw', ['close', '-s', S]);
  }
}
