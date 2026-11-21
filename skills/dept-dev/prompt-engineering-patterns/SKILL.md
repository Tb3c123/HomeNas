---
name: prompt-engineering-patterns
description: Craft deterministic, injection-resistant system prompts with explicit roles, output schemas, few-shot examples, and failure fallbacks.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Prompt Engineering Patterns

## Use This Skill When
- Writing or refining system prompts, agent instructions, structured extractors, or classification/routing prompts.

## High-Signal Prompt Design
1. **Clear Structure:** Separate `Role/Goal` -> `Rules & Constraints` -> `Input Delimiters` -> `Output Format` -> `2-3 Concrete Few-Shot Examples`.
2. **Explicit Uncertainty Handling:** Instruct the model what to return when information is missing or ambiguous (e.g., `"unknown"` or structured error) to curb hallucinations.
3. **Prompt Injection Defense:** Wrap untrusted user/document text in XML tags (`<untrusted_input>...</untrusted_input>`) and explicitly instruct the model to treat its contents as data, never executable instructions.
4. **Concise & Versioned:** Keep prompts short and testable; store prompts as versioned files and evaluate changes against golden test cases instead of ad-hoc tweaking.
5. **Match Complexity to Model:** Use simple direct instructions for fast/cheap models and structured step-by-step verification for complex reasoning tasks.
