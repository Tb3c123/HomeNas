"""Zero-Noise Output Formatter and Idempotent Dedup Matcher for Kanboard Tasks."""

from typing import Any

IDLE_MESSAGE = "[ℹ️ IDLE] Không có thông báo/task mới."


def format_task_line(task: dict[str, Any]) -> str:
    task_id = task.get("id", "?")
    col = task.get("column_name") or task.get("column_id", "Unknown")
    swimlane = task.get("swimlane_name") or ""
    tags_raw = task.get("tags") or []
    if isinstance(tags_raw, dict):
        tags = list(tags_raw.values())
    elif isinstance(tags_raw, list):
        tags = [t.get("name", str(t)) if isinstance(t, dict) else str(t) for t in tags_raw]
    else:
        tags = []
    tag_str = f" [{','.join(tags)}]" if tags else ""
    swim_str = f" [{swimlane}]" if swimlane else ""
    title = str(task.get("title", "")).strip()
    return f"#{task_id} [{col}]{swim_str}{tag_str} {title}"


def format_task_list(tasks: list[dict[str, Any]]) -> str:
    if not tasks:
        return IDLE_MESSAGE
    return "\n".join(format_task_line(t) for t in tasks)


def format_inline_receipt(status: str, task_id: int | str, dept: str, summary: str) -> str:
    icons = {"DONE": "✅ DONE", "REVIEW": "⚠️ REVIEW", "BLOCKED": "❌ BLOCKED", "QUEUED": "⏳ QUEUED"}
    badge = icons.get(status.upper(), status.upper())
    clean_summary = " ".join(summary.strip().splitlines())[:160]
    return f"[{badge} | #{task_id} | {dept}] {clean_summary}"


def find_open_dedup_task(tasks: list[dict[str, Any]], dedup_key: str) -> dict[str, Any] | None:
    marker = f"[DEDUP:{dedup_key}]"
    for task in tasks:
        is_active = str(task.get("is_active", "1")) == "1"
        col_name = str(task.get("column_name", "")).lower()
        if not is_active or col_name == "done":
            continue
        haystack = f"{task.get('title', '')} {task.get('description', '')}"
        if marker in haystack:
            return task
    return None
