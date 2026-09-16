// Profile-aware attach to the user's RUNNING Chrome (Playwright connectOverCDP, no playwright-cli).
// Chrome hosts every open profile in one process; each profile is a CDP browser context.
// Playwright cannot see those contexts (it folds every foreign page into its "default"
// context), so profile selection is done with browser-level CDP: Target.getTargets gives
// each page's browserContextId, Target.createTarget({browserContextId}) opens a tab in a
// chosen profile, and the resulting page is then driven through Playwright by targetId.
// Node's built-in WebSocket cannot complete Chrome's handshake reliably; Playwright's can.
import { readFileSync, existsSync } from 'node:fs';
import { join, basename } from 'node:path';
import { spawn } from 'node:child_process';
import { EXIT, SkillError } from './exit-codes.mjs';
import { findChrome, chromeUserDataRoot } from './chrome.mjs';
import { ATTACH_HOWTO } from './pwcli.mjs';

/** ws://127.0.0.1:<port>/devtools/browser/<id> from DevToolsActivePort, or null. */
export function browserWsUrl() {
  const override = process.env.BROWSER_SKILL_CDP_WS;
  if (override) return override;
  const p = join(chromeUserDataRoot(), 'DevToolsActivePort');
  if (!existsSync(p)) return null;
  const [port, path] = readFileSync(p, 'utf8').trim().split(/\r?\n/);
  if (!/^\d+$/.test(port ?? '') || !path) return null;
  return `ws://127.0.0.1:${port}${path}`;
}

/** Connects Playwright to the user's Chrome. Chrome accepts DevTools sockets on its UI thread, so allow slow handshakes. */
export async function connectBrowser() {
  const ws = browserWsUrl();
  if (!ws) throw new SkillError(EXIT.PRECONDITION, 'Chrome remote debugging is off (DevToolsActivePort not found)', ATTACH_HOWTO);
  const { chromium } = await import('playwright');
  let last;
  for (let i = 0; i < 3; i++) {
    try { return await chromium.connectOverCDP(ws, { timeout: 30000 }); } catch (e) { last = e; }
  }
  throw new SkillError(EXIT.PRECONDITION, `Chrome DevTools endpoint not reachable: ${String(last?.message ?? last).split('\n')[0]}`, ATTACH_HOWTO);
}

/** CDP targetId of a Playwright page. */
export async function targetIdOf(page) {
  const s = await page.context().newCDPSession(page);
  try { return (await s.send('Target.getTargetInfo')).targetInfo.targetId; } finally { await s.detach().catch(() => {}); }
}

/** Finds the page with this targetId across all contexts (polls briefly: a fresh target needs a moment to attach). */
export async function pageByTargetId(browser, targetId, { waitMs = 0 } = {}) {
  const deadline = Date.now() + waitMs;
  do {
    for (const ctx of browser.contexts()) {
      for (const page of ctx.pages()) {
        let tid = null;
        try { tid = await targetIdOf(page); } catch { /* skip */ }
        if (tid === targetId) return page;
      }
    }
    if (Date.now() < deadline) await new Promise((r) => setTimeout(r, 300));
  } while (Date.now() < deadline);
  return null;
}

/** Page targets from the browser session: [{ targetId, url, title, browserContextId }]. */
async function pageTargets(sess) {
  const { targetInfos } = await sess.send('Target.getTargets');
  return targetInfos.filter((t) => t.type === 'page').map((t) => ({ targetId: t.targetId, url: t.url, title: t.title, browserContextId: t.browserContextId ?? null }));
}

/**
 * Opens ONE new tab in the given Chrome profile and returns it.
 * CDP cannot create targets inside a profile's own browser context ("Failed to find browser
 * context"), so Chrome itself is asked to open the tab: `chrome.exe --profile-directory=<dir> <marker-url>`
 * hands the URL to the running process, which opens it in that profile (creating the
 * profile's window if needed). The new tab is recognised by a one-time nonce in its URL,
 * then navigated to `url`. Returns { browser, page, targetId, browserContextId, opened_window }.
 */
export async function openTabInProfile(browser, profileDir, url, { waitMs = 40000, reconnect = null } = {}) {
  const chrome = findChrome();
  if (!chrome) throw new SkillError(EXIT.PRECONDITION, 'Google Chrome not found', 'Run doctor.mjs');
  const nonce = `bwp-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
  const marker = `data:text/html,${nonce}`;
  let sess = await browser.newBrowserCDPSession();
  const before = await pageTargets(sess);
  const knownIds = new Set(before.map((t) => t.targetId));
  spawn(chrome.path, [`--profile-directory=${profileDir}`, marker], { detached: true, stdio: 'ignore', windowsHide: true }).unref();
  const deadline = Date.now() + waitMs;
  let hit = null; let b = browser;
  while (Date.now() < deadline && !hit) {
    await new Promise((r) => setTimeout(r, 700));
    hit = (await pageTargets(sess)).find((t) => !knownIds.has(t.targetId) && t.url.includes(nonce)) ?? null;
  }
  await sess.detach().catch(() => {});
  if (!hit) throw new SkillError(EXIT.TIMEOUT, `Chrome did not open a tab for profile "${profileDir}" within ${waitMs} ms`, 'Ask the user to open that Chrome profile by hand, then run the command once more');
  const opened_window = !before.some((t) => t.browserContextId === hit.browserContextId);
  let page = await pageByTargetId(b, hit.targetId, { waitMs: 8000 });
  if (!page) {
    // A tab in a window opened after connecting is not always surfaced on the old connection.
    b = reconnect ? await reconnect() : (await b.close().catch(() => {}), await connectBrowser());
    page = await pageByTargetId(b, hit.targetId, { waitMs: 8000 });
  }
  if (!page) throw new SkillError(EXIT.TOOL, 'Chrome opened the tab but Playwright could not attach to it', 'Run the command once more');
  return { browser: b, page, targetId: hit.targetId, browserContextId: hit.browserContextId, opened_window };
}

/** [{ browserContextId, pages }] — running contexts (profiles cannot be named from CDP alone). */
export async function contextsSummary(browser) {
  const sess = await browser.newBrowserCDPSession();
  try {
    const targets = await pageTargets(sess);
    return [...new Set(targets.map((t) => t.browserContextId))].map((id) => ({ browserContextId: id, pages: targets.filter((t) => t.browserContextId === id).length }));
  } finally { await sess.detach().catch(() => {}); }
}

/** Number of pages in the browser that are not `page`. */
export function otherPageCount(browser, page) {
  return browser.contexts().reduce((n, c) => n + c.pages().filter((p) => p !== page).length, 0);
}
