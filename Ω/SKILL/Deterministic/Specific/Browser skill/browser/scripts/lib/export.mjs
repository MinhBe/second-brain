// Builds report.md / report.json for a run, including SPEC-1's 14 "Definition of Success" answers.
import { existsSync, readFileSync } from 'node:fs';
import { verifyChain, readTimeline } from './timeline.mjs';
import { fwd } from './paths.mjs';

const QUESTIONS = [
  ['Profile nào được sử dụng?', 'Which profile was used?'],
  ['Profile đó có trạng thái provider như thế nào?', 'What was the provider state of that profile (before → after)?'],
  ['Browser đã mở URL nào?', 'Which URLs did the browser open?'],
  ['Skill đã click/fill/navigation gì?', 'Which Tier-1 actions did the skill take?'],
  ['Prompt nào đã được gửi?', 'Which prompt was sent?'],
  ['Model có bắt đầu generation không?', 'Did generation start?'],
  ['Model trả lời gì?', 'What did the model answer?'],
  ['Có toast/banner/warning/error nào không?', 'Were there toasts, banners, warnings or errors?'],
  ['Nếu usage-limit xuất hiện thì raw text là gì?', 'If a usage limit appeared, what was the raw text?'],
  ['Có reset time hay không?', 'Was a reset time parsed?'],
  ['Có artifact/file nào được tạo không?', 'Were artifacts or files created?'],
  ['Artifact chứa nội dung gì?', 'What did the artifacts contain?'],
  ['Screenshot và evidence nằm ở đâu?', 'Where are the screenshots and evidence?'],
  ['Run kết thúc ở terminal state nào?', 'In which terminal state did the run end?'],
];

export function buildReport(store) {
  const run = store.readRun() ?? {};
  const chain = existsSync(store.paths.timeline) ? verifyChain(store.paths.timeline) : { ok: false, reason: 'no timeline' };
  const events = existsSync(store.paths.timeline) ? readTimeline(store.paths.timeline) : [];
  const notifications = existsSync(store.paths.notifications) ? JSON.parse(readFileSync(store.paths.notifications, 'utf8')) : [];
  const response = existsSync(store.paths.response) ? readFileSync(store.paths.response, 'utf8') : null;
  const fw = store.firewallSummary();
  const urls = events.filter((e) => ['PAGE_OPENED', 'NAVIGATION'].includes(e.event)).map((e) => e.data?.url).filter(Boolean);
  const tier1 = events.filter((e) => e.tier === 1).map((e) => `${e.ts} ${e.event}${e.data?.via ? ' via ' + e.data.via : ''}${e.data?.chars ? ' (' + e.data.chars + ' chars)' : ''}`);
  const usage = notifications.filter((n) => n.normalized_type === 'usage_exhausted' || /usage|limit/i.test(n.raw_text));
  const reset = notifications.find((n) => n.parsed?.reset_time);
  const artifacts = events.filter((e) => e.event === 'ARTIFACT_DISCOVERED');
  const shots = (run.screenshots ?? []).filter((s) => s.file).map((s) => `${s.file} (sha256 ${String(s.sha256).slice(0, 12)}…)`);
  const answers = [
    `${run.profile_id ?? '?'} (${run.user_data_dir ?? ''})`,
    `${run.profile_provider_state_before?.state ?? 'UNKNOWN'} → ${run.profile_provider_state_after?.state ?? 'UNKNOWN'}${run.profile_provider_state_after?.cooldown_until ? ', cooldown until ' + run.profile_provider_state_after.cooldown_until : ''}`,
    urls.length ? urls.join(', ') : 'none',
    tier1.length ? tier1.join('; ') : 'none',
    run.prompt_text ? `"${String(run.prompt_text).slice(0, 300)}" (sha256 ${String(run.prompt_sha256 ?? '').slice(0, 12)}…)` : 'none',
    events.some((e) => e.event === 'GENERATION_STARTED') ? 'yes' : 'no',
    response !== null ? `${response.length} chars in response.md${response.length ? ': ' + JSON.stringify(response.slice(0, 200)) : ''}` : 'no response captured',
    notifications.length ? notifications.map((n) => `[${n.source}/${n.normalized_type}] ${n.raw_text.slice(0, 160)}`).join(' | ') : 'none observed',
    usage.length ? usage.map((n) => JSON.stringify(n.raw_text)).join(' | ') : 'no usage limit',
    reset ? `${reset.parsed.reset_time} local → ${reset.parsed.cooldown_until}` : 'none',
    artifacts.length ? `${artifacts[0].data?.count ?? artifacts.length} candidate(s) detected, not opened (Phase 3)` : 'none detected',
    'not read in this version (Phase 3)',
    `${shots.length} screenshot(s): ${shots.join('; ')}; firewall.jsonl (allowed ${fw.allowed}, blocked ${fw.blocked}); timeline chain ${chain.ok ? 'intact' : 'BROKEN at ' + chain.broken_at}`,
    `${run.status ?? '?'} (terminal_state ${run.terminal_state ?? '?'}, exit ${run.exit ?? '?'})`,
  ];
  const json = { run_id: run.run_id, generated_at: new Date().toISOString(), chain, firewall: fw, answers: QUESTIONS.map((q, i) => ({ n: i + 1, question_vi: q[0], question_en: q[1], answer: answers[i] })), events: events.length, run };
  const md = [
    `# Run ${run.run_id ?? ''}`,
    '',
    `- provider: **${run.provider}** · profile: **${run.profile_id}** · status: **${run.status}** · exit ${run.exit}`,
    `- started ${run.started_at} · finished ${run.finished_at ?? '—'}`,
    `- timeline: ${events.length} events, chain ${chain.ok ? 'OK' : 'BROKEN (' + chain.reason + ' at line ' + chain.broken_at + ')'} · policy ${String(run.policy_sha256 ?? '').slice(0, 12)}…`,
    `- firewall: ${fw.allowed} allowed, ${fw.blocked} blocked${fw.blocked_hosts.length ? ' (' + fw.blocked_hosts.join(', ') + ')' : ''}, ${fw.handler_errors} handler errors`,
    '',
    '## 14 answers',
    '',
    '| # | Question | Answer |',
    '|---|---|---|',
    ...QUESTIONS.map((q, i) => `| ${i + 1} | ${q[1]} | ${String(answers[i]).replace(/\|/g, '\\|').replace(/\n/g, ' ')} |`),
    '',
    '## Timeline',
    '',
    ...events.map((e) => `- \`${e.ts}\` **${e.event}**${e.tier !== null ? ` (tier ${e.tier})` : ''} ${JSON.stringify(e.data).slice(0, 160)}`),
    '',
    '## Files',
    '',
    `- run.json, timeline.jsonl, firewall.jsonl, response.md, notifications.json, browser-state.json under \`${fwd(store.dir)}\``,
    '',
  ].join('\n');
  return { md, json };
}
