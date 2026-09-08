---
description: "WCAG AA requirements for UI components — focus management, ARIA attributes, reduced motion, form controls, and keyboard navigation for frontend applications"
when_to_use: "Read this index to find the right Accessibility Convention child document."
---

# Accessibility Convention

- [Accessibility — Contrast and Focus](./contrast-and-focus.md) — WCAG AA minimum contrast ratios for text and UI components, plus the focus-visible ring pattern for keyboard-only focus indication Use when choosing colors for text/UI elements, or when implementing focus rings on interactive elements.
- [Accessibility — Reduced Motion and ARIA Attributes](./reduced-motion-and-aria-attributes.md) — Honoring the prefers-reduced-motion media query, and the required ARIA attributes for each common component type (button, dialog, input, menu, tooltip, tab list, progress) Use when adding an animation/transition, or when building any component that needs ARIA attributes (buttons, dialogs, inputs, menus, tooltips, tabs, progress bars).
- [Accessibility — Form Inputs and Hit Targets](./form-inputs-and-hit-targets.md) — Visible label requirements, autoComplete and inputMode values for common fields, and minimum touch target sizes for desktop and mobile Use when building any form input, select, or textarea, or any tappable interactive element.
- [Accessibility — Color and Images](./color-and-images.md) — Never rely on color alone to convey status/error/success state, and the alt-text requirements for informative, decorative, and complex-diagram images Use when adding a status/error/success indicator, a status badge, or any image to a UI component.
- [Accessibility — Screen Readers and Keyboard Navigation](./screen-readers-and-keyboard-navigation.md) — DOM-order/reading-order matching, descriptive link text, skip navigation, aria-live regions, and the full keyboard interaction table including focus traps for dialogs Use when reviewing a component's screen-reader behaviour, or implementing keyboard interaction for menus, tabs, dialogs, or lists.
