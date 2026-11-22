"""Unit Tests for v1.8.0: 4 Dev MCP Plugins Sync & Pure-Python Read-Only SQLite MCP Server."""

import importlib.util
import json
import pathlib
import sqlite3
import tempfile
import unittest

from shared.tools.mcp_servers.sqlite_ro_mcp import (
    execute_ro_tool,
    handle_rpc_request,
    validate_readonly_sql,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SYNC_SCRIPT = REPO_ROOT / "platform" / "agy-config" / "sync_mcp_plugins.py"


def _load_sync_module():
    spec = importlib.util.spec_from_file_location("sync_mcp_plugins", SYNC_SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class McpPluginsAndSqliteRoTests(unittest.TestCase):
    def test_sqlite_ro_mcp_allows_select_and_blocks_all_writes_and_injections(self) -> None:
        self.assertEqual(validate_readonly_sql("SELECT id, title FROM tasks;"), "SELECT id, title FROM tasks")
        for bad_sql in [
            "DROP TABLE tasks",
            "DELETE FROM tasks WHERE id=1",
            "UPDATE tasks SET title='x'",
            "INSERT INTO tasks VALUES (1,'a')",
            "SELECT * FROM tasks; DROP TABLE tasks",
            "ATTACH DATABASE '/tmp/evil.db' AS evil",
            "PRAGMA writable_schema = 1",
        ]:
            with self.assertRaises(ValueError):
                validate_readonly_sql(bad_sql)

        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            db_file = pathlib.Path(tmp) / "test.sqlite"
            conn = sqlite3.connect(db_file)
            conn.execute("CREATE TABLE projects (id INTEGER PRIMARY KEY, name TEXT)")
            conn.execute("INSERT INTO projects (id, name) VALUES (1, 'HomeNas'), (2, 'HomeNas Manager')")
            conn.commit()
            conn.close()

            tables = execute_ro_tool("list_tables", {"db_path": str(db_file)})
            self.assertEqual(tables[0]["name"], "projects")

            cols = execute_ro_tool("describe_table", {"db_path": str(db_file), "table": "projects"})
            self.assertEqual([c["name"] for c in cols], ["id", "name"])

            init_resp = handle_rpc_request({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
            self.assertEqual(init_resp["result"]["serverInfo"]["name"], "homenas-sqlite-ro")

            call_ok = handle_rpc_request({
                "jsonrpc": "2.0", "id": 2, "method": "tools/call",
                "params": {"name": "read_query", "arguments": {"db_path": str(db_file), "query": "SELECT name FROM projects ORDER BY id"}},
            })
            self.assertFalse(call_ok["result"]["isError"])
            rows = json.loads(call_ok["result"]["content"][0]["text"])
            self.assertEqual([r["name"] for r in rows], ["HomeNas", "HomeNas Manager"])

            call_blocked = handle_rpc_request({
                "jsonrpc": "2.0", "id": 3, "method": "tools/call",
                "params": {"name": "read_query", "arguments": {"db_path": str(db_file), "query": "DELETE FROM projects"}},
            })
            self.assertTrue(call_blocked["result"]["isError"])
            self.assertIn("Blocked", call_blocked["result"]["content"][0]["text"])

    def test_sync_mcp_plugins_creates_4_manifests_and_preserves_toggle_state(self) -> None:
        sync_mod = _load_sync_module()
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            cfg_root = pathlib.Path(tmp) / "config"
            res1 = sync_mod.sync_mcp_plugins(config_root=cfg_root, repo_root=REPO_ROOT)
            expected = {"mcp-context7", "mcp-github", "mcp-sqlite-ro", "mcp-playwright"}
            self.assertEqual(set(res1["enabled_map"].keys()), expected)
            self.assertTrue(all(v is False for v in res1["enabled_map"].values()))

            for name in expected:
                pdir = cfg_root / "plugins" / name
                self.assertTrue((pdir / "plugin.json").is_file())
                self.assertTrue((pdir / "mcp_config.json").is_file())
                self.assertTrue((pdir / "config.json").is_file())

            # Enable mcp-context7 and mcp-sqlite-ro, then re-sync without args -> must preserve enabled state
            res2 = sync_mod.sync_mcp_plugins(
                config_root=cfg_root, repo_root=REPO_ROOT, enable_list=["mcp-context7", "mcp-sqlite-ro"],
            )
            self.assertTrue(res2["enabled_map"]["mcp-context7"])
            self.assertTrue(res2["enabled_map"]["mcp-sqlite-ro"])
            self.assertFalse(res2["enabled_map"]["mcp-playwright"])

            res3 = sync_mod.sync_mcp_plugins(config_root=cfg_root, repo_root=REPO_ROOT)
            self.assertTrue(res3["enabled_map"]["mcp-context7"])
            self.assertTrue(res3["enabled_map"]["mcp-sqlite-ro"])


if __name__ == "__main__":
    unittest.main()
