---
name: vector-hybrid-search-engineering
description: Engineer high-recall embedding, vector indexing (HNSW/IVF/SQLite-vec), and BM25+dense hybrid retrieval with RRF fusion and latency tuning.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Vector & Hybrid Search Engineering

## Use This Skill When
- Selecting embedding models, vector stores (`pgvector`, `Qdrant`, `SQLite-vec`, `FAISS`), or index parameters.
- Combining lexical search (`BM25`/`FTS5`) with dense vector retrieval for higher precision and recall.
- Tuning retrieval latency, metadata pre-filtering, and recall@K on growing corpora.

## Core Principles
1. **Choose Embeddings Empirically:** Match model to language (multilingual Vietnamese/English support), max token length, and MTEB domain benchmarks; leverage Matryoshka dimension truncation (e.g., `1536 → 512`) or scalar/binary quantization when RAM is tight. Always normalize vectors for cosine similarity.
2. **Hybrid Search Beats Dense-Only:** Dense embeddings capture semantics but miss exact IDs, codes, and rare terms. Combine **BM25/FTS5** + **Dense Vector** retrieval via **Reciprocal Rank Fusion (RRF, $k=60$)** and optional cross-encoder reranking on top-20 candidates.
3. **Right Index & Pre-Filtering Strategy:**
   - `< 50k` vectors: exact flat scan or `SQLite-vec` is fast, simple, and 100% recall—no distributed vector DB needed.
   - `50k–10M+` vectors: HNSW (`M=16–32`, `efConstruction=128–200`, tune `efSearch` at query time) or IVF-PQ for memory-constrained deployments.
   - Apply **metadata pre-filtering** (tenant, ACL, date) carefully so filtered HNSW queries don't return under-filled results.
4. **Versioned Index Hygiene:** Store `embedding_model_id`, `chunk_version`, and `content_hash` alongside every vector to enable incremental upserts, clean deletes, and zero-downtime re-indexing.
5. **Measure Retrieval Independently:** Track **Recall@5/10**, **MRR/nDCG**, and **p95 query latency** on a labeled query set before changing models or index params.

## Delivery Checklist
- Verify exact-match ID/code queries AND semantic paraphrase queries both surface in top-5.
- Confirm idempotent upsert/delete sync between source-of-truth DB and vector index.
