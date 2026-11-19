# 05. User Flows & Inter-Session Communication

## 1. Flow 1: Điều phối Tác vụ (Main Chat ↔ Kanboard ↔ Sub-Chat)

Kanboard đóng vai trò **Message Bus & Single Source of Truth**, giúp Main Chat và Sub-Chats giao tiếp bất đồng bộ, cô lập hoàn toàn context và tuân thủ 100% ToS Antigravity.

```mermaid
sequenceDiagram
    actor PO as Product Owner
    participant DIR as Main Chat (director)
    participant KB as Kanboard (JSON-RPC)
    participant SUB as Sub-Chat (dept-*)

    PO->>DIR: Giao yêu cầu tổng quát
    DIR->>KB: Tạo Task (Swimlane phòng ban, Cột: Ready)
    DIR-->>PO: Xác nhận danh sách Task ID đã phân công

    PO->>SUB: Mở phiên phòng ban / Kích hoạt xử lý
    SUB->>KB: Lấy Task ở cột Ready (đúng Swimlane)
    SUB->>KB: Chuyển trạng thái -> In Progress
    SUB->>SUB: Nạp USER.md + MEMORY.md + 1 Skill (Lazy Load)
    SUB->>SUB: Chạy Tool cục bộ (Zero-Noise Output)
    SUB->>KB: Ghi Comment tóm tắt (≤ 5 dòng) -> Waiting Review / Done
    SUB-->>PO: In Inline Receipt (1-2 dòng) trong agy UI & Reset phiên

    PO->>DIR: Mở lại Main Chat / Hỏi tiến độ
    DIR->>KB: Chạy kanboard-client digest --unread
    DIR-->>PO: Hiển thị Bảng tin chưa đọc (1 dòng/task) ngay trong agy UI
```

## 2. Flow 2: Chế độ Fire-and-Forget (Kèm Thông báo tại `agy` UI)

Áp dụng cho tác vụ độc lập, không cần tương tác nhiều lượt (VD: kiểm tra SMART ổ cứng, xem hàng đợi tải, kiểm tra dung lượng đĩa):

```mermaid
flowchart LR
    A["Task gắn tag: fire-and-forget"] --> B["Sub-Chat đọc đề bài từ Kanboard"]
    B --> C["Chạy 1 Tool/Skill đã lọc nhiễu"]
    C --> D{"An toàn & Không lỗi?"}
    D -->|"Có"| E["Ghi Comment ≤5 dòng -> Cột Done"]
    D -->|"Cần xóa/sửa nặng hoặc Lỗi"| F["Gắn tag needs-approval / blocked -> Cột Waiting Review"]
    E --> N["In Inline Receipt (1-2 dòng) ngay trong agy UI"]
    F --> N
    N --> G["Đóng & Reset phiên ngay"]
```

### Quy chuẩn Thông báo trong `agy` UI (Không cần chuyển sang Kanboard)
1. **Inline Compact Receipt (Tức thời tại Sub-Chat):** Luôn in 1–2 dòng tóm tắt trước khi kết thúc phiên theo mẫu:
   - `[✅ DONE | #<id> | <dept>] <Tóm tắt ngắn 1 dòng>`
   - `[⚠️ REVIEW | #<id> | <dept>] <Lý do cần PO duyệt> (tag: needs-approval)`
   - `[❌ BLOCKED | #<id> | <dept>] <Lỗi ngắn gọn> (tag: blocked)`
2. **Unread Digest (Tổng hợp tại Main Chat `director`):** Khi PO mở lại `director`, tự động (hoặc theo lệnh) gọi `kanboard-client digest --unread` đối chiếu mốc `.state/last_digest_ts` để chỉ hiển thị các task mới hoàn thành/cần duyệt chưa xem, mỗi task đúng 1 dòng.

## 3. Flow 3: Vòng lặp Tự học (Hermes Closed Learning Loop)

Chạy gọn ở bước cuối mỗi Task (chỉ kích hoạt khi có tri thức mới hoặc PO góp ý sửa lỗi):

```mermaid
flowchart TD
    T["Hoàn tất Task / PO góp ý"] --> Q{"Có bài học mới đáng nhớ?"}
    Q -->|"Không"| END["Kết thúc (0 token thừa)"]
    Q -->|"Fact / Kinh nghiệm ngắn"| M["Ghi 1-2 dòng vào memory/<dept>/MEMORY.md"]
    M --> C{"Vượt 100 dòng?"}
    C -->|"Có"| COMP["Tự nén (Compact) các mục cũ"]
    C -->|"Không"| END
    COMP --> END
    Q -->|"Quy trình lặp lại (SOP/Lệnh)"| S["Tạo nháp skills/<dept>/<name>.md"]
    S --> REV["Gắn tag skill-proposal -> Waiting Review + In thông báo trong agy UI"]
```

## 4. Quy tắc Đồng bộ & Ngăn xung đột
- **Chủ sở hữu thẻ:** Tại một thời điểm, chỉ 1 Sub-Chat xử lý thẻ ở cột `In Progress`.
- **Chốt chặn phá hủy (Human-in-the-Loop):** Mọi lệnh xóa file, dừng/xóa container Docker hoặc sửa cấu hình mạng đều **không được tự chạy ở chế độ Fire-and-Forget**; bắt buộc đẩy về `Waiting Review` kèm tag `needs-approval` và in cảnh báo `[⚠️ REVIEW]` ngay trong `agy` UI.
