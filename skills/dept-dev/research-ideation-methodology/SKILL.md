---
name: research-ideation-methodology
description: Formulate high-leverage research questions, design controlled experiments and ablations, and guard against validity threats.
metadata:
  model: inherit
  source: Orchestra-Research/AI-Research-SKILLs (MIT)
---

# Research Ideation & Experimental Methodology

## Use This Skill When
- Turning a broad problem into a sharp, novel, and feasible research or R&D agenda.
- Designing experimental protocols, control groups, baselines, and ablation studies.
- Reviewing an experiment plan for confounding variables or weak evaluation criteria.

## Core Principles
1. **Sharp Problem Framing:** Identify the exact bottleneck or failure mode of current SOTA baselines before proposing a new method. Ask: *"Why does the simplest baseline fail here?"*
2. **Strong, Fair Baselines:** Always compare against a well-tuned simple baseline and the strongest relevant published baseline under identical data splits, compute budgets, and preprocessing.
3. **Controlled Ablation Design:** Isolate each proposed component (remove/swap one factor at a time) to prove which mechanism actually drives gains and which adds only complexity.
4. **Threats to Validity Checklist:**
   - **Internal:** Data leakage, hyperparameter over-tuning on test set, cherry-picked random seeds.
   - **External:** Overfitting to one benchmark/domain; test out-of-distribution or stress regimes.
   - **Statistical:** Report mean ± std across `>= 3` seeds (or bootstrap CI) and check effect size, not just p-value.
5. **Kill Criteria Early:** Define upfront what minimal signal on a cheap pilot experiment justifies scaling up vs. pivoting.

## Delivery Checklist
- Document research question, baseline matrix, ablation table, and fixed evaluation protocol before running full sweeps.
- Specify compute/time budget and explicit stop/pivot criteria.
- Record negative results honestly to prevent repeating dead ends.
