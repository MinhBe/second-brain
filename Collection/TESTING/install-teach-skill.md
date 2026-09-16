# /teach Skill — Installation Instructions

## 1. Repository URL

**https://github.com/mattpocock/skills**

Official skills repository by Matt Pocock. The `/teach` skill lives at `skills/productivity/teach/SKILL.md`.

## 2. Installation Command

```bash
npx skills add https://github.com/mattpocock/skills --skill teach
```

This uses the `skills` CLI (published on npm) to pull the repository and install only the `teach` skill into your local skills directory.

## 3. How to Invoke the Skill Once Installed

Once installed, invoke the skill by its name:

```
/teach
```

When triggered (e.g., via a chat client that supports skills, or through the agent framework), the skill activates in the current directory — treated as a teaching workspace. It is a stateful, multi-session skill: it tracks progress via `MISSION.md`, `RESOURCES.md`, `learning-records/`, `lessons/`, and `reference/` files in the workspace.

**Argument hint:** "What would you like to learn about?" — provide a topic when invoking to ground the teaching session.
