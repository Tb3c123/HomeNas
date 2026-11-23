"""State Machine for HDD/CPU Thermal Policy & Cross-Department Thermal Pause Flag."""

import dataclasses
import json
import pathlib
from typing import Any

DEFAULT_THERMAL_FLAG = pathlib.Path("/tmp/homenas_thermal_state.json")


@dataclasses.dataclass
class ThermalThresholds:
    hdd_warn_c: float = 60.0
    hdd_crit_c: float = 65.0
    hdd_recovery_c: float = 55.0
    cpu_warn_c: float = 88.0
    cpu_crit_c: float = 92.0
    cpu_overload_pct: float = 95.0
    cpu_load5_max: float = 6.0


class ThermalPolicyEngine:
    def __init__(
        self,
        thresholds: ThermalThresholds | None = None,
        state_file: pathlib.Path = DEFAULT_THERMAL_FLAG,
    ) -> None:
        self.t = thresholds or ThermalThresholds()
        self.state_file = state_file
        self.level = "NORMAL"
        self.hdd_warm_minutes = 0.0
        self.cpu_warm_minutes = 0.0
        self.cpu_overload_minutes = 0.0
        self.cool_minutes = 0.0
        self.thermal_paused = False

    def evaluate(self, snapshot: dict[str, Any], elapsed_min: float = 3.0) -> dict[str, Any]:
        hdds = snapshot.get("hdds", {})
        active_temps = [
            float(info["temp_c"])
            for info in hdds.values()
            if info.get("temp_c") is not None
        ]
        disconnected = [k for k, v in hdds.items() if v.get("status") == "disconnected"]
        max_hdd = max(active_temps) if active_temps else 0.0
        cpu_temp = float(snapshot.get("cpu_temp_c", 0.0))
        cpu_pct = float(snapshot.get("cpu_pct", 0.0))
        load5 = float(snapshot.get("load5", 0.0))
        # Eliminate USB I/O-wait false positives: require high real CPU% AND (high load5 OR high CPU temp)
        is_overload = cpu_pct >= self.t.cpu_overload_pct and (load5 > self.t.cpu_load5_max or cpu_temp >= 80.0)

        self.hdd_warm_minutes = (self.hdd_warm_minutes + elapsed_min) if max_hdd >= self.t.hdd_warn_c else 0.0
        self.cpu_warm_minutes = (self.cpu_warm_minutes + elapsed_min) if cpu_temp >= self.t.cpu_warn_c else 0.0
        self.cpu_overload_minutes = (self.cpu_overload_minutes + elapsed_min) if is_overload else 0.0

        reasons: list[str] = []
        if disconnected:
            reasons.append(f"USB Dock disconnected: {','.join(disconnected)}")
        if max_hdd >= self.t.hdd_crit_c:
            reasons.append(f"HDD critical {max_hdd}C >= {self.t.hdd_crit_c}C")
        if self.hdd_warm_minutes > 45.0:
            reasons.append(f"HDD >= {self.t.hdd_warn_c}C for {self.hdd_warm_minutes}m (>45m)")
        if cpu_temp >= self.t.cpu_crit_c and self.cpu_warm_minutes >= 6.0:
            reasons.append(f"CPU critical {cpu_temp}C for {self.cpu_warm_minutes}m")
        if max_hdd >= self.t.hdd_warn_c and is_overload:
            reasons.append(f"Compound risk: HDD {max_hdd}C + CPU overload ({cpu_pct}%/load {load5})")

        if reasons:
            self.level = "EMERGENCY"
            self.thermal_paused = True
            self.cool_minutes = 0.0
        elif self.thermal_paused:
            if max_hdd < self.t.hdd_recovery_c and not is_overload and cpu_temp < self.t.cpu_warn_c:
                self.cool_minutes += elapsed_min
                if self.cool_minutes >= 10.0:
                    self.level = "RECOVERY"
                    self.thermal_paused = False
                    self.cool_minutes = 0.0
            else:
                self.cool_minutes = 0.0
        else:
            warn_reasons: list[str] = []
            if self.hdd_warm_minutes > 15.0:
                warn_reasons.append(f"HDD {max_hdd}C > 15m")
            if self.cpu_overload_minutes > 15.0:
                warn_reasons.append(f"CPU overload > 15m ({cpu_pct}% / load {load5})")
            if self.cpu_warm_minutes > 10.0:
                warn_reasons.append(f"CPU temp {cpu_temp}C > 10m")
            self.level = "WARNING" if warn_reasons else "NORMAL"
            reasons = warn_reasons

        verdict = {
            "level": self.level,
            "thermal_paused": self.thermal_paused,
            "soft_throttle": max_hdd >= self.t.hdd_warn_c and not self.thermal_paused,
            "max_hdd_c": max_hdd,
            "cpu_temp_c": cpu_temp,
            "is_overload": is_overload,
            "reasons": reasons,
        }
        self._persist_flag(verdict)
        return verdict

    def _persist_flag(self, verdict: dict[str, Any]) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(verdict), encoding="utf-8")
