---
name: microservices-patterns
description: Design resilient distributed services with clear bounded contexts, circuit breakers, async messaging, and zero shared-database coupling.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Microservices Patterns

## Use This Skill When
- Decomposing a system into independently deployable services or integrating multiple processes/daemons.
- Adding fault tolerance (timeouts, retries, circuit breakers, bulkheads) across network calls.

## Core Principles
1. **Database per Service:** Never share internal tables across services; communicate strictly via versioned APIs or domain events.
2. **Design for Failure:** Every network call needs explicit connect/read timeouts, bounded exponential backoff with jitter, and circuit breaking.
3. **Async Over Sync Chains:** Prefer event queues/outbox pattern for non-blocking side effects to prevent cascading failures.
4. **Idempotent Consumers:** Every message handler must safely tolerate duplicate delivery using idempotency keys.
5. **Avoid Premature Split:** Default to a modular monolith until team scale, runtime isolation, or scaling bottlenecks justify service boundaries.
