---
name: interactive-canvas-svg-ui
description: Build crisp, high-DPI SVG diagrams and 60fps HTML5 Canvas/WebGL interactive simulations with smooth pan, zoom, and hit-testing.
metadata:
  model: inherit
  source: anthropics/skills (Apache-2.0)
---

# Interactive Canvas & SVG UI

## Use This Skill When
- Building interactive node graphs, Markov/state diagrams, mathematical simulations, or custom visual editors.
- Deciding between DOM/SVG vs. HTML5 Canvas 2D / WebGL for rendering performance.
- Implementing pan/zoom viewports, drag-and-drop nodes, or crisp retina rendering.

## Core Principles
1. **Right Rendering Target:**
   - **SVG:** Best for `< 500` crisp vector elements needing DOM events, CSS styling, accessibility, and infinite zoom sharpness (diagrams, state graphs, icons).
   - **Canvas 2D / WebGL:** Best for `> 500` animated particles, dense heatmaps, or 60fps continuous simulations.
2. **High-DPI Retina Sharpness:** Always scale Canvas backing buffers by `window.devicePixelRatio` while keeping CSS dimensions in logical pixels (`ctx.setTransform(dpr, 0, 0, dpr, 0, 0)`).
3. **Decoupled Simulation & Render Loop:**
   - Separate pure state/math updates from `requestAnimationFrame` drawing; clamp `dt` to avoid jumps when tabs resume.
   - Render on-demand (dirty flag) for static/interactive editors instead of burning CPU/battery with idle 60fps loops.
4. **Ergonomic Viewport Controls:** Implement zoom-toward-cursor, bounded pan, one-click `Fit to View` / `Reset`, and clean pointer capture (`setPointerCapture`) for reliable dragging.
5. **Accessible Fallbacks:** Provide keyboard shortcuts for zoom/selection, `role="img"` + `aria-label` summaries, and a synced text/table representation of interactive diagram state.

## Delivery Checklist
- Verify crisp rendering on `devicePixelRatio >= 2` displays and window resize (`ResizeObserver`).
- Confirm `requestAnimationFrame` loops cancel cleanly on unmount and pause when hidden.
- Test hit-testing accuracy under combined pan + zoom transforms.
