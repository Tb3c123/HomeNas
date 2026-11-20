# 11. Backlog (Do Later — v1.2+): Security Hardening Roadmap

Danh sách nâng cấp bảo mật đã kiểm toán (Red-Team Threat Model), lưu backlog để triển khai ở các phiên bản sau khi hệ thống vận hành ổn định:

## 1. Cô lập Hạ tầng & Quyền truy cập (`antigravity-cli`)
- **Không expose cổng quản trị (`:7681`, `:8085`, `:9000`)** ra Internet qua Cloudflare Tunnel nếu không bọc **Cloudflare Zero Trust (Email OTP)**; ưu tiên truy cập từ xa qua **Tailscale / WireGuard VPN**.
- **Đặt mật khẩu `ttyd` (`-c user:pass`)** cho cổng `:7681` trên mạng LAN.
- **Gỡ `/var/run/docker.sock`** khỏi container `antigravity-cli`, chuyển sang dùng `DOCKER_HOST=tcp://docker-proxy:2375` (`DELETE=0`, `VOLUMES=0`, `EXEC=0`) để chặn leo thang quyền root.

## 2. Nâng cấp `pre_tool_guard.py` (0-Token Intrusion Prevention)
- Bổ sung chặn cứng lệnh đọc/rò rỉ `.env` (`cat/grep/curl ... .env`), lệnh phá đĩa (`mkfs`, `dd of=/dev`, `shred`) và reverse shell (`curl | sh`, `/dev/tcp`).
- Bổ sung **Telegram Intrusion Alert (`🛡️ [SECURITY ALERT]`)**: tự động bắn cảnh báo ngay khi có lệnh bị hook chặn.

## 3. Bảo vệ Tài khoản & Xác thực Con người
- Bật **2FA (Passkey / Authenticator)** cho tài khoản Google chạy `agy`; khóa FaceID/vân tay trên điện thoại.
- Xoay vòng định kỳ `TELEGRAM_BOT_TOKEN` (`/revoke`) và mật khẩu Kanboard `:8085`.
- *(Tùy chọn)* Bổ sung **Mã xác nhận bí mật (PO Passphrase)** trong `AGENTS.md` cho mọi thao tác xóa/sửa hệ thống.
- Nếu mở Telegram Bot nhận lệnh 2 chiều: khóa cứng chỉ chấp nhận duy nhất `TELEGRAM_CHAT_ID=8608642317`.
