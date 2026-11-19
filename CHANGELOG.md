# Changelog

Tất cả thay đổi quan trọng của dự án **HomeNas (Smart Home AI Orchestrator)** được ghi nhận tại đây theo chuẩn [Conventional Commits](https://www.conventionalcommits.org/).

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
