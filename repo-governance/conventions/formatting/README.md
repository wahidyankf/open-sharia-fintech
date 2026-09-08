---
description: Practical Markdown formatting rules that keep repository documentation clear and accessible
when_to_use: Use when you need the right formatting convention (diagrams, colors, emoji, math notation, code fences, timestamps) for a specific markdown element you are adding or reviewing.
---

# Formatting Conventions

Use these rules to make Markdown easy to scan, accessible to more readers, and consistent across the repository. Start with the convention that matches the thing you are adding; you do not need to memorize the whole set.

## Purpose

These conventions define **HOW to format markdown content** including indentation, linking, diagrams, emojis, timestamps, mathematical notation, and code fences. These are the technical formatting rules that ensure consistency and accessibility.

## Scope

**✅ Belongs Here:**

- Markdown syntax and formatting rules
- Visual element standards (diagrams, colors, emojis)
- Technical formatting specifications
- Timestamp and notation formats
- Code fence nesting rules

**❌ Does NOT Belong:**

- Content quality standards (that's writing/)
- Writing style guidelines (that's writing/)
- Tutorial structure (that's tutorials/)

## Conventions

- [Color Accessibility](./color-accessibility.md) — Standards for using color-blind friendly colors across all repository contexts (Mermaid diagrams, emoji categorization, CSS/styling) with verified accessible palette and WCAG compliance requirements. Use when choosing, reviewing, or implementing any color in this repository — diagrams, emoji indicators, agent categorization, or future CSS/styling.
- [Diagram and Schema Convention](./diagrams.md) — Standards for using Mermaid diagrams and ASCII art in open-sharia-enterprise markdown files. Includes color-blind accessibility requirements. Use when adding, reviewing, or fixing any diagram, ASCII art, or plan-doc UI mockup in this repository.
- [Emoji Usage Convention](./emoji.md) — Standards for semantic emoji usage to enhance document scannability and engagement with accessible colored emojis. Use when deciding whether, where, or which emoji to use in repository documentation.
- [Indentation Convention](./indentation.md) — Standard markdown indentation for all files in the repository. Use when indenting bullets, YAML frontmatter, or code blocks in any markdown file.
- [Documentation Linking Convention](./linking.md) — Standards for linking between documentation files in open-sharia-enterprise. Use when adding or reviewing a link between documentation files in this repository.
- [Mathematical Notation Convention](./mathematical-notation.md) — Standards for using LaTeX notation for mathematical equations and formulas in open-sharia-enterprise documentation. Use when writing a mathematical equation or formula in any markdown file in this repository.
- [Nested Code Fence Convention](./nested-code-fences.md) — Standards for properly nesting code fences when documenting markdown structure within markdown content. Use when a markdown example itself needs to show a fenced code block, and the outer/inner fence depth must be chosen correctly.
- [Timestamp Format Convention](./timestamp.md) — Standard timestamp format using UTC+7 (Indonesian WIB Time). Use when writing, generating, or validating any timestamp in this repository.

## Related Documentation

- [Conventions Index](../README.md) — All documentation conventions
- [Accessibility First Principle](../../principles/content/accessibility-first.md) — Why accessibility matters
- [Writing Conventions](../writing/README.md) — Content quality and writing standards
- [Repository Architecture](../../repository-governance-architecture.md) — Six-layer governance model

## Principles Implemented/Respected

This set of conventions implements/respects the following core principles:

- **[Accessibility First](../../principles/content/accessibility-first.md)**: Color Accessibility Convention provides verified color-blind friendly palette, and Diagrams Convention mandates accessible color combinations for all visual elements.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Indentation and Linking Conventions define explicit formatting standards, making file structure and navigation transparent through consistent rules.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Formatting conventions use simple, consistent patterns (2-space indentation, relative paths, standard timestamps) rather than complex custom solutions.
