---
title: "Styling — Applying the Implementation Workflow"
description: The three-stage make-it-work/make-it-right/make-it-fast Implementation Workflow applied specifically to building or refactoring styles
category: explanation
subcategory: development/frontend
tags:
  - styling
  - tailwind
  - css
  - responsive
  - mobile-first
created: 2026-03-28
when_to_use: Use when starting a new styling task or refactor, to decide what to prioritize at each stage.
---

# Applying the Implementation Workflow

Follow the three-stage [Implementation Workflow](../../workflow/implementation.md) when building or refactoring styles:

1. **Make it work** — Apply utility classes directly in TSX. Hard-code values if it gets you to a working component faster.
2. **Make it right** — Extract repeated class combinations into a shared component or a `cva` variant definition. Move one-off overrides out of inline styles and into utilities.
3. **Make it fast** — Audit and remove unused design tokens; eliminate `!important` overrides; consolidate duplicate `@layer base` blocks.

Do not extract patterns in Stage 1. Copy-pasting class strings across components is acceptable while the design is still evolving.
