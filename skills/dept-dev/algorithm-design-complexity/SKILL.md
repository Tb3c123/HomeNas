---
name: algorithm-design-complexity
description: Design and prove optimal algorithms (DP, Graph, Greedy, Divide & Conquer) with rigorous Big-O bounds, invariants, and brute-force stress testing.
metadata:
  model: inherit
  source: Standard CS Algorithms & Data Structures Curated Reference
---

# Algorithm Design & Complexity Analysis

## Use This Skill When
- Solving non-trivial computational problems (graphs, dynamic programming, trees, strings, geometry, streaming).
- Upgrading an $O(N^2)$ or exponential bottleneck to $O(N \log N)$ or $O(N)$ within strict memory limits.
- Verifying algorithmic correctness across tricky boundary cases.

## Core Methodology
1. **Constraints First:** Extract input bounds ($N, M, V, E$, value range, precision, time/memory limits) before choosing a paradigm—bounds dictate whether $O(N \log N)$, $O(N \sqrt{N})$, or bitmask DP is viable.
2. **Select the Right Paradigm & Data Structure:**
   - Overlapping subproblems + optimal substructure → DP (state, transition, base case, space compression).
   - Exchange argument holds → Greedy (prove exchange property before coding!).
   - Connectivity / shortest path / flow → BFS/DFS, Dijkstra, Bellman-Ford, Tarjan SCC, Union-Find, Dinic.
   - Range queries / updates → Prefix sums, Monotonic deque, Fenwick (BIT), Segment Tree, Sparse Table.
3. **Prove Correctness via Invariants:** State the loop invariant or induction hypothesis explicitly; check termination and degenerate inputs ($N=0, 1$, disconnected graphs, negative weights, duplicates, integer overflow).
4. **Complexity Accounting:** Derive both **time** and **auxiliary space** complexity (worst-case and amortized), including hidden constant factors (recursion depth, hash collisions, GC pressure).
5. **Differential Stress Testing:** Write a simple brute-force oracle for small random inputs ($N \le 10$) and fuzz 1,000+ cases against the optimized algorithm to catch subtle edge bugs.

## Delivery Checklist
- Document state/invariant, time & space Big-O, and edge-case handling in concise comments.
- Run differential oracle tests + worst-case max-size benchmark before delivery.
