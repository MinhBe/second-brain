// Layer 2 — page content is data. This scanner only LABELS suspicious text; nothing acts on it.
const RULES = Object.freeze([
  { id: 'ignore-previous', re: /^\s*(ignore|disregard|forget)\s+(all|any|the|your|previous|prior|above|earlier)\b/im },
  { id: 'new-instructions', re: /\b(new|updated|real|actual)\s+instructions?\b|\byou are now\b|\bsystem prompt\b|\bdeveloper message\b/i },
  { id: 'navigate', re: /\b(navigate|go|browse|open|visit)\s+(to\s+)?(https?:|file:|chrome:|about:|www\.)/i },
  { id: 'click-link', re: /\bclick\s+(on\s+)?(the\s+|this\s+|that\s+)?[\w"'-]+\s+(link|button)\b/i },
  { id: 'run-command', re: /\b(run|execute|paste)\s+(this|the|following)?\s*(command|script|code|shell|terminal)\b/i },
  { id: 'shell', re: /\b(curl|wget|powershell|cmd\.exe|bash|sh|node|python)\s+-?\S+/i },
  { id: 'exfil', re: /\b(send|post|upload|paste|share|reveal|print)\s+(me\s+|us\s+)?(the\s+|your\s+)?(cookies?|tokens?|passwords?|credentials?|api\s*keys?|session)\b/i },
  { id: 'settings', re: /\b(change|update|edit)\s+(the\s+|your\s+)?(account|profile|settings?|password|email)\b/i },
]);

/** Returns [{ rule, index, excerpt }]. Empty array means nothing looked like an instruction. */
export function scanForInjection(text, { excerpt = 120 } = {}) {
  const s = String(text ?? '');
  const hits = [];
  for (const r of RULES) {
    const m = s.match(r.re);
    if (!m) continue;
    const idx = m.index ?? 0;
    hits.push({ rule: r.id, index: idx, excerpt: s.slice(Math.max(0, idx - 20), idx + excerpt).replace(/\s+/g, ' ').trim() });
  }
  return hits;
}

export const INJECTION_RULE_IDS = Object.freeze(RULES.map((r) => r.id));
