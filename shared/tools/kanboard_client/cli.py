#!/usr/bin/env python3
"""CLI Entry Point for Kanboard Operations (list, create, move, comment, digest)."""

import argparse
import sys

from shared.tools.kanboard_client.service import KanboardService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kb", description="HomeNas Kanboard CLI")
    parser.add_argument("--project-id", type=int, default=None)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--swimlane", default=None)
    p_list.add_argument("--col", default=None)

    p_create = sub.add_parser("create")
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--desc", default="")
    p_create.add_argument("--tags", default="")
    p_create.add_argument("--dedup-key", default=None)

    p_move = sub.add_parser("move")
    p_move.add_argument("task_id", type=int)
    p_move.add_argument("--col-id", type=int, required=True)

    p_comment = sub.add_parser("comment")
    p_comment.add_argument("task_id", type=int)
    p_comment.add_argument("--text", required=True)

    p_digest = sub.add_parser("digest")
    p_digest.add_argument("--unread", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    svc = KanboardService(project_id=args.project_id)
    if args.cmd == "list":
        print(svc.list_tasks(swimlane=args.swimlane, column=args.col))
    elif args.cmd == "create":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        print(svc.create_task(args.title, args.desc, tags=tags, dedup_key=args.dedup_key))
    elif args.cmd == "move":
        print(svc.move_task(args.task_id, args.col_id))
    elif args.cmd == "comment":
        print(svc.comment_task(args.task_id, args.text))
    elif args.cmd == "digest":
        print(svc.unread_digest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
