# Changelog

Tất cả thay đổi quan trọng của dự án **HomeNas (Smart Home AI Orchestrator)** được ghi nhận tại đây theo chuẩn [Conventional Commits](https://www.conventionalcommits.org/).

## [v1.8.3] - 2026-11-22 *(Zero-Noise Thermal Hotfix: Silent WARNING, USB I/O-Wait Immunity & Emergency Cooldown)*
### Fixed
- `tools/nas_ops/inspector_cli.py`, `policy.py`, `sensors.py`, `emergency.py` & `tests/test_sprint2_nas_watchdog.py`: Tắt hoàn toàn gửi Telegram tức thì ở mức `WARNING` (chỉ lưu log RAM cuối ngày + kích hoạt Thermal Soft-Throttle `2.5 MB/s` trên qBittorrent); chỉ gửi Telegram khi thật sự khẩn cấp (`EMERGENCY` kèm cooldown 30 phút chống lặp, và `AUTO-RECOVERY` tự `unpause`); đo `cpu_pct` từ `/proc/stat` loại trừ `iowait` + yêu cầu `cpu_pct >= 95% AND (load5 > 6.0 OR cpu_temp >= 80°C)` để triệt tiêu báo động giả khi USB Acasis bận ghi đĩa; tăng timeout `smartctl` lên `10s` kèm cache 2 chu kỳ chống tụt nhiệt giả `0.0°C`.

## [v1.8.2] - 2026-11-22 *(Zero-Spam Daily Media Digest at 23:55 & Queue-Clear Notification)*
### Changed
- `tools/media_ops/arr_monitor.py`, `tools/nas_ops/inspector_cli.py` & `tests/test_live_media_monitor.py`: Tắt thông báo Telegram lẻ tẻ khi từng phim tải xong hoặc bị kẹt để chống spam; gom toàn bộ danh sách phim hoàn tất (`completed_today`) và phim bị kẹt (`stalled_today`) vào **1 bản tin Tổng hợp Cuối ngày duy nhất lúc 23:55 (`📊 [MEDIA DAILY DIGEST]`)** (hoặc khi hoàn tất sạch cả hàng đợi `🎉 [MEDIA QUEUE CLEAR]`), đồng thời hiển thị `Xong hôm nay: <N>` ngay trong lệnh `/status`.

## [v1.8.1] - 2026-11-22 *(LiveMediaMonitor Hotfix: Vanished *arr Import Detection, stoppedUP & Anti-Reset Stall Timer)*
### Fixed
- `tools/media_ops/arr_monitor.py` & `tests/test_live_media_monitor.py`: Lưu `active_meta` (`name`, `progress`), bổ sung trạng thái `stoppedup` của qBittorrent v5.x, tự động bắt 100% sự kiện `🎬 [MEDIA DONE]` ngay cả khi Radarr/Sonarr import & xóa torrent khỏi qBittorrent giữa 2 chu kỳ poll (`progress >= 0.85`), dọn sạch hash rác `< 0.85`, giảm ngưỡng kẹt mặc định xuống 20 phút (`1200s`) và chống reset đồng hồ `stalled_since` oan khi tốc độ nhích nhẹ `< 100 KiB/s` hoặc đang `thermal_paused`.

## [v1.8.0] - 2026-11-21 *(4 On-Demand Dev MCP Plugins: Context7, GitHub, Pure-Python SQLite-RO & Playwright)*
### Added
- `shared/tools/mcp_servers/sqlite_ro_mcp.py`: MCP Stdio Server thuần Python 3.11 (0 dependency ngoài) đọc SQLite với khóa Read-Only 3 lớp (`mode=ro&immutable=1`, `PRAGMA query_only=ON`, SQL whitelist chỉ cho phép `SELECT`/`PRAGMA`/`EXPLAIN`).
- `platform/agy-config/sync_mcp_plugins.py` & `tests/test_mcp_plugins.py`: Bộ đồng bộ & bật/tắt 4 plugin (`mcp-context7`, `mcp-github`, `mcp-sqlite-ro`, `mcp-playwright`) vào `/root/.gemini/config/plugins/` (mặc định `disabled: true` để giữ nhẹ ngữ cảnh cho `Main`/`NAS`/`Media`, bảo toàn `config.json` của PO).
### Changed
- `platform/docker-compose.yml`, `platform/.env.example`, `shared/templates/DEV_TEAM_RULES.md` & `docs/departments/03-dept-dev.md`: Bổ sung container on-demand `playwright-mcp` (`profiles: ["dev-mcp"]`, `:8931`) và tài liệu hóa cho mọi dự án con qua Live-Link.

## [v1.7.0] - 2026-11-21 *(0-Token 24/7 Live Media Watcher: qBittorrent/Bazarr Alerts & Telegram /status Queue)*
### Added
- `tools/media_ops/arr_monitor.py` & `tests/test_live_media_monitor.py`: Bộ giám sát tải phim nền 0-token kết nối read-only tới qBittorrent WebUI API & Bazarr API, lưu state dedup trên RAM (`/tmp/homenas_media_monitor.json`), bắn Telegram khi: (a) Phim/Season tải xong 100% + số Sub Việt chờ trên Bazarr, (b) Torrent bị kẹt `stalledDL`/0 seed quá 45 phút (tự bỏ qua nếu đang `thermal_paused`), (c) Toàn bộ hàng đợi hoàn tất (`MEDIA QUEUE CLEAR`).
### Changed
- `tools/nas_ops/inspector_cli.py` & `tools/nas_ops/tg_commands.py`: Tích hợp `LiveMediaMonitor.poll_and_notify()` vào chu kỳ 3 phút của `homenas-watchdog` và hiển thị dòng `- Media Queue:` (phim đang tải, `%`, `MB/s`, số chờ/kẹt) ngay trong lệnh Telegram `/status`.

## [v1.6.1] - 2026-11-21 *(Direct Download Cheat-Sheet Guide & README Quick-Link)*
### Added
- `docs/12-direct-download-guide.md` & `README.md`: Sổ tay hướng dẫn copy 1 chạm cách tải phim từ Google Drive, Fshare VIP (Direct-CDN 5 giây không cần API) và TeraBox, đặt link nổi bật ngay trang chủ `README.md`.

## [v1.6.0] - 2026-11-21 *(Option C AI-Controlled Direct Media Fetcher: Fshare / Google Drive / TeraBox)*
### Added
- `tools/media_ops/direct_fetcher.py` & `inspector_cli.py direct-fetch`: Bộ tải trực tiếp Phương án C cho `Elena (dept-media)` (tự tải thẳng Google Drive ID; nhận Direct-CDN link `download*.fshare.vn` / TeraBox từ trình duyệt cùng mạng LAN không cần API Fshare đã đóng, kèm tùy chọn Web Cookie `FSHARE_COOKIE`/`TERABOX_COOKIE`), tích hợp đủ 5 chốt bảo vệ (chặn đuôi `.exe`/`.sh`, kiểm tra `thermal_paused`, cân bằng `disk1`/`disk2` chuẩn Jellyfin, tải `.part` có resume).
### Changed
- `skills/dept-media/sub-first-download/SKILL.md`, `docs/departments/02-dept-media.md`, `platform/.env.example` & `tests/test_sprint3_media_engine.py`: Cập nhật quy trình Luồng B cho `Elena` và bổ sung unit test kiểm chứng 5 chốt an toàn.

## [v1.5.2] - 2026-11-21 *(External Skill 1000-Line / 64KB Controlled Cap & 2-Step Security Audit Sync)*
### Changed
- `shared/tools/guardrails/pre_tool_guard.py`: Giữ cứng trần `<= 150 dòng` cho toàn bộ code/docs/test/skill nội bộ, đồng thời mở ngoại lệ có kiểm soát `<= 1000 dòng / 64 KB` cho `skills/**/SKILL.md` để tương thích với các skill nguồn ngoài đầy đủ nạp qua `HomeNas Manager (:8090)`.
- `shared/tools/skill_curator/fetcher.py`, `shared/templates/DEV_TEAM_RULES.md` & `tests/test_sprint4_memory_and_skills.py`: Bỏ cơ chế tự cắt cụt ở dòng 150, bổ sung chế độ xem trước 2 bước (`dry_run=True`), cảnh báo (`>150 dòng`, `sudo`, `docker`, `curl`) và chặn cứng `/etc/shadow` & prompt injection.

## [v1.5.1] - 2026-11-21 *(Live-Linked Shared Dev Rules — 1-Update Sync Across All Projects)*
### Added
- `shared/templates/DEV_TEAM_RULES.md`: Hiến pháp vận hành chung của đội 11 Micro-Agents, 48+ Skills Lazy Load, Hermes `💾 Memory` và Guardrails — sửa 1 chỗ tại `HomeNas`, mọi dự án con tự động đồng bộ 100%.
### Changed
- `shared/tools/project_loader/scaffold.py` & `tests/test_project_scaffold.py`: `AGENTS.md` và `project.yaml` của các dự án mới chỉ lưu 4 dòng định danh riêng và Live-Link trực tiếp về `shared/templates/DEV_TEAM_RULES.md`.

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

## [v1.0.0–v1.0.5] - 2026-11-19 *(Sprint 1–5 Complete & Initial Go-Live Hotfixes)*
### Added
- Toàn bộ hạ tầng Shared Platform (Sprint 1), NAS Watchdog & Bảo vệ nhiệt độ (Sprint 2), Media Sub-First & Dual-Disk Mirror (Sprint 3), Hermes 3-Tier Memory & 11 Micro-Agents (Sprint 4), Multi-Project Loader (`loader.py`), Runbook CasaOS (`docs/10-casaos-golive-runbook.md`), `AGENTS.md` đa phiên và E2E Dry-Run (`tests/test_sprint5_e2e_dryrun.py`).

---
*Lịch sử thiết kế Phase 1–4 (`v0.1.0` → `v1.0.0-design-complete`) được lưu trữ tại [`docs/changelog-v0-design.md`](docs/changelog-v0-design.md) để đảm bảo trần ≤ 150 dòng/file.*
