---
name: academic-paper-writing
description: Structure clear, rigorous research papers and technical reports (IMRaD/ML/Systems) with precise math notation, LaTeX, and honest limitations.
metadata:
  model: inherit
  source: Orchestra-Research/AI-Research-SKILLs (MIT)
---

# Academic Paper & Technical Report Writing

## Use This Skill When
- Drafting research papers, technical whitepapers, RFCs, or experimental reports.
- Structuring Abstract, Introduction, Related Work, Method, Experiments, and Limitations.
- Polishing mathematical notation, theorem statements, figures/tables, and LaTeX formatting.

## Core Structure & Craft
1. **Claim-First Narrative:**
   - **Abstract (4–6 sentences):** Problem → Gap → Key Insight/Method → Quantitative Result → Takeaway.
   - **Introduction:** Motivate with a crisp example/figure, state 2–4 explicit contributions, and map each contribution to its validating section/experiment.
2. **Consistent Mathematical Notation:** Define every symbol on first use (scalars `x`, vectors `\mathbf{x}`, matrices `\mathbf{X}`, sets `\mathcal{S}`), keep notation uniform across text, equations, and figures, and state assumptions before every lemma/theorem.
3. **Self-Contained Figures & Tables:** Captions must explain *what is shown* and *what takeaway the reader should notice* without rereading the body; bold best results and include variance/uncertainty.
4. **Precision Over Hype:** Replace vague superlatives ("dramatically outperforms", "novel paradigm") with exact quantitative deltas, regimes, and statistical bounds.
5. **Honest Limitations & Reproducibility:** Dedicate a clear section to failure modes, compute/memory assumptions, ethical/safety considerations, and exact hyperparameters/code links for reproduction.

## Delivery Checklist
- Verify every claim in the Abstract/Intro is backed by a specific table, figure, or proof in the body.
- Check all citations, cross-references (`\ref`, `\eqref`), and symbol definitions for zero undefined references.
- Ensure the conclusion summarizes findings without introducing unsupported new claims.
