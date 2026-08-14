---
title: "Styling — Tailwind Directives and Utility-First Approach"
description: The Tailwind v4 globals.css directive set (@import, @source, @plugin, @custom-variant, @theme, @layer, @utility), and applying styles as utility classes directly in TSX rather than CSS rules
category: explanation
subcategory: development/frontend
tags:
  - styling
  - tailwind
  - css
  - responsive
  - mobile-first
created: 2026-03-28
when_to_use: Use when setting up a new app's globals.css, or deciding whether a style belongs as a utility class or a CSS rule.
---

# Tailwind Directives and Utility-First Approach

## Tailwind v4 Directives

Each app's `globals.css` uses a specific set of Tailwind v4 directives. Use only the directives the app actually needs.

```css
/* Entry point — replaces v3's @tailwind base/components/utilities */
@import "tailwindcss";

/* Content scan path — required when files live outside the default scan root */
/* ayokoding-www uses this because source lives in a non-default location */
@source "../../src/**/*.{ts,tsx}";

/* Tailwind plugins */
/* ayokoding-www uses @tailwindcss/typography for prose content */
@plugin "@tailwindcss/typography";

/* Dark mode variant — class-based (.dark), not media-query-based */
@custom-variant dark (&:is(.dark *));

/* Design tokens — define custom CSS variables for Tailwind to consume */
@theme {
  --color-primary: hsl(221.2 83.2% 53.3%);
  --radius: 0.5rem;
}

/* Base styles — resets and body defaults ONLY */
@layer base {
  body {
    @apply bg-background text-foreground;
  }
}

/* Custom utilities — single-purpose utility definitions */
@utility text-balance {
  text-wrap: balance;
}
```

See `apps/organiclever-app-web/src/app/globals.css` and `apps/ayokoding-www/src/app/globals.css` for the full reference implementations.

## Utility-First Approach

Apply styles with Tailwind utility classes directly in TSX components. Do NOT write CSS rules for component styling.

```tsx
/* Correct — utility classes in TSX */
export function Card({ children }: { children: React.ReactNode }) {
  return <div className="rounded-lg border border-border bg-card p-6 shadow-sm">{children}</div>;
}
```

```css
/* Wrong — component styles in CSS */
.card {
  border-radius: 0.5rem;
  background: var(--card);
  padding: 1.5rem;
}
```

**Exceptions — CSS is correct in these cases:**

- `@layer base` in `globals.css` for reset and body defaults
- Specificity overrides needed to beat third-party library defaults (e.g., `@tailwindcss/typography` prose styles) — place these outside `@layer` so they win the cascade
