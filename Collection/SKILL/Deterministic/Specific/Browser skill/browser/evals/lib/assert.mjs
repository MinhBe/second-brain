// Tiny assertion helpers + STEP markers for evals (stderr lines, ui-test style).
export class EvalFailure extends Error {
  constructor(id, expected, actual, artifact = '') {
    super(`${id}: expected ${expected}, got ${actual}`);
    this.id = id; this.expected = expected; this.actual = actual; this.artifact = artifact;
  }
}

export function stepPass(id, evidence) {
  process.stderr.write(`STEP_PASS|${id}|${String(evidence).slice(0, 200)}\n`);
}

export function stepFail(id, expected, actual, artifact = '') {
  process.stderr.write(`STEP_FAIL|${id}|${expected} -> ${actual}|${artifact}\n`);
}

export function assertEq(id, actual, expected, artifact = '') {
  if (actual !== expected) throw new EvalFailure(id, JSON.stringify(expected), JSON.stringify(actual), artifact);
  stepPass(id, `== ${JSON.stringify(expected)}`);
}

export function assertTrue(id, cond, detail = '', artifact = '') {
  if (!cond) throw new EvalFailure(id, 'true', `false ${detail}`, artifact);
  stepPass(id, detail || 'true');
}

export function assertMatch(id, text, re, artifact = '') {
  if (!re.test(String(text))) throw new EvalFailure(id, String(re), JSON.stringify(String(text).slice(0, 120)), artifact);
  stepPass(id, `matches ${re}`);
}

export async function assertThrows(id, fn, re) {
  try { await fn(); } catch (e) {
    if (re && !re.test(String(e?.message ?? e))) throw new EvalFailure(id, `throw ${re}`, String(e?.message ?? e));
    stepPass(id, `threw ${String(e?.message ?? e).slice(0, 80)}`);
    return e;
  }
  throw new EvalFailure(id, 'throw', 'no throw');
}
