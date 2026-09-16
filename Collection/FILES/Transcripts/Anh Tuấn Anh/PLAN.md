# PLAN: Proving Anh Tuấn Anh's Idea — AI-Inserted WAF Request Flow

Status: Draft (awaiting your sign-off)
Owner: You (Pham Do Anh Minh's thesis + senior critique by Anh Tuấn Anh)
Output dir: C:\Users\Admin\Documents\Second Brain\Ω\FILES\Transcripts\Anh Tuấn Anh\

---

## 0. What we are proving

Anh Tuấn Anh's core idea (voice-018, 00:23–00:51):

> "Instead of only using rule-matching, insert an AI detector into the WAF request-processing pipeline.
> The AI aggregates **signals** from each incoming request and returns a risk flag,
> while the existing rule-based WAF keeps handling the high-throughput filtering.
> But first — you must understand the current WAF flow, measure the latency per request,
> and build it in a **lab** before claiming it works at cloud scale (millions of requests)."

This plan addresses his three knowledge nodes (N1/N2/N3 from `voice-018_KNOWLEDGE.md`):

- **N3 (understand flow + cost before inserting AI):** Step 1–2 below. Map the WAF pipeline, benchmark baseline latency/throughput, then add AI only at a measured insertion point.
- **N1 (clear path from synthetic data → benefit):** Step 3. Use the SeqGAN-improved model (from your thesis Ch. II.4) to generate the SQL-aware training data, then wire that model's detection capability into the WAF pipeline as the AI signal source.
- **N2 (independent evaluation):** Step 5. Evaluate the AI-augmented WAF with a **separate** test harness: WAF-only vs. WAF+AI, using independent metrics (latency, throughput, attack recall, false-positive rate).

---

## 1. Lab Environment Setup (baseline WAF)

| Component | What | Where / How |
|---|---|---|
| Target web app | A minimal Flask/Python HTTP server with an intentionally vulnerable search endpoint (`?q=` that builds a raw SQL string) | `C:\Users\Admin\Documents\Second Brain\Ω\FILES\Transcripts\Anh Tuấn Anh\_work\lab_app\app.py` |
| WAF | ModSecurity v3 with OWASP CRS (same as your thesis Ch. III.1.3) | Docker image `secureteam crs-httpd` or local ModSecurity install |
| WAF rule mode | `SecRuleEngine On`, CRS in `OWASP` paranoia level 1, anomaly threshold 5 | Matches your thesis config (Bảng 3.4) |
| Traffic generator | Python script that sends (a) benign requests, (b) your 1,480 test-set SQLi payloads from `TEST_SET.csv`, (c) the 4,585 improved-SeqGAN-generated payloads — at controlled RPS (100, 500, 1000) | `C:\...\Anh Tuấn Anh\_work\traffic_gen\send_payloads.py` |
| Logging | WAF audit log → JSON lines with timestamp, source IP, action (ALLOW/BLOCK), matched rule ID, elapsed (ms) | Parse into `C:\...\Anh Tuấn Anh\_work\lab_results\baseline_audit.jsonl` |

Deliverable: A self-contained lab directory under `_work\lab_01_baseline` that reproduces the WAF behavior described in your thesis Ch. III.4 (WAF campaign).

---

## 2. Baseline Measurement (WAF only — prove the problem)

| Metric | How to measure | Target |
|---|---|---|
| Avg request latency (no AI) | `time curl` through WAF for 500 requests, log timestamp in/out of WAF | Record p50 / p95 / p99 |
| Throughput ceiling | Send at increasing RPS until WAF drops packets | Document max sustainable RPS |
| False-positive rate on benign traffic | 20 benign queries, count BLOCKED | Must be < 5% |
| Recall on your test-set SQLi | 1,480 payloads, count caught vs missed | Document baseline (senior will challenge low recall) |

This is where Anh Tuấn Anh says "em phải biết luồng nó như thế nào" — you must show him the raw numbers BEFORE any AI is added.

---

## 3. AI Insertion Point Design (prove feasibility)

Two architectures — you'll build the lightweight one first to address his latency concern:

### Architecture A — AI as pre-filter (lightweight, low latency)
- **Insertion point:** WAF → AI-filter → WAF-rules
- **AI model:** A lightweight n-gram + TF-IDF + Logistic Regression classifier trained on your **improved SeqGAN output** + real payloads. (Trained offline, takes ~5ms to score per request.)
- **Logic:** If AI says "benign" → fast-path, skip deep rule inspection. If AI says "suspicious" → pass to full CRS ruleset.
- **Goal latency:** < 7ms added per request (Anh Tuấn Anh asked "bao lâu một request")

### Architecture B — AI + WAF ensemble (full, higher latency)
- **Insertion point:** WAF rules AND AI model run in parallel (or cascade)
- **Decision:** BLOCK if either flags as malicious
- **Goal:** Higher recall, accept higher latency

You'll start with **Architecture A**. This directly answers his question: "nếu tất cả cho con AI thì nó sẽ bị vấn đề gì về tải" — running AI on EVERY request is too slow, so you filter.

---

## 4. AI Model Training (use your thesis + OCR'd papers)

- **Real data:** Your 1,480 SQLi test payloads + 3,900 benign (from thesis Ch. III.1.1)
- **Synthetic data:** 25,000 payloads from your **improved SeqGAN** (Ch. II.4 — with SQL-aware tokenizer, 160-token context, structural reward)
- **Cross-paper techniques:**
  - From `AdvSQLi` paper: hierarchical tree transformations (for data augmentation variety)
  - From `WAF-A-MoLE` paper: adversarial payload generation (to harden the AI model)
- **Model:** Lightweight sklearn TF-IDF (3-5 grams) + LogisticRegression or LightGBM
- **Output:** `C:\...\Anh Tuấn Anh\_work\model\waf_ai_model.joblib`

---

## 5. Proof-of-Fact Implementation (make it live)

**Goal:** A single Python script that intercepts, AI-scans, and routes HTTP requests in the lab.

```
lab_01_baseline/
├── app.py                       # Vulnerable web app
├── modsec_config/               # WAF rules
├── waf_ai_filter.py             # <-- THE PROOF: AI insertion proxy
├── traffic_gen/
│   └── send_payloads.py
├── model/
│   └── waf_ai_model.joblib
└── lab_results/
    ├── baseline_audit.jsonl
    ├── ai_inserted_audit.jsonl
    └── comparison_report.md
```

`waf_ai_filter.py` is a tiny HTTP proxy (using `mitmproxy` or raw Python socket):
1. Receives request → runs AI model (2-5ms) → returns verdict
2. If AI verdict = "BLOCK" → intercept, log, return 403
3. If AI verdict = "BENIGN" → forward to ModSecurity (which may still block)
4. Measures end-to-end latency per request and writes to audit log

---

## 6. Evaluation Matrix (prove it works — against senior's doubts)

Run the traffic generator at 100/500/1000 RPS for each condition:

| Condition | Latency (p95) | Throughput | SQLi Recall | FP Rate (benign) |
|---|---|---|---|---|
| Baseline (WAF only) | Measure | Measure | Measure | Measure |
| AI pre-filter + WAF | Measure | Measure | Measure | Measure |

Key questions the senior will ask (from transcript):
- "Bao lâu một request?" → Show latency per request under load
- "Nó xử lý được dữ liệu như thế?" → Show throughput at 1000 RPS
- "Có thật sự cần thiết ngoài đời doanh nghiệp không?" → Show FP reduction + recall gain vs pure-rules

---

## 7. Next Steps (what to do now)

Phase 1 (this week):
1. Set up lab: Flask app + ModSecurity Docker container + traffic generator
2. Run baseline measurements at 100 RPS
3. Train the lightweight AI model from your SeqGAN output
4. Run AI-inserted version, compare latency/throughput/recall

Phase 2 (present to senior):
1. Show him the comparison table
2. Show him: "At 1000 RPS, latency is X ms (vs Y ms baseline), recall improved by Z%, false positives reduced by W%"
3. Answer his "khác gì payload có sẵn trên mạng" challenge: show the structural diversity metrics from your improved SeqGAN

---

## Key Files Already Available

- `voice-018_TRANSCRIPT.md` + `voice-018_KNOWLEDGE.md` — senior's exact words (see N1/N2/N3)
- `De_an_thac_si_Pham_Do_Anh_Minh_2026_da_sua(1).docx` — your full thesis with SeqGAN improvements (Ch. II.4, II.5)
- `C:\...\OCR PDF\SeqGAN_*.md` — original SeqGAN paper (architecture reference)
- `C:\...\OCR PDF\AdvSQLi_*.md` — adversarial transformation techniques
- `C:\...\OCR PDF\WAF-A-MoLE_*.md` — ML-based WAF attack generation
- `C:\...\OCR PDF\ModSec-Learn_preprint.md` — ModSecurity + ML integration reference
