---
name: ai-safety-guardrails-alignment
description: Harden LLM and agentic systems against prompt injection, jailbreaks, tool-call abuse, PII leaks, and ungrounded hallucinations.
metadata:
  model: inherit
  source: Orchestra-Research/AI-Research-SKILLs (MIT)
---

# AI Safety, Guardrails & Alignment

## Use This Skill When
- Deploying LLM features or tool-using agents that ingest untrusted user input, web pages, files, or emails.
- Adding input/output guardrails, PII redaction, groundedness checks, or human-in-the-loop approvals.
- Red-teaming an AI workflow before production release.

## Core Defense-in-Depth Layers
1. **Separate Instructions From Untrusted Data:** Treat all retrieved documents, web scrapes, file contents, and tool outputs as **untrusted data**, wrapped in clear delimiters—never trust an LLM alone to resist indirect prompt injection.
2. **Least-Privilege Tool Execution (Critical):**
   - Enforce permissions, path allowlists, read-only DB modes, and rate limits **in deterministic application code**, not just in the system prompt.
   - Require explicit human confirmation before destructive, financial, external-network, or privilege-escalating actions.
3. **Input & Output Guardrails:**
   - Validate structured outputs against strict schemas (`Pydantic`/`Zod`) and reject unexpected tool arguments or shell metacharacters.
   - Scan and redact secrets/PII (API keys, tokens, credentials) before logging or sending context to external model providers.
4. **Anti-Hallucination & Groundedness:** Require explicit inline citations to retrieved chunk IDs, allow an explicit `"I don't have enough evidence"` abstention path, and verify factual/numeric claims programmatically where possible.
5. **Adversarial Red-Teaming Suite:** Maintain automated regression tests for direct/indirect prompt injection, system-prompt exfiltration, unauthorized tool invocation, and refusal calibration.

## Delivery Checklist
- Map every untrusted input channel and verify deterministic code-level authorization on every tool.
- Run adversarial prompt-injection test cases and verify zero secret/PII leakage in logs.
