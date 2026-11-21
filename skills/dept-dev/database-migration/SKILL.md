---
name: database-migration
description: Execute zero-downtime, reversible database schema migrations using expand-contract phases, lock timeouts, and verified backups.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Database Migration Safety

## Use This Skill When
- Adding/renaming/dropping columns, backfilling large tables, or creating indexes on production databases.

## Zero-Downtime Expand-Contract Pattern
1. **Expand:** Add new nullable columns/tables and deploy app code that dual-writes (writes both old and new, reads old with fallback).
2. **Backfill in Batches:** Backfill historical rows in small throttled chunks (e.g., 1,000 rows/tx) to avoid table locks and replication lag.
3. **Switch & Validate:** Add `NOT NULL` / `CHECK` constraints as `NOT VALID` first, then `VALIDATE CONSTRAINT`, and switch reads to the new schema.
4. **Contract:** Drop legacy columns only in a later release after verifying rollback is no longer needed.

## Safety Guards
- Create indexes non-blocking (`CREATE INDEX CONCURRENTLY` in Postgres) and set `lock_timeout` so migrations fail fast rather than stalling live traffic.
- Always back up SQLite/Postgres before destructive migrations and test both `up` and `down` paths in staging.
