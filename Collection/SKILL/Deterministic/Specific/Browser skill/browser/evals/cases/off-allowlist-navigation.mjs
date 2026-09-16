// With a real Chrome and the real allowlist: navigating to an off-allowlist host is failed at the
// Fetch layer, the URL stays about:blank, and the target server records zero hits.
// Also runs the OOPIF spike (S4): a cross-origin iframe inside a data: page.
import { join } from 'node:path';
import { mkdirSync, writeFileSync } from 'node:fs';
import { launchObserverBrowser } from '../../scripts/lib/browser.mjs';
import { assertEq, assertTrue, stepPass } from '../lib/assert.mjs';

export const name = 'off-allowlist-navigation';
export const needsBrowser = true;

async function spikeOopif(ctx, srv, routeLayer) {
  const audit = [];
  const dir = join(ctx.evalsDir, `oopif-${routeLayer ? 'route' : 'page'}-${Date.now()}`, 'user-data');
  mkdirSync(dir, { recursive: true });
  const before = srv.hits().length;
  const b = await launchObserverBrowser({ userDataDir: dir, headless: true, audit: (e) => audit.push(e), routeLayer });
  try {
    const html = `<h1>parent</h1><iframe src="${srv.url}iframe-offhost.html" width="300" height="100"></iframe>`;
    await b.page.goto(`data:text/html,${encodeURIComponent(html)}`, { waitUntil: 'domcontentloaded', timeout: 20000 }).catch(() => {});
    await b.page.waitForTimeout(2500);
  } finally { await b.close(); }
  const hits = srv.hits().length - before;
  const seen = audit.filter((e) => e.url && e.url.startsWith(srv.url));
  return { routeLayer, server_hits: hits, blocked_seen: seen.filter((e) => e.verdict === 'blocked').length, layers: [...new Set(seen.map((e) => e.layer ?? 'page-fetch'))] };
}

export async function run(ctx) {
  const srv = await ctx.server();
  const audit = [];
  const dir = join(ctx.evalsDir, `throwaway-${Date.now()}`, 'user-data');
  mkdirSync(dir, { recursive: true });
  const before = srv.hits().length;
  const b = await launchObserverBrowser({ userDataDir: dir, headless: true, audit: (e) => audit.push(e) });
  try {
    assertEq('start-blank', b.page.url(), 'about:blank');
    // raw CDP navigation, exactly what an attacker-controlled instruction would try
    await b.firewall.cdp.send('Page.navigate', { url: srv.url }).catch(() => {});
    await b.page.waitForTimeout(3000);
    const entry = audit.find((e) => e.url === srv.url);
    assertTrue('paused', !!entry, 'Fetch.requestPaused fired for the URL');
    assertEq('blocked', entry.verdict, 'blocked');
    assertEq('decision', entry.cdpDecision, 'Fetch.failRequest');
    // Chrome paints chrome-error:// for a failed document request; browser.mjs restores the last allowed URL.
    assertTrue('url-not-target', !b.page.url().startsWith(srv.url), b.page.url());
    assertEq('url-restored', b.page.url(), 'about:blank');
    assertEq('server-zero-hits', srv.hits().length - before, 0);
    // positive control: internal data: URL loads
    await b.page.goto('data:text/html,<title>ok</title><h1>ok</h1>', { waitUntil: 'domcontentloaded', timeout: 10000 });
    assertEq('data-loads', await b.page.title(), 'ok');
    // page.goto to the off-allowlist server is also blocked (Playwright path)
    let err = null;
    await b.page.goto(srv.url, { waitUntil: 'domcontentloaded', timeout: 10000 }).catch((e) => { err = e; });
    assertTrue('goto-blocked', err !== null || audit.filter((e) => e.url === srv.url && e.verdict === 'blocked').length >= 2, String(err?.message ?? '').slice(0, 80));
    assertEq('server-still-zero', srv.hits().length - before, 0);
    if (ctx.online) {
      await b.page.goto('https://claude.ai/robots.txt', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
      const ok = audit.find((e) => e.host === 'claude.ai' && e.verdict === 'allowed');
      assertTrue('online-allowlisted', !!ok, 'claude.ai allowed');
    }
  } finally {
    await b.close();
  }
  // S4 spike: record, do not fail the build on it
  const pageOnly = await spikeOopif(ctx, srv, false);
  const withRoute = await spikeOopif(ctx, srv, true);
  const result = { page_level: pageOnly, with_context_route: withRoute, recorded_at: new Date().toISOString() };
  writeFileSync(join(ctx.evalsDir, 'oopif-result.json'), JSON.stringify(result, null, 2));
  stepPass('oopif.page-level', `server_hits=${pageOnly.server_hits} blocked_seen=${pageOnly.blocked_seen}`);
  stepPass('oopif.with-route', `server_hits=${withRoute.server_hits} blocked_seen=${withRoute.blocked_seen}`);
  assertTrue('oopif.some-layer-blocks', pageOnly.server_hits === 0 || withRoute.server_hits === 0, JSON.stringify(result));
}
