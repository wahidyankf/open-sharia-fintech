---
title: "Diagram and Schema Convention"
description: "Standards for using Mermaid diagrams and ASCII art in open-sharia-enterprise markdown files. Includes color-blind accessibility requirements"
when_to_use: "Read this index to find the right Diagram and Schema Convention child document."
---

# Diagram and Schema Convention

- [Principles Implemented/Respected](./01-principles-implemented-respected.md) — The accessibility, simplicity, and documentation-first principles this diagram convention implements.
- [Purpose](./02-purpose.md) — You need the one-sentence purpose of this convention before diving into its rules.
- [Scope](./03-scope.md) — Checking whether a diagram or mockup question falls inside this convention's scope.
- [The Core Principle](./04-the-core-principle.md) — Deciding at a high level whether a diagram should be Mermaid or ASCII art.
- [Format Selection Rule and Decision Table](./05-format-selection-rule-and-decision-table.md) — The format-selection decision table mapping diagram purpose to the required format.
- [Format Selection Rule](./06-format-selection-rule-rationale-and-examples.md) — Why Mermaid and ASCII are split the way they are, with worked format-choice examples.
- [Why Mermaid First?](./07-why-mermaid-first.md) — Justifying or challenging the Mermaid-first policy for a specific rendering context.
- [Mermaid Diagrams](./08-mermaid-diagrams-when-why-and-syntax.md) — Starting a new Mermaid diagram and need the baseline when/why/syntax orientation.
- [Common Mermaid Diagram Types](./09-mermaid-common-diagram-types.md) — Choosing which Mermaid diagram type fits the relationship or process you're documenting.
- [Diagram Orientation](./10-mermaid-diagram-orientation.md) — Deciding or reviewing which orientation a Mermaid diagram should use.
- [Flowchart Width Constraints](./11-mermaid-flowchart-width-constraints.md) — A Mermaid flowchart risks becoming too wide to render legibly.
- [Width Violation Fix Strategy Guide](./12-mermaid-width-violation-fix-strategy-guide.md) — A strategy guide for fixing Mermaid diagrams that violate width constraints.
- [State Diagram Width and Label Constraints](./13-mermaid-state-diagram-width-and-label-constraints.md) — Width and label constraints specific to Mermaid state diagrams.
- [Render-Fidelity Caveat](./14-mermaid-render-fidelity-caveat.md) — Why a source-correct Mermaid diagram can still render wrong, and how to catch it.
- [Mermaid Best Practices](./15-mermaid-best-practices.md) — General best practices for writing maintainable, readable Mermaid diagrams.
- [Mermaid Comment Syntax](./16-mermaid-comment-syntax.md) — Adding explanatory comments inside a Mermaid diagram definition.
- [Mermaid Color Accessibility](./17-mermaid-color-accessibility-palette.md) — Why color-blind accessibility matters for Mermaid diagrams and gives the accessible color palette to use.
- [Mermaid Color Accessibility](./18-mermaid-color-accessibility-implementation.md) — Implementing accessible colors in a Mermaid diagram and need a concrete classDef example.
- [Mermaid Color Accessibility](./19-mermaid-color-accessibility-testing-and-docs.md) — Verifying or documenting that a Mermaid diagram's colors meet the accessibility requirements.
- [Mermaid Resources](./20-mermaid-resources.md) — Links to external Mermaid documentation and reference resources.
- [ASCII Art](./21-ascii-art-when-and-why.md) — Deciding whether a diagram should be ASCII art instead of Mermaid.
- [ASCII Art Use Cases](./22-ascii-art-use-cases.md) — Concrete ASCII art use cases, from directory structures to tables.
- [ASCII Art](./23-ascii-art-best-practices-character-sets-and-tools.md) — Authoring ASCII art and need the character-set conventions or a tool recommendation.
- [Decision Matrix](./24-decision-matrix.md) — A quick-reference decision matrix for choosing the right diagram format.
- [Examples in Context](./25-examples-in-context.md) — Four worked examples of diagrams in real documentation.
- [Mixing Formats](./26-mixing-formats.md) — A document seems to need both Mermaid and ASCII art and you're unsure if that's allowed.
- [Migration Strategy](./27-migration-strategy.md) — Migrating a legacy ASCII diagram to Mermaid, or deciding whether a Mermaid diagram needs downgrading.
- [Verification Checklist](./28-verification-checklist.md) — A final checklist before committing a new or edited diagram.
- [Common Mermaid Syntax Errors](./29-common-syntax-errors-special-characters.md) — A Mermaid diagram fails to render on special characters in node or edge text.
- [Common Mermaid Syntax Errors](./30-common-syntax-errors-literal-quotes-and-nested-escaping.md) — A Mermaid diagram has quote characters or nested escaping that isn't rendering correctly.
- [Common Mermaid Syntax Errors](./31-common-syntax-errors-style-commands-and-participant-syntax.md) — A Mermaid sequence diagram's style commands or participant aliasing aren't working as expected.
- [Common Mermaid Syntax Errors](./32-common-syntax-errors-colons-in-state-diagrams.md) — A Mermaid state diagram edge label containing a colon fails to parse.
- [Character Escaping](./33-common-syntax-errors-quick-reference-character-escaping.md) — A quick-reference table summarizing which characters need escaping in Mermaid diagrams and how.
- [Common Mermaid Syntax Errors](./34-common-syntax-errors-escape-sequences.md) — A `\n` in a Mermaid label rendered as literal text.
- [Overview, Rule 1, and Rule 2](./35-common-syntax-errors-label-constraints-overview-and-rules-1-2.md) — Line breaks and HTML inside Mermaid labels.
- [Rule 3, Maximum Line Length](./36-common-syntax-errors-label-constraints-rule-3-line-length.md) — Rule 3: the 20-character maximum line length constraint for Mermaid labels, with examples.
- [Rules 4 and 5](./37-common-syntax-errors-label-constraints-rules-4-5.md) — A Mermaid edge label contains a URL/path, or a separator line looks disproportionate.
- [Quick Reference Summary](./38-common-syntax-errors-label-constraints-quick-reference.md) — The quick-reference summary table for all Mermaid label constraint rules.
- [Diagram Size and Splitting](./39-diagram-size-and-splitting-why-and-when.md) — A diagram feels cluttered and may need splitting.
- [Diagram Size and Splitting](./40-diagram-size-splitting-guidelines.md) — Concrete guidelines for how to split an oversized diagram into multiple focused diagrams.
- [Diagram Size and Splitting](./41-diagram-size-real-world-fixes-and-summary.md) — Shows real-world before/after examples of splitting oversized diagrams, plus a summary of the guidance.
- [UI Mockups in Plan Docs](./42-ui-mockups-principles-and-scope.md) — Why plan docs must carry visible UI design records, and how far that reaches.
- [UI Mockups in Plan Docs](./43-ui-mockups-rendering-support-and-ruled-out-formats.md) — Choosing a mockup format that renders everywhere it must.
- [UI Mockups in Plan Docs](./44-ui-mockups-both-tiers-rule.md) — The required two-tier mockup rule: low-fidelity ASCII wireframes plus high-fidelity Excalidraw PNGs.
- [UI Mockups in Plan Docs](./45-ui-mockups-responsive-design-and-review-heuristic.md) — The mobile/tablet/desktop responsive design requirement and the identical-DOM-per-breakpoint review heuristic.
- [UI Mockups in Plan Docs](./46-ui-mockups-grounding-rule-and-design-funnel.md) — The grounding rule (R5) and the design funnel (R6).
- [the UI Lives in prd.md](./47-ui-mockups-placement-hard-rule-requirements.md) — The hard rule placing UI design funnel artefacts in prd.md, and how it is enforced.
- [the UI Lives in prd.md](./48-ui-mockups-placement-hard-rule-example.md) — A complete copy-paste example of a UI design funnel record formatted for prd.md.
- [UI Mockups in Plan Docs](./49-ui-mockups-prior-art-and-worked-example.md) — The prior-art recommendation (R7) for researching existing patterns, plus a worked mockup example.
- [Related Documentation and External Resources](./50-related-documentation-and-external-resources.md) — Links to related conventions and external Mermaid/ASCII-art resources.
