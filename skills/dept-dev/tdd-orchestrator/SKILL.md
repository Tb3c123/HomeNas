---
name: tdd-orchestrator
description: Enforce disciplined Red-Green-Refactor test-driven development, root-cause debugging, and bounded retry loops across dev agents.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# TDD Orchestrator & Systematic Debugging

## Use This Skill When
- Implementing new features or fixing bugs with guaranteed regression coverage.
- Diagnosing failing tests, flaky behavior, or runtime errors without guesswork.

## Red-Green-Refactor Discipline
1. **RED:** Write the smallest failing test that specifies the exact expected behavior or reproduces the bug. Run it and confirm it fails for the right reason.
2. **GREEN:** Write the minimal clean production code needed to pass the test (no speculative over-engineering).
3. **REFACTOR:** Clean up duplication, naming, and module boundaries while keeping all tests green.

## Systematic Root-Cause Debugging
1. **Reproduce Reliably:** Capture exact command, inputs, environment, and full traceback.
2. **Isolate & Hypothesize:** Narrow down the failing layer (input -> logic -> state -> I/O) before editing code.
3. **Fix Cause, Not Symptom:** Never silence exceptions or relax assertions just to make a test green.
4. **Lock Regression:** Add a targeted unit test covering the root cause.

## Guardrails
- Follow the **Testing Pyramid:** Many fast unit tests, focused integration tests, selective E2E tests.
- Run tests with `PYTHONDONTWRITEBYTECODE=1` and `/tmp` caches to avoid SSD wear.
- Respect `MAX_RETRY_LOOPS = 2`: if still failing after 2 structured fix loops, stop and escalate with diagnostic evidence.
