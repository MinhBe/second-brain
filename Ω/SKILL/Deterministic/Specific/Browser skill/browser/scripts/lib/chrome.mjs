// Locates the installed Google Chrome (channel "chrome") and its version.
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { connect } from 'node:net';

/** The user's real Chrome profile root. Read-only for this skill; never launched on. */
export function chromeUserDataRoot() {
  return join(process.env.LOCALAPPDATA ?? '', 'Google', 'Chrome', 'User Data');
}

/**
 * Reads DevToolsActivePort from the real Chrome User Data dir and probes the port.
 * Chrome writes that file only after the human ticks "Allow remote debugging for this
 * browser instance" at chrome://inspect/#remote-debugging. Mirrors playwright-cli's
 * channel discovery (channelSessions.js readEndpoint). Returns { path, port, open }.
 */
export async function chromeDevToolsPort() {
  // Evals only: BROWSER_SKILL_CDP_ENDPOINT=http://127.0.0.1:<port> points at a test Chrome
  // started with --remote-debugging-port on a throwaway user-data-dir.
  const override = process.env.BROWSER_SKILL_CDP_ENDPOINT;
  let path = join(chromeUserDataRoot(), 'DevToolsActivePort');
  let port = null;
  if (override) {
    try { port = Number(new URL(override).port) || null; path = override; } catch { port = null; }
  } else {
    try {
      const n = parseInt(readFileSync(path, 'utf8').trim().split(/\r?\n/)[0], 10);
      if (Number.isFinite(n) && n > 0) port = n;
    } catch { /* file missing: remote debugging off */ }
  }
  if (!port) return { path, port: null, open: false, endpoint: override ?? 'chrome' };
  const open = await new Promise((res) => {
    const sock = connect({ host: '127.0.0.1', port, timeout: 400 });
    sock.once('connect', () => { sock.destroy(); res(true); });
    sock.once('error', () => res(false));
    sock.once('timeout', () => { sock.destroy(); res(false); });
  });
  return { path, port, open, endpoint: override ?? 'chrome' };
}

export function findChrome() {
  const candidates = [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    join(process.env.LOCALAPPDATA ?? '', 'Google', 'Chrome', 'Application', 'chrome.exe'),
  ];
  for (const p of candidates) {
    if (existsSync(p)) {
      let version = null;
      try { version = readdirSync(join(p, '..')).find((d) => /^\d+\.\d+\.\d+\.\d+$/.test(d)) ?? null; } catch { /* ignore */ }
      return { path: p, version };
    }
  }
  return null;
}
