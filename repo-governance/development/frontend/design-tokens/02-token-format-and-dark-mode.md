---
title: "Design Tokens — Token Format and Dark Mode"
description: The double-indirection and direct-value token formatting approaches (direct value is recommended), and the requirement that every visual token have a .dark counterpart
category: explanation
subcategory: development/frontend
tags:
  - design-tokens
  - css
  - tailwind
  - theming
  - dark-mode
created: 2026-03-28
when_to_use: Use when writing a new token's globals.css declaration, or adding dark-mode support for a token.
---

# Token Format and Dark Mode

## Token Format: Two Current Approaches

The monorepo currently has two formatting approaches in production apps.

**Double indirection** (`organiclever-app-web`):

```css
/* globals.css */
:root {
  --primary: 0 0% 9%;
}

@theme {
  --color-primary: hsl(var(--primary));
}
```

The bare variable holds only the HSL components (no `hsl()` wrapper), and the `@theme` alias wraps it.

**Direct value** (`ayokoding-www`):

```css
/* globals.css */
@theme {
  --color-primary: hsl(221.2 83.2% 53.3%);
}
```

The `@theme` alias holds the complete value directly.

**Recommended for `web-ui-token`**: Use the direct value approach. It is simpler to read, easier to override via CSS cascade, and removes the indirection layer that double indirection introduces without measurable benefit. The shared library defines complete `hsl(...)` values; per-app overrides replace the `--color-*` alias in the app's own `@theme` block.

## Dark Mode Requirements

Every visual token must have a `.dark` counterpart. Omitting a dark-mode value causes the light-mode value to persist in dark contexts, which typically fails WCAG AA contrast.

```css
:root {
  --background: hsl(0 0% 100%);
  --foreground: hsl(222.2 84% 4.9%);
  --primary: hsl(221.2 83.2% 53.3%);
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  --primary: hsl(217.2 91.2% 59.8%);
}
```

Register the dark variant in your Tailwind v4 config using:

```css
@custom-variant dark (&:is([data-theme="dark"] *), &:is(.dark *));
```

The compound selector supports both the `data-theme="dark"` attribute (set via JavaScript,
e.g., `document.documentElement.setAttribute('data-theme', 'dark')`) and the `.dark` class
(set via Tailwind's class-based dark mode). Use whichever pattern your app requires — both
activate the same dark-mode tokens.

Verify WCAG AA contrast (4.5:1 for text, 3:1 for components) independently in both light and dark modes. Do not assume that a passing light-mode contrast automatically satisfies dark mode.
