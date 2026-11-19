# Department 01: `dept-nas-ops` (Hạ tầng NAS, Nhiệt độ & Watchdog)

## 1. Hồ sơ Phần cứng & Ràng buộc Triển khai
- **Thiết bị:** Morefine N6 — Intel N200 (4 cores, 6W TDP), 16GB RAM.
- **Lưu trữ:** 256GB SSD (OS/Docker — **giới hạn ghi tối đa**) + 20TB HDD gắn ngoài qua **dock USB Acasis**.
- **Hệ điều hành & Quản trị:** Debian + **CasaOS** (**100% dịch vụ đóng gói Docker quản lý qua CasaOS**).
- **Kênh cảnh báo tức thời:** Telegram Bot tích hợp trong container `homenas-watchdog` (0 token LLM).

## 2. Container `homenas-watchdog` (0-Token Deterministic Engine)

Đóng gói thành 1 container Docker nhẹ (~25MB RAM) trong stack CasaOS, tách thành 4 module Python nhỏ:
- `sensors.py`: Đọc nhiệt độ CPU (`/sys/class/thermal`), Load Avg (`/proc/loadavg`), RAM/Disk, và nhiệt độ HDD qua `smartctl -n standby -d sat` (bỏ qua nếu HDD đang ngủ `standby`).
- `policy.py`: Máy trạng thái (State Machine) đánh giá ngưỡng nhiệt độ + thời lượng duy trì + điều kiện kép.
- `emergency.py`: Thực thi dừng khẩn cấp **chỉ trên danh sách `STOPPABLE_CONTAINERS`** (qua biến môi trường `.env`), tuyệt đối bảo vệ các container lõi (`casaos`, `kanboard`, `homenas-watchdog`, `agy-runtime`).
- `reporter.py`: Lưu mẫu trong **RAM (`tmpfs`)**, flush đúng **1 lần lúc 23:55** ra `logs/thermal/YYYY-MM-DD.json` (xoay vòng 30 ngày), gửi Telegram, và tổng hợp báo cáo tuần vào Chủ nhật 20:00.

## 3. Ma trận Chính sách Nhiệt độ, Overload & Xử lý Khẩn cấp

| Mức độ | Điều kiện kích hoạt (Chu kỳ đo: 3 phút/lần) | Hành động tự động (0 Token) | Thông báo & Kanboard |
| :--- | :--- | :--- | :--- |
| **Mức 0: Bình thường** | HDD `< 60°C` **VÀ** CPU `< 88°C` **VÀ** không Overload. | Ghi mẫu vào RAM (`tmpfs`), 0 ghi SSD. | Im lặng (không spam). |
| **Mức 1: Cảnh báo (Ngắn hạn)** | HDD `60–64°C` kéo dài `> 15 phút` **HOẶC** CPU Overload (`>= 95%` / `Load 5m > 4.0` `> 15 phút`) **HOẶC** CPU `>= 88°C` `> 10 phút`. | Chưa dừng container; ghi nhận Top 3 container ăn CPU/I/O. | **Telegram Warning** + Thẻ Kanboard `Ready` (`daily-alert`, có `dedup_key`). |
| **Mức 2: Khẩn cấp (Tự xử lý ngay)** | HDD `>= 65°C` **HOẶC** HDD `>= 60°C` kéo dài `> 45 phút` **HOẶC** CPU `>= 92°C` kéo dài **HOẶC** **Nguy hiểm kép** (HDD `>= 60°C` + CPU Overload cùng lúc). | **Thực thi NGAY KHÔNG CẦN DUYỆT:** `docker pause/stop` các container nặng trong `STOPPABLE_CONTAINERS` (VD: torrent, media scan/transcode). | **Telegram Emergency** (kèm nguyên nhân & hướng dẫn xử lý) + Thẻ Kanboard `Waiting Review` (`emergency`). |
| **Hồi phục (Hysteresis)** | Sau Mức 2, HDD giảm `< 55°C` và CPU hết Overload liên tục `10 phút`. | Giữ nguyên trạng thái tạm dừng (không tự bật lại gây vòng lặp nóng). | **Telegram Recovery:** Báo hệ thống đã mát, chờ PO quyết định mở lại container. |

## 4. Tích hợp Antigravity Native Automations, Schedule & Hooks

Tận dụng đầy đủ 3 cơ chế chính thức của Antigravity (100% chuẩn ToS, kết hợp **Remote Control** của `agy` CLI):
1. **`/automation` (Sidecar — Fresh Context):** Chạy **Chủ nhật 20:15 hằng tuần** (cấu hình dễ dàng qua `agy` Remote Control) → tự động mở phiên sạch cho `dept-nas-ops` đọc duy nhất file `weekly-YYYY-Www.md` + `MEMORY.md`, viết nhận xét tối ưu tuổi thọ hệ thống lên Kanboard và gửi bản tóm tắt qua Telegram.
2. **`/schedule` (Ngắn hạn trong phiên):** Dùng cho kiểm tra lại có giới hạn (VD: hẹn 15 phút sau khi bật lại container tải phim để kiểm tra nhiệt độ HDD 1 lần rồi tắt). Không dùng lặp vô hạn để tránh phình context.
3. **`hooks.json` (`PreToolUse` — 0 Token):** Chốt chặn kỹ thuật tự động từ chối nếu AI gọi lệnh phá hủy (`rm -rf`, `docker rm/stop` ngoài quy định) khi chưa có xác nhận của PO.

## 5. Lịch chạy Định kỳ của `dept-nas-ops`
- **Mỗi 3 phút (0 Token, RAM-only):** `homenas-watchdog` đo nhiệt độ HDD (tôn trọng `standby`), CPU, Load, RAM, Disk.
- **03:00 hằng ngày (0 Token):** Backup nóng SQLite của Kanboard (`sqlite3 .backup`), giữ 7 bản; chỉ báo nếu lỗi.
- **23:55 hằng ngày (0 Token):** Ghi **1 lần duy nhất** `logs/thermal/YYYY-MM-DD.json` xuống SSD.
- **20:00 Chủ nhật (0 Token):** Tổng hợp 7 ngày → `logs/thermal/weekly-YYYY-Www.md` (~30 dòng) + tạo thẻ Kanboard `weekly-review`.
- **20:15 Chủ nhật (`/automation` — Fresh Context):** `dept-nas-ops` đọc báo cáo tuần, nhận xét và lưu bài học vào `MEMORY.md`.

## 6. Playbook Vận hành & AGY Skills (`skills/dept-nas-ops/` — Lazy Load)
1. `weekly-thermal-review.md`: Phân tích khung giờ nhiệt cao, đối chiếu container gây tải, nhận xét xu hướng và đề xuất điều chỉnh lịch/tản nhiệt bảo vệ SSD 256GB & HDD 20TB Acasis.
2. `emergency-postmortem.md`: Đọc ≤ 30 dòng log lỗi của container vừa bị dừng khẩn cấp, tìm nguyên nhân gốc và đề xuất hướng xử lý cho PO duyệt.
3. `docker-health-check.md`: Chạy `nas-inspector` (Fire-and-Forget) kiểm tra container CasaOS, SMART 20TB HDD và dung lượng SSD 256GB.
