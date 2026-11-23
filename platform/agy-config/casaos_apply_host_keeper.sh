#!/usr/bin/env bash
# Strict Whitelist Host-Side CasaOS Native App Apply Keeper (runs on Debian host, NOT in container).
# Watches /mnt/disk1/Workspace/HomeNas/.state/casaos_apply_req.json and executes ONLY:
#   casaos-cli app-management apply <slug> --file=/mnt/disk1/Workspace/<dir>/casaos-compose.yml

set -euo pipefail

STATE_DIR="/mnt/disk1/Workspace/HomeNas/.state"
REQ_FILE="${STATE_DIR}/casaos_apply_req.json"
RES_FILE="${STATE_DIR}/casaos_apply_result.txt"
WS_PREFIX="/mnt/disk1/Workspace/"

mkdir -p "${STATE_DIR}"
echo "[casaos_apply_host_keeper] Watching ${REQ_FILE}..."

while true; do
  if [ -f "${REQ_FILE}" ]; then
    ts="$(date '+%Y-%m-%d %H:%M:%S')"
    parsed="$(python3 -c '
import json, pathlib, re, sys
try:
    d = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    app = str(d.get("app", ""))
    fp = pathlib.Path(str(d.get("file", ""))).resolve()
    ws = pathlib.Path(sys.argv[2]).resolve()
    assert re.match(r"^[a-z0-9][a-z0-9-]{1,62}$", app)
    fp.relative_to(ws)
    assert fp.name == "casaos-compose.yml" and fp.is_file()
    print(f"{app}|{fp}")
except Exception as e:
    print(f"ERR|{e}")
' "${REQ_FILE}" "${WS_PREFIX}")"
    rm -f "${REQ_FILE}"

    app="${parsed%%|*}"
    fpath="${parsed#*|}"
    if [ "${app}" = "ERR" ]; then
      echo "[${ts}] REJECTED: ${fpath}" > "${RES_FILE}"
    else
      if output="$(casaos-cli app-management apply "${app}" --file="${fpath}" 2>&1)"; then
        echo "[${ts}] OK app=${app} file=${fpath} :: ${output}" > "${RES_FILE}"
      else
        echo "[${ts}] FAILED app=${app} file=${fpath} :: ${output}" > "${RES_FILE}"
      fi
    fi
  fi
  sleep 3
done
