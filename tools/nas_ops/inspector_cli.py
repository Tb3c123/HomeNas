#!/usr/bin/env python3
"""Zero-Noise NAS Inspector CLI & Watchdog Orchestrator for dept-nas-ops."""

import argparse
import json
import sys
from typing import Any

from shared.tools.kanboard_client.service import KanboardService
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nas-inspector", description="Zero-Noise NAS Inspector")
    parser.add_argument("--once", action="store_true", help="Run one watchdog evaluation cycle")
    args = parser.parse_args(argv)
    snap = collect_snapshot()
    if args.once:
        verdict = NasWatchdogCycle().run_once(snap)
        print(json.dumps({"snapshot": snap, "verdict": verdict}, separators=(",", ":")))
    else:
        print(json.dumps(snap, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
