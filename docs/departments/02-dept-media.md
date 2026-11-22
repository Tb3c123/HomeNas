# Department 02: `dept-media` (Jellyfin, Mirror 1:1 Dual-Disk, Sub-First & Sequential Queue)

## 1. Kiến trúc Lưu trữ Mirror 1:1 (`disk1` & `disk2`) & Cân bằng Dung lượng

Cả 2 ổ 10TB trong dock Acasis (`disk1` WD Gold & `disk2` WD Purple Pro) sử dụng **cấu trúc thư mục giống hệt nhau 1:1** (đã loại bỏ `4K_UHD`):

```text
/mnt/disk{1,2}/Media/
├── .downloads/
│   ├── radarr/                 # Staging tải Movies của riêng ổ đó (Atomic Hardlink)
│   └── sonarr/                 # Staging tải TVShows của riêng ổ đó (Atomic Hardlink)
├── Movies/
│   ├── Cinema/                 # Phim lẻ Âu Mỹ / Quốc tế
│   ├── Asian/                  # Phim lẻ Châu Á (Hàn, Trung, Nhật, Thái...)
│   └── Vietnamese/             # Phim lẻ Việt Nam
└── TVShows/
    ├── International/          # Phim bộ Âu Mỹ / Quốc tế
    ├── K-Drama/                # Phim bộ Hàn Quốc
    ├── C-Drama/                # Phim bộ Trung Quốc
    ├── Vietnamese/             # Phim bộ Việt Nam
    └── Reality_Shows/          # Show thực tế
```

### Quy tắc Chọn Ổ Đích (Disk Placement Policy)
- **Phim lẻ (Movies):** Tự động chọn ổ (`disk1` hoặc `disk2`) có **dung lượng trống lớn hơn** tại thời điểm thêm phim → tải vào `.downloads/radarr` của ổ đó → Hardlink 0-copy vào `Movies/<Category>` trên cùng ổ.
- **Phim bộ (TVShows — All-Seasons-One-Disk):**
  - *Series mới:* Chọn ổ có dung lượng trống lớn hơn.
  - *Season/Tập mới của Series đã có:* **Bắt buộc kiểm tra và dồn toàn bộ các Season về đúng 1 ổ duy nhất** đang chứa series đó, tuyệt đối không để lưu lạc 2 ổ.
- **Tích hợp Container:** Cả `radarr`, `sonarr`, `bazarr`, `qbittorrent` đều mount đủ `/data/disk1` và `/data/disk2` (category `radarr-disk1/disk2`, `sonarr-disk1/disk2`); `jellyfin` đã mount `/media/disk1` & `/media/disk2` nên tự gộp thư viện liền mạch.

## 2. Chính sách Chất lượng, Sub Việt & Tải Tuần tự

1. **Ưu tiên #1 — Sub Việt chuẩn (Bắt buộc):** Tìm Sub Việt chuẩn trước (Bazarr / SubDL / OpenSubtitles), chốt Top 2–3 cặp `[Sub Việt ↔ Release Group khớp]` để tránh lệch timing.
2. **Ưu tiên #2 — Chọn bản Chất lượng/Dung lượng tốt nhất (KHÔNG khóa cứng trần GB):**
   - **Phim lẻ (Movies):** Ưu tiên **2K (1440p) hoặc 4K (2160p)** có **tỷ lệ chất lượng/dung lượng tối ưu nhất** trong các bản khớp Sub Việt (chấp nhận linh hoạt các bản 11–12GB+ nếu đó là bản hợp lý nhất, không khóa cứng gây bỏ sót phim hay; chỉ tránh Remux quá cồng kềnh khi đã có bản nén đẹp nhẹ hơn nhiều). Nếu không có bản 2K/4K hợp lý khớp sub → chọn **1080p chất lượng tốt**.
   - **Phim bộ (TVShows):** Cho phép **1080p chất lượng tốt nhất** (ưu tiên `WEB-DL`, `BluRay`, `WEBRip` sạch; **hạn chế/lọc bỏ `TVRip`, `HDTV`**) khớp Sub Việt chuẩn.
3. **Ưu tiên #3 — Chế độ Tải Tuần tự (`MAX_ACTIVE_DOWNLOADS = 1`):**
   - Chỉ tải **từng phim một**; hoàn tất phim hiện tại (tải xong → Hardlink → gắn `.vi.srt` → Jellyfin nhận diện) mới tự động kích hoạt phim tiếp theo trong hàng đợi.
   - Tối ưu băng thông, đo chính xác ETA và chỉ ghi lên 1 ổ HDD tại 1 thời điểm giúp dock Acasis mát hơn.

## 3. Theo dõi Tốc độ 20–30% ETA & Auto-Fallback (Viết mới 100% — 0 Token)

- **Chính sách mã nguồn:** Loại bỏ toàn bộ script cũ tại `/mnt/storage/Workspace/Archive_Scripts_Memory/`; xây mới hoàn toàn module `media_watcher.py` trong container `homenas-watchdog`.
- **Fire-and-Forget:** `dept-media` đẩy cặp `#1` vào hàng đợi, lưu cặp dự phòng `#2, #3` vào Kanboard, đăng ký theo dõi cho `media_watcher.py` rồi **đóng phiên `agy` ngay** (kèm Inline Receipt 1–2 dòng).
- **Chu kỳ kiểm tra động:** $\Delta t = \text{clamp}(0.25 \times \text{ETA}, \min=3\text{ phút}, \max=20\text{ phút})$.
- **Liên kết chéo nhiệt độ (`dept-nas-ops`):** Nếu `qbittorrent` đang tạm dừng do `sda`/`sdb` ≥ 65°C → giữ nguyên chờ hạ nhiệt, không hủy nhầm.
- **Auto-Fallback khi tải chậm/stalled:** Nếu tốc độ `< 500 KB/s`, `stalled` hoặc `ETA > 2x` liên tiếp 2 mốc → xóa bản kẹt, nạp cặp dự phòng `#2` khớp Sub Việt + bắn Telegram. Hết `#2, #3` → đẩy thẻ Kanboard `Waiting Review` (`blocked`).

## 4. Playbook, AGY Skills & Phân quyền (`skills/dept-media/`)
- **Skills (Lazy Load):** `sub-first-download/SKILL.md`.
- **Tự chạy (Fire-and-Forget):** Tìm sub & chọn bản Best-Value (không khóa cứng GB), chọn ổ cân bằng `disk1`/`disk2` (giữ nguyên ổ cho TVShows), đẩy hàng đợi tuần tự 1-phim-1-lượt, canh 20–30% ETA, Auto-Fallback `#2/#3`, và tải trực tiếp link Fshare/Drive/TeraBox qua 5 chốt an toàn.
- **Bắt buộc PO duyệt (`needs-approval`):** Xóa phim đã nằm trong thư viện `Movies/` hoặc `TVShows/`, dọn thư mục cũ, hoặc tải bản không có Sub Việt chuẩn.

## 5. Luồng Tải Trực Tiếp Fshare / Google Drive / TeraBox (Phương Án C — Không Cần API Fshare)
Do Fshare đã dừng cấp API Developer cho cá nhân, `tools/media_ops/direct_fetcher.py` vận hành theo **Phương án C (Hybrid Direct-CDN + Google Drive + Web Cookie)** với 5 chốt bảo vệ:
1. **Google Drive (`drive.google.com/file/d/<ID>`):** Tự động trích xuất `file_id` và tải thẳng qua `drive.usercontent.google.com` (`confirm=t`) — không cần bấm trình duyệt.
2. **Fshare & TeraBox qua Direct-CDN Link (Khuyên dùng — Bền vững 100%):** PO bấm tải trên trình duyệt (cùng mạng Wi-Fi/LAN với NAS) → Tạm dừng → Copy địa chỉ link tải thật (`https://download*.fshare.vn/dl/...` hoặc CDN TeraBox) gửi cho `Elena`. NAS tiếp nhận và kéo max tốc độ VIP về ổ đích (`disk1`/`disk2`).
3. **Fshare & TeraBox qua Web Cookie (Tùy chọn):** Nếu cấu hình `FSHARE_COOKIE` / `TERABOX_COOKIE` trong `platform/.env`, hệ thống tự lấy CSRF token từ web session để giải link `fshare.vn/file/<CODE>`.
4. **5 Chốt An Toàn Cứng:** Chặn đuôi file độc hại (`.exe`, `.sh`, `.apk`...), kiểm tra `thermal_paused` của 2 ổ Acasis trước khi ghi, tự cân bằng `disk1`/`disk2` theo chuẩn thư mục Jellyfin, và tải với hậu tố `.part` (`aria2c` / `curl -C -` có resume).
