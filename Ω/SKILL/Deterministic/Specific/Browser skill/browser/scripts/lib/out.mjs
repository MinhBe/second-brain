import { writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { EXIT, CODE_BY_EXIT, SkillError } from './exit-codes.mjs';
import { DIRS, tsForFile, fwd } from './paths.mjs';

export const MAX_STDOUT_BYTES = 2048;

const REDACT_KEY = /^(authorization|cookie|set-cookie|x-api-key|x-auth-token|password|passwd|secret|token|access_token|refresh_token|client_secret|api_key)$/i;
const REDACT_URL = /([?&](?:api_key|token|access_token|client_secret|refresh_token)=)[^&#\s]+/gi;

/** Deep-redacts secret-looking keys and URL params. Never mutates the input. */
export function redact(value, depth = 0) {
  if (depth > 12) return '[depth]';
  if (typeof value === 'string') return value.replace(REDACT_URL, '$1***');
  if (Array.isArray(value)) return value.map((v) => redact(v, depth + 1));
  if (value && typeof value === 'object') {
    const out = {};
    for (const [k, v] of Object.entries(value)) {
      out[k] = REDACT_KEY.test(k) ? '***' : redact(v, depth + 1);
    }
    return out;
  }
  return value;
}

/** Human-readable detail goes to stderr only. */
export function log(...parts) {
  process.stderr.write(parts.map((p) => (typeof p === 'string' ? p : JSON.stringify(p))).join(' ') + '\n');
}

function spill(verb, obj) {
  mkdirSync(DIRS.logs, { recursive: true });
  const p = join(DIRS.logs, `${verb.replace(/[^a-z0-9_.-]/gi, '_')}-${tsForFile()}.json`);
  writeFileSync(p, JSON.stringify(obj, null, 2));
  return fwd(p);
}

/**
 * Emits EXACTLY one JSON line on stdout and sets process.exitCode.
 * Fields: ok, verb, code, exit, ...fields, next. Total line <= 2048 bytes,
 * otherwise the full object is written to state/logs and replaced by `_path`.
 */
export function emit(verb, exit, fields = {}, next = '') {
  const base = { ok: exit === EXIT.OK, verb, code: CODE_BY_EXIT[exit] ?? 'INTERNAL', exit };
  const full = redact({ ...base, ...fields, next });
  let line = JSON.stringify(full);
  if (Buffer.byteLength(line, 'utf8') > MAX_STDOUT_BYTES) {
    const _path = spill(verb, full);
    const slim = { ...base, _path, next };
    // keep small scalar fields so the agent still sees the essentials
    for (const [k, v] of Object.entries(full)) {
      if (k in slim) continue;
      if (typeof v === 'string' && v.length <= 120) slim[k] = v;
      else if (typeof v === 'number' || typeof v === 'boolean' || v === null) slim[k] = v;
    }
    line = JSON.stringify(slim);
    if (Buffer.byteLength(line, 'utf8') > MAX_STDOUT_BYTES) {
      line = JSON.stringify({ ...base, _path, next });
    }
  }
  process.stdout.write(line + '\n');
  process.exitCode = exit;
  return exit;
}

export function ok(verb, fields, next) {
  return emit(verb, EXIT.OK, fields, next);
}

export function fail(verb, exit, error, next, fields = {}) {
  return emit(verb, exit, { ...fields, error }, next);
}

/** Top-level guard for every script: converts thrown errors into one JSON line. */
export async function main(verb, fn) {
  try {
    await fn();
  } catch (e) {
    if (e instanceof SkillError) {
      return fail(e.verb ?? verb, e.exit, e.message, e.next ?? '', e.extra);
    }
    const logPath = spill(`${verb}-internal`, { message: String(e?.message ?? e), stack: String(e?.stack ?? '') });
    return fail(verb, EXIT.INTERNAL, String(e?.message ?? e), `Report this error and the log at ${logPath}`, { log_path: logPath });
  }
}

/** `--help` support: one JSON line listing verbs. */
export function helpLine(script, verbs, extra = {}) {
  return ok(`${script}.help`, { script, verbs, ...extra }, `Run: node <skill>/scripts/${script}.mjs <verb> ...`);
}
