---
name: rag-implementation
description: Build accurate Retrieval-Augmented Generation pipelines with semantic chunking, hybrid BM25+vector search, reranking, and grounded citations.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# RAG Implementation

## Use This Skill When
- Indexing codebases, docs, or knowledge bases for semantic search and grounded LLM answers.

## Pipeline Best Practices
1. **Structure-Aware Chunking:** Split by Markdown headings, AST functions, or paragraphs with 10-15% overlap; preserve rich metadata (`source_path`, `section`, `updated_at`).
2. **Hybrid Retrieval:** Combine lexical search (BM25 / SQLite FTS5) with dense vector embeddings using Reciprocal Rank Fusion (RRF) so exact identifiers/error codes are never missed.
3. **Top-K Reranking:** Retrieve ~20 candidates, rerank to top 4-6 highest-relevance chunks before passing to the generator to keep context clean and cheap.
4. **Strict Grounding & Citations:** Require answers to cite exact source IDs/paths and explicitly say "not found in sources" when retrieval confidence is low.
5. **Evaluate Retrieval Separately:** Measure Recall@K / MRR on retrieval before blaming or tuning the generation prompt.
