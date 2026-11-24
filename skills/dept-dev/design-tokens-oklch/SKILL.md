---
name: design-tokens-oklch
description: Build perceptually uniform OKLCH color systems, semantic light/dark surfaces, and accessible contrast tokens without harsh pure black or white.
metadata:
  model: inherit
  source: pbakaus/impeccable (Apache-2.0)
---

# Design Tokens & OKLCH Color Systems

## Use This Skill When
- Establishing or refactoring a design token architecture (CSS variables / Tailwind theme).
- Implementing dark mode and light mode surfaces with consistent perceived contrast.
- Choosing brand, neutral, and semantic status palettes (success, warning, danger, info).

## Core Principles
1. **Perceptually Uniform OKLCH:** Define palettes in `oklch(L C H)` so equal lightness steps look equally bright across hues (unlike HSL where yellow looks brighter than blue at identical L).
2. **Tinted Neutrals Over Pure `#000`/`#fff`:**
   - Give neutrals a subtle hue tint (`C ≈ 0.005–0.015`) matching the brand temperature.
   - Use deep off-black surfaces (`L ≈ 0.14–0.18`) in dark mode and soft off-white (`L ≈ 0.98–0.99`) in light mode to reduce eye strain.
3. **3-Tier Token Architecture:**
   - **Primitive:** Raw scale (`--gray-100..950`, `--accent-500`).
   - **Semantic:** Role-based (`--bg-canvas`, `--bg-surface`, `--bg-elevated`, `--text-primary`, `--text-muted`, `--border-subtle`).
   - **Component:** Scoped overrides (`--btn-primary-bg`) referencing semantic tokens only.
4. **Elevation via Lightness in Dark Mode:** In dark themes, raise elevated surfaces slightly in lightness (`+0.03–0.05 L`) with crisp 1px subtle borders rather than heavy drop shadows.
5. **Contrast Guarantees:** Enforce WCAG AA (`>= 4.5:1` body text, `>= 3:1` UI controls & large text) across every light/dark token pair.

## Delivery Checklist
- Map every color in components to semantic CSS custom properties (zero raw hex literals).
- Verify dark/light polarity switch updates surfaces, borders, focus rings, and chart series cleanly.
- Audit muted text and placeholder contrast against their actual surface token.
