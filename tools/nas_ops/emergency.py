"""Emergency Container Pause/Unpause & Stateless Paused-Container Reconciler."""

import json
import os
import urllib.error
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
SOFT_THROTTLE_BPS = 2621440  # 2.56 MB/s


class EmergencyExecutor:
    def __init__(
        self,
        docker_host: str | None = None,
        stoppable: list[str] | None = None,
        action_runner: Callable[[str, str], bool] | None = None,
        paused_checker: Callable[[str], bool] | None = None,
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
        self.paused_checker = paused_checker or self._docker_is_paused

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

    def _docker_is_paused(self, container: str) -> bool:
        url = f"{self.http_base}/containers/{container}/json"
        try:
            with urllib.request.urlopen(urllib.request.Request(url), timeout=4) as resp:
                info = json.loads(resp.read().decode("utf-8"))
                return bool((info.get("State") or {}).get("Paused", False))
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
            return False

    def trigger_emergency_mitigation(self, action: str = "pause") -> list[str]:
        mitigated: list[str] = []
        for container in self.stoppable:
            if container in HARD_PROTECTED:
                continue
            if self.action_runner(container, action):
                mitigated.append(container)
        return mitigated

    def reconcile_paused_containers(self) -> list[str]:
        """Unpause any stoppable container left Paused after a watchdog restart when NORMAL."""
        unpaused: list[str] = []
        for container in self.stoppable:
            if container in HARD_PROTECTED:
                continue
            if self.paused_checker(container) and self.action_runner(container, "unpause"):
                unpaused.append(container)
        return unpaused
