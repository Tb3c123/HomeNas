# Changelog

Tất cả thay đổi quan trọng của dự án **HomeNas (Smart Home AI Orchestrator)** được ghi nhận tại đây theo chuẩn [Conventional Commits](https://www.conventionalcommits.org/).

## [v1.1.0] - 2026-11-19 *(Clean 4-Command Telegram Bot & Remote Control /reconnect)*
### Added
- `tools/nas_ops/tg_commands.py`: Tự động xóa lệnh thừa cũ (`deleteMyCommands` + `setMyCommands`) chỉ giữ đúng 4 lệnh `/status`, `/reconnect`, `/digest`, `/help`, khóa cứng `TELEGRAM_CHAT_ID`.
- `platform/agy-config/remote_keeper.sh`: Vòng lặp siêu nhẹ giữ `agy remote-control start --name home-nas` luôn sống và xử lý cờ `.state/reconnect_remote.flag` không cần mở `EXEC: 1`.
- `tests/test_tg_commands.py`: Bộ unit test kiểm chứng dọn menu, khóa whitelist `chat_id` và luồng `/reconnect`.
### Changed
- `tools/nas_ops/inspector_cli.py` & `docs/10-casaos-golive-runbook.md`: Tích hợp luồng nền Telegram vào `--daemon` và hướng dẫn chạy `remote_keeper.sh`.

## [v1.0.10] - 2026-11-19 *(Security Backlog Logged)*
### Added
- `docs/11-backlog-security-hardening.md`: Lưu danh sách nâng cấp bảo mật (Red-Team Threat Model) vào backlog Do Later cho v1.2+.

## [v1.0.9] - 2026-11-19 *(4-Frame Sidebar Workflow & Auto Handoff Prompts)*
### Added
- `skills/director/orchestrate-and-digest/SKILL.md` & `AGENTS.md`: Chuẩn hóa quy trình **Lựa chọn B (4 khung sidebar `Main`, `Dept-NasOps`, `Dept-Media`, `Dept-Dev`)** — mỗi khi `Main` tạo thẻ Kanboard sẽ tự động sinh sẵn **Handoff Prompt copy 1 chạm** kèm chỉ dẫn rõ dán vào khung phòng ban nào.

## [v1.0.8] - 2026-11-19 *(Read-Smooth & Plan-Before-Mutate Gate)*
### Changed
- `AGENTS.md`: Bổ sung Mục 4 quy chuẩn **Đọc mượt 100% — Trình Action Plan 1 lần trước khi Thêm/Xóa/Sửa**.
- `platform/agy-config/settings.safe-turbo.json`: Gỡ `docker compose up*` khỏi danh sách `ask` để thực thi trọn gói mượt mà sau khi PO duyệt Action Plan (giữ nguyên khóa cứng `deny` container lõi).

## [v1.0.7] - 2026-11-19 *(Kanboard Real-API Compatibility Hotfix)*
### Fixed
- `shared/tools/kanboard_client/bootstrap.py`: Tự động gán `admin` (`user_id=1`) làm `project-manager` cho Project #1 để bảng `HomeNas Operations` hiển thị ngay trên Dashboard Kanboard (`:8085`).
- `shared/tools/kanboard_client/service.py` & `cli.py`: Ánh xạ `column_id`/`swimlane_id` sang tên cột & Swimlane khi gọi `getAllTasks` thực tế, và bổ sung cờ `--swimlane`/`--col` cho lệnh `create`/`move`.

## [v1.0.6] - 2026-11-19 *(Safe-Turbo CLI Configuration)*
### Added
- `platform/agy-config/settings.safe-turbo.json` & `apply_safe_turbo.py`: Chế độ "Safe-Turbo" (`agentMode: accept-edits`, `toolPermission: always-proceed`, `artifactReviewPolicy: always-proceed`) kèm `permissions.deny`/`ask` bảo vệ container lõi (`adguard-home`, `antigravity-cli`...) và công cụ gộp JSON không làm mất cấu hình cũ.
- `docs/10-casaos-golive-runbook.md` & `tests/test_sprint1_platform.py`: Bổ sung hướng dẫn kích hoạt Safe-Turbo và unit test kiểm chứng gộp cấu hình an toàn.

## [v1.0.5] - 2026-11-19 *(Multi-Session AGENTS.md)*
### Added
- `AGENTS.md`: Tệp định hướng chuẩn cho `antigravity-cli` (37 dòng) giúp 4 phiên chat (`director`, `dept-nas-ops`, `dept-media`, `dept-dev`) tự động nạp đúng bộ nhớ/Skill, in Inline Receipt và tuân thủ toàn bộ chốt chặn bảo vệ/trần 150 dòng.

## [v1.0.4] - 2026-11-19 *(Weekly Telegram Reminder — ToS-Safe Option 1)*
### Added
- `tools/nas_ops/inspector_cli.py`: Tự động bắn tin nhắn Telegram lúc 20:00 Chủ nhật kèm sẵn câu lệnh prompt copy 1 chạm cho `antigravity-cli` (tuân thủ 100% ToS, không dùng daemon ngoài tự gọi `agy -p`).

## [v1.0.3] - 2026-11-19 *(Read-Only SQLite & Kanboard Bootstrap Hotfix)*
### Added
- `shared/tools/kanboard_client/bootstrap.py`: Module tự động đọc `api_token` (chế độ `mode=ro&immutable=1`) và khởi tạo Project `HomeNas Operations` (5 cột, 4 Swimlanes).
### Fixed
- `tools/nas_ops/backup_kanboard.py`: Mở file SQLite nguồn bằng URI `mode=ro&immutable=1` để tương thích 100% với volume mount `:ro`.

## [v1.0.2] - 2026-11-19 *(Hook Path Hotfix)*
### Fixed
- `platform/hooks/hooks.json`: Chuyển sang đường dẫn tuyệt đối `/mnt/disk1/Workspace/HomeNas/shared/tools/guardrails/pre_tool_guard.py` để `PreToolUse` hook chạy chính xác khi `antigravity-cli` thực thi từ `/root/.gemini/config/`.

## [v1.0.1] - 2026-11-19 *(Production Deployment Hotfix)*
### Fixed
- `tools/nas_ops/inspector_cli.py`: Bổ sung cờ `--daemon` cho vòng lặp giám sát 3 phút, flush 23:55, backup Kanboard 03:00 và tổng hợp tuần Chủ nhật 20:00.
- `platform/docker-compose.yml`: Mount thêm `/dev/disk/by-id:/dev/disk/by-id:ro` cho container `homenas-watchdog` để chống đảo tên `sda`/`sdb` sau reboot.

## [v1.0.0] - 2026-11-19 *(Sprint 5 Complete — Production Ready Release)*
### Added
- `shared/tools/project_loader/loader.py`: Bộ nạp cấu hình `project.yaml` đa dự án (0 external dependencies) và kiểm tra quyền hạn tool theo phòng ban.
- `docs/10-casaos-golive-runbook.md`: Sổ tay triển khai Go-Live trên CasaOS, cấu hình `/automation` qua Remote Control và cắm thêm dự án mới.
- `tests/test_sprint5_e2e_dryrun.py`: Kiểm thử diễn tập End-to-End cả 4 kịch bản thực tế (Nhiệt độ HDD 65°C + Media Thermal Wait + Recovery; Sub-First Sequential Download + Auto-Fallback; Multi-Project Plug-in #2; Hook 0-token chặn > 150 dòng & bảo vệ `adguard-home`).

## [v1.0.0-sprint4] - 2026-11-19 *(Sprint 4: Hermes 3-Tier Memory, Direct-Fetch Skills & 11 Micro-Agents)*
### Added
- `shared/memory/USER.md`, `memory/*/MEMORY.md`: Khởi tạo bộ nhớ Hermes Tầng 1 và Tầng 2 cho cả 3 phòng ban.
- `shared/tools/memory_manager/compactor.py`: Cơ chế tự nén bộ nhớ ≤ 100 dòng và chốt chặn Memory Poisoning Guard (`skill-proposal` chờ PO duyệt).
- `shared/tools/skill_curator/fetcher.py` & `skills/*/*/SKILL.md`: Công cụ tải lẻ trực tiếp `SKILL.md` (không cài npm/CLI thừa), kiểm toán bảo mật và bộ Skill chuẩn cho `director`, `dept-nas-ops`, `dept-media`, `dept-dev` (11 Micro-Agents).
- `tests/test_sprint4_memory_and_skills.py`: Bộ unit test Sprint 4 chạy trên RAM `/tmp`.

## [v1.0.0-sprint3] - 2026-11-19 *(Sprint 3: Media Engine & Dual-Disk Mirror)*
### Added
- `tools/media_ops/` (`disk_balancer.py`, `sub_first_matcher.py`, `media_watcher.py`, `inspector_cli.py`): Chuẩn hóa Mirror 1:1 `disk1`/`disk2` (loại bỏ `4K_UHD`), cân bằng dung lượng cho Movies, dồn trọn Season phim bộ về 1 ổ, khớp Sub Việt chuẩn + ưu tiên 2K/4K linh hoạt (phim bộ 1080p lọc bỏ TVRip), hàng đợi tải tuần tự 1-phim-1-lượt và canh 25% ETA có kiểm tra chéo `thermal_paused`.
- `tests/test_sprint3_media_engine.py`: Bộ unit test Sprint 3 chạy trên RAM `/tmp`.

## [v1.0.0-sprint2] - 2026-11-19 *(Sprint 2: NAS Watchdog & Thermal Protection)*
### Added
- `platform/Dockerfile.watchdog`: Image nhẹ cho container `homenas-watchdog`.
- `tools/nas_ops/` (`sensors.py`, `policy.py`, `emergency.py`, `reporter.py`, `backup_kanboard.py`, `inspector_cli.py`): Bộ cảm biến SMART tôn trọng `standby`, State Machine nhiệt độ/overload, dừng khẩn cấp bảo vệ `adguard-home`, lưu mẫu RAM flush 1 lần lúc 23:55, tổng hợp tuần Chủ nhật và backup nóng SQLite Kanboard.
- `tests/test_sprint2_nas_watchdog.py`: Bộ unit test Sprint 2 chạy trên RAM `/tmp`.

## [v1.0.0-sprint1] - 2026-11-19 *(Sprint 1: Shared Platform & Guardrails)*
### Added
- `platform/docker-compose.yml`, `platform/.env.example`, `project.yaml`, `.gitignore`: Hạ tầng Shared Platform cho CasaOS và cấu hình Multi-Project.
- `shared/tools/kanboard_client/` (`rpc_client.py`, `formatter.py`, `digest_state.py`, `service.py`, `cli.py`): Bộ công cụ JSON-RPC 2.0 với hàng đợi offline RAM (`/tmp`), chống trùng thẻ (`dedup_key`), Unread Digest và Inline Receipt.
- `shared/tools/guardrails/pre_tool_guard.py` & `platform/hooks/hooks.json`: Chốt chặn 0-token bảo vệ container lõi (`adguard-home`...) và kiểm tra cứng trần ≤ 150 dòng/file toàn dự án.
- `tests/test_sprint1_platform.py`: Bộ unit test Sprint 1 chạy trên RAM `/tmp`.

## [v1.0.0-design-complete] - 2026-11-19 *(Phase 4 Design Complete)*
### Added
- `docs/09-dev-handoff-and-roadmap.md`: Checklist Pre-Flight và lộ trình thực thi 5 Sprint kèm tiêu chí nghiệm thu (DoD).
- `README.md`: Tổng mục lục điều hướng toàn bộ kiến trúc và tài liệu dự án HomeNas.

## [v0.3.5] - 2026-11-19 *(Phase 3 Complete — tag `v0.3.5-phase3`)*
### Added
- `docs/08-edge-cases-and-guardrails.md`: Hoàn thiện xử lý trạng thái rỗng/đang tải, chịu lỗi phần cứng Morefine N6/Acasis (offline 100%, `/dev/disk/by-id/`), chống hủy nhầm torrent khi HDD nóng và chốt chặn Quota/ToS/Line-Cap.

## [v0.3.4] - 2026-11-19
### Added
- `docs/departments/03-dept-dev.md`: Thiết kế chuyên sâu Phòng 3 (`dept-dev`) với đội hình đầy đủ 11 Micro-Agents (PM, BA, UX/UI, Architect, BE, FE, Refactor, QA, Security, DevOps, Docs/Skill Curator), giao thức tự trao đổi nội bộ (tối đa 2 vòng lặp) & liên phòng ban qua Kanboard, luật trần cứng ≤ 150 dòng toàn dự án (chống lách luật) và kho Agent Skills tải lẻ trực tiếp.

## [v0.3.3] - 2026-11-19
### Added
- `docs/departments/02-dept-media.md`: Thiết kế chuyên sâu Phòng 2 (`dept-media`) theo cấu trúc thực tế — Mirror 1:1 trên `disk1`/`disk2` (loại bỏ `4K_UHD`), cân bằng dung lượng tự động, dồn trọn Season phim bộ về 1 ổ, ưu tiên Sub Việt + 2K/4K linh hoạt (phim bộ 1080p hạn chế TVRip), tải tuần tự 1-phim-1-lượt, canh 20–30% ETA viết mới 100%.
### Changed
- `docs/departments/01-dept-nas-ops.md`: Đồng bộ thông số 2 ổ 10TB thực tế (`sda` WD Gold + `sdb` WD Purple Pro) và khóa bảo vệ `adguard-home`, `portainer`, `antigravity-cli`.

## [v0.3.2] - 2026-11-19
### Added
- `docs/departments/01-dept-nas-ops.md`: Thiết kế chuyên sâu Phòng 1 (`dept-nas-ops`) cho phần cứng Morefine N6 (Intel N200, 16GB RAM, 256GB SSD, 20TB HDD dock Acasis, CasaOS Docker), container `homenas-watchdog` (0-token, lưu RAM flush 1 lần/ngày, Telegram khẩn cấp tự dừng container nặng) và tích hợp Antigravity `/automation` (qua Remote Control), `/schedule`, `hooks.json`.

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
