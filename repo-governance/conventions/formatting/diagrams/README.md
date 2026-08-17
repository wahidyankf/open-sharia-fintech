---
title: "Diagram and Schema Convention"
description: "Standards for using Mermaid diagrams and ASCII art in open-sharia-enterprise markdown files. Includes color-blind accessibility requirements"
when_to_use: "Read this index to find the right Diagram and Schema Convention child document."
---

# Diagram and Schema Convention

- [Principles Implemented/Respected](./01-principles-implemented-respected.md) — You need to understand why this diagram convention requires Mermaid-first, accessible colors.
- [Purpose](./02-purpose.md) — You need the one-sentence purpose of this convention before diving into its rules.
- [Scope](./03-scope.md) — Checking whether a diagram or mockup question falls inside this convention's scope.
- [The Core Principle](./04-the-core-principle.md) — Deciding at a high level whether a diagram should be Mermaid.
- [Format Selection Rule](./05-format-selection-rule-and-decision-table.md) — Picking which diagram format (Mermaid vs.
- [Format Selection Rule](./06-format-selection-rule-rationale-and-examples.md) — You need the reasoning behind the format-selection rule.
- [Why Mermaid First?](./07-why-mermaid-first.md) — Justifying or challenging the Mermaid-first policy for a specific rendering context.
- [Mermaid Diagrams](./08-mermaid-diagrams-when-why-and-syntax.md) — Starting a new Mermaid diagram and need the baseline when/why/syntax orientation.
- [Common Mermaid Diagram Types](./09-mermaid-common-diagram-types.md) — Choosing which Mermaid diagram type fits the relationship or process you're documenting.
- [Diagram Orientation](./10-mermaid-diagram-orientation.md) — Deciding or reviewing which orientation a Mermaid diagram should use.
- [Flowchart Width Constraints](./11-mermaid-flowchart-width-constraints.md) — A Mermaid flowchart risks becoming too wide to render legibly.
- [Width Violation Fix Strategy Guide](./12-mermaid-width-violation-fix-strategy-guide.md) — An existing Mermaid diagram fails a width check.
- [State Diagram Width](./13-mermaid-state-diagram-width-and-label-constraints.md) — Authoring or fixing a Mermaid state diagram that has wide.
- [Render-Fidelity Caveat](./14-mermaid-render-fidelity-caveat.md) — A Mermaid diagram passes syntax validation but still renders wrong.
- [Mermaid Best Practices](./15-mermaid-best-practices.md) — Writing a new Mermaid diagram and want the general best-practices checklist.
- [Mermaid Comment Syntax](./16-mermaid-comment-syntax.md) — Adding explanatory comments inside a Mermaid diagram definition.
- [Mermaid Color Accessibility](./17-mermaid-color-accessibility-palette.md) — Choosing colors for a Mermaid diagram and need the accessible palette.
- [Mermaid Color Accessibility](./18-mermaid-color-accessibility-implementation.md) — Implementing accessible colors in a Mermaid diagram.
- [Mermaid Color Accessibility](./19-mermaid-color-accessibility-testing-and-docs.md) — Verifying or documenting that a Mermaid diagram's colors meet the accessibility requirements.
- [Mermaid Resources](./20-mermaid-resources.md) — Looking for official Mermaid syntax references or tooling links.
- [ASCII Art](./21-ascii-art-when-and-why.md) — Deciding whether a diagram should be ASCII art instead of Mermaid.
- [ASCII Art Use Cases](./22-ascii-art-use-cases.md) — You need a worked ASCII art example for a specific use case like directory trees.
- [ASCII Art](./23-ascii-art-best-practices-character-sets-and-tools.md) — Authoring ASCII art and need the character-set conventions or a tool recommendation.
- [Decision Matrix](./24-decision-matrix.md) — You need a fast lookup table to pick a diagram format instead of reading the full rationale.
- [Examples in Context](./25-examples-in-context.md) — You want to see a diagram format applied in a realistic documentation context before writing your own.
- [Mixing Formats](./26-mixing-formats.md) — A document seems to need both Mermaid and ASCII art.
- [Migration Strategy](./27-migration-strategy.md) — Migrating a legacy ASCII diagram to Mermaid.
- [Verification Checklist](./28-verification-checklist.md) — A final checklist before committing a new or edited diagram.
- [Common Mermaid Syntax Errors](./29-common-syntax-errors-special-characters.md) — A Mermaid diagram fails to render and the node text.
- [Common Mermaid Syntax Errors](./30-common-syntax-errors-literal-quotes-and-nested-escaping.md) — A Mermaid diagram has quote characters.
- [Common Mermaid Syntax Errors](./31-common-syntax-errors-style-commands-and-participant-syntax.md) — A Mermaid sequence diagram's style commands.
- [Common Mermaid Syntax Errors](./32-common-syntax-errors-colons-in-state-diagrams.md) — A Mermaid state diagram edge label containing a colon fails to parse.
- [Character Escaping](./33-common-syntax-errors-quick-reference-character-escaping.md) — A fast lookup when you need to know how to escape a specific character in Mermaid.
- [Common Mermaid Syntax Errors](./34-common-syntax-errors-escape-sequences.md) — You tried `\n` for a line break in a Mermaid label.
- [Overview, Rule 1](./35-common-syntax-errors-label-constraints-overview-and-rules-1-2.md) — A Mermaid label needs a line break or contains HTML.
- [Rule 3](./36-common-syntax-errors-label-constraints-rule-3-line-length.md) — A Mermaid label is too long.
- [Rules 4 and 5](./37-common-syntax-errors-label-constraints-rules-4-5.md) — A Mermaid edge label contains a URL/path.
- [Quick Reference Summary](./38-common-syntax-errors-label-constraints-quick-reference.md) — You want the full label-constraint rules summarized in one quick-reference table.
- [Diagram Size and Splitting](./39-diagram-size-and-splitting-why-and-when.md) — A diagram feels cluttered or hard to read.
- [Diagram Size and Splitting](./40-diagram-size-splitting-guidelines.md) — You've decided a diagram needs splitting.
- [Diagram Size and Splitting](./41-diagram-size-real-world-fixes-and-summary.md) — You want worked before/after examples of diagram splitting.
- [UI Mockups in Plan Docs](./42-ui-mockups-principles-and-scope.md) — You need to understand why plan docs must show UI design exploration.
- [UI Mockups in Plan Docs](./43-ui-mockups-rendering-support-and-ruled-out-formats.md) — Choosing a mockup format and need to confirm it will render on GitHub.
- [UI Mockups in Plan Docs](./44-ui-mockups-both-tiers-rule.md) — Producing UI mockups for a plan.
- [UI Mockups in Plan Docs](./45-ui-mockups-responsive-design-and-review-heuristic.md) — A UI mockup needs to show responsive behavior across breakpoints.
- [UI Mockups in Plan Docs](./46-ui-mockups-grounding-rule-and-design-funnel.md) — A mockup needs to be grounded in real data or components.
- [the UI Lives in prd.md](./47-ui-mockups-placement-hard-rule-requirements.md) — Deciding where to place UI mockups and funnel records in a plan.
- [the UI Lives in prd.md](./48-ui-mockups-placement-hard-rule-example.md) — You need a ready-to-copy template for recording a plan's UI design funnel in prd.md.
- [UI Mockups in Plan Docs](./49-ui-mockups-prior-art-and-worked-example.md) — Starting a new UI mockup and want to research prior art first.
- [Related Documentation](./50-related-documentation-and-external-resources.md) — Looking for related conventions or official external references to cross-check this convention against.
