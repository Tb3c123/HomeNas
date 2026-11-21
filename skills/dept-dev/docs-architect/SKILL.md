---
name: docs-architect
description: Create clear, concise technical documentation, Architecture Decision Records (ADRs), Mermaid diagrams, runbooks, and structured changelogs.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Docs Architect (Technical Specs, ADRs & Diagrams)

## Use This Skill When
- Authoring or updating `README.md`, architecture blueprints, API docs, operational runbooks, ADRs, or `CHANGELOG.md`.
- Visualizing system components, sequence flows, or state machines with Mermaid diagrams.

## Documentation Standards
1. **Audience-First & Scannable:** Lead with executive summary/purpose, use tables and bullet lists, avoid walls of prose, and keep every doc file `<= 150 lines` (split by topic when larger).
2. **Accurate to Code:** Verify file paths, CLI flags, env vars, and ports directly against the codebase — never document guessed behavior.
3. **Architecture Decision Records (ADR):** Capture `Context -> Decision -> Trade-offs / Consequences` concisely so future agents do not repeat rejected approaches.
4. **Mermaid Diagrams:** Use clean `flowchart`, `sequenceDiagram`, or `stateDiagram-v2`; quote node labels containing parentheses or special characters.
5. **Changelog Discipline:** Follow Keep a Changelog (`Added`, `Changed`, `Fixed`, `Security`) tied to semantic tags (`vX.Y.Z`).

## Maintenance Checklist
- Every new feature, env var, or breaking change updates its corresponding doc and `CHANGELOG.md` in the same commit.
- Archive old changelog entries into `docs/` before `CHANGELOG.md` approaches the 150-line ceiling.
