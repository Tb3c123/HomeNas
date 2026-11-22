#!/usr/bin/env python3
"""Zero-Noise Media Inspector CLI for dept-media."""

import argparse
import json
import pathlib
import sys

from tools.media_ops.direct_fetcher import plan_or_execute_direct_fetch
from tools.media_ops.disk_balancer import ensure_mirror_structure, select_target_disk


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="media-inspector", description="HomeNas Media Inspector")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init-mirror")
    p_init.add_argument("--disk1", default="/mnt/disk1")
    p_init.add_argument("--disk2", default="/mnt/disk2")

    p_route = sub.add_parser("route")
    p_route.add_argument("--type", required=True, choices=["movie", "tv"])
    p_route.add_argument("--category", required=True)
    p_route.add_argument("--series", default=None)
    p_route.add_argument("--disk1", default="/mnt/disk1")
    p_route.add_argument("--disk2", default="/mnt/disk2")

    p_df = sub.add_parser("direct-fetch")
    p_df.add_argument("--url", required=True)
    p_df.add_argument("--title", required=True)
    p_df.add_argument("--type", default="movie", choices=["movie", "tv"])
    p_df.add_argument("--category", default="Cinema")
    p_df.add_argument("--season", type=int, default=1)
    p_df.add_argument("--filename", default=None)
    p_df.add_argument("--disk1", default="/mnt/disk1")
    p_df.add_argument("--disk2", default="/mnt/disk2")
    p_df.add_argument("--execute", action="store_true")

    args = parser.parse_args(argv)
    if args.cmd == "init-mirror":
        created = ensure_mirror_structure([pathlib.Path(args.disk1), pathlib.Path(args.disk2)])
        print(json.dumps({"created_count": len(created), "created": created}, separators=(",", ":")))
    elif args.cmd == "route":
        info = select_target_disk(
            media_type=args.type,
            category=args.category,
            series_title=args.series,
            disk1_root=pathlib.Path(args.disk1),
            disk2_root=pathlib.Path(args.disk2),
        )
        print(json.dumps(info, separators=(",", ":")))
    elif args.cmd == "direct-fetch":
        res = plan_or_execute_direct_fetch(
            url=args.url,
            title=args.title,
            media_type=args.type,
            category=args.category,
            season=args.season,
            filename=args.filename,
            disk1_root=pathlib.Path(args.disk1),
            disk2_root=pathlib.Path(args.disk2),
            execute=args.execute,
        )
        print(json.dumps(res, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
