# Department 01: `dept-nas-ops` (Hạ tầng NAS, Nhiệt độ & Watchdog)

## 1. Hồ sơ Phần cứng & Ràng buộc Triển khai
- **Thiết bị:** Morefine N6 — Intel N200 (4 cores, 6W TDP), 16GB RAM.
- **Lưu trữ:** 256GB SSD (OS/Docker — **giới hạn đọc/ghi tối đa**) + 20TB HDD gắn ngoài qua **dock USB Acasis**.
- **Hệ điều hành & Quản trị:** Debian + **CasaOS** (**100% dịch vụ đóng gói Docker quản lý qua CasaOS**).
- **Kênh cảnh báo & điều khiển:** Telegram Bot trong container `homenas-watchdog` (0 token LLM) + **Antigravity CLI (`agy`) Remote Control** (hỗ trợ quản lý phiên & `/automation` từ trình duyệt).

## 2. Container `homenas-watchdog` (0-Token Deterministic Engine)

Đóng gói thành 1 container Docker nhẹ (~25MB RAM) trong stack CasaOS, tách thành 4 module Python nhỏ:
- `sensors.py`: Đọc nhiệt độ CPU (`/sys/class/thermal`), Load Avg (`/proc/loadavg`), RAM/Disk, và nhiệt độ HDD qua `smartctl -n standby -d sat` (bỏ qua nếu HDD đang ngủ `standby`, không đánh thức ổ).
- `policy.py`: Máy trạng thái (State Machine) đánh giá ngưỡng nhiệt độ + thời lượng duy trì + điều kiện kép.
- `emergency.py`: Thực thi dừng khẩn cấp **chỉ trên danh sách `STOPPABLE_CONTAINERS`** (khai báo trong `.env`), tuyệt đối khóa cứng bảo vệ các container lõi (`casaos`, `kanboard`, `homenas-watchdog`, `agy-runtime`).
- `reporter.py`: Lưu mẫu trong **RAM (`tmpfs`)**, flush đúng **1 lần lúc 23:55** ra `logs/thermal/YYYY-MM-DD.json` (xoay vòng 30 ngày), gửi Telegram, và tổng hợp báo cáo tuần vào Chủ nhật 20:00.

## 3. Ma trận Chính sách Nhiệt độ, Overload & Xử lý Khẩn cấp

| Mức độ | Điều kiện kích hoạt (Chu kỳ đo: 3 phút/lần) | Hành động tự động (0 Token) | Thông báo & Kanboard |
| :--- | :--- | :--- | :--- |
| **Mức 0: Bình thường** | HDD `< 60°C` **VÀ** CPU `< 88°C` **VÀ** không Overload. | Ghi mẫu vào RAM (`tmpfs`), 0 ghi SSD. | Im lặng (không spam). |
| **Mức 1: Cảnh báo (Ngắn hạn)** | HDD `60–64°C` kéo dài `> 15 phút` **HOẶC** CPU Overload (`>= 95%` / `Load 5m > 4.0` `> 15 phút`) **HOẶC** CPU `>= 88°C` `> 10 phút`. | Chưa dừng container; ghi nhận Top 3 container ăn CPU/I/O. | **Telegram Warning** + Thẻ Kanboard `Ready` (`daily-alert`, có `dedup_key`). |
| **Mức 2: Khẩn cấp (Tự xử lý ngay)** | HDD `>= 65°C` **HOẶC** HDD `>= 60°C` kéo dài `> 45 phút` **HOẶC** CPU `>= 92°C` kéo dài **HOẶC** **Nguy hiểm kép** (HDD `>= 60°C` + CPU Overload cùng lúc). | **Thực thi NGAY KHÔNG CẦN DUYỆT:** `docker pause/stop` các container nặng trong `STOPPABLE_CONTAINERS` (VD: torrent, media scan/transcode). | **Telegram Emergency** (kèm nguyên nhân & hướng dẫn xử lý) + Thẻ Kanboard `Waiting Review` (`emergency`). |
| **Hồi phục (Hysteresis)** | Sau Mức 2, HDD giảm `< 55°C` và CPU hết Overload liên tục `10 phút`. | Giữ nguyên trạng thái tạm dừng (tránh vòng lặp nóng lại). | **Telegram Recovery:** Báo hệ thống đã mát, chờ PO quyết định mở lại container. |

## 4. Lịch chạy Định kỳ & Tích hợp Antigravity Native (`agy` Remote Control)

### A. Tầng 0-Token (Chạy offline 24/7 trong `homenas-watchdog`)
- **Mỗi 3 phút (RAM-only):** Đo nhiệt độ HDD (tôn trọng `standby`), CPU, Load, RAM, Disk.
- **03:00 hằng ngày:** Backup nóng SQLite của Kanboard (`sqlite3 .backup`), giữ 7 bản; chỉ báo Telegram/Kanboard nếu lỗi.
- **23:55 hằng ngày:** Ghi **1 lần duy nhất** file `logs/thermal/YYYY-MM-DD.json` (min/avg/max + khung giờ đỉnh nhiệt + sự kiện cảnh báo).
- **20:00 Chủ nhật:** Tổng hợp 7 ngày → `logs/thermal/weekly-YYYY-Www.md` (~30 dòng) + tạo thẻ Kanboard `Ready` (tag `weekly-review`).

### B. Tầng AI Native (100% ToS-Safe trong `agy`)
- **`/automation` (quản lý qua `agy` Remote Control — Fresh Context):** Lập lịch **Chủ nhật 20:15** tự động khởi chạy 1 phiên sạch cho `dept-nas-ops` đọc duy nhất `weekly-YYYY-Www.md` (~400 tokens) + `MEMORY.md`, ghi nhận xét vào thẻ Kanboard, cập nhật bài học vào `MEMORY.md` và gửi tóm tắt qua Telegram.
- **`/schedule` (hẹn giờ ngắn hạn trong phiên):** Sau khi PO duyệt mở lại container từng bị dừng khẩn cấp, đặt 1 lần kiểm tra sau 15 phút để xác nhận nhiệt độ ổn định rồi kết thúc.
- **`hooks.json` (`PreToolUse` — 0 Token):** Chốt chặn kỹ thuật tự động ngăn AI thực thi các lệnh phá hủy (`rm -rf`, `docker rm/stop` ngoài quy định) nếu chưa được PO duyệt.

## 5. Playbook & AGY Skills của `dept-nas-ops` (`skills/dept-nas-ops/` — Lazy Load)
1. `weekly-thermal-review.md`: Đọc `weekly-YYYY-Www.md` + `MEMORY.md` → Phân tích khung giờ nhiệt cao, container gây tải, xu hướng tuần và đề xuất tối ưu giúp bảo vệ SSD 256GB & HDD 20TB Acasis lâu bền.
2. `emergency-postmortem.md`: Khi có thẻ `emergency`, đọc log rút gọn (≤ 30 dòng) của container bị dừng, xác định nguyên nhân gốc và đề xuất cách khắc phục cho PO duyệt trước khi bật lại.
3. `docker-health-check.md`: Chạy `nas-inspector` (Fire-and-Forget) kiểm tra trạng thái container CasaOS, SMART 20TB HDD và dung lượng SSD 256GB.

### Ranh giới Quyền của AI `dept-nas-ops`
- **Tự chạy (Fire-and-Forget / `/automation`):** Đọc báo cáo tuần, kiểm tra metrics/SMART, đọc ≤ 30 dòng log lỗi, cập nhật bài học vào `memory/dept-nas-ops/MEMORY.md`.
- **Bắt buộc PO duyệt (`needs-approval`):** Mở lại/xóa container, sửa giới hạn CPU/RAM trong Docker Compose, dọn Docker image/volume, hoặc cập nhật ngưỡng nhiệt trong `.env`.
