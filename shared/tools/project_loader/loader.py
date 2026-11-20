"""Zero-Dependency YAML Subset Parser & Validator for Multi-Project project.yaml."""

import pathlib
import re
from typing import Any


def load_project_manifest(manifest_path: pathlib.Path) -> dict[str, Any]:
    if not manifest_path.exists():
        raise FileNotFoundError(f"Project manifest not found: {manifest_path}")
    text = manifest_path.read_text(encoding="utf-8")

    def _find_val(key: str, default: str = "") -> str:
        m = re.search(rf"^\s*{re.escape(key)}:\s*(.+)$", text, flags=re.MULTILINE)
        return m.group(1).strip().strip('"').strip("'") if m else default

    project_id = _find_val("id", "unknown")
    name = _find_val("name", project_id)
    kb_pid = int(_find_val("kanboard_project_id", "1"))
    max_lines = int(_find_val("max_lines_per_file", "150"))
    max_loops = int(_find_val("max_retry_loops", "2"))

    depts: dict[str, dict[str, Any]] = {}
    in_depts = False
    cur_dept: str | None = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if indent == 0 and stripped.startswith("departments:"):
            in_depts = True
            continue
        if indent == 0 and not stripped.startswith("departments:"):
            in_depts = False
            cur_dept = None
        if in_depts and indent == 2 and stripped.endswith(":"):
            cur_dept = stripped[:-1].strip()
            depts[cur_dept] = {"allowed_tools": []}
        elif in_depts and cur_dept and indent == 4 and ":" in stripped:
            k, v = stripped.split(":", 1)
            k = k.strip()
            v = v.strip()
            if k == "allowed_tools" and v.startswith("["):
                items = [x.strip().strip('"').strip("'") for x in v.strip("[]").split(",") if x.strip()]
                depts[cur_dept]["allowed_tools"] = items
            else:
                depts[cur_dept][k] = v.strip('"').strip("'")

    return {
        "id": project_id,
        "name": name,
        "kanboard_project_id": kb_pid,
        "max_lines_per_file": max_lines,
        "max_retry_loops": max_loops,
        "departments": depts,
    }


def verify_tool_permission(manifest: dict[str, Any], dept: str, tool_name: str) -> bool:
    dept_cfg = manifest.get("departments", {}).get(dept, {})
    allowed = dept_cfg.get("allowed_tools", [])
    return tool_name in allowed
