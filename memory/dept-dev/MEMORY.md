# Tier 2 Memory: `dept-dev` (Max 100 Lines)

## Pinned Facts
- [PINNED] Full 11 Micro-Agent Product Team (`dev-pm-lead`, `dev-ba`, `dev-ux-ui`, `dev-architect`, `dev-backend`, `dev-frontend`, `dev-refactor`, `dev-qa-tester`, `dev-security-reviewer`, `dev-devops`, `dev-docs-curator`).
- [PINNED] Strict project-wide `<= 150 lines/file` cap enforced by `shared/tools/guardrails/pre_tool_guard.py`.
- [PINNED] Inter-agent ping-pong capped at `MAX_RETRY_LOOPS=2`; all test/lint caches must use `/tmp` (RAM).

## Learned Observations
- [2026-11-19] Avoid naming local packages `platform` to prevent shadowing Python stdlib `platform`; place shared tools under `shared/tools/` and `tools/`.
- [2026-11-22] Giữ nguyên mô hình điều phối v1.6.1 hiện tại (không chế thêm cơ chế Handshake); chờ Google Antigravity mở chính thức tính năng Multi-Tab Handshake / Peer-Tab Wakeup trong UI mới phát triển tiếp.
