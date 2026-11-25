#!/usr/bin/env python3
"""Quét nhanh dấu hiệu văn AI bề mặt trong văn bản tiếng Việt/Anh (MIT — viet-nhu-nguoi).

Dùng: python3 -I scan.py FILE [--json] [--max 30]
      cat FILE | python3 -I scan.py [--json]
"""

import argparse
import json
import pathlib
import re
import sys
from typing import Any

RULES: list[tuple[str, int, str]] = [
    ("chatbot_opener", 12, r"(?im)^\s*(tất nhiên rồi|chắc chắn rồi|dưới đây là|sau đây là|rất vui được hỗ trợ|sure|certainly|here is|here are)\b"),
    ("chatbot_closer", 10, r"(?i)(hy vọng (thông tin|bài viết|nội dung) này (sẽ )?(hữu ích|giúp ích)|nếu bạn cần thêm|đừng ngần ngại|let me know if you need)"),
    ("contrast_cliche", 8, r"(?i)\bkhông chỉ\b[^.!?\n]{2,80}\bmà còn\b"),
    ("vn_buzzwords", 6, r"(?i)\b(trong bối cảnh|đóng vai trò then chốt|nâng tầm|mang lại giá trị|một cách toàn diện|hành trình|bước ngoặt|đột phá|tối ưu hóa trải nghiệm|khám phá sâu hơn)\b"),
    ("en_buzzwords", 6, r"(?i)\b(delve|tapestry|testament|pivotal|game-changer|seamlessly|comprehensive overview|leverage)\b"),
    ("summary_filler", 5, r"(?im)^\s*(tóm lại|nhìn chung|kết luận lại|tổng kết lại|in conclusion|in summary)\s*[,:]"),
]


def scan_text(text: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    score = 0
    for rule_id, weight, pattern in RULES:
        matches = re.findall(pattern, text)
        if matches:
            cnt = len(matches)
            pts = min(weight * cnt, weight * 3)
            score += pts
            findings.append({"rule": rule_id, "count": cnt, "points": pts})

    words = max(len(text.split()), 1)
    em_dashes = text.count("—")
    if em_dashes >= 3 and (em_dashes * 100 / words) >= 1.0:
        pts = min(em_dashes * 2, 12)
        score += pts
        findings.append({"rule": "em_dash_overuse", "count": em_dashes, "points": pts})

    bold_spans = len(re.findall(r"\*\*[^*\n]{2,80}\*\*", text))
    if bold_spans >= 6 and (bold_spans * 100 / words) >= 3.0:
        pts = min(bold_spans, 12)
        score += pts
        findings.append({"rule": "bold_overuse", "count": bold_spans, "points": pts})

    score = min(score, 100)
    level = "clean" if score <= 15 else ("review" if score <= 35 else "high_ai_tell")
    return {"score": score, "level": level, "words": words, "findings": findings}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scan", description="Quét dấu hiệu văn AI bề mặt (viet-nhu-nguoi)")
    parser.add_argument("file", nargs="?", help="Đường dẫn file văn bản (bỏ trống để đọc stdin)")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Xuất JSON")
    parser.add_argument("--max", type=int, default=None, dest="max_score", help="Thoát mã 1 nếu điểm > max")
    args = parser.parse_args(argv)

    text = pathlib.Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    res = scan_text(text)
    if args.as_json:
        print(json.dumps(res, ensure_ascii=False))
    else:
        print(f"Score: {res['score']}/100 ({res['level']}, {res['words']} words)")
        for item in res["findings"]:
            print(f"  - {item['rule']}: {item['count']}x (+{item['points']})")
    if args.max_score is not None and res["score"] > args.max_score:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
