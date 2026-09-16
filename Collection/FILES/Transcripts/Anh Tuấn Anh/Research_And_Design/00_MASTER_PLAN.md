# Master Plan & Implementation Roadmap — SQL-Aware SeqGAN for SQLi

## Goal
Design an **algorithm** (not a pipeline runner) that a SeqGAN-like model can *truly learn* SQL Injection structure — producing structurally valid, functionally equivalent, diverse, and WAF-evasive payloads. This is driven by senior feedback (Anh Tuấn Anh) and validated against 18 OCR'd research papers.

## Reading Order
1. `01_Transcript_Analysis.md` — What the seniors/mentors contest and why.
2. `02_OCR_Papers_Technical_Analysis.md` — How the literature (AdvSQLi, WAF-A-MoLE, ModSec-AdvLearn) solved these limits.
3. `03_SQL_Aware_SeqGAN_Algorithm.md` — The actual algorithm spec with runnable Python pseudocode.
4. This file — sequencing, dependencies, acceptance criteria.

---

## Implementation Phases (Ordered by Dependency)

### Phase 1 — Foundation: SQL-aware tokenizer + AST + module locking
- Build `sql_aware_tokenize()` (sqlparse-based semantic units).
- Build `ASTNode` / `SQLiPayload` dataclasses with locked boundaries.
- **Deliverable:** A module that turns any SQLi payload string into a locked, mutable AST.

### Phase 2 — Weighted CFG mutation engine
- Implement `CFG_RULES`, `WeightedCFGEngine` with decay D=0.5.
- Mutation rules: Tautology, DML, Integer/Hex, Whitespace, Comment.
- **Deliverable:** Functions to produce valid mutated mutations of an AST core.

### Phase 3 — MCTS search (UCB1) over AST mutations
- Replace REINFORCE + MC rollouts with tree search.
- **Deliverable:** `MCTSSearch` that returns an optimized payload given a start AST.

### Phase 4 — Sandbox DBMS execution oracle (honest reward)
- Set up Docker MySQL / PostgreSQL with a vulnerable backend (PHP/Python).
- Implement `SandboxDB.execute(sql)` → result + syntax-error flag.
- **Deliverable:** The `R_Exec` oracle that kills any syntax-invalid payload.

### Phase 5 — Discriminator + hybrid reward loop
- Lightweight ℓ1/ℓ∞-regularized linear model on n-gram TF-IDF.
- Implement `HybridReward` = w_waf·R_WAF + w_exec·R_Exec + w_div·R_Div.
- **Deliverable:** Full training loop (MLE pre-train → MCTS adversarial → retrain D).

### Phase 6 — Family-stratified training + 160-token context
- Train 4 separate generators (Boolean/Error/Union/Time) on shared backbone.
- Set max_seq_len = 160.
- **Deliverable:** 4 trained generators + evaluation harness.

### Phase 7 — Honest evaluation + WAF campaign
- Split by family (held-out families for generalization).
- Report: Structural Validity %, Functional Equivalence %, WAF Bypass %, Diversity, Family Generalization.
- **Deliverable:** A report + the algorithm demonstrating senior's claims are addressed.

---

## Key Design Decisions (with rationale)
1. **Grammar-guided MCTS over REINFORCE** — eliminates high-variance rollouts that produce broken SQL.
2. **Boundary locking** — prevents syntactically broken boundary escapes.
3. **Sandbox DB oracle** — ensures semantic validity, not just WAF evasion (HTTP 200 ≠ exploitation).
4. **Hybrid reward** — 70/30 discriminator + structural optimizer prevents reward hacking / mode collapse.
5. **Family-stratified training** — separate generators per attack family to respect grammar differences.
6. **160-token context** — captures long multi-clause SQLi syntax (Union, Time-based).

---

## Acceptance Criteria (final)
- [ ] Tokenizer parses every payload in our test set without losing boundaries.
- [ ] CFG mutations always converge (decay D=0.5 guarantees termination).
- [ ] MCTS returns payloads with Structural Validity Rate ≥ 95%.
- [ ] Sandbox oracle correctly rejects syntax-invalid payloads.
- [ ] Family-stratified training produces payloads diverse vs. training set (AST distance ≥ 0.6).
- [ ] Honest metric table shows WAF bypass AND functional equivalence, not just HTTP 200.