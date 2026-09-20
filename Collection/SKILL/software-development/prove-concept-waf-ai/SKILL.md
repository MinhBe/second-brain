---
name: prove-concept-waf-ai
description: Validate AI-in-WAF feasibility via spike.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ai, waf, spike, proof-of-concept, security, performance]
    related_skills: [spike, pdf]
---

# Prove Concept WAF AI

Use when a senior or mentor proposes adding an AI component to a Web Application Firewall (WAF) request flow and you need to demonstrate feasibility.

## Procedure

1. **Baseline Capture** – Measure current WAF latency and blocking rate. Use `curl` with timing (`-w "%{time_total}"`) against a test endpoint and record ModSecurity logs.
2. **Reproduce Mentor Critique** – From `references/mentor_critique.md`, list each concrete question (throughput, latency, obfuscation handling). Translate each into a spike question.
3. **Design Spike Table** – Create a markdown table with columns: #, Question, Metric, Success Criterion, Risk.
4. **Research Options** – For AI models, pick a lightweight option (e.g., `distilbert-base-uncased` with `onnxruntime`) that can run inference <20ms per request. Document install commands.
5. **Implement Minimal AI Hook** – Write a small Flask app that receives the raw request, runs the model, and returns a decision. Wrap it with `gunicorn --workers 1` to simulate single-threaded integration.
6. **Integrate with ModSecurity** – Use ModSecurity's `SecRuleEngine` to call the external app via `SecRule REQUEST_URI "@exec /path/to/hook.sh"`; the script forwards the request body to the Flask app and exits with status 0 (allow) or 1 (block).
7. **Run Load Test** – Use `hey` or `wrk` to send 10k requests, record total time, error rate, and AI latency (log inside Flask). Compare to baseline.
8. **Verdict** – Fill the spike README with VALIDATED / PARTIAL / INVALIDATED and recommendations.

## Pitfalls

- **Blocking Loop** – If the external hook hangs, ModSecurity will block further processing. Always set a short timeout (`SecRuleTimeout`).
- **Model Warm-up** – First inference can be >200ms; warm the model before measurements.
- **Thread Safety** – `onnxruntime` sessions are not fork-safe; run a single worker or pre-load the session in the main process.
- **Obfuscation Breaks Syntax** – AI models trained on clean SQL may misclassify heavily obfuscated payloads; test with the `obfuscate.py` script from the `pdf` skill references.
- **Logging Overhead** – Writing request logs from the AI hook adds I/O latency; redirect to `/dev/null` for pure performance tests.

## Output

- `spikes/001-waf-ai/README.md` – includes the table, code snippets, and verdict.
- `spikes/001-waf-ai/app.py` – minimal Flask AI service.
- `spikes/001-waf-ai/hook.sh` – ModSecurity exec wrapper.

## Attribution

Adapted from the generic `spike` skill workflow and the mentor-critique notes in `references/mentor_critique.md`.