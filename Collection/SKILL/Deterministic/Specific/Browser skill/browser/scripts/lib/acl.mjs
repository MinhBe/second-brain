// Windows ACL helpers via icacls (no native deps).
import { spawnSync } from 'node:child_process';
import { userInfo } from 'node:os';
import { statSync } from 'node:fs';

const ALWAYS_OK = ['nt authority\\system', 'builtin\\administrators'];

function currentUser() {
  const u = userInfo().username.toLowerCase();
  const d = (process.env.USERDOMAIN ?? '').toLowerCase();
  return { user: u, domain: d };
}

/** Parses `icacls <path>` output into [{principal, perms}]. */
export function aclInfo(path) {
  const r = spawnSync('icacls', [path], { encoding: 'utf8', windowsHide: true });
  if (r.status !== 0) return { ok: false, error: (r.stderr || r.stdout || '').trim(), entries: [] };
  const entries = [];
  // The first line is "<path> <principal>:(perms)"; the path may contain spaces and
  // non-ASCII characters that the console code page mangles, so match the principal
  // from the right: DOMAIN\name (domain has no spaces, except the well-known NT AUTHORITY
  // / BUILTIN / NT SERVICE ones) or a raw SID.
  const PRINCIPAL = /(?:^|\s)((?:NT AUTHORITY|BUILTIN|NT SERVICE|APPLICATION PACKAGE AUTHORITY|[^\s\\]+)\\[^:\\]+|S-1-[0-9-]+):(\(.*\))\s*$/;
  for (const raw of r.stdout.split(/\r?\n/)) {
    const m = raw.match(PRINCIPAL);
    if (m) entries.push({ principal: m[1].trim(), perms: m[2] });
  }
  return { ok: true, entries };
}

/** True when only SYSTEM, Administrators and the current user have any access. */
export function isOwnerOnly(path) {
  const info = aclInfo(path);
  if (!info.ok) return { ok: false, reason: info.error, extra: [] };
  const { user } = currentUser();
  const extra = info.entries
    .map((e) => e.principal.toLowerCase())
    .filter((p) => !ALWAYS_OK.includes(p) && !p.endsWith('\\' + user) && p !== user);
  return { ok: extra.length === 0, extra, entries: info.entries };
}

/** Restricts a file or directory to SYSTEM + Administrators + current user. Returns {ok, output}. */
export function restrict(path) {
  const { user, domain } = currentUser();
  const isDir = statSync(path).isDirectory();
  const inh = isDir ? '(OI)(CI)F' : 'F';
  const principal = domain ? `${domain}\\${user}` : user;
  const args = [path, '/inheritance:r', '/grant:r', `${principal}:${inh}`, `*S-1-5-18:${inh}`, `*S-1-5-32-544:${inh}`];
  const r = spawnSync('icacls', args, { encoding: 'utf8', windowsHide: true });
  return { ok: r.status === 0, output: (r.stdout || '') + (r.stderr || '') };
}
