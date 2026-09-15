// Layer 5 lite: if runs/ is its own git repo, commit and push each run. Never throws.
import { existsSync } from 'node:fs';
import { join, relative } from 'node:path';
import { spawnSync } from 'node:child_process';
import { DIRS } from './paths.mjs';

function git(args, timeoutMs = 60000) {
  const r = spawnSync('git', ['-C', DIRS.runs, ...args], { encoding: 'utf8', timeout: timeoutMs, windowsHide: true });
  return { status: r.status ?? 1, out: ((r.stdout ?? '') + (r.stderr ?? '')).trim() };
}

export function runsRepoStatus() {
  if (!existsSync(join(DIRS.runs, '.git'))) return { repo: false, remote: false };
  const r = git(['remote']);
  return { repo: true, remote: r.status === 0 && r.out.length > 0, remotes: r.out.split(/\r?\n/).filter(Boolean) };
}

/** Commits the run dir and pushes if a remote exists. Returns { pushed, committed, reason, output }. */
export function pushRun(runDir, runId) {
  const st = runsRepoStatus();
  if (!st.repo) return { pushed: false, committed: false, reason: 'runs/ is not a git repo' };
  const rel = relative(DIRS.runs, runDir).replace(/\\/g, '/');
  let r = git(['add', '-A', '--', rel]);
  if (r.status !== 0) return { pushed: false, committed: false, reason: 'git add failed', output: r.out.slice(0, 300) };
  r = git(['commit', '-q', '-m', `run ${runId}`, '--', rel]);
  const committed = r.status === 0;
  if (!committed && !/nothing to commit/i.test(r.out)) return { pushed: false, committed: false, reason: 'git commit failed', output: r.out.slice(0, 300) };
  if (!st.remote) return { pushed: false, committed, reason: 'no remote configured' };
  r = git(['push', '-q'], 120000);
  return { pushed: r.status === 0, committed, reason: r.status === 0 ? 'pushed' : 'git push failed', output: r.out.slice(0, 300) };
}
