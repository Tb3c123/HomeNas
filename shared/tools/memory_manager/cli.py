#!/usr/bin/env python3
"""CLI for Hermes Memory Tool (add, patch, remove, list, propose-skill) with Toast Badges."""

import argparse
import pathlib
import sys

from shared.tools.kanboard_client.service import KanboardService
from shared.tools.memory_manager.compactor import (
    append_memory_fact,
    patch_memory_fact,
    propose_skill_update,
    read_recent_learning_toasts,
    remove_memory_fact,
)


def _resolve_mem_path(dept: str) -> pathlib.Path:
    if dept == "user":
        return pathlib.Path("shared/memory/USER.md")
    return pathlib.Path("memory") / dept / "MEMORY.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hermes-memory", description="HomeNas Hermes Memory CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("--dept", required=True)
    p_add.add_argument("--fact", required=True)

    p_patch = sub.add_parser("patch")
    p_patch.add_argument("--dept", required=True)
    p_patch.add_argument("--old", required=True)
    p_patch.add_argument("--new", required=True)

    p_rm = sub.add_parser("remove")
    p_rm.add_argument("--dept", required=True)
    p_rm.add_argument("--match", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--dept", default=None)

    p_skill = sub.add_parser("propose-skill")
    p_skill.add_argument("--dept", required=True)
    p_skill.add_argument("--name", required=True)
    p_skill.add_argument("--file", required=True)

    args = parser.parse_args(argv)
    if args.cmd == "add":
        res = append_memory_fact(_resolve_mem_path(args.dept), args.fact, dept_label=args.dept)
        print(res["toast"])
    elif args.cmd == "patch":
        res = patch_memory_fact(_resolve_mem_path(args.dept), args.old, args.new, dept_label=args.dept)
        print(res["toast"])
    elif args.cmd == "remove":
        res = remove_memory_fact(_resolve_mem_path(args.dept), args.match, dept_label=args.dept)
        print(res["toast"])
    elif args.cmd == "list":
        if args.dept:
            path = _resolve_mem_path(args.dept)
            print(path.read_text(encoding="utf-8").strip() if path.exists() else f"[EMPTY] {path}")
        else:
            toasts = read_recent_learning_toasts(limit=5)
            print("\n".join(toasts) if toasts else "[ℹ️ IDLE] Chưa có ghi nhận học mới.")
    elif args.cmd == "propose-skill":
        md = pathlib.Path(args.file).read_text(encoding="utf-8")
        res = propose_skill_update(args.dept, args.name, md, kb_service=KanboardService())
        print(res["toast"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
