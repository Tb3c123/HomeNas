# 06. Technical Specifications (Infra, Config & API Contracts)

## 1. Hạ tầng Docker Stack (`agy-platform/docker-compose.yml`)

| Service | Image / Base | Vai trò & Tài nguyên | Volumes & Network |
| :--- | :--- | :--- | :--- |
| `kanboard` | `kanboard/kanboard:latest` | Kanban SQLite (~40MB RAM), Web UI (port LAN `8085:80`) + JSON-RPC endpoint `/jsonrpc.php`. | Mount `./data/kanboard/data` & `plugins`; network `agy-net`. |
| `docker-proxy` *(Khuyên dùng)* | `tecnativa/docker-socket-proxy` | Proxy giới hạn quyền đọc Docker API cho `dept-nas-ops` (chỉ bật `CONTAINERS=1`, `INFO=1`, chặn `POST/DELETE` mặc định). | Mount `/var/run/docker.sock:ro`; chỉ trong `agy-net`. |
| `agy-runtime` | Custom `debian:bookworm-slim` | Cài sẵn `agy` CLI, Python 3, Git, `kanboard-client`. Chạy interactive (`tty: true`, `stdin_open: true`). | Mount `./shared`, `./projects`, và volume lưu session `agy`; network `agy-net`. |

- **Biến môi trường lõi (`.env` tại tầng Platform):**
  - `KANBOARD_URL=http://kanboard/jsonrpc.php`
  - `KANBOARD_API_TOKEN=<token_tu_kanboard_settings>`
  - `DOCKER_HOST=tcp://docker-proxy:2375`

## 2. Schema Cấu hình Dự án (`projects/<name>/project.yaml`)

```yaml
project:
  id: homenas
  name: "HomeNas Operations"
  kanboard_project_id: 1
  columns: ["Backlog", "Ready", "In Progress", "Waiting Review", "Done"]

memory:
  user_profile: "/platform/shared/memory/USER.md"
  max_dept_lines: 100

departments:
  director:
    swimlane: "Director / General"
    skills_dir: "./skills/director"
    allowed_tools: ["kanboard-client"]
  dept-nas-ops:
    swimlane: "NAS Ops"
    memory_file: "./memory/dept-nas-ops/MEMORY.md"
    skills_dir: "./skills/dept-nas-ops"
    allowed_tools: ["kanboard-client", "nas-inspector"]
  dept-media:
    swimlane: "Media & Download"
    memory_file: "./memory/dept-media/MEMORY.md"
    skills_dir: "./skills/dept-media"
    allowed_tools: ["kanboard-client", "media-inspector"]
  dept-dev:
    swimlane: "Dev Studio"
    memory_file: "./memory/dept-dev/MEMORY.md"
    skills_dir: "./skills/dept-dev"
    allowed_tools: ["kanboard-client", "git", "gh"]
```

## 3. Đặc tả `kanboard-client` (Adapter Pattern — Python Stdlib)

Tách thành 4 module nhỏ (< 100 dòng/file) trong `shared/tools/kanboard-client/`:
- `rpc_client.py`: Gửi POST JSON-RPC 2.0 (Basic Auth `jsonrpc:<KANBOARD_API_TOKEN>`, timeout 5s).
- `formatter.py`: Nén response Kanboard thành text 1 dòng/task (Zero-Noise).
- `digest_state.py`: Đọc/ghi mốc timestamp `.state/last_digest_ts` theo từng `project_id`.
- `cli.py`: Parse 5 lệnh chuẩn:

| Lệnh CLI | JSON-RPC Method tương ứng | Output chuẩn (Zero-Noise) |
| :--- | :--- | :--- |
| `kb list --swimlane <name> --col Ready` | `getAllTasks` + lọc cục bộ | `#42 [Ready] [fire-and-forget] Kiểm tra SMART /dev/sda` |
| `kb create --swimlane <name> --title "..." --desc "..." --tags "..."` | `createTask` | `CREATED #45 [Ready] [NAS Ops]` |
| `kb move <task_id> --col <column>` | `moveTaskPosition` | `MOVED #45 -> In Progress` |
| `kb comment <task_id> --text "..."` | `createComment` | `COMMENTED #45 (3 lines)` |
| `kb digest --unread` | `getAllTasks` + lọc `date_modification > last_ts` | Danh sách task mới cập nhật (1 dòng/task) & cập nhật `last_ts` |

## 4. Đặc tả Tools phòng ban (Zero-Noise Contract)
- **`nas-inspector`:** Chỉ trả JSON/text rút gọn gồm: CPU %, RAM %, Disk usage %, nhiệt độ ổ cứng, và tối đa 30 dòng cuối của container bị lỗi (`status != running/healthy`).
- **`media-inspector`:** Chỉ trả số lượng task đang tải, tốc độ tổng, danh sách file lỗi/stalled và dung lượng trống thư mục media.
