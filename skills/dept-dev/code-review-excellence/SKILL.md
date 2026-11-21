---
name: code-review-excellence
description: Conduct systematic, severity-ranked code reviews and clean refactoring to catch bugs, eliminate tech debt, and keep every file modular and under 150 lines.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Code Review Excellence & Clean Refactoring

## Use This Skill When
- Reviewing pull requests, diffs, or agent-generated patches before merge.
- Refactoring complex functions, removing dead code, or splitting files approaching the 150-line cap.

## Systematic Review Dimensions
1. **Correctness & Edge Cases:** Null/empty inputs, boundary values, race conditions, error paths, resource cleanup.
2. **Security & Guardrails:** No hardcoded secrets, safe subprocess/SQL/HTML handling, proper auth checks.
3. **Modularity & Maintainability:** Single-responsibility functions, clear naming, no duplicated logic, every file `<= 150 lines` (no semicolon packing).
4. **Performance & I/O Hygiene:** Avoid N+1 queries, unbounded loops, unnecessary disk writes, or blocking calls on async event loops.
5. **Test Signal:** Verify tests assert real behavior and regressions, not just mocked tautologies.

## Severity-Ranked Output Format
- **Blocking (Must Fix):** Bugs, security flaws, broken contracts, guardrail violations.
- **Important (Should Fix):** Maintainability risks, missing edge-case tests, unclear abstractions.
- **Minor (Nit/Suggestion):** Naming polish, minor simplification.

## Safe Refactoring Discipline
- Always have passing tests before refactoring; make small behavior-preserving steps and re-run tests after each step.
- Extract cohesive helper modules instead of creating god-classes or deep inheritance trees.
