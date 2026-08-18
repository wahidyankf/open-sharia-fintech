---
title: "Best Practices for Development Patterns"
description: "Recommended techniques for the Maker-Checker-Fixer pattern and functional programming practices."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when applying the Maker-Checker-Fixer pattern or functional programming practices."
---

# Best Practices for Development Patterns

> **Companion Document**: For common mistakes to avoid, see [Anti-Patterns](../pattern/anti-patterns.md)

One practice per child page below: principle, good example, bad example, rationale.

## Best Practices

- [Overview and Purpose](./best-practices/overview-and-purpose.md) — Why these best practices matter, and what guidance this document provides. Use when orienting to this document before reading a specific practice.
- [Practice 1: Single Responsibility Per Agent Role](./best-practices/single-responsibility-per-agent-role.md) — Each agent in Maker-Checker-Fixer should have exactly one clear responsibility - create, validate, or fix. Use when designing a new agent or reviewing whether an existing agent mixes maker/checker/fixer responsibilities.
- [Practice 2: Use Makers for User-Driven Content Creation](./best-practices/use-makers-for-user-driven-content-creation.md) — Invoke a maker agent when the user explicitly requests content creation or updates. Use when deciding which agent to invoke for a user-driven content creation or update request.
- [Practice 3: Use Checkers for Validation Workflow](./best-practices/use-checkers-for-validation-workflow.md) — Run a checker agent after creation or before publication to validate content quality. Use when deciding whether to validate content before it is published or deployed.
- [Practice 4: Apply Only HIGH Confidence Fixes Automatically](./best-practices/apply-only-high-confidence-fixes-automatically.md) — Fixers should skip MEDIUM confidence and FALSE_POSITIVE findings. Use when reviewing fixer logic that decides which findings to auto-apply.
- [Practice 5: Use Immutable Data Structures](./best-practices/use-immutable-data-structures.md) — Prefer immutable operations such as spread and array methods over direct mutation. Use when writing code that updates objects or arrays and needs to avoid mutating the original.
- [Practice 6: Write Pure Functions](./best-practices/write-pure-functions.md) — Functions should depend only on their inputs, not on external mutable state. Use when writing or reviewing a function to check whether it depends on hidden external state.
- [Practice 7: Compose Small Functions](./best-practices/compose-small-functions.md) — Build complex behavior from small, composable, reusable functions rather than one large function. Use when a function is growing large and could be decomposed into smaller composable functions.
- [Practice 8: Use Criticality Levels for Prioritization](./best-practices/use-criticality-levels-for-prioritization.md) — Checkers should categorize findings by criticality (CRITICAL/HIGH/MEDIUM/LOW) to prioritize fixes. Use when designing a checker's audit report format or prioritizing which findings to fix first.
- [Practice 9: Iterative Improvement via False Positive Feedback](./best-practices/iterative-improvement-via-false-positive-feedback.md) — Use the fixer's false positive reports to improve checker accuracy over time. Use when a fixer detects a false positive and needs to feed that signal back into checker logic.
- [Practice 10: Functional Core, Imperative Shell](./best-practices/functional-core-imperative-shell.md) — Keep pure logic in a core and push side effects to an imperative shell at the boundaries. Use when structuring code that mixes business logic with database, network, or other I/O calls.
- [Summary and Related Documentation](./best-practices/summary-and-related-documentation.md) — Consolidated summary of all ten best practices and links to related pattern documentation. Use when you need a quick-reference summary of every best practice, or links to related docs.
