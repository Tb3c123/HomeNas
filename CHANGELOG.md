# Changelog

Tất cả thay đổi quan trọng của dự án **HomeNas (Smart Home AI Orchestrator)** được ghi nhận tại đây theo chuẩn [Conventional Commits](https://www.conventionalcommits.org/).

## [v0.3.2] - 2026-11-19
### Added
- `docs/departments/01-dept-nas-ops.md`: Thiết kế chuyên sâu Phòng 1 (`dept-nas-ops`) cho phần cứng Morefine N6 (Intel N200, 16GB RAM, 256GB SSD, 20TB HDD Acasis), container `homenas-watchdog` (0-token, RAM-only, Telegram emergency auto-stop), và tích hợp `agy` native (`/automation` qua Remote Control, `/schedule`, `hooks.json`).

## [v0.3.1] - 2026-11-19
### Added
- `docs/07-system-design-blueprint.md`: Bản thiết kế tổng thể 4 lớp (Control, AI & Orchestration, State & Automation, Target & Security), hợp đồng liên kết và mô hình bảo mật 4 lớp.

## [v0.3.0] - 2026-11-18
### Added
- `docs/06-technical-specs.md`: Đặc tả hạ tầng Docker Stack (`kanboard`, `docker-proxy`, `agy-runtime`), schema cấu hình plug-in `project.yaml` và hợp đồng 4 module cho `kanboard-client` (JSON-RPC).

## [v0.2.1] - 2026-11-18 *(Phase 2 Complete — tag `v0.2.1-phase2`)*
### Added
- `docs/05-user-flows.md`: Đặc tả 3 luồng vận hành cốt lõi (Kanboard-as-Message-Bus, Fire-and-Forget kèm **Inline Compact Receipt** & **Director Unread Digest** trong `agy` UI, và vòng lặp tự học Hermes có duyệt Skill).

## [v0.2.0] - 2026-11-18
### Added
- `docs/04-information-architecture.md`: Thiết kế kiến trúc 2 tầng tách biệt **Shared Platform Infra** (Docker `agy` + `kanboard` + `shared/`) và **Plug-and-Play Multi-Project Workspaces** (qua `project.yaml`), kèm Sitemap Kanboard (1 Project = 1 Dự án, phân luồng theo Swimlanes).

## [v0.1.2] - 2026-11-18 *(Phase 1 Complete — tag `v0.1.2-phase1`)*
### Added
- `docs/03-learning-and-token-budget.md`: Chốt chiến lược tự học 3 tầng (Hermes pattern + Memory Poisoning Guard) và 5 nguyên tắc kiểm soát quota token (Fire-and-Forget, Stateless Session, Zero-Noise Output...).
### Changed
- Chuyển Kanban board từ Vikunja sang **Kanboard** (Docker/SQLite, MIT, JSON-RPC API) và đồng bộ lại toàn bộ `docs/01-vision-and-constraints.md`, `docs/02-mvp-and-departments.md`.

## [v0.1.1] - 2026-11-18
### Added
- `docs/02-mvp-and-departments.md`: Chốt phạm vi MVP (In-Scope / Out-of-Scope) và cấu trúc 1 Main Chat (`director`) + 3 Sub-Chats (`dept-nas-ops`, `dept-media`, `dept-dev`); dời `dept-smarthome` sang v2+.

## [v0.1.0] - 2026-11-18
### Added
- `docs/01-vision-and-constraints.md`: Chốt tầm nhìn sản phẩm, đối tượng sử dụng, kiến trúc Multi-Session cấp cao, ràng buộc tuân thủ ToS Antigravity (Section 6), kiểm soát quota token và lựa chọn **Vikunja** làm Kanban open-source.
