#!/usr/bin/env python3
"""Zero-Noise NAS Inspector CLI & 0-Token Watchdog Daemon for dept-nas-ops."""

import argparse
import json
import os
import pathlib
import sys
import time
from typing import Any

from shared.tools.kanboard_client.service import KanboardService
from tools.media_ops.arr_monitor import LiveMediaMonitor
from tools.media_ops.dead_torrent_healer import DeadTorrentHealer
from tools.nas_ops.backup_kanboard import backup_kanboard_sqlite
from tools.nas_ops.emergency import SOFT_THROTTLE_BPS, EmergencyExecutor
from tools.nas_ops.policy import ThermalPolicyEngine
from tools.nas_ops.reporter import ThermalReporter
from tools.nas_ops.sensors import collect_snapshot

EMERGENCY_COOLDOWN_SEC = 1800


class NasWatchdogCycle:
    def __init__(
        self,
        policy: ThermalPolicyEngine | None = None,
        emergency: EmergencyExecutor | None = None,
        reporter: ThermalReporter | None = None,
        kb_service: KanboardService | None = None,
        media_monitor: LiveMediaMonitor | None = None,
        dead_healer: DeadTorrentHealer | None = None,
        emergency_cooldown_sec: int = EMERGENCY_COOLDOWN_SEC,
    ) -> None:
        self.policy = policy or ThermalPolicyEngine()
        self.emergency = emergency or EmergencyExecutor()
        self.reporter = reporter or ThermalReporter()
        self.kb = kb_service or KanboardService()
        self.media_monitor = media_monitor or LiveMediaMonitor()
        self.dead_healer = dead_healer or DeadTorrentHealer()
        self.emergency_cooldown_sec = emergency_cooldown_sec
        self._last_flush_day = ""
        self._last_backup_day = ""
        self._last_weekly_label = ""
        self._last_emergency_tg_ts = 0.0
        self._throttled = False
        self._cycle_count = 0

    def run_once(self, snapshot: dict[str, Any] | None = None, elapsed_min: float = 3.0, now_ts: float | None = None) -> dict[str, Any]:
        snap = snapshot or collect_snapshot()
        now = float(now_ts if now_ts is not None else time.time())
        verdict = self.policy.evaluate(snap, elapsed_min=elapsed_min)
        self.reporter.record_sample_in_ram(snap, verdict)
        level = verdict["level"]
        reasons = "; ".join(verdict.get("reasons", []))

        if verdict.get("soft_throttle") and not self._throttled:
            self.emergency.set_qbit_download_limit(SOFT_THROTTLE_BPS)
            self._throttled = True
        elif not verdict.get("soft_throttle") and self._throttled and level == "NORMAL":
            self.emergency.set_qbit_download_limit(0)
            self._throttled = False

        if level == "WARNING":
            msg = f"⚠️ [NAS WARNING] HDD:{verdict['max_hdd_c']}C CPU:{verdict['cpu_temp_c']}C | {reasons}"
            self.kb.create_task("[NAS] Thermal/Load Warning", msg, tags=["daily-alert"], dedup_key="nas:thermal", author="watchdog")
        elif level == "EMERGENCY":
            paused = self.emergency.trigger_emergency_mitigation("pause")
            verdict["mitigated_containers"] = paused
            msg = f"🚨 [NAS EMERGENCY] {reasons} | Auto-paused: {','.join(paused) or 'none'}"
            self.kb.create_task("[NAS] EMERGENCY Thermal Mitigation", msg, tags=["emergency"], dedup_key="nas:emergency", author="watchdog")
            if (now - self._last_emergency_tg_ts) >= self.emergency_cooldown_sec:
                self.reporter.send_telegram(msg)
                self._last_emergency_tg_ts = now
        elif level == "RECOVERY":
            unpaused = self.emergency.trigger_emergency_mitigation("unpause")
            self.emergency.set_qbit_download_limit(0)
            self._throttled = False
            self._last_emergency_tg_ts = 0.0
            msg = f"✅ [NAS AUTO-RECOVERY] Cooled down (HDD:{verdict['max_hdd_c']}C). Auto-unpaused: {','.join(unpaused) or 'all'}."
            self.reporter.send_telegram(msg)

        verdict["media_alerts"] = self.media_monitor.poll_and_notify(self.reporter.send_telegram)
        self._cycle_count += 1
        if self._cycle_count % 4 == 0:  # Every 12 minutes (4 x 3m cycles)
            verdict["healer_alerts"] = self.dead_healer.run_heal_cycle(self.reporter.send_telegram)
        return verdict

    def run_scheduled_housekeeping(self) -> None:
        now = time.localtime()
        day = time.strftime("%Y-%m-%d", now)
        week = time.strftime("%Y-W%W", now)
        if now.tm_hour == 23 and now.tm_min >= 55 and self._last_flush_day != day:
            self.reporter.flush_daily_log_to_ssd(date_str=day)
            self.media_monitor.flush_daily_digest(self.reporter.send_telegram, date_str=day)
            self._last_flush_day = day
        if now.tm_hour == 3 and now.tm_min < 10 and self._last_backup_day != day:
            src = pathlib.Path("/kanboard-data/db.sqlite")
            dst = pathlib.Path(os.environ.get("KANBOARD_BACKUP_DIR", "/mnt/disk2/Backups/kanboard"))
            try:
                if src.exists():
                    backup_kanboard_sqlite(src, dst)
            except Exception as exc:
                self.reporter.send_telegram(f"❌ [NAS BACKUP FAIL] Kanboard SQLite backup error: {exc}")
            self._last_backup_day = day
        if now.tm_wday == 6 and now.tm_hour == 20 and now.tm_min < 10 and self._last_weekly_label != week:
            md_path = self.reporter.generate_weekly_markdown(week_label=week)
            self.kb.create_task(f"[NAS] Weekly Thermal Review {week}", f"File: {md_path}", tags=["weekly-review"], dedup_key=f"weekly:{week}", author="watchdog")
            self.reporter.send_telegram(f"📊 [NAS WEEKLY] Đã tổng hợp báo cáo tuần {week} ({md_path}).\nMở antigravity-cli và dán: Chạy weekly-thermal-review cho báo cáo tuần mới nhất.")
            self._last_weekly_label = week


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nas-inspector", description="Zero-Noise NAS Inspector")
    parser.add_argument("--once", action="store_true", help="Run one watchdog evaluation cycle")
    parser.add_argument("--daemon", action="store_true", help="Run continuous 3-minute 0-token watchdog loop")
    args = parser.parse_args(argv)
    if args.daemon:
        import threading
        from tools.nas_ops.tg_commands import TelegramCommandHandler

        cycle = NasWatchdogCycle()
        tg_handler = TelegramCommandHandler(kb_service=cycle.kb)
        threading.Thread(target=tg_handler.run_forever, name="tg-commands", daemon=True).start()
        print("[homenas-watchdog] Started 3m Zero-Noise thermal daemon + 4-command Telegram listener.", flush=True)
        while True:
            try:
                cycle.run_once(elapsed_min=3.0)
                cycle.run_scheduled_housekeeping()
            except Exception as exc:
                print(f"[homenas-watchdog] Cycle error: {exc}", file=sys.stderr, flush=True)
            time.sleep(180)
    snap = collect_snapshot()
    if args.once:
        verdict = NasWatchdogCycle().run_once(snap)
        print(json.dumps({"snapshot": snap, "verdict": verdict}, separators=(",", ":")))
    else:
        print(json.dumps(snap, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
