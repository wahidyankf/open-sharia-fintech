---
title: "Purpose"
description: "States why color accessibility matters and lists the five core rules for using color across the repository."
when_to_use: "Use when applying or auditing the five core color-accessibility rules before adding color to any content."
category: explanation
subcategory: conventions
tags:
  - accessibility
  - color-blindness
  - wcag
  - design
  - conventions
  - mermaid-diagrams
  - color-palette
created: 2025-12-04
---

# Purpose

Color accessibility matters because:

- **8% of males** and **0.5% of females** have some form of color blindness
- **~300 million people worldwide** are affected by color vision deficiency
- Affects **three distinct types** of color blindness:
  - **Protanopia (red-blindness)**: Cannot distinguish red/green, sees them as brownish-yellow
  - **Deuteranopia (green-blindness)**: Cannot distinguish red/green, sees them as brownish-yellow
  - **Tritanopia (blue-yellow blindness)**: Cannot distinguish blue/yellow, sees blues as pink and yellows as light pink

Beyond accessibility compliance, color-blind friendly palettes benefit everyone by providing:

- Clearer visual distinction through better contrast
- More professional and polished appearance
- Universal usability across different viewing conditions
- Future-proof design that works in any lighting or display context

All color usage in this repository must follow these principles:

## 1. Never Rely on Color Alone

**Never** use color as the only method to convey information. Always combine color with: - **Text labels** - Clear, descriptive names or descriptions - **Shape differentiation** - Different node shapes, line styles, or patterns - **Position/location** - Spatial organization that provides context - **Icons or symbols** - Additional visual markers

**Example:**

- FAIL: Bad: Red node means "error" (color only)
- PASS: Good: Red circle labeled "Error" with error icon (color + shape + text + symbol)

## 2. Use Color as Supplementary Enhancement

Color should enhance and reinforce information that is already conveyed through other means. A person viewing the diagram in grayscale should still understand it completely.

## 3. Maintain Sufficient Contrast

All colors must provide sufficient contrast ratios to meet WCAG AA standards:

- **Normal text**: 4.5:1 minimum contrast ratio
- **Large text (18pt+ or 14pt+ bold)**: 3:1 minimum contrast ratio
- **UI components and graphics**: 3:1 minimum contrast ratio

Contrast is measured against both light and dark backgrounds.

## 4. Work in Both Light and Dark Modes

All colors must be tested and verified to work in:

- **Light mode background**: White (#FFFFFF)
- **Dark mode background**: Dark gray (#1E1E2E)

Colors should not require adjustment between light and dark modes.

## 5. Test with Color Blindness Simulators

Before publishing content with colors:

1. Create or design the content using the accessible palette
2. Test in at least one color blindness simulator (protanopia, deuteranopia, or tritanopia)
3. Verify contrast ratios meet WCAG AA standards
4. Confirm shape differentiation is sufficient
5. Test in both light and dark modes
