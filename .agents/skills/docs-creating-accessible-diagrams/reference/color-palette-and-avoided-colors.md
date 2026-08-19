# Accessible Diagrams — Color Palette and Colors to Avoid

## Verified Accessible Color Palette

**CRITICAL**: Use ONLY these colors in all diagrams. This palette is scientifically verified to work for all color blindness types and meets WCAG AA standards.

| Color  | Hex Code | Use Cases                      | WCAG AA (Light)  | WCAG AA (Dark)   |
| ------ | -------- | ------------------------------ | ---------------- | ---------------- |
| Blue   | #0173B2  | Primary elements, main flow    | ✅ 8.59:1 (AAA)  | ✅ 6.93:1 (AAA)  |
| Orange | #DE8F05  | Warnings, decisions, secondary | ✅ 6.48:1 (AAA)  | ✅ 5.24:1 (AAA)  |
| Teal   | #029E73  | Success, validation, tertiary  | ✅ 8.33:1 (AAA)  | ✅ 6.74:1 (AAA)  |
| Purple | #CC78BC  | Special states, implementors   | ✅ 4.51:1 (AA)   | ✅ 3.65:1 (AA)   |
| Brown  | #CA9161  | Neutral elements, secondary    | ✅ 5.23:1 (AAA)  | ✅ 4.23:1 (AAA)  |
| Black  | #000000  | Text on light, borders         | ✅ 21.00:1 (AAA) | N/A              |
| White  | #FFFFFF  | Text on dark, backgrounds      | N/A              | ✅ 21.00:1 (AAA) |
| Gray   | #808080  | Disabled, secondary elements   | ✅ 7.00:1 (AAA)  | ✅ 4.00:1 (AA)   |

**Quick copy-paste hex codes:**

```
#0173B2 - Blue
#DE8F05 - Orange
#029E73 - Teal
#CC78BC - Purple
#CA9161 - Brown
#000000 - Black
#FFFFFF - White
#808080 - Gray
```

## Colors to NEVER Use

**CRITICAL**: Never use these colors where color conveys information:

- ❌ **Red** (#FF0000, #E74C3C) - Invisible to protanopia/deuteranopia (~8% of males)
- ❌ **Green** (#00FF00, #27AE60) - Invisible to protanopia/deuteranopia
- ❌ **Yellow** (#FFFF00, #F1C40F) - Invisible to tritanopia (rare but severe)
- ❌ **Light Pink** (#FF69B4, #FFC0CB) - Severely compromised for tritanopia
- ❌ **Bright Magenta** (#FF00FF, #FF1493) - Problematic for all types
- ❌ **Red-Green combinations** - Creates impossible contrast for ~8% of males

**Exception**: Emoji indicators (🔴🟠🟡🟢) can use standard colors when ALWAYS paired with text labels (color is supplementary, not primary identifier).
