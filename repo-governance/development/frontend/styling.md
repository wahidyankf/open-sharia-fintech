---
title: Styling Convention
description: CSS and Tailwind v4 styling patterns for frontend applications in the open-sharia-enterprise monorepo
category: explanation
subcategory: development/frontend
tags:
  - styling
  - tailwind
  - css
  - responsive
  - mobile-first
created: 2026-03-28
when_to_use: Use when writing or reviewing CSS/Tailwind styling in any frontend app in this monorepo.
---

# Styling Convention

CSS and Tailwind v4 conventions for all frontend applications in the open-sharia-enterprise monorepo. These rules govern how styles are written, organized, and maintained across `organiclever-www` and `ayokoding-www`.

## Contents

- [Tailwind Directives and Utility-First Approach](./styling/tailwind-directives-and-utility-first-approach.md) — the globals.css directive set, and applying styles as utility classes in TSX.
- [`!important` and `@apply` Rules](./styling/important-and-apply-rules.md) — never use `!important` (with one documented exception), and `@apply` only inside `@layer base`.
- [Inline Styles, Class Ordering, and Defensive CSS](./styling/inline-styles-class-ordering-and-defensive-css.md) — no inline `style={}`, automatic class sorting, and overflow/truncation patterns.
- [Responsive Design and Touch Targets](./styling/responsive-design-and-touch-targets.md) — mobile-first breakpoints, container queries, and the 44×44px minimum tap target.
- [Content Visibility, Font Loading, and Fluid Typography](./styling/content-visibility-fonts-and-typography.md) — never hide content on mobile, `next/font` usage, and `clamp()` for smooth text scaling.

## Principles Implemented/Respected

- [Accessibility First](../../principles/content/accessibility-first.md) — Touch target minimums, no hidden content, and WCAG AA contrast requirements (via design tokens) all enforce this principle directly.
- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) — Utility-first styling keeps style logic in one place (the TSX file) and avoids abstract CSS class hierarchies.
- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) — `@theme` tokens, `@custom-variant dark`, and `prettier-plugin-tailwindcss` ordering make every styling decision visible and auditable.

## Conventions Implemented/Respected

- [Color Accessibility Convention](../../conventions/formatting/color-accessibility.md) — Design token values must meet the WCAG AA contrast ratios defined there. The `@theme` block is the authoritative place to enforce this.
- [Indentation Convention](../../conventions/formatting/indentation.md) — All CSS and TSX code examples in this document use 2-space indentation (language-appropriate for CSS and TypeScript/JSX).

## Applying the Implementation Workflow

Follow the three-stage [Implementation Workflow](../workflow/implementation.md) when building or refactoring styles:

1. **Make it work** — Apply utility classes directly in TSX. Hard-code values if it gets you to a working component faster.
2. **Make it right** — Extract repeated class combinations into a shared component or a `cva` variant definition. Move one-off overrides out of inline styles and into utilities.
3. **Make it fast** — Audit and remove unused design tokens; eliminate `!important` overrides; consolidate duplicate `@layer base` blocks.

Do not extract patterns in Stage 1. Copy-pasting class strings across components is acceptable while the design is still evolving.
