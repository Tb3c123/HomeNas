"""Unit Tests for Sprint 1: Shared Platform Guardrails & Kanboard Client."""

import pathlib
import tempfile
import unittest
from typing import Any

from shared.tools.guardrails.pre_tool_guard import (
    audit_repository,
    check_command_safety,
    check_file_compliance,
)
from shared.tools.kanboard_client.service import KanboardService
from shared.tools.kanboard_client.digest_state import DigestStateStore
from shared.tools.kanboard_client.formatter import IDLE_MESSAGE, format_inline_receipt
from shared.tools.kanboard_client.rpc_client import KanboardClient, KanboardRPCError


class FakeKanboardClient(KanboardClient):
    def __init__(self, fallback_path: pathlib.Path) -> None:
        super().__init__(url="http://mock/jsonrpc.php", token="tok", fallback_path=fallback_path)
        self.online = True
        self.tasks: list[dict[str, Any]] = []
        self.comments: list[dict[str, Any]] = []

    def call(self, method: str, params: dict[str, Any] | None = None) -> Any:
        if not self.online:
            raise KanboardRPCError("Mock offline")
        params = params or {}
        if method == "getAllTasks":
            return list(self.tasks)
        if method == "createTask":
            new_id = len(self.tasks) + 1
            self.tasks.append(
                {
                    "id": new_id,
                    "title": params.get("title", ""),
                    "description": params.get("description", ""),
                    "column_name": "Ready",
                    "swimlane_name": "NAS Ops",
                    "tags": params.get("tags", []),
                    "is_active": "1",
                    "date_modification": 100 + new_id,
                }
            )
            return new_id
        if method == "createComment":
            self.comments.append(params)
            return len(self.comments)
        if method == "moveTaskPosition":
            return True
        return None


class Sprint1PlatformTests(unittest.TestCase):
    def test_kanboard_empty_dedup_and_digest(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tmp_path = pathlib.Path(tmp)
            client = FakeKanboardClient(tmp_path / "fallback.jsonl")
            store = DigestStateStore(tmp_path / "digest.json")
            svc = KanboardService(client=client, digest_store=store, project_id=1)

            self.assertEqual(svc.list_tasks(), IDLE_MESSAGE)
            self.assertEqual(svc.unread_digest(), IDLE_MESSAGE)

            res1 = svc.create_task("[NAS] HDD 61C", "Temp warning", dedup_key="thermal:sda")
            self.assertIn("CREATED #1", res1)
            res2 = svc.create_task("[NAS] HDD 62C", "Still warm", dedup_key="thermal:sda")
            self.assertEqual(res2, "DEDUP_UPDATED #1 [thermal:sda]")
            self.assertEqual(len(client.tasks), 1)
            self.assertEqual(len(client.comments), 1)

            digest1 = svc.unread_digest()
            self.assertIn("#1 [Ready] [NAS Ops]", digest1)
            self.assertEqual(svc.unread_digest(), IDLE_MESSAGE)

    def test_kanboard_offline_fallback_and_flush(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tmp_path = pathlib.Path(tmp)
            client = FakeKanboardClient(tmp_path / "fallback.jsonl")
            store = DigestStateStore(tmp_path / "digest.json")
            svc = KanboardService(client=client, digest_store=store, project_id=1)

            client.online = False
            res = svc.create_task("[MEDIA] Queue movie", "Offline test")
            self.assertIn("QUEUED_OFFLINE", res)
            self.assertTrue(client.fallback_path.exists())

            client.online = True
            out = svc.list_tasks()
            self.assertIn("#1 [Ready]", out)
            self.assertFalse(client.fallback_path.exists())

    def test_inline_receipt_and_pre_tool_guard(self) -> None:
        receipt = format_inline_receipt("DONE", 42, "dept-nas-ops", "SMART healthy 38C")
        self.assertEqual(receipt, "[✅ DONE | #42 | dept-nas-ops] SMART healthy 38C")

        self.assertTrue(check_command_safety("docker stop adguard-home"))
        self.assertTrue(check_command_safety("git push origin main --force"))
        self.assertEqual(check_command_safety("docker pause qbittorrent"), [])

        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            long_file = pathlib.Path(tmp) / "too_long.py"
            long_file.write_text("\n".join(f"x = {i}" for i in range(155)), encoding="utf-8")
            self.assertTrue(check_file_compliance(long_file))

        self.assertEqual(audit_repository(pathlib.Path(".")), [])


if __name__ == "__main__":
    unittest.main()
