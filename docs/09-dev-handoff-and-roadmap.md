# 09. Dev Handoff, Setup Checklist & Implementation Roadmap

## 1. Checklist Chuẩn bị của PO Trước Khi Deploy Production (Pre-Flight)
1. **Lấy định danh cứng 2 ổ HDD Acasis:** Chạy `ls -la /dev/disk/by-id/` để ghi nhận ID cố định cho `sda` (WD Gold 10TB) và `sdb` (WD Purple Pro 10TB).
2. **Tạo Telegram Bot:** Tạo bot qua `@BotFather`, lấy `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID`.
3. **API Keys hiện có:** Lấy sẵn API key của `radarr`, `sonarr`, `bazarr`, `prowlarr`, `jellyfin` và thông tin đăng nhập `qbittorrent` (lưu vào `.env` chmod `600`, không commit Git).
4. **Dọn script cũ:** Đánh dấu lưu trữ/xóa các script cũ trong `/mnt/storage/Workspace/Archive_Scripts_Memory/` (xây mới 100%).

## 2. Lộ trình Triển khai 5 Sprint (Milestones cho `dept-dev`)

| Sprint | Mục tiêu chính | Sản phẩm bàn giao (Deliverables) | Tiêu chí Nghiệm thu (DoD) |
| :--- | :--- | :--- | :--- |
| **Sprint 1: Shared Platform** | Dựng hạ tầng dùng chung & Kanban Message Bus. | `docker-compose.yml` (`kanboard`, `docker-proxy`), `project.yaml`, `kanboard-client` (4 module), `hooks.json` (`PreToolUse`: chặn phá hủy + chặn file > 150 dòng). | `kb list/create/move/comment/digest` pass 100% unit test (RAM `/tmp`); `antigravity-cli` kết nối được Kanboard qua `agy-net`. |
| **Sprint 2: NAS Watchdog** | Bảo vệ Morefine N6 + 2 ổ 10TB Acasis (0 token). | Container `homenas-watchdog` (`sensors.py`, `policy.py`, `emergency.py`, `reporter.py`), backup SQLite 03:00, `/automation` Chủ nhật 20:15. | Đo được nhiệt `sda`/`sdb` không đánh thức `standby`; 0 ghi SSD trong ngày (flush 23:55); test dừng khẩn cấp chỉ tác động `STOPPABLE_CONTAINERS` (giữ sống `adguard-home`). |
| **Sprint 3: Media Engine** | Chuẩn hóa Mirror 1:1 & Tải phim thông minh. | Mount đủ `/data/disk1` & `/data/disk2` cho Arr/qBit (bỏ `4K_UHD`), bật `qbittorrent`, viết mới `media_watcher.py` (Sub-First, 2K/4K linh hoạt, tải tuần tự 1-phim-1-lượt, canh 25% ETA). | Hardlink 0-copy hoạt động trên cả 2 ổ; phim bộ tự dồn về 1 ổ; tự động fallback cặp `#2` khi giả lập tải chậm; không hủy nhầm khi `thermal_paused=true`. |
| **Sprint 4: Memory & Team** | Kích hoạt tự học Hermes & 11 Agents `dept-dev`. | `shared/memory/USER.md`, `memory/*/MEMORY.md`, tải lẻ bộ `SKILL.md` theo vai trò (đã audit), cấu hình 11 Micro-Agents (`MAX_RETRY_LOOPS=2`). | `director` hiển thị Unread Digest 1 dòng/task; Sub-Chat in Inline Receipt; toàn bộ file dự án ≤ 150 dòng. |
| **Sprint 5: Dry Run & Go-Live** | Diễn tập thực tế & Bàn giao vận hành. | Test 4 kịch bản end-to-end (nhiệt 65°C, tải phim, thêm Project #2 plug-in, hook chặn > 150 dòng) + Runbook vận hành. | Toàn bộ 4 kịch bản Pass; gắn tag `v1.0.0` và sẵn sàng chạy trên CasaOS. |

## 3. Quy tắc Bắt buộc cho Đội Dev Khi Thực thi
- **Tách nhỏ file:** Mọi file code, test, script, docs đều **≤ 150 dòng** (trừ lockfile cài đặt), kiểm tra tự động qua `hooks.json`.
- **Cache trên RAM:** Luôn đặt `PYTEST_CACHE_DIR=/tmp/.pytest_cache`, `RUFF_CACHE_DIR=/tmp/.ruff_cache` để bảo vệ SSD NVMe 256GB.
- **Nhánh & Duyệt:** Commit theo từng Sprint theo chuẩn Conventional Commits, kèm unit test và kiểm tra trần dòng.
