# SPEC-1-AI-WEB-MULTI-PROFILE-OBSERVER

## Background

Tôi có nhiều Chrome Profile khác nhau trên cùng một máy tính. Mỗi profile chứa tập cookie, local storage, session và trạng thái đăng nhập riêng. Cùng một profile có thể đồng thời đăng nhập các tài khoản khác nhau trên ba dịch vụ AI mà tôi sử dụng:

- Meta AI: `https://www.meta.ai/prompt/`
- Claude: `https://claude.ai/new?incognito=`
- ChatGPT: `https://chatgpt.com/`

Số lượng profile có thể lớn và thay đổi theo thời gian. Do đó hệ thống không được thiết kế theo giả định chỉ có một tài khoản, một profile hoặc một phiên browser cố định.

Mục tiêu là xây dựng một **AI Web Multi-Profile Observer Skill** có khả năng chủ động sử dụng browser, lựa chọn đúng profile được phép sử dụng, điều hướng tới đúng provider, gửi prompt, quan sát mọi trạng thái có ý nghĩa trên UI, đọc các artifact hoặc file được tạo ra, và lưu lại toàn bộ quá trình dưới dạng audit trail có thể kiểm tra lại.

Điểm quan trọng nhất: hệ thống này không nhằm “đọc suy nghĩ bên trong” của model. Nó chỉ quan sát những gì thực sự xuất hiện trong browser, DOM/accessibility tree, file tải về, panel artifact hoặc dữ liệu mà phiên của người dùng được phép truy cập.

---

## Problem Statement

Vấn đề cần giải quyết không phải là:

> Tự động gửi một prompt tới ChatGPT.

Mà là:

> Trong một tập hợp lớn Chrome Profile có authentication state khác nhau, làm thế nào một agent có thể lựa chọn một browser session phù hợp, sử dụng Meta AI, Claude hoặc ChatGPT, theo dõi chính xác mọi phản hồi và trạng thái UI, hiểu các cảnh báo như usage-limit, tiếp tục đọc artifact được sinh ra và tạo ra bằng chứng đầy đủ về toàn bộ quá trình?

Hệ thống cần thay thế chuỗi thao tác thủ công:

1. Mở Chrome.
2. Chọn profile.
3. Kiểm tra tài khoản nào đang đăng nhập.
4. Truy cập đúng website AI.
5. Tạo conversation mới hoặc vào đúng chế độ.
6. Gửi prompt.
7. Chờ generation.
8. Đọc response.
9. Đọc warning, toast, banner, dialog hoặc lỗi.
10. Phát hiện artifact/file/document được sinh ra.
11. Mở và đọc artifact.
12. Ghi lại profile nào đã được dùng.
13. Ghi lại trạng thái account/provider sau lần chạy.
14. Lưu screenshot và timeline để kiểm chứng.

---

## Scope

### In Scope

Hệ thống chỉ cần hỗ trợ ba provider:

#### Meta AI

Entry point:

`https://www.meta.ai/prompt/`

#### Claude

Entry point:

`https://claude.ai/new?incognito=`

Lưu ý: `new?incognito=` là chế độ conversation phía Claude, không đồng nghĩa với Chrome Incognito Mode.

#### ChatGPT

Entry point:

`https://chatgpt.com/`

Hệ thống cần hỗ trợ việc mở conversation mới hoặc truy cập GPT/chat phù hợp khi workflow yêu cầu.

### Out of Scope

Phiên bản MVP không nhằm:

- hỗ trợ browser automation tùy ý trên mọi website;
- reverse engineer private API;
- bypass CAPTCHA;
- bypass provider quota;
- bypass authentication;
- lấy password;
- đánh cắp session;
- trích hidden chain-of-thought;
- suy đoán internal reasoning của model;
- điều khiển tài khoản/profile mà người dùng chưa cho phép.

---

## Core Concepts

### Chrome Profile

Một Chrome Profile là một container session riêng biệt, có thể chứa:

- cookies riêng;
- localStorage riêng;
- IndexedDB riêng;
- sessionStorage riêng;
- authentication state riêng;
- history và browser state riêng.

Tên hiển thị trên Chrome Profile Picker chỉ là nhãn dành cho người dùng, không nên được dùng làm định danh kỹ thuật duy nhất.

Hệ thống cần một `profile_id` ổn định.

Ví dụ:

```yaml
profile_id: chrome-profile-001
display_name: "165"
chrome_profile_directory: "Profile 12"
enabled: true
```

### Provider Account State

Một Chrome Profile không đồng nghĩa với một account duy nhất.

Ví dụ:

```text
Chrome Profile 001
├── ChatGPT Account A
├── Claude Account C
└── Meta Account B
```

Do đó hệ thống phải quản lý theo cặp:

```text
Chrome Profile × Provider
```

chứ không phải chỉ theo Chrome Profile.

---

## Requirements

### Must Have

Hệ thống MUST:

- hỗ trợ số lượng Chrome Profile tùy ý;
- chỉ sử dụng profile đã được người dùng cho phép;
- chỉ hoạt động với:
  - `meta.ai`
  - `claude.ai`
  - `chatgpt.com`
- duy trì registry của các profile;
- duy trì trạng thái của từng provider trong từng profile;
- có khả năng chọn profile phù hợp;
- có khả năng mở hoặc attach browser session;
- có khả năng mở đúng provider;
- xác minh trạng thái login;
- tìm ô nhập prompt;
- gửi prompt;
- phát hiện generation started;
- chờ generation kết thúc hoặc terminal state xuất hiện;
- đọc assistant response;
- đọc warning, toast, banner, alert, modal, dialog;
- nhận biết login/session error;
- nhận biết usage exhausted;
- nhận biết rate limit;
- nhận biết CAPTCHA/verification;
- nhận biết artifact/file/document;
- đọc nội dung artifact nếu browser/session có quyền truy cập;
- lưu timeline;
- lưu screenshot checkpoint;
- lưu evidence cho kết luận;
- tạo một run record độc lập cho mỗi lần chạy;
- không tuyên bố đọc được hidden chain-of-thought.

### Should Have

Hệ thống SHOULD:

- dùng accessibility role/text trước CSS selector cứng;
- có nhiều selector fallback;
- tự phát hiện UI thay đổi;
- lưu DOM/accessibility snapshot tại các checkpoint quan trọng;
- lưu screenshot khi phát hiện lỗi;
- hỗ trợ profile locking;
- hỗ trợ cooldown theo provider/profile;
- lưu raw notification text;
- trích reset time từ usage-limit message khi có thể;
- lưu artifact nguyên gốc và extracted text;
- có khả năng so sánh cùng một prompt giữa nhiều provider;
- có dry-run hoặc inspect mode.

### Could Have

Hệ thống COULD:

- chạy nhiều profile song song;
- chạy ba provider song song;
- sinh report tổng hợp;
- theo dõi lịch sử trạng thái profile;
- tạo dashboard;
- phát hiện UI drift;
- tự động cập nhật selector fallback;
- xuất JSON, Markdown và HTML report;
- hỗ trợ screenshot diff.

### Won't Have in MVP

MVP WON'T:

- tự tạo account;
- tự giải CAPTCHA;
- tự reset password;
- khai thác private endpoint;
- né usage limit;
- giả lập hoặc che giấu fingerprint;
- truy cập domain ngoài allowlist;
- đọc model internal state.

---

## Architecture Overview

```text
                         USER / AGENT
                              │
                              ▼
                       AI WEB SKILL
                              │
                    ┌─────────┴─────────┐
                    │   Orchestrator    │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ Profile Registry  │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Session Router   │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ Browser Controller│
                    └─────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         ChatGPT Adapter   Claude Adapter   Meta Adapter
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                    ┌─────────▼─────────┐
                    │ Observation Engine│
                    └─────────┬─────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
      Responses           Notifications        Artifacts
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
                    ┌─────────▼─────────┐
                    │ Audit / Run Store │
                    └───────────────────┘
```

---

## Components

### 1. Skill Orchestrator

Nhiệm vụ:

- nhận command;
- xác định provider;
- xác định prompt;
- chọn routing strategy;
- yêu cầu Session Router chọn profile;
- acquire profile lock;
- khởi tạo browser session;
- gọi provider adapter;
- khởi động Observation Engine;
- đóng run;
- release lock;
- trả report.

Ví dụ command:

```text
aiweb ask claude --profile auto --prompt prompt.md
aiweb ask chatgpt --profile chrome-profile-001 --prompt "..."
aiweb ask meta --profile auto --prompt "..."
aiweb compare --providers claude,chatgpt,meta --prompt prompt.md
aiweb inspect profiles
aiweb inspect run RUN_ID
aiweb artifacts RUN_ID
```

---

### 2. Profile Registry

Registry chứa metadata cần thiết để quản lý profile mà không lưu password.

Ví dụ:

```yaml
profiles:
  - id: chrome-profile-001
    display_name: "165"
    enabled: true
    profile_directory: "Profile 12"

    providers:
      chatgpt:
        state: authenticated
        account_alias: chatgpt-01

      claude:
        state: usage_exhausted
        cooldown_until: "2026-09-12T05:40:00+07:00"

      meta:
        state: unknown
```

#### Database Schema

```sql
CREATE TABLE browser_profiles (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    profile_directory TEXT,
    automation_user_data_dir TEXT,
    enabled INTEGER NOT NULL DEFAULT 1,
    last_seen_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE provider_accounts (
    id TEXT PRIMARY KEY,
    browser_profile_id TEXT NOT NULL,
    provider TEXT NOT NULL,
    account_alias TEXT,
    auth_state TEXT NOT NULL,
    cooldown_until TEXT,
    last_success_at TEXT,
    last_failure_at TEXT,
    last_checked_at TEXT,
    metadata_json TEXT,
    FOREIGN KEY(browser_profile_id)
      REFERENCES browser_profiles(id),
    UNIQUE(browser_profile_id, provider)
);
```

---

### 3. Provider State Model

Các trạng thái tối thiểu:

```text
UNKNOWN
READY
LOGIN_REQUIRED
SESSION_EXPIRED
USAGE_EXHAUSTED
RATE_LIMITED
VERIFICATION_REQUIRED
CAPTCHA
ERROR
UNAVAILABLE
BUSY
```

Mỗi trạng thái phải có evidence.

Ví dụ:

```json
{
  "profile_id": "chrome-profile-002",
  "provider": "claude",
  "state": "USAGE_EXHAUSTED",
  "evidence": {
    "type": "visible_text",
    "text": "You are out of free messages until 5:40 AM",
    "observed_at": "2026-09-11T14:20:23+07:00"
  }
}
```

---

### 4. Session Router

Session Router chọn profile phù hợp theo provider.

Tiêu chí MVP:

1. profile enabled;
2. provider state là READY hoặc UNKNOWN có thể kiểm tra;
3. không trong cooldown;
4. không bị lock;
5. chưa đạt failure threshold;
6. ưu tiên profile ít được dùng gần đây.

Pseudo-code:

```python
eligible = registry.profiles_for(provider)

eligible = [
    p for p in eligible
    if p.enabled
    and not p.locked
    and not p.in_cooldown(provider)
    and p.state(provider) in {"READY", "UNKNOWN"}
]

selected = min(
    eligible,
    key=lambda p: p.last_success_at(provider) or datetime.min
)
```

Routing này dùng để quản lý session được người dùng cho phép, không dùng để bypass giới hạn của provider.

---

### 5. Profile Locking

Không cho phép hai worker dùng cùng một profile đồng thời.

Schema:

```sql
CREATE TABLE profile_locks (
    browser_profile_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    acquired_at TEXT NOT NULL,
    expires_at TEXT NOT NULL
);
```

Flow:

```text
SELECT PROFILE
     ↓
ACQUIRE LOCK
     ↓
START / ATTACH BROWSER
     ↓
RUN PROVIDER WORKFLOW
     ↓
COLLECT OBSERVATIONS
     ↓
CLOSE / DETACH
     ↓
RELEASE LOCK
```

---

### 6. Browser Controller

Browser Controller chịu trách nhiệm:

- start browser;
- attach browser;
- chọn đúng profile;
- mở URL;
- điều hướng;
- click;
- fill;
- press;
- đọc accessibility tree;
- chụp screenshot;
- theo dõi navigation;
- theo dõi file download;
- theo dõi tab/window mới;
- cung cấp DOM snapshot cho Observer.

Không nên thiết kế MVP bằng cách tự copy raw cookie ra database.

Authentication state nên tiếp tục thuộc về browser profile/session.

---

## Provider Adapters

### ChatGPT Adapter

Entry point:

`https://chatgpt.com/`

Adapter cần:

- xác minh trang ChatGPT đã load;
- xác minh login state;
- tạo conversation mới khi cần;
- tìm composer;
- nhập prompt;
- gửi prompt;
- phát hiện assistant streaming;
- đợi generation hoàn thành;
- đọc final response;
- phát hiện warning/error;
- phát hiện file;
- phát hiện link;
- phát hiện artifact/document panel nếu UI hỗ trợ.

Terminal states:

```text
COMPLETED
LOGIN_REQUIRED
RATE_LIMITED
USAGE_EXHAUSTED
CAPTCHA
ERROR
TIMEOUT
```

---

### Claude Adapter

Entry point:

`https://claude.ai/new?incognito=`

Adapter cần:

- xác minh login;
- xác minh incognito conversation page;
- tìm prompt composer;
- gửi prompt;
- theo dõi assistant stream;
- đọc response;
- đọc usage notification;
- đọc banner;
- đọc modal;
- phát hiện artifact;
- phát hiện downloadable output;
- parse reset time nếu có.

Ví dụ notification:

```text
You are out of free messages until 5:40 AM
```

Normalized event:

```json
{
  "event_type": "usage_limit",
  "provider": "claude",
  "severity": "blocking",
  "blocking": true,
  "raw_text": "You are out of free messages until 5:40 AM",
  "reset_time_local": "05:40"
}
```

Sau đó registry có thể cập nhật:

```text
state = USAGE_EXHAUSTED
cooldown_until = parsed_datetime
```

---

### Meta AI Adapter

Entry point:

`https://www.meta.ai/prompt/`

Adapter cần:

- xác minh login/session;
- tìm composer;
- gửi prompt;
- đọc response;
- nhận biết loading/generation;
- đọc warning;
- phát hiện dialog/error;
- phát hiện downloadable output;
- phát hiện link hoặc artifact có thể truy cập.

---

## Observation Engine

Observation Engine là phần quan trọng nhất.

Nó không chỉ chờ selector của assistant response.

Nó chạy event loop để phát hiện nhiều loại tín hiệu.

```text
                    PAGE CHANGED
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      RESPONSE        NOTIFICATION    ARTIFACT
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                    NORMALIZER
                         │
                         ▼
                      RUN LOG
```

### Observation Sources

Observer có thể đọc từ:

- accessibility tree;
- visible DOM text;
- ARIA roles;
- page URL;
- title;
- toast region;
- alert region;
- modal/dialog;
- disabled states;
- browser download events;
- tab/window events;
- screenshot;
- network/browser failure signal nếu browser backend cung cấp.

### Event Types

```text
PAGE_OPENED
AUTH_VERIFIED
AUTH_FAILED
PROMPT_SUBMITTED
GENERATION_STARTED
GENERATION_PROGRESS
GENERATION_COMPLETED
ASSISTANT_RESPONSE
NOTIFICATION
WARNING
ERROR
USAGE_LIMIT
RATE_LIMIT
LOGIN_REQUIRED
SESSION_EXPIRED
CAPTCHA
ARTIFACT_DISCOVERED
ARTIFACT_OPENED
ARTIFACT_READ
DOWNLOAD_STARTED
DOWNLOAD_COMPLETED
NAVIGATION
SCREENSHOT_CAPTURED
RUN_COMPLETED
RUN_FAILED
```

---

## Notification Understanding

Notification phải được lưu cả raw text và normalized meaning.

Ví dụ:

```json
{
  "event_id": "evt_01",
  "event_type": "USAGE_LIMIT",
  "provider": "claude",
  "profile_id": "chrome-profile-001",
  "raw_text": "You are out of free messages until 5:40 AM",
  "parsed": {
    "reset_time": "05:40"
  },
  "blocking": true,
  "observed_at": "2026-09-11T14:20:23+07:00",
  "page_url": "https://claude.ai/new?incognito="
}
```

Nếu notification chứa link, log cần lưu:

```json
{
  "text": "Understanding usage and length limits",
  "href": "https://..."
}
```

Nếu policy của workflow cho phép, link có thể được mở trong child observation task.

---

## Artifact Reader

Nếu model tạo artifact/file/document, run không nên kết thúc ngay.

Workflow:

```text
ARTIFACT DISCOVERED
        ↓
OPEN / DOWNLOAD
        ↓
DETECT TYPE
        ↓
READ CONTENT
        ↓
SAVE ORIGINAL
        ↓
HASH
        ↓
EXTRACT TEXT
        ↓
ATTACH TO RUN
```

### Supported MVP Artifact Types

- Markdown;
- plain text;
- code;
- JSON;
- downloadable `.md`;
- downloadable `.txt`;
- browser-rendered text document;
- provider artifact panel.

### Artifact Schema

```sql
CREATE TABLE artifacts (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    provider TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    title TEXT,
    source_url TEXT,
    local_path TEXT,
    mime_type TEXT,
    sha256 TEXT,
    extracted_text_path TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(run_id)
      REFERENCES runs(id)
);
```

---

## Run Model

Mỗi run là một đơn vị audit độc lập.

Schema:

```sql
CREATE TABLE runs (
    id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    browser_profile_id TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    entry_url TEXT NOT NULL,
    prompt_text TEXT,
    status TEXT NOT NULL,
    response_path TEXT,
    error_code TEXT,
    metadata_json TEXT,
    FOREIGN KEY(browser_profile_id)
      REFERENCES browser_profiles(id)
);
```

### Example Run Record

```json
{
  "run_id": "run_01JXYZ",
  "provider": "claude",
  "profile_id": "chrome-profile-001",
  "started_at": "2026-09-11T14:20:01+07:00",
  "entry_url": "https://claude.ai/new?incognito=",
  "prompt": "Analyze this document",
  "status": "USAGE_EXHAUSTED",
  "response": null,
  "notifications": [
    {
      "type": "usage_limit",
      "text": "You are out of free messages until 5:40 AM"
    }
  ],
  "artifacts": [],
  "screenshots": [
    "screenshots/003-usage-limit.png"
  ]
}
```

---

## Timeline

Không chỉ lưu final state.

Ví dụ:

```text
14:20:01.120 profile selected: chrome-profile-001
14:20:02.011 profile lock acquired
14:20:03.431 browser attached
14:20:05.008 claude.ai opened
14:20:07.115 authentication verified
14:20:10.208 prompt submitted
14:20:11.004 generation started
14:20:23.882 notification detected
14:20:23.891 usage limit classified
14:20:24.102 screenshot captured
14:20:24.801 provider state updated
14:20:25.003 run terminated
14:20:25.100 profile lock released
```

---

## Evidence Model

Mọi kết luận quan trọng phải trỏ tới evidence.

Ví dụ:

```text
STATUS
USAGE_EXHAUSTED

EVIDENCE
Provider: Claude
Profile: chrome-profile-001
URL: https://claude.ai/new?incognito=
Observed text:
"You are out of free messages until 5:40 AM"
Observed at:
2026-09-11 14:20:23 +07:00
Screenshot:
screenshots/003-usage-limit.png
```

Mục tiêu là phân biệt rõ:

```text
agent inference
```

và:

```text
browser-observed evidence
```

---

## Storage Layout

Đề xuất:

```text
runs/
  2026-09-11/
    run_01JXYZ/
      run.json
      timeline.jsonl
      response.md
      notifications.json
      browser-state.json
      screenshots/
        001-page-opened.png
        002-prompt-submitted.png
        003-usage-limit.png
        004-final.png
      artifacts/
        artifact-001.md
        artifact-001.meta.json
```

---

## Skill Package Layout

```text
ai-web-observer/
├── SKILL.md
├── REFERENCE.md
├── PROVIDERS.md
├── SECURITY.md
├── schemas/
│   ├── run.schema.json
│   ├── event.schema.json
│   ├── artifact.schema.json
│   └── profile.schema.json
├── references/
│   ├── chatgpt.md
│   ├── claude.md
│   ├── meta-ai.md
│   ├── profile-routing.md
│   └── observer-events.md
├── scripts/
│   ├── discover-profiles.mjs
│   ├── inspect-profile.mjs
│   ├── run-prompt.mjs
│   ├── inspect-artifact.mjs
│   └── export-run.mjs
├── src/
│   ├── orchestrator/
│   ├── browser/
│   ├── registry/
│   ├── router/
│   ├── providers/
│   │   ├── chatgpt.ts
│   │   ├── claude.ts
│   │   └── meta.ts
│   ├── observer/
│   ├── artifacts/
│   └── storage/
└── evals/
    ├── happy-path.json
    ├── usage-limit.json
    ├── login-required.json
    ├── artifact-created.json
    └── ui-drift.json
```

---

## Safety Boundary

Hệ thống chỉ được dùng các profile và tài khoản mà người dùng đã cấp quyền.

Hệ thống không được:

- export password;
- tự động bypass login;
- bypass CAPTCHA;
- bypass provider usage limit;
- giả mạo browser state để né giới hạn;
- dùng session của profile ngoài allowlist;
- truy cập domain ngoài allowlist;
- tuyên bố đọc được hidden reasoning.

---

## Observability Boundary

Skill có thể biết:

```text
✓ browser đang ở URL nào
✓ profile nào được sử dụng
✓ UI hiển thị text gì
✓ assistant trả lời gì
✓ notification nói gì
✓ link nào xuất hiện
✓ file nào được tạo
✓ artifact chứa nội dung gì
✓ click/fill/navigation nào đã được thực hiện
✓ screenshot nào chứng minh trạng thái
```

Skill không thể kết luận rằng nó biết:

```text
✗ hidden chain-of-thought
✗ internal reasoning tokens
✗ model state không hiển thị
✗ model "nghĩ gì" nhưng không xuất hiện trên UI
```

---

## Failure Handling

### Login Required

```text
state = LOGIN_REQUIRED
capture screenshot
save evidence
stop run
```

### Usage Exhausted

```text
state = USAGE_EXHAUSTED
parse reset time
save notification
update cooldown
capture screenshot
stop run
```

### CAPTCHA

```text
state = CAPTCHA
capture screenshot
stop automation
require user intervention
```

### Timeout

```text
state = TIMEOUT
capture last known UI
save partial response
save timeline
stop run
```

### UI Drift

Nếu selector không còn hoạt động:

```text
fallback to accessibility search
fallback to text/role search
capture DOM/accessibility snapshot
mark adapter drift
stop if no safe action can be identified
```

---

## Implementation Plan

### Phase 0 — Environment

- tạo project;
- chọn runtime;
- thiết lập browser automation backend;
- tạo database;
- tạo run directory;
- tạo logging framework;
- tạo config format.

### Phase 1 — Single Profile / Single Provider

Mục tiêu:

- một profile;
- một provider;
- gửi prompt;
- đọc response;
- lưu screenshot;
- lưu run.

Nên bắt đầu với Claude hoặc ChatGPT.

### Phase 2 — Observation Engine

Thêm:

- toast detection;
- alert detection;
- dialog detection;
- usage limit;
- login state;
- error state;
- terminal state machine.

### Phase 3 — Artifact Reader

Thêm:

- artifact discovery;
- file download;
- Markdown reader;
- text reader;
- hashing;
- artifact metadata.

### Phase 4 — Multi-Profile Registry

Thêm:

- profile discovery;
- profile registration;
- provider state;
- locking;
- profile inspection.

### Phase 5 — Session Router

Thêm:

- auto profile selection;
- cooldown;
- failure history;
- least-recently-used strategy.

### Phase 6 — Three Provider Support

Hoàn thiện:

- ChatGPTAdapter;
- ClaudeAdapter;
- MetaAIAdapter.

### Phase 7 — Audit and Reporting

Thêm:

- Markdown report;
- JSON export;
- evidence links;
- screenshot index;
- artifact index;
- run inspection command.

---

## Milestones

### M1 — Browser Proof of Concept

Done when:

- browser mở đúng profile;
- truy cập provider;
- gửi prompt;
- đọc response;
- lưu screenshot.

### M2 — Reliable Observer

Done when:

- phát hiện response;
- phát hiện warning;
- phát hiện login error;
- phát hiện usage limit;
- tạo normalized event.

### M3 — Artifact Support

Done when:

- artifact được phát hiện;
- mở được;
- đọc nội dung;
- lưu file;
- liên kết với run.

### M4 — Multi-Profile Support

Done when:

- registry chứa nhiều profile;
- profile state độc lập theo provider;
- profile locking hoạt động.

### M5 — Auto Routing

Done when:

- `--profile auto` chọn profile hợp lệ;
- tránh profile đang cooldown;
- tránh profile đang busy.

### M6 — Full Provider Coverage

Done when:

- ChatGPT;
- Claude;
- Meta AI

đều chạy qua cùng một contract.

### M7 — Auditable MVP

Done when mỗi run trả lời được:

1. Profile nào được dùng?
2. Provider nào được dùng?
3. Skill đã làm gì?
4. AI đã trả gì?
5. Warning/error nào xuất hiện?
6. Artifact nào được tạo?
7. Evidence nằm ở đâu?

---

## Gathering Results

Sau khi chạy production, cần đo:

### Functional Accuracy

- tỷ lệ gửi prompt thành công;
- tỷ lệ đọc đúng assistant response;
- tỷ lệ phát hiện usage-limit;
- tỷ lệ phát hiện login-required;
- tỷ lệ đọc artifact thành công;
- tỷ lệ profile routing đúng.

### Reliability

- run success rate;
- timeout rate;
- selector failure rate;
- UI drift rate;
- browser attach failure rate.

### Observability Quality

- % terminal state có screenshot;
- % kết luận có evidence;
- % artifact có hash;
- % run có timeline đầy đủ.

### Performance

- thời gian từ command đến browser ready;
- thời gian gửi prompt;
- thời gian observer phát hiện generation complete;
- overhead của screenshot/logging.

### Safety

- không truy cập domain ngoài allowlist;
- không dùng profile ngoài allowlist;
- không tự động bypass CAPTCHA;
- không tự động bypass usage limit;
- không lưu password trong log.

---

## Definition of Success

Hệ thống được xem là giải quyết đúng bài toán khi người dùng có thể đưa một yêu cầu như:

```text
aiweb ask claude --profile auto --prompt prompt.md
```

và nhận lại một run report có thể trả lời chính xác:

1. Profile nào được sử dụng?
2. Profile đó có trạng thái Claude như thế nào?
3. Browser đã mở URL nào?
4. Skill đã click/fill/navigation gì?
5. Prompt nào đã được gửi?
6. Model có bắt đầu generation không?
7. Model trả lời gì?
8. Có toast/banner/warning/error nào không?
9. Nếu usage-limit xuất hiện thì raw text là gì?
10. Có reset time hay không?
11. Có artifact/file nào được tạo không?
12. Artifact chứa nội dung gì?
13. Screenshot và evidence nằm ở đâu?
14. Run kết thúc ở terminal state nào?

Mục tiêu cuối cùng là một **AI Web Multi-Profile Observer Skill** hoạt động như lớp điều phối và quan sát phía trên Chrome Profile, thay vì một browser automation script đơn giản.

---

## Need Professional Help in Developing Your Architecture?

Please contact me at [sammuti.com](https://sammuti.com) :)
