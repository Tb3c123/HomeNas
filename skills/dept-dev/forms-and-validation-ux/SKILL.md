---
name: forms-and-validation-ux
description: Design frictionless single- and multi-step forms with timely inline validation, keyboard/autofill support, and zero lost user input.
metadata:
  model: inherit
  source: vercel-labs/agent-skills (Open)
---

# Forms & Validation UX

## Use This Skill When
- Building settings panels, onboarding flows, data-entry forms, or parameter editors.
- Designing validation feedback, multi-step wizards, or unsaved-changes protection.
- Auditing form abandonment, keyboard friction, or mobile input issues.

## Core Principles
1. **Reward Early, Punish Late (Validation Timing):**
   - Never show errors while the user is still typing for the first time.
   - Validate on `blur` or `submit`; once a field is invalid, re-validate on `change` so the error clears the instant the user fixes it.
2. **Never Lose User Input:** Preserve form values across failed submissions, network retries, and accidental navigation (warn on dirty unsaved state; disable submit only during active in-flight requests—keep button clickable to surface validation errors).
3. **Clear Labels & Input Ergonomics:**
   - Always use persistent visible `<label>` elements (never placeholder-only labels).
   - Set proper `type`, `inputMode`, and `autoComplete` attributes; support `Enter` submit and logical `Tab` order.
   - Mark optional fields (`(optional)`) when most are required, or required fields when most are optional.
4. **Actionable Error Placement:** Place inline errors directly beneath the offending input, linked via `aria-describedby` and `aria-invalid="true"`. On submit failure, focus the first invalid field and scroll it into view.
5. **Smart Defaults & Progressive Disclosure:** Pre-fill safe defaults, group complex settings into collapsible sections or clear steps, and show live formatting hints (e.g., units, character count) before submission.

## Delivery Checklist
- Verify full keyboard completion without touching a mouse.
- Confirm server-side validation errors map cleanly back to specific fields or a top alert banner.
- Test double-click submission protection (idempotent in-flight lock).
