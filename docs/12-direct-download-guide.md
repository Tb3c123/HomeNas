# Sổ Tay Tải Phim Trực Tiếp: Google Drive, Fshare & TeraBox (`Elena - dept-media`)

> **Phương án C (AI-Controlled Direct Fetch — `v1.6.1`):** Mọi link tải đều đi qua 5 chốt bảo vệ của `Elena (dept-media)`: chặn file độc hại (`.exe`, `.sh`...), kiểm tra nhiệt độ 2 ổ Acasis (`< 50°C`), tự chọn ổ `disk1`/`disk2` còn trống nhiều hơn, tải `.part` có resume và đặt đúng cấu trúc thư mục Jellyfin.

---

## 1. Tải Phim từ Google Drive (Dán thẳng link chia sẻ)
Không cần bấm tải trên trình duyệt. Chỉ cần copy link chia sẻ (`https://drive.google.com/file/d/.../view`) và dán vào khung **`[Dept-Media]`**:

### Mẫu 1A — Phim Lẻ (`Cinema` | `Asian` | `Vietnamese`)
```text
Elena, kiểm tra an toàn và tải giúp tôi phim lẻ "Dune Part Two (2024)" (thể loại Cinema) từ link Google Drive này:
https://drive.google.com/file/d/DÁN_MÃ_LINK_DRIVE_VÀO_ĐÂY/view
```

### Mẫu 1B — Phim Bộ (`International` | `K-Drama` | `C-Drama` | `Vietnamese` | `Reality_Shows`)
```text
Elena, kiểm tra an toàn và tải giúp tôi phim bộ "Moving (2023)" Season 1 - Tập 01 (thể loại K-Drama, đặt tên file Moving.S01E01.mkv) từ link này:
https://drive.google.com/file/d/DÁN_MÃ_LINK_DRIVE_VÀO_ĐÂY/view
```

---

## 2. Tải Phim từ Fshare.vn & TeraBox (Max Speed VIP — Không cần API)
Do Fshare đã đóng API Developer cá nhân, cách bền vững 100% (ăn trọn tốc độ VIP, không lo Captcha) là **lấy Direct-CDN Link từ trình duyệt cùng mạng Wi-Fi/LAN với NAS trong 5 giây**:

### Thao tác 3 bước (5 giây trên máy tính / điện thoại cùng mạng Wi-Fi với NAS):
1. Mở link `fshare.vn/file/...` (hoặc `terabox.com/s/...`) trên trình duyệt đã đăng nhập tài khoản VIP → Bấm **"Tải xuống / Download"**.
2. Khi trình duyệt vừa bắt đầu tải file (mở mục **Downloads** `Ctrl+J` trên máy tính hoặc danh sách tải trên điện thoại):
   - Bấm **Tạm dừng (Pause)** để máy tính/điện thoại không phải tải.
   - Chuột phải (hoặc chạm giữ) vào file vừa tạm dừng → Chọn **"Sao chép địa chỉ liên kết tải xuống" (Copy Download Link)** (`https://download*.fshare.vn/dl/...` hoặc `https://data.terabox.com/...`).
3. Dán link tải thật đó vào khung **`[Dept-Media]`** theo mẫu:

```text
Elena, kiểm tra an toàn và tải giúp tôi phim "Mai (2024)" (Phim lẻ - thể loại Vietnamese) từ direct-link này:
https://download802.fshare.vn/dl/DÁN_LINK_VỪA_COPY_VÀO_ĐÂY/Mai.2024.2160p.mkv
```
*(Sau khi gửi cho Elena, bạn có thể tắt máy tính/điện thoại ngay — NAS tự tải ngầm về `disk1`/`disk2` và đưa thẳng lên Jellyfin).*

---

## 3. Tùy chọn Nâng cao: Gắn Web Cookie để dán thẳng link `fshare.vn/file/...`
Nếu muốn dán trực tiếp link trang `https://www.fshare.vn/file/ABCDEF...` mà không cần bấm tải trên trình duyệt:
- Copy chuỗi Cookie đăng nhập Fshare từ trình duyệt (`F12` → `Network` → `Cookie`) và nhắn vào khung **`[Main]`**:
```text
Hãy cập nhật biến FSHARE_COOKIE="DÁN_COOKIE_VÀO_ĐÂY" vào tệp platform/.env và khởi động lại homenas-watchdog.
```
- Khi Cookie còn hạn, `Elena` tự lấy CSRF token giải link tự động; khi Cookie hết hạn, `Elena` sẽ nhắc bạn dùng Mục 2.

---

## 4. Bảng Thể Loại (`--category`) Chuẩn Jellyfin trên `disk1` & `disk2`
- **Phim lẻ (`--type movie`):** `Cinema` (Âu Mỹ/Quốc tế), `Asian` (Hàn/Trung/Nhật/Thái), `Vietnamese` (Việt Nam).
- **Phim bộ (`--type tv`):** `International`, `K-Drama`, `C-Drama`, `Vietnamese`, `Reality_Shows`.
