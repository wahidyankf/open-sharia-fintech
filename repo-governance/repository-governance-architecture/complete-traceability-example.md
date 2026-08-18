---
title: "Complete Traceability Example"
description: A full worked example tracing Color Accessibility across all six layers
category: explanation
subcategory: architecture
tags:
  - architecture
  - governance
  - traceability
created: 2026-02-09
when_to_use: Use for a concrete end-to-end traceability example.
---

# Complete Traceability Example

## Color Accessibility (Vision → Agents)

**L0 - Vision**: Democratize Islamic enterprise → accessible to everyone

**L1 - Principle**: [Accessibility First](../principles/content/accessibility-first.md)

- **Vision supported**: Accessible tools enable global participation in Shariah-compliant business
- **Key value**: Universal access from the start, not as an afterthought

**L2 - Convention**: [Color Accessibility Convention](../conventions/formatting/color-accessibility.md)

- **Implements**: Accessibility First principle
- **Rule**: Use verified color-blind friendly palette
- **WCAG AA compliance required**

**L3 - Development**: [AI Agents Convention](../development/agents/ai-agents.md)

- **Respects**: Color Accessibility Convention
- **Practice**: Agent colors use accessible palette
- **Implementation**: Frontmatter `color` field limited to verified palette

**L4 - Agents**:

- `docs-checker` - Validates diagram colors in documentation
- `docs-fixer` - Applies color corrections to diagrams
- `agent-maker` - Validates agent frontmatter colors

**L5 - Workflow**: Maker-Checker-Fixer

- Orchestrates: maker → checker → fixer
- Ensures: All diagrams use accessible colors before publication

**Agent skills (Delivery)**:

- `docs-creating-accessible-diagrams` (inline) - Delivers Mermaid diagram patterns with WCAG colors
- Service relationship: Helps agents understand color conventions

**Complete Chain**:

```
Vision (Democratize access)
    ↓ inspires
Principle (Accessibility First)
    ↓ governs
Convention (Color Accessibility)
    ↓ governs
Development (AI Agents Convention)
    ↓ governs
Agents (docs-checker, docs-fixer, agent-maker)
    ↓ orchestrated by
Workflow (Maker-Checker-Fixer)
    ↓ served by
Agent skills (docs-creating-accessible-diagrams - inline knowledge delivery)
```
