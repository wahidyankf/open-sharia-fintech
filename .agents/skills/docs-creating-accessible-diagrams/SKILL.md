---
name: docs-creating-accessible-diagrams
description: WCAG-compliant Mermaid diagrams using verified accessible color palette. Use when creating diagrams, flowcharts, or any color-dependent visualizations requiring accessibility compliance for color blindness.
---

# Color Accessibility for Diagrams

This Skill provides guidance on creating accessible Mermaid diagrams using a verified color-blind friendly palette that meets WCAG AA standards. Use this when creating visual diagrams to ensure accessibility for all users, including those with color blindness (~300 million people worldwide).

## Purpose

Use this Skill when:

- Creating Mermaid diagrams, flowcharts, or visualizations
- Working with color-dependent visual content
- Need to ensure WCAG compliance for diagrams
- Supporting users with color blindness (protanopia, deuteranopia, tritanopia)
- Choosing colors for documentation, diagrams, or UI components

## Color Palette and Colors to Avoid

See [Color Palette and Colors to Avoid](./reference/color-palette-and-avoided-colors.md) for the
full 8-color verified WCAG AA palette with hex codes and use cases, plus the colors that must
never carry information (red, green, yellow, pink, magenta).

## Core Accessibility Principles

See [Core Accessibility Principles](./reference/core-accessibility-principles.md) for the four
principles — never rely on color alone, use color as enhancement, maintain WCAG AA contrast, and
test for color blindness before publishing.

## Mermaid Diagram Best Practices

See [Mermaid Best Practices](./reference/mermaid-best-practices.md) for the standard accessible
Mermaid template, the ten essential Mermaid rules, comment syntax, and the special-character
escaping table for node text and edge labels.

## Common Mistakes and Testing Tools

See [Common Mistakes and Testing Tools](./reference/common-mistakes-and-testing.md) for the six
most common accessibility mistakes with fixes, plus color blindness simulators and contrast
checkers to verify diagrams before publishing.

## Integration with Repository Conventions

This Skill integrates with:

- **[Color Accessibility Convention](../../../repo-governance/conventions/formatting/color-accessibility.md)** - Complete color accessibility standards
- **[Diagrams Convention](../../../repo-governance/conventions/formatting/diagrams.md)** - Mermaid diagram standards, comment syntax, special character escaping
- **[Content Quality Principles](../../../repo-governance/conventions/writing/quality.md)** - Quality standards for all content including diagrams

## Quick Reference

See [Quick Reference](./reference/quick-reference.md) for the copy-paste palette, the Mermaid
`classDef` template, and the pre-commit accessibility checklist. This also contains the worked
Mermaid template referenced by [Mermaid Best Practices](./reference/mermaid-best-practices.md).

## References

- **[Color Accessibility Convention](../../../repo-governance/conventions/formatting/color-accessibility.md)** - Complete standards, research citations, WCAG compliance
- **[Diagrams Convention](../../../repo-governance/conventions/formatting/diagrams.md)** - Mermaid syntax, comment rules, special character escaping
- **[Accessibility First Principle](../../../repo-governance/principles/content/accessibility-first.md)** - Foundational accessibility principle

## Related Skills

- `repository-architecture` - Understanding how accessibility fits into governance layers
- `apps-ayokoding-www-developing-content` - ayokoding-web diagram requirements
- `factual-validation-methodology` (Phase 2) - Verifying color accessibility claims

---

**Note**: This Skill provides action-oriented guidance for creating accessible diagrams. The authoritative Color Accessibility Convention contains complete scientific research, WCAG standards, and detailed testing procedures.
