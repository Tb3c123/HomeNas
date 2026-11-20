# Changelog Archive — Design Phases (`v0.1.0` → `v1.0.0-design-complete`)

## [v1.0.0-design-complete] - 2026-11-19 *(Phase 4 Design Complete)*
### Added
- `docs/09-dev-handoff-and-roadmap.md`: Checklist Pre-Flight và lộ trình thực thi 5 Sprint kèm tiêu chí nghiệm thu (DoD).
- `README.md`: Tổng mục lục điều hướng toàn bộ kiến trúc và tài liệu dự án HomeNas.

## [v0.3.5] - 2026-11-19 *(Phase 3 Complete — tag `v0.3.5-phase3`)*
### Added
- `docs/08-edge-cases-and-guardrails.md`: Hoàn thiện xử lý trạng thái rỗng/đang tải, chịu lỗi phần cứng Morefine N6/Acasis, chống hủy nhầm torrent khi HDD nóng và chốt chặn Quota/ToS/Line-Cap.

## [v0.3.4] - 2026-11-19
### Added
- `docs/departments/03-dept-dev.md`: Thiết kế chuyên sâu Phòng 3 (`dept-dev`) với đội hình 11 Micro-Agents, giao thức tự trao đổi nội bộ (tối đa 2 vòng lặp), luật trần cứng ≤ 150 dòng toàn dự án và kho Agent Skills tải lẻ trực tiếp.

## [v0.3.3] - 2026-11-19
### Added
- `docs/departments/02-dept-media.md`: Mirror 1:1 trên `disk1`/`disk2` (bỏ `4K_UHD`), cân bằng dung lượng, dồn trọn Season phim bộ về 1 ổ, Sub Việt + 2K/4K linh hoạt (TV 1080p lọc TVRip), tải tuần tự 1-phim-1-lượt, canh 20–30% ETA.
### Changed
- `docs/departments/01-dept-nas-ops.md`: Đồng bộ 2 ổ 10TB thực tế (`sda` WD Gold + `sdb` WD Purple Pro) và khóa bảo vệ `adguard-home`, `portainer`, `antigravity-cli`.

## [v0.3.2] - 2026-11-19
### Added
- `docs/departments/01-dept-nas-ops.md`: Thiết kế Phòng 1 (`dept-nas-ops`) cho Morefine N6, `homenas-watchdog` (0-token, lưu RAM flush 23:55, Telegram khẩn cấp) và tích hợp Antigravity `/schedule`, `hooks.json`.

## [v0.3.1] - 2026-11-19
### Added
- `docs/07-system-design-blueprint.md`: Bản thiết kế tổng thể 4 lớp và mô hình bảo mật 4 lớp.

## [v0.3.0] - 2026-11-18
### Added
- `docs/06-technical-specs.md`: Đặc tả Docker Stack (`kanboard`, `docker-proxy`, `agy-runtime`), schema `project.yaml` và `kanboard-client`.

## [v0.2.1] - 2026-11-18 *(Phase 2 Complete — tag `v0.2.1-phase2`)*
### Added
- `docs/05-user-flows.md`: Đặc tả 3 luồng vận hành cốt lõi kèm Inline Compact Receipt & Director Unread Digest.

## [v0.2.0] - 2026-11-18
### Added
- `docs/04-information-architecture.md`: Kiến trúc 2 tầng Shared Platform Infra & Plug-and-Play Multi-Project Workspaces.

## [v0.1.2] - 2026-11-18 *(Phase 1 Complete — tag `v0.1.2-phase1`)*
### Added
- `docs/03-learning-and-token-budget.md`: Chiến lược tự học Hermes 3 tầng & 5 nguyên tắc kiểm soát quota token.
### Changed
- Chuyển Kanban sang **Kanboard** (Docker/SQLite, MIT, JSON-RPC API).

## [v0.1.1] - 2026-11-18
### Added
- `docs/02-mvp-and-departments.md`: Chốt phạm vi MVP và 1 Main Chat + 3 Sub-Chats.

## [v0.1.0] - 2026-11-18
### Added
- `docs/01-vision-and-constraints.md`: Tầm nhìn sản phẩm, ràng buộc tuân thủ ToS Antigravity (Section 6) & kiểm soát quota token.
