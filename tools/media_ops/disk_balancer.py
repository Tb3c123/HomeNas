"""1:1 Dual-Disk Mirror Manager & Disk Placement Router (disk1 & disk2)."""

import pathlib
import shutil
from typing import Any

MOVIE_CATEGORIES = ("Cinema", "Asian", "Vietnamese")
TV_CATEGORIES = ("International", "K-Drama", "C-Drama", "Vietnamese", "Reality_Shows")


def ensure_mirror_structure(disk_roots: list[pathlib.Path]) -> list[str]:
    created: list[str] = []
    for root in disk_roots:
        media = root / "Media"
        paths = [
            media / ".downloads" / "radarr",
            media / ".downloads" / "sonarr",
            *(media / "Movies" / cat for cat in MOVIE_CATEGORIES),
            *(media / "TVShows" / cat for cat in TV_CATEGORIES),
        ]
        for p in paths:
            if not p.exists():
                p.mkdir(parents=True, exist_ok=True)
                created.append(str(p))
    return created


def _free_bytes(path: pathlib.Path, free_space_override: dict[str, int] | None = None) -> int:
    if free_space_override and path.name in free_space_override:
        return free_space_override[path.name]
    if path.exists():
        return shutil.disk_usage(path).free
    return 0


def _count_seasons(series_dir: pathlib.Path) -> int:
    if not series_dir.exists():
        return 0
    seasons = [d for d in series_dir.iterdir() if d.is_dir() and d.name.lower().startswith("season")]
    return max(1, len(seasons))


def select_target_disk(
    media_type: str,
    category: str,
    series_title: str | None = None,
    disk1_root: pathlib.Path = pathlib.Path("/mnt/disk1"),
    disk2_root: pathlib.Path = pathlib.Path("/mnt/disk2"),
    free_space_override: dict[str, int] | None = None,
) -> dict[str, Any]:
    is_tv = media_type.lower() in ("tv", "tvshows", "series", "sonarr")
    sub_root = "TVShows" if is_tv else "Movies"
    valid_cats = TV_CATEGORIES if is_tv else MOVIE_CATEGORIES
    if category not in valid_cats:
        raise ValueError(f"Invalid category '{category}' for {sub_root}. Allowed: {valid_cats}")

    chosen_disk = "disk1"
    needs_consolidation = False

    if is_tv and series_title:
        d1_series = disk1_root / "Media" / "TVShows" / category / series_title
        d2_series = disk2_root / "Media" / "TVShows" / category / series_title
        c1 = _count_seasons(d1_series)
        c2 = _count_seasons(d2_series)
        if c1 > 0 and c2 > 0:
            needs_consolidation = True
            chosen_disk = "disk1" if c1 >= c2 else "disk2"
        elif c1 > 0:
            chosen_disk = "disk1"
        elif c2 > 0:
            chosen_disk = "disk2"
        else:
            f1 = _free_bytes(disk1_root, free_space_override)
            f2 = _free_bytes(disk2_root, free_space_override)
            chosen_disk = "disk1" if f1 >= f2 else "disk2"
    else:
        f1 = _free_bytes(disk1_root, free_space_override)
        f2 = _free_bytes(disk2_root, free_space_override)
        chosen_disk = "disk1" if f1 >= f2 else "disk2"

    app = "sonarr" if is_tv else "radarr"
    host_root = disk1_root if chosen_disk == "disk1" else disk2_root
    return {
        "disk": chosen_disk,
        "qbit_category": f"{app}-{chosen_disk}",
        "container_staging": f"/data/{chosen_disk}/.downloads/{app}",
        "container_root_folder": f"/data/{chosen_disk}/{sub_root}/{category}",
        "host_target_dir": str(host_root / "Media" / sub_root / category),
        "needs_consolidation": needs_consolidation,
    }
