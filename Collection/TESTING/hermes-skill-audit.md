# Hermes Skills Audit: Teaching & Learning Capabilities

**Audit Date:** 2026-09-16  
**Skills Root:** `C:\Users\Admin\AppData\Local\hermes\skills\`  
**Search Keywords:** `teach`, `learn`, `lesson`, `tutor`, `drill`, `progressive`

---

## 1. Existing Skills with Teaching/Learning Keywords

| Skill Path | Keywords Found | Context |
|---|---|---|
| `autonomous-ai-agents/computer-use/SKILL.md` | `learn` | Describes teaching the `computer_use` action vocabulary to Hermes agents. One-time instructional setup, not a persistent learning track. |
| `creative/claude-design/SKILL.md` | `learn`, `progressive` | Surface "Decide / Learn" (surface 5) and progressive disclosure patterns. Has Tweaks panel with `localStorage` persistence of design preferences, but per-artifact only. |
| `productivity/pdf/SKILL.md` | `learn` | General PDF operations. No inherent teaching/learning tracking. |
| `research/llm-wiki/SKILL.md` | `learn` | Build/query interlinked markdown knowledge base (Karpathy LLM Wiki pattern). **Stateful** — tracks ingested sources, cross-references, contradictions, and synthesis over time. |

---

## 2. Stateful vs. Stateless Evaluation

| Skill | Stateful? | Why |
|---|---|---|
| `autonomous-ai-agents/computer-use` | **Stateless** | Teaches the action vocabulary once; no progress tracking, no persistent student state. Each session is independent. |
| `creative/claude-design` | **Partially stateful** | `localStorage` persists Tweaks values within a single artifact session; surfaces guide composition but no cross-session student progress tracking. |
| `productivity/pdf` | **Stateless** | Pure document manipulation; no learning trajectory or progress persistence. |
| `research/llm-wiki` | **Stateful** | Wiki directory compounds knowledge across sessions: sources ingested, cross-links maintained, contradictions flagged, synthesis updated. Progress is inherently persistent via the markdown files on disk. |

---

## 3. Gaps Where Pocock's `/teach` Approach Could Add Value

The following capabilities from Matt Pocock's `/teach` skill are **not** represented in the current installed skill set, representing clear gaps:

| Gap | Current Status | Pocock `/teach` Feature Missing |
|---|---|---|
| **Student progress tracking** | No skill tracks a learner's level, completed topics, or what's next across sessions. | `/teach` maintains `MISSION.md`, `learning-records/`, and `lessons/` to track current level, completed topics, and curated progression. |
| **Contextual pathing / next-step recommendations** | Design skill's surface selection is one-time; no memory of what came before. | `/teach` knows the "next step" based on previous successes/failures, enabling non-linear, adaptive curriculum. |
| **Memory of what has been mastered** | No skill avoids redundant instruction by remembering prior mastery. | `/teach` remembers what the student has already mastered to prevent re-teaching. |
| **Accumulated resource library** | No skill builds a growing library of resources selected over time. | `/teach` accumulates a `reference/` library of resources that worked across sessions. |
| **Persistent learning record** | Only `llm-wiki` has persistent state, but it's general knowledge-curation, not skill-acquisition tracking. | `/teach` uses a private scratchpad for student preferences, "watch outs," and instructional strategies — the internal "teacher's notes." |
| **Desirable difficulty / retrieval practice** | No skill introduces spacing, interleaving, or retrieval practice to ensure mastery. | `/teach` deliberately introduces "desirable difficulty" (retrieval practice, spacing, interleaving) for storage strength vs. fluency. |

---

## Summary

- **4 installed skills** contain the target keywords.
- **Only 1 skill** (`research/llm-wiki`) is truly stateful in the Pocock sense — it persists knowledge across sessions via a markdown wiki.
- **0 installed skills** match the full `/teach` paradigm of stateful, multi-session student progress tracking.
- **Major gap**: No skill implements Pocock's core principle that *effective teaching is inherently stateful* — remembering progress, pathing the next step, and accumulating a resource library over time.

**Recommendation:** Consider installing Matt Pocock's `/teach` skill (`skills/productivity/teach`) or building a custom stateful teaching skill that tracks a learner's journey from novice to mastery, with persistent records of completed topics, mastered concepts, and curated next steps.

---
*Report generated from search of `C:\Users\Admin\AppData\Local\hermes\skills\` SKILL.md files.*