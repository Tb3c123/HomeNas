"""Direct-Fetch Skill Downloader & 2-Step Security Auditor (Synced with HomeNas Manager :8090)."""

import pathlib
import re
import urllib.request
from typing import Any, Callable

from shared.tools.guardrails.pre_tool_guard import (
    MAX_LINES,
    MAX_SKILL_BYTES,
    MAX_SKILL_LINES,
    check_command_safety,
)

CURATED_SKILL_SOURCES: dict[str, str] = {
    "brainstorming": "https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md",
    "writing-plans": "https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md",
    "test-driven-development": "https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/SKILL.md",
    "systematic-debugging": "https://raw.githubusercontent.com/obra/superpowers/main/skills/systematic-debugging/SKILL.md",
    "requesting-code-review": "https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/SKILL.md",
    "dispatching-parallel-agents": "https://raw.githubusercontent.com/obra/superpowers/main/skills/dispatching-parallel-agents/SKILL.md",
    "skill-creator": "https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md",
    "mcp-builder": "https://raw.githubusercontent.com/anthropics/skills/main/skills/mcp-builder/SKILL.md",
    "frontend-design": "https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md",
    "webapp-testing": "https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md",
}

DANGEROUS_SKILL_PATTERNS = [
    r"curl\s+.*\|\s*(?:ba)?sh",
    r"wget\s+.*\|\s*(?:ba)?sh",
    r"rm\s+-rf\s+/",
    r"chmod\s+777\s+/",
    r"/etc/shadow\b",
    r"ignore\s+(?:all\s+)?previous\s+instructions",
]

WARNING_SKILL_PATTERNS = [
    (r"\bsudo\b", "Contains 'sudo' privilege escalation command."),
    (r"\bdocker\b", "Contains 'docker' command reference."),
    (r"\bcurl\b|\bwget\b", "Contains external network fetch command (curl/wget)."),
]


def inspect_skill_warnings(markdown_text: str) -> list[str]:
    warnings: list[str] = []
    lines = markdown_text.splitlines()
    if len(lines) > MAX_LINES:
        warnings.append(f"External skill has {len(lines)} lines (> {MAX_LINES} internal baseline; <= {MAX_SKILL_LINES} allowed).")
    for pat, msg in WARNING_SKILL_PATTERNS:
        if re.search(pat, markdown_text, flags=re.IGNORECASE):
            warnings.append(msg)
    return warnings


def audit_skill_content(markdown_text: str, max_lines: int = MAX_SKILL_LINES) -> list[str]:
    issues: list[str] = []
    lines = markdown_text.splitlines()
    if len(lines) > max_lines:
        issues.append(f"Skill exceeds {max_lines} lines ({len(lines)} lines).")
    if len(markdown_text.encode("utf-8")) > MAX_SKILL_BYTES:
        issues.append(f"Skill exceeds {MAX_SKILL_BYTES} bytes (64 KB) cap.")
    if not markdown_text.lstrip().startswith("---"):
        issues.append("Missing YAML frontmatter ('---') required by Agent Skills standard.")
    for pat in DANGEROUS_SKILL_PATTERNS:
        if re.search(pat, markdown_text, flags=re.IGNORECASE):
            issues.append(f"Dangerous pattern detected in skill: {pat}")
    issues.extend(check_command_safety(markdown_text))
    return issues


def fetch_and_stage_skill(
    dept: str,
    skill_name: str,
    raw_url: str | None = None,
    skills_root: pathlib.Path = pathlib.Path("skills"),
    http_getter: Callable[[str], str] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    url = raw_url or CURATED_SKILL_SOURCES.get(skill_name)
    if not url:
        raise KeyError(f"Unknown skill '{skill_name}' and no raw_url provided.")

    if http_getter is not None:
        content = http_getter(url)
    else:
        with urllib.request.urlopen(url, timeout=10) as resp:
            content = resp.read().decode("utf-8")

    issues = audit_skill_content(content)
    warnings = inspect_skill_warnings(content)
    line_count = len(content.splitlines())
    if issues:
        return {"staged": False, "skill": skill_name, "issues": issues, "warnings": warnings, "lines": line_count}
    if dry_run:
        return {"staged": False, "preview_ok": True, "skill": skill_name, "issues": [], "warnings": warnings, "lines": line_count}

    dest = skills_root / dept / skill_name / "SKILL.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    return {"staged": True, "skill": skill_name, "path": str(dest), "lines": line_count, "warnings": warnings}
