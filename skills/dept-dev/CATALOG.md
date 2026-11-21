# Dev Team Skill Catalog (Lazy-Load Index — 18 Skills)

> Chỉ đọc đúng `SKILL.md` cần cho tác vụ hiện tại để tiết kiệm quota. Mọi skill dưới đây đều `<= 120 dòng`, chuẩn `model: inherit`, nguồn tinh lọc từ `rmyndharis/antigravity-skills` (MIT) + quy trình lõi HomeNas.

## Tầng 1 — Tư duy & Kỷ luật Kỹ thuật (10 Skills — Dùng cho MỌI dự án)

| Vai trò Micro-Agent | Skill (`skills/dept-dev/<name>/SKILL.md`) | Trọng tâm |
| :--- | :--- | :--- |
| **Điều phối tổng** | `micro-agent-swarm` | 11 Micro-Agents, trần ≤ 150 dòng/file, max 2 vòng sửa |
| `dev-pm-lead`, `dev-ba` | `context-driven-development` | Phân rã Spec → Track → Task, đồng bộ ngữ cảnh |
| `dev-ux-ui` | `ui-ux-designer` | User flow, wireframe, design token, WCAG AA |
| `dev-architect` | `architecture-patterns` | Clean / Hexagonal Architecture, DDD, Ports & Adapters |
| `dev-architect` | `api-design-principles` | Contract-first REST/RPC, status codes, pagination, idempotency |
| `dev-refactor` | `code-review-excellence` | Review theo mức độ Blocking/Important/Minor & refactor sạch |
| `dev-qa-tester` | `tdd-orchestrator` | TDD Red-Green-Refactor & root-cause debugging |
| `dev-security-reviewer` | `security-auditor` | OWASP Top 10, secrets hygiene, least-privilege |
| `dev-devops` | `deployment-engineer` | Docker multi-stage, CI/CD, healthcheck & rollback |
| `dev-docs-curator` | `docs-architect` | Technical specs, ADR, Mermaid diagrams, Changelog |

## Tầng 2 — Ngôn ngữ & Stack Code (8 Skills — Nạp theo tech stack dự án)

| Stack | Skill (`skills/dept-dev/<name>/SKILL.md`) | Trọng tâm |
| :--- | :--- | :--- |
| **Python** | `python-pro` | Python 3.12+, strict typing, stdlib-first, async hygiene |
| **Python API** | `fastapi-pro` | FastAPI, Pydantic v2, Depends DI, lifespan |
| **Python QA** | `python-testing-patterns` | `pytest`, fixtures, fakes, cache `/tmp` |
| **TypeScript** | `typescript-pro` | Strict TS, discriminated unions, Zod boundary validation |
| **Web UI** | `frontend-developer` | React/Next.js/Vite, component composition & state |
| **CSS / UI** | `tailwind-design-system` | Semantic tokens, dark mode, CVA variants, split-pane layout |
| **Node.js** | `nodejs-backend-patterns` | Layered TS backend, safe `spawn`/WS, graceful shutdown |
| **Web QA** | `e2e-testing-patterns` | Playwright semantic locators, POM, flake-free E2E |
