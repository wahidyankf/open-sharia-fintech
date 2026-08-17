---
title: "Diagram and Schema Convention"
description: "Standards for using Mermaid diagrams and ASCII art in open-sharia-enterprise markdown files. Includes color-blind accessibility requirements"
when_to_use: "Read this index to find the right Diagram and Schema Convention child document."
---

# Diagram and Schema Convention

- [Principles Implemented/Respected](./01-principles-implemented-respected.md) — Lists the accessibility, simplicity, and documentation-first principles
- [Purpose](./02-purpose.md) — States that this document defines when and
- [Scope](./03-scope.md) — Lists what this convention covers (Mermaid, ASCII
- [The Core Principle](./04-the-core-principle.md) — States the core principle: Mermaid first for
- [Format Selection Rule and Decision Table](./05-format-selection-rule-and-decision-table.md) — Gives the format-selection decision table mapping diagram
- [Format Selection Rule: Rationale and Examples](./06-format-selection-rule-rationale-and-examples.md) — Explains why Mermaid and ASCII are split
- [Why Mermaid First?](./07-why-mermaid-first.md) — Explains Mermaid's wide platform support and advantages
- [Mermaid Diagrams: When, Why, and Syntax](./08-mermaid-diagrams-when-why-and-syntax.md) — Covers when to use Mermaid, why it's
- [Common Mermaid Diagram Types](./09-mermaid-common-diagram-types.md) — Documents the six common Mermaid diagram types
- [Diagram Orientation](./10-mermaid-diagram-orientation.md) — Specifies orientation rules (top-down vs.
- [Flowchart Width Constraints](./11-mermaid-flowchart-width-constraints.md) — Specifies width constraints for Mermaid flowcharts to
- [Width Violation Fix Strategy Guide](./12-mermaid-width-violation-fix-strategy-guide.md) — Provides a strategy guide for fixing Mermaid
- [State Diagram Width and Label Constraints](./13-mermaid-state-diagram-width-and-label-constraints.md) — Specifies width and label constraints specific to
- [Render-Fidelity Caveat: Source-Correct Can Still Be Render-Wrong](./14-mermaid-render-fidelity-caveat.md) — Warns that a syntactically source-correct Mermaid diagram
- [Mermaid Best Practices](./15-mermaid-best-practices.md) — Lists general best practices for writing maintainable,
- [Mermaid Comment Syntax](./16-mermaid-comment-syntax.md) — Documents Mermaid's comment syntax (%%) and how
- [Mermaid Color Accessibility: Palette and Rationale](./17-mermaid-color-accessibility-palette.md) — Explains why color-blind accessibility matters for Mermaid
- [Mermaid Color Accessibility: Dark Mode, Shape Differentiation, and Implementation Example](./18-mermaid-color-accessibility-implementation.md) — Covers dark/light mode compliance, required shape differentiation,
- [Mermaid Color Accessibility: Testing Requirements, Documentation, and Key Points](./19-mermaid-color-accessibility-testing-and-docs.md) — Covers testing requirements, documentation requirements, and key
- [Mermaid Resources](./20-mermaid-resources.md) — Links to external Mermaid documentation and reference
- [ASCII Art: When to Use and Why It's Optional](./21-ascii-art-when-and-why.md) — Explains when ASCII art is still an
- [ASCII Art Use Cases](./22-ascii-art-use-cases.md) — Lists concrete ASCII art use cases —
- [ASCII Art: Best Practices, Character Sets, and Tools](./23-ascii-art-best-practices-character-sets-and-tools.md) — Covers ASCII art best practices, the character
- [Decision Matrix](./24-decision-matrix.md) — Provides a quick-reference decision matrix for choosing
- [Examples in Context](./25-examples-in-context.md) — Shows four worked examples of diagrams used
- [Mixing Formats](./26-mixing-formats.md) — Explains when and how it's acceptable to
- [Migration Strategy](./27-migration-strategy.md) — Covers how to upgrade existing ASCII art
- [Verification Checklist](./28-verification-checklist.md) — Provides the pre-publish verification checklist for diagrams
- [Common Mermaid Syntax Errors: Special Characters in Node Text and Edge Labels](./29-common-syntax-errors-special-characters.md) — Documents Error 1: how special characters in
- [Common Mermaid Syntax Errors: Literal Quotes and Nested Escaping in Node Text](./30-common-syntax-errors-literal-quotes-and-nested-escaping.md) — Documents Error 2 and Error 3: literal
- [Common Mermaid Syntax Errors: Style Commands and Sequence-Diagram Participant Syntax](./31-common-syntax-errors-style-commands-and-participant-syntax.md) — Documents Error 4 and Error 5: style
- [Common Mermaid Syntax Errors: Colons in State Diagram Edge Labels](./32-common-syntax-errors-colons-in-state-diagrams.md) — Documents Error 6: how colons in Mermaid
- [Common Mermaid Syntax Errors: Quick Reference — Character Escaping](./33-common-syntax-errors-quick-reference-character-escaping.md) — Provides a quick-reference table summarizing which characters
- [Common Mermaid Syntax Errors: Escape Sequences Do Not Create Line Breaks](./34-common-syntax-errors-escape-sequences.md) — Documents Error 7: the `
` escape sequence does not create line breaks in Mermaid rendering, and what to use instead. Use when you tried `
` for a line break in a Mermaid label and it rendered as literal text instead.
- [Common Mermaid Syntax Errors: Label Constraints — Overview, Rule 1, and Rule 2](./35-common-syntax-errors-label-constraints-overview-and-rules-1-2.md) — Documents Error 8's overview plus Rule 1
- [Common Mermaid Syntax Errors: Label Constraints — Rule 3, Maximum Line Length](./36-common-syntax-errors-label-constraints-rule-3-line-length.md) — Documents Rule 3: the 20-character maximum line
- [Common Mermaid Syntax Errors: Label Constraints — Rules 4 and 5](./37-common-syntax-errors-label-constraints-rules-4-5.md) — Documents Rule 4 (no URL paths in
- [Common Mermaid Syntax Errors: Label Constraints — Quick Reference Summary](./38-common-syntax-errors-label-constraints-quick-reference.md) — Provides the quick-reference summary table for all
- [Diagram Size and Splitting: Why It Matters and When to Split](./39-diagram-size-and-splitting-why-and-when.md) — Explains why oversized diagrams are a problem,
- [Diagram Size and Splitting: Splitting Guidelines](./40-diagram-size-splitting-guidelines.md) — Gives concrete guidelines for how to split
- [Diagram Size and Splitting: Real-World Fixes and Summary](./41-diagram-size-real-world-fixes-and-summary.md) — Shows real-world before/after examples of splitting oversized
- [UI Mockups in Plan Docs: Principles in Practice and Scope](./42-ui-mockups-principles-and-scope.md) — States the principles behind requiring visible UI
- [UI Mockups in Plan Docs: Rendering-Support Matrix and Ruled-Out Formats](./43-ui-mockups-rendering-support-and-ruled-out-formats.md) — Compares which mockup formats render properly across
- [UI Mockups in Plan Docs: The Both-Tiers Rule](./44-ui-mockups-both-tiers-rule.md) — Defines the required two-tier mockup rule: low-fidelity
- [UI Mockups in Plan Docs: Responsive Design and Design-Review Heuristic](./45-ui-mockups-responsive-design-and-review-heuristic.md) — Covers the mobile/tablet/desktop responsive design requirement and
- [UI Mockups in Plan Docs: Grounding Rule and Design Funnel](./46-ui-mockups-grounding-rule-and-design-funnel.md) — Defines the grounding rule (R5) tying mockups
- [Placement — the UI Lives in prd.md (HARD RULE): Requirements and Enforcement](./47-ui-mockups-placement-hard-rule-requirements.md) — States the hard rule that all UI
- [Placement — the UI Lives in prd.md (HARD RULE): Copy-Paste Example](./48-ui-mockups-placement-hard-rule-example.md) — Provides a complete copy-paste example of a
- [UI Mockups in Plan Docs: Prior-Art Recommendation and Worked Example](./49-ui-mockups-prior-art-and-worked-example.md) — Gives the prior-art recommendation (R7) for researching
- [Related Documentation and External Resources](./50-related-documentation-and-external-resources.md) — Links to related conventions and external Mermaid/ASCII-art
