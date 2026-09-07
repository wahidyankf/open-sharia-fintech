---
description: Mobile-first breakpoints (375px/768px/1280px), container queries for component-relative layout, and the 44×44px minimum tap target for mobile viewports
when_to_use: Use when building any responsive layout, or sizing an interactive element for mobile.
---

# Responsive Design and Touch Targets

## Responsive Design — Mobile-First

Start with mobile styles (no breakpoint prefix) and layer larger screens with `md:` and `lg:`.

**Standard breakpoints:**

| Prefix | Min-width | Target  |
| ------ | --------- | ------- |
| (none) | 375px     | Mobile  |
| `md:`  | 768px     | Tablet  |
| `lg:`  | 1280px    | Desktop |

```tsx
/* Correct — mobile-first */
<div className="flex flex-col gap-4 md:flex-row md:gap-6 lg:gap-8">

/* Wrong — desktop-first (requires max-width overrides) */
<div className="flex flex-row gap-8 max-md:flex-col">
```

All components must render correctly at all three breakpoints. Test on a 375px viewport before considering a component complete.

**Prefer container queries** when a component's layout depends on the space available to it rather than the viewport width:

```tsx
<div className="@container">
  <div className="flex flex-col @md:flex-row">{/* Layout adapts to container width, not screen width */}</div>
</div>
```

## Touch Targets

Interactive elements (buttons, links, form controls) must have a minimum tap target of 44×44px on mobile viewports, per the [Accessibility First](../../../principles/content/accessibility-first.md) principle.

```tsx
/* Correct — explicit minimum size */
<button className="min-h-[44px] min-w-[44px] px-4 py-2">
  Submit
</button>

/* Correct — padding produces a large enough target */
<a className="block px-4 py-3 text-sm">
  Navigation link
</a>
```

Verify touch target sizes at the 375px breakpoint.
