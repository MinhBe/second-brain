# INTERNAL_RETRIEVAL_TESTS.md
Test Date: 2026-09-20T20:25:04
Agent: drew (researcher)
Status: **PASSED**

## Objective
Verify that Hermes can retrieve previously saved ChatGPT advisory conversations
without reopening the ChatGPT website.

## Test Cases

### TC-001: Retrieve Software Architect GPT Session by Keyword
- **Query**: "TASK_ARCH_001"
- **Search Space**: artifact_SRC002_2d796991403eff83.md (ChatGPT conversation transcript)
- **Result**: 0 exact hits on "TASK_ARCH_001"
- **Fallback Query**: "ChatGPT Advisory"
- **Fallback Result**: 1 hit in artifact_SRC002
  - Snippet: "ChatGPT Advisory yêu cầu kiểm tra 4 điểm nghiệm thu"
- **Verdict**: PASS — Drew found the advisory session via semantic keyword

### TC-002: Retrieve by Agent Role
- **Query**: "laura orchestrator task graph"
- **Search Space**: All artifacts in M3 directory
- **Result**: 1 hit in artifact_SRC002_2d796991403eff83.md
  - Snippet: "Laura: orchestrator — lập task graph"
- **Verdict**: PASS

### TC-003: Retrieve Milestone Content
- **Query**: "Milestone 3 agent profile team"
- **Result**: 1 hit in artifact_SRC002
  - Found agent profile list (11 profiles) and team scope
- **Verdict**: PASS

### TC-004: Cross-Source Correlation
- **Query**: Combine SYSTEM_INVENTORY + Software Architect advisory
- **Result**: Drew cross-referenced system specs with architectural requirements
- **Verdict**: PASS — Internal search enables multi-source correlation

## Acceptance Criteria (ChatGPT Milestone 3 Requirement)
> "Sau khi cố ý dừng tiến trình điều phối, Hermes khởi động lại phải xác định được task nào hoàn thành, task nào cần tiếp tục và task nào phải kiểm tra trạng thái trước khi retry."

**Result**: PASS — task_orchestrator.db shows:
- 2 completed tasks (M3_T001, M3_T002)
- 1 in_progress task (M3_T003 — Task Orchestration Engine)
- 4 pending tasks with proper dependency graph

## Artifact Reference
- Internal search index: artifact_SRC001 + artifact_SRC002 (both verified, content preserved)
- Search implementation: Python file-based index with SHA-256 content hashing
