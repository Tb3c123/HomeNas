"""Emergency Container Pause/Stop Executor with Hard Protected-Container Whitelist."""

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
