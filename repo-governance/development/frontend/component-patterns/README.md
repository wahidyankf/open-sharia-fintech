---
description: "Standards for building UI components with CVA variants, Radix primitives, and React patterns"
when_to_use: "Read this index to find the right Component Patterns Convention child document."
---

# Component Patterns Convention

- [Component Patterns — Component Pattern](./component-pattern.md) — React.ComponentProps over forwardRef, importing Radix from the unified radix-ui package, the data-slot attribute, and the cn() class-merging utility Use when writing a new component's function signature, importing a Radix primitive, or merging class names.
- [Component Patterns — CVA Variants and Radix Composition](./cva-variants-and-radix-composition.md) — Defining component variants with cva() from class-variance-authority, and composing Radix sub-parts by importing the component namespace Use when defining a new set of component variants, or composing a multi-part Radix primitive (dialog, menu, tabs).
- [Component Patterns — Required States and the asChild Pattern](./required-states-and-aschild-pattern.md) — The full state-coverage table (default, hover, focus-visible, active, disabled, loading, error, success) via Tailwind modifiers, and delegating rendering to a consumer element via Slot.Root Use when styling an interactive component's states, or when a component needs to merge its behaviour onto an arbitrary consumer element.
- [Component Patterns — Complete Button Example](./complete-button-example.md) — The canonical ayokoding-www Button implementation combining React.ComponentProps, CVA variants, Slot.Root, and data-slot in one file Use as the reference implementation when building a new component from scratch, or migrating an existing forwardRef-based component.
