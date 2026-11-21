---
name: accessibility-compliance-accessibility-audit
description: Audit and remediate web/app UIs for WCAG 2.1 AA compliance including keyboard navigation, contrast, ARIA semantics, and focus management.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Accessibility Compliance (WCAG 2.1 AA Audit)

## Use This Skill When
- Building or reviewing interactive web UIs, modals, forms, tables, or keyboard-driven developer tools.

## High-Impact WCAG AA Checklist
1. **Semantic HTML First:** Use native `<button>`, `<a href>`, `<label for>`, `<nav>`, `<main>`, and proper heading hierarchy (`h1` -> `h2` -> `h3`) instead of clickable `<div>`s.
2. **Full Keyboard Support:** Every control must be reachable via `Tab`/`Shift+Tab`, activatable via `Enter`/`Space`, and modals/menus must trap focus and close on `Escape` (restoring prior focus).
3. **Visible Focus & Contrast:** Maintain clear `:focus-visible` outlines and contrast ratios >= 4.5:1 (normal text) / >= 3:1 (large text & UI icons); never convey state by color alone.
4. **Forms & Live Regions:** Associate every input with a visible `<label>`, link validation errors via `aria-describedby`, and announce async status updates/toasts with `aria-live="polite"`.
5. **Reduced Motion:** Respect `@media (prefers-reduced-motion: reduce)` for animations and transitions.
