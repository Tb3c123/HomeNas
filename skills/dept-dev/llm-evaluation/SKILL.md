---
name: llm-evaluation
description: Design automated LLM evaluation suites using golden datasets, deterministic assertions, LLM-as-judge rubrics, and latency/cost regression gates.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# LLM Evaluation & Regression Testing

## Use This Skill When
- Comparing models, validating prompt/RAG changes, or gating AI feature releases in CI.

## Evaluation Discipline
1. **Golden Dataset:** Curate 20-100 representative cases covering happy paths, edge cases, adversarial/injection inputs, and real production failures.
2. **Layered Graders (Cheap -> Expensive):**
   - Layer 1 (Deterministic): JSON schema validity, required fields, regex/keyword/tool-call assertions.
   - Layer 2 (Reference-Based): Exact match, F1, or semantic similarity against expected outputs.
   - Layer 3 (LLM-as-Judge): Explicit binary/1-5 rubric with concrete criteria (groundedness, completeness, safety).
3. **Track 3 Axes Together:** Never evaluate quality alone — log **Accuracy**, **Latency (p95)**, and **Token Cost** side by side.
4. **Regression Gate:** Block prompt/model swaps that drop pass rate on critical cases or silently double token cost.
