---
name: api-design-principles
description: Design consistent, versioned, contract-first REST and RPC/GraphQL APIs with predictable error schemas, pagination, and idempotency.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# API Design Principles (Contract-First)

## Use This Skill When
- Defining new HTTP REST, WebSocket, JSON-RPC, or GraphQL contracts between frontend, backend, or services.
- Standardizing error responses, pagination, filtering, authentication, and versioning.

## REST & Contract Standards
1. **Resource-Oriented Naming:** Use plural nouns (`/v1/tasks`, `/v1/projects/{id}/runs`), never verbs in URLs; use HTTP methods semantically (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
2. **Accurate Status Codes:** `200` OK, `201` Created, `204` No Content, `400` Validation Error, `401` Unauthenticated, `403` Forbidden, `404` Not Found, `409` Conflict, `422` Unprocessable, `429` Rate Limited, `500` Internal Error.
3. **Consistent Error Envelope:** Return structured JSON errors (`code`, `message`, `details`, `request_id`) — never leak stack traces or internal secrets.
4. **Pagination & Filtering:** Always bound collection endpoints (`limit`/`cursor` or `page`/`page_size`) with safe maximums.
5. **Idempotency & Safety:** Ensure `GET`/`PUT`/`DELETE` are idempotent; support `Idempotency-Key` for critical mutations (`POST` payments, job triggers).
6. **Backward Compatibility:** Prefer additive schema changes; version breaking changes explicitly (`/v2/...`) and document schemas (OpenAPI / JSON Schema).

## Checklist Before Implementation
- Request/response schemas and validation rules are documented and agreed before coding.
- Auth, rate limits, and timeout/retry behavior are explicitly defined per endpoint.
