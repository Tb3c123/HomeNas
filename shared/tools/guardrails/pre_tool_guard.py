#!/usr/bin/env python3
"""0-Token PreToolUse & Pre-Commit Guardrail for HomeNas.

Enforces:
1. Project-wide <= 150 lines per file cap (except lock/install manifests).
2. Anti-bypass detection (blocks semicolon-crammed single lines > 240 chars).
3. Destructive command blocking (rm -rf /, git push --force, git reset --hard,
   stopping protected containers like adguard-home, portainer, casaos, kanboard).
"""

import json
import pathlib
import re
import sys

MAX_LINES = 150
MAX_SKILL_LINES = 1000
MAX_SKILL_BYTES = 65536
EXEMPT_NAMES = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "uv.lock",
    "poetry.lock",
    "requirements.txt",
}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", "data", "node_modules"}
PROTECTED_CONTAINERS = (
    "adguard-home",
    "portainer",
    "casaos",
    "kanboard",
    "homenas-watchdog",
    "antigravity-cli",
)
FORBIDDEN_PATTERNS = [
    (r"git\s+push\s+.*(-f|--force)", "Blocked: git push --force requires PO approval."),
    (r"git\s+reset\s+--hard", "Blocked: git reset --hard requires PO approval."),
    (r"rm\s+-rf\s+(/|/mnt|/DATA)\b", "Blocked: destructive rm -rf on root/mount paths."),
    (r"docker\s+system\s+prune", "Blocked: docker system prune requires PO approval."),
]


def _is_skill_markdown(path: pathlib.Path) -> bool:
    return path.name == "SKILL.md" and "skills" in path.parts


def _is_extended_markdown(path: pathlib.Path) -> bool:
    return _is_skill_markdown(path) or path.name == "DESIGN.md"


def check_command_safety(command_str: str) -> list[str]:
    errors: list[str] = []
    for pattern, msg in FORBIDDEN_PATTERNS:
        if re.search(pattern, command_str):
            errors.append(msg)
    for container in PROTECTED_CONTAINERS:
        pattern = rf"docker\s+(stop|kill|rm|pause)\b.*\b{re.escape(container)}\b"
        if re.search(pattern, command_str):
            errors.append(f"Blocked: container '{container}' is protected from stop/rm/pause.")
    return errors


def check_file_compliance(path: pathlib.Path) -> list[str]:
    if not path.is_file() or path.name in EXEMPT_NAMES:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    lines = text.splitlines()
    errors: list[str] = []
    extended = _is_extended_markdown(path)
    cap = MAX_SKILL_LINES if extended else MAX_LINES
    if len(lines) > cap:
        errors.append(f"{path}: {len(lines)} lines exceeds cap of {cap} lines.")
    if extended and len(text.encode("utf-8")) > MAX_SKILL_BYTES:
        errors.append(f"{path}: exceeds {MAX_SKILL_BYTES} bytes cap for {path.name}.")
    code_exts = {".py", ".sh", ".js", ".ts", ".jsx", ".tsx", ".css"}
    if path.suffix in code_exts:
        for idx, line in enumerate(lines, start=1):
            if len(line) > 240 and line.count(";") >= 3:
                errors.append(f"{path}:{idx}: Anti-bypass triggered (crammed line with >=3 ';').")
    return errors


def audit_repository(root: pathlib.Path) -> list[str]:
    errors: list[str] = []
    for item in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in item.parts) or item.is_symlink():
            continue
        errors.extend(check_file_compliance(item))
    return errors


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--audit-repo":
        root = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else ".")
        errs = audit_repository(root)
        if errs:
            print("\n".join(errs), file=sys.stderr)
            return 1
        print(f"[OK] All files in {root.resolve()} comply with <= {MAX_LINES} line cap.")
        return 0

    raw = sys.stdin.read().strip()
    if not raw:
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return 0

    cmd = str(payload.get("command") or payload.get("CommandLine") or "")
    errs = check_command_safety(cmd)
    content = payload.get("CodeContent") or payload.get("ReplacementContent")
    target = payload.get("TargetFile")
    target_path = pathlib.Path(target) if target else None
    if isinstance(content, str) and (not target_path or target_path.name not in EXEMPT_NAMES):
        cap = MAX_SKILL_LINES if (target_path and _is_extended_markdown(target_path)) else MAX_LINES
        if len(content.splitlines()) > cap:
            errs.append(f"Blocked write: content has {len(content.splitlines())} lines (> {cap}).")
    if errs:
        print("\n".join(errs), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
