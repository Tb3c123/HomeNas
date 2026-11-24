---
name: combinatorial-optimization
description: Formulate and solve LP, MILP, CP-SAT, routing, scheduling, and metaheuristic optimization problems with feasibility and optimality verification.
metadata:
  model: inherit
  source: Operations Research & OR-Tools / SciPy Curated Reference
---

# Combinatorial & Mathematical Optimization

## Use This Skill When
- Solving scheduling, resource allocation, bin packing, routing, portfolio, or assignment problems.
- Formulating Linear Programming (LP), Mixed-Integer Linear Programming (MILP), or Constraint Programming (CP-SAT).
- Applying metaheuristics (Simulated Annealing, Tabu Search, Genetic Algorithms) when exact solvers exceed time budgets.

## Core Methodology
1. **Formal Mathematical Model First:** Explicitly define before coding:
   - **Decision Variables** (continuous, integer, binary) with tight bounds.
   - **Objective Function** (minimize/maximize; handle multi-objective via lexicographic or weighted normalization).
   - **Hard vs. Soft Constraints** (penalize soft violations via slack variables instead of making the model infeasible).
2. **Choose the Right Solver Class:**
   - Pure continuous linear → LP (`scipy.optimize.linprog`, HiGHS).
   - Mixed integer linear → MILP (HiGHS, CBC, Gurobi) with tight Big-M bounds and symmetry-breaking constraints.
   - Complex logical/scheduling constraints (`AllDifferent`, `NoOverlap`, `Circuit`) → CP-SAT (OR-Tools).
   - Massive NP-hard instances needing fast anytime solutions → Constructive heuristic + Local Search / Simulated Annealing.
3. **Tighten Formulations:** Reduce variable count, avoid loose Big-M values (cause numerical instability & weak LP relaxations), and add valid inequalities or symmetry breakers.
4. **Always Set Time & Gap Limits:** Configure explicit `time_limit` and `mip_rel_gap`; handle `OPTIMAL`, `FEASIBLE`, `INFEASIBLE`, and `UNBOUNDED` statuses gracefully.
5. **Independent Feasibility Checker:** Validate every solver output with a separate, simple constraint checker outside the solver.

## Delivery Checklist
- Verify model on tiny hand-solvable instances first, then benchmark scaling and optimality gap.
- Return both solution quality (objective + optimality gap) and solver status cleanly.
