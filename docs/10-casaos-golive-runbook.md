# 10. CasaOS Go-Live Runbook & Multi-Project Operations Guide

## 1. Khởi tạo Cấu hình & Mirror 1:1 trên Morefine N6
1. **Tạo file `.env` từ mẫu:**
   ```bash
   cp platform/.env.example platform/.env
   chmod 600 platform/.env
   ```
   Cập nhật `DISK1_BY_ID` (WD Gold 10TB), `DISK2_BY_ID` (WD Purple Pro 10TB) từ `ls -la /dev/disk/by-id/`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` và `KANBOARD_API_TOKEN`.
2. **Đồng bộ cây thư mục Mirror 1:1 trên `disk1` & `disk2` (đã loại bỏ `4K_UHD`):**
   ```bash
   python3 -m tools.media_ops.inspector_cli init-mirror --disk1 /mnt/disk1 --disk2 /mnt/disk2
   ```

## 2. Triển khai Stack Docker qua CasaOS
1. Khởi chạy Shared Platform (`kanboard`, `docker-proxy`, `homenas-watchdog`):
   ```bash
   docker compose -f platform/docker-compose.yml up -d --build
   ```
2. Kết nối container `antigravity-cli` vào mạng `agy-net`:
   ```bash
   docker network connect agy-net antigravity-cli
   ```
3. Kích hoạt chốt chặn 0-token (`PreToolUse` hook):
   Copy `platform/hooks/hooks.json` vào `/DATA/AppData/antigravity-cli/gemini/config/hooks.json`.

## 3. Cấu hình `/automation` Đánh giá Nhiệt độ Cuối tuần (Qua Remote Control)
Trong `antigravity-cli` (hoặc Remote Control UI), đăng ký Automation chạy Chủ nhật 20:15:
- **Schedule:** `CRON_TZ=Asia/Ho_Chi_Minh 15 20 * * 0`
- **Prompt:** `Sử dụng skill weekly-thermal-review của dept-nas-ops để đọc file logs/thermal/weekly-*.md mới nhất, nhận xét xu hướng nhiệt độ 2 ổ HDD Acasis & CPU N200, cập nhật thẻ weekly-review trên Kanboard và in Inline Receipt.`

## 4. Cắm thêm Dự án Mới (Zero-Infra Duplication)
1. Tạo Project mới trên Kanboard Web UI (`:8085`), lấy `kanboard_project_id` (VD: `2`).
2. Tạo thư mục `/mnt/disk1/Workspace/<NewProject>/` kèm file `project.yaml` khai báo `kanboard_project_id: 2`.
3. Mọi công cụ (`kanboard-client --project-id 2`, `USER.md`, `pre_tool_guard.py`) tự động hoạt động ngay mà không cần dựng thêm container mới.

## 5. Lệnh Kiểm tra Sức khỏe & Tuân thủ Toàn Dự án
```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v -s tests
PYTHONDONTWRITEBYTECODE=1 python3 shared/tools/guardrails/pre_tool_guard.py --audit-repo .
```
