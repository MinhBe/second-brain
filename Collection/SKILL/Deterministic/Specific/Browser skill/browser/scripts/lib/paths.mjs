import { resolve, join } from 'node:path';
import { mkdirSync } from 'node:fs';

// The skill folder is resolved from this file, never hard-coded, so the
// authoring path (which contains a non-ASCII segment and spaces) is not baked in.
export const SKILL_ROOT = resolve(import.meta.dirname, '..', '..');

// Runtime data (profiles/state/runs) lives inside the skill folder by default.
// BROWSER_SKILL_DATA=<ascii dir> relocates it if some tool chokes on the path.
const DATA_ROOT = process.env.BROWSER_SKILL_DATA
  ? resolve(process.env.BROWSER_SKILL_DATA)
  : SKILL_ROOT;

// Canonical ASCII invocation path used in SKILL.md (an NTFS junction to SKILL_ROOT).
export const CANONICAL = 'C:/Users/Admin/.claude/skills/browser';

export const DIRS = Object.freeze({
  profiles: join(DATA_ROOT, 'profiles'),
  profilesGeneral: join(DATA_ROOT, 'profiles', 'general'),
  state: join(DATA_ROOT, 'state'),
  pwcli: join(DATA_ROOT, 'state', 'pwcli'),
  snapshots: join(DATA_ROOT, 'state', 'snapshots'),
  screenshots: join(DATA_ROOT, 'state', 'screenshots'),
  extracts: join(DATA_ROOT, 'state', 'extracts'),
  storage: join(DATA_ROOT, 'state', 'storage'),
  logs: join(DATA_ROOT, 'state', 'logs'),
  lastRun: join(DATA_ROOT, 'state', 'last-run'),
  doctor: join(DATA_ROOT, 'state', 'doctor'),
  evals: join(DATA_ROOT, 'state', 'evals'),
  runs: join(DATA_ROOT, 'runs'),
});

export const FILES = Object.freeze({
  registry: join(DIRS.profiles, 'profiles.json'),
  pwcliTemplate: join(SKILL_ROOT, 'config', 'pwcli.template.json'),
  policy: join(SKILL_ROOT, 'scripts', 'lib', 'policy.mjs'),
  policyHash: join(SKILL_ROOT, 'evals', 'fixtures', 'policy.sha256'),
  packageJson: join(SKILL_ROOT, 'package.json'),
});

export const NODE_MODULES = join(SKILL_ROOT, 'node_modules');

export function ensureDirs() {
  for (const d of Object.values(DIRS)) mkdirSync(d, { recursive: true });
}

/** Timestamp safe for file names: 2026-09-11T14-20-01-120Z */
export function tsForFile(d = new Date()) {
  return d.toISOString().replace(/[:.]/g, '-');
}

/** Forward-slash form for display/JSON (works in PowerShell and Git Bash). */
export function fwd(p) {
  return String(p).replace(/\\/g, '/');
}
