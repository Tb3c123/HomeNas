---
name: architecture-patterns
description: Apply Clean Architecture, Hexagonal Architecture, and Domain-Driven Design to keep systems modular, testable, decoupled, and maintainable.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Architecture Patterns (Clean, Hexagonal & DDD)

## Use This Skill When
- Designing system boundaries, module structure, and data flow for a new service or app.
- Decoupling business logic from frameworks, databases, CLIs, or external APIs.
- Splitting monolithic files/modules into focused units (`<= 150 lines/file`).

## Core Dependency Rules
1. **Dependency Inversion:** High-level domain/business logic never imports low-level infrastructure (DB, HTTP, filesystem, subprocess). Depend on interfaces/ports instead.
2. **Clean Architecture Layers:**
   - `Domain / Entities`: Pure data structures and invariants (zero framework imports).
   - `Use Cases / Services`: Application orchestration depending only on ports.
   - `Adapters / Infrastructure`: Concrete DB, HTTP, CLI, or filesystem implementations.
3. **Hexagonal (Ports & Adapters):** External inputs (CLI, HTTP, UI) enter via Driving Ports; external side effects (DB, API, Docker) exit via Driven Adapters — making unit tests fast with in-memory fakes.
4. **Domain-Driven Boundaries:** Group code by cohesive feature/bounded context rather than giant catch-all `utils.py` files; keep explicit DTOs at boundaries.

## Verification Checklist
- Can core business logic be unit-tested in milliseconds without network, Docker, or real DB?
- Does each module have one clear responsibility and stay well under 150 lines?
- Are side effects isolated at the edges with explicit error handling?
