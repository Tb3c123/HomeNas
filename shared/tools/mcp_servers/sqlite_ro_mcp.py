#!/usr/bin/env python3
"""Pure-Python 3.11 Read-Only SQLite MCP Server (Stdio JSON-RPC 2.0, 0 External Deps).

3-Layer Read-Only Defense:
1. Opens SQLite via URI `file:<path>?mode=ro&immutable=1`.
2. Enforces `PRAGMA query_only = ON`.
3. Regex whitelist permits ONLY single-statement SELECT / PRAGMA / EXPLAIN queries.
"""

import json
import pathlib
import re
import sqlite3
import sys
from typing import Any
from urllib.parse import quote

FORBIDDEN_SQL_RE = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|ATTACH|DETACH|VACUUM|REINDEX)\b|\bPRAGMA\s+\w+\s*=",
    re.IGNORECASE,
)
ALLOWED_START_RE = re.compile(r"^\s*(SELECT|WITH|PRAGMA|EXPLAIN)\b", re.IGNORECASE)
SAFE_IDENT_RE = re.compile(r"^[A-Za-z0-9_]+$")


def validate_readonly_sql(sql: str) -> str:
    cleaned = sql.strip()
    if cleaned.endswith(";"):
        cleaned = cleaned[:-1].strip()
    if not cleaned:
        raise ValueError("Empty SQL query.")
    if ";" in cleaned:
        raise ValueError("Blocked: Multiple SQL statements (';') are prohibited.")
    if not ALLOWED_START_RE.match(cleaned) or FORBIDDEN_SQL_RE.search(cleaned):
        raise ValueError("Blocked: Only read-only SELECT, PRAGMA, and EXPLAIN queries are permitted.")
    return cleaned


def _connect_ro(db_path: str | pathlib.Path) -> sqlite3.Connection:
    resolved = pathlib.Path(db_path).resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"SQLite file not found: {resolved}")
    uri = f"file:{quote(str(resolved))}?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri=True, timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    return conn


def execute_ro_tool(name: str, args: dict[str, Any]) -> list[dict[str, Any]]:
    db_path = str(args.get("db_path") or "")
    max_rows = min(int(args.get("max_rows", 100)), 500)
    conn = _connect_ro(db_path)
    try:
        if name == "list_tables":
            cur = conn.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','view') ORDER BY name")
            return [dict(r) for r in cur.fetchall()]
        if name == "describe_table":
            tbl = str(args.get("table") or "")
            if not SAFE_IDENT_RE.match(tbl):
                raise ValueError(f"Invalid table identifier: {tbl}")
            cur = conn.execute(f"PRAGMA table_info({tbl})")
            return [dict(r) for r in cur.fetchall()]
        if name == "read_query":
            sql = validate_readonly_sql(str(args.get("query") or ""))
            cur = conn.execute(sql)
            return [dict(r) for r in cur.fetchmany(max_rows)]
        raise ValueError(f"Unknown tool: {name}")
    finally:
        conn.close()


MCP_TOOLS = [
    {
        "name": "list_tables",
        "description": "List all tables and views in a SQLite database (Read-Only).",
        "inputSchema": {"type": "object", "properties": {"db_path": {"type": "string"}}, "required": ["db_path"]},
    },
    {
        "name": "describe_table",
        "description": "Show columns and types of a table in a SQLite database (Read-Only).",
        "inputSchema": {
            "type": "object",
            "properties": {"db_path": {"type": "string"}, "table": {"type": "string"}},
            "required": ["db_path", "table"],
        },
    },
    {
        "name": "read_query",
        "description": "Execute a read-only SELECT/PRAGMA/EXPLAIN query on a SQLite database.",
        "inputSchema": {
            "type": "object",
            "properties": {"db_path": {"type": "string"}, "query": {"type": "string"}, "max_rows": {"type": "integer"}},
            "required": ["db_path", "query"],
        },
    },
]


def handle_rpc_request(req: dict[str, Any]) -> dict[str, Any] | None:
    method = req.get("method", "")
    req_id = req.get("id")
    if method.startswith("notifications/"):
        return None
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "homenas-sqlite-ro", "version": "1.8.0"},
            },
        }
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}
    if method == "tools/call":
        params = req.get("params") or {}
        try:
            rows = execute_ro_tool(str(params.get("name") or ""), params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(rows)}], "isError": False}}
        except Exception as exc:
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": f"Error: {exc}"}], "isError": True}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}


def main() -> int:
    for line in sys.stdin:
        raw = line.strip()
        if not raw:
            continue
        try:
            resp = handle_rpc_request(json.loads(raw))
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            continue
    return 0


if __name__ == "__main__":
    sys.exit(main())
