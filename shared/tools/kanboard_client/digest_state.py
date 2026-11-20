"""Unread Digest Timestamp State Tracker per Kanboard Project."""

import json
import pathlib
from typing import Any

DEFAULT_STATE_FILE = pathlib.Path(".state/last_digest_ts.json")


class DigestStateStore:
    def __init__(self, state_file: pathlib.Path = DEFAULT_STATE_FILE) -> None:
        self.state_file = state_file

    def _load(self) -> dict[str, int]:
        if not self.state_file.exists():
            return {}
        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def get_last_ts(self, project_id: int) -> int:
        return int(self._load().get(str(project_id), 0))

    def set_last_ts(self, project_id: int, timestamp: int) -> None:
        data = self._load()
        data[str(project_id)] = int(timestamp)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def filter_unread_tasks(
        self, project_id: int, tasks: list[dict[str, Any]], update_ts: bool = True
    ) -> list[dict[str, Any]]:
        last_ts = self.get_last_ts(project_id)
        unread: list[dict[str, Any]] = []
        max_ts = last_ts
        for task in tasks:
            mod_ts = int(task.get("date_modification") or task.get("date_creation") or 0)
            if mod_ts > last_ts:
                unread.append(task)
                if mod_ts > max_ts:
                    max_ts = mod_ts
        if update_ts and max_ts > last_ts:
            self.set_last_ts(project_id, max_ts)
        return unread
