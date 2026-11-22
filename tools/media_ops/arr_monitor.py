"""0-Token 24/7 Live Media Monitor (qBittorrent + Bazarr Read-Only Poller & Daily Digest)."""

import http.cookiejar, json, os, pathlib, time, urllib.error, urllib.parse, urllib.request
from typing import Any, Callable
from tools.media_ops.media_watcher import is_thermal_paused
from tools.nas_ops.policy import DEFAULT_THERMAL_FLAG

DEFAULT_MEDIA_STATE = pathlib.Path("/tmp/homenas_media_monitor.json")
DONE_STATES = {"uploading", "stalledup", "pausedup", "stoppedup", "queuedup", "checkingup", "forcedup"}
ACTIVE_DL_STATES = {"downloading", "forceddl", "metadl", "allocating", "checkingdl"}
STALLED_STATES = {"stalleddl", "error", "missingfiles"}
SLOW_SPEED_BYTES, RECOVERY_SPEED_BYTES = 50 * 1024, 100 * 1024


def fetch_qbit_torrents(qbit_url: str | None = None, user: str | None = None, password: str | None = None, timeout: int = 4) -> list[dict[str, Any]] | None:
    base = (qbit_url or os.environ.get("QBIT_URL", "")).rstrip("/")
    if not base:
        return None
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    try:
        u, p = (user if user is not None else os.environ.get("QBIT_USER", "admin")), (password if password is not None else os.environ.get("QBIT_PASS", ""))
        if p and p != "replace_with_qbit_password":
            opener.open(urllib.request.Request(f"{base}/api/v2/auth/login", data=urllib.parse.urlencode({"username": u, "password": p}).encode()), timeout=timeout)
        with opener.open(urllib.request.Request(f"{base}/api/v2/torrents/info"), timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
        return None


def fetch_bazarr_wanted_count(bazarr_url: str | None = None, api_key: str | None = None, timeout: int = 4) -> int | None:
    base, key = (bazarr_url or os.environ.get("BAZARR_URL", "")).rstrip("/"), (api_key if api_key is not None else os.environ.get("BAZARR_API_KEY", ""))
    if not base or not key or key == "replace_with_bazarr_key":
        return None
    try:
        total = 0
        for ep in ("movies/wanted", "episodes/wanted"):
            with urllib.request.urlopen(urllib.request.Request(f"{base}/api/{ep}?length=1", headers={"X-API-KEY": key}), timeout=timeout) as resp:
                total += int(json.loads(resp.read().decode("utf-8")).get("total", 0))
        return total
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError):
        return None


class LiveMediaMonitor:
    def __init__(self, state_file: pathlib.Path = DEFAULT_MEDIA_STATE, thermal_state_file: pathlib.Path = DEFAULT_THERMAL_FLAG, stall_threshold_sec: int | None = None, qbit_fetcher: Callable[[], list[dict[str, Any]] | None] = fetch_qbit_torrents, bazarr_fetcher: Callable[[], int | None] = fetch_bazarr_wanted_count) -> None:
        self.state_file, self.thermal_state_file = state_file, thermal_state_file
        self.stall_threshold_sec = stall_threshold_sec if stall_threshold_sec is not None else int(os.environ.get("MEDIA_STALL_THRESHOLD_SEC", "1200"))
        self.qbit_fetcher, self.bazarr_fetcher = qbit_fetcher, bazarr_fetcher

    def _load_state(self) -> dict[str, Any]:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"initialized": False, "active_meta": {}, "done_notified": [], "completed_today": [], "stalled_since": {}, "stalled_today": {}, "had_queue": False}

    def _save_state(self, st: dict[str, Any]) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(st), encoding="utf-8")

    def poll_and_notify(self, send_tg: Callable[[str], Any] | None = None, now_ts: int | None = None) -> list[str]:
        torrents = self.qbit_fetcher()
        if torrents is None:
            return []
        now, st, thermal = int(now_ts if now_ts is not None else time.time()), self._load_state(), is_thermal_paused(self.thermal_state_file)
        alerts, seen_hashes, incomplete_count = [], set(), 0
        active_meta: dict[str, dict[str, Any]] = dict(st.get("active_meta") or {})
        done_notified, completed_today = set(st.get("done_notified", [])), list(st.get("completed_today", []))
        stalled_since, stalled_today = dict(st.get("stalled_since", {})), dict(st.get("stalled_today", {}))

        for t in torrents:
            h, name = str(t.get("hash") or t.get("name") or ""), str(t.get("name") or "")
            seen_hashes.add(h)
            state, prog, speed = str(t.get("state") or "").lower(), float(t.get("progress") or 0.0), int(t.get("dlspeed") or 0)
            prev_prog = float((active_meta.get(h) or {}).get("progress", 0.0))
            if not (prog >= 1.0 or state in DONE_STATES):
                incomplete_count += 1
                active_meta[h] = {"name": name, "progress": prog}
                prog_delta = prog - prev_prog
                if not thermal and (state in STALLED_STATES or (state in ACTIVE_DL_STATES and speed < SLOW_SPEED_BYTES and prog_delta < 0.01)):
                    first_ts = stalled_since.setdefault(h, now)
                    if (now - first_ts) >= self.stall_threshold_sec:
                        stalled_today[h] = f"{name} ({prog*100:.0f}%, kẹt {(now - first_ts)//60}p)"
                elif not thermal and (speed >= RECOVERY_SPEED_BYTES or prog_delta >= 0.01):
                    stalled_since.pop(h, None)
                    stalled_today.pop(h, None)
            else:
                for d in (stalled_since, stalled_today, active_meta):
                    d.pop(h, None)
                if st.get("initialized") and h not in done_notified and name not in completed_today:
                    completed_today.append(name)
                done_notified.add(h)

        for vh in [k for k in active_meta if k not in seen_hashes]:
            meta, _, _ = active_meta.pop(vh), stalled_since.pop(vh, None), stalled_today.pop(vh, None)
            vname = str(meta.get("name", vh))
            if st.get("initialized") and float(meta.get("progress", 0.0)) >= 0.85 and vh not in done_notified:
                if vname not in completed_today:
                    completed_today.append(vname)
                done_notified.add(vh)

        if st.get("initialized") and st.get("had_queue") and incomplete_count == 0:
            wanted = self.bazarr_fetcher()
            sub_note = f" | Bazarr Sub Việt chờ: {wanted}" if wanted is not None else ""
            alerts.append(f"🎉 [MEDIA QUEUE CLEAR] Toàn bộ hàng đợi đã tải xong 100% ({len(completed_today)} phim hoàn tất hôm nay)!{sub_note}")

        self._save_state({"initialized": True, "active_meta": active_meta, "done_notified": sorted(done_notified)[-300:], "completed_today": completed_today[-100:], "stalled_since": stalled_since, "stalled_today": stalled_today, "had_queue": incomplete_count > 0})
        for msg in (alerts if send_tg else []):
            send_tg(msg)  # type: ignore[misc]
        return alerts

    def flush_daily_digest(self, send_tg: Callable[[str], Any] | None = None, date_str: str | None = None) -> str | None:
        st = self._load_state()
        done_list, stalled_map = list(st.get("completed_today", [])), dict(st.get("stalled_today", {}))
        if not done_list and not stalled_map:
            return None
        lines = [f"📊 [MEDIA DAILY DIGEST — {date_str or time.strftime('%Y-%m-%d')}]"]
        if done_list:
            lines.append(f"✅ Hoàn tất hôm nay ({len(done_list)} phim): " + ", ".join(done_list[:10]) + (f" (+{len(done_list)-10} phim)" if len(done_list) > 10 else ""))
        if stalled_map:
            lines.append(f"⚠️ Đang kẹt quá ngưỡng ({len(stalled_map)}): " + "; ".join(list(stalled_map.values())[:5]))
        lines.append(f"⏳ Hàng đợi: {self.format_queue_status_line()}")
        wanted = self.bazarr_fetcher()
        if wanted is not None:
            lines.append(f"🔤 Bazarr Sub Việt đang chờ: {wanted}")
        st["completed_today"] = []
        self._save_state(st)
        msg = "\n".join(lines)
        if send_tg:
            send_tg(msg)
        return msg

    def format_queue_status_line(self) -> str:
        torrents = self.qbit_fetcher()
        if torrents is None:
            return "qBittorrent: offline/chưa kết nối"
        done_cnt = len(self._load_state().get("completed_today", []))
        inc = [t for t in torrents if float(t.get("progress") or 0.0) < 1.0 and str(t.get("state") or "").lower() not in DONE_STATES]
        if not inc:
            return f"Idle (0 đang tải | Xong hôm nay: {done_cnt} | Tổng seed: {len(torrents)})"
        act = [t for t in inc if str(t.get("state") or "").lower() in ACTIVE_DL_STATES]
        stl = [t for t in inc if str(t.get("state") or "").lower() in STALLED_STATES]
        q_cnt = len(inc) - len(act) - len(stl)
        if act:
            top = act[0]
            return f"Đang tải '{str(top.get('name'))[:32]}' ({float(top.get('progress') or 0)*100:.0f}% @ {float(top.get('dlspeed') or 0)/(1024*1024):.1f} MB/s) | Xong hôm nay: {done_cnt} | Chờ: {q_cnt} | Kẹt: {len(stl)}"
        return f"Đang tải: 0 | Xong hôm nay: {done_cnt} | Chờ: {q_cnt} | Kẹt: {len(stl)}"
