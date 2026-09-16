# Technical Code Review: Matt Pocock `/teach` Skill

**Source:** `mattpocock/skills` → `skills/productivity/teach/`
**Files analyzed:** `SKILL.md`, `MISSION-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `agents/openai.yaml`
**Date:** 2026-09-16

---

## 1. Architecture Overview

The `/teach` skill is **not** code-heavy — it is primarily a structured prompt system. There is no executable logic (no `.js`, no Python). The "intelligence" lives entirely in:

- A markdown skill file that instructs the agent how to behave
- Format templates (Markdown files) that define the schema of every output
- A YAML policy file that controls invocation rules

---

## 2. File Inventory

```
teach/
├── SKILL.md                    ← Main prompt/instruction file
├── MISSION-FORMAT.md           ← Template for MISSION.md
├── LEARNING-RECORD-FORMAT.md  ← Template for learning-records/*.md
├── RESOURCES-FORMAT.md         ← Template for RESOURCES.md
├── GLOSSARY-FORMAT.md          ← Template for glossary entries
└── agents/
    └── openai.yaml             ← Invocation policy (display name, short description)
```

---

## 3. How It Decides "What to Teach Next" — Zone of Proximal Development (ZPD)

The ZPD logic is **entirely implicit** — there is no algorithm. The skill instructs the agent to:

```
Figure out their zone of proximal development by:
- Reading their `learning-records`
- Figuring out the right thing to teach them based on their mission
- Teach the most relevant thing that fits in their zone of proximal development
```

This means the agent itself performs the reasoning. The data it reads to decide:

| Input | Location | Purpose |
|---|---|---|
| **Mission** | `MISSION.md` (workspace root) | Why is the user learning this? What does success look like? |
| **Prior knowledge** | `learning-records/*.md` | What has the user already demonstrated mastery of? |
| **Gaps/misconceptions** | `learning-records/*.md` | What was wrong and is now corrected? What should be avoided? |
| **Constraints** | `MISSION.md` | What is out of scope? What bounds the approach? |

The agent then synthesizes: *"What is the most relevant thing the user cannot yet do, that is closest to what they already know?"*

---

## 4. Learning Record: The Core State Mechanism

`LEARNING-RECORD-FORMAT.md` defines a learning record as the teaching equivalent of an **ADR (Architecture Decision Record)**. It is deliberately minimal:

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned, and why it changes what to teach next.}
```

**Trigger conditions** — write a learning record when:
1. User demonstrated genuine understanding (not just exposure)
2. User disclosed prior knowledge ("I already know X")
3. A misconception was corrected
4. The mission shifted

**Key design insight:** Learning records are **decision-grade evidence**, not a journal. Session logs are explicitly forbidden. Only facts that steer future decisions qualify.

**Supersession:** When understanding evolves, the old record is marked `Status: superseded by LR-NNNN` — never deleted. This preserves the history of how understanding deepened, which itself is useful signal.

---

## 5. The "Next Lesson" Algorithm (Implicit)

The skill does not define an explicit scheduling algorithm. Instead, lesson selection follows this priority order:

```
IF user specifies a specific topic:
  → Teach that topic (aligned to mission)
ELSE:
  → Read all learning-records
  → Find the concept just beyond current mastery (ZPD)
  → Design a lesson that:
      - Is short and completable quickly
      - Gives one tangible win
      - Is tied directly to the mission
      - Is at the edge of working memory (Tufte-style, clean typography)
```

**Spacing:** The skill does NOT implement algorithmic spaced repetition. It relies on:
- File modification time (`mtime`) of lessons
- The agent's own judgment about when to revisit
- Progress tracked in `learning-records/` — the agent decides when to schedule review

---

## 6. System Prompt Segments — Teacher Personality

### Core Identity
> "You are a teacher. The user is your student. The agent is their tutor."

### Preamble
> "The user has asked you to teach them something. This is a **stateful request** — they intend to learn the topic over multiple sessions."

### Philosophy: Knowledge → Skills → Wisdom
> To learn at a deep level, the user needs three things:
> - **Knowledge** — from high-quality, high-trust resources
> - **Skills** — acquired through interactive lessons
> - **Wisdom** — from real-world community interaction

### The Most Critical Instruction
> "Before the `RESOURCES.md` is well-populated, your focus should be to find high-quality resources. **Never trust your parametric knowledge.**"

### Desirable Difficulty Mandate
> "Fluency can give the user an illusory sense of mastery, but storage strength is the real goal."
>
> Design lessons with:
> - Retrieval practice (recall from memory, not re-reading)
> - Spacing (distribute practice over time)
> - Interleaving (mix related but distinct subskills)

### Lesson Quality Standard
> "Each lesson should be **beautiful**, with clean, readable typography. Think Tufte. Lessons will rarely be revisited — but reference documents will be."

### Community Handoff
> "When the user asks a question that appears to require wisdom, your default posture should be to attempt to answer — but to ultimately delegate to a **community**."

---

## 7. Invocation Policy

`agents/openai.yaml`:
```yaml
interface:
  display_name: "Teach"
  short_description: "Learn a concept in a guided workspace"
policy:
  allow_implicit_invocation: false   # Must be explicitly triggered
```

`disable-model-invocation: true` in SKILL.md frontmatter means this skill does not recursively invoke another model call within its execution.

---

## 8. Key Technical Observations

| Aspect | Finding |
|---|---|
| **Executable code** | None. Entirely prompt-driven. |
| **Spaced repetition algorithm** | Not implemented. Relies on agent judgment + file `mtime`. |
| **State persistence** | Plain Markdown/HTML files in workspace. |
| **ZPD calculation** | Implicit — agent reads records and synthesizes. |
| **Invocation** | Explicit only (`allow_implicit_invocation: false`). |
| **Reuse enforcement** | Lessons must use `./assets/` components — no duplication. |
| **Reuse default** | "Reuse is the default, not the exception." |

---

## 9. What This Means for Building on This Pattern

1. **No code = fully portable** — the skill is just markdown files; no build step, no dependencies.
2. **The agent IS the scheduler** — there is no SM-2 or FSRS algorithm; the agent decides when to review based on reading its own lesson outputs.
3. **The knowledge/skill/wisdom ladder** is the real pedagogical backbone — every lesson should serve exactly one of these three stages.
4. **The MISSION is the compass** — every teaching decision traces back to it. If the mission is vague, the teaching will drift.

---

*Technical review compiled from source at `mattpocock/skills` → `skills/productivity/teach/`*