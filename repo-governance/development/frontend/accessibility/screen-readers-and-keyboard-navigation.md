---
title: "Accessibility — Screen Readers and Keyboard Navigation"
description: DOM-order/reading-order matching, descriptive link text, skip navigation, aria-live regions, and the full keyboard interaction table including focus traps for dialogs
category: explanation
subcategory: development/frontend
tags:
  - accessibility
  - wcag
  - a11y
  - aria
  - focus
created: 2026-03-28
when_to_use: Use when reviewing a component's screen-reader behavior, or implementing keyboard interaction for menus, tabs, dialogs, or lists.
---

# Screen Readers and Keyboard Navigation

## Screen Reader Compatibility

- DOM order must match visual reading order. CSS `order`, `flex-direction: row-reverse`, and absolute positioning can create mismatches — verify with a screen reader.
- Link text must describe the destination, not the action. Use "View invoice INV-2025-001" not "Click here".
- Provide skip navigation for layouts with repeated headers or sidebars:

```tsx
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:bg-white focus:px-4 focus:py-2"
>
  Skip to main content
</a>
```

- Use `aria-live="polite"` for dynamic content updates (toast notifications, form validation results) so screen readers announce changes without interrupting the user.

## Keyboard Navigation

All interactive elements must follow these keyboard interaction patterns:

| Key        | Behavior                                           |
| ---------- | -------------------------------------------------- |
| Tab        | Move focus forward through interactive elements    |
| Shift+Tab  | Move focus backward                                |
| Enter      | Activate button, follow link, submit form          |
| Space      | Activate button, toggle checkbox                   |
| Escape     | Dismiss dialog, close dropdown, cancel action      |
| Arrow keys | Navigate within menus, tabs, radio groups, sliders |
| Home/End   | Move to first/last item in a list or menu          |

Dialogs require a **focus trap**: Tab and Shift+Tab must cycle only within the dialog while it is open. Return focus to the triggering element when the dialog closes.
