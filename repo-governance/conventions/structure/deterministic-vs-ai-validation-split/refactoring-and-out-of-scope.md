---
title: "Refactoring to Deterministic, and Out of Scope"
description: The triggers for moving an AI-only category to deterministic, and what this convention deliberately does not define.
when_to_use: Use when an AI-checker category keeps producing the same false positives and might be a candidate to become deterministic, or when checking whether a related concern is covered by this convention.
category: explanation
subcategory: conventions
tags:
  - conventions
  - governance
  - validation
  - quality-gate
  - automation
created: 2026-08-13
---

# Refactoring to Deterministic, and Out of Scope

## When to refactor a category from AI to deterministic

If an AI category accumulates repeated false-positive patterns that can be encoded as predicates, it is a candidate for refactoring to a deterministic check. The triggers:

- The same false-positive shape appears in 3+ consecutive audit reports.
- The shape can be expressed as a regex, file-existence test, or hash comparison.
- Encoding it deterministically would not lose semantic information the AI provides.

When all three hold, propose a new deterministic subcommand in a plan; the AI category's coverage shrinks correspondingly.

## Out of scope

This convention does NOT define:

- **Severity-to-action mapping** — that lives in the [Maker-Checker-Fixer pattern](../../../development/pattern/maker-checker-fixer.md).
- **Skip-list management** — that lives in `local-tmp/.known-false-positives.md` and is governed by the maker-checker-fixer workflow.
- **Which AI model handles which sub-portion** — model selection is a binding concern, not a governance concern; see the [Model Selection guide](../../../development/agents/model-selection.md).
- **CLI implementation language or framework** — those are binding-implementation details; this convention specifies the contract (envelope shape, exit codes), not the implementation.
