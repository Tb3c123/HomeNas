---
name: design-md-system
description: Adopt, fetch, or author a root DESIGN.md (getdesign.md / Google Stitch format) as the single visual source of truth before prototyping and coding UI.
metadata:
  model: inherit
  source: VoltAgent/awesome-design-md (MIT) + google-labs-code/design.md (Apache-2.0)
---

# DESIGN.md Visual System (getdesign.md MIT-First)

## Use This Skill When
- Starting any new web app, dashboard, or landing page before the Design-Preview Gate.
- Restyling an existing UI so every page shares one cohesive visual language without "AI slop".
- Translating brand/reference aesthetics into concrete tokens, typography, and component rules.

## Workflow (MIT-First — Zero Account Required)
1. **Pick or Author `./DESIGN.md` at Project Root:**
   - **Option A — Fetch Free MIT Template (84+ curated systems):**
     - Via CLI: `npx getdesign@latest add <slug>` (browse slugs with `npx getdesign@latest list` or `https://getdesign.md`).
     - Via Raw GitHub (no Node needed): fetch from `https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/<slug>/DESIGN.md`.
   - **Option B — Author Custom `./DESIGN.md`:** Use the 9 canonical sections: (1) Visual Theme & Atmosphere, (2) Color Palette & Roles, (3) Typography Rules, (4) Component Stylings, (5) Layout Principles, (6) Depth & Elevation, (7) Do's & Don'ts, (8) Responsive Behavior, (9) Agent Prompt Guide.
2. **Recommended MIT Baseline Slugs by Domain:**
   - *SaaS / Dev Dashboard:* `linear`, `vercel`, `supabase`, `raycast`, `sentry`
   - *Editorial / Docs / Workspace:* `notion`, `claude`, `mintlify`, `cursor`
   - *Fintech / Analytics:* `stripe`, `mercury`, `posthog`, `wise`
   - *Consumer / Media / Showcase:* `apple`, `airbnb`, `spotify`, `framer`
3. **Adapt, Never Clone Trademarks:** Treat any fetched `DESIGN.md` as a structural & aesthetic baseline; replace brand names, logos, and copy with the project's own identity.
4. **Gate Integration (Design-Preview Gate):**
   - Read `./DESIGN.md` **before** building the interactive `.html` prototype.
   - Verify Light/Dark surfaces, contrast (WCAG AA), and component states in Desktop (`1280px`) + Mobile (`390px`) Playwright screenshots before coding production UI.
   - Keep `./DESIGN.md` under `<= 1000 lines / 64 KB` (trimmed to decisions that matter so agents don't dilute rules).

## Delivery Checklist
- `./DESIGN.md` exists at project root and is referenced before UI prototyping & implementation.
- Color tokens, typography scale, radius, elevation, and Do's/Don'ts are reflected in CSS/Tailwind theme.
- Prototype screenshots (`1280px` & `390px`) match `./DESIGN.md` with zero off-system colors or font drift.
