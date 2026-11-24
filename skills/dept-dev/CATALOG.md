# Dev Team Skill Catalog (Lazy-Load Index — 76 Skills)

> Chỉ đọc đúng 1–2 `SKILL.md` cần cho tác vụ hiện tại để tiết kiệm quota. Mọi skill đều `<= 60 dòng`, `model: inherit`, tuyển chọn 100% không trùng lặp từ các kho MIT / Apache-2.0 tốt nhất (`anthropics/skills`, `ui-ux-pro-max`, `impeccable`, `vercel-labs`, `K-Dense-AI`, `Orchestra-Research`, `rmyndharis/antigravity-skills`).

## 1. Quy trình, Sản phẩm & Kiến trúc Hệ thống (9 Skills)
| Skill (`skills/dept-dev/<name>/SKILL.md`) | Trọng tâm |
| :--- | :--- |
| `micro-agent-swarm` | Điều phối 11 Micro-Agents, ≤ 150 dòng/file, max 2 vòng sửa |
| `context-driven-development` | Phân rã Spec → Track → Task, đồng bộ ngữ cảnh |
| `architecture-patterns` | Clean / Hexagonal Architecture, DDD, Ports & Adapters |
| `api-design-principles` | Contract-first REST/RPC, status codes, pagination, idempotency |
| `microservices-patterns` | Bounded contexts, circuit breakers, async outbox |
| `event-sourcing-architect` | Append-only event logs, CQRS, idempotent projections |
| `performance-engineer` | Profiling BE, p95/p99 latency, caching, memory bounds |
| `monorepo-architect` | Acyclic package graph, shared libs, affected-only CI |
| `docs-architect` | Technical specs, ADR, Mermaid diagrams, Changelog |

## 2. UI/UX Sạch, Đẹp & Tương Tác Chuẩn (15 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `ui-ux-designer` | User flow, wireframe, IA, trạng thái component cơ bản |
| `frontend-aesthetic-design` | Thẩm mỹ có chủ đích, chống "AI slop", visual hierarchy sạch |
| `design-tokens-oklch` | Hệ màu OKLCH đều mắt, tinted neutrals, dark/light surface |
| `typography-and-hierarchy` | Font pairing, modular scale, measure `45–75ch`, `tabular-nums` |
| `tailwind-design-system` | Tailwind semantic tokens, dark mode, CVA variants |
| `web-interaction-motion` | Micro-interactions, Optimistic UI, GPU-only `transform/opacity` |
| `ui-critique-and-polish` | Phê bình & đánh bóng UI 6 bước trước khi bàn giao |
| `ux-copywriting-microcopy` | Nhãn nút động từ rõ, empty/error states & confirmation copy |
| `forms-and-validation-ux` | Form đa bước, inline validation đúng lúc, không mất dữ liệu |
| `responsive-layout-architecture` | CSS Grid/Subgrid, Container Queries, `100dvh`, 0 tràn ngang |
| `react-composition-patterns` | Compound components, headless primitives, diệt re-render/waterfall |
| `data-visualization-ux` | Biểu đồ, heatmap/ma trận sạch, colorblind-safe, 0 chartjunk |
| `interactive-canvas-svg-ui` | SVG sắc nét, Canvas 2D/WebGL 60fps, retina DPI, pan/zoom |
| `web-performance-core-vitals` | Tối ưu LCP, INP, CLS, code-splitting & virtualized lists |
| `accessibility-compliance-accessibility-audit` | WCAG 2.1 AA, keyboard/focus traps, ARIA, contrast |

## 3. Nghiên cứu Khoa học, Toán & Thuật toán (9 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `scientific-research-synthesis` | Tổng hợp tài liệu có dẫn chứng, tách fact vs. assumption |
| `research-ideation-methodology` | Đặt câu hỏi nghiên cứu, thiết kế baseline, ablation & validity |
| `academic-paper-writing` | Cấu trúc paper/báo cáo kỹ thuật, ký hiệu toán LaTeX, limitations |
| `autoresearch-experiment-loop` | Vòng lặp thực nghiệm (`Baseline → 1-Var → Metric Gate → Keep/Revert`) |
| `algorithm-design-complexity` | DP, Graph, Greedy, bất biến (invariant), Big-O & oracle fuzzing |
| `combinatorial-optimization` | LP/MILP, CP-SAT, lập lịch/phân bổ tài nguyên & metaheuristics |
| `mathematical-stochastic-modeling` | Đại số tuyến tính, ma trận ngẫu nhiên/Markov, Monte Carlo, thống kê |
| `numerical-computing-vectorization` | Vector hóa NumPy/SciPy, ma trận thưa (CSR/CSC), kiểm soát float |
| `time-series-forecasting` | Chuỗi thời gian, STL, anomaly detection & walk-forward CV |

## 4. AI, Machine Learning & LLM Engineering (12 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `ml-modeling-classical` | Tabular ML, `scikit-learn` pipeline chống leakage, GBDT, calibration |
| `deep-learning-pytorch` | PyTorch architecture, shape contracts, AMP/bf16, grad clipping |
| `llm-finetuning-post-training` | SFT, LoRA/QLoRA, DPO/GRPO, chống catastrophic forgetting |
| `ai-inference-optimization` | Quantization (GGUF/AWQ/INT8), KV-cache, batching, TTFT/TPS |
| `multimodal-vision-audio-ai` | VLM/OCR, Whisper+VAD, cross-modal embeddings & provenance |
| `ai-safety-guardrails-alignment` | Chống prompt injection, code-level least privilege, PII/groundedness |
| `vector-hybrid-search-engineering` | Embeddings, HNSW/SQLite-vec, BM25+dense RRF & recall tuning |
| `ai-engineer` | Provider adapters, structured outputs, token budget, ToS safety |
| `prompt-engineering-patterns` | System prompts, few-shot, anti-prompt-injection delimiters |
| `rag-implementation` | Semantic chunking, hybrid retrieval, reranking, citations |
| `llm-evaluation` | Golden datasets, layered graders, accuracy/latency/cost gates |
| `agent-orchestration-multi-agent-optimize` | Context isolation, compact handoffs, bounded retry loops |

## 5. Dữ liệu & Cơ sở dữ liệu (5 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `database-architect` | Relational modeling, constraints, indexing, retention |
| `postgresql` | EXPLAIN ANALYZE, B-tree/GIN, JSONB, SKIP LOCKED |
| `sql-optimization-patterns` | Kill N+1, composite indexes, keyset pagination |
| `database-migration` | Zero-downtime expand-contract, concurrent indexes, rollback |
| `data-engineer` | Idempotent ETL/ELT, schema validation, dead-letter queues |

## 6. Ngôn ngữ, Web & Mobile (12 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `python-pro` | Python 3.12+, strict typing, stdlib-first, async hygiene |
| `fastapi-pro` | FastAPI, Pydantic v2, Depends DI, lifespan |
| `typescript-pro` | Strict TS, discriminated unions, Zod boundary validation |
| `frontend-developer` | React/Next.js/Vite, component composition & state |
| `nodejs-backend-patterns` | Layered TS backend, safe `spawn`/WS, graceful shutdown |
| `golang-pro` | Idiomatic Go, small interfaces, `context`, `-race` concurrency |
| `rust-pro` | Ownership/borrowing, `Result`/no-unwrap, Tokio async, clippy |
| `java-pro` | Java 21+, records, sealed types, virtual threads, JUnit 5 |
| `csharp-pro` | .NET 8+, nullable safety, `CancellationToken`, EF Core |
| `flutter-expert` | `const` widgets, Riverpod/Bloc state, cross-platform responsive |
| `react-native-architecture` | Typed navigation, FlashList, offline sync, SecureStore |
| `bash-pro` | Defensive Bash (`set -euo pipefail`), quoting, `trap` cleanup |

## 7. Chất lượng, Kiểm thử, Debug & Bảo mật (9 Skills)
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

## 8. DevOps, Cloud, Git & Observability (5 Skills)
| Skill | Trọng tâm |
| :--- | :--- |
| `deployment-engineer` | Docker multi-stage, CI/CD, healthcheck & rollback |
| `git-advanced-workflows` | `git worktree` song song, atomic commits, `git bisect` |
| `github-actions-templates` | Least-privilege CI, caching, concurrency, injection safety |
| `kubernetes-architect` | Probes, resource limits, non-root SecurityContext, GitOps |
| `observability-engineer` | JSON logs, RED/USE metrics, tracing, zero alert fatigue |
