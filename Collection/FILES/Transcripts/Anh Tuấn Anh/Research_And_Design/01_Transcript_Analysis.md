# Research Insights: Transcript Analysis (Thầy Lâm, Mentor, Anh Tuấn Anh)

## 1. Core Critiques of Current SeqGAN / AI Approach
* **Reward Hacking:** Generators exploit the discriminator instead of learning SQLi semantics. Models converge to identical ~99% metrics, indicating mode collapse and dataset-level overfitting.
* **HTTP 200 ≠ Exploitation:** A successful WAF bypass (200 OK) does not mean the payload actually works; without a live backend DB, 200 can just mean noise or benign traffic.
* **Marginal Value:** Public SQLi payloads are plentiful. Proving the GAN's value requires demonstrating bypasses of modern enterprise WAFs using *new* payloads that don't exist in public feeds.
* **Latency Infeasibility:** Inline AI insertion (100–1000 RPS) is unfeasible without significant architectural engineering (async/pre-filtering).
* **Purpose Ambiguity:** The fundamental question (GAN for *detection* vs. *generation*) remains unresolved, causing evaluation ambiguity.

## 2. Conceptual Insights: SQLi vs. AI
* **Non-Monolithic Structure:** Boolean/Error-based injections are syntactically simpler than Union/Time-based injections, which require DB-dialect knowledge and strict grammar.
* **Tokenization Failures:** Character-level tokenization destroys SQL semantics. SQL-aware tokenization (keywords, operators, delimiters as units) is required.
* **Hybrid Reward Engineering:** A 100% Discriminator-based reward is fatal. Needs ~70% Discriminator + ~30% structural syntax validator (e.g., `sqlparse`).
* **Context Windows:** Must expand from ~20 to 160+ tokens to learn complex multi-clause SQLi syntax.
* **Family-Stratified Training:** Train separate generators (Boolean, Error, Union, Time) to avoid average-based performance.

## 3. Data & Validation Gaps
* **Noise Filtering:** Raw CVE datasets are largely noise; require filtering by interquartile length ranges.
* **Independent Evaluation:** Use held-out families (unseen during training) for validation.
* **Production Integration:** Recommend a two-stage pipeline: fast rule-based WAF + offline/asynchronous SeqGAN-augmented classifier.
