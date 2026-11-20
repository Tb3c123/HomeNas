# Tier 1: Product Owner Profile & Immutable Rules (USER.md)

## 1. Hardware & Platform Context
- **Host:** Morefine N6 (Intel N200 4C, 16GB RAM, 256GB NVMe SSD `/`, Debian + CasaOS).
- **Storage:** 2x10TB HDD via Acasis USB Dock (`disk1` WD Gold `/mnt/disk1`, `disk2` WD Purple Pro `/mnt/disk2`).
- **Protected Containers (NEVER stop/pause/rm):** `adguard-home`, `portainer`, `casaos`, `kanboard`, `homenas-watchdog`, `antigravity-cli`.

## 2. Mandatory Operating Rules
- **ToS & Quota:** 100% Antigravity ToS-safe; use Fire-and-Forget + Inline Receipt (`1-2 lines`) + Unread Digest.
- **Low-Wear Storage:** Minimize SSD writes (use `/tmp` RAM for caches & daily thermal buffer; single flush at 23:55). Respect HDD `standby`.
- **Media Preferences:** Sub-First (Vietnamese subtitle matched to release group is mandatory). Movies: 2K/4K best-value quality/size (no rigid GB cap), fallback 1080p. TVShows: 1080p clean (`WEB-DL`/`BluRay`), no `TVRip`/`HDTV`, all seasons on 1 disk. Sequential download (`MAX_ACTIVE_DOWNLOADS=1`).
- **Project-Wide Line Cap:** Every file in any project MUST be `<= 150 lines` (except auto-generated lockfiles).
