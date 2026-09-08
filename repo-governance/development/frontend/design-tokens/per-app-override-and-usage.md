---
description: How an app imports shared tokens and declares brand overrides in its own globals.css, and referencing tokens through Tailwind utility classes rather than raw CSS property access
when_to_use: Use when a new app needs to declare its brand token overrides, or when writing component markup that consumes tokens.
---

# Per-App Override and Usage

## Per-App Override Pattern

An app imports the shared structural and semantic tokens, then declares its brand overrides in the same `globals.css`:

```css
/* apps/my-app/src/app/globals.css */
@import "@open-sharia-enterprise/web-ui-token/tokens.css";

@theme {
  /* Brand override — replaces the shared default */
  --color-primary: hsl(221.2 83.2% 53.3%);
  --color-primary-foreground: hsl(0 0% 100%);
  --color-secondary: hsl(210 40% 96.1%);
  --color-secondary-foreground: hsl(222.2 47.4% 11.2%);
}
```

The CSS cascade ensures the app's `@theme` declarations take precedence over imported defaults. Structural tokens (`--radius`, spacing, typography) are not overridden — only brand tokens.

## Using Tokens in Tailwind Utilities

Reference tokens through Tailwind utility classes, never through raw CSS custom property access in component files.

```tsx
/* Correct */
<button className="bg-primary text-primary-foreground rounded-md px-4 py-2">
  Save
</button>

<p className="text-muted-foreground text-sm">Optional description</p>

<div className="border border-border bg-background">
  Content area
</div>
```

This keeps component code free of CSS property names and ensures the token layer is the single place to change values.
