"""0-Token Telegram Bot Command Listener (Strict Chat ID Whitelist & Clean 4-Command Menu)."""

import json
import os
import pathlib
import time
import urllib.error
import urllib.request
from typing import Any, Callable

from shared.tools.kanboard_client.service import KanboardService
from tools.nas_ops.sensors import collect_snapshot

DEFAULT_STATE_DIR = pathlib.Path("/mnt/disk1/Workspace/HomeNas/.state")

BOT_COMMANDS = [
    {"command": "status", "description": "Xem nhiệt độ CPU/HDD Acasis & trạng thái Remote Control"},
    {"command": "reconnect", "description": "Khởi động lại agy remote-control (home-nas)"},
    {"command": "digest", "description": "Xem thẻ Kanboard mới cập nhật / chờ duyệt"},
    {"command": "help", "description": "Hiển thị 4 lệnh đang hỗ trợ"},
]


class TelegramCommandHandler:
    def __init__(
        self,
        bot_token: str | None = None,
        allowed_chat_id: str | None = None,
        state_dir: pathlib.Path = DEFAULT_STATE_DIR,
        kb_service: KanboardService | None = None,
        snapshot_fn: Callable[[], dict[str, Any]] = collect_snapshot,
        api_caller: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
    ) -> None:
        self.bot_token = bot_token if bot_token is not None else os.environ.get("TELEGRAM_BOT_TOKEN", "")
        self.allowed_chat_id = str(allowed_chat_id or os.environ.get("TELEGRAM_CHAT_ID", "")).strip()
        self.state_dir = state_dir
        self.kb = kb_service or KanboardService()
        self.snapshot_fn = snapshot_fn
        self._api_caller = api_caller or self._call_telegram_api
        self._offset = 0
        self._last_status_mtime = 0.0

    def _call_telegram_api(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.bot_token:
            return {"ok": False}
        url = f"https://api.telegram.org/bot{self.bot_token}/{method}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
            return {"ok": False}

    def sync_bot_menu(self) -> bool:
        self._api_caller("deleteMyCommands", {})
        res = self._api_caller("setMyCommands", {"commands": BOT_COMMANDS})
        return bool(res.get("ok"))

    def handle_message(self, chat_id: int | str, text: str) -> str | None:
        if not self.allowed_chat_id or str(chat_id).strip() != self.allowed_chat_id:
            return None
        cmd = text.strip().split()[0].split("@")[0].lower() if text.strip() else ""
        if cmd == "/status":
            return self._build_status_text()
        if cmd == "/reconnect":
            self.state_dir.mkdir(parents=True, exist_ok=True)
            flag = self.state_dir / "reconnect_remote.flag"
            flag.write_text(str(int(time.time())), encoding="utf-8")
            return "🔄 Đã gửi yêu cầu khởi động lại `agy remote-control start --name home-nas`. Chờ 5–10 giây..."
        if cmd == "/digest":
            try:
                return f"📋 Kanboard Unread Digest:\n{self.kb.unread_digest()}"
            except Exception as exc:
                return f"⚠️ Không đọc được Kanboard: {exc}"
        if cmd == "/help":
            lines = ["🤖 HomeNas Bot — 4 lệnh hỗ trợ:"]
            lines.extend(f"/{c['command']} — {c['description']}" for c in BOT_COMMANDS)
            return "\n".join(lines)
        return "ℹ️ Lệnh không hỗ trợ. Gõ /help để xem đúng 4 lệnh hiện có."

    def _build_status_text(self) -> str:
        snap = self.snapshot_fn()
        hdds = snap.get("hdds", {})
        d1 = hdds.get("disk1", {})
        d2 = hdds.get("disk2", {})
        d1_s = f"{d1['temp_c']}°C" if d1.get("temp_c") is not None else d1.get("status", "unknown")
        d2_s = f"{d2['temp_c']}°C" if d2.get("temp_c") is not None else d2.get("status", "unknown")
        rc_file = self.state_dir / "remote_status.txt"
        rc_line = rc_file.read_text(encoding="utf-8").strip().splitlines()[-1] if rc_file.exists() and rc_file.read_text(encoding="utf-8").strip() else "Chưa bật remote_keeper.sh"
        return (
            f"🖥️ Morefine N6 Status:\n"
            f"- CPU N200: {snap.get('cpu_temp_c')}°C | Load5: {snap.get('load5')} | RAM: {snap.get('ram_pct')}%\n"
            f"- HDD Acasis: disk1={d1_s} | disk2={d2_s}\n"
            f"- Remote Control: {rc_line[:160]}"
        )

    def check_remote_status_update(self) -> str | None:
        rc_file = self.state_dir / "remote_status.txt"
        if not rc_file.exists():
            return None
        mtime = rc_file.stat().st_mtime
        if self._last_status_mtime == 0.0:
            self._last_status_mtime = mtime
            return None
        if mtime > self._last_status_mtime:
            self._last_status_mtime = mtime
            text = rc_file.read_text(encoding="utf-8").strip()
            if text:
                return f"🔗 [Remote Control Update]\n{text[:300]}"
        return None

    def poll_once(self) -> None:
        res = self._api_caller("getUpdates", {"offset": self._offset, "timeout": 15, "allowed_updates": ["message"]})
        for upd in res.get("result", []):
            self._offset = max(self._offset, int(upd.get("update_id", 0)) + 1)
            msg = upd.get("message") or {}
            chat_id = (msg.get("chat") or {}).get("id")
            text = str(msg.get("text") or "")
            if chat_id is not None and text:
                reply = self.handle_message(chat_id, text)
                if reply:
                    self._api_caller("sendMessage", {"chat_id": self.allowed_chat_id, "text": reply})
        rc_update = self.check_remote_status_update()
        if rc_update and self.allowed_chat_id:
            self._api_caller("sendMessage", {"chat_id": self.allowed_chat_id, "text": rc_update})

    def run_forever(self) -> None:
        self.sync_bot_menu()
        while True:
            try:
                self.poll_once()
            except Exception:
                time.sleep(5)
            time.sleep(1)
