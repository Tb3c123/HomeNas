# Dev Team Skill Catalog (Lazy-Load Index — 48 Skills)

> Chỉ đọc đúng `SKILL.md` cần cho tác vụ hiện tại để tiết kiệm quota. Mọi skill đều `<= 60 dòng`, `model: inherit`, nguồn tinh lọc từ `rmyndharis/antigravity-skills` (MIT) + quy trình lõi HomeNas.

## 1. Quy trình, Sản phẩm & Kiến trúc Hệ thống (10 Skills)
| Skill (`skills/dept-dev/<name>/SKILL.md`) | Trọng tâm |
| :--- | :--- |
| `micro-agent-swarm` | Điều phối 11 Micro-Agents, ≤ 150 dòng/file, max 2 vòng sửa |
| `context-driven-development` | Phân rã Spec → Track → Task, đồng bộ ngữ cảnh |
| `ui-ux-designer` | User flow, wireframe, design tokens, WCAG AA |
| `architecture-patterns` | Clean / Hexagonal Architecture, DDD, Ports & Adapters |
| `api-design-principles` | Contract-first REST/RPC, status codes, pagination, idempotency |
| `microservices-patterns` | Bounded contexts, circuit breakers, async outbox |
| `event-sourcing-architect` | Append-only event logs, CQRS, idempotent projections |
| `performance-engineer` | Profiling, p95/p99 latency, caching, memory bounds |
| `monorepo-architect` | Acyclic package graph, shared libs, affected-only CI |
| `docs-architect` | Technical specs, ADR, Mermaid diagrams, Changelog |

## 2. Dữ liệu & Cơ sở dữ liệu (5 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `database-architect` | Relational modeling, constraints, indexing, retention |
| `postgresql` | EXPLAIN ANALYZE, B-tree/GIN, JSONB, SKIP LOCKED |
| `sql-optimization-patterns` | Kill N+1, composite indexes, keyset pagination |
| `database-migration` | Zero-downtime expand-contract, concurrent indexes, rollback |
| `data-engineer` | Idempotent ETL/ELT, schema validation, dead-letter queues |

## 3. AI / LLM & Multi-Agent Engineering (5 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `ai-engineer` | Provider adapters, structured outputs, token budget, ToS safety |
| `prompt-engineering-patterns` | System prompts, few-shot, anti-prompt-injection delimiters |
| `rag-implementation` | Semantic chunking, hybrid BM25+vector, reranking, citations |
| `llm-evaluation` | Golden datasets, layered graders, accuracy/latency/cost gates |
| `agent-orchestration-multi-agent-optimize` | Context isolation, compact handoffs, bounded retry loops |

## 4. Ngôn ngữ, Web & Mobile (13 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `python-pro` | Python 3.12+, strict typing, stdlib-first, async hygiene |
| `fastapi-pro` | FastAPI, Pydantic v2, Depends DI, lifespan |
| `typescript-pro` | Strict TS, discriminated unions, Zod boundary validation |
| `frontend-developer` | React/Next.js/Vite, component composition & state |
| `tailwind-design-system` | Semantic tokens, dark mode, CVA variants, split-pane layout |
| `nodejs-backend-patterns` | Layered TS backend, safe `spawn`/WS, graceful shutdown |
| `golang-pro` | Idiomatic Go, small interfaces, `context`, `-race` concurrency |
| `rust-pro` | Ownership/borrowing, `Result`/no-unwrap, Tokio async, clippy |
| `java-pro` | Java 21+, records, sealed types, virtual threads, JUnit 5 |
| `csharp-pro` | .NET 8+, nullable safety, `CancellationToken`, EF Core |
| `flutter-expert` | `const` widgets, Riverpod/Bloc state, cross-platform responsive |
| `react-native-architecture` | Typed navigation, FlashList, offline sync, SecureStore |
| `bash-pro` | Defensive Bash (`set -euo pipefail`), quoting, `trap` cleanup |

## 5. Chất lượng, Kiểm thử, Debug & Bảo mật (10 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `code-review-excellence` | Review theo mức độ Blocking/Important/Minor & refactor sạch |
| `tdd-orchestrator` | TDD Red-Green-Refactor & bounded retry loops |
| `python-testing-patterns` | `pytest`, fixtures, fakes, cache `/tmp` |
| `e2e-testing-patterns` | Playwright semantic locators, POM, flake-free E2E |
| `debugging-strategies` | Minimal repro, `git bisect`, falsifiable hypotheses |
| `error-handling-patterns` | Typed errors, capped backoff retries, fail-fast validation |
| `security-auditor` | OWASP Top 10, secrets hygiene, least-privilege |
| `auth-implementation-patterns` | OAuth2/OIDC + PKCE, sessions/JWT, RBAC/ABAC |
| `threat-modeling-expert` | STRIDE trust boundaries & risk-ranked mitigations |
| `accessibility-compliance-accessibility-audit` | WCAG 2.1 AA, keyboard/focus traps, ARIA, contrast |

## 6. DevOps, Cloud, Git & Observability (5 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `deployment-engineer` | Docker multi-stage, CI/CD, healthcheck & rollback |
| `git-advanced-workflows` | `git worktree` song song, atomic commits, `git bisect` |
| `github-actions-templates` | Least-privilege CI, caching, concurrency, injection safety |
| `kubernetes-architect` | Probes, resource limits, non-root SecurityContext, GitOps |
| `observability-engineer` | JSON logs, RED/USE metrics, tracing, zero alert fatigue |
