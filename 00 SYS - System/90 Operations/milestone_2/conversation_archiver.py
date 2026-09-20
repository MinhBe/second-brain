#!/usr/bin/env python3
"""
Conversation Archiver for Hermes AI Team
Stores structured conversation logs, messages, and metadata under 00 SYS - System/30 Outputs/AI Conversations/
"""
import os
import json
import time

class ConversationArchiver:
    def __init__(self, storage_root):
        self.storage_root = storage_root
        os.makedirs(self.storage_root, exist_ok=True)

    def archive(self, conversation_id, task_id, provider, profile_id, title, tags, messages, started_at, ended_at, status="completed", source_refs=None, related_notes=None):
        conv_dir = os.path.join(self.storage_root, conversation_id)
        os.makedirs(conv_dir, exist_ok=True)

        metadata = {
            "conversation_id": conversation_id,
            "task_id": task_id,
            "provider": provider,
            "profile_id": profile_id,
            "title": title,
            "tags": tags or [],
            "started_at": started_at,
            "ended_at": ended_at,
            "status": status,
            "source_references": source_refs or [],
            "related_notes": related_notes or []
        }

        # 1. metadata.json
        with open(os.path.join(conv_dir, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # 2. messages.jsonl
        with open(os.path.join(conv_dir, "messages.jsonl"), "w", encoding="utf-8") as f:
            for m in messages:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

        # 3. conversation.md
        md_lines = [
            f"# {title}",
            f"**Conversation ID:** `{conversation_id}` | **Task ID:** `{task_id}` | **Status:** `{status}`",
            f"**Provider:** `{provider}` ({profile_id}) | **Time:** {started_at} → {ended_at}",
            f"**Tags:** {', '.join(tags) if tags else 'none'}",
            "",
            "---",
            ""
        ]
        for m in messages:
            role = m.get("role", "unknown").upper()
            content = m.get("content", "").strip()
            md_lines.append(f"### {role}")
            md_lines.append(content)
            md_lines.append("")

        with open(os.path.join(conv_dir, "conversation.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines).strip() + "\n")

        return conv_dir

    def get_by_task_id(self, task_id):
        matches = []
        for d in os.listdir(self.storage_root):
            dp = os.path.join(self.storage_root, d)
            meta_file = os.path.join(dp, "metadata.json")
            if os.path.exists(meta_file):
                try:
                    with open(meta_file, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    if meta.get("task_id") == task_id:
                        matches.append(meta)
                except:
                    pass
        return matches
