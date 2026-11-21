---
name: event-sourcing-architect
description: Design append-only event logs, CQRS read/write separation, idempotent projections, and replayable audit trails.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Event Sourcing & CQRS Architect

## Use This Skill When
- Building audit-heavy systems, state machines, activity feeds, or workflows requiring full history and replayability.
- Separating high-write command models from optimized query/read projections.

## Core Rules
1. **Immutable Past-Tense Events:** Store facts as append-only events (`TaskCreated`, `ThermalPaused`) with schema `version`, `timestamp`, and `correlation_id`.
2. **Command Validation First:** Validate invariants against current aggregate state before appending new events; never mutate or delete past events.
3. **Idempotent Projections:** Build read views purely from event streams so projections can be rebuilt from scratch at any time.
4. **Snapshots for Long Streams:** Snapshot aggregate state periodically when event counts grow large to keep load times bounded.
5. **Upcasting Schema Evolution:** Handle old event versions via deterministic upcasters during reads instead of rewriting history.
