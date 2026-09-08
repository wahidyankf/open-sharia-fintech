---
description: "Provides the pre-publish checklist confirming palette, borders, contrast, and testing requirements are all met."
when_to_use: "Use as a final checklist immediately before committing content that uses color."
---

# Verification Checklist

Use this checklist before considering color usage complete:

- [ ] Only colors from verified palette used (Blue, Orange, Teal, Purple, Brown, Black, White, Gray)
- [ ] No red, green, yellow, or bright magenta colors used
- [ ] Black borders (#000000) included on all color-filled elements
- [ ] White text (#FFFFFF) on dark fills, black text (#000000) on light fills
- [ ] Hex color codes used (not CSS color names)
- [ ] Documentation comment above diagram explaining color scheme
- [ ] Tested in Coblis simulator (protanopia, deuteranopia, tritanopia)
- [ ] Contrast ratios verified with WebAIM checker
- [ ] Light mode tested (white background)
- [ ] Dark mode tested (dark background)
- [ ] Shape differentiation sufficient (not color-only)
- [ ] Text labels clear and descriptive
- [ ] Diagram remains understandable in grayscale
