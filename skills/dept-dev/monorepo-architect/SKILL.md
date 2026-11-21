---
name: monorepo-architect
description: Structure multi-package repositories with clean dependency graphs, shared internal libraries, and fast incremental builds/tests.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Monorepo Architect

## Use This Skill When
- Managing frontend, backend, CLI, and shared contract packages inside one repository.
- Preventing circular dependencies and keeping CI builds/tests fast as packages grow.

## Core Conventions
1. **Clear Package Boundaries:** Separate `apps/` (deployable units) from `packages/` or `shared/` (reusable libraries/types); apps never import from other apps.
2. **Acyclic Dependency Graph:** Enforce strict one-way imports (`apps -> shared -> core`) with linter/tooling checks to prevent cycles.
3. **Single Version Policy:** Keep shared runtime/dev dependencies aligned across workspaces to avoid duplicate bundle bloat and subtle version mismatches.
4. **Affected-Only CI:** Cache build/test outputs and run lint/test only on affected packages in PRs, with full verification on `main`.
5. **Consistent Scripts:** Standardize `build`, `test`, `lint`, and `typecheck` entrypoints across every package.
