---
title: "Surgical Changes — Principle"
description: The touch-only-what-you-must principle for editing existing code, its four core rules, and the one-sentence test for scope.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - implementation
  - optimization
  - refactoring
  - surgical-changes
  - goal-driven
  - test-driven
created: 2025-12-15
when_to_use: Use when editing existing code and deciding what is and is not in scope for the change.
---

# Surgical Changes — Principle

## Principle: Touch Only What You Must

When editing existing code, practice surgical precision. Clean up only your own mess.

**Core Rules**:

1. **Don't "improve" adjacent code**
   - No fixing nearby formatting
   - No refactoring unrelated code
   - No updating comments you didn't change
   - No type annotation additions to unchanged code

2. **Don't refactor things that aren't broken**
   - If it works and isn't part of your task, leave it
   - "While I'm here" is a red flag
   - Separate refactoring from feature work

3. **Match existing style, even if you'd do it differently**
   - Use tabs if the file uses tabs
   - Follow existing naming conventions
   - Match indentation patterns
   - Consistency > your preferences

4. **Dead code handling**
   - If you notice unrelated dead code, mention it - don't delete it
   - Only remove what YOUR changes made unused
   - Don't remove pre-existing dead code unless asked

**The Test**: Every changed line should trace directly to the user's request.
