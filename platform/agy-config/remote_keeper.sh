#!/usr/bin/env bash
# Zero-Privilege Flag-File Keeper for Antigravity CLI Remote Control (home-nas)
# Runs inside antigravity-cli container (e.g. inside tmux). Only executes ONE fixed command.

set -u

STATE_DIR="/mnt/disk1/Workspace/HomeNas/.state"
FLAG_FILE="${STATE_DIR}/reconnect_remote.flag"
STATUS_FILE="${STATE_DIR}/remote_status.txt"
SESSION_NAME="home-nas"

mkdir -p "${STATE_DIR}"

start_remote_control() {
  local reason="$1"
  local ts
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  pkill -f "agy remote-control" 2>/dev/null || true
  sleep 1
  nohup agy remote-control start --name "${SESSION_NAME}" > /tmp/agy_remote.log 2>&1 &
  sleep 4
  if pgrep -f "remote-control" > /dev/null 2>&1; then
    local url
    url="$(grep -Eo 'https://[^[:space:]]+' /tmp/agy_remote.log | tail -n 1 || true)"
    echo "[${ts}] ONLINE (${reason}) name=${SESSION_NAME} ${url}" > "${STATUS_FILE}"
  else
    local err
    err="$(tail -n 2 /tmp/agy_remote.log 2>/dev/null | tr '\n' ' ')"
    echo "[${ts}] FAILED (${reason}): ${err}" > "${STATUS_FILE}"
  fi
}

echo "[remote_keeper] Watching ${FLAG_FILE} & keeping '${SESSION_NAME}' alive..."
tick=0
while true; do
  if [ -f "${FLAG_FILE}" ]; then
    rm -f "${FLAG_FILE}"
    start_remote_control "telegram-/reconnect"
    tick=0
  elif [ $((tick % 12)) -eq 0 ]; then
    if ! pgrep -f "remote-control" > /dev/null 2>&1; then
      start_remote_control "auto-recovery"
    fi
  fi
  tick=$((tick + 1))
  sleep 5
done
