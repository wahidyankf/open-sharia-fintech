---
title: "Styling Convention"
description: "CSS and Tailwind v4 styling patterns for frontend applications in the open-sharia-enterprise monorepo"
when_to_use: "Read this index to find the right Styling Convention child document."
---

# Styling Convention

- [Styling — Tailwind Directives and Utility-First Approach](./tailwind-directives-and-utility-first-approach.md) — The Tailwind v4 globals.css directive set (@import, @source, @plugin, @custom-variant, @theme, @layer, @utility), and applying styles as utility classes directly in TSX rather than CSS rules Use when setting up a new app's globals.css, or deciding whether a style belongs as a utility class or a CSS rule.
- [Styling — !important and @apply Rules](./important-and-apply-rules.md) — Never use !important (with one documented, currently-necessary exception involving rehype-pretty-code inline styles), and @apply only inside @layer base Use when tempted to reach for !important or @apply outside a base-layer reset.
- [Styling — Inline Styles, Class Ordering, and Defensive CSS](./inline-styles-class-ordering-and-defensive-css.md) — No inline style={} props (except temporary migrations), automatic Tailwind class sorting via prettier-plugin-tailwindcss, and defensive CSS patterns that prevent layout breakage Use when tempted to add an inline style prop, when Tailwind classes appear unsorted after save, or when a layout risks content overflow.
- [Styling — Responsive Design and Touch Targets](./responsive-design-and-touch-targets.md) — Mobile-first breakpoints (375px/768px/1280px), container queries for component-relative layout, and the 44×44px minimum tap target for mobile viewports Use when building any responsive layout, or sizing an interactive element for mobile.
- [Styling — Content Visibility, Font Loading, and Fluid Typography](./content-visibility-fonts-and-typography.md) — Never hide content on mobile (adapt the layout instead), use next/font for all font loading, and use clamp() or Tailwind responsive utilities for text that scales between breakpoints Use when a component might hide content on small screens, when adding a font, or when sizing text that must scale across breakpoints.
- [Styling — Applying the Implementation Workflow](./applying-the-implementation-workflow.md) — The three-stage make-it-work/make-it-right/make-it-fast Implementation Workflow applied specifically to building or refactoring styles Use when starting a new styling task or refactor, to decide what to prioritize at each stage.
