---
name: agent-orchestration-multi-agent-optimize
description: Optimize multi-agent workflows with isolated contexts, compact file-based handoffs, bounded retry loops, and minimal token overhead.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Multi-Agent Orchestration & Optimization

## Use This Skill When
- Coordinating multiple specialized agents (Planner, Coder, Reviewer, QA) or multi-CLI workspaces.
- Reducing token burn, context drift, or infinite agent ping-pong loops.

## Optimization Rules
1. **Context Isolation:** Give each agent only the files, spec, and memory relevant to its role — never dump entire chat histories across agents.
2. **Compact Handoff Contracts:** Pass state via structured files (`SPEC.md`, `HANDOFF.md`, Kanban tickets) using `STATUS | ARTIFACT | NEXT_ACTION` (`<= 5 lines`).
3. **Bounded Retry Loops:** Enforce hard ceilings (`MAX_RETRY_LOOPS = 2`) between implementer and verifier; escalate to human PO with diagnostic summary on failure.
4. **Parallelize Independent Work Only:** Run independent read/research or isolated Git-worktree tasks in parallel; serialize shared-file edits to avoid merge conflicts.
5. **Human-in-the-Loop Gates:** Require explicit human approval before destructive writes, external deployments, or cross-provider subscription actions.
