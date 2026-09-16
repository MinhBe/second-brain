// Layer 3 — fail-closed state classifier. Data-driven by scripts/lib/providers/<p>.mjs.
// Either a rule matches WITH evidence, or the state is UNKNOWN. There is no "else: try something".
import { BLOCKING_STATES, STATES } from './policy.mjs';
import { allText } from './observe.mjs';
import { getProvider } from './providers/index.mjs';

function testWhen(when, o) {
  const text = allText(o);
  const checks = [];
  if (when.url_re) checks.push({ ok: when.url_re.test(o.url), src: 'url', sample: o.url });
  if (when.not_url_re) checks.push({ ok: !when.not_url_re.test(o.url), src: 'url', sample: o.url });
  if (when.text_re) { const m = text.match(when.text_re); checks.push({ ok: !!m, src: 'visible_text', sample: m ? m[0] : null }); }
  if (when.aria_re) { const m = (o.aria_yaml ?? '').match(when.aria_re); checks.push({ ok: !!m, src: 'aria', sample: m ? m[0] : null }); }
  if (when.alerts_re) { const hit = (o.alerts ?? []).find((a) => when.alerts_re.test(a)); checks.push({ ok: !!hit, src: 'alert', sample: hit ?? null }); }
  if (when.dialogs_re) { const hit = (o.dialogs ?? []).find((a) => when.dialogs_re.test(a)); checks.push({ ok: !!hit, src: 'dialog', sample: hit ?? null }); }
  if (when.iframe_title_re) { const hit = (o.iframes ?? []).find((f) => when.iframe_title_re.test(f.title ?? '')); checks.push({ ok: !!hit, src: 'iframe', sample: hit?.title ?? null }); }
  if (when.iframe_host_re) { const hit = (o.iframes ?? []).find((f) => when.iframe_host_re.test(f.src_host ?? '')); checks.push({ ok: !!hit, src: 'iframe', sample: hit?.src_host ?? null }); }
  if (!checks.length) return { ok: false, evidence: null };
  const ok = checks.every((c) => c.ok);
  const ev = checks.find((c) => c.ok && c.sample) ?? checks[0];
  return { ok, evidence: ok ? { type: ev.src, text: String(ev.sample ?? '').slice(0, 200) } : null };
}

/** Counts composer candidates in the aria snapshot using the provider's ladder (aria_re entries only). */
export function findComposerInAria(o, provider) {
  const p = getProvider(provider);
  const results = [];
  for (const step of p.composer) {
    if (!step.aria_re) continue;
    const re = new RegExp(step.aria_re.source, step.aria_re.flags.includes('g') ? step.aria_re.flags : step.aria_re.flags + 'g');
    const count = ((o.aria_yaml ?? '').match(re) ?? []).length;
    results.push({ step: step.id, count });
    if (count === 1) return { found: 1, step: step.id, ladder: results };
    if (count > 1) return { found: count, step: step.id, ladder: results };
  }
  return { found: 0, step: null, ladder: results };
}

/**
 * classify(observation, providerId) -> { state, evidence, blocking, matched: [...], reason }
 * Order: provider.rules (blocking first) -> READY needs exactly one composer -> else UNKNOWN.
 */
export function classify(o, providerId) {
  const p = getProvider(providerId);
  const matched = [];
  for (const rule of p.rules) {
    const r = testWhen(rule.when, o);
    if (r.ok) matched.push({ state: rule.state, rule: rule.id, evidence: r.evidence, blocking: BLOCKING_STATES.includes(rule.state) });
  }
  const blocking = matched.filter((m) => m.blocking);
  const distinct = [...new Set(blocking.map((m) => m.state))];
  if (distinct.length > 1) {
    return { state: 'UNKNOWN', evidence: { type: 'ambiguous', text: distinct.join(' vs ') }, blocking: true, matched, reason: 'two blocking states matched' };
  }
  if (distinct.length === 1) {
    const m = blocking[0];
    return { state: m.state, evidence: { ...m.evidence, rule: m.rule }, blocking: true, matched, reason: `rule ${m.rule}` };
  }
  const nonBlocking = matched.filter((m) => !m.blocking && m.state !== 'READY');
  if (nonBlocking.length) {
    const m = nonBlocking[0];
    return { state: m.state, evidence: { ...m.evidence, rule: m.rule }, blocking: false, matched, reason: `rule ${m.rule}` };
  }
  const composer = findComposerInAria(o, providerId);
  if (composer.found === 1 && (!p.readyWhen || testWhen(p.readyWhen, o).ok)) {
    return { state: 'READY', evidence: { type: 'aria', text: `composer via ${composer.step}` }, blocking: false, matched, reason: 'exactly one composer' };
  }
  return {
    state: 'UNKNOWN',
    evidence: { type: 'composer', text: composer.found === 0 ? 'no composer candidate matched' : `${composer.found} composer candidates matched (${composer.step})` },
    blocking: true, matched, reason: composer.found === 0 ? 'composer not found' : 'composer ambiguous', drift: composer.found !== 1,
  };
}

export function isKnownState(s) { return STATES.includes(s); }
