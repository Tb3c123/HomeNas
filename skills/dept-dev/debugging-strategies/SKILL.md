---
name: debugging-strategies
description: Isolate hard bugs rapidly using minimal reproductions, binary search (git bisect), hypothesis testing, and invariant assertions.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Debugging Strategies (Scientific Root-Cause Isolation)

## Use This Skill When
- Investigating intermittent bugs, race conditions, environment-only failures, or regressions across multiple layers.

## 5-Step Scientific Loop
1. **Freeze & Reproduce:** Capture the exact failing input, stack trace, env vars, and a minimal 1-command reproducer.
2. **Bisect the Search Space:** Cut the system in half (input -> boundary -> core -> output, or `git bisect` across commits) to pinpoint the exact failing component or commit.
3. **Form One Falsifiable Hypothesis:** State what you expect a targeted log/assertion/debugger inspection to show before running it — avoid random trial-and-error edits.
4. **Verify Root Cause, Not Symptom:** Confirm why the bug happens under the hood; fix the underlying invariant instead of adding brittle `sleep()` or broad `try/except`.
5. **Prevent Recurrence:** Add a permanent regression test and clean up all temporary debug logs before committing.
