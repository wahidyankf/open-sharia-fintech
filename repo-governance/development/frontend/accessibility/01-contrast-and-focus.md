---
title: "Accessibility — Contrast and Focus"
description: WCAG AA minimum contrast ratios for text and UI components, plus the focus-visible ring pattern for keyboard-only focus indication
category: explanation
subcategory: development/frontend
tags:
  - accessibility
  - wcag
  - a11y
  - aria
  - focus
created: 2026-03-28
when_to_use: Use when choosing colors for text/UI elements, or when implementing focus rings on interactive elements.
---

# Contrast and Focus

## WCAG AA Minimum Requirements

All UI components must satisfy these contrast ratios:

| Text / Element Type                          | Minimum Contrast |
| -------------------------------------------- | ---------------- |
| Normal text (below 18px regular, 14px bold)  | 4.5:1            |
| Large text (18px+ regular or 14px+ bold)     | 3:1              |
| UI components (inputs, buttons, focus rings) | 3:1              |
| Graphical objects that convey meaning        | 3:1              |

Verify contrast ratios with [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) before merging any new color values.

**Preferred algorithm**: APCA (Accessible Perceptual Contrast Algorithm) is preferred over WCAG 2.0 for perceptual accuracy on modern displays. When tooling supports it (e.g., Figma APCA plugin, Polychrome), use APCA. WCAG AA (4.5:1 / 3:1) remains the enforceable floor.

## Focus Management

Every interactive element must be reachable via Tab and activatable via Enter or Space.

**Use `focus-visible`, not `focus`**. The `focus` pseudo-class shows a focus ring on mouse click, which is visually noisy and not needed for pointer users. `focus-visible` limits the ring to keyboard navigation only.

```tsx
// Tailwind — correct focus ring pattern
<button className="focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:outline-none">
  Submit
</button>
```

```tsx
// Tailwind — wrong: shows ring on mouse click too
<button className="focus:ring-2 focus:ring-blue-500">Submit</button>
```

Focus rings must meet 3:1 contrast against the adjacent background. Use `ring-offset-2` to create separation from the element's own background, especially on dark surfaces.
