"""Kanboard Domain Service Layer (Facade over RPC Client, Formatter, and Digest Store)."""

import os
from typing import Any

from shared.tools.kanboard_client.digest_state import DigestStateStore
from shared.tools.kanboard_client.formatter import find_open_dedup_task, format_task_list
from shared.tools.kanboard_client.rpc_client import KanboardClient, KanboardRPCError


class KanboardService:
    def __init__(
        self,
        client: KanboardClient | None = None,
        digest_store: DigestStateStore | None = None,
        project_id: int | None = None,
    ) -> None:
        self.client = client or KanboardClient()
        self.digest_store = digest_store or DigestStateStore()
        self.project_id = project_id or int(os.environ.get("KANBOARD_PROJECT_ID", "1"))
        self._user_cache: dict[str, int] = {}

    def _resolve_user_id(self, author: str | None) -> int:
        if not author:
            return 1
        key = author.strip().lower()
        if key in self._user_cache:
            return self._user_cache[key]
        try:
            user = self.client.call("getUserByName", {"username": key})
            if isinstance(user, dict) and user.get("id"):
                uid = int(user["id"])
                self._user_cache[key] = uid
                return uid
        except KanboardRPCError:
            pass
        return 1

    def _board_maps(self) -> tuple[dict[str, int], dict[int, str], dict[str, int], dict[int, str]]:
        try:
            cols = self.client.call("getColumns", {"project_id": self.project_id}) or []
            lanes = self.client.call("getAllSwimlanes", {"project_id": self.project_id}) or []
        except KanboardRPCError:
            return {}, {}, {}, {}
        col_by_name = {str(c["title"]): int(c["id"]) for c in cols if "title" in c}
        col_by_id = {int(c["id"]): str(c["title"]) for c in cols if "title" in c}
        lane_by_name = {str(l["name"]): int(l["id"]) for l in lanes if "name" in l}
        lane_by_id = {int(l["id"]): str(l["name"]) for l in lanes if "name" in l}
        return col_by_name, col_by_id, lane_by_name, lane_by_id

    def _enrich_tasks(self, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        _, col_by_id, _, lane_by_id = self._board_maps()
        for t in tasks:
            if not t.get("column_name") and t.get("column_id") is not None:
                t["column_name"] = col_by_id.get(int(t["column_id"]), str(t["column_id"]))
            if not t.get("swimlane_name") and t.get("swimlane_id") is not None:
                t["swimlane_name"] = lane_by_id.get(int(t["swimlane_id"]), str(t["swimlane_id"]))
        return tasks

    def list_tasks(self, swimlane: str | None = None, column: str | None = None) -> str:
        self.client.flush_offline_queue()
        tasks = self._enrich_tasks(self.client.call("getAllTasks", {"project_id": self.project_id, "status_id": 1}) or [])
        if swimlane:
            tasks = [t for t in tasks if t.get("swimlane_name") == swimlane]
        if column:
            tasks = [t for t in tasks if t.get("column_name") == column]
        return format_task_list(tasks)

    def create_task(
        self,
        title: str,
        description: str = "",
        swimlane_id: int | None = None,
        column_id: int | None = None,
        swimlane: str | None = None,
        column: str | None = None,
        tags: list[str] | None = None,
        dedup_key: str | None = None,
        author: str | None = None,
    ) -> str:
        col_by_name, _, lane_by_name, _ = self._board_maps()
        column_id = column_id or (col_by_name.get(column) if column else None)
        swimlane_id = swimlane_id or (lane_by_name.get(swimlane) if swimlane else None)
        if dedup_key:
            try:
                tasks = self._enrich_tasks(self.client.call("getAllTasks", {"project_id": self.project_id, "status_id": 1}) or [])
            except KanboardRPCError:
                tasks = []
            existing = find_open_dedup_task(tasks, dedup_key)
            if existing:
                tid = int(existing["id"])
                self.comment_task(tid, f"[DEDUP-UPDATE] {description or title}", author=author)
                return f"DEDUP_UPDATED #{tid} [{dedup_key}]"
            title = f"{title} [DEDUP:{dedup_key}]"

        params: dict[str, Any] = {"project_id": self.project_id, "title": title, "description": description}
        if swimlane_id:
            params["swimlane_id"] = swimlane_id
        if column_id:
            params["column_id"] = column_id
        if tags:
            params["tags"] = tags
        if author:
            uid = self._resolve_user_id(author)
            params["creator_id"] = uid
            params["owner_id"] = uid
        try:
            task_id = self.client.call("createTask", params)
            return f"CREATED #{task_id} {title}"
        except KanboardRPCError:
            self.client.queue_offline_action("createTask", params)
            return f"QUEUED_OFFLINE createTask: {title}"

    def move_task(
        self, task_id: int, column_id: int | None = None, swimlane_id: int = 1, column: str | None = None
    ) -> str:
        col_by_name, _, _, _ = self._board_maps()
        resolved_col = column_id or (col_by_name.get(column) if column else None) or 1
        params = {"project_id": self.project_id, "task_id": task_id, "column_id": resolved_col, "position": 1, "swimlane_id": swimlane_id}
        try:
            self.client.call("moveTaskPosition", params)
            return f"MOVED #{task_id} -> col:{column or resolved_col}"
        except KanboardRPCError:
            self.client.queue_offline_action("moveTaskPosition", params)
            return f"QUEUED_OFFLINE moveTaskPosition #{task_id}"

    def comment_task(self, task_id: int, text: str, user_id: int | None = None, author: str | None = None) -> str:
        resolved_uid = user_id if user_id is not None else self._resolve_user_id(author)
        lines = text.strip().splitlines()[:5]
        if author and lines and not lines[0].startswith(f"[{author}]"):
            lines[0] = f"[{author}] {lines[0]}"
        params = {"task_id": task_id, "user_id": resolved_uid, "content": "\n".join(lines)}
        try:
            self.client.call("createComment", params)
            return f"COMMENTED #{task_id} ({len(lines)} lines)"
        except KanboardRPCError:
            self.client.queue_offline_action("createComment", params)
            return f"QUEUED_OFFLINE createComment #{task_id}"

    def unread_digest(self) -> str:
        tasks = self._enrich_tasks(self.client.call("getAllTasks", {"project_id": self.project_id, "status_id": 1}) or [])
        unread = self.digest_store.filter_unread_tasks(self.project_id, tasks)
        return format_task_list(unread)
