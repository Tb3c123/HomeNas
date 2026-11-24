---
name: llm-finetuning-post-training
description: Plan and execute LLM fine-tuning (SFT, LoRA/QLoRA) and preference post-training (DPO/GRPO) with clean datasets and regression benchmarks.
metadata:
  model: inherit
  source: Orchestra-Research/AI-Research-SKILLs (MIT)
---

# LLM Fine-Tuning & Post-Training

## Use This Skill When
- Deciding whether a task truly needs fine-tuning vs. prompting/RAG, and executing SFT/LoRA/QLoRA.
- Aligning model behavior with preference optimization (DPO, ORPO, GRPO) or domain-specific formatting.
- Auditing dataset quality, chat template consistency, or catastrophic forgetting.

## Core Principles
1. **Justify Fine-Tuning First:** Exhaust prompt engineering, few-shot examples, and RAG before fine-tuning. Fine-tune primarily for consistent style/schema adherence, specialized domain reasoning, or distilling a large model into a fast small model.
2. **Data Quality Beats Volume:**
   - Deduplicate examples (exact + near-duplicate), strip contamination from eval sets, and audit 50+ random samples by hand.
   - Enforce **exact chat template & special token parity** between training and inference (mask loss on prompt tokens so loss computes on assistant completions only).
3. **Parameter-Efficient Defaults (LoRA / QLoRA):**
   - Apply LoRA to attention + MLP linear projections (`q/k/v/o/gate/up/down`), start with moderate rank (`r=16–32`, `alpha=2*r`), conservative LR (`1e-4–2e-4` for LoRA, `1e-5` for full SFT), and monitor eval loss closely to avoid overfitting after 1–3 epochs.
4. **Preference Alignment (DPO / GRPO):** Ensure chosen vs. rejected pairs have clear, verifiable quality separation; keep KL/beta regularization tuned to prevent reward hacking or verbosity bloat.
5. **Guard Against Catastrophic Forgetting:** Evaluate every checkpoint on **both** target-task benchmarks and a general capability/safety regression suite before promotion.

## Delivery Checklist
- Document base model ID, dataset hash/counts, chat template, hyperparameters, and before/after eval table.
- Verify merged/adapter weights load cleanly in the target inference runtime.
