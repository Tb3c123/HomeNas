# Changelog

Tất cả thay đổi quan trọng của dự án **HomeNas (Smart Home AI Orchestrator)** được ghi nhận tại đây theo chuẩn [Conventional Commits](https://www.conventionalcommits.org/).

## [v1.5.0] - 2026-11-21 *(Expanded 48-Skill Dev Library — 6 Full-Stack Engineering Domains)*
### Added
- `skills/dept-dev/` (+30 skill mới từ `rmyndharis/antigravity-skills` MIT, nâng tổng lên **48 skills** phủ kín 6 lĩnh vực: Kiến trúc/Hiệu năng, DB/Data, AI/LLM/Multi-Agent, 13 Ngôn ngữ & Mobile, QA/Debug/Security/Auth, DevOps/Git/K8s/Observability — mỗi file ≤ 60 dòng, `model: inherit`).
### Changed
- `skills/dept-dev/CATALOG.md`, `shared/tools/project_loader/scaffold.py` & `tests/test_dev_skills_pack.py`: Nâng cấp mục lục Lazy-Load 6 lĩnh vực (≤ 100 dòng) và kiểm chứng tự động đủ 48/48 skill.

## [v1.4.0] - 2026-11-21 *(Curated 18-Skill Dev Team Library — Mindset + Language Packs)*
### Added
- `skills/dept-dev/` (17 skill mới tinh lọc từ `rmyndharis/antigravity-skills` MIT + `micro-agent-swarm` = **18 skills**, mỗi file ≤ 120 dòng, chuẩn `model: inherit`) & `skills/dept-dev/CATALOG.md` (mục lục Lazy-Load 2 tầng: 10 Tư duy Kỹ thuật + 8 Ngôn ngữ Python/TS/Web).
- `tests/test_dev_skills_pack.py`: Unit test xác thực đủ 18 skill, YAML frontmatter, trần ≤ 120 dòng và đồng bộ `CATALOG.md`.
### Changed
- `shared/tools/project_loader/scaffold.py`: `AGENTS.md` của mọi dự án mới tạo trỏ trực tiếp tới `skills/dept-dev/CATALOG.md`.

## [v1.3.0] - 2026-11-20 *(Hermes Verified Learning Toasts, Memory CLI & ARCHIVE.jsonl)*
### Added
- `shared/tools/memory_manager/cli.py` & `compactor.py`: Chuẩn hóa theo `NousResearch/hermes-agent` (`add`, `patch`, `remove`, `list`, `propose-skill`), tự động lưu bài học bị nén/sửa/xóa vào `memory/ARCHIVE.jsonl` (chống mất tri thức), ghi `.state/learning_feed.jsonl` và xuất badge trực quan **`💾 Memory [<dept>] ➕/✏️/🗑️ ...`** & **`💾 Skill ... 📦 Proposed`**.
### Changed
- `tools/nas_ops/tg_commands.py`, `AGENTS.md` & `shared/tools/project_loader/scaffold.py`: Hiển thị 3 bài học mới nhất trong lệnh `/digest` trên Telegram và bắt buộc Agent in dòng `💾 Memory` qua CLI mỗi khi học được tri thức mới.

## [v1.2.2] - 2026-11-20 *(Instant 1-Turn Project Factory & Clean UI Guide + Kickoff Prompt)*
### Changed
- `AGENTS.md`, `skills/director/orchestrate-and-digest/SKILL.md` & `shared/tools/project_loader/scaffold.py`: Khi PO yêu cầu khởi động/tạo dự án mới hoặc giao task trong `Main`, `Main` tự thực thi ngầm ngay trong 1 lượt (không dừng hỏi Action Plan, không in lệnh terminal) và chỉ xuất **Hướng dẫn 2 bước trên giao diện + Khung Prompt Khởi động copy 1 chạm**.

## [v1.2.1] - 2026-11-20 *(Zero-Host-SSH Docker Compose & Instant 1s Watchdog Reload)*
### Added
- `platform/compose.sh`: Wrapper tự động chạy `docker compose` (fallback qua `docker:cli`) ngay từ `antigravity-cli`, không bao giờ bắt PO tự mở host SSH.
### Changed
- `platform/docker-compose.yml` & `AGENTS.md`: Bind-mount trực tiếp `../shared`, `../tools`, `../project.yaml` vào `homenas-watchdog` — từ nay cập nhật code chỉ cần `git pull && docker restart homenas-watchdog` (1 giây, 0 rebuild, 0 ghi rác SSD).

## [v1.2.0] - 2026-11-20 *(Standalone Project Factory & 1-Tap Kickoff Prompts)*
### Added
- `shared/tools/project_loader/scaffold.py` & `tests/test_project_scaffold.py`: Bộ sinh dự án độc lập (tạo thư mục `/mnt/disk1/Workspace/<TenDuAn>`, Kanboard Project riêng 5 cột + 4 Swimlanes Dev, `project.yaml`, `AGENTS.md` đội 11 Micro-Agents, `memory/MEMORY.md`) và tự xuất **Prompt Khởi động copy 1 chạm**.
### Changed
- `skills/director/orchestrate-and-digest/SKILL.md` & `AGENTS.md`: Chỉ cần nhắn tự nhiên vào `Main` (*"Tạo dự án A..."*), `Main` tự dựng dự án mới & trả Prompt Khởi động; thu gọn `dept-dev` trong `HomeNas` về bảo trì lõi HomeNas.

## [v1.1.2] - 2026-11-20 *(Kanboard Human-Named Agent Users & --author Attribution)*
### Added
- `shared/tools/kanboard_client/bootstrap.py`: Tự động tạo 5 tài khoản nhân sự AI trên Kanboard (`Alex (Director)`, `Marcus (NAS Ops)`, `Elena (Media)`, `Liam (Dev Lead)`, `Sentinel (Watchdog)`) và gán vào Project #1.
- `shared/tools/kanboard_client/service.py` & `cli.py`: Bổ sung cờ `--author` tự ánh xạ `username → user_id` và gắn prefix `[<role>]` cho bình luận/thẻ.
### Changed
- `tools/nas_ops/inspector_cli.py`, `AGENTS.md` & `tests/test_sprint1_platform.py`: Đồng bộ `author="watchdog"`, cập nhật danh tính nhân sự trong `AGENTS.md` và bổ sung unit test định danh tác giả.

## [v1.1.1] - 2026-11-19 *(2-Way Copy-Ready Return Prompts: Sub-Chats → Main)*
### Added
- `AGENTS.md` & `skills/director/orchestrate-and-digest/SKILL.md`: Bổ sung mẫu **Return Prompt copy 1 chạm (`📤 Dán lại vào khung [Main]`)** bắt buộc ở cuối mỗi phiên Sub-Chat, hoàn thiện vòng giao tiếp 2 chiều siêu nhanh giữa 4 khung sidebar.

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

---
*Lịch sử thiết kế Phase 1–4 (`v0.1.0` → `v1.0.0-design-complete`) được lưu trữ tại [`docs/changelog-v0-design.md`](docs/changelog-v0-design.md) để đảm bảo trần ≤ 150 dòng/file.*
