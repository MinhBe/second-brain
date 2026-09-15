// COMPILED-IN POLICY. This file is code, not configuration.
// Its sha256 is pinned in evals/fixtures/policy.sha256; doctor.mjs and the
// `allowlist-frozen` eval fail when it changes without the pin being updated.
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

function frozenSet(items) {
  const set = new Set(items.map((s) => String(s).toLowerCase()));
  return new Proxy(set, {
    get(target, prop) {
      if (prop === 'add' || prop === 'delete' || prop === 'clear') {
        return () => { throw new Error('policy set is immutable'); };
      }
      const v = Reflect.get(target, prop, target);
      return typeof v === 'function' ? v.bind(target) : v;
    },
    set() { throw new Error('policy set is immutable'); },
    deleteProperty() { throw new Error('policy set is immutable'); },
  });
}

/**
 * Hosts an observer run may talk to. Exact host match, case-insensitive, no www-stripping.
 * challenges.cloudflare.com: spike S2, run_20260911T142559Z_8bb9 — claude.ai's front door loads its
 * bot-check script from this host; with it blocked, Cloudflare shows "Incompatible browser extension or
 * network configuration" and nothing else ever renders. Allowing the host only lets the site's own
 * verification run as it would in any browser; the observer never clicks or solves a challenge
 * (CAPTCHA is a stop state). Adding a host here is a code change + hash re-pin, never a runtime flag.
 */
export const OBSERVER_ALLOWLIST = frozenSet(['claude.ai', 'chatgpt.com', 'www.meta.ai', 'challenges.cloudflare.com', 'assets-proxy.anthropic.com']);

/** Extra hosts allowed ONLY during `profile login` (human sign-in). Confirmed/expanded by spike S2. */
export const LOGIN_EXTRA_HOSTS = frozenSet([
  'accounts.google.com',
  'www.gstatic.com',
  'ssl.gstatic.com',
  'apis.google.com',
  'fonts.gstatic.com',
  'lh3.googleusercontent.com',
]);

/** Provider hosts that bw.mjs refuses (they must go through aiweb.mjs / profile login). Includes subdomains. */
export const RESERVED_HOSTS = frozenSet(['claude.ai', 'chatgpt.com', 'meta.ai']);

export const INTERNAL_URL_RE = /^(about|chrome|devtools|data|blob):/i;

export const STATES = Object.freeze([
  'UNKNOWN', 'READY', 'LOGIN_REQUIRED', 'SESSION_EXPIRED', 'USAGE_EXHAUSTED',
  'RATE_LIMITED', 'VERIFICATION_REQUIRED', 'CAPTCHA', 'ERROR', 'UNAVAILABLE', 'BUSY',
]);

export const BLOCKING_STATES = Object.freeze([
  'LOGIN_REQUIRED', 'SESSION_EXPIRED', 'USAGE_EXHAUSTED', 'RATE_LIMITED',
  'VERIFICATION_REQUIRED', 'CAPTCHA', 'ERROR', 'UNAVAILABLE',
]);

export const EVENTS = Object.freeze([
  // SPEC-1
  'PAGE_OPENED', 'AUTH_VERIFIED', 'AUTH_FAILED', 'PROMPT_SUBMITTED', 'GENERATION_STARTED',
  'GENERATION_PROGRESS', 'GENERATION_COMPLETED', 'ASSISTANT_RESPONSE', 'NOTIFICATION', 'WARNING',
  'ERROR', 'USAGE_LIMIT', 'RATE_LIMIT', 'LOGIN_REQUIRED', 'SESSION_EXPIRED', 'CAPTCHA',
  'ARTIFACT_DISCOVERED', 'ARTIFACT_OPENED', 'ARTIFACT_READ', 'DOWNLOAD_STARTED', 'DOWNLOAD_COMPLETED',
  'NAVIGATION', 'SCREENSHOT_CAPTURED', 'RUN_COMPLETED', 'RUN_FAILED',
  // added by this skill
  'RUN_STARTED', 'PROFILE_SELECTED', 'PROFILE_LOCK_ACQUIRED', 'PROFILE_LOCK_RELEASED', 'BROWSER_LAUNCHED',
  'BLOCKED_NAVIGATION', 'HANDLER_ERROR_BLOCKED', 'POPUP_BLOCKED', 'DOWNLOAD_BLOCKED',
  'SUSPECTED_INJECTION', 'ADAPTER_DRIFT', 'COMPOSER_FOCUSED', 'PROMPT_TYPED', 'COMPOSER_VERIFIED',
  'STATE_CLASSIFIED', 'DRY_RUN_STOP', 'TIMEOUT', 'AUDIT_PUSHED', 'AUDIT_PUSH_SKIPPED',
]);

export const TIERS = Object.freeze({ OBSERVE: 0, INTERACT: 1, HUMAN: 2 });

/** Actions the observer may take on its own inside a locked run (Tier 1). Nothing else exists. */
export const TIER1_ACTIONS = Object.freeze(['open', 'verify_auth', 'focus_composer', 'type', 'send', 'poll']);

export function isReservedHost(host) {
  const h = String(host ?? '').toLowerCase();
  for (const r of RESERVED_HOSTS) {
    if (h === r || h.endsWith('.' + r)) return true;
  }
  return false;
}

export function hostOf(url) {
  return new URL(url).hostname.toLowerCase();
}

export function policySha256() {
  const bytes = readFileSync(import.meta.filename);
  return createHash('sha256').update(bytes).digest('hex');
}
