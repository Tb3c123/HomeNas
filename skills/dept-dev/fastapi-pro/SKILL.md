---
name: fastapi-pro
description: Build high-performance, type-safe FastAPI backends with Pydantic v2 validation, dependency injection, async SQLAlchemy, and clean router layering.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# FastAPI Pro (Async Python Web APIs)

## Use This Skill When
- Building REST/WebSocket backends or microservices in Python with FastAPI and Pydantic v2.
- Designing dependency injection, request/response schemas, middleware, and async DB sessions.

## Architectural Conventions
1. **Thin Routers, Thick Services:** Route handlers validate inputs, invoke a service/use-case, and map domain errors to HTTP status codes — never embed SQL or complex business logic directly in routes.
2. **Pydantic v2 Schemas:** Separate `Create`, `Update`, and `Response` models explicitly; use `ConfigDict(from_attributes=True)` and strict field validators.
3. **Dependency Injection (`Depends`):** Inject DB sessions, current authenticated user, and config settings cleanly so tests can swap them via `app.dependency_overrides`.
4. **Async Hygiene:** Use `async def` only for non-blocking async I/O (`httpx.AsyncClient`, async DB driver); use plain `def` routes for blocking sync libraries so FastAPI runs them in its threadpool.
5. **Lifespan & Observability:** Use `lifespan` context manager (not deprecated `@app.on_event`) to initialize/close pools; expose `/healthz` and structured JSON logs.

## Verification Checklist
- OpenAPI schema renders cleanly with accurate response models and status codes.
- Integration tests run via `TestClient` / `httpx.AsyncClient` with isolated test DB or fakes.
