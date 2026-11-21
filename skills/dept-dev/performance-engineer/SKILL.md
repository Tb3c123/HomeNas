---
name: performance-engineer
description: Profile, benchmark, and optimize latency (p95/p99), memory footprint, I/O bottlenecks, and caching with measured evidence.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Performance Engineer

## Use This Skill When
- Diagnosing slow endpoints, high CPU/RAM usage, disk thrashing, or UI frame drops.
- Designing caching layers, batching, pagination, or load-testing benchmarks.

## Measure-First Discipline
1. **Profile Before Optimizing:** Capture real flamegraphs, query plans, or p50/p95/p99 timings — never guess bottlenecks.
2. **Eliminate Big-O & I/O Waste First:** Fix N+1 queries, unbounded payload loads, redundant network roundtrips, and synchronous disk writes before micro-optimizing syntax.
3. **Smart Caching:** Cache expensive read-heavy computations with explicit TTL, bounded size (LRU), and clear invalidation rules; avoid thundering herds.
4. **Memory & Resource Bounds:** Stream large files/responses instead of buffering everything in RAM; bound queue sizes and worker pools.
5. **Verify Regression:** Re-run benchmarks after changes and assert both correctness and speedup.
