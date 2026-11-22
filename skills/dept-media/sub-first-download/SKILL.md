---
name: sub-first-download
description: Sub-First Vietnamese subtitle matching, Option C Direct Fetch (Fshare/Google Drive/TeraBox), 1:1 dual-disk routing, and sequential queue.
---

# Media & Download: Sub-First & Option C Direct-Link Router (`Elena`)

## 1. Luồng A — Tìm & Tải Phim Tự Động (Torrent / Arr Stack)
1. Tìm Sub Việt chuẩn trước (Bazarr / SubDL / OpenSubtitles) và lấy danh sách release group khớp.
2. Chấm điểm qua `tools.media_ops.sub_first_matcher`:
   - **Movies:** Ưu tiên 2K/4K có tỷ lệ chất lượng/dung lượng tốt nhất (linh hoạt 11–12GB+ nếu encode đẹp), fallback 1080p.
   - **TVShows:** Ưu tiên 1080p sạch (`WEB-DL`/`BluRay`/`WEBRip`), loại bỏ `TVRip`/`HDTV`.
   - Nếu không có Sub Việt khớp: chuyển thẻ sang `Waiting Review` (`needs-approval`), in `[⚠️ REVIEW]` và dừng.
3. Chọn ổ đích qua `tools.media_ops.disk_balancer` (Movies theo ổ trống nhiều hơn; TVShows gom toàn bộ Season về 1 ổ).
4. Đẩy ứng viên `#1` (lưu `#2, #3` dự phòng) vào `SequentialMediaWatcher` (`MAX_ACTIVE_DOWNLOADS=1`, kiểm tra mỗi 25% ETA).

## 2. Luồng B — Tải Trực Tiếp Link Fshare / Google Drive / TeraBox (Phương án C)
Khi PO gửi link trực tiếp (`drive.google.com`, `download*.fshare.vn`, `fshare.vn/file/...`, `terabox.com`):
1. **Bước 1 — Kiểm tra An toàn & Lập kế hoạch (Dry-Run):**
   `docker exec homenas-watchdog python3 -m tools.media_ops.inspector_cli direct-fetch --url "<URL>" --title "<Tên Phim (Năm)>" --type <movie|tv> --category <Cinema|Asian|Vietnamese|K-Drama...>`
   - Hệ thống tự động chặn đuôi độc hại (`.exe`, `.sh`, `.apk`), kiểm tra nhiệt độ 2 ổ Acasis (`THERMAL_WAIT` nếu ≥ 50°C), và chọn ổ `disk1`/`disk2`.
   - Nếu trả về `NEEDS_BROWSER_DIRECT_LINK` (khi PO gửi link trang `fshare.vn/file/...` mà chưa có `FSHARE_COOKIE`): Hướng dẫn PO bấm tải trên trình duyệt (cùng mạng Wi-Fi/LAN với NAS), tạm dừng và copy link tải thật `https://download*.fshare.vn/dl/...` dán lại cho Elena.
2. **Bước 2 — Thực thi Tải Tuần Tự (Có `.part` & Resume):**
   Khi `status == "PLANNED"`, chạy lại lệnh trên kèm cờ `--execute` để tải thẳng về thư mục chuẩn Jellyfin, kiểm tra Sub Việt (Bazarr) và xuất Receipt + Return Prompt về `Main`.
