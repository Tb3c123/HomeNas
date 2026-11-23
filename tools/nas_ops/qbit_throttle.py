"""Stateless qBittorrent Thermal Soft-Throttle Reconciler (Alternative Speed Mode & Global Limit)."""

import http.cookiejar
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable

ALT_DL_LIMIT_BPS = 2621440  # 2.56 MB/s (2560 KiB/s)
ALT_UL_LIMIT_BPS = 524288   # 512 KB/s


class QbitThrottleController:
    def __init__(
        self,
        qbit_url: str | None = None,
        user: str | None = None,
        password: str | None = None,
        timeout: int = 4,
        mode_getter: Callable[[], str | None] | None = None,
        mode_setter: Callable[[str], bool] | None = None,
        limit_clearer: Callable[[], bool] | None = None,
    ) -> None:
        self.base = (qbit_url if qbit_url is not None else os.environ.get("QBIT_URL", "")).rstrip("/")
        self.user = user if user is not None else os.environ.get("QBIT_USER", "admin")
        self.password = password if password is not None else os.environ.get("QBIT_PASS", "")
        self.timeout = timeout
        self._mode_getter = mode_getter
        self._mode_setter = mode_setter
        self._limit_clearer = limit_clearer

    def _build_opener(self) -> urllib.request.OpenerDirector | None:
        if not self.base:
            return None
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        if self.password and self.password != "replace_with_qbit_password":
            data = urllib.parse.urlencode({"username": self.user, "password": self.password}).encode()
            opener.open(urllib.request.Request(f"{self.base}/api/v2/auth/login", data=data), timeout=self.timeout)
        return opener

    def get_speed_limits_mode(self) -> str | None:
        if self._mode_getter is not None:
            return self._mode_getter()
        try:
            opener = self._build_opener()
            if opener is None:
                return None
            with opener.open(urllib.request.Request(f"{self.base}/api/v2/transfer/speedLimitsMode"), timeout=self.timeout) as r:
                return r.read().decode("utf-8").strip()
        except (urllib.error.URLError, TimeoutError, OSError):
            return None

    def set_alt_speed_mode(self, target_mode: str) -> bool:
        if self._mode_setter is not None:
            return self._mode_setter(target_mode)
        try:
            opener = self._build_opener()
            if opener is None:
                return False
            if target_mode == "1":
                prefs = json.dumps({"alt_dl_limit": ALT_DL_LIMIT_BPS, "alt_up_limit": ALT_UL_LIMIT_BPS})
                body = urllib.parse.urlencode({"json": prefs}).encode()
                opener.open(urllib.request.Request(f"{self.base}/api/v2/app/setPreferences", data=body), timeout=self.timeout)
            with opener.open(urllib.request.Request(f"{self.base}/api/v2/transfer/toggleSpeedLimitsMode", data=b""), timeout=self.timeout) as r:
                return r.status == 200
        except (urllib.error.URLError, TimeoutError, OSError):
            return False

    def clear_global_download_limit(self) -> bool:
        if self._limit_clearer is not None:
            return self._limit_clearer()
        try:
            opener = self._build_opener()
            if opener is None:
                return False
            with opener.open(urllib.request.Request(f"{self.base}/api/v2/transfer/downloadLimit"), timeout=self.timeout) as r:
                cur = int(r.read().decode("utf-8").strip() or "0")
            if cur > 0:
                body = urllib.parse.urlencode({"limit": 0}).encode()
                with opener.open(urllib.request.Request(f"{self.base}/api/v2/transfer/setDownloadLimit", data=body), timeout=self.timeout) as r2:
                    return r2.status == 200
            return True
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            return False

    def reconcile(self, should_throttle: bool) -> dict[str, Any]:
        """Statelessly reconcile qBittorrent live mode against desired thermal state."""
        live_mode = self.get_speed_limits_mode()
        if live_mode is None:
            return {"changed": False, "live_mode": None, "throttled": should_throttle}

        desired = "1" if should_throttle else "0"
        changed = False
        if live_mode != desired:
            changed = self.set_alt_speed_mode(desired)
        if not should_throttle:
            self.clear_global_download_limit()
        return {"changed": changed, "live_mode": desired if changed else live_mode, "throttled": should_throttle}
