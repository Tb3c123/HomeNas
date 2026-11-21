---
name: error-handling-patterns
description: Design resilient error hierarchies, bounded retries with backoff, fail-fast validation, and actionable user/operator error messages.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Error Handling Patterns

## Use This Skill When
- Designing exception/Result types, external API/CLI wrappers, background workers, or user-facing error states.

## Core Resilience Rules
1. **Distinguish Operational vs. Programmer Errors:** Handle expected operational failures (network timeout, 429, missing file) gracefully; fail fast on invariant/config bugs.
2. **Typed & Contextual Errors:** Wrap low-level errors with domain context (`operation`, `target_id`, `retryable`) while preserving the original cause chain.
3. **Bounded Retries Only for Transient Faults:** Retry only idempotent calls on transient errors (429/502/503/timeout) with capped exponential backoff + jitter — never retry 400/401/403/404 or infinite loops.
4. **Never Swallow Exceptions Silently:** Either handle with explicit fallback, log with structured context, or re-raise; empty `catch {}` / `except: pass` hides root causes.
5. **Safe User Messages:** Show clear, actionable guidance to users while logging diagnostic details internally (never expose secrets or raw stack traces externally).
