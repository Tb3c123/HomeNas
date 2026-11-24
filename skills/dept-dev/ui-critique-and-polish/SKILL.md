---
name: ui-critique-and-polish
description: Run a systematic pre-ship UI critique and polish pass covering alignment, visual noise, cognitive load, and edge states.
metadata:
  model: inherit
  source: pbakaus/impeccable (Apache-2.0)
---

# UI Critique & Polish Pass

## Use This Skill When
- Reviewing a newly built screen or component before marking a frontend task Done.
- Diagnosing why a UI feels "off", cluttered, cramped, or unfinished.
- Conducting a final pre-release visual QA sweep.

## 6-Point Critique Rubric
1. **First-Glance Clarity (3-Second Test):** Can a new user immediately tell what this page does and what the primary action is? Demote competing CTAs to secondary/ghost variants.
2. **Alignment & Optical Balance:** Check pixel alignment along vertical/horizontal grid lines, icon-to-text optical centering, consistent border-radius nesting (`outerRadius = innerRadius + padding`), and uniform card padding.
3. **Cognitive Load & Visual Noise:** Remove redundant labels, duplicate dividers, unnecessary shadows, and walls of badges. Group related controls by proximity first, borders second.
4. **Edge & Stress States:** Inspect with:
   - Empty data (helpful guidance + primary CTA, not a blank box).
   - Extreme content (very long titles, 0 items, 1000+ items, narrow 360px viewport).
   - Error & slow-loading states (actionable retry, preserved user input).
5. **Interactive Affordance:** Ensure clickable items look clickable (cursor, hover shift, focus ring), destructive actions are separated and confirmed, and disabled states explain why when non-obvious.
6. **Polish Details:** Check favicon, page `<title>`, scrollbar styling, clipped tooltips/dropdowns (`overflow: hidden` traps), and consistent icon stroke weights.

## Output Format
- Report findings ranked by severity (`[Blocking]`, `[Polish]`, `[Nice-to-have]`) with exact component/selector and concrete fix.
