# Plan: Learn Agent Mindset via YouTube + Hermes /teach Skill

**Date:** 2026-09-16
**Status:** Planning phase — no action taken yet

---

## 1. What You Want

- Search YouTube for "teach and learn skill" content
- Watch / read transcripts of relevant videos (e.g. Matt Pocock's `/teach` skill video)
- Analyze the mindset/philosophy about learning and teaching
- Check if Hermes already has a matching skill
- If not, create/save one
- Organize all results in `Ω/TESTING/`

---

## 2. Pre-flight Check — What You Have

| Item | Status |
|------|--------|
| `youtube-content` skill | ✅ Installed |
| `hermes-agent` skill | ✅ Installed |
| `/teach` skill (Matt Pocock's) | ❌ NOT installed |
| `delegate_task` (parallel agents) | ✅ Ready out of the box |
| Default `max_concurrent_children` | 3 (no unlock needed) |

**No setup is required before running parallel agents.** `delegate_task` works immediately. To increase from 3 to more, run:
```
hermes config set delegation.max_concurrent_children 10
```
But start with the default — 3 agents in parallel is fine.

---

## 3. Video Already Analyzed

**Video:** https://www.youtube.com/watch?v=s5T5oQJcJ6U
**Title:** "Learn anything with the /teach skill" by Matt Pocock
**Key philosophy extracted:**

### Core Idea: `/teach` Must Be Stateful

- **Stateless skill** = no memory between runs, no file system persistence (e.g. `grill-me` skill)
- **Stateful skill** = retains state, tracks progress, saves notes locally (e.g. `grill-with-docs` saves ADRs/glossaries)
- Good teaching is **stateful** — the teacher remembers your level, what you've learned, what's next
- `/teach` skill must remember: your current level, completed topics, resources that worked before

### Matt Pocock's Teaching Philosophy
1. A real teacher is **aligned with your mission** — not just generic content
2. A real teacher **remembers where you are** in the learning journey
3. A real teacher **knows what comes next** — curated progression
4. A real teacher **has a library of resources** accumulated over time
5. Teaching improves with repetition (the skill gets better over time if stateful)

### Install Command (when ready)
```
# From mapper.got skills repo → skills.sh installer → choose "Teach"
# Then run inside any coding agent in an empty directory:
/teach
```

---

## 4. Your Plan (Parallel Execution)

```
Agent 1 → Transcript & analyze the Pocock video in full detail
Agent 2 → Search for more YouTube videos on "teach AI agent skill learning" 
          and transcript top results
Agent 3 → Search the Hermes skill catalog for any existing 
          learn/teach/skill-building skill
Agent 4 → Search web for Matt Pocock's full skill repo / mapper.got 
          to understand /teach installation details
```

All output → `C:\Users\Admin\Documents\Second Brain\Ω\TESTING\`

---

## 5. What To Do RIGHT NOW

Just say the word and I'll dispatch all 4 agents in parallel using `delegate_task`. No config changes needed. The system will:

1. Run up to 3 concurrently (your default cap)
2. Dispatch agent 4 as soon as a slot opens
3. Collect all results and write markdown files to `Ω/TESTING/`

**Say "go" and I'll launch them all.**