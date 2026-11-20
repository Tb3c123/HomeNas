# HomeNas — Smart Home AI Orchestrator (Antigravity CLI + Kanboard + CasaOS)

Hệ thống điều phối và tự động hóa quản trị Home NAS (**Morefine N6 Intel N200, 16GB RAM, 256GB NVMe SSD, 2×10TB HDD Acasis, Debian + CasaOS**) vận hành trên **Antigravity CLI (`agy`)**, tuân thủ tuyệt đối ToS, tối ưu quota token và tích hợp cơ chế tự học Hermes 3 tầng.

## Kiến trúc Cốt lõi
- **2-Layer Multi-Project:** Tách biệt **Shared Platform Infra** (1 container `kanboard` + `docker-proxy` + `homenas-watchdog` + `antigravity-cli`) và **Plug-and-Play Projects** (qua `project.yaml`).
- **Multi-Session Topology:** `1 Main Chat (director)` + `3 Sub-Chats` (`dept-nas-ops`, `dept-media`, `dept-dev` gồm 11 Micro-Agents).
- **0-Token Automation & Guardrails:** Giám sát nhiệt độ/Telegram khẩn cấp, canh tải phim 20–30% ETA, backup Kanboard và chốt chặn `hooks.json` (≤ 150 dòng/file) chạy hoàn toàn 0 token.

## Bản đồ Tài liệu Thiết kế (`docs/`)

| Phase | Tài liệu | Nội dung chính |
| :--- | :--- | :--- |
| **Phase 1** | [`docs/01-vision-and-constraints.md`](docs/01-vision-and-constraints.md) | Tầm nhìn, ràng buộc cứng ToS Antigravity & Kanboard |
| | [`docs/02-mvp-and-departments.md`](docs/02-mvp-and-departments.md) | Phạm vi MVP & cơ cấu 1 Director + 3 Phòng ban |
| | [`docs/03-learning-and-token-budget.md`](docs/03-learning-and-token-budget.md) | Cơ chế tự học Hermes 3 tầng & 5 quy tắc tiết kiệm token |
| **Phase 2** | [`docs/04-information-architecture.md`](docs/04-information-architecture.md) | Kiến trúc 2 tầng Shared Infra + Multi-Project & Sitemap Kanboard |
| | [`docs/05-user-flows.md`](docs/05-user-flows.md) | Luồng giao tiếp, Fire-and-Forget & Thông báo trong `agy` UI |
| **Phase 3** | [`docs/06-technical-specs.md`](docs/06-technical-specs.md) | Docker Stack, schema `project.yaml` & `kanboard-client` |
| | [`docs/07-system-design-blueprint.md`](docs/07-system-design-blueprint.md) | Bản thiết kế tổng thể 4 lớp & Bảo mật 4 lớp |
| | [`docs/departments/01-dept-nas-ops.md`](docs/departments/01-dept-nas-ops.md) | Phòng 1: Phần cứng Morefine N6, Watchdog nhiệt độ & Telegram |
| | [`docs/departments/02-dept-media.md`](docs/departments/02-dept-media.md) | Phòng 2: Jellyfin/Arr, Mirror 1:1 `disk1`/`disk2`, Sub-First & ETA |
| | [`docs/departments/03-dept-dev.md`](docs/departments/03-dept-dev.md) | Phòng 3: 11 Micro-Agents, luật ≤ 150 dòng & kho Skill tải lẻ |
| | [`docs/08-edge-cases-and-guardrails.md`](docs/08-edge-cases-and-guardrails.md) | Edge Cases, Empty/Loading States & Quota/ToS Guardrails |
| **Phase 4** | [`docs/09-dev-handoff-and-roadmap.md`](docs/09-dev-handoff-and-roadmap.md) | Checklist chuẩn bị, lộ trình 5 Sprint & Tiêu chí nghiệm thu |
| **Go-Live** | [`docs/10-casaos-golive-runbook.md`](docs/10-casaos-golive-runbook.md) | Hướng dẫn triển khai thực tế trên CasaOS, `/automation` & Multi-Project |

## Cấu trúc Mã nguồn & Công cụ (`v1.0.0`)
- `platform/`: `docker-compose.yml` (`kanboard`, `docker-proxy`, `homenas-watchdog`), `Dockerfile.watchdog`, `.env.example`, `hooks/hooks.json`.
- `shared/tools/kanboard_client/`: Adapter JSON-RPC 2.0, hàng đợi offline RAM `/tmp`, chống trùng thẻ (`dedup_key`), Unread Digest & Inline Receipt.
- `shared/tools/guardrails/pre_tool_guard.py`: Chốt chặn 0-token bảo vệ container lõi (`adguard-home`...) và trần cứng **≤ 150 dòng/file** toàn dự án.
- `shared/tools/memory_manager/` & `skill_curator/`: Tự nén `MEMORY.md` (≤ 100 dòng), chốt chặn `skill-proposal` và tải lẻ trực tiếp `SKILL.md`.
- `tools/nas_ops/`: Cảm biến SMART tôn trọng `standby`, State Machine nhiệt độ/overload, lưu mẫu RAM flush 1 lần lúc 23:55, tổng hợp tuần Chủ nhật & backup SQLite.
- `tools/media_ops/`: Mirror 1:1 `disk1`/`disk2` (bỏ `4K_UHD`), cân bằng dung lượng, Sub-First 2K/4K linh hoạt (TV 1080p lọc TVRip), hàng đợi tải tuần tự 1-phim-1-lượt & canh 25% ETA.

Xem lịch sử phiên bản đầy đủ tại [`CHANGELOG.md`](CHANGELOG.md).
