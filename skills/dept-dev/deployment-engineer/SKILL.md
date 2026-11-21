---
name: deployment-engineer
description: Design reproducible Docker builds, CI/CD pipelines, healthchecks, safe zero-downtime rollouts, and verified rollback procedures.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Deployment Engineer (Docker, CI/CD & Rollback)

## Use This Skill When
- Writing Dockerfiles, `docker-compose.yml`, GitHub Actions CI/CD workflows, or release scripts.
- Hardening service startup, healthchecks, log rotation, and rollback paths.

## Container & Build Best Practices
1. **Minimal Reproducible Images:** Use pinned base image versions (e.g., `python:3.12-slim`, `node:22-alpine`), multi-stage builds, and `.dockerignore` to exclude `.git`, caches, and secrets.
2. **Layer Caching & Hygiene:** Copy lockfiles (`requirements.txt`, `package-lock.json`) and install dependencies before copying source code; clean package caches in the same `RUN` layer.
3. **Runtime Resilience:** Define explicit `healthcheck`, `restart: unless-stopped`, memory/log limits (`max-size`, `max-file`), and read-only mounts (`:ro`) where possible.

## CI/CD & Release Discipline
1. **Automated Quality Gates:** Every PR/push runs lint, line-cap audit, unit tests, and build verification before deploy.
2. **Environment Parity:** Separate code from config (`.env.example` committed, real `.env` gitignored); validate required env vars at startup (fail fast).
3. **Safe Rollout & Rollback:** Tag releases semantically (`vX.Y.Z`), verify healthcheck post-deploy, and document a 1-command rollback to the previous known-good image/tag.
4. **Safety First:** Never stop/remove protected core infrastructure containers or run unverified destructive migrations without backup.
