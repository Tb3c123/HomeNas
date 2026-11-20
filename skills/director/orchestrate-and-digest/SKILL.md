---
name: orchestrate-and-digest
description: Director skill for unread Kanboard digest, task routing across 4 sidebar chats, copy-ready handoff prompts, and token budget shielding.
---

# Director: Orchestrate, Unread Digest & Copy-Ready Handoff Skill

## 1. Session Start (Unread Digest)
1. Run `docker exec homenas-watchdog python3 -m shared.tools.kanboard_client.cli digest --unread`.
2. Display the output directly in `agy` UI (1 line per updated/completed/alert task, or `[ℹ️ IDLE] Không có thông báo/task mới.`).

## 2. Task Decomposition & Routing
- Never read raw logs or execute heavy system commands in `director` (`Main`).
- Decompose PO requests into concise Kanboard cards (`<= 3 lines` description) via `kb create --swimlane "<name>" --col Ready --tags "<tags>"`:
  - Swimlane `NAS Ops` → Khung sidebar **`Dept-NasOps`**
  - Swimlane `Media & Download` → Khung sidebar **`Dept-Media`**
  - Swimlane `Dev Studio` → Khung sidebar **`Dept-Dev`**
- Tag independent read/check tasks with `fire-and-forget` and write/modify tasks with `needs-approval`.

## 3. Xuất Handoff Prompt Copy 1 Chạm (Bắt buộc sau khi tạo Task)
Ngay sau khi tạo xong mỗi thẻ trên Kanboard, **LUÔN in sẵn khối Handoff Prompt** ghi rõ khung chat đích để PO copy 1 chạm dán sang:

```text
📌 Dán vào khung [<Dept-NasOps | Dept-Media | Dept-Dev>] — Task #<id>:
Vai trò: <dept-nas-ops | dept-media | dept-dev>. Nhận và xử lý thẻ #<id> trên Kanboard theo đúng AGENTS.md (đọc mượt không hỏi lặt vặt; nếu có thêm/xóa/sửa hãy trình Action Plan ≤ 8 dòng chờ tôi duyệt 1 lần; xong việc ghi Comment ≤ 5 dòng lên Kanboard, in Inline Receipt và xuất Return Prompt dán về Main).
```

## 4. Nhận Return Prompt từ Sub-Chat
Khi PO dán dòng `Báo cáo <dept> | #<id> | <STATUS> | <Tóm tắt>` vào `Main`:
- Chạy nhanh `digest --unread` để đồng bộ trạng thái Kanboard.
- Nếu `DONE` → xác nhận gọn 1 dòng & đề xuất task tiếp theo (nếu có).
- Nếu `REVIEW` / `BLOCKED` → tóm tắt ngắn điểm cần PO quyết định và chờ PO duyệt rồi xuất Handoff Prompt bước kế tiếp.

## 5. Khởi tạo Dự án Phần mềm Mới (Project Factory)
Khi PO nhắn trong `Main` yêu cầu tạo dự án mới (VD: *"Tạo dự án A — mô tả..."*):
1. Chạy `docker exec homenas-watchdog python3 -m shared.tools.project_loader.scaffold --name "<TenDuAn>" --summary "<MoTa>"` để tự tạo thư mục `/mnt/disk1/Workspace/<TenDuAn>/` (kèm `project.yaml`, `AGENTS.md`, `memory/MEMORY.md`) và khởi tạo Project riêng trên Kanboard.
2. In nguyên khối **`🚀 Dán vào khung chat mới tại thư mục [...]`** trả về cho PO copy 1 chạm mang sang dự án mới chat ngay (KHÔNG code dự án ngoài bên trong `HomeNas`).
