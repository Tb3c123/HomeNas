---
name: sub-first-download
description: Sub-First Vietnamese subtitle matching, flexible 2K/4K Movie & 1080p TV selection, 1:1 dual-disk routing, and sequential queue submission.
---

# Media & Download: Sub-First & Dual-Disk Router Skill

## 1. Execution Steps (Fire-and-Forget)
1. Search verified Vietnamese subtitles first (Bazarr / SubDL / OpenSubtitles) and extract matching release groups.
2. Score releases via `tools.media_ops.sub_first_matcher`:
   - **Movies:** Prioritize 2K/4K best-value quality/size (no rigid GB cap; 11-12GB+ allowed if best encode), fallback 1080p.
   - **TVShows:** Prioritize 1080p clean (`WEB-DL`/`BluRay`/`WEBRip`), exclude `TVRip`/`HDTV`.
   - If 0 matched Vietnamese subtitles exist: move card to `Waiting Review` (`needs-approval`), print `[⚠️ REVIEW]` receipt, and stop.
3. Select target disk via `tools.media_ops.disk_balancer`:
   - Balance Movies by free space (`disk1` vs `disk2`); pin all seasons of a TVShow to 1 disk.
4. Enqueue candidate `#1` (and save fallbacks `#2, #3`) into `SequentialMediaWatcher` (`MAX_ACTIVE_DOWNLOADS=1`, check every 25% ETA), print `[⏳ QUEUED]` receipt, and close session immediately.
