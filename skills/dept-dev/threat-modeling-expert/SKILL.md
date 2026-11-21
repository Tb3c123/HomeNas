---
name: threat-modeling-expert
description: Perform practical STRIDE threat modeling, trust-boundary mapping, and risk-ranked mitigation planning before building sensitive features.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Threat Modeling Expert (STRIDE)

## Use This Skill When
- Designing new network-exposed services, multi-CLI/subprocess runners, auth systems, or host/Docker integrations.

## Compact STRIDE Workflow
1. **Map Assets & Trust Boundaries:** Identify crown jewels (credentials, DB, host shell, Docker socket) and where untrusted input crosses into trusted execution.
2. **Evaluate STRIDE per Boundary:**
   - **S**poofing (identity forged?)
   - **T**ampering (data/config modified in transit or at rest?)
   - **R**epudiation (actions unlogged/unattributable?)
   - **I**nformation Disclosure (secrets/PII leaked in logs, errors, or mounts?)
   - **D**enial of Service (unbounded loops, disk fill, resource exhaustion?)
   - **E**levation of Privilege (container escape, shell injection, IDOR?)
3. **Prioritize & Mitigate:** Rank threats by `Impact x Likelihood`; implement concrete controls (least privilege, read-only mounts, allowlists, rate limits) and log deferred risks in a security backlog.
