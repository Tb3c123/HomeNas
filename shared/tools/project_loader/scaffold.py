#!/usr/bin/env python3
"""Project Factory Scaffolder: Spins up an isolated 11-Agent Dev Project & Kickoff Prompt."""

import argparse
import pathlib
import re
import sys
from typing import Any

from shared.tools.kanboard_client.rpc_client import KanboardClient, KanboardRPCError

DEV_COLUMNS = ["Backlog", "Ready", "In Progress", "Waiting Review", "Done"]
DEV_SWIMLANES = ["Product & Design", "Backend", "Frontend", "QA & DevOps"]


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip()).strip("-")
    return slug or "new-project"


def _create_kanboard_dev_project(kb: KanboardClient, project_name: str) -> int:
    projects = kb.call("getAllProjects") or []
    existing = next((p for p in projects if p.get("name") == project_name), None)
    pid = int(existing["id"]) if existing else int(kb.call("createProject", {"name": project_name}))
    kb.call("addProjectUser", {"project_id": pid, "user_id": 1, "role": "project-manager"})
    liam = kb.call("getUserByName", {"username": "dept-dev"})
    if isinstance(liam, dict) and liam.get("id"):
        kb.call("addProjectUser", {"project_id": pid, "user_id": int(liam["id"]), "role": "project-member"})

    cols = kb.call("getColumns", {"project_id": pid}) or []
    by_title = {c["title"]: int(c["id"]) for c in cols}
    if "Work in progress" in by_title and "In Progress" not in by_title:
        kb.call("updateColumn", {"column_id": by_title["Work in progress"], "title": "In Progress"})
    cols = kb.call("getColumns", {"project_id": pid}) or []
    existing_cols = {c["title"] for c in cols}
    for col in DEV_COLUMNS:
        if col not in existing_cols:
            kb.call("addColumn", {"project_id": pid, "title": col})

    lanes = kb.call("getAllSwimlanes", {"project_id": pid}) or []
    lane_map = {ln["name"]: int(ln["id"]) for ln in lanes}
    if "Default swimlane" in lane_map and DEV_SWIMLANES[0] not in lane_map:
        kb.call("updateSwimlane", {"project_id": pid, "swimlane_id": lane_map["Default swimlane"], "name": DEV_SWIMLANES[0]})
        lane_map[DEV_SWIMLANES[0]] = lane_map.pop("Default swimlane")
    for lane in DEV_SWIMLANES:
        if lane not in lane_map:
            kb.call("addSwimlane", {"project_id": pid, "name": lane})
    return pid


def build_kickoff_prompt(project_name: str, project_dir: pathlib.Path, kb_project_id: int, summary: str) -> str:
    goal = summary.strip() or f"xây dựng sản phẩm {project_name}"
    return (
        f"✅ Đã khởi tạo xong không gian dự án **{project_name}** (Kanboard Project `#{kb_project_id}`).\n\n"
        f"### 🧭 Hướng dẫn 2 bước bắt đầu (Không cần chạy lệnh):\n"
        f"1. Trên giao diện Antigravity, bấm **New Chat / Open Folder** và chọn thư mục: `{project_dir}`\n"
        f"2. Bấm nút **Copy** ở góc phải khung dưới đây, dán vào khung chat mới đó và gửi:\n\n"
        f"```text\n"
        f"Chào đội ngũ! Hãy khởi động dự án {project_name} (Kanboard Project #{kb_project_id}) với vai trò Đội ngũ Thiết kế & Phát triển Sản phẩm 11 Micro-Agents theo đúng tệp AGENTS.md trong thư mục này.\n"
        f"Mục tiêu sản phẩm của tôi: {goal}.\n"
        f"Hãy xác nhận đã nạp AGENTS.md, USER.md cùng bộ skills, và đặt câu hỏi đầu tiên ở Phase 1 - Bước 1.1 để chúng ta bắt đầu thiết kế từng bước.\n"
        f"```"
    )


def scaffold_project(
    name: str,
    summary: str = "",
    workspace_root: pathlib.Path = pathlib.Path("/mnt/disk1/Workspace"),
    kb_client: KanboardClient | None = None,
    skip_kanboard: bool = False,
) -> dict[str, Any]:
    slug = _slugify(name)
    proj_dir = workspace_root / slug
    (proj_dir / "docs").mkdir(parents=True, exist_ok=True)
    (proj_dir / "memory").mkdir(parents=True, exist_ok=True)

    kb_pid = 0
    if not skip_kanboard:
        try:
            kb_pid = _create_kanboard_dev_project(kb_client or KanboardClient(), name)
        except KanboardRPCError:
            kb_pid = 0

    (proj_dir / "project.yaml").write_text(
        f"project:\n  id: {slug.lower()}\n  name: \"{name}\"\n  kanboard_project_id: {kb_pid}\n"
        f"  constraints:\n    max_lines_per_file: 150\n    max_retry_loops: 2\n"
        f"memory:\n  user_profile: \"/mnt/disk1/Workspace/HomeNas/shared/memory/USER.md\"\n"
        f"  project_memory: \"./memory/MEMORY.md\"\n"
        f"skills:\n  shared_dev_skills: \"/mnt/disk1/Workspace/HomeNas/skills/dept-dev\"\n",
        encoding="utf-8",
    )
    (proj_dir / "memory" / "MEMORY.md").write_text(
        f"# Tier 2 Memory: {name} (Max 100 Lines)\n\n## Pinned Facts\n"
        f"- [PINNED] Standalone project (Kanboard Project #{kb_pid}). Max 150 lines/file.\n\n"
        f"## Learned Observations\n",
        encoding="utf-8",
    )
    (proj_dir / "AGENTS.md").write_text(
        f"# {name} — Standalone 11 Micro-Agent Product Team (`AGENTS.md`)\n\n"
        f"- **Kanboard:** Project `#{kb_pid}` (`docker exec homenas-watchdog python3 -m shared.tools.kanboard_client.cli --project-id {kb_pid} ... --author dept-dev`).\n"
        f"- **Kế thừa Shared Platform:** Đọc `/mnt/disk1/Workspace/HomeNas/shared/memory/USER.md`, `./memory/MEMORY.md`, và nạp Lazy Load skills tại `/mnt/disk1/Workspace/HomeNas/skills/dept-dev/`.\n"
        f"- **Đội hình 11 Micro-Agents:** `dev-pm-lead`, `dev-ba`, `dev-ux-ui`, `dev-architect`, `dev-backend`, `dev-frontend`, `dev-refactor`, `dev-qa-tester`, `dev-security-reviewer`, `dev-devops`, `dev-docs-curator` (tối đa 2 vòng tự sửa `MAX_RETRY_LOOPS=2`).\n"
        f"- **Tự học Hermes Minh bạch:** Khi rút ra bài học mới, gọi `python3 /mnt/disk1/Workspace/HomeNas/shared/tools/memory_manager/cli.py add --dept {slug.lower()} --fact \"...\"` và in dòng `💾 Memory [{slug.lower()}] ➕ ...` ra khung chat.\n"
        f"- **Quy tắc cứng:** Mọi file ≤ 150 dòng (kiểm tra bằng `python3 /mnt/disk1/Workspace/HomeNas/shared/tools/guardrails/pre_tool_guard.py --audit-repo .`); cache test trên `/tmp`; đọc tự động mượt — trình Action Plan ≤ 8 dòng chờ PO duyệt 1 lần trước khi thêm/xóa/sửa.\n",
        encoding="utf-8",
    )
    prompt = build_kickoff_prompt(name, proj_dir, kb_pid, summary)
    return {"project_dir": str(proj_dir), "kanboard_project_id": kb_pid, "kickoff_prompt": prompt}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scaffold", description="Create standalone 11-Agent Dev Project")
    parser.add_argument("--name", required=True)
    parser.add_argument("--summary", default="")
    parser.add_argument("--workspace-root", default="/mnt/disk1/Workspace")
    parser.add_argument("--skip-kanboard", action="store_true")
    args = parser.parse_args(argv)
    res = scaffold_project(
        name=args.name,
        summary=args.summary,
        workspace_root=pathlib.Path(args.workspace_root),
        skip_kanboard=args.skip_kanboard,
    )
    print(res["kickoff_prompt"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
