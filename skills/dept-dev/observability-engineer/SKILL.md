---
name: observability-engineer
description: Instrument applications with structured JSON logging, RED/USE metrics, distributed tracing, and actionable SLO alerts without alert fatigue.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Observability Engineer (Logs, Metrics & Traces)

## Use This Skill When
- Adding structured logging, health/metrics endpoints, Prometheus/Grafana monitoring, OpenTelemetry tracing, or alerting rules.

## Three Pillars Discipline
1. **Structured Logs (JSON):** Emit machine-parseable logs with `timestamp`, `level`, `service`, `request_id`/`trace_id`, and `event`; scrub all tokens, passwords, and PII before logging.
2. **RED & USE Metrics:** Track **R**ate, **E**rrors, **D**uration (p50/p95/p99) for services, and **U**tilization, **S**aturation, **E**rrors for infrastructure (CPU, RAM, disk, temp). Avoid high-cardinality labels (never put `user_id` or raw URLs in Prometheus labels).
3. **Trace Propagation:** Propagate `traceparent` / `X-Request-ID` across HTTP, queues, and background tasks so failures correlate end-to-end.
4. **Actionable Alerting (Zero Fatigue):** Alert on user-impacting symptoms or critical hardware thresholds (with hysteresis/cooldown), never noisy transient blips; attach runbook links to every alert.
