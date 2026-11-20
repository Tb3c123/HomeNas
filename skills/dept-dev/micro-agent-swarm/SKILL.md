---
name: micro-agent-swarm
description: Orchestrate the 11 Micro-Agents in dept-dev with Design Patterns, <=150 line cap, max 2 retry loops, and direct-fetch skills.
---

# Dev Studio: 11 Micro-Agent Swarm & Engineering Discipline

## 1. On-Demand Micro-Agent Roster (Invoke Only Needed Roles)
- **Product & Design:** `dev-pm-lead`, `dev-ba`, `dev-ux-ui`
- **Arch & Engineering:** `dev-architect`, `dev-backend`, `dev-frontend`, `dev-refactor`
- **QA, Security & Delivery:** `dev-qa-tester`, `dev-security-reviewer`, `dev-devops`, `dev-docs-curator`

## 2. Inter-Agent Handoff & Quota Guardrails
- Communicate via compact Contract Files (`<= 60 lines`) and structured 3-5 line messages (`STATUS | FILE | ACTION`).
- **Max Retry Loops:** `MAX_RETRY_LOOPS = 2` between Coder and QA/Reviewer. If still failing after 2 loops, mark card `blocked` on Kanboard and alert PO.
- **Line-Cap Law:** Every file in the project MUST be `<= 150 lines` (verified via `python3 shared/tools/guardrails/pre_tool_guard.py --audit-repo .`).
- **Low-Wear CI:** Run all tests and linters with `/tmp` RAM caches (`PYTEST_CACHE_DIR=/tmp/.pytest_cache`).
