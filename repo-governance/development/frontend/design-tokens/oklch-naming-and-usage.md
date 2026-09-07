---
description: The hue/ink/wash and warm-neutral naming convention for OKLCH tokens, the rule against hardcoding OKLCH literals, and how to apply a runtime-determined hue via inline style
when_to_use: Use when naming a new OKLCH token, reviewing a component for hardcoded color literals, or building a component whose color varies at runtime.
---

# OKLCH Naming and Usage

## Naming Convention for OKLCH Tokens

- `--hue-{name}` — base hue for backgrounds, icon fills, button bg
- `--hue-{name}-ink` — text/icon color on a white or wash surface
- `--hue-{name}-wash` — very light background tint for cards, alert backgrounds
- `--warm-{0,50,100,…,900}` — neutral scale with warm bias
- Semantic aliases (`--color-primary`, `--color-ring`) map to hue tokens via `var()`

## Do Not Hardcode OKLCH Literals in Components

Components must reference `var(--hue-teal)`, not the literal `oklch(68% 0.10 195)`.
The token layer is the single authority for color values.

## Dynamic Hue Backgrounds

When a component's hue is determined at runtime (e.g., `<StatCard hue="terracotta">`),
Tailwind cannot detect constructed class names at build time. Use inline `style` prop:

```tsx
/* Correct — resolved at runtime via CSS cascade */
<div style={{ backgroundColor: `var(--hue-${hue})` }} />

/* Wrong — Tailwind cannot detect template literal class names */
<div className={`bg-[var(--hue-${hue})]`} />
```
