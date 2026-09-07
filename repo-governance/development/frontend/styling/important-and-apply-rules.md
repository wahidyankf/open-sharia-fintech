---
description: Never use !important (with one documented, currently-necessary exception involving rehype-pretty-code inline styles), and @apply only inside @layer base
when_to_use: Use when tempted to reach for !important or @apply outside a base-layer reset.
---

# !important and @apply Rules

## No `!important`

Never use `!important`. Use `@layer` ordering or Tailwind modifiers for specificity control instead.

```css
/* Wrong */
.prose pre {
  background-color: #f6f8fa !important;
}

/* Correct — place outside @layer to beat Tailwind defaults */
.prose pre {
  background-color: #f6f8fa;
}
```

**Known violation (revisited 2026-07-22)**: `ayokoding-www/src/app/globals.css` contains 10
`!important` declarations in code block styles. The rules are already placed outside `@layer base`
(the fix this note originally called for), yet the `!important` on the
`figure[data-rehype-pretty-code-figure] pre` background rules cannot be dropped by cascade-ordering
alone: `rehype-pretty-code`'s `keepBackground: true` option
(`apps/ayokoding-www/src/features/content/core/parser.ts`) writes an inline
`style="--shiki-light-bg:#fff"` attribute on every code block, and an element's inline `style`
attribute always outranks any external stylesheet rule regardless of `@layer`/source order — only
`!important` (or removing the inline style at its source) can override it. Dropping the
`!important` here was tried and reverted as a real regression (DWT-001, tracked in
`plans/done/2026-07-16__web-ui-code-block-copy-button/learnings.md`): the light-theme code
background rendered pure white instead of the intended `#f6f8fa`. Full removal requires reworking
the `rehype-pretty-code` config (e.g. disabling `keepBackground`) — a design change, not a
mechanical CSS edit — so this is tracked as deliberate, currently-necessary debt rather than
"scheduled for removal" on any near-term timeline.

## No `@apply` Outside `@layer base`

Use `@apply` only inside `@layer base` for base/reset styles. Using `@apply` inside component styles defeats the utility-first approach and creates hidden CSS dependencies.

```css
/* Correct — @apply inside @layer base */
@layer base {
  body {
    @apply bg-background text-foreground;
  }
}

/* Wrong — @apply in component styles */
.my-button {
  @apply rounded-lg bg-primary px-4 py-2 text-white;
}
```
