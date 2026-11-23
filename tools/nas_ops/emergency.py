"""Emergency Container Pause/Unpause & qBittorrent Thermal Soft-Throttle Executor."""

import http.cookiejar
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Callable

HARD_PROTECTED = {
    "adguard-home",
    "portainer",
    "casaos",
    "kanboard",
    "homenas-watchdog",
    "antigravity-cli",
    "docker-proxy",
}
DEFAULT_STOPPABLE = ["qbittorrent", "jellyfin", "radarr", "sonarr", "bazarr"]
SOFT_THROTTLE_BPS = 2621440  # 2.5 MB/s


class EmergencyExecutor:
    def __init__(
        self,
        docker_host: str | None = None,
        stoppable: list[str] | None = None,
        action_runner: Callable[[str, str], bool] | None = None,
    ) -> None:
        raw_host = docker_host or os.environ.get("DOCKER_HOST", "http://docker-proxy:2375")
        self.http_base = raw_host.replace("tcp://", "http://").rstrip("/")
        if stoppable is not None:
            candidates = stoppable
        else:
            env_list = os.environ.get("STOPPABLE_CONTAINERS", ",".join(DEFAULT_STOPPABLE))
            candidates = [c.strip() for c in env_list.split(",") if c.strip()]
        self.stoppable = [c for c in candidates if c not in HARD_PROTECTED]
        self.action_runner = action_runner or self._docker_api_action

    def _docker_api_action(self, container: str, action: str) -> bool:
        if container in HARD_PROTECTED:
            raise PermissionError(f"Container '{container}' is strictly protected!")
        url = f"{self.http_base}/containers/{container}/{action}"
        req = urllib.request.Request(url, data=b"", method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status in (200, 204, 304)
        except (urllib.error.URLError, TimeoutError, OSError):
            return False

    def trigger_emergency_mitigation(self, action: str = "pause") -> list[str]:
        mitigated: list[str] = []
        for container in self.stoppable:
            if container in HARD_PROTECTED:
                continue
            if self.action_runner(container, action):
                mitigated.append(container)
        return mitigated

    def set_qbit_download_limit(self, limit_bps: int, qbit_url: str | None = None) -> bool:
        base = (qbit_url or os.environ.get("QBIT_URL", "")).rstrip("/")
        if not base:
            return False
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        try:
            u = os.environ.get("QBIT_USER", "admin")
            p = os.environ.get("QBIT_PASS", "")
            if p and p != "replace_with_qbit_password":
                login_data = urllib.parse.urlencode({"username": u, "password": p}).encode()
                opener.open(urllib.request.Request(f"{base}/api/v2/auth/login", data=login_data), timeout=4)
            body = urllib.parse.urlencode({"limit": int(limit_bps)}).encode()
            with opener.open(urllib.request.Request(f"{base}/api/v2/transfer/setDownloadLimit", data=body), timeout=4) as r:
                return r.status == 200
        except (urllib.error.URLError, TimeoutError, OSError):
            return False
