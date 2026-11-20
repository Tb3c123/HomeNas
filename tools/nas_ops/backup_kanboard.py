"""03:00 Daily Hot SQLite Backup for Kanboard with 7-Day Rotation."""

import pathlib
import sqlite3
import time


def backup_kanboard_sqlite(
    source_db: pathlib.Path,
    backup_dir: pathlib.Path,
    keep_copies: int = 7,
    stamp: str | None = None,
) -> pathlib.Path:
    if not source_db.exists():
        raise FileNotFoundError(f"Kanboard DB not found: {source_db}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = stamp or time.strftime("%Y%m%d-%H%M%S")
    dest_db = backup_dir / f"kanboard-{ts}.sqlite"

    src_uri = f"file:{source_db}?mode=ro&immutable=1"
    with sqlite3.connect(src_uri, uri=True) as src_conn:
        with sqlite3.connect(str(dest_db)) as dst_conn:
            src_conn.backup(dst_conn)

    if not dest_db.exists() or dest_db.stat().st_size == 0:
        raise RuntimeError("Kanboard backup produced empty file!")

    backups = sorted(backup_dir.glob("kanboard-*.sqlite"))
    for old_backup in backups[:-keep_copies]:
        old_backup.unlink(missing_ok=True)
    return dest_db
