# 03. Self-Learning Strategy (Hermes Pattern) & Token Budget

## 1. Kiến trúc Tự học 3 tầng (Kế thừa Hermes Agent)

Hệ thống không retrain model mà áp dụng **Closed Learning Loop** (Thực thi → Đánh giá → Trích xuất → Tinh chỉnh) thông qua bộ nhớ dạng file cục bộ và **AGY Skills** (100% tuân thủ ToS Antigravity):

| Tầng | Đường dẫn | Phạm vi & Mục đích | Ngưỡng kích thước |
| :--- | :--- | :--- | :--- |
| **Tầng 1: User Profile** | `memory/USER.md` | Thói quen, sở thích và quy tắc cứng của PO dùng chung toàn dự án. | ≤ 300 tokens |
| **Tầng 2: Dept Memory** | `memory/<dept>/MEMORY.md` | Kinh nghiệm, lỗi hay gặp và ngữ cảnh dài hạn riêng của từng phòng ban. | ≤ 100 dòng (~800 tokens) |
| **Tầng 3: Skills** | `skills/<dept>/*.md` | Quy trình chuẩn (SOP/Runbook) tái sử dụng dưới dạng AGY Skills. | Nạp theo yêu cầu (Lazy Load) |

### Quy tắc kiểm duyệt tự học (Memory Poisoning Guard)
- **Ghi nhận sự thật (Facts):** Sub-Chat chỉ ghi vào `MEMORY.md` khi xuất hiện bài học mới có giá trị lặp lại; tự động nén (compact) khi chạm ngưỡng dòng; mọi thay đổi đều được Git theo dõi.
- **Tạo/Sửa Skill thực thi:** Mọi đề xuất tạo mới hoặc chỉnh sửa `skills/<dept>/*.md` có chứa lệnh hệ thống **bắt buộc qua xác nhận của PO** để ngăn chặn việc tự học quy trình sai hoặc mất an toàn.

## 2. Chiến lược Kiểm soát Quota Token

1. **Fire-and-Forget Pattern:** Tác vụ độc lập (kiểm tra hệ thống, dọn dẹp, kiểm tra tiến độ tải) chạy theo phiên ngắn hạn, xuất kết quả tóm tắt (≤ 5 dòng) vào thẻ **Kanboard** và kết thúc ngay, không duy trì lịch sử hội thoại dài.
2. **Stateless Session per Task:** Trạng thái công việc lưu tại **Kanboard**, tri thức dài hạn lưu tại **`memory/`** → Sub-Chat reset context sau mỗi task hoàn thành để tránh phình input token.
3. **Zero-Noise Tool Output:** Mọi CLI/MCP script phải lọc, cắt gọn (ví dụ: `--tail`, `grep`, JSON rút gọn) trước khi trả kết quả về LLM.
4. **Director Context Shield:** Main Chat (`director`) chỉ tiếp nhận bản tóm tắt trạng thái từ Kanboard/Sub-Chats, không đọc raw log hay mã nguồn chi tiết.
5. **Model Tiering:** Phân bổ model nhẹ/nhanh cho routing, cập nhật Kanboard và đọc metric cơ bản; chỉ dùng model năng lực cao cho debug phức tạp hoặc phát triển tính năng tại `dept-dev`.
