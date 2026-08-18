---
title: "Anti-Patterns in Development Patterns"
description: "Common mistakes when applying the development patterns in this directory."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when reviewing a change for a known anti-pattern."
---

# Anti-Patterns in Development Patterns

> **Companion Document**: For positive guidance on what to do, see [Best Practices](../pattern/best-practices.md)

One anti-pattern per child page below: problem, bad example, solution, rationale.

## Anti-Patterns

- [Overview and Purpose](./anti-patterns/overview-and-purpose.md) — Why pattern anti-patterns matter, and what this document provides. Use when orienting to this document before reading a specific anti-pattern.
- [Anti-Pattern 1: God Agent in Maker-Checker-Fixer](./anti-patterns/god-agent-in-maker-checker-fixer.md) — A single agent tries to create, validate, and fix content instead of using separate maker/checker/fixer agents. Use when designing or reviewing an agent that both creates and validates its own content.
- [Anti-Pattern 2: Skipping Validation Workflow](./anti-patterns/skipping-validation-workflow.md) — Content is deployed without running a checker, skipping the quality gate between creation and publication. Use when a workflow proposes deploying maker output without a checker validation step.
- [Anti-Pattern 3: Applying All Fixes Blindly](./anti-patterns/applying-all-fixes-blindly.md) — A fixer applies every finding without assessing confidence, risking incorrect automated changes. Use when reviewing fixer logic that applies findings without a confidence check.
- [Anti-Pattern 4: Mutating Shared State](./anti-patterns/mutating-shared-state.md) — Code mutates data structures in place instead of creating new ones. Use when reviewing code that mutates function arguments or shared objects.
- [Anti-Pattern 5: Impure Functions with Hidden Dependencies](./anti-patterns/impure-functions-with-hidden-dependencies.md) — A function reads or depends on external mutable state, making its output non-deterministic. Use when a function's output depends on global state.
- [Anti-Pattern 6: Monolithic Functions](./anti-patterns/monolithic-functions.md) — A single large function performs many unrelated responsibilities instead of composing small functions. Use when reviewing a function that mixes validation, transformation, filtering, and aggregation together.
- [Anti-Pattern 7: Ignoring False Positive Feedback](./anti-patterns/ignoring-false-positive-feedback.md) — Fixer-detected false positives are discarded instead of being fed back to improve the checker. Use when a fixer finds a false positive and there is no mechanism to report it back to the checker.
- [Anti-Pattern 8: No Criticality Categorization](./anti-patterns/no-criticality-categorization.md) — Checker findings are listed as a flat, unprioritized list instead of being grouped by criticality. Use when reviewing an audit report that treats all issues as equally important.
- [Anti-Pattern 9: Side Effects Throughout Codebase](./anti-patterns/side-effects-throughout-codebase.md) — Side effects such as logging or notifications are mixed directly into business logic instead of isolated at the boundary. Use when reviewing a function that mixes I/O or side effects with its core calculation.
- [Anti-Pattern 10: Using Maker Instead of Fixer](./anti-patterns/using-maker-instead-of-fixer.md) — A maker agent is used to apply fixes from an audit report, when a validation-driven fixer is the correct tool. Use when deciding whether to invoke a maker or a fixer to address audit-report findings.
- [Summary, Conclusion, and Related Documentation](./anti-patterns/summary-conclusion-and-related-documentation.md) — Summary table of all ten anti-patterns, closing guidance, and links to related pattern documentation. Use when you need a quick-reference table of every anti-pattern and its solution, or links to related docs.
