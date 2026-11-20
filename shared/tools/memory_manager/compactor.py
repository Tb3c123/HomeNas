"""Hermes Memory Engine (add, patch, remove, <=100-line compaction & Toast notifications)."""

import pathlib
import time
from typing import Any

from shared.tools.kanboard_client.service import KanboardService
from shared.tools.memory_manager.archive_store import (
    DEFAULT_ARCHIVE,
    DEFAULT_FEED,
    read_recent_learning_toasts,
    record_archive,
    record_learning_toast,
)

MAX_MEMORY_LINES = 100


def compact_memory_lines(
    lines: list[str],
    max_lines: int = MAX_MEMORY_LINES,
    archive_path: pathlib.Path = DEFAULT_ARCHIVE,
    target_label: str = "MEMORY.md",
) -> list[str]:
    preserved, observations = [], []
    for ln in lines:
        if ln.startswith("- [20") and "[PINNED]" not in ln:
            if ln not in observations:
                observations.append(ln)
        else:
            preserved.append(ln)
    budget = max(5, max_lines - len(preserved))
    evicted = observations[:-budget] if len(observations) > budget else []
    record_archive(archive_path, "compact", target_label, evicted)
    return preserved + observations[-budget:]


def append_memory_fact(
    memory_file: pathlib.Path,
    fact: str,
    max_lines: int = MAX_MEMORY_LINES,
    date_str: str | None = None,
    dept_label: str | None = None,
    archive_path: pathlib.Path = DEFAULT_ARCHIVE,
    feed_path: pathlib.Path = DEFAULT_FEED,
) -> dict[str, Any]:
    memory_file.parent.mkdir(parents=True, exist_ok=True)
    existing = (
        memory_file.read_text(encoding="utf-8").splitlines()
        if memory_file.exists()
        else ["# Tier 2 Memory", "", "## Pinned Facts", "", "## Learned Observations"]
    )
    clean = " ".join(fact.strip().splitlines())
    label = dept_label or memory_file.parent.name or "global"
    if any(clean.lower() in ln.lower() for ln in existing):
        toast = f"💾 Memory [{label}] ℹ️ Already known (no duplicate added)"
        return {"added": False, "compacted": False, "line_count": len(existing), "toast": toast}

    stamp = date_str or time.strftime("%Y-%m-%d")
    existing.append(f"- [{stamp}] {clean}")
    compacted = len(existing) > max_lines
    if compacted:
        existing = compact_memory_lines(existing, max_lines=max_lines, archive_path=archive_path, target_label=label)

    memory_file.write_text("\n".join(existing) + "\n", encoding="utf-8")
    toast = f"💾 Memory [{label}] ➕ {clean}"
    record_learning_toast(feed_path, toast)
    return {"added": True, "compacted": compacted, "line_count": len(existing), "toast": toast}


def patch_memory_fact(
    memory_file: pathlib.Path,
    old_substring: str,
    new_fact: str,
    dept_label: str | None = None,
    archive_path: pathlib.Path = DEFAULT_ARCHIVE,
    feed_path: pathlib.Path = DEFAULT_FEED,
) -> dict[str, Any]:
    label = dept_label or memory_file.parent.name or "global"
    if not memory_file.exists():
        return {"patched": False, "toast": f"💾 Memory [{label}] ⚠️ File not found"}
    lines = memory_file.read_text(encoding="utf-8").splitlines()
    clean_new = " ".join(new_fact.strip().splitlines())
    stamp = time.strftime("%Y-%m-%d")
    for idx, ln in enumerate(lines):
        if old_substring.lower() in ln.lower():
            record_archive(archive_path, "patch", label, [ln])
            lines[idx] = f"- [{stamp}] {clean_new}"
            memory_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            toast = f"💾 Memory [{label}] ✏️ {old_substring} -> {clean_new}"
            record_learning_toast(feed_path, toast)
            return {"patched": True, "toast": toast}
    return {"patched": False, "toast": f"💾 Memory [{label}] ⚠️ Entry '{old_substring}' not found"}


def remove_memory_fact(
    memory_file: pathlib.Path,
    old_substring: str,
    dept_label: str | None = None,
    archive_path: pathlib.Path = DEFAULT_ARCHIVE,
    feed_path: pathlib.Path = DEFAULT_FEED,
) -> dict[str, Any]:
    label = dept_label or memory_file.parent.name or "global"
    if not memory_file.exists():
        return {"removed": False, "toast": f"💾 Memory [{label}] ⚠️ File not found"}
    lines = memory_file.read_text(encoding="utf-8").splitlines()
    kept = [ln for ln in lines if not (old_substring.lower() in ln.lower() and "[PINNED]" not in ln)]
    removed = [ln for ln in lines if old_substring.lower() in ln.lower() and "[PINNED]" not in ln]
    if not removed:
        return {"removed": False, "toast": f"💾 Memory [{label}] ⚠️ No removable match for '{old_substring}'"}
    record_archive(archive_path, "remove", label, removed)
    memory_file.write_text("\n".join(kept) + "\n", encoding="utf-8")
    toast = f"💾 Memory [{label}] 🗑️ Removed {len(removed)} entry ({old_substring})"
    record_learning_toast(feed_path, toast)
    return {"removed": True, "toast": toast}


def propose_skill_update(
    dept: str,
    skill_name: str,
    skill_markdown: str,
    skills_root: pathlib.Path = pathlib.Path("skills"),
    kb_service: KanboardService | None = None,
    feed_path: pathlib.Path = DEFAULT_FEED,
) -> dict[str, Any]:
    lines = skill_markdown.splitlines()
    if len(lines) > 150:
        raise ValueError(f"Skill proposal rejected: {len(lines)} lines exceeds 150-line cap.")
    draft_path = skills_root / dept / skill_name / "SKILL.draft.md"
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text(skill_markdown, encoding="utf-8")
    kb_res = "SKIPPED_KB"
    if kb_service is not None:
        kb_res = kb_service.create_task(
            title=f"[SKILL-PROPOSAL] {dept}/{skill_name}",
            description=f"Draft saved at {draft_path} ({len(lines)} lines). Awaiting PO review.",
            tags=["skill-proposal", "needs-approval"],
            dedup_key=f"skill:{dept}:{skill_name}",
            author=dept,
        )
    toast = f"💾 Skill [{dept}/{skill_name}] 📦 Proposed ({len(lines)}L) -> {kb_res}"
    record_learning_toast(feed_path, toast)
    return {"draft_path": str(draft_path), "kanboard_result": kb_res, "lines": len(lines), "toast": toast}
