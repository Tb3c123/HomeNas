# 02. MVP Scope & Department Topology (Sub-Chats)

## 1. Phạm vi MVP (v1.0)

### In-Scope (Triển khai ở v1.0)
- **Hạ tầng Docker (CasaOS/Debian):** Container chạy `agy` CLI kết hợp container **Kanboard** (SQLite) làm Kanban quản lý tác vụ.
- **Kiến trúc Multi-Session:** 1 Main Chat (`director`) điều phối **3 Sub-Chats** chuyên trách với context cô lập.
- **Kết nối Kanban (Single Source of Truth):** Đọc/ghi trạng thái task qua **Kanboard JSON-RPC API** (CLI/MCP cục bộ).
- **An toàn vận hành:** Mặc định ưu tiên thao tác đọc/kiểm tra; bắt buộc xác nhận (Human-in-the-loop) với lệnh có tính phá hủy (xóa dữ liệu, dừng container quan trọng, thay đổi cấu hình mạng).
- **Tự học & Kiểm soát Quota:** Tích hợp AGY Skills + Local Memory (Hermes pattern) và quy chuẩn tiết kiệm token.

### Out-of-Scope (Để sang v2+)
- Phòng ban điều khiển nhà thông minh / IoT (`dept-smarthome`, Home Assistant / MQTT).
- Xây dựng Web UI / Mobile App riêng (sử dụng CLI + Web UI có sẵn của Kanboard & CasaOS).
- Đa người dùng & phân quyền chi tiết cho nhiều thành viên gia đình.
- Điều khiển bằng giọng nói (Voice Assistant / STT / TTS).
- Tự động gọi `agy` 24/7 bằng OAuth không có người kích hoạt (vi phạm ToS).

## 2. Cấu trúc Phòng ban (Multi-Chat Topology)

### 2.1. Main Chat — `director` (Giám đốc điều hành)
- **Vai trò:** Giao tiếp trực tiếp với PO, phân tích yêu cầu, tách nhỏ task, đẩy task lên Kanboard và điều hướng sang đúng Sub-Chat.
- **Nguyên tắc:** Không trực tiếp đọc log dài hay xử lý tác vụ kỹ thuật nặng; chỉ làm việc với bản tóm tắt kết quả và trạng thái Kanban.

### 2.2. 3 Sub-Chats (Phòng ban chuyên trách trong MVP)
1. **`dept-nas-ops` (Hạ tầng & NAS Ops):**
   - Giám sát tài nguyên (CPU, RAM, Disk, nhiệt độ, SMART).
   - Quản lý container Docker / ứng dụng CasaOS, kiểm tra log lỗi, hỗ trợ backup.
2. **`dept-media` (Media & Download):**
   - Quản lý hàng đợi tải xuống (qBittorrent/Aria2/yt-dlp...).
   - Sắp xếp, dọn dẹp và tối ưu dung lượng thư viện media (Jellyfin/Plex/Arr stack).
3. **`dept-dev` (Đội ngũ Dev dự án):**
   - Phát triển, refactor, viết test cho các tool/MCP của HomeNas và các dự án phần mềm cá nhân khác.
   - Quản lý Git branch, PR và tài liệu kỹ thuật.

## 3. Ánh xạ Phòng ban sang Kanban (Kanboard)
- Mỗi phòng ban tương ứng với **1 Swimlane (hoặc Project/Category)** trên Kanboard.
- Luồng cột chuẩn trên Kanban: `Backlog` → `Ready (Assigned)` → `In Progress` → `Waiting Review` → `Done`.
