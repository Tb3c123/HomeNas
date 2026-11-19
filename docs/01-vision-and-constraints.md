# 01. Product Vision, Constraints & Core Stack

## 1. Tổng quan & Tầm nhìn (Vision)
**HomeNas (Smart Home AI Orchestrator)** là hệ thống trợ lý quản lý nhà thông minh và hạ tầng Home NAS, vận hành trực tiếp trên nền tảng **Antigravity CLI (`agy`)** triển khai qua Docker trên **CasaOS / Debian**.

- **Đối tượng người dùng:** Cá nhân chủ sở hữu Homelab / Home NAS (Single Power User).
- **Mục tiêu cốt lõi:** Điều phối, giám sát và tự động hóa các tác vụ quản lý hạ tầng, media và phát triển dự án qua CLI; tích hợp Kanban lưu trữ trạng thái công việc và khả năng tự học theo thói quen sử dụng.

## 2. Kiến trúc vận hành cấp cao (High-Level Topology)
- **Multi-Session Project:**
  - **1 Main Chat (Director):** Tiếp nhận yêu cầu, phân rã nhiệm vụ, điều phối phòng ban và kiểm soát ngân sách token.
  - **N Sub-Chats (Workers / Phòng ban):** Mỗi phiên chuyên trách một miền nghiệp vụ độc lập, giữ context cục bộ để tối ưu hiệu năng.
- **Task Memory & Tracking (Kanban):** **Vikunja** (Docker/SQLite, AGPLv3, OpenAPI REST API) làm nguồn sự thật duy nhất (Single Source of Truth) cho trạng thái tác vụ.
- **Self-Learning Mechanism:** Kế thừa mô hình Closed Learning Loop từ **Hermes Agent** (`MEMORY.md`, `USER.md`, `skills/`) nhưng triển khai thuần bằng **AGY Skills + Local Memory** bên trong `agy`.

## 3. Ràng buộc cứng (Hard Constraints)
1. **Tuân thủ tuyệt đối ToS Antigravity (Section 6):**
   - Không bọc `agy` / `agy -p` bên trong agent hay ứng dụng bên thứ 3 bằng tài khoản OAuth cá nhân.
   - Không trích xuất OAuth token, không xoay vòng tài khoản, không script tự động poll `/usage`.
   - Tận dụng tính năng chính thống: `agy` CLI, AGY Skills, MCP Servers cục bộ.
   - Tác vụ giám sát 24/7 chạy bằng script deterministic (Bash/Python); chỉ dùng `GEMINI_API_KEY` riêng nếu cần AI chạy nền không có người kích hoạt.
2. **Kiểm soát chặt chẽ Quota Token:**
   - Cô lập context theo từng Sub-Chat.
   - Áp dụng cơ chế tóm tắt bộ nhớ, truy xuất có chọn lọc và mẫu thực thi tiết kiệm token (*fire-and-forget* cho tác vụ độc lập).
3. **Tổ chức mã nguồn & tài liệu dạng Module:**
   - Chia nhỏ file theo trách nhiệm (Design Patterns / Modular Docs), tránh file phình to gây lãng phí token khi đọc/sửa.
