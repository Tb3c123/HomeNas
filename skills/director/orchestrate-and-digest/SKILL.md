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
Vai trò: <dept-nas-ops | dept-media | dept-dev>. Nhận và xử lý thẻ #<id> trên Kanboard theo đúng AGENTS.md (đọc mượt không hỏi lặt vặt; nếu có thêm/xóa/sửa hãy trình Action Plan ≤ 8 dòng chờ tôi duyệt 1 lần; xong việc ghi Comment ≤ 5 dòng lên Kanboard và in Inline Receipt).
```
