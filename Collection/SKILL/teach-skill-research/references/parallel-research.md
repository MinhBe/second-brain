# Parallel Research Reference

## Spaced Repetition via Filesystem
- **Timestamp method**: Store each lesson as `lesson_<N>.md`. Use the file's `mtime` to compute the interval since the last review.
- **Algorithm**: Read all timestamps, sort ascending, and pick the one whose age exceeds the current interval (e.g., 1-day → 3-days → 7-days). Update its `mtime` after the session.
- **Implementation**: Bash snippet to get age in days:  `age=$(( ( $(date +%s) - $(stat -c %Y lesson_1.md) ) / 86400 ))`
- **Desirable difficulty**: Add a short quiz in `quiz_<N>.md` after a lesson. Store the result in `progress.json` (simple JSON with `lesson_id` and `last_score`).

## Zone of Proximal Development (ZPD) Tracking
- **Mission file** (`MISSION.md`): declares the learner's high-level goal.
- **Learning record** (`learning-records/<topic>.md`): contains `status: pending|mastered` and `last_review:` date.
- **Next-step selector**: script reads all timestamps, sorts ascending, and picks the lesson whose age exceeds the current interval.

## Workspace-Based State (General Pattern)
- Keep a dedicated directory per learning project.
- Persist all artefacts as Markdown/JSON; the agent treats the directory as its external memory.
- Use `git` to version-control the workspace for rollback and audit.

## Example Directory Layout
```
learn-project/
├─ MISSION.md
├─ lessons/
│  ├─ lesson_01.md
│  └─ lesson_02.md
├─ quizzes/
│  └─ quiz_01.md
├─ learning-records/
│  └─ rubiks_cube.md
├─ progress.json
└─ scripts/
   └─ select_next.sh
```

*Patterns distilled from the Matt Pocock `/teach` skill and the parallel research session.*