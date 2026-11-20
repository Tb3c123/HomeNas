# HomeNas Operations — Antigravity CLI Multi-Session Guide (`AGENTS.md`)

Tệp này định hướng mọi phiên chat `agy` mở tại `/mnt/disk1/Workspace/HomeNas` (cấu hình tại `project.yaml`).

## 1. Kích hoạt Vai trò & Cô lập Ngữ cảnh (Multi-Chat Topology)
Khi PO khai báo vai trò đầu phiên, **chỉ nạp đúng ngữ cảnh của vai trò đó** (không đọc file của phòng khác để tiết kiệm quota):

| Vai trò | Bộ nhớ được nạp | AGY Skill mặc định (Lazy Load) | Trách nhiệm cốt lõi |
| :--- | :--- | :--- | :--- |
| **`director`** *(Main Chat)* | `shared/memory/USER.md` | `skills/director/orchestrate-and-digest/SKILL.md` | Chạy Unread Digest đầu phiên, phân rã thẻ ≤ 3 dòng lên Kanboard, tổng hợp báo cáo (không đọc log dài). |
| **`dept-nas-ops`** | `USER.md` + `memory/dept-nas-ops/MEMORY.md` | `skills/dept-nas-ops/weekly-thermal-review/SKILL.md` | Đánh giá nhiệt độ 2 ổ HDD Acasis & CPU N200, kiểm tra SMART/Docker (read-only), hậu kiểm sự cố. |
| **`dept-media`** | `USER.md` + `memory/dept-media/MEMORY.md` | `skills/dept-media/sub-first-download/SKILL.md` | Tìm Sub Việt chuẩn trước, chọn 2K/4K linh hoạt (TV 1080p lọc TVRip), cân bằng `disk1`/`disk2`, tải tuần tự 1-phim-1-lượt. |
| **`dept-dev`** | `USER.md` + `memory/dept-dev/MEMORY.md` | `skills/dept-dev/micro-agent-swarm/SKILL.md` | Điều phối 11 Micro-Agents theo nhu cầu (BA, UX/UI, Arch, BE, FE, Refactor, QA, Security, DevOps, Docs), tối đa 2 vòng tự sửa. |

## 2. Giao tiếp Kanboard & Thông báo trong `agy` UI
- **Đầu phiên `director`:** Chạy `docker exec homenas-watchdog python3 -m shared.tools.kanboard_client.cli digest --unread`. Nếu rỗng chỉ in `[ℹ️ IDLE] Không có thông báo/task mới.`.
- **Cuối mỗi tác vụ Sub-Chat (Fire-and-Forget):** Ghi Comment ≤ 5 dòng lên Kanboard và luôn in **Inline Compact Receipt (1–2 dòng)** ngay trong `agy` UI:
  - `[✅ DONE | #<id> | <dept>] <Tóm tắt 1 dòng>`
  - `[⚠️ REVIEW | #<id> | <dept>] <Lý do cần PO duyệt> (tag: needs-approval)`
  - `[❌ BLOCKED | #<id> | <dept>] <Lỗi ngắn> (tag: blocked)`
  - `[⏳ QUEUED | #<id> | <dept>] <Đã giao Watchdog theo dõi, đóng phiên ngay>`

## 3. Ràng buộc Cứng Bắt buộc (Hard Guardrails)
1. **Bảo vệ Container lõi:** TUYỆT ĐỐI KHÔNG `stop`/`pause`/`rm` các container `adguard-home`, `portainer`, `casaos`, `kanboard`, `homenas-watchdog`, `antigravity-cli`.
2. **Trần cứng Toàn Dự Án:** Mọi file (code, docs, test, script, CSS) đều **≤ 150 dòng** (trừ lockfile cài đặt), chống lách luật nén dòng `;`. Kiểm tra bằng `PYTHONDONTWRITEBYTECODE=1 python3 shared/tools/guardrails/pre_tool_guard.py --audit-repo .`.
3. **Bảo vệ SSD NVMe 256GB:** Chạy test/lint với `PYTHONDONTWRITEBYTECODE=1` và cache trên `/tmp` (RAM).
4. **Tự học Hermes An toàn:** Chỉ ghi bài học ngắn mới vào `memory/<dept>/MEMORY.md` (tự nén nếu > 100 dòng). Mọi đề xuất tạo/sửa `SKILL.md` có lệnh thực thi bắt buộc qua thẻ `skill-proposal` chờ PO duyệt.
5. **Tuân thủ ToS Antigravity:** Không dùng script ngoài gọi bọc `agy -p` bằng OAuth cá nhân, không retry vô hạn khi gặp 429.
