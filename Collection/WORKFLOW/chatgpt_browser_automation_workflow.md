# ChatGPT Browser Automation Workflow

This workflow interacts with an **existing authenticated ChatGPT conversation** through the `chrome-real` MCP server.

For execution details, use the narrower skill:

```text
Collection/SKILL/chatgpt-thread-controller/SKILL.md
```

## Invariants

- Reuse the exact `https://chatgpt.com/c/<conversation-id>` thread.
- Prefer an already-open matching tab.
- Use the user's authenticated visible Chrome session.
- Never create a clean/headless profile as a silent fallback.
- Never extract cookies or authentication material.
- Take a fresh snapshot before every UID-based interaction.
- Verify the user turn appears after submission.
- Wait for a stable assistant response.
- Leave the original conversation tab open.
- Do not allow two agents to write to the same conversation simultaneously.

## Minimal MCP Sequence

### 1. Find the target

```text
mcp__chrome_real__list_pages()
```

If an exact matching conversation is present, reuse it. Otherwise:

```text
mcp__chrome_real__new_page(url="https://chatgpt.com/c/...")
```

### 2. Select the target

```text
mcp__chrome_real__select_page(pageId=<id>, bringToFront=true)
```

### 3. Inspect current UI

```text
mcp__chrome_real__take_snapshot(pageId=<id>)
```

Confirm the expected conversation URL and find the current composer semantically.

### 4. Enter and send

Use the latest snapshot UID only.

```text
mcp__chrome_real__fill_form(
  pageId=<id>,
  elements=[{"uid":"<current-composer-uid>","value":"<exact user prompt>"}]
)

mcp__chrome_real__press_key(pageId=<id>, key="Enter")
```

A visible Send button may be clicked instead when the current snapshot makes that safer.

### 5. Verify submission

Take a new snapshot and verify the new user message is present. If it is not present, the interaction has not succeeded.

### 6. Wait for completion

Prefer observed UI state or `wait_for` where useful. Do not rely on a single arbitrary sleep.

### 7. Capture the corresponding response

Take a final snapshot and extract the latest assistant turn **after** the submitted user message.

## Success Criteria

- exact target conversation: observed
- authenticated session reuse: observed
- user prompt submitted: observed
- assistant response stable: observed
- correct latest response captured: observed
- original tab left open: observed

No run is successful solely because a navigation or input tool returned without error.
