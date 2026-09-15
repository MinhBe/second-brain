// Scripted BrowserPort for flow evals. No browser, no LLM. Records every action.
import { readFileSync } from 'node:fs';
import { fromFixture } from '../../scripts/lib/observe.mjs';

/**
 * new FakeBrowser({ observation, composerCount, sendCount, response, streamTicks, stopAfterSend, midGenerationObservation, artifactCount })
 */
export class FakeBrowser {
  constructor(opts) {
    this.o = fromFixture(opts.observation);
    this.composerCount = opts.composerCount ?? 1;
    this.sendCount = opts.sendCount ?? 1;
    this.response = opts.response ?? 'PONG';
    this.streamTicks = opts.streamTicks ?? 3;
    this.artifactCount = opts.artifactCount ?? 0;
    this.midGenerationObservation = opts.midGenerationObservation ? fromFixture(opts.midGenerationObservation) : null;
    this.midAfterTicks = opts.midAfterTicks ?? 2;
    this.composerText = '';
    this.sent = false;
    this.tick = 0;
    this.actions = [];
    this.page = { screenshot: async () => { throw new Error('fake: no screenshots'); } };
    this._url = 'about:blank';
  }
  url() { return this._url; }
  // goto "lands" on the fixture's URL (a login redirect, for example), like a real browser would.
  async goto(u) { this._url = this.o.url || u; this.actions.push({ action: 'goto', url: u }); }
  async wait() { if (this.sent) this.tick++; }
  async observe() {
    if (this.sent && this.midGenerationObservation && this.tick >= this.midAfterTicks) return this.midGenerationObservation;
    return { ...this.o };
  }
  async count(spec) {
    if (spec.role === 'button' && /stop/i.test(String(spec.name_re))) return this.sent && this.tick < this.streamTicks ? 1 : 0;
    if (spec.role === 'button' && /send/i.test(String(spec.name_re))) return this.sendCount;
    if (spec.role === 'button' && /artifact/i.test(String(spec.name_re))) return this.artifactCount;
    if (spec.css && /assistant/.test(spec.css)) return this.sent && this.tick >= 1 ? 1 : 0;
    return 0;
  }
  async findOne(ladder) {
    const first = ladder[0];
    if (first && first.locator?.role === 'textbox') {
      const n = this.composerCount;
      return { count: n, step: n ? first.id : null, handle: n ? { kind: 'composer' } : null, ladder: [{ step: first.id, count: n }] };
    }
    if (first && /send/i.test(String(first.locator?.name_re))) {
      return { count: this.sendCount, step: this.sendCount ? first.id : null, handle: this.sendCount ? { kind: 'send' } : null, ladder: [] };
    }
    return { count: 0, step: null, handle: null, ladder: [] };
  }
  async click(h) { this.actions.push({ action: 'click', target: h?.kind }); if (h?.kind === 'send') { this.sent = true; this.tick = 0; } }
  async fill(h, text) { this.actions.push({ action: 'fill', target: h?.kind, chars: text.length }); this.composerText = text; }
  async insertText(h, text) { this.actions.push({ action: 'insertText', target: h?.kind }); this.composerText = text; }
  async readText() { return this.composerText; }
  async press(k) { this.actions.push({ action: 'press', key: k }); if (k === 'Enter') { this.sent = true; this.tick = 0; } }
  async lastAssistantText() {
    if (!this.sent || this.tick < 1) return '';
    const n = Math.min(this.tick, this.streamTicks);
    return this.response.slice(0, Math.ceil((this.response.length * n) / this.streamTicks));
  }
}

export function loadObservation(fixturesDir, name) {
  return JSON.parse(readFileSync(`${fixturesDir}/observations/${name}.json`, 'utf8'));
}
