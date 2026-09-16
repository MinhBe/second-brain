import { EXIT, SkillError } from './exit-codes.mjs';

/**
 * Strict argv parser. No dependencies.
 * spec = {
 *   positional: ['name', ...],            // required positionals in order
 *   optional:   ['name', ...],            // optional positionals after the required ones
 *   flags: { name: { type: 'string'|'bool'|'int', required?, values?, default?, alias?, pattern? } }
 * }
 * Accepts --flag value, --flag=value, -s value, -s=value. Unknown flags -> USAGE.
 */
export function parseArgs(argv, spec, usageHint) {
  const flags = {};
  const pos = [];
  const known = new Map();
  for (const [name, def] of Object.entries(spec.flags ?? {})) {
    known.set(name, { name, ...def });
    if (def.alias) known.set(def.alias, { name, ...def });
  }
  const looksLikeFlag = (s) => typeof s === 'string' && s.startsWith('-') && s.length > 1 && !/^-\d/.test(s);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--') { pos.push(...argv.slice(i + 1)); break; }
    if (looksLikeFlag(a)) {
      let key = a.replace(/^--?/, '');
      let val;
      const eq = key.indexOf('=');
      if (eq >= 0) { val = key.slice(eq + 1); key = key.slice(0, eq); }
      const def = known.get(key);
      if (!def) throw new SkillError(EXIT.USAGE, `Unknown flag: ${a}`, usageHint);
      if (def.type === 'bool') {
        if (val !== undefined) throw new SkillError(EXIT.USAGE, `Flag --${def.name} takes no value`, usageHint);
        flags[def.name] = true;
        continue;
      }
      if (val === undefined) {
        val = argv[i + 1];
        if (val === undefined || looksLikeFlag(val)) {
          throw new SkillError(EXIT.USAGE, `Flag --${def.name} needs a value`, usageHint);
        }
        i++;
      }
      if (def.type === 'int') {
        if (!/^\d+$/.test(val)) throw new SkillError(EXIT.USAGE, `Flag --${def.name} must be an integer`, usageHint);
        val = Number(val);
      }
      if (def.values && !def.values.includes(val)) {
        throw new SkillError(EXIT.USAGE, `Flag --${def.name} must be one of: ${def.values.join('|')}`, usageHint);
      }
      if (def.pattern && !def.pattern.test(String(val))) {
        throw new SkillError(EXIT.USAGE, `Flag --${def.name} has an invalid value (${def.patternHint ?? def.pattern})`, usageHint);
      }
      flags[def.name] = val;
    } else {
      pos.push(a);
    }
  }
  for (const [name, def] of Object.entries(spec.flags ?? {})) {
    if (flags[name] === undefined && def.default !== undefined) flags[name] = def.default;
    if (flags[name] === undefined && def.required) {
      throw new SkillError(EXIT.USAGE, `Missing required flag --${name}`, usageHint);
    }
  }
  const required = spec.positional ?? [];
  const optional = spec.optional ?? [];
  if (pos.length < required.length) {
    throw new SkillError(EXIT.USAGE, `Missing argument <${required[pos.length]}>`, usageHint);
  }
  if (pos.length > required.length + optional.length) {
    throw new SkillError(EXIT.USAGE, `Unexpected extra argument: ${pos[required.length + optional.length]}`, usageHint);
  }
  const named = {};
  required.forEach((n, i) => { named[n] = pos[i]; });
  optional.forEach((n, i) => { if (pos[required.length + i] !== undefined) named[n] = pos[required.length + i]; });
  return { pos: named, flags };
}

/** Splits `verb` off argv[0]; returns { verb, rest }. */
export function takeVerb(argv) {
  const [verb, ...rest] = argv;
  return { verb: verb ?? '', rest };
}
