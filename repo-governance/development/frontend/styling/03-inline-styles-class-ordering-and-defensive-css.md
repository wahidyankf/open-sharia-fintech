---
title: "Styling — Inline Styles, Class Ordering, and Defensive CSS"
description: No inline style={} props (except temporary migrations), automatic Tailwind class sorting via prettier-plugin-tailwindcss, and defensive CSS patterns that prevent layout breakage
category: explanation
subcategory: development/frontend
tags:
  - styling
  - tailwind
  - css
  - responsive
  - mobile-first
created: 2026-03-28
when_to_use: Use when tempted to add an inline style prop, when Tailwind classes appear unsorted after save, or when a layout risks content overflow.
---

# Inline Styles, Class Ordering, and Defensive CSS

## No Inline `style={}` Props

Use Tailwind utilities instead of inline styles. Inline styles bypass the design token system and `prettier-plugin-tailwindcss` ordering.

```tsx
/* Wrong */
<div style={{ padding: "1rem", backgroundColor: "var(--card)" }}>

/* Correct */
<div className="bg-card p-4">
```

**Exception**: Apps migrating from a non-Tailwind baseline may use inline styles temporarily. Remove them before the migration is complete.

## Class Ordering

`prettier-plugin-tailwindcss` automatically sorts Tailwind classes into canonical order on save via the pre-commit hook. Do not sort classes manually.

For Tailwind v4, the plugin requires a `tailwindStylesheet` configuration option pointing to the app's `globals.css`:

```json
{
  "tailwindStylesheet": "./src/app/globals.css"
}
```

If classes appear unsorted after a save, verify that `tailwindStylesheet` points to the correct file for that app.

## Defensive CSS Patterns

Apply these patterns proactively to prevent layout breakage:

```tsx
/* Prevent content bleed from overflowing children */
<section className="overflow-hidden">

/* Prevent flex children from expanding past their container */
<div className="flex min-w-0 gap-4">
  <span className="min-w-0 truncate">Long title that might overflow</span>
</div>

/* Single-line text overflow with ellipsis */
<p className="truncate">Long text</p>

/* User-generated content that may contain long words or URLs */
<p className="break-words">User content here</p>
```
