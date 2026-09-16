// BrowserPort over a Playwright page. flow.mjs only talks to this interface (or the fake in evals).
// All locator specs come from scripts/lib/providers/<p>.mjs; nothing here is agent-authored.
import { capture } from './observe.mjs';

export function playwrightPort(page) {
  const loc = (spec) => {
    if (spec.role) return page.getByRole(spec.role, { name: spec.name_re ?? spec.name, exact: !!spec.exact });
    return page.locator(spec.css);
  };
  const count = async (spec) => { if (!spec || spec.key) return 0; try { return await loc(spec).count(); } catch { return 0; } };
  return {
    page,
    url: () => page.url(),
    goto: (u) => page.goto(u, { waitUntil: 'domcontentloaded', timeout: 60000 }),
    wait: (ms) => page.waitForTimeout(ms),
    observe: () => capture(page),
    count,
    /** Walks a ladder; returns the first step with >= 1 match: { count, step, handle, ladder }. */
    async findOne(ladder) {
      const results = [];
      for (const step of ladder) {
        if (!step.locator || step.locator.key) continue;
        const n = await count(step.locator);
        results.push({ step: step.id, count: n });
        if (n >= 1) return { count: n, step: step.id, handle: loc(step.locator).first(), ladder: results };
      }
      return { count: 0, step: null, handle: null, ladder: results };
    },
    click: (h) => h.click({ timeout: 5000 }),
    async fill(h, text) {
      try { await h.fill(text, { timeout: 5000 }); }
      catch { await h.click({ timeout: 5000 }); await page.keyboard.insertText(text); }
    },
    async insertText(h, text) {
      await h.click({ timeout: 5000 });
      await page.keyboard.press('Control+a');
      await page.keyboard.insertText(text);
    },
    readText: (h) => h.evaluate((el) => {
      const isField = el.tagName === 'TEXTAREA' || el.tagName === 'INPUT';
      return isField ? (el.value ?? '') : (el.innerText ?? el.textContent ?? '');
    }, undefined, { timeout: 5000 }).catch(() => ''),
    press: (k) => page.keyboard.press(k),
    /** innerText of the LAST element matched by the first ladder step that matches anything. */
    async lastAssistantText(ladder) {
      for (const step of ladder) {
        if (!step.locator?.css) continue;
        const l = page.locator(step.locator.css);
        const n = await l.count().catch(() => 0);
        if (n > 0) return (await l.nth(n - 1).innerText({ timeout: 5000 }).catch(() => '')).trim();
      }
      return '';
    },
  };
}
