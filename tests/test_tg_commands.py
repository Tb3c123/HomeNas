"""Unit Tests for 4-Command Telegram Bot Listener, Menu Cleanup & /reconnect Flag Bridge."""

import pathlib
import tempfile
import time
import unittest
from typing import Any

from shared.tools.kanboard_client.digest_state import DigestStateStore
from shared.tools.kanboard_client.service import KanboardService
from tests.test_sprint1_platform import FakeKanboardClient
from tools.nas_ops.tg_commands import BOT_COMMANDS, TelegramCommandHandler


class TelegramCommandsTests(unittest.TestCase):
    def test_sync_bot_menu_clears_old_and_sets_exact_4_commands(self) -> None:
        calls: list[tuple[str, dict[str, Any]]] = []

        def fake_api(method: str, payload: dict[str, Any]) -> dict[str, Any]:
            calls.append((method, payload))
            return {"ok": True}

        handler = TelegramCommandHandler(bot_token="tok", allowed_chat_id="8608642317", api_caller=fake_api)
        self.assertTrue(handler.sync_bot_menu())
        self.assertEqual(calls[0][0], "deleteMyCommands")
        self.assertEqual(calls[1][0], "setMyCommands")
        cmds = [c["command"] for c in calls[1][1]["commands"]]
        self.assertEqual(cmds, ["status", "reconnect", "digest", "help"])
        self.assertEqual(len(BOT_COMMANDS), 4)

    def test_strict_chat_id_whitelist_and_commands(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            kb_client = FakeKanboardClient(tpath / "kb.jsonl")
            kb_svc = KanboardService(client=kb_client, digest_store=DigestStateStore(tpath / "d.json"))
            kb_svc.create_task("[NAS] Check fan", "Desc")

            snap = {
                "cpu_temp_c": 58.0,
                "load5": 0.4,
                "ram_pct": 22.0,
                "hdds": {
                    "disk1": {"status": "standby", "temp_c": None},
                    "disk2": {"status": "active", "temp_c": 41.0},
                },
            }
            handler = TelegramCommandHandler(
                bot_token="tok",
                allowed_chat_id="8608642317",
                state_dir=tpath,
                kb_service=kb_svc,
                snapshot_fn=lambda: snap,
            )

            self.assertIsNone(handler.handle_message("999999999", "/reconnect"))
            self.assertIsNone(handler.handle_message("999999999", "/status"))

            out_status = handler.handle_message("8608642317", "/status") or ""
            self.assertIn("58.0°C", out_status)
            self.assertIn("disk1=standby", out_status)
            self.assertIn("disk2=41.0°C", out_status)

            out_rec = handler.handle_message("8608642317", "/reconnect") or ""
            self.assertIn("home-nas", out_rec)
            self.assertTrue((tpath / "reconnect_remote.flag").exists())

            out_dig = handler.handle_message("8608642317", "/digest") or ""
            self.assertIn("#1", out_dig)

            out_help = handler.handle_message("8608642317", "/help") or ""
            self.assertIn("/reconnect", out_help)

            rc_file = tpath / "remote_status.txt"
            rc_file.write_text("[2026-11-19] ONLINE name=home-nas", encoding="utf-8")
            self.assertIsNone(handler.check_remote_status_update())
            time.sleep(0.02)
            rc_file.write_text("[2026-11-19] ONLINE (telegram-/reconnect) https://agy.example/r", encoding="utf-8")
            update = handler.check_remote_status_update() or ""
            self.assertIn("Remote Control Update", update)


if __name__ == "__main__":
    unittest.main()
