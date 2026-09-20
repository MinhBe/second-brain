# Mentor Critique — Anh Tuấn Anh (voice-018)

## Core Points
1. **Understand the Baseline First** – Document current WAF ruleset behavior, latency, and blocking rate before touching AI.
2. **Reproduce the Critique** – Each question from the mentor becomes a measurable spike (throughput, latency, obfuscation handling).
3. **Lab Environment** – All experiments must run in a strictly isolated lab (ModSecurity + OWASP CRS) to avoid side effects.
4. **Feasibility Question** – Can AI process every request at scale (millions/day) without violating latency SLA?
5. **SQL Structure Knowledge** – Must understand query structure and WAF blocking mechanisms before optimizing.

## Key Quotes
- "Hiểu luồng hiện tại và chi phí trước khi chèn AI" (Understand current flow and cost before inserting AI).
- "Về làm lab ngay" (Go do lab work immediately).
- Questioned whether AI can handle millions of requests and whether obfuscation actually helps or just breaks syntax.

## Linked Files
- Transcripts: `voice-018_TRANSCRIPT.md`, `voice-018_KNOWLEDGE.md`
- DOI_CHIEU.md: summary of mentor feedback
