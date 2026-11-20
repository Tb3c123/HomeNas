"""RAM-Buffered Thermal Reporter (23:55 Single SSD Flush, Weekly Digest & Telegram Queue)."""

import json
import os
import pathlib
import time
import urllib.error
import urllib.request
from typing import Any

DEFAULT_RAM_BUFFER = pathlib.Path("/tmp/thermal_samples_today.jsonl")
DEFAULT_TG_QUEUE = pathlib.Path("/tmp/telegram_offline_queue.jsonl")


class ThermalReporter:
    def __init__(
        self,
        log_dir: pathlib.Path = pathlib.Path("logs/thermal"),
        ram_buffer: pathlib.Path = DEFAULT_RAM_BUFFER,
        tg_queue: pathlib.Path = DEFAULT_TG_QUEUE,
        bot_token: str | None = None,
        chat_id: str | None = None,
    ) -> None:
        self.log_dir = log_dir
        self.ram_buffer = ram_buffer
        self.tg_queue = tg_queue
        self.bot_token = bot_token if bot_token is not None else os.environ.get("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = chat_id if chat_id is not None else os.environ.get("TELEGRAM_CHAT_ID", "")

    def record_sample_in_ram(self, snapshot: dict[str, Any], verdict: dict[str, Any]) -> None:
        self.ram_buffer.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": int(time.time()),
            "hour": time.strftime("%H:00"),
            "cpu_c": snapshot.get("cpu_temp_c", 0.0),
            "load5": snapshot.get("load5", 0.0),
            "hdd_max_c": verdict.get("max_hdd_c", 0.0),
            "level": verdict.get("level", "NORMAL"),
        }
        with self.ram_buffer.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(entry) + "\n")

    def flush_daily_log_to_ssd(self, date_str: str | None = None, keep_days: int = 30) -> pathlib.Path | None:
        if not self.ram_buffer.exists():
            return None
        lines = [ln for ln in self.ram_buffer.read_text(encoding="utf-8").splitlines() if ln]
        if not lines:
            return None
        samples = [json.loads(ln) for ln in lines]
        hdd_vals = [float(s["hdd_max_c"]) for s in samples if s.get("hdd_max_c")]
        cpu_vals = [float(s["cpu_c"]) for s in samples if s.get("cpu_c")]
        peak_hours = sorted({s["hour"] for s in samples if float(s.get("hdd_max_c", 0)) >= 60.0})
        alerts = sum(1 for s in samples if s.get("level") in ("WARNING", "EMERGENCY"))
        day = date_str or time.strftime("%Y-%m-%d")
        summary = {
            "date": day,
            "samples": len(samples),
            "hdd_min_c": min(hdd_vals) if hdd_vals else 0.0,
            "hdd_avg_c": round(sum(hdd_vals) / len(hdd_vals), 1) if hdd_vals else 0.0,
            "hdd_max_c": max(hdd_vals) if hdd_vals else 0.0,
            "cpu_avg_c": round(sum(cpu_vals) / len(cpu_vals), 1) if cpu_vals else 0.0,
            "cpu_max_c": max(cpu_vals) if cpu_vals else 0.0,
            "peak_hours": peak_hours,
            "alerts_count": alerts,
        }
        self.log_dir.mkdir(parents=True, exist_ok=True)
        out_path = self.log_dir / f"{day}.json"
        out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        self.ram_buffer.unlink(missing_ok=True)
        self._rotate_daily_logs(keep_days)
        return out_path

    def _rotate_daily_logs(self, keep_days: int) -> None:
        daily_files = sorted(self.log_dir.glob("20*-*-*.json"))
        for old_file in daily_files[:-keep_days]:
            old_file.unlink(missing_ok=True)

    def generate_weekly_markdown(self, week_label: str | None = None) -> pathlib.Path:
        self.log_dir.mkdir(parents=True, exist_ok=True)
        daily_files = sorted(self.log_dir.glob("20*-*-*.json"))[-7:]
        records = [json.loads(f.read_text(encoding="utf-8")) for f in daily_files]
        label = week_label or time.strftime("%Y-W%W")
        lines = [f"# Weekly Thermal Summary ({label})", "", "| Date | HDD Avg/Max | CPU Avg/Max | Peak Hours | Alerts |", "| :--- | :--- | :--- | :--- | :--- |"]
        for r in records:
            peaks = ",".join(r.get("peak_hours", [])) or "-"
            lines.append(
                f"| {r['date']} | {r['hdd_avg_c']}C / {r['hdd_max_c']}C | "
                f"{r['cpu_avg_c']}C / {r['cpu_max_c']}C | {peaks} | {r['alerts_count']} |"
            )
        out_md = self.log_dir / f"weekly-{label}.md"
        out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return out_md

    def send_telegram(self, text: str) -> bool:
        if not self.bot_token or not self.chat_id:
            self._queue_tg(text)
            return False
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = json.dumps({"chat_id": self.chat_id, "text": text}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200
        except (urllib.error.URLError, TimeoutError, OSError):
            self._queue_tg(text)
            return False

    def _queue_tg(self, text: str) -> None:
        self.tg_queue.parent.mkdir(parents=True, exist_ok=True)
        with self.tg_queue.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps({"ts": int(time.time()), "text": text}) + "\n")
