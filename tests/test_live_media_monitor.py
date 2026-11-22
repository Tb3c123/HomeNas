"""Unit Tests for 0-Token 24/7 LiveMediaMonitor (v1.8.2: Zero-Spam Daily Digest & Queue Clear)."""

import json
import pathlib
import tempfile
import unittest
from typing import Any

from tools.media_ops.arr_monitor import LiveMediaMonitor


class LiveMediaMonitorTests(unittest.TestCase):
    def test_daily_digest_batches_completions_and_stalls_without_per_movie_spam(self) -> None:
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

            # Cycle 1 (t=1000): Baseline initialization
            self.assertEqual(mon.poll_and_notify(send_tg=sent_messages.append, now_ts=1000), [])

            # Cycle 2 (t=1600): h1 finishes (stoppedUP); h2 still downloading slowly -> MUST NOT spam Telegram per movie!
            current_torrents[0]["state"] = "stoppedUP"
            current_torrents[0]["progress"] = 1.0
            current_torrents[1]["state"] = "downloading"
            current_torrents[1]["dlspeed"] = 1024
            current_torrents[1]["progress"] = 0.102
            self.assertEqual(mon.poll_and_notify(send_tg=sent_messages.append, now_ts=1600), [])
            self.assertIn("Xong hôm nay: 1", mon.format_queue_status_line())

            # Cycle 3 (t=2300): h2 stalled >= 1200s -> recorded in daily state, zero immediate spam
            self.assertEqual(mon.poll_and_notify(send_tg=sent_messages.append, now_ts=2300), [])

            # 23:55 Daily Digest Flush -> sends exactly 1 consolidated daily message!
            digest = mon.flush_daily_digest(send_tg=sent_messages.append, date_str="2026-11-22")
            self.assertIsNotNone(digest)
            self.assertEqual(len(sent_messages), 1)
            self.assertIn("📊 [MEDIA DAILY DIGEST — 2026-11-22]", sent_messages[0])
            self.assertIn("Iron.Man.2008.2160p", sent_messages[0])
            self.assertIn("Thor.2011.2160p", sent_messages[0])
            self.assertIn("Bazarr Sub Việt đang chờ: 3", sent_messages[0])

            # Cycle 4 (t=2500): Last torrent h2 finishes -> fires MEDIA QUEUE CLEAR!
            current_torrents[1]["state"] = "stalledUP"
            current_torrents[1]["progress"] = 1.0
            a4 = mon.poll_and_notify(send_tg=sent_messages.append, now_ts=2500)
            self.assertEqual(len(a4), 1)
            self.assertIn("🎉 [MEDIA QUEUE CLEAR]", a4[0])

    def test_vanished_torrent_imported_by_arr_recorded_in_daily_digest(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            state_file = tpath / "media_state.json"
            thermal_file = tpath / "thermal.json"
            thermal_file.write_text(json.dumps({"thermal_paused": False}), encoding="utf-8")

            torrents: list[dict[str, Any]] = [
                {"hash": "h_fast", "name": "Avengers.2012.2160p", "state": "downloading", "progress": 0.92, "dlspeed": 20971520, "num_seeds": 25},
                {"hash": "h_other", "name": "Still.Running.Movie", "state": "downloading", "progress": 0.30, "dlspeed": 5242880, "num_seeds": 10},
            ]
            mon = LiveMediaMonitor(
                state_file=state_file, thermal_state_file=thermal_file,
                qbit_fetcher=lambda: torrents, bazarr_fetcher=lambda: 0,
            )
            mon.poll_and_notify(now_ts=1000)

            # h_fast vanishes after Radarr import while h_other keeps running -> recorded silently in completed_today
            torrents.pop(0)
            self.assertEqual(mon.poll_and_notify(now_ts=1180), [])
            saved = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual(saved["completed_today"], ["Avengers.2012.2160p"])


if __name__ == "__main__":
    unittest.main()
