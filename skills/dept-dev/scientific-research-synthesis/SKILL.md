---
name: scientific-research-synthesis
description: Conduct rigorous literature synthesis, evidence grading, falsifiable hypothesis formulation, and clear separation of facts vs. assumptions.
metadata:
  model: inherit
  source: K-Dense-AI/scientific-agent-skills (MIT)
---

# Scientific Research Synthesis

## Use This Skill When
- Reviewing papers, technical literature, or benchmarks to guide engineering or research decisions.
- Formulating testable hypotheses before running experiments or building prototypes.
- Synthesizing conflicting findings across multiple sources into an evidence-backed brief.

## Core Methodology
1. **Explicit Scope & Search Criteria:** Define the exact research question, inclusion/exclusion criteria, time window, and primary venues (peer-reviewed journals, top conferences, authoritative preprints).
2. **Primary Sources Over Secondary Summaries:** Trace claims back to original papers, proofs, datasets, or reproducible codebases. Never fabricate citations, DOIs, or benchmark numbers—mark unverified claims as `[UNVERIFIED]`.
3. **Fact vs. Assumption Separation:** Clearly label:
   - **Verified Evidence:** Direct results with dataset, metric, and sample size/conditions.
   - **Assumptions / Extrapolations:** Conditions assumed to hold in our target domain.
   - **Contradictions & Gaps:** Where studies disagree or fail to generalize.
4. **Evidence Matrix:** Compare competing methods across consistent axes (assumptions, asymptotic complexity, empirical accuracy, failure modes, compute cost).
5. **Falsifiable Hypotheses:** End synthesis with concrete hypotheses (`If we change X under condition Y, metric Z will improve by >= delta; falsified if ...`).

## Delivery Checklist
- Provide structured synthesis with inline source citations and explicit limitations.
- Highlight strongest counter-evidence and boundary conditions where methods break down.
- Output 1–3 prioritized, falsifiable next hypotheses ready for experimentation.
