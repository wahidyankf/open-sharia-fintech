---
title: "Design Tokens — When to Create a New Token, and Anti-Patterns"
description: The three-question decision rule for tokenizing a value, and four common mistakes - hardcoded hex values, !important on token definitions, duplicated structural tokens, and partial dark mode coverage
category: explanation
subcategory: development/frontend
tags:
  - design-tokens
  - css
  - tailwind
  - theming
  - dark-mode
created: 2026-03-28
when_to_use: Use when deciding whether a repeated value warrants a new token, or when reviewing CSS for token-system violations.
---

# When to Create a New Token, and Anti-Patterns

## When to Create a New Token

Use this decision rule before adding a token:

1. Is the value used in **3 or more places**? If no, use an existing token or a one-off value.
2. Does it represent a **semantic concept** (e.g., "sidebar background", "destructive action")? If no, it is likely a coincidental shared value — do not tokenize it.
3. Does an existing token already cover this semantic concept? If yes, use the existing token.

Only create a new token when all three conditions are met: repeated use, semantic meaning, and no existing token covers it. Tokenizing coincidental shared values creates false coupling between unrelated parts of the UI.

## Anti-Patterns

**Hardcoded hex values in component files**

```css
/* Wrong */
background-color: #f6f8fa;
color: #24292f;
```

These bypass the token system and break dark mode. Use `bg-muted` and `text-foreground` instead.

**`!important` on token definitions**

```css
/* Wrong */
:root {
  --primary: hsl(221.2 83.2% 53.3%) !important;
}
```

`!important` on custom properties prevents the CSS cascade from applying per-app overrides. Token composition depends on the cascade working correctly.

**Duplicating structural tokens in app `globals.css`**

```css
/* Wrong — do not copy-paste structural tokens from web-ui-token */
:root {
  --radius: 0.5rem;
  --space-4: 1rem;
}
```

Import `web-ui-token` and let the shared library own structural values. Duplicating them creates divergence risk when the shared library updates.

**Defining dark-mode values for only some tokens**

If a token appears in `:root`, it must also appear in `.dark`. Partial dark mode coverage creates inconsistent contrast and visual artifacts that are difficult to debug.
