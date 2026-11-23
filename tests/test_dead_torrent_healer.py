"""Unit Tests for v2.0.0 DeadTorrentHealer (2-Step Reannounce -> Radarr/Sonarr Auto-Replace & >=20% Guard)."""

import json
import pathlib
import tempfile
import unittest
from typing import Any

from tools.media_ops.dead_torrent_healer import DeadTorrentHealer


class DeadTorrentHealerTests(unittest.TestCase):
    def test_healer_ignores_thermal_pause_queued_and_replaces_dead_0_seed_torrent(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            state_file = tpath / "healer.json"
            thermal_file = tpath / "thermal.json"

            torrents: list[dict[str, Any]] = [
                # 1. Dead torrent: < 5% progress, 0 seeds, stalledDL
                {"hash": "h_dead", "name": "Dead.Movie.2026.2160p", "state": "stalledDL", "progress": 0.02, "dlspeed": 0, "num_seeds": 0, "num_complete": 0},
                # 2. Queued torrent: 0% progress, 0 seeds, queuedDL -> MUST BE IGNORED
                {"hash": "h_queue", "name": "Queued.Movie.2026", "state": "queuedDL", "progress": 0.0, "dlspeed": 0, "num_seeds": 0, "num_complete": 0},
                # 3. Protected deep torrent: >= 20% progress (45%), total seeds = 8 (> 5) -> NEVER auto-delete, only warn after 2h
                {"hash": "h_deep", "name": "Deep.Movie.2026", "state": "stalledDL", "progress": 0.45, "dlspeed": 0, "num_seeds": 0, "num_complete": 8},
            ]
            reannounced: list[str] = []
            replaced: list[str] = []
            tg_msgs: list[str] = []

            healer = DeadTorrentHealer(
                state_file=state_file,
                thermal_state_file=thermal_file,
                min_speed_kbps=500.0,
                dead_sec=1200,
                deep_warn_sec=7200,
                qbit_fetcher=lambda: torrents,
                reannouncer=lambda h: reannounced.append(h) or True,
                arr_replacer=lambda h: (replaced.append(h) or "Radarr"),
            )

            # A. Thermal paused = True -> skips completely
            thermal_file.write_text(json.dumps({"thermal_paused": True}), encoding="utf-8")
            self.assertEqual(healer.run_heal_cycle(send_tg=tg_msgs.append, now_ts=1000), [])
            self.assertEqual(reannounced, [])

            # B. Thermal normal (t=1000): starts tracking h_dead and h_deep (ignores h_queue)
            thermal_file.write_text(json.dumps({"thermal_paused": False}), encoding="utf-8")
            self.assertEqual(healer.run_heal_cycle(send_tg=tg_msgs.append, now_ts=1000), [])
            saved = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertIn("h_dead", saved["tracked"])
            self.assertIn("h_deep", saved["tracked"])
            self.assertNotIn("h_queue", saved["tracked"])

            # C. t=2300 (> 20m = 1200s): Step 1 triggers reannounce + tracker boost for h_dead (no deletion yet)
            self.assertEqual(healer.run_heal_cycle(send_tg=tg_msgs.append, now_ts=2300), [])
            self.assertEqual(reannounced, ["h_dead"])
            self.assertEqual(replaced, [])

            # D. t=3000 (next 12m cycle, still 0 seeds): Step 2 calls Radarr DELETE blocklist + sends Telegram!
            m_step2 = healer.run_heal_cycle(send_tg=tg_msgs.append, now_ts=3000)
            self.assertEqual(replaced, ["h_dead"])
            self.assertEqual(len(m_step2), 1)
            self.assertIn("♻️ [MEDIA AUTO-REPLACE]", m_step2[0])
            self.assertIn("Radarr", m_step2[0])

            # E. t=8500 (> 2 hours = 7200s): h_deep (>= 20%, 8 seeds) is NOT deleted, only sends 1 gentle warning
            m_deep = healer.run_heal_cycle(send_tg=tg_msgs.append, now_ts=8500)
            self.assertEqual(replaced, ["h_dead"])  # h_deep never in replaced!
            self.assertEqual(len(m_deep), 1)
            self.assertIn("⏳ [MEDIA SLOW >2H] 'Deep.Movie.2026'", m_deep[0])


if __name__ == "__main__":
    unittest.main()
