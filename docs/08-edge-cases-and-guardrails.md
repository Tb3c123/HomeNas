# 08. Edge Cases, Empty/Loading States & Quota/ToS Guardrails

## 1. Trạng thái Rỗng & Đang tải (Empty / Loading States trong `agy` UI)
- **Trạng thái Rỗng (Empty):** Khi `kb digest --unread` hoặc `kb list --col Ready` không có thẻ nào → in đúng 1 dòng `[ℹ️ IDLE] Không có thông báo/task mới.`, kết thúc ngay (không gọi thêm tool).
- **Tác vụ ngắn (Loading 5–30s):** Áp dụng timeout cứng (`5s` Kanboard RPC, `10s` Arr/qBit API, `60s` pytest/lint); quá timeout trả lỗi gọn 1 dòng thay vì treo phiên.
- **Tác vụ dài (> 30s — tải phim, theo dõi nhiệt):** Cấm chờ trực tiếp trong `agy`; ủy quyền `homenas-watchdog` (0 token), in `[⏳ QUEUED | #<id>] Đã đẩy hàng đợi (ETA ~X phút).` rồi đóng phiên.

## 2. Edge Cases Hạ tầng & Phần cứng (`dept-nas-ops` & Platform)

| Tình huống Edge Case | Cách hệ thống xử lý an toàn |
| :--- | :--- |
| **Reboot NAS đổi tên `/dev/sda` ↔ `/dev/sdb`** | `sensors.py` dùng định danh cố định `/dev/disk/by-id/` (theo serial WD Gold & WD Purple Pro), không hardcode `/dev/sdX`. |
| **Dock Acasis rớt USB / lỗi I/O SMART** | Bắn **Telegram Critical** ngay lập tức + tạo thẻ `emergency`; không cố mount đè gây hỏng dữ liệu. |
| **HDD đang ngủ `standby`** | `smartctl -n standby` trả mã thoát `2` → ghi nhận `STANDBY` trên RAM (an toàn, không đánh thức ổ, không báo lỗi giả). |
| **Mất Internet (WAN down)** | `homenas-watchdog` vẫn giám sát & tự `pause/stop` container nặng khi HDD ≥ 65°C **offline 100%**; lưu tin Telegram vào RAM và gửi bù khi có mạng. |
| **Container Kanboard down / restart** | `kanboard-client` fail-fast sau 5s, ghi tạm vào `/tmp/kb-fallback-queue.jsonl` (RAM) + báo Telegram; tự đồng bộ bù khi Kanboard sống lại. |

## 3. Edge Cases Media & Download (`dept-media`)

| Tình huống Edge Case | Cách hệ thống xử lý an toàn |
| :--- | :--- |
| **Tải chậm giả do HDD nóng** | `media_watcher.py` kiểm tra cờ `thermal_paused` trước → nếu đang pause do nhiệt thì bỏ qua đếm stalled, không hủy nhầm bản phim đẹp. |
| **Không có Sub Việt khớp bản nào** | Dừng trước bước tải, đẩy thẻ `Waiting Review` (`needs-approval`), tuyệt đối không tải bừa phim lệch/thiếu sub. |
| **Hết cả 3 cặp dự phòng (#1, #2, #3) đều kẹt** | Tạm dừng tải, gắn tag `blocked`, nhắn Telegram và giải phóng slot tải tuần tự cho phim kế tiếp trong hàng đợi. |
| **Series cũ bị nằm rải rác trên cả `disk1` & `disk2`** | Tự động chọn ổ đang chứa nhiều season hơn cho tập mới, đồng thời tạo thẻ `needs-approval` đề xuất PO gộp về 1 ổ. |

## 4. Edge Cases Dev, Memory & Quota/ToS Guardrails

| Tình huống Edge Case | Cách hệ thống xử lý an toàn |
| :--- | :--- |
| **Chạm giới hạn Quota `agy` (HTTP 429)** | Dừng phiên êm ái (graceful stop), lưu điểm dừng vào Comment Kanboard; **tuyệt đối không retry tự động hay xoay tài khoản** (chuẩn ToS Section 6). |
| **Nội bộ `dept-dev` tự sửa lỗi không hội tụ** | Ngắt cứng sau `MAX_RETRY_LOOPS = 2`, gắn tag `blocked` trên Kanboard báo PO can thiệp. |
| **File vượt trần 150 dòng hoặc cố lách luật** | Hook `PreToolUse` (0 token) chặn ngay trước khi commit và chuyển `dev-refactor` tách module. |
| **`MEMORY.md` vượt 100 dòng / trùng ý** | Kích hoạt nén (Compaction) gộp bài học trùng, xóa thông tin cũ, giữ nguyên lịch sử trong Git. |
| **Xung đột 2 phiên mở cùng 1 thẻ Kanboard** | Kiểm tra trạng thái cột trước khi nhận việc: chỉ nhận thẻ ở `Ready`, lập tức kéo sang `In Progress` để khóa quyền sở hữu. |
