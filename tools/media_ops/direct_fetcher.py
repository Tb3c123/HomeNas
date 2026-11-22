"""AI-Controlled Direct Media Fetcher (Option C: Direct-CDN + Google Drive + Web Cookie)."""

import json
import os
import pathlib
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
from typing import Any, Callable

from tools.media_ops.disk_balancer import select_target_disk
from tools.media_ops.media_watcher import is_thermal_paused
from tools.nas_ops.policy import DEFAULT_THERMAL_FLAG

ALLOWED_EXTENSIONS = {".mkv", ".mp4", ".avi", ".mov", ".m2ts", ".iso", ".srt", ".ass", ".ssa", ".sub", ".vtt"}
BLOCKED_EXTENSIONS = {".exe", ".msi", ".bat", ".cmd", ".sh", ".py", ".apk", ".scr", ".vbs", ".js", ".php", ".dll"}


def sanitize_media_name(name: str, default_ext: str = ".mkv") -> str:
    cleaned = re.sub(r'[\\/*?:"<>|]+', " ", name).strip()
    cleaned = re.sub(r"\.\.+", ".", cleaned).strip(". ") or "Media_Download"
    ext = pathlib.Path(cleaned).suffix.lower()
    if ext in BLOCKED_EXTENSIONS:
        raise ValueError(f"Blocked dangerous file extension '{ext}'.")
    return cleaned if ext in ALLOWED_EXTENSIONS else f"{cleaned}{default_ext}"


def classify_and_validate_url(url: str) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(url.strip())
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("Only valid HTTPS media URLs are permitted.")
    host = parsed.netloc.lower()
    path = urllib.parse.unquote(parsed.path)
    ext = pathlib.Path(path).suffix.lower()
    if ext in BLOCKED_EXTENSIONS:
        raise ValueError(f"Blocked dangerous file extension '{ext}' in URL.")

    if re.match(r"^download\d*\.fshare\.vn$", host):
        return {"provider": "fshare_cdn", "direct_url": url, "host": host}
    if host in ("fshare.vn", "www.fshare.vn"):
        m = re.search(r"/file/([A-Za-z0-9]+)", path)
        if not m:
            raise ValueError("Invalid Fshare file URL (expected /file/<CODE>).")
        return {"provider": "fshare_page", "file_code": m.group(1), "host": host}
    if host in ("drive.google.com", "docs.google.com", "drive.usercontent.google.com"):
        m = re.search(r"/d/([A-Za-z0-9_-]+)", path) or re.search(r"(?:^|&)id=([A-Za-z0-9_-]+)", parsed.query)
        if not m:
            raise ValueError("Could not extract Google Drive file ID from URL.")
        fid = m.group(1)
        return {"provider": "gdrive", "file_id": fid, "direct_url": f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t", "host": host}
    if any(host.endswith(d) for d in ("terabox.com", "1024terabox.com", "teraboxapp.com", "4funbox.com")):
        if "/s/" in path:
            return {"provider": "terabox_page", "surl": path.split("/s/", 1)[1].split("/")[0], "host": host}
        return {"provider": "terabox_cdn", "direct_url": url, "host": host}
    if ext in ALLOWED_EXTENSIONS:
        return {"provider": "direct_cdn", "direct_url": url, "host": host}
    raise ValueError(f"Unsupported host '{host}'. Use Fshare, Google Drive, TeraBox, or direct media CDN link.")


def resolve_fshare_cookie_url(page_url: str, cookie_str: str) -> str:
    headers = {"Cookie": cookie_str, "User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}
    with urllib.request.urlopen(urllib.request.Request(page_url, headers=headers), timeout=10) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    m_csrf = re.search(r'name="_csrf-app"\s+value="([^"]+)"', html)
    m_code = re.search(r"/file/([A-Za-z0-9]+)", page_url)
    if not m_csrf or not m_code:
        raise RuntimeError("Fshare cookie expired. Paste browser download*.fshare.vn link.")
    payload = urllib.parse.urlencode({"_csrf-app": m_csrf.group(1), "linkcode": m_code.group(1), "withFcode5": 0, "fcode": ""}).encode()
    with urllib.request.urlopen(urllib.request.Request("https://www.fshare.vn/download/get", data=payload, headers=headers), timeout=10) as r2:
        loc = json.loads(r2.read().decode("utf-8")).get("location")
    if not loc:
        raise RuntimeError("Fshare did not return direct location. Paste browser download*.fshare.vn link.")
    return str(loc)


def plan_or_execute_direct_fetch(
    url: str, title: str, media_type: str = "movie", category: str = "Cinema",
    season: int = 1, filename: str | None = None,
    disk1_root: pathlib.Path = pathlib.Path("/mnt/disk1"),
    disk2_root: pathlib.Path = pathlib.Path("/mnt/disk2"),
    thermal_state_file: pathlib.Path = DEFAULT_THERMAL_FLAG,
    free_space_override: dict[str, int] | None = None,
    execute: bool = False, runner: Callable[[list[str]], int] | None = None,
) -> dict[str, Any]:
    info = classify_and_validate_url(url)
    safe_title = re.sub(r'[\\/*?:"<>|]+', " ", title).strip()
    safe_file = sanitize_media_name(filename or safe_title)
    if is_thermal_paused(thermal_state_file):
        return {"status": "THERMAL_WAIT", "provider": info["provider"], "reason": "HDD thermal protection active."}

    route = select_target_disk(
        media_type=media_type, category=category, series_title=safe_title if media_type == "tv" else None,
        disk1_root=disk1_root, disk2_root=disk2_root, free_space_override=free_space_override,
    )
    base_dir = pathlib.Path(route["host_target_dir"]) / safe_title
    if media_type == "tv":
        base_dir = base_dir / f"Season {int(season):02d}"
    dest_file = base_dir / safe_file

    direct_url = info.get("direct_url")
    if info["provider"] == "fshare_page":
        cookie = os.environ.get("FSHARE_COOKIE", "").strip()
        if not cookie:
            return {"status": "NEEDS_BROWSER_DIRECT_LINK", "provider": "fshare_page", "target_disk": route["disk"], "dest_path": str(dest_file), "hint": "Click Download in browser, pause, and paste download*.fshare.vn link."}
        direct_url = resolve_fshare_cookie_url(url, cookie)
    elif info["provider"] == "terabox_page" and not os.environ.get("TERABOX_COOKIE", "").strip():
        return {"status": "NEEDS_BROWSER_DIRECT_LINK", "provider": "terabox_page", "target_disk": route["disk"], "dest_path": str(dest_file), "hint": "Click Download in browser, pause, and paste direct TeraBox CDN link."}

    plan = {"status": "PLANNED", "provider": info["provider"], "target_disk": route["disk"], "dest_path": str(dest_file), "direct_url": direct_url}
    if not execute or not direct_url:
        return plan

    base_dir.mkdir(parents=True, exist_ok=True)
    part = dest_file.with_suffix(dest_file.suffix + ".part")
    cmd = ["aria2c", "-x", "4", "-s", "4", "--continue=true", "-d", str(base_dir), "-o", part.name, direct_url] if shutil.which("aria2c") else ["curl", "-L", "-f", "-C", "-", "--retry", "3", "-o", str(part), direct_url]
    rc = runner(cmd) if runner else subprocess.run(cmd, check=False).returncode
    if rc != 0:
        return {**plan, "status": "FAILED", "returncode": rc}
    if part.exists():
        part.replace(dest_file)
    return {**plan, "status": "DOWNLOADED"}
