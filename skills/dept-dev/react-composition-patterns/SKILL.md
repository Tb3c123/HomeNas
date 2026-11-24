---
name: react-composition-patterns
description: Structure scalable React UIs using compound components, headless primitives, clean state ownership, and waterfall/re-render elimination.
metadata:
  model: inherit
  source: vercel-labs/agent-skills (Open)
---

# React Composition & State Patterns

## Use This Skill When
- Designing reusable React component libraries, complex interactive widgets, or multi-pane apps.
- Refactoring prop-heavy "god components" with boolean flag proliferation (`isCompact`, `hasFooter`, `showExtra`).
- Diagnosing unnecessary re-renders, effect chains, or client data-fetching waterfalls.

## Core Principles
1. **Composition Over Configuration:** Replace giant config-prop components with **Compound Components** (`<Dialog><Dialog.Trigger /><Dialog.Content /></Dialog>`) and `children`/slot props so callers control layout without bloating APIs.
2. **Headless Behavior + Thin Styling:** Separate keyboard/ARIA/state logic (hooks or Radix/Aria primitives) from visual presentation so styling can evolve without breaking accessibility.
3. **Minimal, Derived State:**
   - Never mirror props or derivable values in `useState` + `useEffect`; compute them during render (or `useMemo` only when profiling proves cost).
   - Lift state only to the lowest common ancestor; split high-frequency state (hover, typing, drag) from low-frequency global context to avoid cascading re-renders.
4. **Effect Hygiene:** Reserve `useEffect` strictly for synchronizing with external systems (DOM APIs, WebSockets, subscriptions, timers) with deterministic cleanup—never for event-driven business logic.
5. **Eliminate Waterfalls:** Fetch independent data in parallel (`Promise.all`), hoist queries above conditional branches, and use `AbortController` / React Query cancellation for stale requests.

## Delivery Checklist
- Verify no boolean-prop explosion; prefer explicit sub-components or discriminated variants.
- Confirm every `useEffect` has accurate dependencies and cleanup.
- Check key stability in lists (never use array index as `key` for reorderable/filterable items).
