"""Unit Tests for 0-Token 24/7 LiveMediaMonitor (qBittorrent + Bazarr + Telegram Alerts & /status)."""

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
                stall_threshold_sec=2700,
                qbit_fetcher=lambda: current_torrents,
                bazarr_fetcher=lambda: 3,
            )

            # Cycle 1 (t=1000): Baseline initialization (no spam for already-seeded h0)
            a1 = mon.poll_and_notify(send_tg=sent_messages.append, now_ts=1000)
            self.assertEqual(a1, [])
            status_line = mon.format_queue_status_line()
            self.assertIn("Iron.Man.2008.2160p", status_line)
            self.assertIn("45% @ 5.0 MB/s", status_line)
            self.assertIn("Kẹt: 1", status_line)

            # Cycle 2 (t=2000): h1 finishes (100%), h2 stalled for 1000s (< 2700s threshold)
            current_torrents[0]["state"] = "uploading"
            current_torrents[0]["progress"] = 1.0
            a2 = mon.poll_and_notify(send_tg=sent_messages.append, now_ts=2000)
            self.assertEqual(len(a2), 1)
            self.assertIn("🎬 [MEDIA DONE] 'Iron.Man.2008.2160p'", a2[0])
            self.assertIn("Bazarr Sub Việt chờ: 3", a2[0])

            # Cycle 3 (t=3800): Thermal paused = True -> should NOT fire stalled alert for h2
            thermal_file.write_text(json.dumps({"thermal_paused": True}), encoding="utf-8")
            a3 = mon.poll_and_notify(send_tg=sent_messages.append, now_ts=3800)
            self.assertEqual(a3, [])

            # Cycle 4 (t=4000) & Cycle 5 (t=6800): Thermal normal -> h2 stalled >= 45m fires once
            thermal_file.write_text(json.dumps({"thermal_paused": False}), encoding="utf-8")
            mon.poll_and_notify(send_tg=sent_messages.append, now_ts=4000)
            a5 = mon.poll_and_notify(send_tg=sent_messages.append, now_ts=6800)
            self.assertEqual(len(a5), 1)
            self.assertIn("⚠️ [MEDIA STALLED] 'Thor.2011.2160p'", a5[0])
            self.assertIn("Direct Fetch", a5[0])

            # Cycle 6 (t=7000): No duplicate stalled spam
            self.assertEqual(mon.poll_and_notify(send_tg=sent_messages.append, now_ts=7000), [])

            # Cycle 7 (t=7500): Last torrent h2 finishes -> both MEDIA DONE and MEDIA QUEUE CLEAR fire!
            current_torrents[1]["state"] = "stalledUP"
            current_torrents[1]["progress"] = 1.0
            a7 = mon.poll_and_notify(send_tg=sent_messages.append, now_ts=7500)
            self.assertEqual(len(a7), 2)
            self.assertIn("🎬 [MEDIA DONE] 'Thor.2011.2160p'", a7[0])
            self.assertIn("🎉 [MEDIA QUEUE CLEAR]", a7[1])
            self.assertIn("Idle (0 đang tải / 3 hoàn tất)", mon.format_queue_status_line())


if __name__ == "__main__":
    unittest.main()
