// Layer 0 — domain allowlist enforced at the CDP Fetch layer.
// Adapted from skills-main/skills/safe-browser/templates/claude-agent-sdk/hn-scraper-demo.mjs
// (lines 94-178) with three changes required by SECURITY.md §3:
//   1. internal browser URLs (about:, chrome:, devtools:, data:, blob:) pass without a host check
//   2. any exception inside the handler FAILS CLOSED (Fetch.failRequest), never falls through
//   3. hosts are matched exactly and case-insensitively; no "www." stripping
// This module is pure: it only needs an object with `on(event, fn)` and `send(method, params)`,
// so evals drive it with a fake CDP session and no browser.
import { INTERNAL_URL_RE, OBSERVER_ALLOWLIST } from './policy.mjs';

export function createFirewall(cdp, audit, opts = {}) {
  const allowlist = opts.allowlist ?? OBSERVER_ALLOWLIST;
  const hostOf = opts.hostOf ?? ((url) => new URL(url).hostname.toLowerCase());
  const stats = { allowed: 0, blocked: 0, internal: 0, handler_errors: 0 };
  const write = (entry) => { try { audit(entry); } catch { /* audit sink must never break enforcement */ } };

  async function decide(params) {
    const url = String(params?.request?.url ?? '');
    const requestId = params?.requestId;
    const base = { ts: new Date().toISOString(), requestId, url, resourceType: params?.resourceType ?? null };
    try {
      if (INTERNAL_URL_RE.test(url)) {
        await cdp.send('Fetch.continueRequest', { requestId });
        stats.internal++;
        write({ ...base, host: null, verdict: 'allowed', reason: 'internal browser URL', cdpDecision: 'Fetch.continueRequest' });
        return 'allowed';
      }
      const host = hostOf(url);
      if (allowlist.has(host)) {
        await cdp.send('Fetch.continueRequest', { requestId });
        stats.allowed++;
        write({ ...base, host, verdict: 'allowed', reason: 'host in allowlist', cdpDecision: 'Fetch.continueRequest' });
        return 'allowed';
      }
      await cdp.send('Fetch.failRequest', { requestId, errorReason: 'BlockedByClient' });
      stats.blocked++;
      write({ ...base, host, verdict: 'blocked', reason: 'host not in allowlist', cdpDecision: 'Fetch.failRequest' });
      return 'blocked';
    } catch (err) {
      stats.handler_errors++;
      write({ ...base, host: null, verdict: 'blocked', reason: `handler error: ${String(err?.message ?? err)}`, cdpDecision: 'Fetch.failRequest', event: 'HANDLER_ERROR_BLOCKED' });
      try { await cdp.send('Fetch.failRequest', { requestId, errorReason: 'BlockedByClient' }); } catch { /* request may already be gone */ }
      return 'blocked';
    }
  }

  cdp.on('Fetch.requestPaused', decide);

  return {
    stats,
    allowlist,
    decide,
    async enable() {
      await cdp.send('Fetch.enable', { patterns: [{ urlPattern: '*' }] });
      return true;
    },
  };
}

/** Attaches a firewall to a Playwright page. Awaits Fetch.enable BEFORE returning. */
export async function attachFirewall(page, audit, opts = {}) {
  const cdp = await page.context().newCDPSession(page);
  const fw = createFirewall(cdp, audit, opts);
  await fw.enable();
  return { ...fw, cdp };
}

/**
 * Second layer for frames/workers/popups the page-level CDP session cannot see (OOPIF).
 * Uses Playwright routing on the whole context. Same allowlist, same audit sink.
 */
export async function attachContextRoute(context, audit, opts = {}) {
  const allowlist = opts.allowlist ?? OBSERVER_ALLOWLIST;
  const stats = { allowed: 0, blocked: 0 };
  await context.route('**/*', async (route) => {
    const url = route.request().url();
    const base = { ts: new Date().toISOString(), requestId: null, url, resourceType: route.request().resourceType(), layer: 'context-route' };
    try {
      if (INTERNAL_URL_RE.test(url)) { await route.continue(); return; }
      const host = new URL(url).hostname.toLowerCase();
      if (allowlist.has(host)) { stats.allowed++; await route.continue(); return; }
      stats.blocked++;
      audit({ ...base, host, verdict: 'blocked', reason: 'host not in allowlist', cdpDecision: 'route.abort' });
      await route.abort('blockedbyclient');
    } catch (err) {
      audit({ ...base, host: null, verdict: 'blocked', reason: `route handler error: ${err?.message}`, cdpDecision: 'route.abort', event: 'HANDLER_ERROR_BLOCKED' });
      try { await route.abort('blockedbyclient'); } catch { /* ignore */ }
    }
  });
  return { stats };
}
