# Shared Dev Team Operating Constitution (`DEV_TEAM_RULES.md`)

> **Live-Linked Rulebook (`/mnt/disk1/Workspace/shared`):** Mọi dự án tạo từ Project Factory đều kế thừa trực tiếp tệp này qua không gian tên độc lập `/mnt/disk1/Workspace/shared/...`. Khi lớp nền tảng cập nhật quy trình, skills hoặc guardrails, **tất cả các dự án con tự động nhận bản nâng cấp mới nhất ngay lập tức**.

## 1. Đội hình 11 Micro-Agents (On-Demand — Chỉ gọi đúng vai trò cần dùng)
- **Product & Design:** `dev-pm-lead` (Điều phối & Spec), `dev-ba` (Nghiệp vụ & Edge cases), `dev-ux-ui` (User flow, Design System, WCAG AA).
- **Architecture & Coding:** `dev-architect` (Clean/Hexagonal/ADR/API Contract), `dev-backend`, `dev-frontend`, `dev-refactor` (Code Review & chống phình dòng).
- **QA, Security & Delivery:** `dev-qa-tester` (TDD Red-Green-Refactor), `dev-security-reviewer` (OWASP/STRIDE/Secrets), `dev-devops` (Docker/CI-CD/Rollback), `dev-docs-curator` (Docs/Mermaid/Changelog).

## 2. Cơ chế Nạp Ngữ cảnh & 78 Dev Skills (Lazy Load qua `/Workspace/shared`)
1. **Đầu phiên:** Đọc `/mnt/disk1/Workspace/shared/memory/USER.md` + `./memory/MEMORY.md` của dự án hiện tại.
2. **Tra cứu Kỹ năng:** Đọc bảng mục lục `/mnt/disk1/Workspace/shared/skills/dept-dev/CATALOG.md` (78 skills qua 8 lĩnh vực) và **chỉ mở đúng 1–2 tệp `SKILL.md` phù hợp với tác vụ đang làm**.
3. **Bộ 5 MCP Plugins Chuyên Dụng (`sync_mcp_plugins.py`):** Mặc định tắt (`disabled: true`) để giữ nhẹ ngữ cảnh cho `Main/NAS/Media`; bật theo nhu cầu dự án Dev (`agy plugin enable <name>`):
   - `mcp-context7`: Tra cứu tài liệu thư viện phiên bản mới nhất (`https://mcp.context7.com/mcp`).
   - `mcp-github`: Quản lý PR/Issue/Actions qua `GITHUB_PERSONAL_ACCESS_TOKEN`.
   - `mcp-sqlite-ro`: Soi DB SQLite (`Kanboard`, `*arr`, project DB) ở chế độ **Read-Only 3 lớp** (`/mnt/disk1/Workspace/shared/tools/mcp_servers/sqlite_ro_mcp.py`).
   - `mcp-playwright`: Kiểm thử giao diện Web headless qua container on-demand (`playwright-mcp` `:8931`).
   - `mcp-code-graph-rag`: Phân tích AST/Call-Graph đa ngôn ngữ qua `code-graph-rag[treesitter-full,ast-grep]` (`uv tool install --python 3.12`) + SQLite nhúng (`SQLITE_GRAPH_PATH=/mnt/disk1/Workspace/.cache/cgr/graph.sqlite`, không Memgraph/semantic).
4. **Giao tiếp Liên-Agent:** Bàn giao qua Contract Files gọn (`<= 60 dòng`) và gói tin `STATUS | FILE | ACTION`. Tối đa **2 vòng tự sửa (`MAX_RETRY_LOOPS = 2`)** giữa Coder và QA/Reviewer; nếu vẫn lỗi thì gắn `blocked` trên Kanboard và báo PO.

## 3. Ràng buộc Cứng & Tự học Minh bạch (Hard Guardrails)
1. **Trần cứng Toàn Dự Án:** Mọi file (`code`, `docs`, `test`, `script`, `CSS`, skill tự viết nội bộ) đều **`<= 150 dòng`** (cấm nén dòng bằng `;`). Riêng `skills/**/SKILL.md` nguồn ngoài nạp qua sàng lọc 2 bước (HomeNas Manager `:8090` / `fetcher.py`) được phép tối đa **`<= 1000 dòng / 64 KB`** (chặn cứng `curl|sh`, `rm -rf`, `git --force`, dừng 6 container lõi, `/etc/shadow`, prompt injection). Kiểm tra bằng:
   `PYTHONDONTWRITEBYTECODE=1 python3 /mnt/disk1/Workspace/shared/tools/guardrails/pre_tool_guard.py --audit-repo .`
2. **Bảo vệ SSD NVMe & Tránh Nghẽn USB HDD:** Mọi lệnh test/build/cache/SQLite test đều đẩy vào `/tmp` (`PYTHONDONTWRITEBYTECODE=1`, `cache_dir=/tmp/.pytest_cache`, `DATABASE_URL=sqlite+aiosqlite:////tmp/<app>_test.db`) để tránh ghi rác SSD và tránh nghẽn `fsync` trên USB HDD `/mnt/disk1`.
3. **Tự học Hermes Minh bạch (`💾 Memory`):** Khi phát hiện bài học/workaround mới, bắt buộc gọi CLI:
   `python3 /mnt/disk1/Workspace/shared/tools/memory_manager/cli.py <add|patch|remove> --dept <project-slug> ...`
   và **in nguyên dòng badge `💾 Memory [<project-slug>] ➕/✏️ ...` ra khung chat** để PO kiểm chứng.
4. **Đọc mượt 100% — Trình Action Plan trước khi Sửa:** Tự chạy mượt mọi lệnh chỉ đọc/test/kiểm tra. Trước khi thêm/xóa/sửa code, cấu hình hoặc container, trình **Action Plan `<= 8 dòng`** chờ PO duyệt **1 lần duy nhất**, sau đó tự thực thi trọn gói.
5. **Chuẩn Đóng Gói CasaOS Native App (Cấm để thành `Legacy App`):** Khi PO yêu cầu build/deploy app lên CasaOS, đội Dev BẮT BUỘC dùng mô hình **2 tệp Compose**:
   - `docker-compose.yml`: Dùng để build local với `build:` + gắn thẻ `image: <app-slug>-<svc>:latest` (chỉ chạy `docker compose build`, **KHÔNG tự chạy `docker compose up -d`** gây `Legacy App`).
   - `casaos-compose.yml`: **TUYỆT ĐỐI KHÔNG có trường `build:`**, chỉ trỏ tới các image đã build sẵn (`image: <app-slug>-<svc>:latest`), có đủ metadata `x-casaos:` (root & services), `store_app_id: <app-slug>`, và `is_uncontrolled: false`.
   - **Tránh trùng cổng Host đã chiếm:** Luôn kiểm tra trước khi chọn port; KHÔNG dùng các cổng đã chiếm: `3000` (AdGuard Home), `8000` (Portainer), `8085` (Kanboard), `8090` (HomeManager), `8096` (Jellyfin), `7681` (antigravity-cli).
   - Sau khi PO duyệt deploy, gọi `python3 /mnt/disk1/Workspace/shared/tools/project_loader/casaos_apply.py --app <app-slug> --file /mnt/disk1/Workspace/<app-slug>/casaos-compose.yml --wait 10` (Host Keeper tự `apply`, gặp `404` tự fallback `install -f` thành Native App).
