"""Sub-First & Best-Value Quality Release Matcher (2K/4K Flexible for Movies, 1080p Clean for TV)."""

from typing import Any

BAD_TV_SOURCES = {"tvrip", "hdtv", "cam", "ts", "telecine"}


def _normalize_tokens(items: list[str]) -> set[str]:
    return {t.strip().lower() for t in items if t.strip()}


def match_sub_to_release(sub: dict[str, Any], release: dict[str, Any]) -> bool:
    sub_tags = _normalize_tokens(sub.get("release_tags", []))
    rel_group = str(release.get("release_group", "")).strip().lower()
    rel_source = str(release.get("source", "")).strip().lower()
    rel_title = str(release.get("title", "")).strip().lower()
    if rel_group and rel_group in sub_tags:
        return True
    for tag in sub_tags:
        if len(tag) >= 3 and (tag in rel_title or tag == rel_source):
            return True
    return False


def score_movie_release(release: dict[str, Any]) -> float:
    res = str(release.get("resolution", "")).lower()
    source = str(release.get("source", "")).lower()
    codec = str(release.get("codec", "")).lower()
    size_gb = float(release.get("size_gb", 5.0))

    if source in BAD_TV_SOURCES or "remux" in source or size_gb > 30.0:
        return -100.0

    score = 0.0
    if res in ("2160p", "4k", "1440p", "2k"):
        score += 100.0
        if 3.5 <= size_gb <= 14.0:
            score += 40.0 - abs(size_gb - 7.5) * 1.5
        elif size_gb <= 20.0:
            score += 15.0
    elif res == "1080p":
        score += 65.0
        if 1.8 <= size_gb <= 8.0:
            score += 25.0 - abs(size_gb - 4.0) * 1.5
    else:
        score += 10.0

    if any(c in codec for c in ("x265", "hevc", "av1")):
        score += 15.0
    if any(s in source for s in ("web-dl", "bluray", "webrip")):
        score += 10.0
    return round(score, 2)


def score_tv_release(release: dict[str, Any]) -> float:
    res = str(release.get("resolution", "")).lower()
    source = str(release.get("source", "")).lower()
    codec = str(release.get("codec", "")).lower()
    size_gb = float(release.get("size_gb", 1.2))

    if any(bad in source for bad in BAD_TV_SOURCES):
        return -100.0

    score = 0.0
    if res == "1080p":
        score += 100.0
    elif res in ("2160p", "4k", "1440p", "2k") and size_gb <= 3.0:
        score += 85.0
    elif res == "720p":
        score += 30.0

    if "web-dl" in source or "bluray" in source:
        score += 25.0
    elif "webrip" in source:
        score += 15.0
    if any(c in codec for c in ("x265", "hevc", "av1")):
        score += 10.0
    return round(score, 2)


def select_sub_first_candidates(
    media_type: str,
    subtitles: list[dict[str, Any]],
    releases: list[dict[str, Any]],
    top_k: int = 3,
) -> list[dict[str, Any]]:
    vi_subs = [s for s in subtitles if str(s.get("lang", "vi")).lower() in ("vi", "vie", "vietnamese")]
    if not vi_subs:
        return []

    is_tv = media_type.lower() in ("tv", "tvshows", "series", "sonarr")
    scorer = score_tv_release if is_tv else score_movie_release
    pairs: list[dict[str, Any]] = []

    for rel in releases:
        matched_sub = next((s for s in vi_subs if match_sub_to_release(s, rel)), None)
        if not matched_sub:
            continue
        pts = scorer(rel)
        if pts < 0:
            continue
        pairs.append(
            {
                "score": pts,
                "release": rel,
                "subtitle": matched_sub,
            }
        )

    pairs.sort(key=lambda item: item["score"], reverse=True)
    return pairs[:top_k]
