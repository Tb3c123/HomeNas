---
name: autoresearch-experiment-loop
description: Run disciplined autonomous experiment loops (Baseline -> Single-Variable Hypothesis -> Metric Gate -> Keep/Revert) with reproducible logs.
metadata:
  model: inherit
  source: Orchestra-Research/AI-Research-SKILLs (MIT)
---

# Autoresearch Experiment Loop

## Use This Skill When
- Iteratively optimizing a model, algorithm, prompt, or numerical solver against a measurable benchmark.
- Running bounded automated search/tuning cycles where each change must prove empirical improvement.
- Maintaining a clean, reproducible experiment ledger across many iterations.

## Disciplined 5-Step Loop
1. **Lock Baseline & Immutable Eval:** Freeze the validation split, metric script, and random seed first. Record Baseline score (`iter_0`) before editing anything.
2. **Single-Variable Hypothesis:** Change **one coherent idea per iteration** and write a 1-line hypothesis predicting direction and magnitude of metric impact.
3. **Bounded Execution:** Run inside strict time/step/memory budgets (store temp artifacts in `/tmp` to protect SSD). Abort early on NaN, divergence, or constraint breach.
4. **Objective Metric Gate (Keep vs. Revert):**
   - **KEEP** only if primary metric improves beyond noise threshold AND no guardrail metric (latency, memory, validity) regresses.
   - **REVERT** cleanly (`git checkout` / restore state) if flat or worse—never accumulate unverified complexity.
5. **Structured Experiment Ledger:** Append one compact row per run (`iter | hypothesis | metric_before | metric_after | delta | decision | notes`) to prevent repeating failed ideas.

## Guardrails
- Never modify the evaluation script or validation set mid-loop to "make numbers go up".
- Cap consecutive failed iterations (e.g., max 5 without gain) and pause to rethink the representation or problem formulation.
