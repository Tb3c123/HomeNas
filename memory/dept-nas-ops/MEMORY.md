# Tier 2 Memory: `dept-nas-ops` (Max 100 Lines)

## Pinned Facts
- [PINNED] Dual 10TB HDDs (`sda` WD Gold `/mnt/disk1`, `sdb` WD Purple Pro `/mnt/disk2`) run in Acasis USB dock; poll with `smartctl -n standby -d sat` every 3 minutes.
- [PINNED] HDD `< 60C` normal; `60-64C > 15m` warning; `>= 65C` or `>= 60C > 45m` or `(HDD >= 60C + CPU overload)` triggers immediate pause of `STOPPABLE_CONTAINERS`.
- [PINNED] Never stop `adguard-home` (LAN DNS) or `kanboard`.

## Learned Observations
- [2026-11-19] Initialized RAM-buffered thermal logging (`/tmp/thermal_samples_today.jsonl`) with single daily SSD flush at 23:55.
