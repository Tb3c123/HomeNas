---
name: sql-optimization-patterns
description: Eliminate N+1 queries, optimize JOINs and composite indexes, and use keyset pagination for fast, predictable SQL performance.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# SQL Optimization Patterns

## Use This Skill When
- Tuning slow SQL queries, ORM-generated lookups, reporting aggregations, or paginated API endpoints.

## High-Impact Patterns
1. **Kill N+1 Queries:** Replace per-row loops with batch `WHERE id IN (...)`, `JOIN`, or ORM eager loading (`selectinload` / `joinedload`).
2. **Composite Index Column Order:** Put equality (`=`) columns first, then range (`>`, `<`, `BETWEEN`) or `ORDER BY` columns; use covering indexes (`INCLUDE`) for hot reads.
3. **SARGable Predicates:** Avoid wrapping indexed columns in functions (`WHERE LOWER(email) = ...` breaks plain index; use expression index or `citext`).
4. **Keyset (Cursor) Pagination:** Replace deep `OFFSET N` scans with `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT $3`.
5. **Select Only Needed Columns:** Avoid `SELECT *` in production queries to cut network, memory, and index-only scan misses.
