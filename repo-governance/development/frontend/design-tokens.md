---
title: Design Tokens Convention
description: Conventions for CSS design tokens across frontend apps in the open-sharia-enterprise monorepo, covering structural shared tokens, per-app brand overrides, dark mode requirements, and Tailwind v4 integration.
category: explanation
subcategory: development/frontend
tags:
  - design-tokens
  - css
  - tailwind
  - theming
  - dark-mode
created: 2026-03-28
when_to_use: Use when adding, naming, or overriding a CSS design token, or deciding whether a color/spacing value should be tokenized.
---

# Design Tokens Convention

Design tokens are the named CSS custom properties that form the shared visual vocabulary across all frontend applications in the monorepo. This document defines which tokens exist, how to name and format them, how apps override shared values, and what to avoid.

## Scope Clarification: Docs Palette vs UI Colors

The [Color Accessibility Convention](../../conventions/formatting/color-accessibility.md) defines a **5-color accessible palette** (`#0173B2`, `#DE8F05`, `#029E73`, `#CC78BC`, `#CA9161`) intended exclusively for documentation diagrams, Mermaid charts, and emoji categorization in `docs/` and `repo-governance/`.

That palette does **not** govern UI application colors. Frontend apps may use any colors provided they meet WCAG AA contrast requirements:

- Normal text: **4.5:1** minimum contrast ratio against its background
- Large text (18 pt / 14 pt bold): **3:1** minimum
- UI components and graphical elements: **3:1** minimum

The `color-accessibility` convention remains the master reference for diagrams. This document governs token-based color decisions within app CSS.

## Contents

- [Token Categories and Naming Convention](./design-tokens/token-categories-and-naming-convention.md) — structural vs. brand tokens, and the bare-variable/Tailwind-alias naming pattern.
- [Token Format and Dark Mode](./design-tokens/token-format-and-dark-mode.md) — the two current formatting approaches, and the required .dark counterpart for every token.
- [Per-App Override and Usage](./design-tokens/per-app-override-and-usage.md) — how an app overrides brand tokens, and referencing tokens through Tailwind utilities.
- [OKLCH Brand Tokens (OrganicLever)](./design-tokens/oklch-brand-tokens.md) — the warm OKLCH palette and hue/ink/wash token structure.
- [OKLCH Naming and Usage](./design-tokens/oklch-naming-and-usage.md) — the OKLCH naming convention, and dynamic runtime hue backgrounds.
- [When to Create a New Token, and Anti-Patterns](./design-tokens/when-to-create-and-anti-patterns.md) — the three-question decision rule, and four common token mistakes.

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Accessibility First](../../principles/content/accessibility-first.md)**: Every visual token requires a `.dark` counterpart and must meet WCAG AA contrast (4.5:1 text, 3:1 UI components) in both modes. Token-based theming makes contrast verification systematic rather than per-component.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Naming tokens by semantic role (`--primary`, `--muted-foreground`, `--destructive`) makes visual intent explicit. Raw hex values in components hide their meaning.
- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: The direct-value token format is preferred over double indirection. The per-app override pattern through CSS cascade avoids build-time configuration complexity.
- **[Immutability Over Mutability](../../principles/software-engineering/immutability.md)**: Structural tokens in `web-ui-token` are not overridden by apps. Only brand tokens vary per app, preserving the shared visual contract.

## Conventions Implemented/Respected

This document implements the following conventions:

- **[Color Accessibility Convention](../../conventions/formatting/color-accessibility.md)**: Clarifies that the 5-color docs palette governs diagrams only. UI apps follow WCAG AA contrast rules using any colors appropriate to their brand.
- **[Indentation Convention](../../conventions/formatting/indentation.md)**: All CSS examples in this document use 2-space indentation per the project CSS standard.
