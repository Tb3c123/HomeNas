"""Hermes Archive Store (ARCHIVE.jsonl) & Learning Toast Feed (.state/learning_feed.jsonl)."""

import json
import pathlib
import time

DEFAULT_ARCHIVE = pathlib.Path("memory/ARCHIVE.jsonl")
DEFAULT_FEED = pathlib.Path(".state/learning_feed.jsonl")


def record_archive(archive_path: pathlib.Path, action: str, target: str, evicted: list[str]) -> None:
    if not evicted:
        return
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": int(time.time()), "action": action, "target": target, "evicted": evicted}
    with archive_path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(entry, ensure_ascii=False) + "\n")


def record_learning_toast(feed_path: pathlib.Path, toast: str) -> None:
    feed_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": int(time.time()), "toast": toast}
    with feed_path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_recent_learning_toasts(feed_path: pathlib.Path = DEFAULT_FEED, limit: int = 3) -> list[str]:
    if not feed_path.exists():
        return []
    lines = [ln for ln in feed_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    toasts: list[str] = []
    for ln in lines[-limit:]:
        try:
            toasts.append(str(json.loads(ln).get("toast", "")))
        except json.JSONDecodeError:
            continue
    return [t for t in toasts if t]
