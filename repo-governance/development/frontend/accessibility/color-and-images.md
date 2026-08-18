---
title: "Accessibility — Color and Images"
description: Never rely on color alone to convey status/error/success state, and the alt-text requirements for informative, decorative, and complex-diagram images
category: explanation
subcategory: development/frontend
tags:
  - accessibility
  - wcag
  - a11y
  - aria
  - focus
created: 2026-03-28
when_to_use: Use when adding a status/error/success indicator, a status badge, or any image to a UI component.
---

# Color and Images

## No Color-Only Indicators

Status, errors, warnings, and success states MUST include text labels and/or distinct shapes. Never rely on color alone — approximately 8% of males cannot distinguish red from green.

```tsx
// Correct — color + icon + text label
<span className="text-amber-700 flex items-center gap-1">
  <WarningIcon aria-hidden="true" />
  Incomplete — missing required fields
</span>

// Wrong — color alone conveys error state
<span className="text-red-500">3 errors</span>
```

For status badges, combine background color with a text label or icon:

```tsx
// Correct — shape (badge) + text + color
<Badge variant="destructive">Failed</Badge>
<Badge variant="success">Published</Badge>

// Wrong — colored dot only
<span className="h-2 w-2 rounded-full bg-red-500" />
```

## Image Accessibility

- **Informative images**: Write descriptive `alt` text that conveys the image's meaning, not just its appearance. Include text visible in the image if it is not already in surrounding content.
- **Decorative images**: Use `alt=""` so screen readers skip them. Never omit the `alt` attribute entirely.
- **Complex diagrams**: Supplement with a text summary below the image or via `aria-describedby`.

```tsx
// Informative image
<img
  src="/charts/revenue.png"
  alt="Bar chart showing Q1–Q4 revenue with Q3 peak at $2.4M"
/>

// Decorative image
<img src="/decorations/wave.svg" alt="" />
```
