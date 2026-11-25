#!/usr/bin/env python3
"""Đối chiếu bảo toàn dữ kiện giữa văn bản gốc và bản đã biên tập (MIT — viet-nhu-nguoi).

Dùng: python3 -I check_facts.py ORIG_FILE EDITED_FILE [--json]
"""

import argparse
import json
import pathlib
import re
import sys
from collections import Counter
from typing import Any

FACT_PATTERNS: dict[str, str] = {
    "numbers": r"\b\d+(?:[.,:/-]\d+)*%?\b",
    "urls": r"https?://[^\s)\]>\"']+",
    "emails": r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
}
NEGATION_RE = re.compile(r"(?i)\b(không|chưa|đừng|chẳng|hết|tránh|cấm|never|not|no|cannot|don't|won't)\b")


def extract_facts(text: str) -> dict[str, Counter[str]]:
    return {
        key: Counter(re.findall(pat, text))
        for key, pat in FACT_PATTERNS.items()
    }


def compare_facts(orig_text: str, edited_text: str) -> dict[str, Any]:
    orig = extract_facts(orig_text)
    edited = extract_facts(edited_text)
    missing: dict[str, list[str]] = {}
    added: dict[str, list[str]] = {}

    for key in FACT_PATTERNS:
        miss = list((orig[key] - edited[key]).elements())
        extra = list((edited[key] - orig[key]).elements())
        if miss:
            missing[key] = sorted(miss)
        if extra:
            added[key] = sorted(extra)

    orig_neg = len(NEGATION_RE.findall(orig_text))
    edit_neg = len(NEGATION_RE.findall(edited_text))
    neg_drift = edit_neg - orig_neg
    ok = not missing and not added and abs(neg_drift) <= 1
    return {
        "ok": ok,
        "missing_facts": missing,
        "added_facts": added,
        "negation_count": {"orig": orig_neg, "edited": edit_neg, "drift": neg_drift},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check_facts", description="Kiểm tra bảo toàn dữ kiện gốc vs bản sửa")
    parser.add_argument("orig_file", help="Đường dẫn văn bản gốc")
    parser.add_argument("edited_file", help="Đường dẫn văn bản đã biên tập")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Xuất JSON")
    args = parser.parse_args(argv)

    orig_text = pathlib.Path(args.orig_file).read_text(encoding="utf-8")
    edited_text = pathlib.Path(args.edited_file).read_text(encoding="utf-8")
    res = compare_facts(orig_text, edited_text)
    if args.as_json:
        print(json.dumps(res, ensure_ascii=False))
    else:
        status = "OK" if res["ok"] else "MISMATCH"
        print(f"[{status}] negation={res['negation_count']} missing={res['missing_facts']} added={res['added_facts']}")
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
