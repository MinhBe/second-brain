# Pedagogical Patterns in AI Agentic Teaching

## 1. Calculating Spacing Without a Database

### File-Based State Persistence

When no external database is available, an AI agent can persist spaced-repetition state entirely in the local file system. The canonical pattern uses **JSON files with structured frontmatter** co-located with learning assets. Each lesson/item file carries:

| Field | Purpose | Typical Format |
|---|---|---|
| `createdAt` | ISO 8601 timestamp of when the lesson was first introduced | `2026-09-01T10:30:00Z` |
| `lastReviewed` | ISO 8601 timestamp of the most recent review | `2026-09-10T14:15:00Z` |
| `nextReviewDate` | ISO 8601 timestamp when the item is due for review | `2026-09-17T09:00:00Z` |
| `easinessFactor` / `AF` | Item-specific ease modifier (SM-2: starts at 2.5, FSRS: learned parameter) | float, min 1.3 (SM-2) or inferred (FSRS) |
| `interval` | Current gap in days between reviews | integer (days) |
| `repetitionCount` | Number of successful reviews logged | integer |
| `reviewHistory` | Array of `{date, rating}` entries for algorithm input | `[{"date":"2026-09-10","rating":"good"}]` |

### Spacing Calculation Workflow

1. **Discovery**: Agent scans a vault/directory for lesson files (e.g., `**/*.md`, `**/*.json`).
2. **Filtering**: Select files where `nextReviewDate <= currentTimestamp` (due for review) or where `lastReviewed` exists and elapsed time triggers a re-evaluation.
3. **Elapsed-time computation**: For each candidate file, compute `elapsedDays = floor((currentTimestamp - lastReviewed) / 86400)`.
4. **Algorithm application**:
   - **SM-2**: `newInterval = max(1, round(interval * AF))`; if `elapsedDays >= newInterval`, the item is due; after rating (1–5), update `AF` by `+1/3` if rating ≥ 4, or `AF = AF - 0.2` if rating = 2; repeat interval = `newInterval`.
   - **FSRS** (more recent, gradient-based): Given `MemoryState { stability, difficulty }` and elapsed days, compute `nextState = ForgettingCurve(elapsedDays, stability)`; derive `newStability` and `newDifficulty` from the review rating; compute `newInterval` by solving `R(newInterval, newStability) = targetRetention` (typically 0.9).
5. **Persist**: Write back the updated `nextReviewDate`, `interval`, `repetitionCount`, and append to `reviewHistory`.

### Pure-Timestamp Approach (no frontmatter)

If the agent cannot rely on file annotations, it can infer spacing from **file modification timestamps** (`mtime`) and **log files**:

- **First-review marker**: When a lesson file is created, the agent records `creationTime = file.mtime`.
- **Review log**: Each review appends a line to a JSONL log: `{"file":"lessons/foo.md","reviewedAt":"2026-09-10T14:15:00Z","rating":"good"}`.
- **Spacing check**: Agent reads the latest log entry for the file, computes `elapsedDays = floor((now - reviewedAt) / 86400)`, and applies a simplified interval rule (e.g., "1st review → 1 day, 2nd → 2 days, 3rd → 4 days, 4th+ → double").

> **Key insight**: The filesystem becomes the state store. As long as timestamps and minimal metadata are preserved across sessions, the agent can reconstruct the full spaced-repetition schedule without a separate DB.

---

## 2. Desirable Difficulty Patterns in Agentic Teaching

### The Four Canonical Difficulties

| Difficulty | Mechanism | AI Risk (over-scaffolding) | Agentic Pattern |
|---|---|---|---|
| **Spacing** | Distributing practice across time > massed practice | Scheduling every review too close together; instant re-generation of "fresh" content | Space lessons across days using `nextReviewDate`; do not re-present a just-reviewed item within 24h |
| **Interleaving** | Mixing problem types or topics > blocking (one topic at a time) | Presenting all examples of one type before switching; AI tutor giving a single-mindset focus | Randomly permute lesson topics within a session; alternate between related but distinct subskills |
| **Generation** | Producing answers before receiving them > recognition/recall | AI immediately generating the answer; students recognizing rather than retrieving | Prompt: "Attempt to answer before seeing the solution"; hide solutions behind `[[reveal]]` or require a free-response entry before disclosure |
| **Retrieval Practice** | Testing yourself > restudying material | AI providing summaries or re-reading; eliminating the "struggle" | Present a question, wait for the agent/student to generate an answer, then compare/grade; do not auto-reveal |

### Calibration Principles (from Bjork & recent AI-ED research)

- **Difficulty must engage effortful retrieval from memory**, not external sources. If the AI can "just look it up," the difficulty is undesirable.
- **Difficulty must engage generative processing** — the learner must construct responses, not recognize them.
- **Difficulty must force discrimination between alternatives** — the learner must categorize, not just pattern-match.
- **Difficulty must introduce variation** that prevents overfitting to a single context.

> **Crucial**: The "performance–learning gap" means that what looks like good performance during practice (e.g., AI provides the answer, student nods) is not the same as durable learning. AI systems must **preserve productive struggle** rather than collapse to answer-giving.

### ZPD-Aligned Difficulty Calibration

The **Zone of Proximal Development** (Vygotsky) overlaps directly with desirable difficulty: the task should be just beyond the learner's current autonomous capability, requiring guided support.

A practical agentic pattern:

1. **Competence tracking**: Maintain a `competenceLevel` (0.0–1.0) per skill/concept, updated after each attempt:
   - `competence ← competence + η × (success - currentCompetence)` where `η` is a learning rate (e.g., 0.1).
   - On failure, increase support; on success, fade support.
2. **Support-level ladder** (4 levels, fading automatically):
   - **L1 – Direct Guidance**: Explicit steps, definitions, formulas.
   - **L2 – Heuristic Questioning**: Guiding questions focused on key concepts.
   - **L3 – Metacognitive Guidance**: Prompts on strategy selection and process evaluation.
   - **L4 – Motivational & Emotional Support**: Encouragement, task decomposition, frustration management.
3. **Dynamic decision rule** (prioritized):
   - If learner expresses negative emotion (`"too hard"`, `"confused"`) → L4
   - If `helpCount == 1` → L1
   - If query contains `"why"` or `"how to choose"` → L3
   - If current step is `calculation_execution` → L2
   - If `helpCount >= 2` → L3
   - Else → L2 (default)
4. **Competence decay**: Apply a periodic `decayFactor` (e.g., 0.95 per week) so competence slowly erodes without practice, naturally pushing the agent to re-introduce spaced review.

> **Result**: The agent dynamically presents tasks at the edge of the learner's current competence, with just-in-time scaffolding that fades as mastery grows — preserving the productive struggle that drives durable learning.

---

## 3. Implementation Summary

| Concept | File-System Technique | Key Algorithm / Pattern |
|---|---|---|
| **Spacing** | JSON frontmatter (`nextReviewDate`, `interval`, `easinessFactor`) or timestamp + JSONL log | SM-2 or FSRS; compute elapsed days from `lastReviewed`; schedule next review |
| **Retrieval Practice** | Hide solution behind user-generated answer; log attempt before reveal | Present question → wait for free-response → compare → reveal |
| **Interleaving** | Randomly permute topic order within a session; rotate lesson sets | `shuffle(topics)` per session; avoid blocking same-type items consecutively |
| **Generation** | Require free-response before showing model answer; use `[[reveal]]` toggles | Prompt: "Write your answer first"; only then display the solution |
| **Desirable Difficulty Calibration** | Track `competenceLevel` per skill; apply decay; map to support level | Competence update + decay + support-ladder decision engine; fade support on success, increase on failure |
| **ZPD Alignment** | competence ∈ [0,1]; task difficulty = f(competence); support level = g(competence, helpCount) | LKP/MKO framework: task unsolvable by LKP but solvable by MKO = ZPD; dynamic scaffolding levels 1–4 |

---

## 4. Practical File-System Workflow (End-to-End)

```
# 1. Agent discovers lessons in ~/lessons/
# 2. For each lesson file with frontmatter:
#    - Read: createdAt, lastReviewed, nextReviewDate, interval, easinessFactor, reviewHistory
#    - Compute: elapsedDays = floor((now - lastReviewed) / 86400)
#    - If elapsedDays >= interval: item is due
#    - Present question; learner answers (free-text or multiple choice)
#    - Log the attempt: append {"file":"lessons/foo.md","reviewedAt":"now","rating":"good"} to reviews.jsonl
#    - Apply SM-2/FSRS using: interval, easinessFactor, rating, elapsedDays
#    - Write back: new nextReviewDate, new interval, updated easinessFactor, appended reviewHistory
# 3. Session ends; all state persists in the filesystem
```

> **No database required**. The only invariants are: (a) timestamps are ISO 8601 and preserved across runs; (b) review logs are append-only JSONL (never overwritten); (c) lesson files carry the agreed frontmatter schema.

---

## References (selected)

- Bjork, R.A. & Bjork, E.L. (2011). *Making things hard on yourself but easier to learn: The theory of desirable difficulties*.
- Wang, Y. & Shan, Y. (2026). *The "Safety Gap" in AI-assisted learning*.
- Kim, J. et al. (2026). *AI design principles for preserving desirable difficulties*.
- AgentFrontier: ZPD-guided data synthesis (arXiv 2510.24695) — LKP/MKO framework for capability frontier calibration.
- Dynamic AI scaffolding based on ZPD (STEMM Press, 2022) — four-level prompt framework: Direct Guidance → Heuristic Questioning → Metacognitive Guidance → Motivational Support.
- FSRS algorithm (open-spaced-repetition) — stability/difficulty-based interval calculation with target retention.
- SM-2 algorithm — classic SRS with easiness factor and interval growth.