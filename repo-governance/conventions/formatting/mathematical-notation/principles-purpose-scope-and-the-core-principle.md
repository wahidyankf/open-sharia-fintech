---
description: The principles this convention implements, what it covers and does not cover, an overview of where math notation appears, and the core LaTeX rule.
when_to_use: Use when you need to understand why this repository standardizes on LaTeX for math or what the convention covers.
---

# Principles, Purpose, Scope, and the Core Principle

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: LaTeX notation as the single standard for all equations. No mixing different math syntaxes or rolling custom solutions.

- **[Accessibility First](../../../principles/content/accessibility-first.md)**: LaTeX notation renders properly in modern browsers and can be parsed by screen readers with math support. Text-based source allows assistive technology to interpret mathematical content.

## Purpose

This convention establishes LaTeX notation as the standard for all mathematical expressions in markdown files. It ensures equations render consistently across GitHub and Next.js sites using `$...$` (inline) and `$$...$$` (display) syntax, providing professional mathematical typography.

## Scope

### What This Convention Covers

- **LaTeX syntax** - Inline `$...$` and display `$$...$$` notation
- **Where to use math** - Documentation, tutorials, technical explanations
- **Math rendering** - How different platforms render LaTeX
- **Common patterns** - Frequently used mathematical expressions
- **Equation formatting** - Alignment, multi-line equations, numbering

### What This Convention Does NOT Cover

- **Code blocks** - Math notation is NOT used in code examples (use actual code syntax)
- **Mermaid diagrams** - Math notation is NOT supported in Mermaid
- **ASCII art** - Alternative plain-text representations of math
- **Complex mathematical publishing** - This is for inline documentation math, not research papers

## Overview

Mathematical notation appears throughout enterprise documentation - from financial formulas like WACC and CAPM to statistical models and algorithmic complexity analysis. This convention ensures all mathematical expressions are:

1. **Readable** - Clear notation that renders properly
2. **Consistent** - Same syntax across all documentation
3. **Compatible** - Renders on GitHub and standard markdown viewers
4. **Maintainable** - Easy to edit and version control

## The Core Principle

**Use LaTeX notation for all mathematical equations and formulas in documentation.**

GitHub has supported LaTeX math rendering in markdown since May 2022. This makes LaTeX the universal standard for mathematical notation in modern documentation.
