---
description: "Covers testing requirements, documentation requirements, and key implementation points for accessible Mermaid colors."
when_to_use: "Use when verifying or documenting that a Mermaid diagram's colors meet the accessibility requirements."
---

# Mermaid Color Accessibility: Testing Requirements, Documentation, and Key Points

## Testing Requirements

All diagrams SHOULD be tested with color blindness simulators before publishing:

- **Simulators**: [Coblis Color Blindness Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/)
- **Contrast Checker**: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

**Testing Process:**

1. Create diagram with accessible color palette
2. Test in at least one color blindness simulator (protanopia, deuteranopia, or tritanopia)
3. Verify contrast ratios meet WCAG AA standards
4. Confirm shape differentiation is sufficient

## Documentation Requirements

**IMPORTANT DISTINCTION:**

- **REQUIRED FOR ACCESSIBILITY**: Using accessible hex codes in `classDef` from the verified palette - this is what makes diagrams accessible
- **RECOMMENDED FOR DOCUMENTATION**: Adding a color palette comment listing which colors are used - this aids verification and signals intent, but is somewhat redundant

For each diagram using colors:

1. **Use accessible hex codes in `classDef`** (REQUIRED)
   - Example: `classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF`
   - This is the functional accessibility requirement
2. **Add ONE color palette comment** (RECOMMENDED)
   - Example: `<!-- Uses colors #0173B2 (blue), #DE8F05 (orange) for accessibility -->`
   - This is a documentation/transparency practice
   - **CRITICAL**: Each diagram should have exactly ONE color palette comment (no duplicates)
   - Multiple identical comments add unnecessary clutter and create maintenance burden
   - Comment is helpful for quick verification but is redundant with the hex codes in `classDef`
3. **Include labels** that don't rely solely on color
4. **Test verification** noted in diagram documentation (if applicable)

## Key Implementation Points

When creating Mermaid diagrams:

- Use hex color codes (not CSS color names like "red", "green")
- Always include black borders (`#000000`) for shape definition
- Use white text (`#FFFFFF`) for dark-filled backgrounds
- Use black text (`#000000`) for light-filled backgrounds
- Define colors in `classDef` sections, not inline
- Ensure contrast ratios meet WCAG AA (4.5:1 for normal text)
