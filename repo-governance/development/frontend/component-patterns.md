---
title: Component Patterns Convention
description: Standards for building UI components with CVA variants, Radix primitives, and React patterns
category: explanation
subcategory: development/frontend
tags:
  - components
  - react
  - radix
  - cva
  - shadcn
created: 2026-03-28
when_to_use: Use when creating or reviewing any UI component in ayokoding-www or organiclever-app-web.
---

# Component Patterns Convention

Standards for building UI components in the open-sharia-enterprise monorepo. These rules govern how components are structured, composed, and styled across `ayokoding-www` and `organiclever-app-web`.

## File Structure

Each non-trivial UI component lives in its own directory:

```
components/ui/button/
├── button.tsx          # Component implementation
├── button.variants.ts  # CVA variant definitions
├── button.test.tsx     # Unit tests (Vitest + Testing Library)
└── button.stories.tsx  # Storybook stories
```

Simple, single-variant components may colocate the variant definition inline in `.tsx`. Extract to `.variants.ts` when the `cva()` call exceeds approximately 10 lines or when multiple components share variants.

## Contents

- [Component Pattern](./component-patterns/component-pattern.md) — React.ComponentProps over forwardRef, the unified radix-ui import, data-slot, and cn().
- [CVA Variants and Radix Composition](./component-patterns/cva-variants-and-radix-composition.md) — defining variants with cva(), and composing Radix sub-parts.
- [Required States and the asChild Pattern](./component-patterns/required-states-and-aschild-pattern.md) — the full state-coverage table, and delegating rendering via Slot.Root.
- [Complete Button Example](./component-patterns/complete-button-example.md) — the canonical ayokoding-www Button implementation.

## Principles Implemented/Respected

- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) — `React.ComponentProps` eliminates the `forwardRef` wrapper boilerplate. CVA centralizes all variant logic in one declarative object instead of scattered conditional class strings.
- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) — `data-slot` attributes make component structure visible to CSS and tests. `VariantProps` exports make the full variant surface area explicit at the type level.
- [Progressive Disclosure](../../principles/content/progressive-disclosure.md) — The `asChild` prop exposes composition capability only when needed. Consumers start with the default element and opt into polymorphism explicitly.

## Conventions Implemented/Respected

- [Styling Convention](../frontend/styling.md) — All variant class strings use Tailwind utilities and follow the utility-first approach. No `@apply` or inline `style={}` props appear in component implementations.
- [Design Tokens Convention](../frontend/design-tokens.md) — Variant classes reference semantic tokens (`bg-primary`, `text-destructive`, `ring-ring`) rather than raw color values, ensuring design token governance is respected throughout.
- [Indentation Convention](../../conventions/formatting/indentation.md) — All TypeScript and TSX examples in this document use 2-space indentation per the project standard.
