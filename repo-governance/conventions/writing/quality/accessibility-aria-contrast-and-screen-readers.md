---
description: "When to use ARIA labels, required color-contrast ratios, and structuring content for screen-reader comprehension"
when_to_use: "Read this when adding custom HTML/ARIA to markdown, styling a diagram, or reviewing content for screen-reader friendliness."
---

# Accessibility: ARIA, Color Contrast, and Screen Readers

## ARIA Labels and Accessibility Attributes

**Use ARIA labels when HTML alone is insufficient** for accessibility.

**When to use ARIA**:

- Complex interactive components
- Custom widgets or controls
- Additional context for screen readers
- Landmark regions in documentation

**Example (Using HTML with ARIA in documentation)**:

```html
<details>
  <summary aria-label="Expand to see advanced configuration options">Advanced Configuration</summary>
  <p>Advanced options content here...</p>
</details>
```

**Note**: In most cases, proper markdown structure provides sufficient accessibility. Use ARIA sparingly and only when semantic HTML is insufficient.

## Color Contrast

**Ensure sufficient color contrast** in diagrams and custom styling.

**Reference**: [Color Accessibility Convention](../../formatting/color-accessibility.md)

**Requirements**:

- **Text contrast**: Minimum 4.5:1 ratio for normal text (WCAG AA)
- **Large text contrast**: Minimum 3:1 ratio for large text (≥18pt)
- **Non-text contrast**: Minimum 3:1 ratio for UI components and diagrams

**Use Accessible Color Palette** in all Mermaid diagrams:

- Blue: `#0173B2`
- Orange: `#DE8F05`
- Teal: `#029E73`
- Purple: `#CC78BC`
- Brown: `#CA9161`

**Never rely on color alone** to convey information - use text labels, patterns, or icons as well.

## Screen Reader Considerations

**Structure content for screen reader comprehension**.

**Best Practices**:

1. **Logical reading order** - Content flows naturally from top to bottom
2. **Descriptive link text** - Links describe destination, not "click here"
3. **Table headers** - Use header rows in tables for column identification
4. **List structure** - Use proper list syntax (not manual bullets)
5. **Heading hierarchy** - Proper H1-H6 nesting for document outline

PASS: **Good (Descriptive Link Text)**:

```markdown
See the `Authentication Guide` for setup instructions.
```

FAIL: **Avoid (Generic Link Text)**:

```markdown
For setup instructions, click [here](./auth-guide.md).
```
