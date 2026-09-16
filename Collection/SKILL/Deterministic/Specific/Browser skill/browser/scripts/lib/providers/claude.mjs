// Claude (claude.ai) adapter DATA. No code that acts; only entry URL, hosts, state rules and locator ladders.
// provenance: values marked TO_CAPTURE are best-known defaults and must be confirmed against a live,
// sanitized accessibility snapshot during Phase C (see references/providers/claude.md).
export const id = 'claude';
export const implemented = true;
export const phase = 'phase-1';
export const entryUrl = 'https://claude.ai/new?incognito=';
export const hosts = Object.freeze(['claude.ai']);

// Blocking-state rules, evaluated in order. A rule matches when ALL `when` conditions hold.
export const rules = Object.freeze([
  { id: 'captcha-turnstile', state: 'CAPTCHA', when: { iframe_title_re: /cloudflare|security challenge|turnstile/i } },
  // captured live 2026-09-11 (run_20260911T142559Z_8bb9): title "Just a moment...", heading "Performing security verification"
  { id: 'cf-interstitial', state: 'CAPTCHA', when: { text_re: /just a moment|performing security verification|verif(?:y|ies) (?:that )?you are (?:a human|not a bot)|security service to protect against malicious bots|checking (?:if the site connection is secure|your browser)/i } },
  { id: 'captcha-text', state: 'CAPTCHA', when: { text_re: /verify (that )?you are (a )?human|security check|complete the (captcha|challenge)|blocked from reaching .challenges\.cloudflare\.com/i } },
  { id: 'verification', state: 'VERIFICATION_REQUIRED', when: { text_re: /verify your (phone|email|identity)|enter the (verification )?code|we sent (you )?a code|two-factor|2fa/i } },
  { id: 'login-url', state: 'LOGIN_REQUIRED', when: { url_re: /^https:\/\/claude\.ai\/(login|magic-link|oauth)/i } },
  { id: 'login-text', state: 'LOGIN_REQUIRED', when: { not_url_re: /^https:\/\/claude\.ai\/(new|chat)/i, text_re: /continue with google|log in with|sign in with|sign in to claude|log in to claude|create (an )?account/i } },
  { id: 'session-expired', state: 'SESSION_EXPIRED', when: { text_re: /session (has )?expired|you('ve| have) been (logged|signed) out|please (log|sign) in again/i } },
  { id: 'usage-limit', state: 'USAGE_EXHAUSTED', when: { text_re: /out of (free )?messages|reached your (usage|message) limit|usage limit reached|you('ve| have) reached the limit|limit resets|until \d{1,2}(:\d{2})?\s?[ap]m/i } },
  { id: 'rate-limit', state: 'RATE_LIMITED', when: { text_re: /rate limit|too many requests|slow down|unusual activity|try again in a (few|moment)/i } },
  { id: 'unavailable', state: 'UNAVAILABLE', when: { text_re: /temporarily unavailable|under maintenance|is down for|503|502 bad gateway|we('re| are) experiencing (an )?(outage|high demand|issues)/i } },
  { id: 'error', state: 'ERROR', when: { alerts_re: /something went wrong|an error occurred|unable to|failed to/i } },
]);

// Composer ladder. Exactly ONE candidate must match, else ADAPTER_DRIFT -> UNKNOWN.
// aria_re is used on the snapshot text (classify); locator is used live (flow).
export const composer = Object.freeze([
  { id: 'textbox-prompt', aria_re: /- textbox "[^"]*(prompt|message|help|reply|talk|ask)[^"]*"/i, locator: { role: 'textbox', name_re: /(prompt|message|help|reply|talk|ask)/i }, provenance: 'TO_CAPTURE' },
  { id: 'contenteditable', aria_re: null, locator: { css: 'div[contenteditable="true"][data-placeholder], div.ProseMirror[contenteditable="true"]' }, provenance: 'TO_CAPTURE' },
]);

export const send = Object.freeze([
  { id: 'send-button', locator: { role: 'button', name_re: /^send( message)?$/i }, provenance: 'TO_CAPTURE' },
  { id: 'enter-key', locator: { key: 'Enter' } },
]);

export const generationStarted = Object.freeze([
  { id: 'stop-button', locator: { role: 'button', name_re: /^stop( response| generating)?$/i }, provenance: 'TO_CAPTURE' },
  { id: 'assistant-node', locator: { css: '[data-testid="assistant-message"], .font-claude-message, div[data-is-streaming]' }, provenance: 'TO_CAPTURE' },
]);

export const assistantMessage = Object.freeze([
  { id: 'assistant-testid', locator: { css: '[data-testid="assistant-message"]' }, provenance: 'TO_CAPTURE' },
  { id: 'assistant-class', locator: { css: '.font-claude-message' }, provenance: 'TO_CAPTURE' },
  { id: 'assistant-streaming-attr', locator: { css: 'div[data-is-streaming]' }, provenance: 'TO_CAPTURE' },
]);

export const userMessage = Object.freeze([
  { id: 'user-testid', locator: { css: '[data-testid="user-message"]' }, provenance: 'TO_CAPTURE' },
]);

export const artifactHints = Object.freeze([
  { id: 'artifact-button', locator: { role: 'button', name_re: /artifact|preview|open in|download/i } },
]);

export const notificationRegions = Object.freeze({
  toast_css: '[role="status"], [role="alert"], [data-sonner-toast], [class*="toast"]',
  banner_css: '[role="banner"] [class*="banner"], [class*="notice"], [class*="Banner"]',
});

/** Parses a reset time such as "until 5:40 AM" -> { time: '05:40', raw } or null. */
export function parseResetTime(text) {
  const m = String(text ?? '').match(/until\s+(\d{1,2})(?::(\d{2}))?\s?([ap])\.?m\.?/i);
  if (!m) return null;
  let h = Number(m[1]) % 12; if (m[3].toLowerCase() === 'p') h += 12;
  const mm = m[2] ?? '00';
  return { time: `${String(h).padStart(2, '0')}:${mm}`, raw: m[0] };
}

/** Turns a parsed HH:MM (local) into the next ISO timestamp after `now`. */
export function nextLocalTime(hhmm, now = new Date()) {
  const [h, m] = hhmm.split(':').map(Number);
  const d = new Date(now); d.setHours(h, m, 0, 0);
  if (d <= now) d.setDate(d.getDate() + 1);
  return d.toISOString();
}

export const notes = 'Terms of service: claude.ai prohibits automated access; use a profile whose account is separate from the one that runs Claude Code, keep runs human-paced, single-shot.';
