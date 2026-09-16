// Observation = what the browser actually shows. Same shape from a live page or a fixture.
// { url, title, aria_yaml, alerts[], dialogs[], iframes[{title, src_host}], visible_text_sample, captured_at }
export const OBSERVATION_KEYS = Object.freeze(['url', 'title', 'aria_yaml', 'alerts', 'dialogs', 'iframes', 'visible_text_sample', 'captured_at']);

async function safe(p, fallback) { try { return await p; } catch { return fallback; } }

export async function capture(page, { textSample = 4000 } = {}) {
  const url = page.url();
  const title = await safe(page.title(), '');
  const aria_yaml = await safe(page.locator('body').ariaSnapshot(), '');
  const alerts = await safe(page.locator('[role="alert"], [role="status"], [aria-live="assertive"], [aria-live="polite"]').allInnerTexts(), []);
  const dialogs = await safe(page.locator('[role="dialog"], [role="alertdialog"], dialog[open]').allInnerTexts(), []);
  const iframes = [];
  for (const f of page.frames()) {
    if (f === page.mainFrame()) continue;
    let host = null; try { host = new URL(f.url()).hostname; } catch { /* about:blank etc. */ }
    iframes.push({ title: await safe(f.title(), ''), src_host: host, name: f.name() || null });
  }
  const visible_text_sample = (await safe(page.locator('body').innerText(), '')).replace(/\s+/g, ' ').slice(0, textSample);
  return {
    url, title, aria_yaml,
    alerts: alerts.map((t) => t.trim()).filter(Boolean),
    dialogs: dialogs.map((t) => t.trim()).filter(Boolean),
    iframes,
    visible_text_sample,
    captured_at: new Date().toISOString(),
  };
}

/** Validates a fixture / stored observation. Throws on missing keys. */
export function fromFixture(obj) {
  const o = { alerts: [], dialogs: [], iframes: [], visible_text_sample: '', ...obj };
  for (const k of ['url', 'title', 'aria_yaml']) if (typeof o[k] !== 'string') throw new Error(`observation.${k} must be a string`);
  o.captured_at = o.captured_at ?? new Date().toISOString();
  return o;
}

/** All text an observation exposes, for text rules. */
export function allText(o) {
  return [o.title, o.aria_yaml, ...(o.alerts ?? []), ...(o.dialogs ?? []), o.visible_text_sample ?? ''].join('\n');
}
