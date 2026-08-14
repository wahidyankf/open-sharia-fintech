---
title: "Color Accessibility for Colored Emojis"
description: How to use colored square emojis for agent categorization accessibly, so color is always supplementary to text and shape.
when_to_use: Use when using colored emojis (like the agent-role squares) for visual categorization and you need to keep them accessible.
category: explanation
subcategory: conventions
tags:
  - emoji
  - accessibility
  - scannability
  - conventions
  - markdown
created: 2025-12-04
---

# Color Accessibility for Colored Emojis

**Master Reference**: All colored emoji usage MUST follow the [Color Accessibility Convention](../color-accessibility.md) — the authoritative source for accessible color palette, WCAG standards, and testing methodology. This section provides emoji-specific guidance.

**Where colored emojis (like 🟦🟩🟨🟪) are used for visual categorization, ensure:**

1. **Colors are SUPPLEMENTARY to semantic information**
   - Primary identification relies on non-color factors (shape, text label, context)
   - Color enhances visual scannability but is never the sole identifier

2. **All colors used are from the verified accessible palette**
   - Blue (#0173B2), Orange (#DE8F05), Teal (#029E73), Purple (#CC78BC), Brown (#CA9161)
   - See [Color Accessibility Convention](../color-accessibility.md) for complete palette details, WCAG compliance verification, and testing tools

3. **Users with color blindness can still identify items by shape/text alone**
   - Square emoji shape (🟦) is distinct from other emoji shapes
   - Text labels ("Writer", "Checker", "Fixer") provide semantic meaning
   - Context (placement next to agent names) provides additional cues

4. **Never rely on color alone for categorization**
   - Always combine color with text labels
   - Always combine color with shape differentiation
   - Always provide context through surrounding text

**Example of accessible colored emoji usage:**

PASS: **Good - Color + Text + Shape:**

```markdown
### 🟦 `docs-maker.md`

Expert documentation writer specializing in GitHub-compatible markdown and Diátaxis framework.
```

**Why this works:**

- Color: Blue square (accessible color from verified palette)
- Shape: Square emoji (distinguishable shape)
- Text: "docs-maker.md" (primary identifier)
- Description: "Expert documentation writer..." (semantic meaning)

FAIL: **Bad - Color only:**

```markdown
### 🟦

Agent for documentation
```

**Why this fails:**

- No text label to identify specific agent
- Relies solely on color and shape
- No semantic context provided

For complete color accessibility guidelines including WCAG standards, testing tools, and research sources, see [Color Accessibility Convention](../color-accessibility.md).
