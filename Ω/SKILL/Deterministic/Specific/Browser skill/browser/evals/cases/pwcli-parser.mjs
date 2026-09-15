// The playwright-cli text parser and error mapping hold against captured real outputs.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { parseText, mapError } from '../../scripts/lib/pwcli.mjs';
import { EXIT } from '../../scripts/lib/exit-codes.mjs';
import { assertEq, assertTrue, assertMatch } from '../lib/assert.mjs';

export const name = 'pwcli-parser';

export async function run(ctx) {
  const fx = (n) => readFileSync(join(ctx.fixtures, 'pwcli', `${n}.txt`), 'utf8');
  let p = parseText(fx('open'));
  assertEq('open.session', p.opened?.session, 'cap');
  assertEq('open.url', p.url, 'http://127.0.0.1:47831/');
  assertEq('open.title', p.title, 'bw smoke fixture');
  assertMatch('open.snapshot', p.snapshotFile, /page-.*\.yml$/);
  assertEq('open.console', p.console?.errors, 1);

  p = parseText(fx('snapshot'));
  assertTrue('snapshot.inline', p.snapshotInline && p.snapshotInline.includes('[ref=e6]'), 'inline yaml with refs');
  p = parseText(fx('snapshot-file'));
  assertEq('snapshot-file.path', p.snapshotFile, './snap1.yml');

  p = parseText(fx('click-role'));
  assertMatch('click-role.modal', p.modal, /confirm.*dialog/);
  assertEq('click-role.url', p.url, 'http://127.0.0.1:47831/index.html#top');

  p = parseText(fx('click-bad'));
  assertMatch('click-bad.error', p.error, /Ref e999 not found/);
  assertEq('click-bad.map', mapError(p.error, 'click', 'x').exit, EXIT.TARGET);

  p = parseText(fx('goto-badhost'));
  assertMatch('goto-badhost.error', p.error, /ERR_NAME_NOT_RESOLVED/);
  assertEq('goto-badhost.map', mapError(p.error, 'goto', 'x').exit, EXIT.TIMEOUT);
  assertTrue('goto-badhost.no-ansi', !p.error.includes('[2m'), 'ansi stripped');

  p = parseText(fx('nosession-click'));
  assertMatch('nosession.result', p.result, /is not open/);
  assertEq('nosession.map', mapError(p.result, 'click', 'nosuch').exit, EXIT.NOT_FOUND);

  p = parseText(fx('runcode-wait-fail'));
  assertMatch('wait.error', p.error, /Timeout 1500ms exceeded/);

  p = parseText(fx('find-regex'));
  assertMatch('find.result', p.result, /Found 2 matches/);
  assertTrue('find.refs', /\[ref=e6\]/.test(p.result) && /\[ref=e17\]/.test(p.result), 'both refs present');

  p = parseText(fx('tab-list'));
  assertMatch('tabs.result', p.result, /^- 0: \(current\) \[bw smoke fixture\]\(http/);

  p = parseText(fx('close'));
  assertMatch('close.result', p.result, /closed/);

  // attach / detach (user's running Chrome)
  p = parseText(fx('attach'));
  assertEq('attach.session', p.attached?.session, 'live');
  assertEq('attach.endpoint', p.attached?.endpoint, 'chrome');
  assertEq('attach.not-opened', p.opened, null);
  assertEq('attach.url', p.url, 'data:text/html,<title>user tab B</title>B');
  assertMatch('attach.snapshot', p.snapshotFile, /page-.*\.yml$/);
  p = parseText(fx('detach'));
  assertMatch('detach.result', p.result, /detached/);
  p = parseText(fx('detach-notattached'));
  assertEq('detach-notattached.map', mapError(p.result, 'close', 'fmt').exit, EXIT.NOT_FOUND);
  p = parseText(fx('tab-new'));
  assertMatch('tab-new.result', p.result, /^- 0: \[user tab B\]/);
  assertMatch('tab-new.current', p.result, /- 2: \(current\) \[Example Domain\]\(https:\/\/example\.com\/\)/);
  p = parseText(fx('runcode-owned-list'));
  assertEq('runcode.result', JSON.stringify(JSON.parse(p.result.trim())), '[false,false,true]');
  const noport = readFileSync(join(ctx.fixtures, 'pwcli', 'attach-noport.stderr.txt'), 'utf8').match(/PlaywrightError: ([^\r\n]+)/)?.[1];
  assertMatch('attach-noport.msg', noport, /DevToolsActivePort/);
  assertEq('attach-noport.map', mapError(noport, 'attach', 'x').exit, EXIT.PRECONDITION);
  assertMatch('attach-noport.next', mapError(noport, 'attach', 'x').next, /chrome:\/\/inspect/);

  const j = JSON.parse(fx('json-list'));
  assertEq('json-list.name', j.browsers?.[0]?.name, 'cap');
  const je = JSON.parse(fx('json-click-bad'));
  assertEq('json-error.flag', je.isError, true);
}
