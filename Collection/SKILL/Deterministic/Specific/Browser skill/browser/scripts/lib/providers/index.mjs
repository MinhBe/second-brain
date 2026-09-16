import * as claude from './claude.mjs';
import * as chatgpt from './chatgpt.mjs';
import * as meta from './meta.mjs';
import { EXIT, SkillError } from '../exit-codes.mjs';

const REGISTRY = Object.freeze({ claude, chatgpt, meta });
export const PROVIDER_IDS = Object.freeze(Object.keys(REGISTRY));

export function getProvider(id) {
  const p = REGISTRY[id];
  if (!p) throw new SkillError(EXIT.USAGE, `Unknown provider ${id}`, `Use one of: ${PROVIDER_IDS.join(', ')}`);
  return p;
}

export function requireImplemented(id) {
  const p = getProvider(id);
  if (!p.implemented) throw new SkillError(EXIT.USAGE, `Provider ${id} is not implemented yet (${p.phase})`, 'Use provider claude in this version');
  return p;
}
