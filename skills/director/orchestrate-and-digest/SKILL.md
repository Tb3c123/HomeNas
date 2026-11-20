---
name: orchestrate-and-digest
description: Director skill for unread Kanboard digest, task routing across departments, and token budget shielding.
---

# Director: Orchestrate & Unread Digest Skill

## 1. Session Start (Unread Digest)
1. Run `python3 -m shared.tools.kanboard_client.cli digest --unread`.
2. Display the output directly in `agy` UI (1 line per updated/completed/alert task, or `[ℹ️ IDLE] Không có thông báo/task mới.`).

## 2. Task Decomposition & Routing
- Never read raw logs or execute heavy system commands in `director`.
- Decompose PO requests into concise Kanboard cards (`<= 3 lines` description) and assign to:
  - `NAS Ops` (`dept-nas-ops`)
  - `Media & Download` (`dept-media`)
  - `Dev Studio` (`dept-dev`)
- Tag independent tasks with `fire-and-forget` and destructive/risky tasks with `needs-approval`.
