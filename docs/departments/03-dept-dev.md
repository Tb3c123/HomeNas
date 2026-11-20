# Department 03: `dept-dev` (Full Product Team, Line-Cap Law & Direct-Fetch Skills)

## 1. Phạm vi & Không gian Làm việc
- **Workspace thực tế:** `/mnt/disk1/Workspace/` (mount sẵn trong `antigravity-cli`).
- **Nhiệm vụ kép:** (1) Xây mới & bảo trì toàn bộ công cụ lõi HomeNas; (2) Phát triển hoàn chỉnh các dự án sản phẩm cá nhân khác (Multi-Project qua `project.yaml`).

## 2. Đội hình 11 Micro-Agents Đầy đủ (On-Demand / Lazy-Invoked)

Chỉ kích hoạt đúng 2–4 agent cần cho từng thẻ task (qua `agy` subagents / `/run-workflow`) để tối ưu quota:

| Khối | Micro-Agent | Trách nhiệm cốt lõi |
| :--- | :--- | :--- |
| **Product & Design** | `dev-pm-lead` | Nhận thẻ Kanboard, chốt scope, phân rã task, điều phối đúng agent, báo cáo ≤ 5 dòng. |
| | `dev-ba` | Phân tích nghiệp vụ, viết User Stories, Acceptance Criteria & Edge Cases trước khi thiết kế. |
| | `dev-ux-ui` | Thiết kế User Flow, Wireframe, Design System, Responsive & Empty/Loading/Error states. |
| **Arch & Eng** | `dev-architect` | Chọn Design Pattern, thiết kế kiến trúc hệ thống, DB Schema & API Contract (BE ↔ FE). |
| | `dev-backend` | Triển khai API, business logic, DB repository, CLI/MCP tools, workers đúng Contract. |
| | `dev-frontend` | Triển khai giao diện UI/UX, state management, kết nối API đúng thiết kế `dev-ux-ui`. |
| | `dev-refactor` | Tách file chạm trần dòng, khử trùng lặp, giữ cấu trúc sạch dễ chỉnh sửa. |
| **QA & Delivery** | `dev-qa-tester` | Viết & chạy Unit/Integration/E2E test + Linter (cache RAM `/tmp`), đối chiếu tiêu chí BA. |
| | `dev-security-reviewer` | Review độc lập diff: bảo mật (OWASP, secrets), logic, Pattern & **luật trần dòng**. |
| | `dev-devops` | Multi-stage Dockerfile, Docker Compose chuẩn CasaOS, CI/CD, healthcheck & rollback. |
| | `dev-docs-curator` | Chia nhỏ docs `.md`, cập nhật `CHANGELOG.md`, tải lẻ & thẩm định `SKILL.md` cho cả team. |

## 3. Giao thức Tự trao đổi Nội bộ & Liên Phòng ban
- **Nội bộ 11 Agents (`agy` subagents + `send_message` + `/run-workflow`):** Tự động truyền giao giữa các vai trò (`BA` → `UX/UI` & `Architect` → `BE`/`FE` song song → `QA` ↔ `Coder` tự sửa → `Security Reviewer`).
  - *Chống đốt quota:* Trao đổi qua **Contract File ngắn (≤ 60 dòng)**; tin nhắn nén 3–5 dòng (`STATUS | FILE | ACTION`); **giới hạn cứng tối đa 2 vòng Ping-Pong (`MAX_RETRY_LOOPS = 2`)** — quá 2 vòng vẫn lỗi sẽ tự dừng, gắn tag `blocked` trên Kanboard báo PO.
- **Liên phòng ban (`dept-dev` ↔ `dept-nas-ops` ↔ `dept-media`):** Bất đồng bộ qua **Kanboard Message Bus** (phòng khác tạo thẻ vào Swimlane `Dev Studio` cột `Ready`, 0-token waiting, chuẩn ToS).

## 4. Luật Cứng Trần Số Dòng Toàn Dự Án & Design Patterns
- **Trần cứng toàn dự án:** **≤ 150 dòng/file** áp dụng cho **MỌI file** (source code, docs `.md`, test, script, CSS, config logic). *Ngoại lệ duy nhất:* file cài đặt/lock sinh tự động (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `uv.lock`, `poetry.lock`, `requirements.txt`).
- **Chống lách luật (Anti-Bypass):** Cấm gộp nhiều lệnh lên 1 dòng (semicolon chaining/minify) hay nhồi nhiều trách nhiệm vào 1 file. Kiểm tra tự động **0-token qua `hooks.json` (`wc -l`)** trước khi commit — vi phạm sẽ chặn và gọi `dev-refactor` tách file ngay.
- **Design Patterns tự chọn theo bài toán (`dev-architect`):**
  - *Creational:* Factory, Builder, Dependency Injection.
  - *Structural:* Adapter, Facade, Decorator/Middleware, Repository.
  - *Behavioral:* Strategy, State Machine, Observer/Event Bus, Command, Chain of Responsibility.
  - *Architectural:* Clean/Hexagonal, Plugin Architecture, Pipeline/Filter, Feature-Sliced Design (FE).

## 5. Chiến lược Bộ Skill Toàn Đội (Tải Lẻ Trực Tiếp — Không Cài Đặt Thừa)
- **Nguyên tắc:** Trừ `google/skills` (cài qua `agy plugin install`), mọi skill khác được `dev-docs-curator` **tải trực tiếp từng file `SKILL.md` riêng lẻ** bằng `curl` từ raw GitHub vào `skills/<dept>/<name>/SKILL.md` (không cài CLI/npm thừa) → đọc kiểm duyệt an toàn → chờ PO duyệt (`skill-proposal`).
- **Bản đồ Kho Skill Mở (`SKILL.md`) theo Vai trò:**
  - **PM & BA:** `brainstorming`, `writing-plans` (`obra/superpowers`), `prd-writer` / `user-stories` (`sickn33/agentic-awesome-skills`).
  - **UX/UI & Frontend:** `frontend-design` (`anthropics/skills`), `web-design-guidelines` & `react-best-practices` (`vercel-labs/agent-skills`), `ui-ux-audit` (`rmyndharis/antigravity-skills`).
  - **Architect & Backend:** `mcp-builder` (`anthropics/skills`), `systematic-debugging` (`obra/superpowers`), `api-design` & `database-design` (`sickn33/agentic-awesome-skills`, `VoltAgent/awesome-agent-skills`).
  - **QA & Security:** `test-driven-development`, `requesting-code-review` (`obra/superpowers`), `webapp-testing` (`anthropics/skills`), `security-audit` (`rmyndharis/antigravity-skills`).
  - **DevOps, NAS Ops & Media:** `docker-expert` & `linux-sysadmin` (`sickn33/agentic-awesome-skills`), `skill-creator` (`anthropics/skills`), kết hợp Skill nội bộ `dept-nas-ops` & `dept-media`.

## 6. Low-Wear CI & Phân quyền
- **Bảo vệ cứng (`hooks.json` `PreToolUse` — 0 Token):** Chặn `git push --force`, `git reset --hard`, file vượt 150 dòng, và lệnh deploy đè container CasaOS khi chưa có PO duyệt.
- **Bắt buộc PO duyệt (`needs-approval`):** Merge vào `main`, deploy/build đè container CasaOS, xóa nhánh/repo, hoặc kích hoạt chính thức Skill mới (`skill-proposal`).
