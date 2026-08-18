---
title: "Mathematical Notation Convention"
description: Standards for using LaTeX notation for mathematical equations and formulas in open-sharia-enterprise documentation
when_to_use: Use when writing a mathematical equation or formula in any markdown file in this repository.
category: explanation
subcategory: conventions
tags:
  - latex
  - mathematics
  - formulas
  - notation
  - conventions
created: 2025-12-02
---

# Mathematical Notation Convention

This document defines how to write mathematical equations and formulas in the open-sharia-enterprise project. Using LaTeX notation ensures mathematical expressions render correctly and consistently across all documentation platforms.

## In This Convention

- [Principles, Purpose, Scope, and the Core Principle](./mathematical-notation/principles-purpose-scope-and-the-core-principle.md) — What this convention covers and the core LaTeX rule
- [Why LaTeX?](./mathematical-notation/why-latex.md) — Universal rendering, professional quality, and version-control friendliness
- [LaTeX Syntax: Inline and Display Math](./mathematical-notation/latex-syntax-inline-and-display-math.md) — `$...$` versus `$$...$$` syntax
- [LaTeX Syntax: Delimiter Placement Rules](./mathematical-notation/latex-syntax-delimiter-placement-rules.md) — Critical rules for single vs. double dollar delimiters and `aligned` blocks
- [Where to Use LaTeX](./mathematical-notation/where-to-use-latex.md) — Documentation files, README files, and plans
- [Where NOT to Use LaTeX](./mathematical-notation/where-not-to-use-latex.md) — Code blocks, Mermaid diagrams, ASCII art, and config files
- [Common LaTeX Patterns](./mathematical-notation/common-latex-patterns.md) — Subscripts, Greek letters, fractions, summations, roots, and operators
- [Finance Formula Examples: WACC and CAPM](./mathematical-notation/finance-formula-examples-wacc-and-capm.md) — Worked LaTeX examples
- [Finance Formula Examples: NPV, Sharpe Ratio, and Compound Interest](./mathematical-notation/finance-formula-examples-npv-sharpe-ratio-and-compound-interest.md) — Worked LaTeX examples
- [Testing LaTeX Rendering](./mathematical-notation/testing-latex-rendering.md) — Verifying on GitHub and fixing common rendering issues
- [Best Practices](./mathematical-notation/best-practices.md) — Defining variables, consistent notation, and formatting complex formulas
- [Migration Strategy](./mathematical-notation/migration-strategy.md) — Rules for new and existing documentation
- [LaTeX Reference](./mathematical-notation/latex-reference.md) — Quick-reference table of commands and finance symbols
- [Validation Checklist and Important Notes](./mathematical-notation/validation-checklist-and-important-notes.md) — Pre-commit checklist and browser/performance/accessibility notes

## Related Conventions

- [Diagram and Schema Convention](../formatting/diagrams.md) — When to use Mermaid diagrams vs ASCII art (plain text for diagrams, LaTeX for math)
- [Emoji Usage Convention](../formatting/emoji.md) — Semantic emoji usage in documentation
- [File Naming Convention](../structure/file-naming.md) — How to name documentation files
- [Conventions Index](../README.md) — Overview of all conventions

## External Resources

- [LaTeX Mathematics Wikibook](https://en.wikibooks.org/wiki/LaTeX/Mathematics) - Comprehensive LaTeX math reference
- [Detexify](https://detexify.kirelabs.org/classify.html) - Draw a symbol to find its LaTeX command
- [MathJax Documentation](https://www.mathjax.org/) - Rendering engine used by many platforms
- [GitHub Math Support Announcement](https://github.blog/2022-05-19-math-support-in-markdown/) - Official GitHub blog post (May 2022)
