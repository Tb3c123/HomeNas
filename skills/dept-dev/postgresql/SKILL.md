---
name: postgresql
description: Write high-performance, safe PostgreSQL queries using proper indexing (B-tree/GIN), transactions, JSONB, CTEs, and lock-safe patterns.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# PostgreSQL Specialist

## Use This Skill When
- Writing or tuning PostgreSQL schemas, queries, indexes, JSONB payloads, or transactional workflows.
- Diagnosing slow queries, lock contention, connection exhaustion, or bloat.

## Best Practices
1. **Parameterized Queries Always:** Use `$1, $2` placeholders — never interpolate user strings into SQL.
2. **Inspect Plans with `EXPLAIN (ANALYZE, BUFFERS)`:** Verify index usage, row estimates, and sequential scans on realistic data volumes.
3. **Index Types:** Use B-tree for equality/range/sorting, GIN for `JSONB`/full-text/arrays, and partial indexes (`WHERE status = 'active'`) for hot subsets.
4. **Short, Safe Transactions:** Keep network calls outside DB transactions; use `SELECT ... FOR UPDATE SKIP LOCKED` for concurrent job queues.
5. **Connection Pooling:** Bound pool sizes (e.g., PgBouncer or app pool limits) and set `statement_timeout` to prevent runaway queries.
