#!/usr/bin/env bash
# Zero-Host-SSH Docker Compose Wrapper for antigravity-cli container.
set -euo pipefail

if docker compose version >/dev/null 2>&1; then
  exec docker compose "$@"
fi

exec docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /mnt/disk1/Workspace/HomeNas:/mnt/disk1/Workspace/HomeNas \
  -w /mnt/disk1/Workspace/HomeNas \
  docker:cli compose "$@"
