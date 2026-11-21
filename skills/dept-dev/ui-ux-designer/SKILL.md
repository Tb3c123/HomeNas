---
name: ui-ux-designer
description: Design intuitive user flows, wireframes, design systems, and WCAG-accessible interfaces with clear visual hierarchy and responsive layouts.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# UI/UX Designer & Design Systems

## Use This Skill When
- Designing user flows, information architecture, wireframes, or interactive UI prototypes.
- Defining design tokens (color, typography, spacing, elevation) and reusable component states.
- Auditing visual hierarchy, usability friction, and WCAG 2.1 AA accessibility.

## Core Design Principles
1. **Task-First Clarity:** Primary user action must be immediately obvious; minimize cognitive load and click depth.
2. **Design Tokens Over Magic Values:** Standardize semantic color roles (surface, text, accent, status), type scale, and 4px/8px spacing grid.
3. **Complete Component States:** Every interactive element must define `default`, `hover`, `focus-visible`, `active`, `disabled`, `loading`, `empty`, and `error` states.
4. **Accessibility (WCAG AA) by Default:**
   - Text contrast >= 4.5:1 (large text >= 3:1).
   - Full keyboard navigation, visible focus rings, semantic landmarks, and descriptive `aria-label`s.
   - Touch/click targets >= 44x44px on mobile/touch interfaces.
5. **Responsive & Fluid Layouts:** Design mobile-first or adaptive split-pane layouts without horizontal overflow.

## Delivery Checklist
- Map critical user journeys and edge states (empty, error, offline, slow network).
- Specify layout structure, component inventory, and visual token palette.
- Validate keyboard navigation, contrast ratios, and clear microcopy before frontend handoff.
