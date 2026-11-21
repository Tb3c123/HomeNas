---
name: kubernetes-architect
description: Design production Kubernetes workloads with readiness/liveness probes, resource requests/limits, non-root security contexts, and GitOps rollouts.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Kubernetes Architect

## Use This Skill When
- Authoring Kubernetes manifests, Helm charts, NetworkPolicies, or scaling/rollout configs for containerized services.

## Production Workload Baseline
1. **Probes & Graceful Shutdown:** Define `startupProbe`, `readinessProbe`, and `livenessProbe`; handle `SIGTERM` and set `terminationGracePeriodSeconds` so in-flight requests drain cleanly.
2. **Resource Requests & Limits:** Always declare CPU/memory `requests` and memory `limits` to prevent OOM neighbor eviction and enable accurate scheduling/HPA.
3. **Hardened SecurityContext:** Run with `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, and drop `ALL` Linux capabilities.
4. **Config & Secrets Separation:** Store non-sensitive config in `ConfigMap`, sensitive values in external secret managers/sealed secrets (never raw base64 in Git).
5. **Declarative GitOps:** Keep manifests versioned in Git with PodDisruptionBudgets and rolling update `maxUnavailable: 0` for stateless services.
