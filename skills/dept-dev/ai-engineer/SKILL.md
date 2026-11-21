---
name: ai-engineer
description: Architect production LLM applications with structured outputs, tool calling, streaming UX, cost/latency budgets, and ToS-compliant provider adapters.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# AI Engineer (Production LLM Systems)

## Use This Skill When
- Integrating LLM APIs, ACP/MCP agents, tool-calling loops, streaming responses, or multi-provider model adapters.

## Production Architecture Rules
1. **Provider-Agnostic Adapter Layer:** Isolate provider SDKs behind a clean interface (`complete`, `stream`, `embed`) with explicit timeouts, rate-limit backoff, and fallback routing (API-key mode).
2. **Structured Outputs Over Regex:** Enforce JSON Schema / Pydantic / Zod validation on model outputs; retry with schema feedback on parse errors.
3. **Context & Token Budgeting:** Cap history length, summarize/compact old turns, and log input/output token counts + estimated cost per request.
4. **ToS & Auth Compliance:** Never extract or proxy personal consumer OAuth tokens in third-party routers; separate interactive thin-client PTY/ACP sessions from programmatic API-key routes.
5. **Graceful Degradation:** Stream tokens to UI for low perceived latency, support user cancellation (`AbortController`), and handle 429/5xx cleanly.
