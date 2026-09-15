// Fake CDP session for firewall tests: records send() calls, can be told to throw.
import { EventEmitter } from 'node:events';

export class FakeCdp extends EventEmitter {
  constructor({ failOn = [] } = {}) {
    super();
    this.sent = [];
    this.failOn = new Set(failOn);
  }
  async send(method, params) {
    this.sent.push({ method, params });
    if (this.failOn.has(method)) throw new Error(`fake ${method} failure`);
    return {};
  }
  methods() { return this.sent.map((s) => s.method); }
  /** Emits Fetch.requestPaused and waits for all handlers to settle. */
  async pause(url, extra = {}) {
    const params = { requestId: `r${this.sent.length + 1}`, request: { url }, resourceType: 'Document', ...extra };
    const handlers = this.listeners('Fetch.requestPaused');
    await Promise.all(handlers.map((h) => h(params)));
    return params.requestId;
  }
}
