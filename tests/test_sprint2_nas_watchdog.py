"""Unit Tests for Sprint 2 (v1.8.3): Zero-Noise Thermal Policy, I/O-Wait Immunity & Emergency Cooldown."""

import pathlib
import sqlite3
import tempfile
import unittest

from shared.tools.kanboard_client.digest_state import DigestStateStore
from shared.tools.kanboard_client.service import KanboardService
from tests.test_sprint1_platform import FakeKanboardClient
from tools.nas_ops.backup_kanboard import backup_kanboard_sqlite
from tools.nas_ops.emergency import EmergencyExecutor
from tools.nas_ops.inspector_cli import NasWatchdogCycle
from tools.nas_ops.policy import ThermalPolicyEngine
from tools.nas_ops.reporter import ThermalReporter
from tools.nas_ops.sensors import parse_smartctl_output


class Sprint2NasWatchdogTests(unittest.TestCase):
    def test_smartctl_standby_and_active_parsing(self) -> None:
        res_standby = parse_smartctl_output(2, "Device is in STANDBY mode, exit(2)")
        self.assertEqual(res_standby["status"], "standby")
        self.assertIsNone(res_standby["temp_c"])

        res_json = parse_smartctl_output(0, '{"temperature": {"current": 41}}')
        self.assertEqual(res_json["status"], "active")
        self.assertEqual(res_json["temp_c"], 41.0)

    def test_usb_iowait_high_load5_does_not_trigger_false_cpu_overload(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            state_file = pathlib.Path(tmp) / "thermal_state.json"
            engine = ThermalPolicyEngine(state_file=state_file)

            # High load5=9.0 due to USB HDD I/O wait, but real CPU=22% and CPU temp=48C -> MUST stay NORMAL!
            snap_iowait = {
                "cpu_temp_c": 48.0,
                "cpu_pct": 22.0,
                "load5": 9.0,
                "hdds": {"disk1": {"status": "active", "temp_c": 56.0}, "disk2": {"status": "standby", "temp_c": None}},
            }
            v_io = engine.evaluate(snap_iowait, elapsed_min=30.0)
            self.assertEqual(v_io["level"], "NORMAL")
            self.assertFalse(v_io["is_overload"])
            self.assertFalse(v_io["thermal_paused"])

            snap_warm = {
                "cpu_temp_c": 65.0,
                "cpu_pct": 40.0,
                "load5": 1.5,
                "hdds": {"disk1": {"status": "active", "temp_c": 61.0}, "disk2": {"status": "active", "temp_c": 58.0}},
            }
            v_warn = engine.evaluate(snap_warm, elapsed_min=18.0)
            self.assertEqual(v_warn["level"], "WARNING")
            self.assertTrue(v_warn["soft_throttle"])

            snap_compound = {
                "cpu_temp_c": 85.0,
                "cpu_pct": 97.0,
                "load5": 6.5,
                "hdds": {"disk1": {"status": "active", "temp_c": 61.0}},
            }
            v_emerg = engine.evaluate(snap_compound, elapsed_min=3.0)
            self.assertEqual(v_emerg["level"], "EMERGENCY")
            self.assertTrue(v_emerg["thermal_paused"])

            snap_cool = {
                "cpu_temp_c": 48.0,
                "cpu_pct": 20.0,
                "load5": 1.0,
                "hdds": {"disk1": {"status": "active", "temp_c": 50.0}},
            }
            v_rec = engine.evaluate(snap_cool, elapsed_min=12.0)
            self.assertEqual(v_rec["level"], "RECOVERY")
            self.assertFalse(v_rec["thermal_paused"])

    def test_emergency_executor_protects_core_containers(self) -> None:
        called: list[str] = []
        executor = EmergencyExecutor(
            stoppable=["qbittorrent", "adguard-home", "portainer", "jellyfin", "kanboard"],
            action_runner=lambda c, a: called.append(f"{a}:{c}") or True,
        )
        paused = executor.trigger_emergency_mitigation("pause")
        self.assertEqual(paused, ["qbittorrent", "jellyfin"])
        self.assertNotIn("pause:adguard-home", called)
        self.assertNotIn("pause:kanboard", called)

    def test_warning_is_silent_on_telegram_and_emergency_respects_cooldown(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            reporter = ThermalReporter(
                log_dir=tpath / "logs",
                ram_buffer=tpath / "ram_samples.jsonl",
                tg_queue=tpath / "tg_queue.jsonl",
                bot_token="",
                chat_id="",
            )
            kb_client = FakeKanboardClient(tpath / "kb_fallback.jsonl")
            kb_svc = KanboardService(client=kb_client, digest_store=DigestStateStore(tpath / "digest.json"))
            policy = ThermalPolicyEngine(state_file=tpath / "thermal.json")
            actions: list[str] = []
            emergency = EmergencyExecutor(
                stoppable=["qbittorrent"],
                action_runner=lambda c, a: actions.append(f"{a}:{c}") or True,
            )
            cycle = NasWatchdogCycle(
                policy=policy, emergency=emergency, reporter=reporter, kb_service=kb_svc, emergency_cooldown_sec=1800,
            )

            # 1. WARNING must NOT send instant Telegram
            snap_warn = {"cpu_temp_c": 60.0, "cpu_pct": 30.0, "load5": 1.0, "hdds": {"disk1": {"status": "active", "temp_c": 61.0}}}
            v_w = cycle.run_once(snap_warn, elapsed_min=18.0, now_ts=1000.0)
            self.assertEqual(v_w["level"], "WARNING")
            self.assertFalse(reporter.tg_queue.exists())

            # 2. EMERGENCY sends 1 Telegram at t=2000, then suppresses repeat at t=2180 (< 1800s cooldown)
            snap_crit = {"cpu_temp_c": 78.0, "cpu_pct": 60.0, "load5": 2.0, "hdds": {"disk1": {"status": "active", "temp_c": 66.0}}}
            cycle.run_once(snap_crit, elapsed_min=3.0, now_ts=2000.0)
            self.assertEqual(len(reporter.tg_queue.read_text(encoding="utf-8").splitlines()), 1)

            cycle.run_once(snap_crit, elapsed_min=3.0, now_ts=2180.0)
            self.assertEqual(len(reporter.tg_queue.read_text(encoding="utf-8").splitlines()), 1)

            # 3. RECOVERY auto-unpauses and sends 1 recovery Telegram
            snap_cool = {"cpu_temp_c": 46.0, "cpu_pct": 15.0, "load5": 0.5, "hdds": {"disk1": {"status": "active", "temp_c": 49.0}}}
            v_r = cycle.run_once(snap_cool, elapsed_min=12.0, now_ts=3000.0)
            self.assertEqual(v_r["level"], "RECOVERY")
            self.assertIn("unpause:qbittorrent", actions)
            self.assertEqual(len(reporter.tg_queue.read_text(encoding="utf-8").splitlines()), 2)

            daily_json = reporter.flush_daily_log_to_ssd(date_str="2026-11-19")
            self.assertIsNotNone(daily_json)
            weekly_md = reporter.generate_weekly_markdown(week_label="2026-W46")
            self.assertIn("66.0C", weekly_md.read_text(encoding="utf-8"))

    def test_kanboard_hot_sqlite_backup_and_rotation(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            src_db = tpath / "kb.sqlite"
            with sqlite3.connect(str(src_db)) as conn:
                conn.execute("CREATE TABLE tasks (id INT PRIMARY KEY, title TEXT)")
                conn.execute("INSERT INTO tasks VALUES (1, 'Test backup')")
            bdir = tpath / "backups"
            for i in range(9):
                backup_kanboard_sqlite(src_db, bdir, keep_copies=7, stamp=f"20261119-03000{i}")
            self.assertEqual(len(list(bdir.glob("kanboard-*.sqlite"))), 7)


if __name__ == "__main__":
    unittest.main()
