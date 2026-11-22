"""0-Token 24/7 Live Media Monitor (qBittorrent + Bazarr Read-Only Poller & RAM Dedup)."""

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
        u = user if user is not None else os.environ.get("QBIT_USER", "admin")
        p = password if password is not None else os.environ.get("QBIT_PASS", "")
        if p and p != "replace_with_qbit_password":
            data = urllib.parse.urlencode({"username": u, "password": p}).encode()
            opener.open(urllib.request.Request(f"{base}/api/v2/auth/login", data=data), timeout=timeout)
        with opener.open(urllib.request.Request(f"{base}/api/v2/torrents/info"), timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
        return None


def fetch_bazarr_wanted_count(bazarr_url: str | None = None, api_key: str | None = None, timeout: int = 4) -> int | None:
    base = (bazarr_url or os.environ.get("BAZARR_URL", "")).rstrip("/")
    key = api_key if api_key is not None else os.environ.get("BAZARR_API_KEY", "")
    if not base or not key or key == "replace_with_bazarr_key":
        return None
    total = 0
    try:
        for ep in ("movies/wanted", "episodes/wanted"):
            req = urllib.request.Request(f"{base}/api/{ep}?length=1", headers={"X-API-KEY": key})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                total += int(json.loads(resp.read().decode("utf-8")).get("total", 0))
        return total
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError):
        return None


class LiveMediaMonitor:
    def __init__(
        self, state_file: pathlib.Path = DEFAULT_MEDIA_STATE, thermal_state_file: pathlib.Path = DEFAULT_THERMAL_FLAG,
        stall_threshold_sec: int | None = None, qbit_fetcher: Callable[[], list[dict[str, Any]] | None] = fetch_qbit_torrents,
        bazarr_fetcher: Callable[[], int | None] = fetch_bazarr_wanted_count,
    ) -> None:
        self.state_file, self.thermal_state_file = state_file, thermal_state_file
        env_thr = int(os.environ.get("MEDIA_STALL_THRESHOLD_SEC", "1200"))
        self.stall_threshold_sec = stall_threshold_sec if stall_threshold_sec is not None else env_thr
        self.qbit_fetcher, self.bazarr_fetcher = qbit_fetcher, bazarr_fetcher

    def _load_state(self) -> dict[str, Any]:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"initialized": False, "active_meta": {}, "done_notified": [], "stalled_since": {}, "stalled_notified": [], "had_queue": False}

    def _sub_suffix(self) -> str:
        wanted = self.bazarr_fetcher()
        return f" | Bazarr Sub Việt chờ: {wanted}" if wanted is not None else ""

    def poll_and_notify(self, send_tg: Callable[[str], Any] | None = None, now_ts: int | None = None) -> list[str]:
        torrents = self.qbit_fetcher()
        if torrents is None:
            return []
        now = int(now_ts if now_ts is not None else time.time())
        st = self._load_state()
        thermal = is_thermal_paused(self.thermal_state_file)
        alerts: list[str] = []
        active_meta: dict[str, dict[str, Any]] = dict(st.get("active_meta") or {})
        for old_h in st.get("active_hashes", []):
            active_meta.setdefault(old_h, {"name": old_h, "progress": 0.0})
        done_notified, stalled_notified = set(st.get("done_notified", [])), set(st.get("stalled_notified", []))
        stalled_since: dict[str, int] = dict(st.get("stalled_since", {}))
        seen_hashes: set[str] = set()
        incomplete_count = 0

        for t in torrents:
            h, name = str(t.get("hash") or t.get("name") or ""), str(t.get("name") or "")
            seen_hashes.add(h)
            state, prog, speed = str(t.get("state") or "").lower(), float(t.get("progress") or 0.0), int(t.get("dlspeed") or 0)
            prev_prog = float((active_meta.get(h) or {}).get("progress", 0.0))
            if not (prog >= 1.0 or state in DONE_STATES):
                incomplete_count += 1
                active_meta[h] = {"name": name, "progress": prog}
                prog_delta = prog - prev_prog
                is_stuck = state in STALLED_STATES or (state in ACTIVE_DL_STATES and speed < SLOW_SPEED_BYTES and prog_delta < 0.01)
                if not thermal and is_stuck:
                    first_ts = stalled_since.setdefault(h, now)
                    if (now - first_ts) >= self.stall_threshold_sec and h not in stalled_notified:
                        alerts.append(f"⚠️ [MEDIA STALLED] '{name}' bị kẹt ({state}, {prog*100:.0f}%) quá {(now - first_ts)//60} phút. Gợi ý: Kiểm tra seed hoặc tải qua Direct Fetch (Fshare/Drive/TeraBox).")
                        stalled_notified.add(h)
                elif not thermal and (speed >= RECOVERY_SPEED_BYTES or prog_delta >= 0.01):
                    stalled_since.pop(h, None)
            else:
                stalled_since.pop(h, None)
                active_meta.pop(h, None)
                if st.get("initialized") and h not in done_notified:
                    alerts.append(f"🎬 [MEDIA DONE] '{name}' đã tải xong 100%!{self._sub_suffix()}")
                    done_notified.add(h)
                elif not st.get("initialized"):
                    done_notified.add(h)

        for vanish_h in [vh for vh in active_meta if vh not in seen_hashes]:
            meta = active_meta.pop(vanish_h)
            stalled_since.pop(vanish_h, None)
            if st.get("initialized") and float(meta.get("progress", 0.0)) >= 0.85 and vanish_h not in done_notified:
                alerts.append(f"🎬 [MEDIA DONE] '{meta.get('name', vanish_h)}' đã tải xong & import 100%!{self._sub_suffix()}")
                done_notified.add(vanish_h)

        if st.get("initialized") and st.get("had_queue") and incomplete_count == 0:
            alerts.append("🎉 [MEDIA QUEUE CLEAR] Toàn bộ hàng đợi tải phim trên qBittorrent đã hoàn tất 100%!")

        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps({
            "initialized": True, "active_meta": active_meta, "done_notified": sorted(done_notified)[-300:],
            "stalled_since": stalled_since, "stalled_notified": sorted(stalled_notified)[-200:], "had_queue": incomplete_count > 0,
        }), encoding="utf-8")
        for msg in (alerts if send_tg else []):
            send_tg(msg)  # type: ignore[misc]
        return alerts

    def format_queue_status_line(self) -> str:
        torrents = self.qbit_fetcher()
        if torrents is None:
            return "qBittorrent: offline/chưa kết nối"
        inc = [t for t in torrents if float(t.get("progress") or 0.0) < 1.0 and str(t.get("state") or "").lower() not in DONE_STATES]
        if not inc:
            return f"Idle (0 đang tải / {len(torrents)} hoàn tất)"
        act = [t for t in inc if str(t.get("state") or "").lower() in ACTIVE_DL_STATES]
        stl = [t for t in inc if str(t.get("state") or "").lower() in STALLED_STATES]
        q_cnt = len(inc) - len(act) - len(stl)
        if act:
            top = act[0]
            return f"Đang tải '{str(top.get('name'))[:38]}' ({float(top.get('progress') or 0)*100:.0f}% @ {float(top.get('dlspeed') or 0)/(1024*1024):.1f} MB/s) | Chờ: {q_cnt} | Kẹt: {len(stl)}"
        return f"Đang tải: 0 | Chờ: {q_cnt} | Kẹt: {len(stl)}"
