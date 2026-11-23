"""0-Token Dead Torrent Healer (10-15m Periodic Reannounce & Radarr/Sonarr Auto-Blocklist Replacement)."""

import http.cookiejar, json, os, pathlib, time, urllib.error, urllib.parse, urllib.request
from typing import Any, Callable
from tools.media_ops.arr_monitor import fetch_qbit_torrents
from tools.media_ops.media_watcher import is_thermal_paused
from tools.nas_ops.policy import DEFAULT_THERMAL_FLAG

DEFAULT_HEALER_STATE = pathlib.Path("/tmp/homenas_dead_healer.json")
CHECKED_STATES = {"downloading", "stalleddl", "metadl", "missingfiles"}
PUBLIC_TRACKERS = "\n".join([
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://open.stealth.si:80/announce",
    "udp://tracker.torrent.eu.org:451/announce",
    "udp://exodus.desync.com:6969/announce",
])


def qbit_reannounce_and_boost(torrent_hash: str, qbit_url: str | None = None, timeout: int = 4) -> bool:
    base = (qbit_url or os.environ.get("QBIT_URL", "")).rstrip("/")
    if not base or not torrent_hash:
        return False
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    try:
        u, p = os.environ.get("QBIT_USER", "admin"), os.environ.get("QBIT_PASS", "")
        if p and p != "replace_with_qbit_password":
            opener.open(urllib.request.Request(f"{base}/api/v2/auth/login", data=urllib.parse.urlencode({"username": u, "password": p}).encode()), timeout=timeout)
        tr_data = urllib.parse.urlencode({"hash": torrent_hash, "urls": PUBLIC_TRACKERS}).encode()
        opener.open(urllib.request.Request(f"{base}/api/v2/torrents/addTrackers", data=tr_data), timeout=timeout)
        ra_data = urllib.parse.urlencode({"hashes": torrent_hash}).encode()
        with opener.open(urllib.request.Request(f"{base}/api/v2/torrents/reannounce", data=ra_data), timeout=timeout) as r:
            return r.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def arr_blocklist_and_replace(torrent_hash: str, timeout: int = 6) -> str | None:
    target = torrent_hash.strip().upper()
    services = [
        ("Radarr", os.environ.get("RADARR_URL", ""), os.environ.get("RADARR_API_KEY", "")),
        ("Sonarr", os.environ.get("SONARR_URL", ""), os.environ.get("SONARR_API_KEY", "")),
    ]
    for label, raw_url, key in services:
        base = raw_url.rstrip("/")
        if not base or not key or key.startswith("replace_with_"):
            continue
        headers = {"X-Api-Key": key}
        try:
            req = urllib.request.Request(f"{base}/api/v3/queue?page=1&pageSize=200", headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                records = json.loads(resp.read().decode("utf-8")).get("records", [])
            for item in records:
                if str(item.get("downloadId") or "").strip().upper() == target and item.get("id") is not None:
                    qid = item["id"]
                    del_url = f"{base}/api/v3/queue/{qid}?removeFromClient=true&blocklist=true&skipRedownload=false"
                    del_req = urllib.request.Request(del_url, headers=headers, method="DELETE")
                    with urllib.request.urlopen(del_req, timeout=timeout) as dresp:
                        if dresp.status in (200, 202, 204):
                            return label
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
            continue
    return None


class DeadTorrentHealer:
    def __init__(
        self, state_file: pathlib.Path = DEFAULT_HEALER_STATE, thermal_state_file: pathlib.Path = DEFAULT_THERMAL_FLAG,
        min_speed_kbps: float | None = None, dead_sec: int = 1200, deep_warn_sec: int = 7200,
        qbit_fetcher: Callable[[], list[dict[str, Any]] | None] = fetch_qbit_torrents,
        reannouncer: Callable[[str], bool] = qbit_reannounce_and_boost,
        arr_replacer: Callable[[str], str | None] = arr_blocklist_and_replace,
    ) -> None:
        self.state_file, self.thermal_state_file = state_file, thermal_state_file
        env_spd = float(os.environ.get("MIN_DL_SPEED_KBPS", "500"))
        self.min_speed_bps = (min_speed_kbps if min_speed_kbps is not None else env_spd) * 1024.0
        self.dead_sec, self.deep_warn_sec = dead_sec, deep_warn_sec
        self.qbit_fetcher, self.reannouncer, self.arr_replacer = qbit_fetcher, reannouncer, arr_replacer

    def _load(self) -> dict[str, Any]:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"tracked": {}}

    def _save(self, st: dict[str, Any]) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(st), encoding="utf-8")

    def run_heal_cycle(self, send_tg: Callable[[str], Any] | None = None, now_ts: int | None = None) -> list[str]:
        if is_thermal_paused(self.thermal_state_file):
            return []
        torrents = self.qbit_fetcher()
        if torrents is None:
            return []
        now = int(now_ts if now_ts is not None else time.time())
        st = self._load()
        tracked: dict[str, dict[str, Any]] = dict(st.get("tracked") or {})
        active_hashes: set[str] = set()
        messages: list[str] = []

        for t in torrents:
            state = str(t.get("state") or "").lower()
            if state not in CHECKED_STATES:
                continue  # Ignore queuedDL, pausedDL, completed/seeding
            h = str(t.get("hash") or t.get("name") or "")
            name = str(t.get("name") or h)
            prog = float(t.get("progress") or 0.0)
            speed = float(t.get("dlspeed") or 0.0)
            seeds = int(t.get("num_seeds") or 0)
            total_seeds = max(seeds, int(t.get("num_complete") or seeds))
            active_hashes.add(h)

            is_slow_or_stalled = state in ("stalleddl", "missingfiles", "metadl") or speed < self.min_speed_bps
            if not is_slow_or_stalled:
                tracked.pop(h, None)
                continue

            entry = tracked.setdefault(h, {"since": now, "reannounced": False, "warned_2h": False, "replaced": False})
            elapsed = now - int(entry.get("since", now))

            # Protected Rule: >= 20% progress with > 5 total seeds -> NEVER auto-delete, only gentle warn after 2h
            if prog >= 0.20 and total_seeds > 5:
                if elapsed > self.deep_warn_sec and not entry.get("warned_2h"):
                    messages.append(f"⏳ [MEDIA SLOW >2H] '{name}' ({prog*100:.0f}%, {total_seeds} seeds) đang đứng im >2 tiếng. Hệ thống giữ nguyên không xóa.")
                    entry["warned_2h"] = True
                continue

            # Auto-Heal Rule: (< 5% progress AND 0 seeds for > 20m) OR missingFiles
            is_dead_candidate = state == "missingfiles" or (prog < 0.05 and seeds == 0 and elapsed > self.dead_sec)
            if is_dead_candidate and not entry.get("replaced"):
                if not entry.get("reannounced"):
                    self.reannouncer(h)
                    entry["reannounced"] = True
                else:
                    arr_name = self.arr_replacer(h)
                    entry["replaced"] = True
                    if arr_name:
                        messages.append(f"♻️ [MEDIA AUTO-REPLACE] Đã gỡ & blocklist torrent chết seed '{name}' ({prog*100:.1f}%, 0 seed) qua {arr_name} để tự tìm bản thay thế.")
                    else:
                        messages.append(f"⚠️ [MEDIA DEAD SEED] '{name}' ({prog*100:.1f}%, 0 seed) vẫn kẹt sau khi bơm tracker (không tìm thấy trên queue Radarr/Sonarr).")

        for old_h in [k for k in tracked if k not in active_hashes]:
            tracked.pop(old_h, None)

        self._save({"tracked": tracked})
        for m in (messages if send_tg else []):
            send_tg(m)  # type: ignore[misc]
        return messages
