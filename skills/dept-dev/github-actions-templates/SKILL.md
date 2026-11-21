---
name: github-actions-templates
description: Author fast, secure GitHub Actions CI/CD workflows with pinned actions, dependency caching, concurrency cancellation, and least-privilege permissions.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# GitHub Actions CI/CD Templates

## Use This Skill When
- Creating or optimizing `.github/workflows/*.yml` pipelines for lint, test, security scan, Docker build, or release automation.

## Secure & Fast Workflow Rules
1. **Least-Privilege `permissions:`:** Always set explicit top-level `permissions: { contents: read }` and elevate only in specific release jobs.
2. **Cancel Stale Runs:** Configure `concurrency: { group: "${{ github.workflow }}-${{ github.ref }}", cancel-in-progress: true }` on PR branches to save CI minutes.
3. **Dependency Caching & Timeouts:** Enable built-in cache (`actions/setup-python`, `actions/setup-node`, `Swatinem/rust-cache`) and set `timeout-minutes: 15` on every job.
4. **Prevent Script Injection:** Never interpolate untrusted PR titles/comments directly inside `run:` shell commands; pass them via `env:` variables.
5. **Pin Actions & Secrets:** Pin third-party actions to major tags or full commit SHAs; never echo secrets in logs.
