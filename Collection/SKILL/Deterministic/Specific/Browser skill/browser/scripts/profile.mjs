#!/usr/bin/env node
// profile.mjs — logical profiles for the AI Web Observer.
//   register | list | enable | disable | remove | login
// A logical profile maps to an AUTOMATION user-data-dir under profiles/<id>/user-data.
// `login` opens a headed browser with the firewall on and WAITS for the human to sign in; it never types.
import { existsSync, mkdirSync, cpSync, rmSync, writeFileSync, appendFileSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { parseArgs, takeVerb } from './lib/args.mjs';
import { EXIT, SkillError } from './lib/exit-codes.mjs';
import { ok, main, helpLine, log, emit } from './lib/out.mjs';
import { DIRS, CANONICAL, ensureDirs, tsForFile, fwd } from './lib/paths.mjs';
import { ID_RE, PROVIDERS, loadRegistry, saveRegistry, getProfile, requireProfile, setProviderState, userDataDirFor, acquireLock, describeProfile, providerState } from './lib/registry.mjs';
import { userDataDir as chromeUserDataDir, listProfiles } from './lib/chrome-local-state.mjs';
import { OBSERVER_ALLOWLIST, LOGIN_EXTRA_HOSTS, BLOCKING_STATES } from './lib/policy.mjs';
import { launchObserverBrowser } from './lib/browser.mjs';
import { capture } from './lib/observe.mjs';
import { classify } from './lib/classify.mjs';
import { requireImplemented, getProvider } from './lib/providers/index.mjs';

const S = `node ${CANONICAL}/scripts/profile.mjs`;
const VERBS = ['register', 'list', 'enable', 'disable', 'remove', 'login'];
const usage = (v) => `Usage: ${S} ${v} ... (see references/profiles.md)`;
const idFlag = { id: { type: 'string', required: true, pattern: ID_RE, patternHint: 'lowercase letters, digits, dashes, 2-32 chars' } };

function chromeRunning() {
  const r = spawnSync('tasklist', ['/FI', 'IMAGENAME eq chrome.exe', '/NH'], { encoding: 'utf8', windowsHide: true });
  return /chrome\.exe/i.test(r.stdout ?? '');
}

function unionAllowlist() {
  const s = new Set([...OBSERVER_ALLOWLIST, ...LOGIN_EXTRA_HOSTS]);
  return { has: (h) => s.has(h), size: s.size, [Symbol.iterator]: () => s[Symbol.iterator]() };
}

async function run() {
  ensureDirs();
  const { verb, rest } = takeVerb(process.argv.slice(2));
  if (!verb || verb === '--help' || verb === 'help') return helpLine('profile', VERBS, { canonical: `${S} <verb> --id <id> ...` });
  if (!VERBS.includes(verb)) throw new SkillError(EXIT.USAGE, `Unknown verb ${verb}`, `Verbs: ${VERBS.join(', ')}`);
  const reg = loadRegistry();

  switch (verb) {
    case 'register': {
      const { flags } = parseArgs(rest, { flags: { ...idFlag, name: { type: 'string', required: true }, 'from-chrome': { type: 'string' }, copy: { type: 'bool' } } }, usage('register'));
      if (flags.id === 'general') throw new SkillError(EXIT.USAGE, 'The id "general" is reserved for bw.mjs sessions', 'Pick another id, e.g. p001');
      if (getProfile(reg, flags.id)) throw new SkillError(EXIT.USAGE, `Profile ${flags.id} already exists`, `Run: ${S} list`);
      if (flags.copy && !flags['from-chrome']) throw new SkillError(EXIT.USAGE, '--copy needs --from-chrome "<Profile N>"', usage('register'));
      let chromeDir = null;
      if (flags['from-chrome']) {
        const known = listProfiles('chrome').find((p) => p.directory === flags['from-chrome']);
        if (!known) throw new SkillError(EXIT.NOT_FOUND, `Chrome profile directory ${flags['from-chrome']} not found in Local State`, `Run: node ${CANONICAL}/scripts/discover-profiles.mjs`);
        chromeDir = known.directory;
      }
      const dir = userDataDirFor(flags.id);
      mkdirSync(dir, { recursive: true });
      let copied = false;
      if (flags.copy) {
        if (chromeRunning()) throw new SkillError(EXIT.PRECONDITION, 'Chrome is running; close it completely before --copy', 'Ask the user to close Chrome, then run register --copy again');
        const src = chromeUserDataDir('chrome');
        const skip = /\\(Cache|Code Cache|GPUCache|DawnCache|GrShaderCache|ShaderCache|Service Worker\\CacheStorage|Crashpad)(\\|$)/i;
        cpSync(join(src, 'Local State'), join(dir, 'Local State'));
        cpSync(join(src, chromeDir), join(dir, chromeDir), { recursive: true, filter: (p) => !skip.test(p) });
        copied = true;
      }
      const now = new Date().toISOString();
      reg.profiles.push({ id: flags.id, display_name: flags.name, chrome_profile_directory: chromeDir, automation_user_data_dir: fwd(dir), copied_from: copied ? fwd(join(chromeUserDataDir('chrome'), chromeDir)) : null, enabled: true, created_at: now, updated_at: now, providers: {} });
      saveRegistry(reg);
      return ok('profile.register', { id: flags.id, name: flags.name, chrome_dir: chromeDir, user_data_dir: fwd(dir), copied },
        `Sign in once (human does the typing): ${S} login --id ${flags.id} --provider claude`);
    }
    case 'list': {
      parseArgs(rest, { flags: {} }, usage('list'));
      const profiles = reg.profiles.map(describeProfile);
      return ok('profile.list', { count: profiles.length, profiles },
        profiles.length ? `Ask: node ${CANONICAL}/scripts/aiweb.mjs ask claude --profile ${profiles[0].id} --prompt-file <file>` : `Register: node ${CANONICAL}/scripts/discover-profiles.mjs then ${S} register --id p001 --name "<name>"`);
    }
    case 'enable':
    case 'disable': {
      const { flags } = parseArgs(rest, { flags: idFlag }, usage(verb));
      const p = requireProfile(reg, flags.id);
      p.enabled = verb === 'enable'; p.updated_at = new Date().toISOString();
      saveRegistry(reg);
      return ok(`profile.${verb}`, { id: p.id, enabled: p.enabled }, `${S} list`);
    }
    case 'remove': {
      const { flags } = parseArgs(rest, { flags: { ...idFlag, 'delete-data': { type: 'bool' } } }, usage('remove'));
      const p = requireProfile(reg, flags.id);
      reg.profiles = reg.profiles.filter((x) => x.id !== p.id);
      saveRegistry(reg);
      let deleted = false;
      if (flags['delete-data']) { rmSync(join(DIRS.profiles, p.id), { recursive: true, force: true }); deleted = true; }
      return ok('profile.remove', { id: p.id, registry_removed: true, data_deleted: deleted }, deleted ? `${S} list` : `Data kept at ${p.automation_user_data_dir}; re-run with --delete-data to delete it`);
    }
    case 'login': {
      const { flags } = parseArgs(rest, { flags: { ...idFlag, provider: { type: 'string', required: true, values: PROVIDERS }, 'timeout-sec': { type: 'int', default: 600 }, 'poll-sec': { type: 'int', default: 3 } } }, usage('login'));
      const p = requireProfile(reg, flags.id);
      if (!p.enabled) throw new SkillError(EXIT.POLICY, `Profile ${p.id} is disabled`, `${S} enable --id ${p.id}`);
      const prov = requireImplemented(flags.provider);
      const { release } = acquireLock(p.id, `login_${tsForFile()}`, (flags['timeout-sec'] + 120) * 1000);
      const auditPath = join(DIRS.logs, `login-${p.id}-${prov.id}-${tsForFile()}.jsonl`);
      writeFileSync(auditPath, '');
      const blockedHosts = new Set();
      const audit = (e) => { appendFileSync(auditPath, JSON.stringify(e) + '\n'); if (e.verdict === 'blocked' && e.host) blockedHosts.add(e.host); };
      const events = [];
      let browser = null;
      let last = { state: 'UNKNOWN', evidence: null };
      const started = Date.now();
      try {
        browser = await launchObserverBrowser({ userDataDir: p.automation_user_data_dir, headless: false, allowlist: unionAllowlist(), audit, onEvent: (n, d) => events.push({ n, d }), profileDirectory: p.copied_from ? p.chrome_profile_directory : null });
        await browser.page.goto(prov.entryUrl, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch((e) => log(`goto: ${e.message}`));
        log(`Sign in to ${prov.id} in the Chrome window (profile ${p.id}). Waiting up to ${flags['timeout-sec']} s ...`);
        while ((Date.now() - started) / 1000 < flags['timeout-sec']) {
          await browser.page.waitForTimeout(flags['poll-sec'] * 1000);
          const o = await capture(browser.page);
          last = classify(o, prov.id);
          log(`[${Math.floor((Date.now() - started) / 1000)}s] ${last.state} ${last.evidence?.text ? '— ' + String(last.evidence.text).slice(0, 80) : ''}`);
          if (last.state === 'READY') break;
        }
      } finally {
        if (browser) await browser.close();
        release();
      }
      const elapsed = Math.round((Date.now() - started) / 1000);
      const now = new Date().toISOString();
      if (last.state === 'READY') {
        setProviderState(reg, p.id, prov.id, { state: 'READY', evidence: last.evidence, last_checked_at: now, cooldown_until: null });
        return ok('profile.login', { id: p.id, provider: prov.id, state: 'READY', evidence: last.evidence, elapsed_sec: elapsed, blocked_hosts: [...blockedHosts].slice(0, 30), audit_path: fwd(auditPath) },
          `Ask something: node ${CANONICAL}/scripts/aiweb.mjs ask ${prov.id} --profile ${p.id} --prompt-file <file>`);
      }
      setProviderState(reg, p.id, prov.id, { state: last.state, evidence: last.evidence, last_checked_at: now });
      const human = ['CAPTCHA', 'VERIFICATION_REQUIRED'].includes(last.state);
      return emit('profile.login', human ? EXIT.HUMAN : EXIT.TIMEOUT, { id: p.id, provider: prov.id, state: last.state, evidence: last.evidence, elapsed_sec: elapsed, blocked_hosts: [...blockedHosts].slice(0, 30), audit_path: fwd(auditPath), error: human ? `Sign-in stopped at ${last.state}` : `Not READY after ${elapsed} s (last state ${last.state})` },
        human ? 'The human must complete the challenge themselves; then run login again' : `Check blocked_hosts in audit_path (a sign-in host may need to be added to LOGIN_EXTRA_HOSTS — a code change), then run login again`);
    }
    default:
      throw new SkillError(EXIT.USAGE, `Unknown verb ${verb}`, `Verbs: ${VERBS.join(', ')}`);
  }
}

main('profile', async () => {
  const { verb } = takeVerb(process.argv.slice(2));
  try { await run(); } catch (e) { if (e instanceof SkillError && VERBS.includes(verb)) e.verb = `profile.${verb}`; throw e; }
});
