// Phase 1 observer flow: a FIXED, linear list of steps against a BrowserPort.
// No step reads response text to decide what to do; text only gets stored and labelled.
// Imports no Playwright, so evals drive it with evals/lib/fake-browser.mjs.
import { classify } from './classify.mjs';
import { scanForInjection } from './injection.mjs';
import { TIERS } from './policy.mjs';
import { sha256Text } from './run-store.mjs';

const norm = (s) => String(s ?? '').replace(/\s+/g, ' ').trim();

const EVENT_FOR_STATE = Object.freeze({
  LOGIN_REQUIRED: 'LOGIN_REQUIRED', SESSION_EXPIRED: 'SESSION_EXPIRED', USAGE_EXHAUSTED: 'USAGE_LIMIT', RATE_LIMITED: 'RATE_LIMIT',
  CAPTCHA: 'CAPTCHA', VERIFICATION_REQUIRED: 'WARNING', ERROR: 'ERROR', UNAVAILABLE: 'ERROR', TIMEOUT: 'TIMEOUT', UNKNOWN: null,
});

/** Notifications from an observation: raw text kept, normalized via the provider's rules, links never followed. */
export function collectNotifications(o, provider) {
  const out = [];
  const texts = [...(o.alerts ?? []).map((t) => ({ t, src: 'alert' })), ...(o.dialogs ?? []).map((t) => ({ t, src: 'dialog' }))];
  for (const { t, src } of texts) {
    const raw = norm(t); if (!raw) continue;
    let normalized_type = 'notification'; let blocking = false;
    for (const rule of provider.rules) {
      if (rule.when.text_re && rule.when.text_re.test(raw)) { normalized_type = rule.state.toLowerCase(); blocking = true; break; }
      if (rule.when.alerts_re && rule.when.alerts_re.test(raw)) { normalized_type = rule.state.toLowerCase(); blocking = true; break; }
    }
    const parsed = {};
    const reset = provider.parseResetTime ? provider.parseResetTime(raw) : null;
    if (reset) { parsed.reset_time = reset.time; parsed.cooldown_until = provider.nextLocalTime(reset.time); }
    out.push({ source: src, raw_text: raw.slice(0, 1000), normalized_type, blocking, parsed, observed_at: o.captured_at, page_url: o.url });
  }
  return out;
}

/**
 * runFlow({ port, store, timeline, provider, prompt, timeoutSec, dryRun, pollMs, progressEverySec, log })
 * -> { status, terminal_state, evidence, reason, response, response_meta, partial_response,
 *      notifications, injection, artifacts_discovered, generation_started, observations, cooldown_until }
 */
export async function runFlow({ port, store, timeline, provider, prompt, timeoutSec = 180, dryRun = false, pollMs = 1000, progressEverySec = 5, startWindowMs = 20000, log = () => {} }) {
  const t = (event, data = {}, tier = null) => timeline.append(event, data, tier);
  const result = { status: null, terminal_state: null, evidence: null, reason: null, response: null, response_meta: null, partial_response: null, notifications: [], injection: [], artifacts_discovered: 0, generation_started: false, observations: 0, cooldown_until: null };
  const shot = async (slug) => { const r = await store.screenshot(port.page, slug); t('SCREENSHOT_CAPTURED', { file: r.file, sha256: r.sha256, slug }, TIERS.OBSERVE); return r; };
  const observe = async () => { const o = await port.observe(); result.observations++; return o; };
  const finish = async (state, o, cls, extra = {}) => {
    await shot(state.toLowerCase());
    if (o) store.writeObservation(o);
    const ev = EVENT_FOR_STATE[state];
    if (ev) t(ev, { evidence: cls?.evidence ?? null, ...extra }, TIERS.OBSERVE);
    result.status = state; result.terminal_state = state; result.evidence = cls?.evidence ?? null; result.reason = cls?.reason ?? null;
    if (o) { result.notifications = collectNotifications(o, provider); store.writeNotifications(result.notifications); const cd = result.notifications.find((n) => n.parsed?.cooldown_until); if (cd) result.cooldown_until = cd.parsed.cooldown_until; }
    return result;
  };
  const classifyOrStop = async (o) => { const cls = classify(o, provider.id); t('STATE_CLASSIFIED', { state: cls.state, evidence: cls.evidence, reason: cls.reason }, TIERS.OBSERVE); return cls; };

  // 1. open
  await port.goto(provider.entryUrl).catch((e) => log(`goto: ${e.message}`));
  t('PAGE_OPENED', { url: port.url(), entry_url: provider.entryUrl }, TIERS.INTERACT);
  await port.wait(2000);
  await shot('page-opened');

  // 2. verify auth
  let o = await observe();
  let cls = await classifyOrStop(o);
  if (cls.state !== 'READY') {
    if (cls.state === 'LOGIN_REQUIRED' || cls.state === 'SESSION_EXPIRED') t('AUTH_FAILED', { evidence: cls.evidence }, TIERS.OBSERVE);
    return finish(cls.state, o, cls);
  }
  t('AUTH_VERIFIED', { evidence: cls.evidence }, TIERS.OBSERVE);
  await shot('auth-verified');

  // 3. composer (exactly one)
  const comp = await port.findOne(provider.composer);
  if (comp.count !== 1) {
    t('ADAPTER_DRIFT', { part: 'composer', ladder: comp.ladder }, TIERS.OBSERVE);
    return finish('UNKNOWN', o, { evidence: { type: 'composer', text: `${comp.count} composer candidates` }, reason: 'composer ladder' });
  }

  // 4. focus + type + read back
  await port.click(comp.handle);
  t('COMPOSER_FOCUSED', { step: comp.step }, TIERS.INTERACT);
  await port.fill(comp.handle, prompt);
  t('PROMPT_TYPED', { chars: prompt.length, sha256: sha256Text(prompt) }, TIERS.INTERACT);
  let typed = await port.readText(comp.handle);
  if (norm(typed) !== norm(prompt)) {
    await port.insertText(comp.handle, prompt);
    typed = await port.readText(comp.handle);
  }
  if (norm(typed) !== norm(prompt)) {
    t('ADAPTER_DRIFT', { part: 'composer-readback', typed_chars: norm(typed).length, expected_chars: norm(prompt).length }, TIERS.OBSERVE);
    return finish('UNKNOWN', await observe(), { evidence: { type: 'composer', text: 'typed text did not match the prompt' }, reason: 'composer readback' });
  }
  t('COMPOSER_VERIFIED', { chars: norm(typed).length }, TIERS.OBSERVE);
  await shot('composer-verified');
  if (dryRun) {
    t('DRY_RUN_STOP', {}, null);
    result.status = 'DRY_RUN'; result.terminal_state = 'READY'; result.evidence = cls.evidence;
    return result;
  }

  // 5. send
  const snd = await port.findOne(provider.send.filter((s) => !s.locator.key));
  if (snd.count === 1) await port.click(snd.handle); else await port.press('Enter');
  t('PROMPT_SUBMITTED', { via: snd.count === 1 ? snd.step : 'enter-key', prompt_sha256: sha256Text(prompt) }, TIERS.INTERACT);
  await shot('prompt-submitted');

  // 6. generation started
  const stopSpec = provider.generationStarted.find((g) => g.locator.role)?.locator ?? null;
  const startDeadline = Date.now() + startWindowMs;
  let started = false;
  while (Date.now() < startDeadline) {
    const stopVisible = stopSpec ? (await port.count(stopSpec)) > 0 : false;
    const assistant = await port.lastAssistantText(provider.assistantMessage);
    if (stopVisible || assistant.length > 0) { started = true; break; }
    await port.wait(500);
  }
  if (!started) {
    o = await observe(); cls = await classifyOrStop(o);
    if (cls.blocking && cls.state !== 'UNKNOWN') return finish(cls.state, o, cls);
    return finish('UNKNOWN', o, { evidence: { type: 'generation', text: `no generation signal within ${startWindowMs} ms` }, reason: 'no generation' });
  }
  t('GENERATION_STARTED', {}, TIERS.OBSERVE);
  result.generation_started = true;
  await shot('generation-started');

  // 7. poll until complete
  const deadline = Date.now() + timeoutSec * 1000;
  let lastText = '', stable = 0, lastProgress = Date.now(), completed = false, ticks = 0;
  while (Date.now() < deadline) {
    await port.wait(pollMs);
    ticks++;
    const stopVisible = stopSpec ? (await port.count(stopSpec)) > 0 : false;
    const text = await port.lastAssistantText(provider.assistantMessage);
    if (Date.now() - lastProgress >= progressEverySec * 1000) { t('GENERATION_PROGRESS', { chars: text.length, stop_visible: stopVisible }, TIERS.OBSERVE); lastProgress = Date.now(); }
    if (ticks % 3 === 0 || stopVisible === false) {
      o = await observe();
      const mid = classify(o, provider.id);
      if (mid.blocking && mid.state !== 'UNKNOWN') {
        t('STATE_CLASSIFIED', { state: mid.state, evidence: mid.evidence, reason: mid.reason, during: 'generation' }, TIERS.OBSERVE);
        if (text) { store.writeResponse(text); result.partial_response = text; }
        return finish(mid.state, o, mid, { partial_chars: text.length });
      }
    }
    if (!stopVisible && text.length > 0 && text === lastText) { stable++; if (stable >= 2) { completed = true; break; } } else stable = 0;
    lastText = text;
  }
  if (!completed) {
    if (lastText) { store.writeResponse(lastText); result.partial_response = lastText; }
    return finish('TIMEOUT', await observe(), { evidence: { type: 'timeout', text: `no completion within ${timeoutSec} s` }, reason: 'timeout' }, { partial_chars: lastText.length });
  }
  t('GENERATION_COMPLETED', { chars: lastText.length }, TIERS.OBSERVE);

  // 8. response = data
  const meta = store.writeResponse(lastText);
  t('ASSISTANT_RESPONSE', { chars: meta.chars, sha256: meta.sha256 }, TIERS.OBSERVE);
  result.response = lastText; result.response_meta = meta;
  result.injection = scanForInjection(lastText);
  for (const h of result.injection) t('SUSPECTED_INJECTION', { rule: h.rule, excerpt: h.excerpt }, TIERS.OBSERVE);

  // 9. notifications on the final page
  o = await observe();
  result.notifications = collectNotifications(o, provider);
  store.writeNotifications(result.notifications);
  for (const n of result.notifications) t(n.normalized_type === 'usage_exhausted' ? 'USAGE_LIMIT' : n.normalized_type === 'rate_limited' ? 'RATE_LIMIT' : 'NOTIFICATION', { raw_text: n.raw_text.slice(0, 300), normalized_type: n.normalized_type, blocking: n.blocking, parsed: n.parsed }, TIERS.OBSERVE);
  const cd = result.notifications.find((n) => n.parsed?.cooldown_until); if (cd) result.cooldown_until = cd.parsed.cooldown_until;

  // 10. artifacts: detect only
  const art = provider.artifactHints[0] ? await port.count(provider.artifactHints[0].locator) : 0;
  if (art > 0) { t('ARTIFACT_DISCOVERED', { count: art, note: 'not opened; artifact reader lands in Phase 3' }, TIERS.OBSERVE); result.artifacts_discovered = art; }

  await shot('final');
  store.writeObservation(o);
  result.status = 'COMPLETED'; result.terminal_state = 'READY'; result.evidence = cls.evidence;
  return result;
}
