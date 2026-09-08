---
description: "Conventions for CSS design tokens across frontend apps in the open-sharia-enterprise monorepo, covering structural shared tokens, per-app brand overrides, dark mode requirements, and Tailwind v4 integration."
when_to_use: "Read this index to find the right Design Tokens Convention child document."
---

# Design Tokens Convention

- [Design Tokens — Token Categories and Naming Convention](./token-categories-and-naming-convention.md) — Structural tokens (shared, not overridable) vs. brand tokens (per-app override), and the bare-HSL-variable plus Tailwind-theme-alias naming pattern Use when deciding whether a new value belongs in the shared structural set or a per-app brand override, or when naming a new token.
- [Design Tokens — Token Format and Dark Mode](./token-format-and-dark-mode.md) — The double-indirection and direct-value token formatting approaches (direct value is recommended), and the requirement that every visual token have a .dark counterpart Use when writing a new token's globals.css declaration, or adding dark-mode support for a token.
- [Design Tokens — Per-App Override and Usage](./per-app-override-and-usage.md) — How an app imports shared tokens and declares brand overrides in its own globals.css, and referencing tokens through Tailwind utility classes rather than raw CSS property access Use when a new app needs to declare its brand token overrides, or when writing component markup that consumes tokens.
- [Design Tokens — OKLCH Brand Tokens (OrganicLever)](./oklch-brand-tokens.md) — OrganicLever's warm OKLCH palette - why OKLCH over HSL, and the hue/ink/wash and warm-neutral token structure including dark mode Use when working on organiclever-app-web's token layer and need the OKLCH rationale or token structure.
- [Design Tokens — OKLCH Naming and Usage](./oklch-naming-and-usage.md) — The hue/ink/wash and warm-neutral naming convention for OKLCH tokens, the rule against hardcoding OKLCH literals, and how to apply a runtime-determined hue via inline style Use when naming a new OKLCH token, reviewing a component for hardcoded color literals, or building a component whose color varies at runtime.
- [Design Tokens — When to Create a New Token, and Anti-Patterns](./when-to-create-and-anti-patterns.md) — The three-question decision rule for tokenizing a value, and four common mistakes - hardcoded hex values, !important on token definitions, duplicated structural tokens, and partial dark mode coverage Use when deciding whether a repeated value warrants a new token, or when reviewing CSS for token-system violations.
