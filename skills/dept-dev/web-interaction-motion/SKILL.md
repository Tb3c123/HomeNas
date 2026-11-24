---
name: web-interaction-motion
description: Engineer purposeful micro-interactions, GPU-composited transitions, optimistic UI feedback, and reduced-motion accessibility.
metadata:
  model: inherit
  source: vercel-labs/agent-skills (Open) + pbakaus/impeccable (Apache-2.0)
---

# Web Interaction & Motion Design

## Use This Skill When
- Designing hover/press states, modals, drawers, tabs, route transitions, or optimistic UI updates.
- Making interactive controls feel responsive, tactile, and clear without distracting gimmicks.
- Fixing janky animations or slow perceived latency.

## Core Principles
1. **Purposeful Motion Only:** Every animation must clarify spatial orientation, confirm user action, or bridge state transitions—never animate solely for decoration.
2. **GPU-Composited Properties Only:** Animate strictly `transform` and `opacity` (and View Transitions API where supported). Never animate layout-triggering properties (`width`, `height`, `top`, `left`, `margin`, `padding`).
3. **Crisp Timing & Natural Curves:**
   - Micro-feedback (hover, toggle, press): `100–150ms`.
   - Component transitions (popover, drawer, tab indicator): `180–260ms`.
   - Use decelerating curves (`cubic-bezier(0.22, 1, 0.36, 1)` / `ease-out-quart`) for entrances and brisk `ease-in` for exits; avoid cartoonish elastic bounce.
4. **Immediate Perceived Responsiveness:**
   - Apply subtle tactile press feedback (`active:scale-[0.98]`), optimistic state updates with rollback on error, and skeleton placeholders matched to final layout geometry.
   - Show loading spinners only after a short delay (`~150–200ms`) to prevent flicker on fast responses.
5. **Respect User Preferences:** Always honor `@media (prefers-reduced-motion: reduce)` by disabling spatial movement and falling back to instant or soft opacity crossfades.

## Delivery Checklist
- Confirm zero layout thrashing (`transform`/`opacity` only) at 60fps.
- Verify keyboard focus transitions remain visible and uninterrupted during animated mounts/unmounts.
- Test with `prefers-reduced-motion: reduce` enabled.
