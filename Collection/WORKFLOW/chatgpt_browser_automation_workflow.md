# ChatGPT Browser Automation Workflow

This workflow documents the procedure to interact with an authenticated ChatGPT session using the `chrome-real` MCP server.

## Prerequisites
- Google Chrome must be running on the host system.
- `chrome-real` MCP server must be available.

## Workflow Steps

### 1. Identify Target Conversation
Use the list of open tabs to locate the desired ChatGPT conversation.
```bash
# Call via MCP
mcp__chrome_real__list_pages()
```

### 2. Access Conversation
If the conversation is not open, open it using the target URL.
```bash
# Call via MCP
mcp__chrome_real__new_page(url="https://chatgpt.com/c/...")
```

### 3. DOM Inspection
Always capture the current state of the page before interacting.
```bash
# Call via MCP
mcp__chrome_real__take_snapshot(pageId=...)
```

### 4. Interaction
Fill the identified message box and submit.
```bash
# Identify the textbox UID from the snapshot (e.g., '13_271')
mcp__chrome_real__fill_form(pageId=..., elements=[{"uid": "...", "value": "your prompt"}])
mcp__chrome_real__press_key(pageId=..., key="Enter")
```

### 5. Verification
Wait for response generation, then re-capture the snapshot to extract the response.
```bash
mcp__chrome_real__take_snapshot(pageId=...)
# Extract response from the StaticText elements in the snapshot
```

## Success Criteria
- Browser connection: SUCCESS.
- Interaction type: Authenticated session reuse (no profile creation).
- Validation: Bi-directional confirmation (User Message matches, Assistant Response is stable).
