# Shared Dev Team Operating Constitution (`DEV_TEAM_RULES.md`)

> **Live-Linked Rulebook:** Mọi dự án tạo từ `HomeNas` Project Factory đều kế thừa trực tiếp tệp này. Khi `HomeNas` cập nhật quy trình, skills hoặc guardrails, **tất cả các dự án con tự động nhận bản nâng cấp mới nhất ngay lập tức** mà không cần sửa từng dự án.

## 1. Đội hình 11 Micro-Agents (On-Demand — Chỉ gọi đúng vai trò cần dùng)
- **Product & Design:** `dev-pm-lead` (Điều phối & Spec), `dev-ba` (Nghiệp vụ & Edge cases), `dev-ux-ui` (User flow, Design System, WCAG AA).
- **Architecture & Coding:** `dev-architect` (Clean/Hexagonal/ADR/API Contract), `dev-backend`, `dev-frontend`, `dev-refactor` (Code Review & chống phình dòng).
- **QA, Security & Delivery:** `dev-qa-tester` (TDD Red-Green-Refactor), `dev-security-reviewer` (OWASP/STRIDE/Secrets), `dev-devops` (Docker/CI-CD/Rollback), `dev-docs-curator` (Docs/Mermaid/Changelog).

## 2. Cơ chế Nạp Ngữ cảnh & 48+ Dev Skills (Lazy Load)
1. **Đầu phiên:** Đọc `/mnt/disk1/Workspace/HomeNas/shared/memory/USER.md` + `./memory/MEMORY.md` của dự án hiện tại.
2. **Tra cứu Kỹ năng:** Đọc bảng mục lục `/mnt/disk1/Workspace/HomeNas/skills/dept-dev/CATALOG.md` (48 skills qua 6 lĩnh vực) và **chỉ mở đúng 1–2 tệp `SKILL.md` phù hợp với tác vụ đang làm**.
3. **Giao tiếp Liên-Agent:** Bàn giao qua Contract Files gọn (`<= 60 dòng`) và gói tin `STATUS | FILE | ACTION`. Tối đa **2 vòng tự sửa (`MAX_RETRY_LOOPS = 2`)** giữa Coder và QA/Reviewer; nếu vẫn lỗi thì gắn `blocked` trên Kanboard và báo PO.

## 3. Ràng buộc Cứng & Tự học Minh bạch (Hard Guardrails)
1. **Trần cứng Toàn Dự Án:** Mọi file (`code`, `docs`, `test`, `script`, `CSS`, skill tự viết nội bộ) đều **`<= 150 dòng`** (cấm nén dòng bằng `;`). Riêng `skills/**/SKILL.md` nguồn ngoài nạp qua sàng lọc 2 bước (HomeNas Manager `:8090` / `fetcher.py`) được phép tối đa **`<= 1000 dòng / 64 KB`** (chặn cứng `curl|sh`, `rm -rf`, `git --force`, dừng 6 container lõi, `/etc/shadow`, prompt injection). Kiểm tra bằng:
   `PYTHONDONTWRITEBYTECODE=1 python3 /mnt/disk1/Workspace/HomeNas/shared/tools/guardrails/pre_tool_guard.py --audit-repo .`
2. **Bảo vệ SSD NVMe:** Mọi lệnh test/build/cache đều đẩy vào `/tmp` (`PYTHONDONTWRITEBYTECODE=1`, `cache_dir=/tmp/.pytest_cache`).
3. **Tự học Hermes Minh bạch (`💾 Memory`):** Khi phát hiện bài học/workaround mới, bắt buộc gọi CLI:
   `python3 /mnt/disk1/Workspace/HomeNas/shared/tools/memory_manager/cli.py <add|patch|remove> --dept <project-slug> ...`
   và **in nguyên dòng badge `💾 Memory [<project-slug>] ➕/✏️ ...` ra khung chat** để PO kiểm chứng.
4. **Đọc mượt 100% — Trình Action Plan trước khi Sửa:** Tự chạy mượt mọi lệnh chỉ đọc/test/kiểm tra. Trước khi thêm/xóa/sửa code, cấu hình hoặc container, trình **Action Plan `<= 8 dòng`** chờ PO duyệt **1 lần duy nhất**, sau đó tự thực thi trọn gói.
