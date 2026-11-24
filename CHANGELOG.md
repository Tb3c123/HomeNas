# Changelog

Tất cả thay đổi quan trọng của dự án **HomeNas (Smart Home AI Orchestrator)** được ghi nhận tại đây theo chuẩn [Conventional Commits](https://www.conventionalcommits.org/).

## [v2.1.0] - 2026-11-24 *(Curated 76-Skill Zero-Duplicate Dev Library: +12 UI/UX Pro & +16 Research/Algorithms/AI)*
### Added
- `skills/dept-dev/` (+28 skill tinh hoa không trùng lặp, nâng tổng từ **48 → 76 skills**, mỗi tệp `≤ 60 dòng`, `model: inherit`, MIT/Apache-2.0): **+12 UI/UX Pro** (`frontend-aesthetic-design`, `design-tokens-oklch`, `typography-and-hierarchy`, `web-interaction-motion`, `ui-critique-and-polish`, `ux-copywriting-microcopy`, `forms-and-validation-ux`, `responsive-layout-architecture`, `react-composition-patterns`, `data-visualization-ux`, `interactive-canvas-svg-ui`, `web-performance-core-vitals`) và **+16 Nghiên cứu / Thuật toán / AI** (`scientific-research-synthesis`, `research-ideation-methodology`, `academic-paper-writing`, `autoresearch-experiment-loop`, `algorithm-design-complexity`, `combinatorial-optimization`, `mathematical-stochastic-modeling`, `numerical-computing-vectorization`, `time-series-forecasting`, `ml-modeling-classical`, `deep-learning-pytorch`, `llm-finetuning-post-training`, `ai-inference-optimization`, `multimodal-vision-audio-ai`, `ai-safety-guardrails-alignment`, `vector-hybrid-search-engineering`).
### Changed
- `skills/dept-dev/CATALOG.md`, `shared/templates/DEV_TEAM_RULES.md`, `shared/tools/project_loader/scaffold.py` & `tests/test_dev_skills_pack.py`: Nâng cấp mục lục Lazy-Load 8 lĩnh vực (76/76 skills, không trùng lặp, tự đồng bộ Live-Link tới toàn bộ dự án con qua `/mnt/disk1/Workspace/shared`).

## [v2.0.4] - 2026-11-23 *(Stateless Reconciliation: Fix Stuck qBittorrent 2.56 MB/s Mode & Paused Containers After Restart)*
### Fixed
- `tools/nas_ops/qbit_throttle.py`, `emergency.py`, `policy.py`, `inspector_cli.py` & `tests/test_stateless_reconcile.py`: Chuyển sang đối chiếu trạng thái thật (`GET /api/v2/transfer/speedLimitsMode` & Docker `State.Paused`) thay vì chỉ dựa vào cờ `self._throttled` trong RAM — tự động nhả `Alternative Speed Mode = "0"` (mở trần tốc độ) và `unpause` container media bị kẹt ngay cả sau khi `homenas-watchdog` khởi động lại.

## [v2.0.2] - 2026-11-22 *(CasaOS Host Keeper `404→install -f` + Systemd, Memory CLI `PYTHONPATH` Fix & `GEMINI.md` Root Link)*
### Added
- `platform/agy-config/casaos-apply-keeper.service`: Unit `systemd` (`User=root`, `Restart=always`) cho Host Keeper tự khởi động cùng Debian host.
- `shared/tools/project_loader/scaffold.py`: Tự sinh `GEMINI.md` trỏ đúng `@[AGENTS.md](AGENTS.md)` (kèm auto-fix trong `bootstrap_workspace.py`).
### Fixed
- `platform/agy-config/casaos_apply_host_keeper.sh` & `casaos_apply.py`: Tự động fallback sang `casaos-cli app-management install -f` khi `apply` trả về `404 Not Found` (cài app mới lần đầu), ghi rõ trạng thái `APPLIED` vs `INSTALLED`.
- `shared/tools/memory_manager/cli.py`: Tự chèn thư mục gốc `HomeNas` vào `sys.path` để chạy thẳng từ mọi dự án con không cần export `PYTHONPATH`.
- `shared/templates/DEV_TEAM_RULES.md`: Bổ sung `store_app_id`, `is_uncontrolled: false`, danh sách cổng host cần tránh (`3000`, `8000`, `8085`, `8090`, `8096`) và lưu ý chạy test SQLite trên `/tmp` tránh nghẽn `fsync` USB HDD.

## [v2.0.1] - 2026-11-22 *(CasaOS Native App 2-File Standard & Safe Host-Keeper Bridge)*
### Added
- `shared/tools/project_loader/casaos_apply.py`, `platform/agy-config/casaos_apply_host_keeper.sh` & `tests/test_casaos_apply.py`: Bộ kiểm chuẩn `casaos-compose.yml` (cấm `build:`, bắt buộc `x-casaos:` & `image:`) kèm cầu nối Host Keeper an toàn (whitelist chỉ chạy `casaos-cli app-management apply` cho file nằm trong `/mnt/disk1/Workspace/`).
### Changed
- `shared/templates/DEV_TEAM_RULES.md` & `skills/dept-dev/deployment-engineer/SKILL.md`: Khóa cứng **Chuẩn Đóng Gói CasaOS Native App** (2 tệp `docker-compose.yml` để build + `casaos-compose.yml` không `build:` để đăng ký Native App, cấm tự `docker compose up -d` gây `Legacy App`) tự động đồng bộ tới mọi đội Dev qua `/mnt/disk1/Workspace/shared`.

## [v2.0.0] - 2026-11-22 *(Auto Dead-Torrent Healer via Radarr/Sonarr & Solo Tech Secretary Topology)*
### Added
- `tools/media_ops/dead_torrent_healer.py` & `tests/test_dead_torrent_healer.py`: Luồng nền tự động mỗi 12 phút trong `homenas-watchdog` kiểm tra torrent active (`downloading`, `stalledDL`, `metaDL`, `missingFiles`, bỏ qua `queuedDL` và `thermal_paused`); với torrent `< 5%` chết `0` seed `> 20 phút` (hoặc `missingFiles`) tự thử `reannounce` + bơm public trackers ở kỳ 1, nếu kỳ sau vẫn kẹt tự gọi API Radarr/Sonarr (`DELETE /api/v3/queue/{id}?removeFromClient=true&blocklist=true&skipRedownload=false`) để gỡ & tìm bản thay thế; bảo vệ không xóa torrent `>= 20%` còn `> 5` seed (chỉ báo nhẹ sau `> 2 tiếng`).
### Changed
- `AGENTS.md`, `project.yaml`, `skills/director/orchestrate-and-digest/SKILL.md` & `shared/tools/kanboard_client/bootstrap.py`: Loại bỏ hoàn toàn phòng `Dept-Dev` (11 Micro-Agents) khỏi `HomeNas` (chỉ dùng cho các Project phần mềm riêng qua `/mnt/disk1/Workspace/shared`); tái định nghĩa `Liam` thành **Thư ký Kỹ thuật đơn lẻ (`Liam - Tech Secretary`)** chuyên hỗ trợ viết/sửa script hệ thống cho team.

## [v1.9.0] - 2026-11-22 *(Option 1+ Canonical `/Workspace/shared` Namespace & Child-Project Auto-Migrator)*
### Added
- `shared/tools/project_loader/bootstrap_workspace.py`: Tự động tạo không gian tên ngang hàng `/mnt/disk1/Workspace/shared` (kèm cầu nối `/mnt/disk1/Workspace/shared/skills/dept-dev`) và tự động nâng cấp `AGENTS.md` + `project.yaml` của toàn bộ dự án con hiện có (`HomeManager`, `stochastic-matrix-lab`...) sang đường dẫn `/mnt/disk1/Workspace/shared/...` độc lập, xóa bỏ sự phụ thuộc tên `HomeNas` mà vẫn giữ 1 repo Git cập nhật 1 chạm.
### Changed
- `shared/templates/DEV_TEAM_RULES.md`, `shared/tools/project_loader/scaffold.py`, `shared/tools/guardrails/pre_tool_guard.py`, `.gitignore` & `tests/test_project_scaffold.py`: Đồng bộ 100% đường dẫn dự án con về `/mnt/disk1/Workspace/shared/...`.

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

## [v1.0.0–v1.0.10] - 2026-11-19 *(Sprint 1–5 Complete, Safe-Turbo, 4-Frame Workflow & Security Backlog)*
### Added
- Toàn bộ hạ tầng Shared Platform (Sprint 1–5), `AGENTS.md`, Safe-Turbo (`apply_safe_turbo.py`), tương thích API Kanboard thực tế, quy chuẩn Read-Smooth / Plan-Before-Mutate, luồng 4 khung Handoff Prompt và backlog bảo mật (`docs/11-backlog-security-hardening.md`).

---
*Lịch sử thiết kế Phase 1–4 (`v0.1.0` → `v1.0.0-design-complete`) được lưu trữ tại [`docs/changelog-v0-design.md`](docs/changelog-v0-design.md) để đảm bảo trần ≤ 150 dòng/file.*
