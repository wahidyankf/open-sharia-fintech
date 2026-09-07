---
description: React.ComponentProps over forwardRef, importing Radix from the unified radix-ui package, the data-slot attribute, and the cn() class-merging utility
when_to_use: Use when writing a new component's function signature, importing a Radix primitive, or merging class names.
---

# Component Pattern

## Use `React.ComponentProps`, Not `forwardRef`

All components use `React.ComponentProps<"element">` for prop spreading. Do NOT use `React.forwardRef` — React 19 passes refs as plain props, making `forwardRef` unnecessary.

```tsx
// Correct — React.ComponentProps, function declaration
function Button({
  className,
  variant = "default",
  size = "default",
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  }) {
  // ...
}

// Wrong — forwardRef (legacy pattern)
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    // ...
  },
);
Button.displayName = "Button";
```

## Import Radix from the Unified Package

Import all Radix primitives from `radix-ui` (the unified package), NOT from individual `@radix-ui/react-*` packages.

```tsx
// Correct — unified package
import { Slot, Dialog, DropdownMenu } from "radix-ui";

// Wrong — individual packages
import { Slot } from "@radix-ui/react-slot";
import * as Dialog from "@radix-ui/react-dialog";
```

**Note**: Always use `Slot.Root` (not bare `Slot`) when rendering the slot component. `Slot` is
imported as a namespace from the unified `radix-ui` package; `Slot.Root` is the composable element.

```tsx
// Correct
const Comp = asChild ? Slot.Root : "button";

// Wrong — bare Slot is a namespace, not a renderable element
const Comp = asChild ? Slot : "button";
```

## `data-slot` Attribute

Every component root element carries a `data-slot` attribute identifying the component part. This enables CSS selection and test targeting without relying on class names.

```tsx
<Comp data-slot="button" ... />
<div data-slot="card" ... />
<header data-slot="card-header" ... />
```

## `cn()` Utility

Merge class names with `cn()` from `src/lib/utils` (or `@/lib/utils`). Always pass `className` last so consumer overrides win.

```tsx
import { cn } from "src/lib/utils";

className={cn(buttonVariants({ variant, size, className }))}
```
