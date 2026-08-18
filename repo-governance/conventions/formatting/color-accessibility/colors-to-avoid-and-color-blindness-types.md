---
title: "Colors to Avoid and Color Blindness Types"
description: "Lists prohibited colors and combinations, and explains how each color blindness type perceives them."
when_to_use: "Use when checking whether a proposed color or color combination is unsafe for color-blind users."
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

# Colors to Avoid and Color Blindness Types

## Colors to Avoid

**CRITICAL**: Never use these colors in any context where color is meant to convey information:

| Color                  | Hex Code                  | Problem                                                   | Affects Type(s)          |
| ---------------------- | ------------------------- | --------------------------------------------------------- | ------------------------ |
| Red                    | #FF0000, #E74C3C, #DC143C | Completely invisible or appears brownish-yellow           | Protanopia, Deuteranopia |
| Green                  | #00FF00, #27AE60, #2ECC71 | Completely invisible or appears brownish-yellow           | Protanopia, Deuteranopia |
| Yellow                 | #FFFF00, #F1C40F          | Invisible or severely compromised visibility              | Tritanopia               |
| Light Pink             | #FF69B4, #FFC0CB          | Severely compromised visibility, appears light pink/white | Tritanopia               |
| Bright Magenta         | #FF00FF, #FF1493          | Difficult to distinguish, problematic appearance          | All types                |
| Red-Green Combinations | Any red + any green       | Creates impossible contrast for red/green blindness       | Protanopia, Deuteranopia |

### Why Each Is Problematic

**Red and Green**: Account for ~99% of color blindness cases. Red-blind and green-blind individuals cannot distinguish between these colors; both appear as brownish-yellow. Red-green combinations create complete information loss for these users.

**Yellow**: Invisible to tritanopia (blue-yellow blindness). Users see it as a very light color or off-white, indistinguishable from background.

**Light Pink/Magenta**: Causes confusion and reduced visibility for tritanopia users. Pink appears as light pink or white, defeating color coding.

**Bright Magenta**: Problematic for all color blindness types. Difficult to distinguish and renders inconsistently.

## Color Blindness Type Guidance

### Protanopia (Red-Blindness)

**Who it affects**: ~1% of males, rare in females

**How it appears**: Red and green both appear as brownish-yellow; reds appear darker, greens appear lighter in the brownish spectrum

**Safe palette**: All colors in the verified palette work perfectly (Blue, Orange, Teal, Purple, Brown)

**Testing tool**: [Coblis Protanopia Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/)

### Deuteranopia (Green-Blindness)

**Who it affects**: ~1% of males, rare in females

**How it appears**: Red and green both appear as brownish-yellow; similar appearance to protanopia but with slightly different perception of the brownish spectrum

**Safe palette**: All colors in the verified palette work perfectly (Blue, Orange, Teal, Purple, Brown)

**Testing tool**: [Coblis Deuteranopia Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/)

### Tritanopia (Blue-Yellow Blindness)

**Who it affects**: ~0.001% of population, extremely rare, usually inherited or acquired

**How it appears**: Blue appears as pink or reddish-pink; yellow appears as light pink or off-white; dark colors remain distinguishable

**Safe palette**: All colors in the verified palette work safely (Blue, Orange, Teal, Purple, Brown all distinct from tritanopia perspective)

**Testing tool**: [Coblis Tritanopia Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/)
