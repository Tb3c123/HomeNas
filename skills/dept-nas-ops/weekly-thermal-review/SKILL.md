---
name: weekly-thermal-review
description: Analyze weekly thermal summary for Morefine N6 (Intel N200) and Acasis 2x10TB HDDs to recommend longevity optimizations.
---

# NAS Ops: Weekly Thermal & Longevity Review

## 1. Input Context (Minimal Token Footprint)
1. Read `shared/memory/USER.md` and `memory/dept-nas-ops/MEMORY.md`.
2. Read ONLY the latest `logs/thermal/weekly-YYYY-Www.md` (~25 lines). Do NOT load raw daily JSON files unless investigating a specific emergency.

## 2. Analysis Checklist
- Identify peak temperature hours (`>= 60C` on `disk1` WD Gold or `disk2` WD Purple Pro).
- Correlate thermal spikes or CPU N200 overload (`>= 95%` / `load5 > 4.0`) with active workloads.
- Recommend schedule shifts, cooling adjustments, or container throttling to protect SSD & HDD lifespan.
- Post a `<= 5 line` summary to the Kanboard `weekly-review` card, append any new durable lesson to `memory/dept-nas-ops/MEMORY.md`, and print an Inline Receipt (`[✅ DONE | #<id> | dept-nas-ops] ...`).
