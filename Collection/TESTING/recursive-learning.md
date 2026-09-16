# Learning by Teaching and Feynman Technique for AI Agents

## Can an agent improve its own mastery of a skill by generating a curriculum for someone else?

**Yes, research demonstrates this is effective.**

Key findings from academic literature:

1. **Learning by Teaching (LbT) for LLMs**: Recent studies (arXiv:2406.14629, NeurIPS 2024) show that when LLMs generate teaching materials for other models, they improve their own reasoning capabilities. The mechanism works because:
   - Creating teaching materials forces clearer and more accurate logic
   - Feedback from "students" (even other LLMs) provides valuable signals for improvement
   - Teaching weaker models can enhance stronger models through weak-to-strong generalization
   - Diversity in student models improves learning outcomes

2. **Three Levels of LbT Implementation**:
   - **L1**: Observing student feedback (e.g., using student performance to score teacher rationales)
   - **L2**: Learning from feedback (e.g., fine-tuning based on teaching effectiveness scores)
   - **L3**: Iterative learning (refining teaching materials based on multiple rounds of student feedback)

3. **Empirical Results**: 
   - M1 method improved GPT-4o's accuracy on MATH dataset from 87.84% to 96.69%
   - M2 (fine-tuning with LbT scores) outperformed correctness-based DPO
   - M3 showed iterative refinement of in-context examples improved both student and teacher performance

4. **Practical Implementation**: The approach can be implemented via prompting pipelines without requiring model fine-tuning, making it accessible for immediate use.

## Are there existing 'mindsets' or prompts that force an agent to 'explain it like I'm five' (ELI5) to consolidate its own 'State'?

**Yes, several established implementations exist:**

### 1. Feynman Technique Agent Skills
- **evanshlee/feynman-technique** (GitHub): An interactive agent skill that implements the Feynman Technique:
  - Forces users to explain concepts in their own words
  - Identifies exactly ONE gap per turn using a 7-category taxonomy
  - Requires learners to re-explain after identifying gaps
  - Continues until 4/5 mastery criteria are met
  - Includes session logging for review and resumption

### 2. Teach-Back Skills
- **skills.lc/opelpleple/meta-skills/teach-back**: Designed specifically for checking understanding:
  - Activated by phrases like "explain like I'm 5", "ELI5", "do I actually understand this"
  - Drives concepts to "ten-year-old clarity"
  - Hunts for explanation seams where understanding breaks down
  - Flags gaps when explanations become vague or hand-wavy

### 3. Socratic AI Framework
- **aiindigo.com blog**: Combines role definition with teach-back loops:
  - Sets hard constraints: "Forbidden from providing direct answers"
  - Uses targeted questions to guide discovery
  - Implements teach-back: "I will now explain [Concept Y] back to you..."
  - Interrupts when conceptual errors or fuzzy language are detected

### 4. BytesAgain Feynman Technique Explainer
- **bytesagain.com/skill/feynman-technique-explainer**: Structured four-part approach:
  - Plain-language explanation (with forbidden jargon list)
  - Real-world example
  - Comprehension quiz (application-focused questions)
  - Answer evaluation and gap filling

### 5. Metacognitive Prompting Techniques
- **ACL 2026 paper "Beyond Meta-Reasoning"**: Shows metacognitive consolidation improves LLM reasoning:
  - Three-level consolidation: instance-level → batch-level → global-level
  - Self-reflection prompts that guide error analysis
  - Demonstrated improvement on Math-500 and TheoremQA benchmarks

## Key Insights for AI Agent Implementation

### For Curriculum Generation (LbT):
1. **Student Modeling**: Configure appropriate knowledge levels for student agents to maximize feedback quality
2. **Feedback Utilization**: Use student performance as a signal for teacher improvement
3. **Iterative Refinement**: Allow multiple rounds of teaching-feedback-revision cycles
4. **Diversity Benefit**: Teaching multiple diverse students yields better results than single student

### For ELI5/Consolidation Prompts:
1. **Constraint-Based Prompting**: Explicitly forbid jargon and technical terms
2. **Gap Detection**: Implement mechanisms to identify explanation weaknesses
3. **Iterative Loop**: Require re-explanation after gap identification
4. **Mastery Criteria**: Define clear completion conditions (e.g., 4/5 criteria met)
5. **Analogy Requirement**: Mandate concrete, everyday analogies
6. **Session Persistence**: Save progress for resumption and review

Both approaches leverage the **protégé effect** (where teaching enhances the teacher's understanding) and combat the **illusion of explanatory depth** by forcing agents to confront gaps in their knowledge through explanation attempts.

The research confirms that these techniques are not just pedagogical tools but effective mechanisms for AI self-improvement and knowledge consolidation.