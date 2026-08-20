# Accessible Diagrams — Core Accessibility Principles

## 1. Never Rely on Color Alone

Always combine color with:

- ✅ **Text labels** - Clear descriptions
- ✅ **Shape differentiation** - Different node shapes (rectangles, diamonds, circles)
- ✅ **Line styles** - Solid, dashed, dotted
- ✅ **Position** - Spatial organization
- ✅ **Icons** - Additional visual markers

**Example:**

- ❌ Bad: Red node means "error" (color only)
- ✅ Good: Orange diamond labeled "Error State" with error icon

## 2. Use Color as Enhancement

Color should enhance information already conveyed through other means. A grayscale version should remain understandable.

## 3. Maintain WCAG AA Contrast

All text and UI components must meet minimum contrast:

- Normal text: 4.5:1 minimum
- Large text (18pt+ or 14pt+ bold): 3:1 minimum
- UI components/graphics: 3:1 minimum

## 4. Test for Color Blindness

Before publishing diagrams:

1. Create using accessible palette
2. Test in color blindness simulator (protanopia, deuteranopia, tritanopia)
3. Verify contrast ratios with WebAIM checker
4. Confirm shape differentiation sufficient
5. Test in both light and dark modes
