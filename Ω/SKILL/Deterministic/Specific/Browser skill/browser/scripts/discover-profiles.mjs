#!/usr/bin/env node
// discover-profiles.mjs — list the real Chrome/Edge profiles (directory + display name). Read-only.
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { parseArgs } from './lib/args.mjs';
import { EXIT, SkillError } from './lib/exit-codes.mjs';
import { ok, main, helpLine } from './lib/out.mjs';
import { DIRS, CANONICAL, ensureDirs, fwd } from './lib/paths.mjs';
import { listProfiles, localStatePath } from './lib/chrome-local-state.mjs';

const USAGE = `Usage: node ${CANONICAL}/scripts/discover-profiles.mjs [--browser chrome|edge] [--with-account] [--out <file>]`;

async function run() {
  const argv = process.argv.slice(2);
  if (argv[0] === '--help' || argv[0] === 'help') return helpLine('discover-profiles', ['(no verbs) [--browser chrome|edge] [--with-account] [--out <file>]']);
  const { flags } = parseArgs(argv, { flags: { browser: { type: 'string', values: ['chrome', 'edge'], default: 'chrome' }, 'with-account': { type: 'bool' }, out: { type: 'string' }, help: { type: 'bool' } } }, USAGE);
  if (flags.help) return helpLine('discover-profiles', ['(no verbs) [--browser chrome|edge] [--with-account] [--out <file>]']);
  ensureDirs();
  let profiles;
  try {
    profiles = listProfiles(flags.browser, { withAccount: !!flags['with-account'] });
  } catch (e) {
    if (e.code === 'ENOENT') throw new SkillError(EXIT.NOT_FOUND, e.message, `Is ${flags.browser} installed for this user? Expected ${fwd(localStatePath(flags.browser))}`);
    throw e;
  }
  const outPath = flags.out ? flags.out : join(DIRS.state, `discovered-profiles-${flags.browser}.json`);
  writeFileSync(outPath, JSON.stringify({ browser: flags.browser, discovered_at: new Date().toISOString(), profiles }, null, 2));
  const fields = { browser: flags.browser, count: profiles.length, profiles, profiles_path: fwd(outPath) };
  return ok('discover-profiles', fields,
    `Register one: node ${CANONICAL}/scripts/profile.mjs register --id <id> --name "<display name>" --from-chrome "<directory>"`);
}

main('discover-profiles', run);
