---
name: typography-and-hierarchy
description: Design legible, expressive typographic systems using modular scales, intentional font pairing, optimal measure, and tabular numerals.
metadata:
  model: inherit
  source: nextlevelbuilder/ui-ux-pro-max-skill (MIT) + pbakaus/impeccable (Apache-2.0)
---

# Typography & Hierarchy

## Use This Skill When
- Selecting font pairings and building a responsive type scale for web apps or documentation.
- Designing data-dense dashboards, tables, mathematical views, or long-form reading interfaces.
- Fixing cramped headings, unreadable paragraphs, or jittering numeric counters.

## Core Principles
1. **Intentional Pairing (Max 2–3 Families):** Pair at most one expressive display/editorial font with one neutral UI sans-serif, plus a crisp monospace for code/IDs/matrices. Ensure full Vietnamese diacritic support when localizing.
2. **Modular Type Scale & Fluid Sizing:** Use a disciplined ratio (e.g., `1.20` Minor Third for apps, `1.25–1.333` for editorial) with `clamp()` for hero headings so text scales smoothly without abrupt breakpoint jumps.
3. **Reading Comfort & Measure:**
   - Constrain body prose width to `45–75ch` (`max-w-prose`).
   - Body line-height `1.5–1.65`; display heading line-height `1.05–1.2` with tight letter-spacing (`-0.02em` to `-0.03em`).
   - Uppercase micro-labels (`11–12px`) get positive tracking (`+0.04em` to `+0.08em`).
4. **Tabular Numerals for Data:** Always apply `font-variant-numeric: tabular-nums` to tables, KPIs, timers, prices, and matrix cells so digits align vertically and never jitter during live updates.
5. **Semantic Text Wrapping:** Use `text-wrap: balance` on headings and `text-wrap: pretty` on paragraphs to eliminate awkward orphan words.

## Delivery Checklist
- Verify font weights loaded match only those actually used (avoid faux bold/italic).
- Check Vietnamese/Unicode rendering and fallback font metrics to prevent layout shift (CLS).
- Confirm clear distinction between H1/H2/H3, body, caption, and monospace code styles.
