// Observer browser: launches a persistent Chrome context on an AUTOMATION user-data-dir, with
// Layer 0 (CDP Fetch allowlist) attached to every page BEFORE any navigation, popups closed,
// downloads cancelled, dialogs dismissed and logged. Never touches the real Chrome User Data dir.
import { join } from 'node:path';
import { existsSync } from 'node:fs';
import { EXIT, SkillError } from './exit-codes.mjs';
import { attachFirewall, attachContextRoute } from './firewall.mjs';
import { OBSERVER_ALLOWLIST } from './policy.mjs';
import { findChrome } from './chrome.mjs';

function realUserData() {
  return join(process.env.LOCALAPPDATA ?? '', 'Google', 'Chrome', 'User Data').toLowerCase();
}

/**
 * launchObserverBrowser({ userDataDir, headless, allowlist, audit, onEvent, profileDirectory, routeLayer })
 * audit(entry)          -> firewall.jsonl sink
 * onEvent(name, data)   -> timeline sink (POPUP_BLOCKED, DOWNLOAD_STARTED/BLOCKED, NOTIFICATION for dialogs)
 * Returns { context, page, firewall, chrome, close() }.
 */
export async function launchObserverBrowser(opts) {
  const { userDataDir, headless = false, allowlist = OBSERVER_ALLOWLIST, audit, onEvent = () => {}, profileDirectory = null, routeLayer = process.env.BROWSER_SKILL_ROUTE_LAYER === '1' } = opts;
  if (!userDataDir) throw new SkillError(EXIT.USAGE, 'userDataDir is required', 'Register a profile first');
  if (String(userDataDir).toLowerCase().startsWith(realUserData())) {
    throw new SkillError(EXIT.POLICY, 'Refusing to drive the real Chrome User Data directory', 'Use an automation profile (profile.mjs register)');
  }
  const { chromium } = await import('playwright');
  const channel = (process.env.BROWSER_SKILL_CHANNEL ?? 'chrome').toLowerCase();
  const chrome = channel === 'chrome' ? findChrome() : null;
  if (channel === 'chrome' && !chrome) throw new SkillError(EXIT.PRECONDITION, 'Google Chrome not found', 'Run doctor.mjs');
  const args = ['--no-first-run', '--no-default-browser-check', '--disable-background-networking'];
  if (profileDirectory) args.push(`--profile-directory=${profileDirectory}`);
  if (process.env.BROWSER_SKILL_NO_AUTOMATION_FLAG === '1') { /* spike S5 */ }
  let context;
  try {
    context = await chromium.launchPersistentContext(userDataDir, {
      ...(channel === 'chrome' ? { channel: 'chrome' } : {}),
      headless,
      viewport: { width: 1280, height: 900 },
      serviceWorkers: 'block',
      acceptDownloads: true,
      args,
      ...(process.env.BROWSER_SKILL_NO_AUTOMATION_FLAG === '1' ? { ignoreDefaultArgs: ['--enable-automation'] } : {}),
      timeout: 60000,
    });
  } catch (e) {
    throw new SkillError(EXIT.TOOL, `Chrome failed to launch: ${String(e?.message ?? e).split('\n')[0]}`, 'Close other automation on this profile dir, then run doctor.mjs', { user_data_dir: userDataDir });
  }

  // Layer 0 on every page, before navigation. Popups are Tier 2: firewall them, log, close.
  const firewalls = [];
  const arm = async (p) => { const fw = await attachFirewall(p, audit, { allowlist }); firewalls.push(fw); return fw; };
  const page = context.pages()[0] ?? (await context.newPage());
  const firewall = await arm(page);
  let routeStats = null;
  if (routeLayer) routeStats = (await attachContextRoute(context, audit, { allowlist })).stats;

  context.on('page', async (p) => {
    try { await arm(p); } catch (e) { audit({ ts: new Date().toISOString(), url: p.url(), verdict: 'blocked', reason: `popup firewall attach failed: ${e.message}`, cdpDecision: 'page.close', event: 'HANDLER_ERROR_BLOCKED' }); }
    onEvent('POPUP_BLOCKED', { url: p.url() });
    await p.close().catch(() => {});
  });
  context.on('download', async (d) => {
    onEvent('DOWNLOAD_STARTED', { url: d.url(), suggested_filename: d.suggestedFilename() });
    await d.cancel().catch(() => {});
    onEvent('DOWNLOAD_BLOCKED', { url: d.url(), reason: 'artifact reader lands in Phase 3' });
  });
  page.on('dialog', async (d) => {
    onEvent('NOTIFICATION', { type: 'dialog', dialog_type: d.type(), message: d.message().slice(0, 300), action: 'dismissed' });
    await d.dismiss().catch(() => {});
  });
  // Restore after a blocked navigation: Chrome shows chrome-error:// when the Fetch layer fails a
  // document request. Go back to the last allowed page so the URL never stays on an error page.
  let lastAllowedUrl = 'about:blank';
  let restoring = false;
  page.on('framenavigated', async (frame) => {
    if (frame !== page.mainFrame()) return;
    const u = frame.url();
    if (u.startsWith('chrome-error://')) {
      if (restoring) return;
      restoring = true;
      onEvent('NAVIGATION', { restored_to: lastAllowedUrl, reason: 'blocked navigation left an error page' });
      await page.goto(lastAllowedUrl, { waitUntil: 'commit', timeout: 10000 }).catch(() => {});
      restoring = false;
      return;
    }
    if (!u.startsWith('chrome://') && !u.startsWith('devtools://')) lastAllowedUrl = u;
  });

  return {
    context,
    page,
    firewall,
    routeStats,
    chrome: { channel, path: chrome?.path ?? null, version: chrome?.version ?? null },
    stats: () => ({ page: firewall.stats, route: routeStats, pages_armed: firewalls.length }),
    async close() { try { await context.close(); } catch { /* ignore */ } },
  };
}

export function automationDirExists(dir) { return existsSync(dir); }
