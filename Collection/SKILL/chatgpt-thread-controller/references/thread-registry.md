# ChatGPT Thread Registry

Keep personal ChatGPT conversation URLs out of a public skill repository.

Create the local registry on the Hermes host:

```text
~/.hermes/chatgpt-threads.yaml
```

Example:

```yaml
threads:
  history:
    url: "https://chatgpt.com/c/REPLACE-WITH-CONVERSATION-ID"
    reuse_existing_tab: true
    keep_open: true

  math:
    url: "https://chatgpt.com/c/REPLACE-WITH-CONVERSATION-ID"
    reuse_existing_tab: true
    keep_open: true
```

Resolution rules:

1. A URL explicitly supplied by the user overrides the registry.
2. An alias must resolve to exactly one URL.
3. Never invent or fuzzy-match a conversation ID.
4. Never commit a user's private thread registry back to a public repository.
5. The registry stores routing metadata only; it must not contain cookies, tokens, passwords, or exported browser state.
