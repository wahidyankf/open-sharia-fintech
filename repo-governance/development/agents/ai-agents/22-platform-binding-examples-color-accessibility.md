---
title: "Platform Binding Examples — Color Accessibility for Agent Identification"
description: "Covers multiple identification methods and accessible color-palette verification for agent colors."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when verifying that an agent's assigned color remains distinguishable for accessibility.
---

# Platform Binding Examples — Color Accessibility for Agent Identification

**CRITICAL**: Colored square emojis (🟦🟩🟨🟪) provide visual categorization but are SUPPLEMENTARY to semantic information. Agents must be identifiable without relying on color perception.

## Multiple Identification Methods

Agents are identified through FIVE independent methods:

| Identification Method | Example                          | Purpose                                   |
| --------------------- | -------------------------------- | ----------------------------------------- |
| **Agent Name**        | "docs-maker"                     | Primary text-based identifier             |
| **Role Suffix**       | "-maker" (maker)                 | Indicates category through naming pattern |
| **Emoji Shape**       | 🟦 (square)                      | Shape differentiation (not color)         |
| **Description**       | "Expert documentation writer..." | Semantic purpose statement                |
| **Color Field**       | `color: blue`                    | Text value in frontmatter                 |

**Users with color blindness can identify agents by:**

- Reading the agent name
- Recognizing the role suffix pattern (-maker, -checker, -fixer, -dev, -deployer, -manager)
- Seeing that the emoji is a square (shape, not color)
- Reading the description field

**Color perception is NOT required** to use agents effectively.

## Accessible Color Palette Verification

All agent colors are from the verified accessible palette:

| Color  | Emoji | Hex Code | WCAG AA (Light) | WCAG AA (Dark) | Safe For               |
| ------ | ----- | -------- | --------------- | -------------- | ---------------------- |
| Blue   | 🟦    | #0173B2  | PASS: 4.88:1    | PASS: 4.30:1   | All types (excellent)  |
| Green  | 🟩    | #029E73  | PASS: 4.67:1    | PASS: 4.50:1   | All types (good)       |
| Yellow | 🟨    | #F1C40F  | 3.51:1          | 2.99:1         | All types (moderate)\* |
| Purple | 🟪    | #CC78BC  | PASS: 3.65:1    | PASS: 5.74:1   | All types (moderate)   |

\*Yellow emoji (#F1C40F) has slightly lower contrast but remains distinguishable because it's combined with:

- Square shape (not relying on color alone)
- Text label "Fixer"
- Role suffix "-fixer"

**Source**: Verified through ColorBrewer2, Paul Tol's schemes, and WCAG testing. See [Color Accessibility Convention](../../../conventions/formatting/color-accessibility.md) - the master reference for all color usage - for complete palette details, scientific verification sources, testing methodology, and WCAG compliance standards.

## Why These Colors Were Chosen

1. **Protanopia & Deuteranopia (red-green blindness)**: Blue, yellow, and purple remain distinct. We avoid red and green entirely.
2. **Tritanopia (blue-yellow blindness)**: Blue appears pink, yellow appears light pink, but shape and text differentiation ensure identification.
3. **WCAG AA Compliance**: All colors meet minimum contrast requirements against both light and dark backgrounds.
4. **Cross-Platform Consistency**: Colors render consistently across GitHub, VS Code, and terminals.
