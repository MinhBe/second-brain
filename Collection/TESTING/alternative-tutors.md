# Non-Chatbot AI Tutoring Systems: Workspace/Filesystem Memory Comparison

## Overview
This document compares three non-chatbot AI tutoring systems that use a **workspace or filesystem as their primary memory mechanism** — Matt Pocock's `/teach` skill, OpenTutor, and DeepTutor — focusing on their state/data structures and architectural approaches.

---

## 1. Matt Pocock `/teach` Skill (Claude Code)

### Source
- Repository: `mattpocock/skills` (bundled skill: `teach`)
- Documentation: [skills.sh](https://topaiskills.com/skills/general/teach), [vibehackers.io](https://vibehackers.io/claude-code/skills/teach-mattpocock)

### Workspace Structure (State)
The skill treats the **current directory as a teaching workspace**. State persists as plain files:

| File/Directory | Format | Purpose |
|----------------|--------|---------|
| `MISSION.md` | Markdown | High-level learning goal; grounds all teaching |
| `RESOURCES.md` | Markdown | Curated, annotated sources (knowledge + wisdom/communities) |
| `NOTES.md` | Markdown | Scratchpad for user preferences, working notes |
| `lessons/*.html` | HTML | Primary teaching output — self-contained, numbered `0001-slug.html` |
| `reference/*.html` | HTML | Compressed cheat-sheets, syntax references, algorithms, glossaries |
| `learning-records/*.md` | Markdown | ADR-style records of what was demonstrably learned (`status: pending\|mastered`, `last_review:`) |
| `assets/*` | Various | Reusable components (shared stylesheet, quiz widgets, simulators) |
| `progress.json` | JSON | Tracks quiz scores, intervals for spaced repetition |

### State Characteristics
- **File-backed**: Every artifact is a readable file — no hidden vector DB
- **Lazy creation**: Files created only when needed (empty workspace stays empty)
- **Append-only logs**: `learning-records/` and `lessons/` are additive
- **Spaced repetition**: Uses file `mtime` + `progress.json` for intervals (1d → 3d → 7d)
- **Zone of Proximal Development (ZPD)**: Determined by reading timestamps + `learning-records/` status

### Architecture Notes
- **Parametric knowledge treated as untrusted**: Before teaching, it fetches high-trust sources → records in `RESOURCES.md` → cites in every lesson
- **Lesson = single tightly-scoped concept**: One HTML file, completable quickly, retrieval practice built in
- **Knowledge → Skills → Wisdom ladder**: Lessons develop both knowledge (what to know) and skills (what to practice); eventually hands off to real communities
- **CLI-invoked**: `/teach` command in Claude Code; one mission per workspace

---

## 2. OpenTutor (zijinz456/OpenTutor)

### Source
- Repository: https://github.com/zijinz456/OpenTutor
- Local-first, self-hosted AI learning platform (Docker / manual)
- Block-based adaptive workspace

### Workspace Structure (State)
Uses a **Docker volume / local `data/` directory** with this layout:

```
data/
├── user/                      # Admin workspace + global settings
├── users/<uid>/               # Per-user scope
│   ├── chat_history.db        # SQLite
│   ├── settings/interface.json
│   ├── workspace/
│   │   ├── chat/
│   │   ├── co-writer/
│   │   ├── book/
│   │   ├── memory/            # ← Memory files here
│   │   ├── notebook/
│   │   └── knowledge_bases/
└── partners/<id>/workspace/   # Partner (synthetic-user) scope
```

### Data Structures for State

| Layer | Format | Location | Description |
|-------|--------|----------|-------------|
| **Chat History** | SQLite (`chat_history.db`) | `users/<uid>/` | Full conversation history |
| **Settings** | JSON (`interface.json`, `main.yaml`) | `settings/` | UI prefs, model config, memory budgets |
| **Knowledge Bases** | LlamaIndex indices (versioned `version-N/`) | `knowledge_bases/` | RAG document collections |
| **Notebooks** | Markdown + index JSON | `workspace/notebook/` | Color-coded learning records |
| **Spaced Repetition** | FSRS 4.5 algorithm | Internal (SQLite) | Flashcard scheduling |
| **Knowledge Graph (LOOM)** | Graph structure | Experimental | Concept mastery, prerequisites |
| **Workspace Blocks** | JSON (12 block types) | Frontend state | Notes, quiz, flashcards, KG, study plan, analytics |

### State Characteristics
- **Multi-surface workspace**: Chat, notebook, co-writer, book, quiz are separate but connected workspaces
- **Block-based**: 12 composable learning blocks; AI suggests layout changes based on behavior
- **FSRS 4.5**: Algorithmic spaced repetition for flashcards (not file-mtime based)
- **Local-first**: Ollama by default, no API keys required
- **Agent system**: 3 specialist agents (Tutor, Planner, Layout) coordinated by intent-router

### Architecture Notes
- **Not a chatbot**: The "Tutor" agent teaches with adaptive depth, Socratic questioning, source citations
- **Adaptive workspace**: AI reconfigures block layout based on user behavior (fatigue, error patterns, brevity)
- **Content ingestion**: 30-sec PDF/DOCX/PPTX → structured notes, flashcards, quizzes (7 question types)
- **Experimental**: LOOM knowledge graph + LECTOR semantic review (graph-aware FSRS)

---

## 3. DeepTutor (HKUDS/DeepTutor)

### Source
- Repository: https://github.com/HKUDS/DeepTutor
- Agent-native learning workspace with **three-layer inspectable memory**

### Workspace Structure (State)
```
data/
├── user/                      # Admin workspace
├── users/<uid>/
│   ├── chat_history.db
│   ├── settings/
│   └── workspace/
│       ├── memory/            # ← Three-layer memory system
│       │   ├── trace/<surface>/<date>.jsonl    # L1
│       │   ├── L2/<surface>.md                 # L2
│       │   └── L3/<slot>.md                    # L3
│       ├── notebook/
│       ├── co-writer/
│       ├── book/
│       └── chat/
└── partners/<id>/workspace/
```

### Three-Layer Memory Architecture

| Layer | Tag | Storage | Scope | Format | Purpose |
|-------|-----|---------|-------|--------|---------|
| **L1 · Workspace Mirror** | LIVE | `trace/<surface>/<date>.jsonl` | Per-turn, per-surface | JSONL (append-only) | Raw event trace: chat turns, notebook edits, tool calls |
| **L2 · Per-Surface Summaries** | CURATED | `L2/<surface>.md` | Per-session/context | Markdown + footnote citations | Distilled facts per surface (`chat`, `notebook`, `quiz`, `kb`, `book`, `partner`, `cowriter`), each citing L1 events |
| **L3 · Cross-Surface Synthesis** | SYNTHESIS | `L3/<profile\|recent\|scope\|preferences>.md` | Cross-session | Markdown | Global propositions: profile, recent timeline, knowledge scope, preferences — hedged claims backed by L2 evidence |

### State Characteristics
- **Deliberately not a hidden vector store**: File-backed, human-readable, auditable
- **Memory Graph**: Visualizes L3 → L2 → L1 traceability (click any claim to see raw evidence)
- **Consolidator pipeline**: LLM-driven (Update / Audit / Dedup modes) with chunk-based processing
- **Surfaces tracked**: `chat`, `notebook`, `quiz`, `kb`, `book`, `tutorbot`, `cowriter`
- **CLI-accessible**: `deeptutor memory show/clear`, `deeptutor session list/show`
- **Atomic writes + locking**: `_atomic_write` (temp file + rename), per-file `asyncio.Lock`

### Architecture Notes
- **Agent-native runtime**: `ChatOrchestrator` routes turns → capabilities; `ToolRegistry` + `CapabilityRegistry`
- **Unified chat workspace**: 5 modes (Chat, Deep Solve, Deep Question, Deep Research, Math Animator) share context
- **Partners**: Persistent synthetic companions with own workspace/memory/personality (built on `nanobot`)
- **Knowledge Bases**: Versioned RAG (LlamaIndex, PageIndex, LightRAG, WeKnora) — flat `version-N` layout
- **Multi-user**: Optional auth → admin workspace + isolated per-user workspaces under `data/users/<uid>/`

---

## 4. Comparison Matrix

| Dimension | Matt Pocock `/teach` | OpenTutor | DeepTutor |
|-----------|---------------------|-----------|-----------|
| **Primary paradigm** | Single-mission teaching workspace | Block-based adaptive learning platform | Agent-native lifelong tutoring workspace |
| **State storage** | Plain files (MD, HTML, JSON) in CWD | SQLite + JSON + Markdown in `data/` volume | Three-layer: JSONL (L1) + MD (L2/L3) in `data/users/<uid>/workspace/memory/` |
| **Memory model** | Implicit via file timestamps + `learning-records/` + `progress.json` | FSRS 4.5 (algorithmic) + Knowledge Graph (LOOM) | Explicit 3-layer: Trace → Surface → Synthesis |
| **Traceability** | Manual (read `learning-records/` + `RESOURCES.md`) | Via source citations in Tutor answers | Full L3→L2→L1 graph (click to trace any claim to raw event) |
| **Spaced repetition** | File `mtime` + `progress.json` (1d/3d/7d intervals) | FSRS 4.5 (industry-standard algorithm) | Consolidator-driven (Update/Audit/Dedup budgets) |
| **Multi-session** | Yes — workspace persists across sessions | Yes — per-user workspace + notebooks | Yes — cross-session L3 synthesis survives sessions |
| **Multi-user** | No (one mission per workspace) | Single-user beta (multi-user out of scope) | Yes — `data/users/<uid>/` isolation |
| **Extensibility** | Skills (HTML components in `assets/`) | Plugin system for custom blocks | MCP servers, installable community skills (EduHub), custom tools |
| **Teaching approach** | Retrieval practice, desirable difficulty, ZPD | Adaptive depth, Socratic mode, fatigue detection | Capability-based (Deep Solve, Deep Research, Quiz Gen, Visualize) |
| **Human readability** | High — all files are Markdown/HTML | Medium — SQLite + JSON + MD | High — all memory layers are Markdown/JSONL |
| **Auditability** | Manual git versioning | Limited (chat history DB) | Built-in: Memory Graph, workbench UI, `deeptutor memory` CLI |

---

## 5. Key Architectural Contrasts

### `/teach` vs. OpenTutor vs. DeepTutor

| Aspect | `/teach` | OpenTutor | DeepTutor |
|--------|----------|-----------|-----------|
| **Philosophy** | "Make yourself unnecessary" — hand off to community | "Adaptive workspace reshapes to how you learn" | "Inspectable personalization — not a black box" |
| **Memory as code** | Workspace **is** the curriculum (lessons = output) | Workspace = block layout + scheduled flashcards | Workspace = trace → facts → synthesis pipeline |
| **State granularity** | Per-lesson (ADR-style records) | Per-block + per-flashcard (FSRS) | Per-event (L1) → per-surface (L2) → global (L3) |
| **User agency** | High — user invokes `/teach`, directs mission | Medium — AI suggests layout, user configures | High — user edits L2/L3 directly in workbench |
| **Learning science** | Explicit: fluency vs. storage strength, ZPD, interleaving | Explicit: FSRS, cognitive load detection, LOOM/LECTOR | Implicit: consolidation budgets, cross-surface synthesis |
| **Non-chatbot evidence** | Produces HTML lessons, not chat replies | Produces structured notes/quizzes, Tutor agent teaches | Produces Co-Writer drafts, Book pages, Quiz gen, Visualizations |

---

## 6. Data Structure Patterns Summary

### Pattern 1: Append-Only Lesson Log (`/teach`)
```
lessons/0001-topic.html
lessons/0002-topic.html
learning-records/topic.md  ← status + last_review
progress.json              ← {lesson_id, last_score}
```
- **Strength**: Simple, portable, git-friendly
- **Weakness**: Manual interval calculation; no algorithmic scheduling

### Pattern 2: Algorithmic Scheduler + Block Workspace (OpenTutor)
```
workspace/
  blocks/ (12 types, JSON config)
  flashcards/ (FSRS state in SQLite)
  knowledge_graph/ (LOOM nodes/edges)
```
- **Strength**: Proven spaced repetition (FSRS), adaptive UI
- **Weakness**: More complex; SQLite less portable than plain files

### Pattern 3: Hierarchical Trace → Fact → Synthesis (DeepTutor)
```
memory/
  trace/chat/2026-01-15.jsonl   ← raw events
  L2/chat.md                     ← cited facts
  L3/profile.md                  ← synthesized claims
```
- **Strength**: Full audit trail, human-editable, cross-surface learning
- **Weakness**: Requires consolidator LLM pipeline; more moving parts

---

## 7. Recommendations for a `/teach`-Inspired System

If building on the `/teach` pattern with lessons from OpenTutor/DeepTutor:

1. **Keep file-backed simplicity** — `/teach`'s Markdown/HTML approach is its superpower
2. **Add explicit L1 trace** — JSONL per session (like DeepTutor) for auditability
3. **Adopt FSRS for flashcards** — Replace file-mtime intervals with algorithmic scheduling
4. **Surface memory layers** — Expose `trace/`, `facts/`, `synthesis/` directories (DeepTutor style)
5. **Enable cross-session synthesis** — L3-like `profile.md` + `scope.md` that accumulate
6. **Make it inspectable** — CLI commands to show memory state (`teach memory show`)

---

## References

- Matt Pocock `/teach`: [topaiskills.com/skills/general/teach](https://topaiskills.com/skills/general/teach), [vibehackers.io/claude-code/skills/teach-mattpocock](https://vibehackers.io/claude-code/skills/teach-mattpocock)
- OpenTutor: [github.com/zijinz456/OpenTutor](https://github.com/zijinz456/OpenTutor)
- DeepTutor: [github.com/HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor), [docs.deeptutor.info/explore/memory/](https://docs.deeptutor.info/explore/memory/), [DeepWiki Memory System](https://deepwiki.com/tekorakle/DeepTutor/7-memory-system)
- Local research patterns: `.\\teach-skill-research\\references\\parallel-research.md`