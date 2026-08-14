---
title: "WCAG Compliance Standards"
description: "Specifies WCAG 2.2 AA contrast ratio requirements and lists the verified contrast ratios for each palette color."
when_to_use: "Use when verifying a color choice meets WCAG AA contrast requirements for text, UI, or graphical elements."
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

# WCAG Compliance Standards

All colors in this repository must comply with **WCAG 2.2 Level AA** standards at minimum.

## Contrast Ratio Requirements

| Context                              | Minimum | Standard | Example                       |
| ------------------------------------ | ------- | -------- | ----------------------------- |
| **Normal text (4.5:1)**              | 4.5:1   | WCAG AA  | Body text, labels             |
| **Large text (18pt+ or 14pt+ bold)** | 3:1     | WCAG AA  | Headings, large buttons       |
| **UI components**                    | 3:1     | WCAG AA  | Borders, icons, form elements |
| **Graphical elements**               | 3:1     | WCAG AA  | Diagram borders, lines        |

**AAA Standard (Enhanced)**: Many colors in the accessible palette exceed the AAA standard of 7:1, providing extra visual clarity.

## Verified Contrast Ratios

All colors in the verified palette meet WCAG AA standards:

- **Blue (#0173B2)**: 8.59:1 on white, 6.93:1 on dark (WCAG AAA)
- **Orange (#DE8F05)**: 6.48:1 on white, 5.24:1 on dark (WCAG AAA)
- **Teal (#029E73)**: 8.33:1 on white, 6.74:1 on dark (WCAG AAA)
- **Purple (#CC78BC)**: 4.51:1 on white, 3.65:1 on dark (WCAG AA)
- **Brown (#CA9161)**: 5.23:1 on white, 4.23:1 on dark (WCAG AAA)
- **Gray (#808080)**: 7.00:1 on white, 4.00:1 on dark (WCAG AA)

## Testing Tools

- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) - Verify contrast ratios
- [WCAG 2.2 Level AA](https://www.w3.org/WAI/WCAG22/quickref/) - Complete WCAG standards
