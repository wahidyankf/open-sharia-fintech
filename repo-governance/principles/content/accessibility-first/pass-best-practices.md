---
description: Actionable best practices for accessible color palettes, testing, contrast verification, alt text, headings, and multi-cue design.
when_to_use: Use as a checklist when producing or reviewing visual content, diagrams, or documents for accessibility.
---

# PASS: Best Practices

## 1. Always Use Accessible Color Palette

**For all visual content** - diagrams, styling, UI:

```css
/* Only use these verified accessible colors */
#0173B2  /* Blue */
#DE8F05  /* Orange */
#029E73  /* Teal */
#CC78BC  /* Purple */
#CA9161  /* Brown */
#000000  /* Black */
#FFFFFF  /* White */
#808080  /* Gray */
```

**Never use**: Red, green, yellow, bright magenta, or any colors outside the verified palette.

## 2. Test with Color Blindness Simulators

**Before publishing**, test all visual content:

1. Open [Coblis Color Blindness Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/)
2. Upload diagram or screenshot
3. Test all three types: Protanopia, Deuteranopia, Tritanopia
4. Verify elements remain distinguishable
5. Confirm shape differentiation is sufficient

## 3. Verify Contrast Ratios

**For all text and UI elements**:

1. Open [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
2. Enter foreground and background colors
3. Verify WCAG AA compliance (4.5:1 for normal text, 3:1 for large text)
4. Adjust colors if needed

## 4. Write Descriptive Alt Text

**For every image**:

- Describe what the image shows
- Explain why it's relevant
- Keep it concise (1-2 sentences)
- Avoid "image of" or "picture of"
- Include text from image if important

## 5. Use Proper Heading Structure

**For all documents**:

- Single H1 (document title)
- Logical H2-H6 hierarchy
- No skipped levels
- Descriptive heading text
- Headings for structure, not styling

## 6. Combine Multiple Visual Cues

**Never rely on a single visual cue**:

- PASS: Color + shape + text label
- PASS: Color + icon + position
- FAIL: Color alone
- FAIL: Shape alone without labels
