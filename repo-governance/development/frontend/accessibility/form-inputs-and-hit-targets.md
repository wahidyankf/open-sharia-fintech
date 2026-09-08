---
description: Visible label requirements, autoComplete and inputMode values for common fields, and minimum touch target sizes for desktop and mobile
when_to_use: Use when building any form input, select, or textarea, or any tappable interactive element.
---

# Form Inputs and Hit Targets

## Form Input Requirements

Every `<input>`, `<select>`, and `<textarea>` requires a visible `<label>` element linked via matching `htmlFor` / `id` pair. Placeholder text does not substitute for a label — placeholders disappear on input and have insufficient contrast in many browsers.

```tsx
// Correct — visible label linked to input
<label htmlFor="username">Username</label>
<input id="username" type="text" autoComplete="username" />

// Wrong — placeholder as label substitute
<input type="text" placeholder="Username" />
```

Add `autoComplete` for common fields to support password managers and autofill:

| Field        | `autoComplete` value |
| ------------ | -------------------- |
| Full name    | `name`               |
| Email        | `email`              |
| Phone        | `tel`                |
| Street       | `address-line1`      |
| City         | `address-level2`     |
| Postal code  | `postal-code`        |
| New password | `new-password`       |

Add `inputMode` for mobile keyboards to show the appropriate input type:

```tsx
<input inputMode="numeric" pattern="[0-9]*" /> // number pad
<input inputMode="email" type="email" />        // email keyboard
<input inputMode="tel" type="tel" />            // phone keyboard
<input inputMode="url" type="url" />            // url keyboard
```

## Hit Targets

Interactive elements must meet minimum touch target sizes:

- **Desktop**: 24 × 24 px minimum (WCAG 2.2 Target Size, Level AA)
- **Mobile viewports** (≤768px): 44 × 44 px minimum

Use padding to extend hit area without changing visual size:

```tsx
// Icon button — padding extends hit target to 44px on mobile
<button className="p-2 md:p-1">
  <SearchIcon className="h-5 w-5" aria-hidden="true" />
</button>
```

Verify actual rendered sizes in browser DevTools before merging compact UI components.
