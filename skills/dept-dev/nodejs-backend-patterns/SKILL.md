---
name: nodejs-backend-patterns
description: Build resilient Node.js/TypeScript backend services with layered architecture, structured logging, safe subprocess/WebSocket handling, and graceful shutdown.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Node.js Backend Patterns (TypeScript / Express / Fastify)

## Use This Skill When
- Building Node.js/TS HTTP APIs, WebSocket servers, local daemon backends, or PTY/CLI orchestration bridges.
- Implementing auth middleware, request validation, error handling, and graceful shutdown.

## Layered Architecture & Reliability
1. **Clean Separation:** Split `routes/controllers` (HTTP/WS parsing) -> `services` (business logic) -> `repositories/adapters` (DB, filesystem, child processes).
2. **Centralized Error Handling:** Define typed application error classes (`AppError` with HTTP status + machine code) and handle them in one error middleware — never crash the process on unhandled promise rejections.
3. **Runtime Validation:** Validate all `req.body`, `req.query`, `req.params`, and WebSocket frames with Zod before touching business logic.
4. **Safe Subprocess & Streaming:** Prefer `spawn` with explicit arg arrays (`shell: false`), enforce timeouts/backpressure, and clean up child processes when clients disconnect.
5. **Graceful Shutdown & Logs:** Handle `SIGINT`/`SIGTERM` to close HTTP/WS servers, DB pools, and child processes cleanly; emit structured JSON logs (Pino) without leaking tokens.
