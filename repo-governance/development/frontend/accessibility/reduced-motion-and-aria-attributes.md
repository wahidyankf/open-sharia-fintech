---
description: Honoring the prefers-reduced-motion media query, and the required ARIA attributes for each common component type (button, dialog, input, menu, tooltip, tab list, progress)
when_to_use: Use when adding an animation/transition, or when building any component that needs ARIA attributes (buttons, dialogs, inputs, menus, tooltips, tabs, progress bars).
---

# Reduced Motion and ARIA Attributes

## Reduced Motion

Honor the `prefers-reduced-motion` media query. Users who configure this setting experience vestibular disorders or motion sensitivity — ignoring the preference causes real harm.

```tsx
// Tailwind — disable animation for reduced-motion users
<div className="animate-spin motion-reduce:animate-none" />

// Tailwind — simplify transition instead of removing entirely
<div className="transition-all duration-300 motion-reduce:transition-none" />
```

```css
/* CSS — for custom keyframe animations outside Tailwind */
@media (prefers-reduced-motion: reduce) {
  .animated-element {
    animation: none;
    transition: none;
  }
}
```

Remove or simplify animations; do not merely slow them down. A slow animation is still motion.

## ARIA Attributes by Component Type

| Component        | Required ARIA                                                             | Notes                                                         |
| ---------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Button           | `aria-label` (icon-only), `aria-disabled`, `aria-pressed` (toggles)       | Never use `div` or `span` as a button without `role="button"` |
| Dialog / Modal   | `aria-modal="true"`, `aria-labelledby`, `aria-describedby`                | Requires focus trap; return focus to trigger on close         |
| Input / Textarea | `aria-invalid`, `aria-describedby` (error message id), `aria-required`    | `aria-invalid="true"` only when validation has run and failed |
| Menu / Dropdown  | `aria-expanded`, `aria-haspopup="menu"`, `role="menu"`, `role="menuitem"` | Arrow keys must navigate items; Escape closes                 |
| Tooltip          | `role="tooltip"`, `aria-describedby` on trigger element                   | Must be visible on keyboard focus, not hover only             |
| Tab List         | `role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls`          | Arrow keys switch tabs; Tab moves into panel                  |
| Progress         | `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`   | Include `aria-label` if no visible label present              |

```tsx
// Icon-only button — requires aria-label
<button aria-label="Close dialog" className="...">
  <XIcon aria-hidden="true" />
</button>

// Toggle button — aria-pressed reflects state
<button aria-pressed={isActive} className="...">
  Bold
</button>

// Input with validation error
<div>
  <label htmlFor="email">Email</label>
  <input
    id="email"
    aria-invalid={hasError}
    aria-describedby={hasError ? "email-error" : undefined}
    aria-required
  />
  {hasError && (
    <span id="email-error" role="alert">
      Enter a valid email address
    </span>
  )}
</div>
```
