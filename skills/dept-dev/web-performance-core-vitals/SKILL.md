---
name: web-performance-core-vitals
description: Optimize browser rendering and Core Web Vitals (LCP, INP, CLS), asset loading, bundle budgets, and virtualized lists.
metadata:
  model: inherit
  source: vercel-labs/agent-skills (Open) + web.dev Core Web Vitals
---

# Web Performance & Core Web Vitals

## Use This Skill When
- Auditing slow initial loads, input lag, layout jumps, or bloated JS bundles in web apps.
- Optimizing image/font delivery, code splitting, or rendering large tables/lists (`> 200` rows).
- Setting measurable frontend performance budgets before production release.

## Core Targets & Tactics
1. **LCP (Largest Contentful Paint `<= 2.5s`):**
   - Preload the hero image (`fetchpriority="high"`), serve modern formats (WebP/AVIF) with responsive `srcset`, and avoid hiding LCP content behind client-only JS spinners.
   - Inline critical CSS or keep initial bundle lean (`< 150 KB` gzipped JS for app shell).
2. **INP (Interaction to Next Paint `<= 200ms`):**
   - Break up long main-thread tasks (`> 50ms`), offload heavy math/parsing to Web Workers, and debounce expensive filter/search computations.
   - Virtualize long lists/tables (`@tanstack/react-virtual` or windowing) instead of mounting thousands of DOM nodes.
3. **CLS (Cumulative Layout Shift `<= 0.1`):**
   - Always specify explicit `width`/`height` or `aspect-ratio` on images, videos, and charts.
   - Reserve space for async banners/skeletons and use `font-display: swap` with metric-matched fallback fonts.
4. **Code Splitting & Caching:** Lazy-load heavy routes, charts, and editors via dynamic `import()`; leverage immutable content-hashed static assets with long cache headers.
5. **Measure Before & After:** Profile with Lighthouse, Chrome Performance trace, and bundle analyzer—never optimize blindly.

## Delivery Checklist
- Verify zero console warnings, zero layout jumps during initial load, and responsive clicks under 4x CPU throttling.
- Confirm heavy visualization/math libraries are code-split out of the critical landing bundle.
- Record before/after bundle size and Core Web Vitals metrics.
