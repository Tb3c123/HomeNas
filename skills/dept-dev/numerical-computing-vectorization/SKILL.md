---
name: numerical-computing-vectorization
description: Write fast, memory-safe vectorized NumPy/SciPy numerical code using sparse matrices, broadcasting, and floating-point error control.
metadata:
  model: inherit
  source: K-Dense-AI/scientific-agent-skills (MIT)
---

# Numerical Computing & Vectorization

## Use This Skill When
- Accelerating slow Python loops over arrays, matrices, graphs, or scientific datasets.
- Handling large matrices with sparse representations (`scipy.sparse`) or memory-bounded chunking.
- Debugging floating-point precision loss, NaN/Inf propagation, or unexpected array copies.

## Core Principles
1. **Eliminate Python Inner Loops:** Replace element-wise `for` loops with vectorized NumPy ufuncs, broadcasting, `np.einsum`, or `scipy.linalg` / `scipy.spatial` primitives (typically 20x–200x faster).
2. **Use Sparse Structures When Density < 10%:**
   - Construct sparse matrices via COO/LIL, then convert to **CSR** (fast row slicing & matrix-vector products `A @ x`) or **CSC** (fast column slicing & direct solvers `spsolve`).
   - Never call `.toarray()` on a large sparse matrix without checking memory footprint first.
3. **Memory Layout & View Hygiene:**
   - Watch implicit broadcasting blow-ups (e.g., `(N, 1) - (1, N)` allocates $O(N^2)$ RAM); chunk or use `cdist`/KD-tree instead.
   - Choose explicit `dtype` (`float64` for sensitive linear algebra, `float32` for large ML tensors) and avoid unintended copies inside tight loops.
4. **Floating-Point Discipline:**
   - Never compare floats with `==`; use `np.isclose` / `np.allclose(rtol, atol)`.
   - Guard against catastrophic cancellation, division by zero (`np.where` / `eps`), and silent `NaN`/`Inf` via explicit finite assertions at module boundaries.
5. **Profile Before Micro-Optimizing:** Measure with `time.perf_counter()` and memory peaks; reach for Numba/Cython only when pure vectorized NumPy/SciPy cannot express the recurrence.

## Delivery Checklist
- Verify vectorized implementation matches naive reference implementation within `allclose`.
- Document expected array shapes and dtypes in function signatures/docstrings.
