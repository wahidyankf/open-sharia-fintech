---
title: "Design Tokens — OKLCH Brand Tokens (OrganicLever)"
description: OrganicLever's warm OKLCH palette - why OKLCH over HSL, and the hue/ink/wash and warm-neutral token structure including dark mode
category: explanation
subcategory: development/frontend
tags:
  - design-tokens
  - css
  - tailwind
  - theming
  - dark-mode
created: 2026-03-28
when_to_use: Use when working on organiclever-app-web's token layer and need the OKLCH rationale or token structure.
---

# OKLCH Brand Tokens (OrganicLever)

`organiclever-app-web` uses a warm OKLCH palette rather than HSL. OKLCH is the CSS Colors Level 4
perceptual color space — it provides **perceptually uniform chroma** so that hues at the same
`L%` and `C` level look equally vivid, unlike HSL where `50% saturation` produces wildly
different perceived intensity across hues.

## Why OKLCH for OrganicLever

- **Perceptual uniformity** — `oklch(68% 0.10 195)` (teal) and `oklch(68% 0.10 25)`
  (terracotta) have the same perceived lightness at any chroma value. HSL equivalents drift.
- **Wide-gamut ready** — OKLCH values outside the sRGB gamut are automatically clamped to
  display-p3 on P3 screens, with no authored fallback needed for modern browsers.
- **Design handoff fidelity** — the OL design tokens were authored in OKLCH; roundtripping
  through HSL introduces rounding error. Keeping OKLCH preserves the designer's intent exactly.

## OL Token Structure

OL brand tokens live in `libs/web-ui-token/src/organiclever.css` (opt-in per-app import).

**Six semantic hues × three tints**:

```css
:root {
  /* base — full saturation, reading-legible on white */
  --hue-teal: oklch(68% 0.1 195);
  --hue-teal-ink: oklch(38% 0.09 195); /* dark text on wash */
  --hue-teal-wash: oklch(95% 0.03 195); /* light background tint */

  /* repeated for: terracotta (25°), honey (75°), sage (145°), sky (235°), plum (300°) */
}
```

**Warm neutral scale** — `--warm-0` through `--warm-900`, all with hue ~80 (warm cream bias):

```css
:root {
  --warm-0: oklch(99% 0.005 80); /* near-white cream */
  --warm-100: oklch(96% 0.008 80);
  /* … */
  --warm-900: oklch(18% 0.01 80); /* near-black warm */
}
```

**Semantic overrides** (in `@theme`, reference the `:root` vars above):

```css
@theme {
  --color-background: var(--warm-0);
  --color-foreground: var(--warm-900);
  --color-primary: var(--hue-sage);
  --color-ring: var(--hue-teal);
  --radius-md: 12px; /* OL geometry: rounder than the neutral baseline */
}
```

**Dark mode** — in `[data-theme="dark"], .dark { … }`:

```css
[data-theme="dark"],
.dark {
  --warm-0: oklch(22% 0.012 80);
  --color-card: var(--warm-50); /* must be explicit — @theme hex can't auto-derive */
  --color-popover: var(--warm-50);
  --hue-teal: oklch(72% 0.12 195); /* lifted for dark-bg legibility */
}
```
