---
description: Structural tokens (shared, not overridable) vs. brand tokens (per-app override), and the bare-HSL-variable plus Tailwind-theme-alias naming pattern
when_to_use: Use when deciding whether a new value belongs in the shared structural set or a per-app brand override, or when naming a new token.
---

# Token Categories and Naming Convention

## Token Categories

### Structural Tokens (Shared via `web-ui-token`)

Structural tokens live in the `libs/web-ui-token` library and are imported by every frontend app. They represent values that are layout- and brand-neutral — apps should not override them.

**Border radius**

```css
--radius: 0.5rem;
--radius-lg: 0.75rem;
--radius-md: 0.5rem;
--radius-sm: 0.25rem;
```

**Spacing (4-point system)**

```css
--space-1: 0.25rem; /* 4px */
--space-2: 0.5rem; /* 8px */
--space-3: 0.75rem; /* 12px */
--space-4: 1rem; /* 16px */
--space-6: 1.5rem; /* 24px */
--space-8: 2rem; /* 32px */
--space-12: 3rem; /* 48px */
--space-16: 4rem; /* 64px */
```

**Typography scale**

```css
--text-xs: 0.75rem;
--text-sm: 0.875rem;
--text-base: 1rem;
--text-lg: 1.125rem;
--text-xl: 1.25rem;
--text-2xl: 1.5rem;
--text-3xl: 1.875rem;
--text-4xl: 2.25rem;
```

**Base neutrals**

```css
--background: ...;
--foreground: ...;
--border: ...;
--input: ...;
--ring: ...;
```

**Semantic tokens**

```css
--muted: ...;
--muted-foreground: ...;
--destructive: ...;
--destructive-foreground: ...;
```

### Brand Tokens (Per-App Override)

Brand tokens express each app's visual identity. Apps define these in their own `globals.css` by overriding the defaults from `web-ui-token`.

**Core brand palette**

```css
--primary: ...;
--primary-foreground: ...;
--secondary: ...;
--secondary-foreground: ...;
--accent: ...;
--accent-foreground: ...;
```

**App-specific extensions**

- `organiclever-app-web`: chart tokens `--chart-1` through `--chart-5`
- `ayokoding-www`: sidebar tokens `--sidebar-background`, `--sidebar-foreground`, `--sidebar-primary`, `--sidebar-primary-foreground`, `--sidebar-accent`, `--sidebar-accent-foreground`, `--sidebar-border`, `--sidebar-ring`

## Naming Convention

The monorepo uses two token levels for Tailwind v4 integration.

**Bare HSL variable** — defined in `:root` and `.dark`:

```css
:root {
  --primary: 221.2 83.2% 53.3%;
}
```

**Tailwind theme alias** — defined in `@theme` block, consumes the bare variable:

```css
@theme {
  --color-primary: hsl(var(--primary));
}
```

The `--color-{name}` form is what Tailwind v4 resolves to utility classes like `bg-primary` and `text-primary-foreground`. The bare `--{name}` variable is the overridable value. Keep these two levels strictly separated — bare variables belong in `:root`/`.dark`, Tailwind aliases belong in `@theme`.

> **Caveat — `@theme` can silently drop a declaration**: Tailwind v4's `@theme {}` directive routes
> through Lightning CSS's theme-token compiler rather than passing custom properties straight to
> `:root`, and that compiler has been observed to silently drop a newly added custom-property
> declaration — no build error, no warning, the property just never reaches the compiled
> stylesheet — even when its shape is identical to other declarations in the same block that do
> resolve correctly. Before trusting a new custom property added inside `@theme {}`, verify it
> resolves via `getComputedStyle(document.documentElement).getPropertyValue("--your-token")` on a
> live page rather than assuming parity with existing declarations.
