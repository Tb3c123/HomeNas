"""0-Token 24/7 Live Media Monitor (qBittorrent + Bazarr Read-Only Poller & RAM Dedup)."""

import http.cookiejar
import json
import os
import pathlib
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable

from tools.media_ops.media_watcher import is_thermal_paused
from tools.nas_ops.policy import DEFAULT_THERMAL_FLAG

DEFAULT_MEDIA_STATE = pathlib.Path("/tmp/homenas_media_monitor.json")
DONE_STATES = {"uploading", "stalledup", "pausedup", "queuedup", "checkingup", "forcedup"}
ACTIVE_DL_STATES = {"downloading", "forceddl", "metadl", "allocating", "checkingdl"}
STALLED_STATES = {"stalleddl", "error", "missingfiles"}


def fetch_qbit_torrents(
    qbit_url: str | None = None, user: str | None = None, password: str | None = None, timeout: int = 4,
) -> list[dict[str, Any]] | None:
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
        self,
        state_file: pathlib.Path = DEFAULT_MEDIA_STATE,
        thermal_state_file: pathlib.Path = DEFAULT_THERMAL_FLAG,
        stall_threshold_sec: int = 2700,
        qbit_fetcher: Callable[[], list[dict[str, Any]] | None] = fetch_qbit_torrents,
        bazarr_fetcher: Callable[[], int | None] = fetch_bazarr_wanted_count,
    ) -> None:
        self.state_file = state_file
        self.thermal_state_file = thermal_state_file
        self.stall_threshold_sec = stall_threshold_sec
        self.qbit_fetcher = qbit_fetcher
        self.bazarr_fetcher = bazarr_fetcher

    def _load_state(self) -> dict[str, Any]:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"initialized": False, "active_hashes": [], "done_notified": [], "stalled_since": {}, "stalled_notified": [], "had_queue": False}

    def poll_and_notify(self, send_tg: Callable[[str], Any] | None = None, now_ts: int | None = None) -> list[str]:
        torrents = self.qbit_fetcher()
        if torrents is None:
            return []
        now = int(now_ts if now_ts is not None else time.time())
        st = self._load_state()
        thermal = is_thermal_paused(self.thermal_state_file)
        alerts: list[str] = []
        active_set, done_notified = set(st.get("active_hashes", [])), set(st.get("done_notified", []))
        stalled_since, stalled_notified = dict(st.get("stalled_since", {})), set(st.get("stalled_notified", []))
        incomplete_count = 0

        for t in torrents:
            h, name = str(t.get("hash") or t.get("name") or ""), str(t.get("name") or "")
            state, prog = str(t.get("state") or "").lower(), float(t.get("progress") or 0.0)
            if not (prog >= 1.0 or state in DONE_STATES):
                incomplete_count += 1
                active_set.add(h)
                is_stuck = state in STALLED_STATES or (state in ACTIVE_DL_STATES and int(t.get("num_seeds", 1)) == 0 and int(t.get("dlspeed", 0)) == 0)
                if not thermal and is_stuck:
                    first_ts = stalled_since.setdefault(h, now)
                    if (now - first_ts) >= self.stall_threshold_sec and h not in stalled_notified:
                        alerts.append(f"⚠️ [MEDIA STALLED] '{name}' bị kẹt ({state}, {prog*100:.0f}%) quá {(now - first_ts)//60} phút. Gợi ý: Kiểm tra seed hoặc tải qua Direct Fetch (Fshare/Drive/TeraBox).")
                        stalled_notified.add(h)
                else:
                    stalled_since.pop(h, None)
            else:
                stalled_since.pop(h, None)
                if st.get("initialized") and h in active_set and h not in done_notified:
                    wanted = self.bazarr_fetcher()
                    sub_note = f" | Bazarr Sub Việt chờ: {wanted}" if wanted is not None else ""
                    alerts.append(f"🎬 [MEDIA DONE] '{name}' đã tải xong 100%!{sub_note}")
                    done_notified.add(h)
                    active_set.discard(h)
                elif not st.get("initialized"):
                    done_notified.add(h)

        if st.get("initialized") and st.get("had_queue") and incomplete_count == 0:
            alerts.append("🎉 [MEDIA QUEUE CLEAR] Toàn bộ hàng đợi tải phim trên qBittorrent đã hoàn tất 100%!")

        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps({
            "initialized": True, "active_hashes": sorted(active_set), "done_notified": sorted(done_notified)[-300:],
            "stalled_since": stalled_since, "stalled_notified": sorted(stalled_notified)[-200:], "had_queue": incomplete_count > 0,
        }), encoding="utf-8")
        if send_tg:
            for msg in alerts:
                send_tg(msg)
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
