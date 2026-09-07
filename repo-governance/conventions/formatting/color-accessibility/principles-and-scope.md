---
description: "Explains the accessibility and simplicity principles behind this convention plus what it covers and excludes."
when_to_use: "Use when you need to understand why this color accessibility convention exists or what falls inside/outside its scope."
---

# Principles and Scope

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Accessibility First](../../../principles/content/accessibility-first.md)**: Color accessibility is a fundamental accessibility requirement. This entire convention exists to ensure users with color blindness (8% of males, 0.5% of females, ~300 million people worldwide) can perceive all visual information. By requiring color-blind friendly palettes, sufficient contrast ratios (WCAG AA), and never relying on color alone, we make our documentation and visualizations universally accessible.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Rather than maintaining multiple color palettes for different contexts or allowing arbitrary color choices, we provide a single verified accessible palette (8 colors) that works for all use cases. One palette, tested once, used everywhere. No per-context adjustments needed between light and dark modes.

## Scope

### What This Convention Covers

- **Color-blind friendly palette** - Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161
- **Palette application** - When and how to use each color
- **WCAG AA compliance** - Contrast ratios and accessibility requirements
- **Context-specific rules** - Different requirements for diagrams vs. indicators
- **Tool-specific guidance** - Mermaid, HTML, CSS color usage
- **Testing accessibility** - How to verify color accessibility

### What This Convention Does NOT Cover

- **Brand colors** - Marketing or brand identity (this is functional accessibility)
- **UI design** - Application interface colors (covered in app-specific design docs)
- **Print colors** - CMYK or print-specific color spaces
- **Dynamic theming** - Light/dark mode switching (implementation detail)
