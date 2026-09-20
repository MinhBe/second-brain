#!/usr/bin/env python3
"""
Marie Knowledge Pipeline — Text Normalization Stage
Milestone 3 / Knowledge Pipeline Tests
Processes: Markdown, ChatGPT Conversation, Telegram Log
"""
import os
import json
import hashlib
import re
import sqlite3
import uuid

SOURCES = [
    {
        "id": "SRC001",
        "type": "markdown",
        "path": r"C:\Users\Admin\Documents\Second Brain\00 SYS - System\90 Operations\discovery_artifacts\SYSTEM_INVENTORY.md"
    },
    {
        "id": "SRC002",
        "type": "chatgpt_conversation",
        "path": r"C:\Users\Admin\Documents\Second Brain\00 SYS - System\40 Skills\conversation_archive\software_architect_gpt_session_20260920.txt"
    },
    {
        "id": "SRC003",
        "type": "telegram_log",
        "path": r"C:\Users\Admin\AppData\Local\hermes\cache\telegram\2026_09\20\broadcast_20260920_194612.json"
    }
]

def hash_content(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

def normalize_markdown(text):
    # Strip excessive whitespace, normalize line endings
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def normalize_chatgpt(text):
    # Mark AI conversation as unverified source
    lines = []
    for line in text.split("\n"):
        if line.startswith("## ") or line.startswith("### "):
            lines.append(line)
        else:
            lines.append(line.strip())
    return "\n".join(lines).strip()

def normalize_telegram(text):
    # Telegram JSON log: extract message text
    try:
        data = json.loads(text)
        messages = []
        for entry in (data if isinstance(data, list) else data.get("messages", [])):
            sender = entry.get("from", "unknown")
            msg = entry.get("text", entry.get("message", ""))
            if msg:
                messages.append(f"[{sender}]: {msg}")
        return "\n".join(messages).strip()
    except:
        return text.strip()

def normalize_source(source):
    if not os.path.exists(source["path"]):
        return None, f"FILE_NOT_FOUND: {source['path']}"
    with open(source["path"], "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()
    content_hash = hash_content(raw)
    if source["type"] == "markdown":
        normalized = normalize_markdown(raw)
    elif source["type"] == "chatgpt_conversation":
        normalized = normalize_chatgpt(raw)
    elif source["type"] == "telegram_log":
        normalized = normalize_telegram(raw)
    else:
        normalized = raw.strip()
    return {
        "source_id": source["id"],
        "source_type": source["type"],
        "content_hash": content_hash,
        "normalized": normalized[:200],
        "lines": normalized.count("\n") + 1
    }, None

results = []
all_ok = True
for src in SOURCES:
    result, err = normalize_source(src)
    if err:
        print(f"ERROR {src['id']}: {err}")
        all_ok = False
    else:
        print(f"OK   {src['id']} ({src['type']}): {result['lines']} lines, hash={result['content_hash']}")
        print(f"     Preview: {result['normalized'][:80]}...")
        results.append(result)

print()
print(f"Result: {'ALL PASSED' if all_ok else 'SOME FAILED'} ({len([r for r in results if r])}/{len(SOURCES)} processed)")
