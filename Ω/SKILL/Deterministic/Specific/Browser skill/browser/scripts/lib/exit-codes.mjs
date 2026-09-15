// Exit codes shared by every script. Documented for agents in references/exit-codes.md.
export const EXIT = Object.freeze({
  OK: 0,
  INTERNAL: 1,
  USAGE: 2,
  PRECONDITION: 3,
  NOT_FOUND: 4,
  TARGET: 5,
  TIMEOUT: 6,
  POLICY: 7,
  HUMAN: 8,
  UNKNOWN: 9,
  PROVIDER: 10,
  TOOL: 11,
  BUSY: 12,
  AUDIT: 13,
});

export const CODE_BY_EXIT = Object.freeze(
  Object.fromEntries(Object.entries(EXIT).map(([code, n]) => [n, code])),
);

/** Error that carries an exit code and an agent-facing `next` hint. */
export class SkillError extends Error {
  constructor(exit, message, next, extra = {}) {
    super(message);
    this.name = 'SkillError';
    this.exit = exit;
    this.code = CODE_BY_EXIT[exit] ?? 'INTERNAL';
    this.next = next;
    this.extra = extra;
  }
}
