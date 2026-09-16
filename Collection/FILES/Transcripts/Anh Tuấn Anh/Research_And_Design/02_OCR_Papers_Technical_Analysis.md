# Technical Analysis: OCR Papers (AdvSQLi, WAF-A-MoLE, ModSec-AdvLearn, SeqGAN)

## 1. Limitations of Vanilla SeqGAN
* **Gradient Discontinuity:** Discrete token spaces prevent direct backpropagation; REINFORCE policy gradients suffer from high-variance MC rollouts that generate invalid SQL strings.
* **Sparse Rewards:** Terminal-only discriminator feedback provides no step-level structural credit assignment for syntax errors.
* **No Semantic Preservation:** SeqGAN optimizes purely for fooling the adversary, leading to broken syntax or semantically invalid payloads.

## 2. Advanced Architectural Solutions
* **Hierarchical AST + Module Locking (AdvSQLi):**
  - Payload = `[Left Boundary] + [Query Core] + [Right Boundary]`
  - Boundaries are locked during generation; Query Core is converted into an Abstract Syntax Tree (AST).
* **Context-Free Grammar (CFG) & Weighted Selection:**
  - Mutations governed by CFG production rules $G = (S, V, \Sigma, R)$ (Tautology rewriting, DML substitution, integer encoding, whitespace/comment insertion).
  - Exponential decay rate $D = 0.5$ (`Weight(e) = D^C[e]`) to prevent infinite recursive rule expansion.
* **Monte Carlo Tree Search (MCTS) over REINFORCE:**
  - Replaces stochastic rollouts with UCB1 tree search (`UCB1(v') = Q(v') + c * sqrt(2 ln N(v) / N(v'))`) for structured AST mutation exploration.
* **Sandbox Execution Oracles & Hybrid Rewards:**
  - $R_{\text{total}} = w_1 \cdot R_{\text{WAF}} + w_2 \cdot R_{\text{Exec}} + w_3 \cdot R_{\text{Div}}$
  - $R_{\text{Exec}}$ validates payload against an isolated sandbox DBMS (MySQL/PostgreSQL) to guarantee Validity of Generated Payloads (VGP = 1.0).
* **Adversarial Retraining (ModSec-AdvLearn):**
  - $\ell_1 / \ell_\infty$-regularized linear surrogate discriminators to prevent reward saturation.
