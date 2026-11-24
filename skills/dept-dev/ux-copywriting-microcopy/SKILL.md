---
name: ux-copywriting-microcopy
description: Write concise, action-oriented UI labels, empathetic error/empty states, and clear confirmation dialogs that reduce user hesitation.
metadata:
  model: inherit
  source: vercel-labs/agent-skills (Open) + pbakaus/impeccable (Apache-2.0)
---

# UX Copywriting & Microcopy

## Use This Skill When
- Writing or refining button labels, form helpers, tooltips, empty states, toasts, and error messages.
- Designing destructive confirmation modals or onboarding checklists.
- Localizing UI copy cleanly (e.g., natural Vietnamese or concise English) without robotic phrasing.

## Core Principles
1. **Verb + Object Buttons:** Replace vague `OK` / `Submit` / `Yes` with specific actions (`Save Changes`, `Delete Project`, `Run Simulation`). Keep labels to 1–3 words.
2. **Constructive Error Messages:** Every error must state **(a) what happened** in plain language and **(b) how to fix it**—never blame the user or dump raw stack traces/HTTP codes alone.
3. **Actionable Empty States:** Explain the value of the empty section in one sentence and provide a direct button or example to create the first item.
4. **Confirmation Dialogs That Prevent Mistakes:** State the exact consequence and scope (`Delete "Alpha" and its 12 records? This cannot be undone.`), and match the confirm button verb to the action (`Delete Project`, not `Confirm`).
5. **Scannable & Consistent Terminology:** Use one term per concept across the entire app (do not mix `Workspace`, `Project`, and `Board` for the same entity). Front-load key information in headings and tooltips.

## Delivery Checklist
- Audit all buttons, modal titles, and destructive prompts for exact verb clarity.
- Verify error, loading, and empty messages give the user a clear next step.
- Eliminate filler words ("Please note that...", "Successfully completed...") in favor of crisp status text (`Saved`, `Copied`).
