---
title: "Nested Code Fence Convention"
description: Standards for properly nesting code fences when documenting markdown structure within markdown content
when_to_use: Use when a markdown example itself needs to show a fenced code block, and the outer/inner fence depth must be chosen correctly.
category: explanation
subcategory: conventions
tags:
  - markdown
  - code-fences
  - nesting
  - syntax
  - documentation
created: 2025-12-23
---

# Nested Code Fence Convention

This convention defines how to properly nest code fences when documenting markdown structure within markdown content. Understanding the correct nesting pattern prevents rendering bugs that break markdown formatting.

## In This Convention

- [Purpose, Scope, and the Orphaned Fence Problem](./nested-code-fences/purpose-scope-and-the-orphaned-fence-problem.md) — Principles, scope, and how an orphaned closing fence breaks rendering
- [Fence Depth Rules and Complete Nesting Examples](./nested-code-fences/fence-depth-rules-and-complete-nesting-examples.md) — The 4-backtick outer / 3-backtick inner rule and three worked examples
- [Common Mistakes and How to Fix Them](./nested-code-fences/common-mistakes-and-how-to-fix-them.md) — Extra closing fences, wrong fence depth, and mismatched fence pairs
- [Validation Checklist and Troubleshooting](./nested-code-fences/validation-checklist-and-troubleshooting.md) — Pre-commit checklist and symptom-based rendering troubleshooting
- [Testing, Integration, and Related Conventions](./nested-code-fences/testing-integration-and-related-conventions.md) — How to test nested fences and how this convention relates to others
- [Examples in Documentation Types and References](./nested-code-fences/examples-in-documentation-types-and-references.md) — Tutorial, how-to, and reference examples, plus spec references
