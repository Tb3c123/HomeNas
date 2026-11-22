"""Unit Tests for 0-Token 24/7 LiveMediaMonitor (v1.8.1: Vanished *arr Import, Anti-Reset Stall & stoppedUP)."""

import json
import pathlib
import tempfile
import unittest
from typing import Any

from tools.media_ops.arr_monitor import LiveMediaMonitor


class LiveMediaMonitorTests(unittest.TestCase):
    def test_completion_stalled_queue_clear_and_thermal_suppression(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            state_file = tpath / "media_state.json"
            thermal_file = tpath / "thermal.json"
            thermal_file.write_text(json.dumps({"thermal_paused": False}), encoding="utf-8")

            current_torrents: list[dict[str, Any]] = [
                {"hash": "h1", "name": "Iron.Man.2008.2160p", "state": "downloading", "progress": 0.45, "dlspeed": 5242880, "num_seeds": 12},
                {"hash": "h2", "name": "Thor.2011.2160p", "state": "stalledDL", "progress": 0.10, "dlspeed": 0, "num_seeds": 0},
                {"hash": "h0", "name": "Old.Seeded.Movie", "state": "uploading", "progress": 1.0, "dlspeed": 0, "num_seeds": 5},
            ]
            sent_messages: list[str] = []
            mon = LiveMediaMonitor(
                state_file=state_file,
                thermal_state_file=thermal_file,
                stall_threshold_sec=1200,
                qbit_fetcher=lambda: current_torrents,
                bazarr_fetcher=lambda: 3,
            )

            # Cycle 1 (t=1000): Baseline initialization (no spam for already-seeded h0)
            self.assertEqual(mon.poll_and_notify(send_tg=sent_messages.append, now_ts=1000), [])
            status_line = mon.format_queue_status_line()
            self.assertIn("Iron.Man.2008.2160p", status_line)
            self.assertIn("45% @ 5.0 MB/s", status_line)

            # Cycle 2 (t=1600): h1 reaches stoppedUP (qBittorrent v5.x); h2 flickers to downloading at 1 KB/s (must NOT reset stall timer!)
            current_torrents[0]["state"] = "stoppedUP"
            current_torrents[0]["progress"] = 1.0
            current_torrents[1]["state"] = "downloading"
            current_torrents[1]["dlspeed"] = 1024  # 1 KB/s < 50 KB/s threshold
            current_torrents[1]["progress"] = 0.102  # < 1% progress delta
            a2 = mon.poll_and_notify(send_tg=sent_messages.append, now_ts=1600)
            self.assertEqual(len(a2), 1)
            self.assertIn("🎬 [MEDIA DONE] 'Iron.Man.2008.2160p'", a2[0])

            # Cycle 3 (t=2000): Thermal paused = True -> must suppress alert AND preserve stalled_since=1000
            thermal_file.write_text(json.dumps({"thermal_paused": True}), encoding="utf-8")
            self.assertEqual(mon.poll_and_notify(send_tg=sent_messages.append, now_ts=2000), [])

            # Cycle 4 (t=2300): Thermal normal -> (2300 - 1000 = 1300s >= 1200s) fires MEDIA STALLED immediately without reset!
            thermal_file.write_text(json.dumps({"thermal_paused": False}), encoding="utf-8")
            a4 = mon.poll_and_notify(send_tg=sent_messages.append, now_ts=2300)
            self.assertEqual(len(a4), 1)
            self.assertIn("⚠️ [MEDIA STALLED] 'Thor.2011.2160p'", a4[0])

            # Cycle 5 (t=2500): Last torrent h2 finishes -> both MEDIA DONE and MEDIA QUEUE CLEAR fire!
            current_torrents[1]["state"] = "stalledUP"
            current_torrents[1]["progress"] = 1.0
            a5 = mon.poll_and_notify(send_tg=sent_messages.append, now_ts=2500)
            self.assertEqual(len(a5), 2)
            self.assertIn("🎬 [MEDIA DONE] 'Thor.2011.2160p'", a5[0])
            self.assertIn("🎉 [MEDIA QUEUE CLEAR]", a5[1])

    def test_vanished_torrent_imported_by_arr_and_canceled_cleanup(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            state_file = tpath / "media_state.json"
            thermal_file = tpath / "thermal.json"
            thermal_file.write_text(json.dumps({"thermal_paused": False}), encoding="utf-8")

            torrents: list[dict[str, Any]] = [
                {"hash": "h_fast", "name": "Avengers.2012.2160p", "state": "downloading", "progress": 0.92, "dlspeed": 20971520, "num_seeds": 25},
                {"hash": "h_cancel", "name": "Canceled.Movie", "state": "stalledDL", "progress": 0.15, "dlspeed": 0, "num_seeds": 0},
            ]
            mon = LiveMediaMonitor(
                state_file=state_file, thermal_state_file=thermal_file,
                qbit_fetcher=lambda: torrents, bazarr_fetcher=lambda: 0,
            )
            mon.poll_and_notify(now_ts=1000)

            # Both torrents vanish before next 3m poll: h_fast (>=0.85) was imported & removed by Radarr; h_cancel (<0.85) was deleted by user
            torrents.clear()
            alerts = mon.poll_and_notify(now_ts=1180)
            self.assertEqual(len(alerts), 2)
            self.assertIn("🎬 [MEDIA DONE] 'Avengers.2012.2160p' đã tải xong & import 100%!", alerts[0])
            self.assertIn("🎉 [MEDIA QUEUE CLEAR]", alerts[1])

            saved = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual(saved["active_meta"], {})
            self.assertEqual(saved["stalled_since"], {})


if __name__ == "__main__":
    unittest.main()
