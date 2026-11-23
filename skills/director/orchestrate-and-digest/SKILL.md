---
name: orchestrate-and-digest
description: Director skill for unread Kanboard digest, task routing across NAS Ops, Media, and solo Tech Secretary (Liam), and 1-turn Project Factory.
---

# Director: Orchestrate, Unread Digest & Copy-Ready Handoff Skill

## 1. Session Start (Unread Digest)
1. Run `docker exec homenas-watchdog python3 -m shared.tools.kanboard_client.cli digest --unread`.
2. Display the output directly in `agy` UI (1 line per updated/completed/alert task, or `[ℹ️ IDLE] Không có thông báo/task mới.`).

## 2. Task Decomposition & Routing (HomeNas Operations Only)
- Never read raw logs or execute heavy system commands in `director` (`Main`).
- **Important:** `HomeNas` does **NOT** have a `Dept-Dev` software department. Only route NAS operational tasks here:
  - Swimlane `NAS Ops` → Khung **`Dept-NasOps`** (`Marcus` — Nhiệt độ, SMART, Docker, Backup)
  - Swimlane `Media & Download` → Khung **`Dept-Media`** (`Elena` — Sub Việt, 2K/4K, Fshare/Drive/TeraBox, `disk1`/`disk2`)
  - Swimlane `Tech Secretary / Scripts` (hoặc `Dev Studio`) → **`Liam (Tech Secretary)`** (Thư ký kỹ thuật đơn lẻ: chỉ hỗ trợ viết/sửa nhỏ script vận hành hệ thống của NAS khi team cần).
- Tag independent read/check tasks with `fire-and-forget` and write/modify tasks with `needs-approval`.

## 3. Xuất Handoff Prompt Copy 1 Chạm (Bắt buộc sau khi tạo Task)
Ngay sau khi tạo xong mỗi thẻ trên Kanboard, **LUÔN in sẵn khối Handoff Prompt** ghi rõ người nhận để PO copy 1 chạm:

```text
📌 Dán vào khung [<Dept-NasOps | Dept-Media | Liam - Tech Secretary>] — Task #<id>:
Vai trò: <dept-nas-ops | dept-media | tech-secretary>. Nhận và xử lý thẻ #<id> trên Kanboard theo đúng AGENTS.md (đọc mượt không hỏi lặt vặt; nếu có thêm/xóa/sửa hãy trình Action Plan ≤ 8 dòng chờ tôi duyệt 1 lần; xong việc ghi Comment ≤ 5 dòng lên Kanboard, in Inline Receipt và xuất Return Prompt dán về Main).
```

## 4. Nhận Return Prompt từ Sub-Chat
Khi PO dán dòng `Báo cáo <role> | #<id> | <STATUS> | <Tóm tắt>` vào `Main`:
- Chạy nhanh `digest --unread` để đồng bộ trạng thái Kanboard.
- Nếu `DONE` → xác nhận gọn 1 dòng & đề xuất task tiếp theo (nếu có).
- Nếu `REVIEW` / `BLOCKED` → tóm tắt ngắn điểm cần PO quyết định và chờ PO duyệt rồi xuất Handoff Prompt bước kế tiếp.

## 5. Khởi tạo Dự án Phần mềm Mới (Project Factory — Chạy Thẳng 1 Lượt)
Khi PO nhắn trong `Main` yêu cầu tạo/khởi động dự án phần mềm mới (VD: *"Khởi động dự án X — mô tả..."*):
- **TUYỆT ĐỐI KHÔNG giao cho `Liam` trong `HomeNas` và KHÔNG dừng lại hỏi Action Plan**.
- Tự chạy ngầm ngay: `docker exec homenas-watchdog python3 -m shared.tools.project_loader.scaffold --name "<TenDuAn>" --summary "<MoTa>"`.
- Chỉ hiển thị ra màn hình **Hướng dẫn 2 bước mở dự án trên giao diện + Khung Prompt Khởi động copy 1 chạm** do tool xuất ra.
