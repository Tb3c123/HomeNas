---
name: mathematical-stochastic-modeling
description: Model linear algebra, Markov chains, stochastic matrices, Monte Carlo simulations, and statistical hypothesis tests with numerical stability.
metadata:
  model: inherit
  source: K-Dense-AI/scientific-agent-skills (MIT)
---

# Mathematical & Stochastic Modeling

## Use This Skill When
- Building Markov chain / stochastic matrix analyzers, queuing models, or Monte Carlo simulations.
- Performing symbolic derivations (`SymPy`), eigen/SVD decompositions, or statistical inference.
- Validating mathematical invariants, convergence rates, and uncertainty bounds.

## Core Principles
1. **Verify Mathematical Invariants at Boundaries:**
   - Stochastic matrices: non-negative entries ($P_{ij} \ge 0$) and row/column sums equal to $1$ within strict tolerance (`atol=1e-9`).
   - Check irreducibility, aperiodicity, absorbing states, and spectral radius before assuming a unique stationary distribution $\pi P = \pi$.
2. **Numerically Stable Linear Algebra:**
   - Prefer `np.linalg.solve` / QR / SVD / Schur decompositions over explicit matrix inversion `inv(A)`.
   - Compute probabilities in **log-space** (`logsumexp`) for long chains or products to prevent underflow.
   - Inspect condition number $\kappa(A)$ and warn when ill-conditioned.
3. **Reproducible Stochastic Simulation:**
   - Always use explicit local RNG generators (`np.random.default_rng(seed)`), never global `np.random.seed`.
   - Report Monte Carlo Standard Error ($\text{MCSE} = s/\sqrt{N}$) or bootstrap confidence intervals; use variance reduction (antithetic variates, control variates, stratified sampling) when appropriate.
4. **Statistical Rigor:** Check distributional assumptions, report effect sizes + CIs alongside p-values, and apply multiple-testing correction (Benjamini-Hochberg / Bonferroni) when running many tests.
5. **Symbolic-to-Numeric Verification:** Cross-check closed-form analytical solutions (`SymPy`) against numerical simulations on small cases.

## Delivery Checklist
- Assert domain invariants (non-negativity, probability sum, symmetry/PSD) with clear errors.
- Include deterministic seeded tests verifying known analytical results (e.g., exact stationary vector).
