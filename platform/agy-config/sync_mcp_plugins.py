#!/usr/bin/env python3
"""Sync & Manage the 5 HomeNas Dev MCP Plugins for Antigravity CLI (/root/.gemini/config).

Plugins installed (default disabled=True to keep Main/NAS Ops/Media contexts lean):
1. mcp-context7       (Streamable HTTP -> https://mcp.context7.com/mcp)
2. mcp-github         (Streamable HTTP -> https://api.githubcopilot.com/mcp/)
3. mcp-sqlite-ro      (Local Python 3.11 Stdio -> shared/tools/mcp_servers/sqlite_ro_mcp.py)
4. mcp-playwright     (On-Demand Docker Streamable HTTP -> http://playwright-mcp:8931/mcp)
5. mcp-code-graph-rag (On-Demand Stdio -> code-graph-rag mcp-server + SQLite graph, no Memgraph)
"""

import argparse
import json
import os
import pathlib
import sys
from typing import Any

DEFAULT_CONFIG_ROOT = pathlib.Path("/root/.gemini/config")
DEFAULT_REPO_ROOT = pathlib.Path("/mnt/disk1/Workspace/HomeNas")


def build_plugin_definitions(repo_root: pathlib.Path = DEFAULT_REPO_ROOT) -> dict[str, dict[str, Any]]:
    sqlite_script = str(repo_root / "shared" / "tools" / "mcp_servers" / "sqlite_ro_mcp.py")
    pw_url = os.environ.get("PLAYWRIGHT_MCP_URL", "http://playwright-mcp:8931/mcp")
    cgr_db = os.environ.get("SQLITE_GRAPH_PATH", "/mnt/disk1/Workspace/.cache/cgr/graph.sqlite")
    return {
        "mcp-context7": {
            "title": "Context7 Live Docs MCP",
            "description": "Real-time version-accurate library & framework documentation via Context7 Streamable HTTP.",
            "mcpServers": {
                "context7": {
                    "url": "https://mcp.context7.com/mcp",
                }
            },
        },
        "mcp-github": {
            "title": "GitHub Official Remote MCP",
            "description": "GitHub PRs, Issues, Actions & Code search via GITHUB_PERSONAL_ACCESS_TOKEN.",
            "mcpServers": {
                "github": {
                    "url": "https://api.githubcopilot.com/mcp/",
                    "headers": {
                        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}",
                    },
                }
            },
        },
        "mcp-sqlite-ro": {
            "title": "HomeNas SQLite Read-Only Inspector MCP",
            "description": "Pure-Python 3.11 3-layer Read-Only SQLite inspector for Kanboard, *arr & project DBs.",
            "mcpServers": {
                "sqlite-ro": {
                    "command": "python3",
                    "args": [sqlite_script],
                    "env": {"PYTHONDONTWRITEBYTECODE": "1"},
                }
            },
        },
        "mcp-playwright": {
            "title": "Playwright Headless UI Tester MCP (On-Demand Docker)",
            "description": "Streamable HTTP bridge to on-demand playwright-mcp container (:8931).",
            "mcpServers": {
                "playwright": {
                    "url": pw_url,
                }
            },
        },
        "mcp-code-graph-rag": {
            "title": "Code-Graph-RAG AST & Call-Graph MCP (On-Demand SQLite)",
            "description": "Lightweight Tree-sitter + ast-grep MCP using embedded SQLite (no Memgraph/semantic).",
            "mcpServers": {
                "code-graph-rag": {
                    "command": "code-graph-rag",
                    "args": ["mcp-server"],
                    "env": {"SQLITE_GRAPH_PATH": cgr_db, "CGR_CAPTURE": "io", "PYTHONDONTWRITEBYTECODE": "1"},
                }
            },
        },
    }


def sync_mcp_plugins(
    config_root: pathlib.Path = DEFAULT_CONFIG_ROOT,
    repo_root: pathlib.Path = DEFAULT_REPO_ROOT,
    enable_list: list[str] | None = None,
    disable_list: list[str] | None = None,
) -> dict[str, Any]:
    plugins_dir = config_root / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    defs = build_plugin_definitions(repo_root=repo_root)
    enable_set = set(enable_list or [])
    disable_set = set(disable_list or [])
    installed: dict[str, bool] = {}

    for name, spec in defs.items():
        pdir = plugins_dir / name
        pdir.mkdir(parents=True, exist_ok=True)
        cfg_file = pdir / "config.json"

        disabled = True
        if cfg_file.exists():
            try:
                disabled = bool(json.loads(cfg_file.read_text(encoding="utf-8")).get("disabled", True))
            except (json.JSONDecodeError, OSError):
                disabled = True
        if name in enable_set:
            disabled = False
        elif name in disable_set:
            disabled = True

        plugin_json = {
            "name": name,
            "version": "2.2.0",
            "title": spec["title"],
            "description": spec["description"],
            "mcpConfigPath": "mcp_config.json",
        }
        (pdir / "plugin.json").write_text(json.dumps(plugin_json, indent=2) + "\n", encoding="utf-8")
        (pdir / "mcp_config.json").write_text(
            json.dumps({"mcpServers": spec["mcpServers"]}, indent=2) + "\n", encoding="utf-8",
        )
        cfg_file.write_text(json.dumps({"disabled": disabled}, indent=2) + "\n", encoding="utf-8")
        installed[name] = not disabled

    return {"plugins_dir": str(plugins_dir), "enabled_map": installed}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sync-mcp-plugins", description="Sync HomeNas 5 Dev MCP Plugins")
    parser.add_argument("--config-root", default=str(DEFAULT_CONFIG_ROOT))
    parser.add_argument("--repo-root", default=str(DEFAULT_REPO_ROOT))
    parser.add_argument("--enable", nargs="*", default=[], help="Plugin names to enable")
    parser.add_argument("--disable", nargs="*", default=[], help="Plugin names to disable")
    args = parser.parse_args(argv)
    res = sync_mcp_plugins(
        config_root=pathlib.Path(args.config_root),
        repo_root=pathlib.Path(args.repo_root),
        enable_list=args.enable,
        disable_list=args.disable,
    )
    print(json.dumps(res, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
