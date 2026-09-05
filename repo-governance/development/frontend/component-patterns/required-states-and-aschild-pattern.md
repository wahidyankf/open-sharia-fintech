---
title: "Component Patterns — Required States and the asChild Pattern"
description: The full state-coverage table (default, hover, focus-visible, active, disabled, loading, error, success) via Tailwind modifiers, and delegating rendering to a consumer element via Slot.Root
category: explanation
subcategory: development/frontend
tags:
  - components
  - react
  - radix
  - cva
  - shadcn
created: 2026-03-28
when_to_use: Use when styling an interactive component's states, or when a component needs to merge its behaviour onto an arbitrary consumer element.
---

# Required States and the asChild Pattern

## Required States

Every interactive component must cover all meaningful states via Tailwind variant classes:

| State         | Tailwind Modifier                    |
| ------------- | ------------------------------------ |
| Default       | Base classes in `cva()`              |
| Hover         | `hover:`                             |
| Focus-visible | `focus-visible:`                     |
| Active        | `active:`                            |
| Disabled      | `disabled:` (+ `aria-disabled:`)     |
| Loading       | `data-loading:` or `aria-busy:`      |
| Error         | `aria-invalid:` (+ ring color token) |
| Success       | `data-success:` or `aria-checked:`   |

Encode all state styles in the `cva()` base string or in named variants — never apply state classes conditionally with template literals.

## `asChild` Pattern

The `asChild` prop delegates rendering to the consumer's element via `Slot.Root`. Use it when the component must merge its behaviour onto an arbitrary element (e.g., wrapping a Next.js `Link` in a `Button`).

```tsx
import { Slot } from "radix-ui";

const Comp = asChild ? Slot.Root : "button";
return <Comp data-slot="button" className={cn(buttonVariants({ variant, size, className }))} {...props} />;
```

```tsx
// Consumer usage — renders an <a> with button styles
<Button asChild>
  <Link href="/dashboard">Go to Dashboard</Link>
</Button>
```
