// Profile registry (profiles/profiles.json), per-profile locks, cooldown and pacing.
// Phase 0-1 backend: JSON files. Phase 4 swaps this module's internals for node:sqlite.
import { existsSync, readFileSync, writeFileSync, mkdirSync, renameSync, unlinkSync } from 'node:fs';
import { join } from 'node:path';
import { EXIT, SkillError } from './exit-codes.mjs';
import { DIRS, FILES, fwd } from './paths.mjs';

export const ID_RE = /^[a-z0-9][a-z0-9-]{1,31}$/;
export const PROVIDERS = Object.freeze(['claude', 'chatgpt', 'meta']);

export function loadRegistry() {
  if (!existsSync(FILES.registry)) return { version: 1, profiles: [] };
  const reg = JSON.parse(readFileSync(FILES.registry, 'utf8'));
  if (reg.version !== 1 || !Array.isArray(reg.profiles)) throw new SkillError(EXIT.PRECONDITION, 'profiles.json has an unexpected shape', 'Inspect profiles/profiles.json or move it aside and register profiles again');
  return reg;
}

export function saveRegistry(reg) {
  mkdirSync(DIRS.profiles, { recursive: true });
  const tmp = FILES.registry + '.tmp';
  writeFileSync(tmp, JSON.stringify(reg, null, 2) + '\n');
  renameSync(tmp, FILES.registry);
}

export function getProfile(reg, id) {
  return reg.profiles.find((p) => p.id === id) ?? null;
}

export function requireProfile(reg, id) {
  const p = getProfile(reg, id);
  if (!p) throw new SkillError(EXIT.NOT_FOUND, `No profile with id ${id}`, 'Run: node <skill>/scripts/profile.mjs list');
  return p;
}

export function providerState(profile, provider) {
  return profile.providers?.[provider] ?? { state: 'UNKNOWN', evidence: null, last_checked_at: null, last_success_at: null, cooldown_until: null };
}

export function setProviderState(reg, id, provider, patch) {
  const p = requireProfile(reg, id);
  p.providers = p.providers ?? {};
  p.providers[provider] = { ...providerState(p, provider), ...patch };
  p.updated_at = new Date().toISOString();
  saveRegistry(reg);
  return p.providers[provider];
}

export function userDataDirFor(id) {
  return join(DIRS.profiles, id, 'user-data');
}

function lockPath(id) { return join(DIRS.profiles, id, '.lock'); }

function pidAlive(pid) {
  if (!pid) return false;
  try { process.kill(pid, 0); return true; } catch (e) { return e.code === 'EPERM'; }
}

export function readLock(id) {
  const p = lockPath(id);
  if (!existsSync(p)) return null;
  try { return JSON.parse(readFileSync(p, 'utf8')); } catch { return { corrupt: true }; }
}

export function isLocked(id) {
  const l = readLock(id);
  if (!l || l.corrupt) return false;
  const expired = l.expires_at && Date.parse(l.expires_at) < Date.now();
  return !expired && pidAlive(l.pid);
}

/** Acquires profiles/<id>/.lock or throws BUSY. Returns release(). Stale locks (dead pid or expired) are taken over. */
export function acquireLock(id, runId, ttlMs = 15 * 60 * 1000) {
  mkdirSync(join(DIRS.profiles, id), { recursive: true });
  const existing = readLock(id);
  if (existing && !existing.corrupt) {
    const expired = existing.expires_at && Date.parse(existing.expires_at) < Date.now();
    if (!expired && pidAlive(existing.pid) && existing.run_id !== runId) {
      throw new SkillError(EXIT.BUSY, `Profile ${id} is locked by run ${existing.run_id} (pid ${existing.pid}) until ${existing.expires_at}`,
        'Wait for that run to finish; do not start another run on this profile', { locked_by: existing.run_id, expires_at: existing.expires_at });
    }
  }
  const lock = { run_id: runId, pid: process.pid, acquired_at: new Date().toISOString(), expires_at: new Date(Date.now() + ttlMs).toISOString() };
  writeFileSync(lockPath(id), JSON.stringify(lock, null, 2));
  let released = false;
  const release = () => {
    if (released) return; released = true;
    try { const cur = readLock(id); if (cur && cur.run_id === runId) unlinkSync(lockPath(id)); } catch { /* ignore */ }
  };
  return { lock, release };
}

function lastRunPath(provider, id) { return join(DIRS.lastRun, `${provider}-${id}.json`); }

export function readLastRun(provider, id) {
  const p = lastRunPath(provider, id);
  if (!existsSync(p)) return null;
  try { return JSON.parse(readFileSync(p, 'utf8')); } catch { return null; }
}

export function recordLastRun(provider, id, info) {
  mkdirSync(DIRS.lastRun, { recursive: true });
  writeFileSync(lastRunPath(provider, id), JSON.stringify({ ...info, recorded_at: new Date().toISOString() }, null, 2));
}

/**
 * Pacing / cooldown gate. Throws BUSY when the profile must not be used yet.
 * - cooldown_until in the registry (from a parsed usage-limit reset time)
 * - min gap since the last run on this (provider, profile)
 */
export function pacingGate(profile, provider, minGapSec) {
  const st = providerState(profile, provider);
  if (st.cooldown_until && Date.parse(st.cooldown_until) > Date.now()) {
    throw new SkillError(EXIT.BUSY, `Profile ${profile.id} is in cooldown for ${provider} until ${st.cooldown_until}`,
      `Do not retry before cooldown_until`, { cooldown_until: st.cooldown_until });
  }
  const last = readLastRun(provider, profile.id);
  if (last?.finished_at && minGapSec > 0) {
    const elapsed = (Date.now() - Date.parse(last.finished_at)) / 1000;
    if (elapsed < minGapSec) {
      const wait = Math.ceil(minGapSec - elapsed);
      throw new SkillError(EXIT.BUSY, `Pacing: last ${provider} run on ${profile.id} finished ${Math.floor(elapsed)} s ago; minimum gap is ${minGapSec} s`,
        `Wait ${wait} s, then run once. Never loop`, { wait_sec: wait });
    }
  }
  return true;
}

export function describeProfile(p) {
  const out = { id: p.id, name: p.display_name, enabled: !!p.enabled, chrome_dir: p.chrome_profile_directory ?? null };
  for (const prov of PROVIDERS) {
    const s = p.providers?.[prov];
    if (s) { out[prov] = s.state; if (s.cooldown_until) out[`${prov}_cooldown_until`] = s.cooldown_until; }
  }
  out.locked = isLocked(p.id);
  return out;
}

export function fwdDir(p) { return fwd(p); }
