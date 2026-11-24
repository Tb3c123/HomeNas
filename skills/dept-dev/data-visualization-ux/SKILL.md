---
name: data-visualization-ux
description: Design truthful, clutter-free charts, heatmaps, matrices, and analytical tables with colorblind-safe palettes and clear interactivity.
metadata:
  model: inherit
  source: K-Dense-AI/scientific-agent-skills (MIT) + Orchestra-Research/AI-Research-SKILLs (MIT)
---

# Data Visualization UX

## Use This Skill When
- Building analytical dashboards, scientific plots, transition matrices, heatmaps, or telemetry charts.
- Choosing chart types, color scales, legends, tooltips, and interactive filters.
- Removing chartjunk and making quantitative comparisons effortless to read.

## Core Principles
1. **Match Chart Type to Analytical Question:**
   - Trend over time → Line/Area chart.
   - Ranked comparison → Horizontal bar chart (zero-based axis).
   - Distribution → Histogram, box/violin plot, or CDF.
   - Matrix / 2D correlation → Heatmap with perceptually uniform sequential (`Viridis`/`Cividis`) or diverging (`RdBu`) scale.
   - Avoid 3D charts, pie charts with >4 slices, and dual-axis charts that distort correlation.
2. **High Data-Ink Ratio (Zero Chartjunk):** Remove heavy gridlines, redundant borders, and legend hunting—prefer direct end-of-line labels, muted hairline gridlines, and clear titles stating the takeaway + units.
3. **Colorblind-Safe & Accessible Encoding:** Never rely on red/green hue alone; use Okabe-Ito or Viridis palettes, pair color with shape/dash pattern/direct values, and provide a tabular view or CSV export for screen readers.
4. **Truthful Scales:** Start bar axes at zero; explicitly label log scales or truncated line axes; show confidence intervals / error bars when plotting uncertain estimates.
5. **Precision Interactivity:** Provide crisp hover crosshairs, tabular-num tooltips showing exact values and deltas, and click-to-highlight series isolation without jittering layout.

## Delivery Checklist
- Verify every axis has explicit units and readable tick density (no overlapping labels).
- Confirm color palettes remain distinguishable in grayscale and deuteranopia simulation.
- Test chart responsiveness and empty/single-point edge cases.
