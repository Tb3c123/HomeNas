#!/usr/bin/env python3
"""Idempotent Bootstrap for Kanboard Project 'HomeNas Operations' (Columns, Swimlanes & Agent Users)."""

import secrets
import sqlite3
import sys

from shared.tools.kanboard_client.rpc_client import KanboardClient

COLUMNS = ["Backlog", "Ready", "In Progress", "Waiting Review", "Done"]
SWIMLANES = ["Director / General", "NAS Ops", "Media & Download", "Dev Studio"]
AGENT_USERS = [
    ("director", "Alex (Director)"),
    ("dept-nas-ops", "Marcus (NAS Ops)"),
    ("dept-media", "Elena (Media)"),
    ("dept-dev", "Liam (Dev Lead)"),
    ("watchdog", "Sentinel (Watchdog)"),
]


def read_api_token_from_sqlite(db_path: str = "/kanboard-data/db.sqlite") -> str:
    uri = f"file:{db_path}?mode=ro&immutable=1"
    with sqlite3.connect(uri, uri=True) as conn:
        row = conn.execute("SELECT value FROM settings WHERE option='api_token'").fetchone()
        return str(row[0]) if row and row[0] else ""


def ensure_agent_users(kb: KanboardClient, project_id: int) -> dict[str, int]:
    user_ids: dict[str, int] = {}
    for username, display_name in AGENT_USERS:
        existing = kb.call("getUserByName", {"username": username})
        if existing and isinstance(existing, dict) and existing.get("id"):
            uid = int(existing["id"])
            if existing.get("name") != display_name:
                kb.call("updateUser", {"id": uid, "name": display_name})
        else:
            uid = int(
                kb.call(
                    "createUser",
                    {
                        "username": username,
                        "password": secrets.token_hex(16),
                        "name": display_name,
                        "role": "app-user",
                    },
                )
            )
        kb.call("addProjectUser", {"project_id": project_id, "user_id": uid, "role": "project-member"})
        user_ids[username] = uid
    return user_ids


def bootstrap_homenas_board(client: KanboardClient | None = None, project_name: str = "HomeNas Operations") -> int:
    kb = client or KanboardClient()
    projects = kb.call("getAllProjects") or []
    proj = next((p for p in projects if p["name"] == project_name), None)
    pid = int(proj["id"]) if proj else int(kb.call("createProject", {"name": project_name}))
    kb.call("addProjectUser", {"project_id": pid, "user_id": 1, "role": "project-manager"})
    ensure_agent_users(kb, pid)

    cols = kb.call("getColumns", {"project_id": pid}) or []
    by_title = {c["title"]: int(c["id"]) for c in cols}
    if "Work in progress" in by_title and "In Progress" not in by_title:
        kb.call("updateColumn", {"column_id": by_title["Work in progress"], "title": "In Progress"})

    cols = kb.call("getColumns", {"project_id": pid}) or []
    existing_titles = {c["title"] for c in cols}
    for col in COLUMNS:
        if col not in existing_titles:
            kb.call("addColumn", {"project_id": pid, "title": col})

    cols = kb.call("getColumns", {"project_id": pid}) or []
    col_map = {c["title"]: int(c["id"]) for c in cols}
    for pos, col in enumerate(COLUMNS, start=1):
        kb.call("changeColumnPosition", {"project_id": pid, "column_id": col_map[col], "position": pos})

    lanes = kb.call("getAllSwimlanes", {"project_id": pid}) or []
    lane_map = {ln["name"]: int(ln["id"]) for ln in lanes}
    if "Default swimlane" in lane_map and "Director / General" not in lane_map:
        kb.call("updateSwimlane", {"project_id": pid, "swimlane_id": lane_map["Default swimlane"], "name": "Director / General"})
        lane_map["Director / General"] = lane_map.pop("Default swimlane")
    for lane in SWIMLANES:
        if lane not in lane_map:
            kb.call("addSwimlane", {"project_id": pid, "name": lane})
    return pid


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--print-token":
        print(read_api_token_from_sqlite())
        return 0
    pid = bootstrap_homenas_board()
    print(f"[OK] Kanboard Project #{pid} 'HomeNas Operations' ready (5 columns, 4 swimlanes, 5 agent users).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
