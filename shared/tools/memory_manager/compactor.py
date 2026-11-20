"""Hermes Memory Compactor (<=100 Lines Cap) & Skill Proposal Gatekeeper."""

import pathlib
import time
from typing import Any

from shared.tools.kanboard_client.service import KanboardService

MAX_MEMORY_LINES = 100


def append_memory_fact(
    memory_file: pathlib.Path,
    fact: str,
    max_lines: int = MAX_MEMORY_LINES,
    date_str: str | None = None,
) -> dict[str, Any]:
    memory_file.parent.mkdir(parents=True, exist_ok=True)
    existing_lines = (
        memory_file.read_text(encoding="utf-8").splitlines()
        if memory_file.exists()
        else ["# Tier 2 Memory", "", "## Pinned Facts", "", "## Learned Observations"]
    )
    clean_fact = " ".join(fact.strip().splitlines())
    if any(clean_fact.lower() in ln.lower() for ln in existing_lines):
        return {"added": False, "compacted": False, "line_count": len(existing_lines)}

    stamp = date_str or time.strftime("%Y-%m-%d")
    existing_lines.append(f"- [{stamp}] {clean_fact}")
    compacted = False
    if len(existing_lines) > max_lines:
        existing_lines = compact_memory_lines(existing_lines, max_lines=max_lines)
        compacted = True

    memory_file.write_text("\n".join(existing_lines) + "\n", encoding="utf-8")
    return {"added": True, "compacted": compacted, "line_count": len(existing_lines)}


def compact_memory_lines(lines: list[str], max_lines: int = MAX_MEMORY_LINES) -> list[str]:
    preserved: list[str] = []
    observations: list[str] = []
    for ln in lines:
        if ln.startswith("- [20") and "[PINNED]" not in ln:
            if ln not in observations:
                observations.append(ln)
        else:
            preserved.append(ln)

    budget = max(5, max_lines - len(preserved))
    kept_obs = observations[-budget:]
    return preserved + kept_obs


def propose_skill_update(
    dept: str,
    skill_name: str,
    skill_markdown: str,
    skills_root: pathlib.Path = pathlib.Path("skills"),
    kb_service: KanboardService | None = None,
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
        )
    return {"draft_path": str(draft_path), "kanboard_result": kb_res, "lines": len(lines)}
