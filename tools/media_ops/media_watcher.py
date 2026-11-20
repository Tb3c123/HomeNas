"""Sequential 1-at-a-Time Download Queue & Adaptive 25% ETA Watcher (0-Token)."""

import json
import pathlib
from typing import Any

from tools.nas_ops.policy import DEFAULT_THERMAL_FLAG


def compute_check_interval_sec(eta_sec: int, ratio: float = 0.25) -> int:
    raw = int(eta_sec * ratio)
    return max(180, min(1200, raw))


def is_thermal_paused(thermal_state_file: pathlib.Path = DEFAULT_THERMAL_FLAG) -> bool:
    if not thermal_state_file.exists():
        return False
    try:
        data = json.loads(thermal_state_file.read_text(encoding="utf-8"))
        return bool(data.get("thermal_paused", False))
    except (json.JSONDecodeError, OSError):
        return False


class SequentialMediaWatcher:
    def __init__(
        self,
        min_speed_kbps: float = 500.0,
        thermal_state_file: pathlib.Path = DEFAULT_THERMAL_FLAG,
    ) -> None:
        self.min_speed_kbps = min_speed_kbps
        self.thermal_state_file = thermal_state_file
        self.queue: list[dict[str, Any]] = []
        self.active_job: dict[str, Any] | None = None

    def enqueue_job(
        self,
        task_id: int,
        title: str,
        candidates: list[dict[str, Any]],
        target_disk_info: dict[str, Any],
        initial_eta_sec: int = 1800,
    ) -> dict[str, Any]:
        if not candidates:
            return {"status": "NEEDS_APPROVAL", "reason": "No matched Vietnamese subtitle found."}
        job = {
            "task_id": task_id,
            "title": title,
            "candidates": list(candidates),
            "current_index": 0,
            "target_disk": target_disk_info,
            "initial_eta_sec": initial_eta_sec,
            "check_interval_sec": compute_check_interval_sec(initial_eta_sec),
            "slow_strikes": 0,
            "status": "QUEUED",
        }
        if self.active_job is None:
            job["status"] = "DOWNLOADING"
            self.active_job = job
        else:
            self.queue.append(job)
        return job

    def evaluate_active_download(
        self,
        progress_pct: float,
        speed_kbps: float,
        current_eta_sec: int,
        state: str = "downloading",
    ) -> dict[str, Any]:
        if self.active_job is None:
            return {"action": "IDLE"}

        job = self.active_job
        if progress_pct >= 100.0 or state.lower() in ("completed", "seeding"):
            completed_pair = job["candidates"][job["current_index"]]
            finished_id = job["task_id"]
            self._advance_queue()
            return {
                "action": "COMPLETED",
                "task_id": finished_id,
                "pair": completed_pair,
                "next_active_task_id": self.active_job["task_id"] if self.active_job else None,
            }

        if is_thermal_paused(self.thermal_state_file):
            return {
                "action": "THERMAL_WAIT",
                "task_id": job["task_id"],
                "reason": "Paused by dept-nas-ops due to HDD thermal protection.",
            }

        is_stalled = state.lower() in ("stalleddl", "error", "missingfiles")
        is_slow = speed_kbps < self.min_speed_kbps or current_eta_sec > int(job["initial_eta_sec"] * 2.0)

        if is_stalled or is_slow:
            job["slow_strikes"] += 1
        else:
            job["slow_strikes"] = 0
            job["check_interval_sec"] = compute_check_interval_sec(current_eta_sec)
            return {"action": "CONTINUE", "task_id": job["task_id"], "next_check_sec": job["check_interval_sec"]}

        if job["slow_strikes"] < 2 and not is_stalled:
            return {"action": "WARN_SLOW", "task_id": job["task_id"], "strikes": job["slow_strikes"]}

        next_idx = job["current_index"] + 1
        if next_idx < len(job["candidates"]):
            job["current_index"] = next_idx
            job["slow_strikes"] = 0
            return {
                "action": "FALLBACK_SWAP",
                "task_id": job["task_id"],
                "new_candidate_index": next_idx,
                "new_pair": job["candidates"][next_idx],
            }

        blocked_id = job["task_id"]
        self._advance_queue()
        return {
            "action": "BLOCKED_EXHAUSTED",
            "task_id": blocked_id,
            "next_active_task_id": self.active_job["task_id"] if self.active_job else None,
        }

    def _advance_queue(self) -> None:
        if self.queue:
            self.active_job = self.queue.pop(0)
            self.active_job["status"] = "DOWNLOADING"
        else:
            self.active_job = None
