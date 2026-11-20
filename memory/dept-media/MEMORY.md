# Tier 2 Memory: `dept-media` (Max 100 Lines)

## Pinned Facts
- [PINNED] Both `/mnt/disk1/Media` and `/mnt/disk2/Media` use identical 1:1 folder structure (`Movies/{Cinema,Asian,Vietnamese}`, `TVShows/{International,K-Drama,C-Drama,Vietnamese,Reality_Shows}`, `.downloads/{radarr,sonarr}`). No `4K_UHD` folder.
- [PINNED] Movies balance across `disk1`/`disk2` by free space; TVShows pin all seasons of a series to a single disk.
- [PINNED] Sub-First rule: verify Vietnamese subtitle release match before downloading. Sequential queue (`MAX_ACTIVE_DOWNLOADS=1`), check speed every 25% ETA (clamp 3-20m).

## Learned Observations
- [2026-11-19] Always check `/tmp/homenas_thermal_state.json` (`thermal_paused`) before treating a 0 KB/s torrent as stalled.
