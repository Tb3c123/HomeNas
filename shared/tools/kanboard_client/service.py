"""Kanboard Domain Service Layer (Facade over RPC Client, Formatter, and Digest Store)."""

import os
from typing import Any

from shared.tools.kanboard_client.digest_state import DigestStateStore
from shared.tools.kanboard_client.formatter import (
    find_open_dedup_task,
    format_task_list,
)
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

    def list_tasks(self, swimlane: str | None = None, column: str | None = None) -> str:
        self.client.flush_offline_queue()
        tasks: list[dict[str, Any]] = self.client.call(
            "getAllTasks", {"project_id": self.project_id, "status_id": 1}
        ) or []
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
        tags: list[str] | None = None,
        dedup_key: str | None = None,
    ) -> str:
        if dedup_key:
            try:
                tasks = self.client.call(
                    "getAllTasks", {"project_id": self.project_id, "status_id": 1}
                ) or []
            except KanboardRPCError:
                tasks = []
            existing = find_open_dedup_task(tasks, dedup_key)
            if existing:
                tid = int(existing["id"])
                self.comment_task(tid, f"[DEDUP-UPDATE] {description or title}")
                return f"DEDUP_UPDATED #{tid} [{dedup_key}]"
            title = f"{title} [DEDUP:{dedup_key}]"

        params: dict[str, Any] = {
            "project_id": self.project_id,
            "title": title,
            "description": description,
        }
        if swimlane_id:
            params["swimlane_id"] = swimlane_id
        if column_id:
            params["column_id"] = column_id
        if tags:
            params["tags"] = tags
        try:
            task_id = self.client.call("createTask", params)
            return f"CREATED #{task_id} {title}"
        except KanboardRPCError:
            self.client.queue_offline_action("createTask", params)
            return f"QUEUED_OFFLINE createTask: {title}"

    def move_task(self, task_id: int, column_id: int, swimlane_id: int = 1) -> str:
        params = {
            "project_id": self.project_id,
            "task_id": task_id,
            "column_id": column_id,
            "position": 1,
            "swimlane_id": swimlane_id,
        }
        try:
            self.client.call("moveTaskPosition", params)
            return f"MOVED #{task_id} -> col:{column_id}"
        except KanboardRPCError:
            self.client.queue_offline_action("moveTaskPosition", params)
            return f"QUEUED_OFFLINE moveTaskPosition #{task_id}"

    def comment_task(self, task_id: int, text: str, user_id: int = 1) -> str:
        lines = text.strip().splitlines()[:5]
        compact = "\n".join(lines)
        params = {"task_id": task_id, "user_id": user_id, "content": compact}
        try:
            self.client.call("createComment", params)
            return f"COMMENTED #{task_id} ({len(lines)} lines)"
        except KanboardRPCError:
            self.client.queue_offline_action("createComment", params)
            return f"QUEUED_OFFLINE createComment #{task_id}"

    def unread_digest(self) -> str:
        tasks = self.client.call(
            "getAllTasks", {"project_id": self.project_id, "status_id": 1}
        ) or []
        unread = self.digest_store.filter_unread_tasks(self.project_id, tasks)
        return format_task_list(unread)
