---
name: responsive-layout-architecture
description: Architect resilient responsive layouts with CSS Grid, Subgrid, Container Queries, adaptive split-panes, and zero horizontal overflow.
metadata:
  model: inherit
  source: kozz36/frontend-designer-skill (MIT) + web.dev layout patterns
---

# Responsive Layout Architecture

## Use This Skill When
- Structuring application shells (sidebar + main + inspector), dashboards, or multi-column tools.
- Making complex desktop workspaces degrade cleanly on tablet and mobile screens.
- Fixing horizontal scrollbugs, clipped panels, or misaligned card grids.

## Core Principles
1. **Intrinsic Sizing Over Brittle Breakpoints:** Prefer `repeat(auto-fit, minmax(min(100%, 280px), 1fr))`, `clamp()`, and flexbox wrapping so layouts adapt naturally to content and viewport width.
2. **Component-Driven Container Queries:** Use `@container` queries for reusable cards, widgets, and split-pane modules so they adapt to their parent panel width rather than global viewport width.
3. **Subgrid for Cross-Card Alignment:** Use `grid-template-rows: subgrid` when adjacent cards have variable-length titles or descriptions so footers and action rows align horizontally.
4. **Safe App-Shell Patterns:**
   - Use `100dvh` (dynamic viewport height) instead of `100vh` to prevent mobile address-bar clipping.
   - Apply `min-width: 0` / `min-height: 0` on flex/grid children containing scrollable or truncated content (`overflow-x: auto`, `text-overflow: ellipsis`).
   - Collapse secondary sidebars/inspectors into accessible slide-over drawers or bottom sheets on narrow screens.
5. **Zero Unintended Horizontal Overflow:** Keep tables and wide matrices inside dedicated horizontal scroll containers with subtle scroll-fade indicators—never let the entire page overflow horizontally.

## Delivery Checklist
- Test at `360px`, `768px`, `1280px`, and `1920px` widths plus `200%` browser zoom.
- Verify sticky headers/toolbars do not overlap focused inputs or anchored headings (`scroll-margin-top`).
- Confirm zero unwanted horizontal page scrollbars across all views.
