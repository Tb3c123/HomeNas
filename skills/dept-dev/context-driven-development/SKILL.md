---
name: context-driven-development
description: Break product goals into structured specs, tracks, and actionable tasks while keeping project context synchronized across all dev micro-agents.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Context-Driven Development (Spec -> Track -> Task)

## Use This Skill When
- Starting a greenfield project or onboarding onto an existing (brownfield) codebase.
- Breaking a high-level PO goal into verifiable specs, implementation tracks, and Kanboard tasks.
- Keeping `AGENTS.md`, `docs/`, and `memory/MEMORY.md` aligned as requirements evolve.

## Core Philosophy
1. **Context as Managed Artifact:** Architecture, tech stack, and constraints live in versioned Markdown docs, never only in chat history.
2. **Plan Before Implement:** Never write production code before clarifying scope, acceptance criteria, and edge cases.
3. **Single Source of Truth:** Every feature track references one spec and one task checklist; update docs when code changes behavior.

## Standard Workflow
1. **Setup Context:** Capture product vision, constraints, and tech stack in `docs/` and `project.yaml`.
2. **Create Track:** For each feature or bugfix, define:
   - `Goal` (1-2 sentences)
   - `Acceptance Criteria` (testable checkboxes)
   - `Out of Scope` (explicit boundaries to prevent scope creep)
3. **Decompose Tasks:** Split into small, independently testable increments (each touching minimal files, all `<= 150 lines/file`).
4. **Execute & Verify:** Follow Red-Green-Refactor, run tests, and update task status + changelog.
5. **Sync Learnings:** Record durable architecture decisions (ADR) and new lessons via `memory_manager`.

## Greenfield vs. Brownfield Rules
- **Greenfield:** Lock vision, constraints, and folder structure first; scaffold minimal vertical slice early.
- **Brownfield:** Inspect existing code, tests, and conventions first; match existing style and avoid unnecessary rewrites.
