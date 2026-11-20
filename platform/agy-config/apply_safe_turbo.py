#!/usr/bin/env python3
"""Safely merge Safe-Turbo settings into Antigravity CLI settings.json without data loss."""

import json
import pathlib
import sys
from typing import Any

DEFAULT_TEMPLATE = pathlib.Path(__file__).resolve().parent / "settings.safe-turbo.json"
DEFAULT_TARGET = pathlib.Path("/root/.gemini/antigravity-cli/settings.json")


def _merge_unique_list(base: list[str], extra: list[str]) -> list[str]:
    result = list(base)
    for item in extra:
        if item not in result:
            result.append(item)
    return result


def merge_settings(existing: dict[str, Any], template: dict[str, Any]) -> dict[str, Any]:
    merged = dict(existing)
    for key in ("agentMode", "toolPermission", "artifactReviewPolicy"):
        if key in template:
            merged[key] = template[key]

    merged["trustedWorkspaces"] = _merge_unique_list(
        list(existing.get("trustedWorkspaces", [])),
        list(template.get("trustedWorkspaces", [])),
    )

    perms = dict(existing.get("permissions", {}))
    tpl_perms = template.get("permissions", {})
    for bucket in ("allow", "deny", "ask"):
        if bucket in tpl_perms:
            perms[bucket] = _merge_unique_list(list(perms.get(bucket, [])), list(tpl_perms[bucket]))
    merged["permissions"] = perms
    return merged


def apply_safe_turbo(target: pathlib.Path = DEFAULT_TARGET, template: pathlib.Path = DEFAULT_TEMPLATE) -> pathlib.Path:
    tpl_data = json.loads(template.read_text(encoding="utf-8"))
    existing_data: dict[str, Any] = {}
    if target.exists():
        raw = target.read_text(encoding="utf-8").strip()
        if raw:
            existing_data = json.loads(raw)
    merged = merge_settings(existing_data, tpl_data)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    target = pathlib.Path(args[0]) if args else DEFAULT_TARGET
    out = apply_safe_turbo(target=target)
    print(f"[OK] Safe-Turbo merged into {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
