---
title: "Purpose, Scope, and Bullet Indentation Rules"
description: Defines what the Indentation Convention covers, the principles it implements, the core space-indentation principle, and the standard markdown bullet indentation rules.
when_to_use: Use when you need to know why this repository uses space indentation or how to indent nested markdown bullets.
category: explanation
subcategory: conventions
tags:
  - indentation
  - formatting
  - markdown
created: 2025-12-12
---

# Purpose, Scope, and Bullet Indentation Rules

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Uses standard markdown space indentation (2 spaces per level) instead of complex tab/space mixing schemes. One simple rule for all markdown files - no exceptions, no edge cases.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Spaces are visible and consistent across all editors. No hidden tab characters that render differently depending on editor configuration. What you see is what you get.

## Purpose

This convention establishes consistent indentation standards for all markdown files in the repository. It ensures bullet points, code blocks, and YAML frontmatter use appropriate indentation (spaces for bullets, 2 spaces for YAML, 4 spaces for code), improving readability and cross-tool compatibility.

## Scope

### What This Convention Covers

- **Bullet indentation** - Space indentation for nested bullets (2 spaces per level)
- **YAML frontmatter indentation** - 2-space indentation for YAML
- **Code block indentation** - How to indent code within markdown
- **Nested list formatting** - Multi-level bullet and numbered lists

### What This Convention Does NOT Cover

- **Source code indentation** - This convention is for markdown files, not application code
- **Diagram indentation** - Mermaid diagrams have their own syntax rules

## Core Principle

**All markdown files use STANDARD MARKDOWN bullet formatting** with space indentation.

**Why?**

- **Standard markdown compatibility**: Works in all markdown processors (GitHub, VS Code)
- **Universal compatibility**: Same format works everywhere (GitHub web, local editors, note-taking apps)
- **Editor consistency**: All text editors handle spaces consistently
- **Project-wide consistency**: All markdown files follow the same indentation rules

## Basic Rules

### Markdown Bullet Indentation

**Standard markdown format:**

- `- Text` (dash, SPACE, text) for same-level bullets
- Nested bullets use SPACES for indentation (2 spaces per level)

**Correct Pattern:**

```markdown
PASS: CORRECT - Standard markdown format:

- Main point
  - Nested detail (2 spaces before dash)
  - Another detail (2 spaces before dash)
    - Deeper elaboration (4 spaces before dash)

FAIL: INCORRECT - Tab after dash (NEVER use this):

-<TAB>Main point (tab after dash - WRONG!) -<TAB>Nested detail (tab after dash - WRONG!)

FAIL: INCORRECT - Tab before dash (NEVER use this):

- Main point
  <TAB>- Nested detail (tab before dash - WRONG!)
  <TAB><TAB>- Deeper elaboration (tabs before dash - WRONG!)
```

**Important**: Standard markdown uses:

1. Dash (`-`)
2. Single space
3. Text content

For nested bullets, add 2 spaces per indentation level BEFORE the dash. The pattern is always: `[SPACES]- Text` where SPACES determine nesting level (0 spaces = level 1, 2 spaces = level 2, 4 spaces = level 3, etc.).
