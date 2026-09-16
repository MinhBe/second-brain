// Reads Chrome/Edge "Local State" to list profiles. Read-only. Emails are masked unless asked for.
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

export function userDataDir(browser = 'chrome') {
  const local = process.env.LOCALAPPDATA ?? join(process.env.USERPROFILE ?? '', 'AppData', 'Local');
  return browser === 'edge'
    ? join(local, 'Microsoft', 'Edge', 'User Data')
    : join(local, 'Google', 'Chrome', 'User Data');
}

export function localStatePath(browser = 'chrome') {
  return join(userDataDir(browser), 'Local State');
}

export function maskEmail(e) {
  if (!e || typeof e !== 'string') return null;
  const [user, domain] = e.split('@');
  if (!domain) return e[0] + '***';
  return `${user[0] ?? ''}***@${domain}`;
}

function naturalKey(dir) {
  if (dir === 'Default') return [0, 0];
  const m = dir.match(/^Profile (\d+)$/);
  return m ? [1, Number(m[1])] : [2, 0];
}

/** Returns [{ directory, name, account? }]. Throws if Local State is missing. */
export function listProfiles(browser = 'chrome', { withAccount = false } = {}) {
  const p = localStatePath(browser);
  if (!existsSync(p)) { const e = new Error(`Local State not found: ${p}`); e.code = 'ENOENT'; throw e; }
  const json = JSON.parse(readFileSync(p, 'utf8'));
  const cache = json?.profile?.info_cache ?? {};
  const out = Object.entries(cache).map(([directory, info]) => {
    const row = { directory, name: String(info?.name ?? info?.shortcut_name ?? directory) };
    if (withAccount) row.account = maskEmail(info?.user_name) ?? null;
    return row;
  });
  out.sort((a, b) => { const ka = naturalKey(a.directory), kb = naturalKey(b.directory); return ka[0] - kb[0] || ka[1] - kb[1] || a.directory.localeCompare(b.directory); });
  return out;
}
