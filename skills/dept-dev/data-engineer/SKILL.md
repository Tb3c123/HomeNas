---
name: data-engineer
description: Build idempotent, schema-validated ETL/ELT data pipelines with incremental ingestion, dead-letter handling, and data quality checks.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Data Engineer (Pipelines & Data Quality)

## Use This Skill When
- Designing batch/streaming ingestion jobs, JSON/CSV/SQLite/Parquet transformations, or analytics aggregations.

## Core Pipeline Discipline
1. **Idempotency by Design:** Re-running a job for the same time window or input must produce identical results (use upsert/merge or partition overwrite, never blind append).
2. **Explicit Contracts & Validation:** Validate schema, nullability, ranges, and row-count sanity at ingestion boundaries; route malformed records to a dead-letter file/table instead of silently dropping them.
3. **Layered Storage:** Separate `raw` (immutable source copy) -> `staged/cleaned` (typed, deduplicated) -> `curated/mart` (query-ready aggregates).
4. **Incremental & Checkpointed:** Track high-water marks/cursors so jobs process only deltas and resume cleanly after interruption.
5. **Observability:** Log record counts (in/out/rejected), duration, and freshness SLA for every pipeline run.
