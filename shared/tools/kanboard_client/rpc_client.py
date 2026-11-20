"""Kanboard JSON-RPC 2.0 Client with 5s timeout and RAM offline fallback queue."""

import base64
import json
import os
import pathlib
import time
import urllib.error
import urllib.request
from typing import Any

DEFAULT_FALLBACK_PATH = pathlib.Path("/tmp/kb-fallback-queue.jsonl")


class KanboardRPCError(RuntimeError):
    """Raised when Kanboard JSON-RPC call fails."""


class KanboardClient:
    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        user: str | None = None,
        timeout: float = 5.0,
        fallback_path: pathlib.Path = DEFAULT_FALLBACK_PATH,
    ) -> None:
        self.url = url or os.environ.get("KANBOARD_URL", "http://kanboard/jsonrpc.php")
        self.user = user or os.environ.get("KANBOARD_API_USER", "jsonrpc")
        self.token = token or os.environ.get("KANBOARD_API_TOKEN", "")
        self.timeout = timeout
        self.fallback_path = fallback_path
        self._req_id = 0

    def _auth_header(self) -> str:
        raw = f"{self.user}:{self.token}".encode("utf-8")
        return "Basic " + base64.b64encode(raw).decode("ascii")

    def call(self, method: str, params: dict[str, Any] | None = None) -> Any:
        self._req_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self._req_id,
            "params": params or {},
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": self._auth_header(),
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise KanboardRPCError(f"Kanboard unreachable ({exc})") from exc

        if "error" in body and body["error"]:
            raise KanboardRPCError(f"RPC error: {body['error']}")
        return body.get("result")

    def queue_offline_action(self, method: str, params: dict[str, Any]) -> None:
        self.fallback_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {"ts": int(time.time()), "method": method, "params": params}
        with self.fallback_path.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def flush_offline_queue(self) -> int:
        if not self.fallback_path.exists():
            return 0
        lines = [ln for ln in self.fallback_path.read_text(encoding="utf-8").splitlines() if ln]
        if not lines:
            return 0
        remaining: list[str] = []
        flushed = 0
        for idx, line in enumerate(lines):
            item = json.loads(line)
            try:
                self.call(item["method"], item["params"])
                flushed += 1
            except KanboardRPCError:
                remaining = lines[idx:]
                break
        if remaining:
            self.fallback_path.write_text("\n".join(remaining) + "\n", encoding="utf-8")
        else:
            self.fallback_path.unlink(missing_ok=True)
        return flushed
