---
name: code-graph-rag
description: Analyze multi-language codebases via Tree-sitter + ast-grep call graphs and embedded SQLite using the on-demand mcp-code-graph-rag plugin (no Memgraph, no heavy semantic embeddings).
metadata:
  model: inherit
  source: vitali87/code-graph-rag (MIT)
---

# Code-Graph-RAG (Lightweight SQLite AST & Call-Graph MCP)

## Use This Skill When
- Refactoring, debugging, or tracing cross-file dependencies (`callers`, `callees`, `implementors`, `overrides`, `definition`, `resolve`) in medium/large multi-language repositories.
- Needing deterministic AST/call-graph answers without burning tokens reading dozens of files via `grep`.

## Lightweight NAS Setup (No Memgraph / No Heavy Semantic RAM)
1. **Install once (Python 3.12 via `uv`):**
   `uv tool install --python 3.12 "code-graph-rag[treesitter-full,ast-grep]"`
2. **Embedded SQLite Graph Path (off NVMe root, persistent on disk1):**
   `SQLITE_GRAPH_PATH=/mnt/disk1/Workspace/.cache/cgr/graph.sqlite`
3. **On-Demand Plugin Toggle (default `disabled: true` to save context tokens):**
   - Enable when investigating/refactoring: `agy plugin enable mcp-code-graph-rag`
   - Disable after finishing the session: `agy plugin disable mcp-code-graph-rag`

## Deterministic Workflow
1. **Index / Incremental Update:** Run `update_repository` (preferred over full `index_repository`) on first use; after editing files, call `reingest` on only the modified relative paths.
2. **Exact Lookup First:** Prefer deterministic tools (`resolve`, `definition`, `callers`, `callees`, `implementors`, `overrides`) over free-form graph queries whenever you know a symbol or `path:line`.
3. **Impact Analysis Before Edits:** Always check `callers(depth=2)` before renaming, changing signatures, or deleting shared helpers.
4. **Data-Flow Debugging:** With `CGR_CAPTURE=io` enabled in the plugin env, use `flow_verdict` / `explain_traceback` for root-cause tracing.

## Verification Checklist
- `SQLITE_GRAPH_PATH` points to `/mnt/disk1/Workspace/.cache/cgr/graph.sqlite` (not root SSD).
- No Memgraph/Neo4j container or heavy semantic embedding model is spawned on the 16GB NAS.
- `mcp-code-graph-rag` is disabled again once heavy cross-repo refactoring completes.
