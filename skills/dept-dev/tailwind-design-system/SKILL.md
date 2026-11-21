---
name: tailwind-design-system
description: Build cohesive, themeable UI design systems with Tailwind CSS semantic tokens, CVA component variants, dark mode, and responsive grids.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Tailwind Design System & Component Styling

## Use This Skill When
- Setting up Tailwind CSS theme tokens, dark/light themes, typography scale, or reusable UI primitives.
- Styling dashboards, forms, tables, and multi-pane desktop/web layouts consistently.

## Token & Component Architecture
1. **Semantic CSS Variables:** Define theme tokens (`--bg-surface`, `--text-primary`, `--accent`, `--border-subtle`) in CSS and map them to Tailwind theme keys so dark/light themes switch cleanly without scattered `dark:` overrides.
2. **Variant-Driven Primitives:** Extract repeated class combinations into small typed components (using `cva` + `tailwind-merge` / `cn()` helper) instead of copy-pasting 15 utility classes everywhere.
3. **Consistent Rhythm & Density:** Stick to Tailwind's spacing scale (`gap-2`, `p-4`, `p-6`) and clear typographic hierarchy (heading, body, caption, monospace for logs/code).
4. **Accessible Focus & Contrast:** Always style `focus-visible:ring-2` and verify readable contrast on badges, muted labels, and buttons in both light and dark modes.
5. **Layout Hygiene:** Use Flexbox/Grid (`min-w-0`, `overflow-hidden`, `truncate`) to prevent long logs or URLs from breaking split-pane layouts.
