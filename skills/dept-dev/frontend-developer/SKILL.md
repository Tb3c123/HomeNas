---
name: frontend-developer
description: Build responsive, accessible React/Next.js/Vite web applications with clean component composition, predictable state management, and fast rendering.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Frontend Developer (React, Next.js & Modern Web)

## Use This Skill When
- Building interactive web apps, dashboards, multi-pane cockpits, or component libraries in React / Next.js / Vite.
- Structuring client/server state, custom hooks, forms, and error/loading boundaries.

## Component & State Best Practices
1. **Small, Focused Components:** Keep each component `<= 150 lines`; separate presentational UI from data-fetching/side-effect hooks.
2. **Right-Sized State:**
   - Local UI state -> `useState` / `useReducer`.
   - Server/async state -> TanStack Query / SWR (caching, deduping, retries).
   - Shared client state -> lightweight store (Zustand / Context) only when truly cross-tree.
3. **Avoid `useEffect` Pitfalls:** Derive computed values during render instead of syncing state in `useEffect`; always clean up subscriptions, timers, and WebSockets.
4. **Resilient UX:** Wrap views in Error Boundaries, render skeleton/loading and empty states gracefully, and prevent layout shift.
5. **Accessibility & Performance:** Use semantic HTML (`<button>`, `<nav>`, `<main>`), keyboard shortcuts, and memoize only measured bottlenecks.

## Verification Checklist
- Build (`npm run build`) and type-check (`tsc --noEmit`) pass with zero warnings.
- Works cleanly across desktop and mobile viewports with zero console errors.
