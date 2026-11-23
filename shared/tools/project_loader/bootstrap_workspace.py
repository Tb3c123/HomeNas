#!/usr/bin/env python3
"""Option 1+ Workspace Shared Namespace Bootstrapper & Child-Project Path Migrator.

Creates canonical peer symlinks so all child projects (Project #2..#N) use:
  /mnt/disk1/Workspace/shared/templates/DEV_TEAM_RULES.md
  /mnt/disk1/Workspace/shared/memory/USER.md
  /mnt/disk1/Workspace/shared/skills/dept-dev/CATALOG.md
  /mnt/disk1/Workspace/shared/tools/...
without any path dependency on 'HomeNas', while keeping 1 single Git repository.
"""

import argparse
import json
import pathlib
import sys
from typing import Any

LEGACY_REPLACEMENTS = [
    ("/mnt/disk1/Workspace/HomeNas/shared/", "/mnt/disk1/Workspace/shared/"),
    ("/mnt/disk1/Workspace/HomeNas/skills/dept-dev", "/mnt/disk1/Workspace/shared/skills/dept-dev"),
]


def _ensure_symlink(link_path: pathlib.Path, target_path: pathlib.Path) -> str:
    link_path.parent.mkdir(parents=True, exist_ok=True)
    if link_path.is_symlink():
        if link_path.resolve() == target_path.resolve():
            return "unchanged"
        link_path.unlink()
    elif link_path.exists():
        return "skipped_real_dir"
    link_path.symlink_to(target_path, target_is_directory=True)
    return "linked"


def bootstrap_workspace_shared(
    workspace_root: pathlib.Path = pathlib.Path("/mnt/disk1/Workspace"),
    homenas_name: str = "HomeNas",
) -> dict[str, Any]:
    homenas_dir = workspace_root / homenas_name
    shared_src = homenas_dir / "shared"
    dev_skills_src = homenas_dir / "skills" / "dept-dev"

    ws_shared_link = workspace_root / "shared"
    skills_bridge_link = shared_src / "skills" / "dept-dev"

    top_status = _ensure_symlink(ws_shared_link, shared_src)
    skills_status = _ensure_symlink(skills_bridge_link, dev_skills_src)

    migrated_projects: list[str] = []
    for child in sorted(workspace_root.iterdir()):
        if not child.is_dir() or child.is_symlink() or child.name in (homenas_name, "shared"):
            continue
        touched = False
        for fname in ("AGENTS.md", "project.yaml"):
            fpath = child / fname
            if not fpath.is_file():
                continue
            original = fpath.read_text(encoding="utf-8")
            updated = original
            for old_str, new_str in LEGACY_REPLACEMENTS:
                updated = updated.replace(old_str, new_str)
            if updated != original:
                fpath.write_text(updated, encoding="utf-8")
                touched = True
        if touched:
            migrated_projects.append(child.name)

    return {
        "workspace_shared": str(ws_shared_link),
        "top_symlink": top_status,
        "skills_bridge": skills_status,
        "migrated_projects": migrated_projects,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bootstrap-workspace", description="Bootstrap /Workspace/shared Option 1+")
    parser.add_argument("--workspace-root", default="/mnt/disk1/Workspace")
    parser.add_argument("--homenas-name", default="HomeNas")
    args = parser.parse_args(argv)
    res = bootstrap_workspace_shared(
        workspace_root=pathlib.Path(args.workspace_root),
        homenas_name=args.homenas_name,
    )
    print(json.dumps(res, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
