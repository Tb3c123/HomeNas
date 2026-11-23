"""Hardware Sensors for Morefine N6 (Intel N200) and Acasis Dual-10TB HDDs."""

import json
import os
import pathlib
import re
import shutil
import subprocess
import time
from typing import Any

_LAST_VALID_HDD: dict[str, dict[str, Any]] = {}


def read_cpu_temp_c(thermal_root: pathlib.Path = pathlib.Path("/sys/class/thermal")) -> float:
    temps: list[float] = []
    if thermal_root.exists():
        for zone in sorted(thermal_root.glob("thermal_zone*/temp")):
            try:
                raw = int(zone.read_text(encoding="utf-8").strip())
                if raw > 0:
                    temps.append(raw / 1000.0 if raw > 200 else float(raw))
            except (ValueError, OSError):
                continue
    return round(max(temps), 1) if temps else 42.0


def _read_proc_stat_cpu(proc_root: pathlib.Path) -> tuple[int, int] | None:
    try:
        first = (proc_root / "stat").read_text(encoding="utf-8").splitlines()[0].split()
        if first[0] != "cpu" or len(first) < 6:
            return None
        vals = [int(v) for v in first[1:9]]
        idle_and_iowait = vals[3] + vals[4]
        total = sum(vals)
        active = total - idle_and_iowait
        return active, total
    except (OSError, ValueError, IndexError):
        return None


def read_load_and_ram(proc_root: pathlib.Path = pathlib.Path("/proc"), sample_delay_sec: float = 0.2) -> dict[str, float]:
    load5, cpu_pct, ram_pct = 0.0, 0.0, 0.0
    try:
        parts = (proc_root / "loadavg").read_text(encoding="utf-8").split()
        load5 = float(parts[1])
    except (OSError, ValueError, IndexError):
        pass

    s1 = _read_proc_stat_cpu(proc_root)
    if s1 is not None and sample_delay_sec > 0:
        time.sleep(sample_delay_sec)
        s2 = _read_proc_stat_cpu(proc_root)
        if s2 is not None and (s2[1] - s1[1]) > 0:
            cpu_pct = round(max(0.0, min(100.0, ((s2[0] - s1[0]) / (s2[1] - s1[1])) * 100.0)), 1)

    try:
        mem = (proc_root / "meminfo").read_text(encoding="utf-8")
        total = int(re.search(r"MemTotal:\s+(\d+)", mem).group(1))  # type: ignore[union-attr]
        avail = int(re.search(r"MemAvailable:\s+(\d+)", mem).group(1))  # type: ignore[union-attr]
        if total > 0:
            ram_pct = round(((total - avail) / total) * 100.0, 1)
    except (OSError, ValueError, AttributeError):
        pass
    return {"load5": load5, "cpu_pct": cpu_pct, "ram_pct": ram_pct}


def parse_smartctl_output(returncode: int, stdout: str) -> dict[str, Any]:
    if returncode == 2 or "STANDBY" in stdout.upper() or "SLEEP" in stdout.upper():
        return {"status": "standby", "temp_c": None}
    try:
        data = json.loads(stdout)
        power_mode = str(data.get("power_mode", "")).lower()
        if "standby" in power_mode:
            return {"status": "standby", "temp_c": None}
        temp = data.get("temperature", {}).get("current")
        if isinstance(temp, (int, float)):
            return {"status": "active", "temp_c": float(temp)}
    except json.JSONDecodeError:
        pass
    match = re.search(r"(?:194|190)\s+Temperature_Celsius\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\d+)", stdout)
    if not match:
        match = re.search(r"Current Drive Temperature:\s+(\d+)", stdout)
    if match:
        return {"status": "active", "temp_c": float(match.group(1))}
    return {"status": "unknown", "temp_c": None}


def read_hdd_smart(device_path: str, max_stale_cycles: int = 2) -> dict[str, Any]:
    if not pathlib.Path(device_path).exists():
        _LAST_VALID_HDD.pop(device_path, None)
        return {"device": device_path, "status": "disconnected", "temp_c": None}
    try:
        proc = subprocess.run(
            ["smartctl", "-n", "standby", "-d", "sat", "-A", "-j", device_path],
            capture_output=True, text=True, timeout=10, check=False,
        )
        res = parse_smartctl_output(proc.returncode, proc.stdout)
        res["device"] = device_path
        if res["status"] in ("active", "standby"):
            _LAST_VALID_HDD[device_path] = {"res": dict(res), "misses": 0}
            return res
    except (OSError, subprocess.SubprocessError):
        pass

    cached = _LAST_VALID_HDD.get(device_path)
    if cached and int(cached.get("misses", 0)) < max_stale_cycles:
        cached["misses"] = int(cached["misses"]) + 1
        fallback = dict(cached["res"])
        fallback["stale_cache"] = True
        return fallback
    return {"device": device_path, "status": "error", "temp_c": None}


def read_disk_usage_pct(paths: list[str] | None = None) -> dict[str, float]:
    targets = paths or ["/", "/mnt/disk1", "/mnt/disk2"]
    usage: dict[str, float] = {}
    for p in targets:
        if pathlib.Path(p).exists():
            total, used, _ = shutil.disk_usage(p)
            usage[p] = round((used / total) * 100.0, 1) if total > 0 else 0.0
    return usage


def collect_snapshot() -> dict[str, Any]:
    d1 = os.environ.get("DISK1_BY_ID", "/dev/sda")
    d2 = os.environ.get("DISK2_BY_ID", "/dev/sdb")
    sys_metrics = read_load_and_ram()
    return {
        "cpu_temp_c": read_cpu_temp_c(),
        "cpu_pct": sys_metrics["cpu_pct"],
        "load5": sys_metrics["load5"],
        "ram_pct": sys_metrics["ram_pct"],
        "hdds": {"disk1": read_hdd_smart(d1), "disk2": read_hdd_smart(d2)},
        "disk_usage_pct": read_disk_usage_pct(),
    }
