---
name: database-architect
description: Design normalized relational schemas, indexing strategies, constraints, and data lifecycles tailored to real query workloads.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Database Architect

## Use This Skill When
- Modeling entities, relationships, keys, indexes, and constraints for PostgreSQL, SQLite, or MySQL.
- Choosing between relational tables, JSONB columns, time-series partitioning, or read caches.

## Schema Design Rules
1. **Enforce Integrity in the DB:** Use `NOT NULL`, `UNIQUE`, `CHECK`, and `FOREIGN KEY` constraints so invalid data cannot enter even if app code has bugs.
2. **Query-Driven Indexing:** Design indexes around real `WHERE`, `JOIN`, and `ORDER BY` access patterns; avoid over-indexing write-heavy tables.
3. **Right Primary Keys:** Prefer monotonic keys (`BIGINT GENERATED ALWAYS AS IDENTITY` or UUIDv7) to avoid B-tree page fragmentation.
4. **Explicit Timestamps & Soft Deletes:** Store UTC timestamps (`TIMESTAMPTZ` / ISO-8601 UTC); use soft deletes (`deleted_at`) only when audit/recovery is required.
5. **Plan Retention Early:** Define archival/TTL policies for append-only logs and metrics so storage never grows unbounded.
