"""Sprint 5 End-to-End Dry Run Tests: 4 Real-World Acceptance Scenarios."""

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from shared.tools.kanboard_client.digest_state import DigestStateStore
from shared.tools.kanboard_client.service import KanboardService
from shared.tools.project_loader.loader import load_project_manifest, verify_tool_permission
from tests.test_sprint1_platform import FakeKanboardClient
from tools.media_ops.disk_balancer import ensure_mirror_structure, select_target_disk
from tools.media_ops.media_watcher import SequentialMediaWatcher
from tools.media_ops.sub_first_matcher import select_sub_first_candidates
from tools.nas_ops.emergency import EmergencyExecutor
from tools.nas_ops.inspector_cli import NasWatchdogCycle
from tools.nas_ops.policy import ThermalPolicyEngine
from tools.nas_ops.reporter import ThermalReporter


class Sprint5EndToEndDryRunTests(unittest.TestCase):
    def test_scenario_1_and_2_thermal_65c_and_sub_first_sequential_media(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            d1, d2 = tpath / "disk1", tpath / "disk2"
            ensure_mirror_structure([d1, d2])

            thermal_flag = tpath / "thermal_state.json"
            kb_client = FakeKanboardClient(tpath / "kb_fallback.jsonl")
            kb_svc = KanboardService(client=kb_client, digest_store=DigestStateStore(tpath / "digest.json"))
            paused: list[str] = []
            cycle = NasWatchdogCycle(
                policy=ThermalPolicyEngine(state_file=thermal_flag),
                emergency=EmergencyExecutor(
                    stoppable=["qbittorrent", "adguard-home"],
                    action_runner=lambda c, a: paused.append(c) or True,
                ),
                reporter=ThermalReporter(
                    log_dir=tpath / "logs",
                    ram_buffer=tpath / "ram.jsonl",
                    tg_queue=tpath / "tg.jsonl",
                    bot_token="",
                    chat_id="",
                ),
                kb_service=kb_svc,
            )

            subs = [{"sub_id": "vi-1", "lang": "vi", "release_tags": ["flux", "ntb"]}]
            rels = [
                {"title": "Dune.2160p.WEB-DL.x265-FLUX", "resolution": "2160p", "source": "WEB-DL", "codec": "x265", "size_gb": 11.5, "release_group": "FLUX"},
                {"title": "Dune.1080p.WEB-DL.x265-NTB", "resolution": "1080p", "source": "WEB-DL", "codec": "x265", "size_gb": 4.5, "release_group": "NTB"},
            ]
            cands = select_sub_first_candidates("movie", subs, rels)
            route = select_target_disk("movie", "Cinema", disk1_root=d1, disk2_root=d2, free_space_override={"disk1": 800, "disk2": 400})

            watcher = SequentialMediaWatcher(min_speed_kbps=500.0, thermal_state_file=thermal_flag)
            watcher.enqueue_job(1, "Dune Part Two", cands, route, initial_eta_sec=1600)
            watcher.enqueue_job(2, "Next Movie", cands, route, initial_eta_sec=1600)

            verdict_hot = cycle.run_once({"cpu_temp_c": 75.0, "cpu_pct": 55.0, "load5": 1.8, "hdds": {"disk1": {"status": "active", "temp_c": 65.5}}})
            self.assertEqual(verdict_hot["level"], "EMERGENCY")
            self.assertEqual(paused, ["qbittorrent"])

            w_thermal = watcher.evaluate_active_download(30.0, 0.0, 99999, state="pausedDL")
            self.assertEqual(w_thermal["action"], "THERMAL_WAIT")

            verdict_cool = cycle.run_once(
                {"cpu_temp_c": 50.0, "cpu_pct": 20.0, "load5": 0.5, "hdds": {"disk1": {"status": "active", "temp_c": 49.0}}},
                elapsed_min=12.0,
            )
            self.assertEqual(verdict_cool["level"], "RECOVERY")
            thermal_flag.write_text(json.dumps({"thermal_paused": False}), encoding="utf-8")

            watcher.evaluate_active_download(32.0, 100.0, 5000)
            w_swap = watcher.evaluate_active_download(33.0, 90.0, 5500)
            self.assertEqual(w_swap["action"], "FALLBACK_SWAP")
            w_done = watcher.evaluate_active_download(100.0, 9000.0, 0, state="completed")
            self.assertEqual(w_done["action"], "COMPLETED")
            self.assertEqual(w_done["next_active_task_id"], 2)

    def test_scenario_3_multi_project_plugin_isolation(self) -> None:
        root_manifest = load_project_manifest(pathlib.Path("project.yaml"))
        self.assertEqual(root_manifest["kanboard_project_id"], 1)
        self.assertTrue(verify_tool_permission(root_manifest, "dept-nas-ops", "nas-inspector"))
        self.assertFalse(verify_tool_permission(root_manifest, "director", "nas-inspector"))

        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            p2_yaml = pathlib.Path(tmp) / "project.yaml"
            p2_yaml.write_text(
                "project:\n  id: sideapp\n  name: SideApp\n  kanboard_project_id: 2\n"
                "departments:\n  director:\n    allowed_tools: [\"kanboard-client\"]\n",
                encoding="utf-8",
            )
            m2 = load_project_manifest(p2_yaml)
            self.assertEqual(m2["id"], "sideapp")
            self.assertEqual(m2["kanboard_project_id"], 2)

    def test_scenario_4_hook_stdin_blocks_151_lines_and_protected_stop(self) -> None:
        bad_payload = json.dumps({"CommandLine": "docker stop adguard-home"})
        proc1 = subprocess.run(
            [sys.executable, "shared/tools/guardrails/pre_tool_guard.py"],
            input=bad_payload,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc1.returncode, 2)

        over_150_code = "\n".join(f"line = {i}" for i in range(152))
        bad_write = json.dumps({"TargetFile": "foo.py", "CodeContent": over_150_code})
        proc2 = subprocess.run(
            [sys.executable, "shared/tools/guardrails/pre_tool_guard.py"],
            input=bad_write,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc2.returncode, 2)


if __name__ == "__main__":
    unittest.main()
