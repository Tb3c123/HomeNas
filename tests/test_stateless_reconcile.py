"""Unit Tests for v2.0.4 Stateless Reconciliation (qBittorrent Alternative Speed Mode & Paused Containers after Restart)."""

import pathlib
import tempfile
import unittest

from shared.tools.kanboard_client.digest_state import DigestStateStore
from shared.tools.kanboard_client.service import KanboardService
from tests.test_sprint1_platform import FakeKanboardClient
from tools.nas_ops.emergency import EmergencyExecutor
from tools.nas_ops.inspector_cli import NasWatchdogCycle
from tools.nas_ops.policy import ThermalPolicyEngine
from tools.nas_ops.qbit_throttle import QbitThrottleController
from tools.nas_ops.reporter import ThermalReporter


class StatelessReconcileTests(unittest.TestCase):
    def test_qbit_alt_speed_mode_releases_automatically_after_watchdog_restart(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            live_qbit = {"mode": "0", "cleared_global": 0}

            def fake_setter(target: str) -> bool:
                live_qbit["mode"] = target
                return True

            def fake_clear() -> bool:
                live_qbit["cleared_global"] += 1
                return True

            def make_cycle() -> NasWatchdogCycle:
                kb_client = FakeKanboardClient(tpath / "kb.jsonl")
                kb_svc = KanboardService(client=kb_client, digest_store=DigestStateStore(tpath / "digest.json"))
                qbit = QbitThrottleController(
                    mode_getter=lambda: live_qbit["mode"],
                    mode_setter=fake_setter,
                    limit_clearer=fake_clear,
                )
                return NasWatchdogCycle(
                    policy=ThermalPolicyEngine(state_file=tpath / "thermal.json"),
                    emergency=EmergencyExecutor(stoppable=["qbittorrent"], action_runner=lambda c, a: True, paused_checker=lambda c: False),
                    reporter=ThermalReporter(log_dir=tpath / "logs", ram_buffer=tpath / "ram.jsonl", tg_queue=tpath / "tg.jsonl", bot_token="", chat_id=""),
                    kb_service=kb_svc,
                    qbit_throttle=qbit,
                )

            # 1. Watchdog instance #1 sees warm HDD (61C) -> enables Alternative Speed Mode = "1"
            cycle1 = make_cycle()
            snap_warm = {"cpu_temp_c": 58.0, "cpu_pct": 30.0, "load5": 1.2, "hdds": {"disk1": {"status": "active", "temp_c": 61.0}}}
            v1 = cycle1.run_once(snap_warm, elapsed_min=3.0)
            self.assertTrue(v1["soft_throttle"])
            self.assertEqual(live_qbit["mode"], "1")

            # 2. Simulate container restart: brand-new Watchdog instance #2 starts with self._throttled = False
            cycle2 = make_cycle()
            self.assertFalse(cycle2._throttled)

            # 3. HDD cools down to NORMAL (50C) -> must reconcile live qBittorrent mode "1" -> "0" automatically!
            snap_cool = {"cpu_temp_c": 46.0, "cpu_pct": 15.0, "load5": 0.5, "hdds": {"disk1": {"status": "active", "temp_c": 50.0}}}
            v2 = cycle2.run_once(snap_cool, elapsed_min=3.0)
            self.assertEqual(v2["level"], "NORMAL")
            self.assertEqual(live_qbit["mode"], "0")
            self.assertFalse(cycle2._throttled)
            self.assertGreaterEqual(live_qbit["cleared_global"], 1)

    def test_paused_container_auto_unpauses_after_watchdog_restart_when_normal(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            paused_state = {"qbittorrent": True, "jellyfin": False}
            actions: list[str] = []

            def fake_action(container: str, action: str) -> bool:
                actions.append(f"{action}:{container}")
                if action == "unpause":
                    paused_state[container] = False
                return True

            kb_client = FakeKanboardClient(tpath / "kb.jsonl")
            kb_svc = KanboardService(client=kb_client, digest_store=DigestStateStore(tpath / "digest.json"))
            cycle = NasWatchdogCycle(
                policy=ThermalPolicyEngine(state_file=tpath / "thermal.json"),
                emergency=EmergencyExecutor(
                    stoppable=["qbittorrent", "jellyfin"],
                    action_runner=fake_action,
                    paused_checker=lambda c: paused_state.get(c, False),
                ),
                reporter=ThermalReporter(log_dir=tpath / "logs", ram_buffer=tpath / "ram.jsonl", tg_queue=tpath / "tg.jsonl", bot_token="", chat_id=""),
                kb_service=kb_svc,
                qbit_throttle=QbitThrottleController(mode_getter=lambda: "0", mode_setter=lambda m: True, limit_clearer=lambda: True),
            )
            snap_cool = {"cpu_temp_c": 45.0, "cpu_pct": 10.0, "load5": 0.4, "hdds": {"disk1": {"status": "active", "temp_c": 48.0}}}
            verdict = cycle.run_once(snap_cool, elapsed_min=3.0)
            self.assertEqual(verdict["level"], "NORMAL")
            self.assertEqual(actions, ["unpause:qbittorrent"])
            self.assertFalse(paused_state["qbittorrent"])


if __name__ == "__main__":
    unittest.main()
