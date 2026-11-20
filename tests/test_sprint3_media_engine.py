"""Unit Tests for Sprint 3: 1:1 Disk Mirror, Sub-First Matcher & Sequential 25% ETA Media Watcher."""

import json
import pathlib
import tempfile
import unittest

from tools.media_ops.disk_balancer import ensure_mirror_structure, select_target_disk
from tools.media_ops.media_watcher import SequentialMediaWatcher, compute_check_interval_sec
from tools.media_ops.sub_first_matcher import select_sub_first_candidates


class Sprint3MediaEngineTests(unittest.TestCase):
    def test_mirror_1_to_1_structure_and_disk_balancing(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            d1 = tpath / "disk1"
            d2 = tpath / "disk2"
            created = ensure_mirror_structure([d1, d2])
            self.assertTrue(len(created) >= 20)
            self.assertFalse((d1 / "Media" / "Movies" / "4K_UHD").exists())
            self.assertTrue((d1 / "Media" / "Movies" / "Cinema").exists())
            self.assertTrue((d2 / "Media" / "Movies" / "Cinema").exists())

            route_movie = select_target_disk(
                "movie",
                "Cinema",
                disk1_root=d1,
                disk2_root=d2,
                free_space_override={"disk1": 500, "disk2": 900},
            )
            self.assertEqual(route_movie["disk"], "disk2")
            self.assertEqual(route_movie["qbit_category"], "radarr-disk2")

            (d1 / "Media" / "TVShows" / "International" / "Loki (2021)" / "Season 01").mkdir(parents=True)
            route_tv = select_target_disk(
                "tv",
                "International",
                series_title="Loki (2021)",
                disk1_root=d1,
                disk2_root=d2,
                free_space_override={"disk1": 100, "disk2": 9000},
            )
            self.assertEqual(route_tv["disk"], "disk1")
            self.assertFalse(route_tv["needs_consolidation"])

    def test_sub_first_flexible_2k_4k_and_tv_1080p_no_tvrip(self) -> None:
        subs = [
            {"sub_id": "sub1", "lang": "vi", "release_tags": ["flux", "framestor"]},
        ]
        movie_releases = [
            {"title": "Movie.2026.2160p.WEB-DL.x265-FLUX", "resolution": "2160p", "source": "WEB-DL", "codec": "x265", "size_gb": 11.8, "release_group": "FLUX"},
            {"title": "Movie.2026.1080p.WEB-DL.x264-FLUX", "resolution": "1080p", "source": "WEB-DL", "codec": "x264", "size_gb": 4.2, "release_group": "FLUX"},
            {"title": "Movie.2026.2160p.Remux-FRAMESTOR", "resolution": "2160p", "source": "Remux", "codec": "AVC", "size_gb": 55.0, "release_group": "FRAMESTOR"},
            {"title": "Movie.2026.2160p.WEB-DL.x265-NOSUBGROUP", "resolution": "2160p", "source": "WEB-DL", "codec": "x265", "size_gb": 6.0, "release_group": "NOSUBGROUP"},
        ]
        ranked_movies = select_sub_first_candidates("movie", subs, movie_releases)
        self.assertEqual(len(ranked_movies), 2)
        self.assertEqual(ranked_movies[0]["release"]["resolution"], "2160p")
        self.assertEqual(ranked_movies[0]["release"]["size_gb"], 11.8)

        tv_releases = [
            {"title": "Show.S01E01.1080p.TVRip-FLUX", "resolution": "1080p", "source": "TVRip", "codec": "x264", "size_gb": 1.0, "release_group": "FLUX"},
            {"title": "Show.S01E01.1080p.WEB-DL.x265-FLUX", "resolution": "1080p", "source": "WEB-DL", "codec": "x265", "size_gb": 1.4, "release_group": "FLUX"},
        ]
        ranked_tv = select_sub_first_candidates("tv", subs, tv_releases)
        self.assertEqual(len(ranked_tv), 1)
        self.assertEqual(ranked_tv[0]["release"]["source"], "WEB-DL")

    def test_sequential_queue_adaptive_eta_and_thermal_pause_guard(self) -> None:
        self.assertEqual(compute_check_interval_sec(200), 180)
        self.assertEqual(compute_check_interval_sec(2000), 500)
        self.assertEqual(compute_check_interval_sec(10000), 1200)

        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            thermal_flag = pathlib.Path(tmp) / "thermal.json"
            watcher = SequentialMediaWatcher(min_speed_kbps=500.0, thermal_state_file=thermal_flag)
            cands = [{"release": {"title": "Cand1"}, "subtitle": {"sub_id": "s1"}}, {"release": {"title": "Cand2"}, "subtitle": {"sub_id": "s2"}}]

            job1 = watcher.enqueue_job(101, "Movie A", cands, {"disk": "disk1"}, initial_eta_sec=1200)
            job2 = watcher.enqueue_job(102, "Movie B", cands, {"disk": "disk2"}, initial_eta_sec=1200)
            self.assertEqual(job1["status"], "DOWNLOADING")
            self.assertEqual(job2["status"], "QUEUED")

            thermal_flag.write_text(json.dumps({"thermal_paused": True}), encoding="utf-8")
            res_therm = watcher.evaluate_active_download(20.0, 0.0, 99999, state="pausedDL")
            self.assertEqual(res_therm["action"], "THERMAL_WAIT")

            thermal_flag.write_text(json.dumps({"thermal_paused": False}), encoding="utf-8")
            res_slow1 = watcher.evaluate_active_download(25.0, 120.0, 3600)
            self.assertEqual(res_slow1["action"], "WARN_SLOW")
            res_swap = watcher.evaluate_active_download(26.0, 100.0, 4000)
            self.assertEqual(res_swap["action"], "FALLBACK_SWAP")
            self.assertEqual(res_swap["new_candidate_index"], 1)

            res_done = watcher.evaluate_active_download(100.0, 8000.0, 0, state="completed")
            self.assertEqual(res_done["action"], "COMPLETED")
            self.assertEqual(res_done["next_active_task_id"], 102)


if __name__ == "__main__":
    unittest.main()
