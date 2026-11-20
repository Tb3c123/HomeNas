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
from tools.nas_ops.backup_kanboard import backup_kanboard_sqlite
from tools.nas_ops.emergency import EmergencyExecutor
from tools.nas_ops.policy import ThermalPolicyEngine
from tools.nas_ops.reporter import ThermalReporter
from tools.nas_ops.sensors import collect_snapshot


class NasWatchdogCycle:
    def __init__(
        self,
        policy: ThermalPolicyEngine | None = None,
        emergency: EmergencyExecutor | None = None,
        reporter: ThermalReporter | None = None,
        kb_service: KanboardService | None = None,
    ) -> None:
        self.policy = policy or ThermalPolicyEngine()
        self.emergency = emergency or EmergencyExecutor()
        self.reporter = reporter or ThermalReporter()
        self.kb = kb_service or KanboardService()
        self._last_flush_day = ""
        self._last_backup_day = ""
        self._last_weekly_label = ""

    def run_once(self, snapshot: dict[str, Any] | None = None, elapsed_min: float = 3.0) -> dict[str, Any]:
        snap = snapshot or collect_snapshot()
        verdict = self.policy.evaluate(snap, elapsed_min=elapsed_min)
        self.reporter.record_sample_in_ram(snap, verdict)
        level = verdict["level"]
        reasons = "; ".join(verdict.get("reasons", []))

        if level == "WARNING":
            msg = f"⚠️ [NAS WARNING] HDD:{verdict['max_hdd_c']}C CPU:{verdict['cpu_temp_c']}C | {reasons}"
            self.reporter.send_telegram(msg)
            self.kb.create_task("[NAS] Thermal/Load Warning", msg, tags=["daily-alert"], dedup_key="nas:thermal")
        elif level == "EMERGENCY":
            paused = self.emergency.trigger_emergency_mitigation("pause")
            msg = f"🚨 [NAS EMERGENCY] {reasons} | Auto-paused: {','.join(paused) or 'none'}"
            self.reporter.send_telegram(msg)
            self.kb.create_task("[NAS] EMERGENCY Thermal Mitigation", msg, tags=["emergency"], dedup_key="nas:emergency")
            verdict["mitigated_containers"] = paused
        elif level == "RECOVERY":
            msg = f"✅ [NAS RECOVERY] Cooled down (HDD:{verdict['max_hdd_c']}C). Ready for PO review to unpause."
            self.reporter.send_telegram(msg)
        return verdict

    def run_scheduled_housekeeping(self) -> None:
        now = time.localtime()
        day = time.strftime("%Y-%m-%d", now)
        week = time.strftime("%Y-W%W", now)
        if now.tm_hour == 23 and now.tm_min >= 55 and self._last_flush_day != day:
            self.reporter.flush_daily_log_to_ssd(date_str=day)
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
            self.kb.create_task(f"[NAS] Weekly Thermal Review {week}", f"File: {md_path}", tags=["weekly-review"], dedup_key=f"weekly:{week}")
            self.reporter.send_telegram(
                f"📊 [NAS WEEKLY] Đã tổng hợp báo cáo tuần {week} ({md_path}).\n"
                "Mở antigravity-cli và dán: Chạy weekly-thermal-review cho báo cáo tuần mới nhất."
            )
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
        print("[homenas-watchdog] Started 3m thermal daemon + 4-command Telegram listener.", flush=True)
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
