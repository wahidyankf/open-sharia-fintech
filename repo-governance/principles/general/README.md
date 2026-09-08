---
description: Foundational problem-solving values that apply across the repository
when_to_use: Use when deciding whether a cross-cutting, domain-independent value belongs here, or looking up a specific general principle.
---

# General Principles

These principles guide decisions before a task becomes code, a document, or a workflow. Use them when there is more than one plausible path and you need a durable basis for choosing.

## Purpose

These principles define **WHY we value fundamental approaches** that transcend specific domains. They apply universally to all work in this repository, from software development to documentation writing to process design.

## Scope

**✅ Belongs Here:**

- Universal values applicable across all domains
- Foundational beliefs about problem-solving
- Cross-cutting philosophical stances
- Timeless principles guiding all decisions

**❌ Does NOT Belong:**

- Domain-specific principles (software engineering, content)
- Specific implementation rules (that's a convention)
- How-to solve particular problems (that's a guide)

## Principles Implemented/Respected

- [Deliberate Problem-Solving](./deliberate-problem-solving.md) — Think before coding - surface assumptions, tradeoffs, and confusion rather than hiding them Use when about to implement a solution and need to check whether assumptions, alternatives, or confusion have been surfaced first.
- [Simplicity Over Complexity](./simplicity-over-complexity.md) — Choose the smallest responsible change that satisfies the outcome and all applicable rules without unnecessary lasting mechanisms. Use when deciding whether a mechanism is needed, choosing its shape, or deciding when work is complete.
- [Root Cause Orientation](./root-cause-orientation.md) — Find root causes and fix them properly - no temporary fixes, no laziness, senior engineer standards Use when diagnosing a bug or planning a fix and need to check whether the change addresses the actual cause with minimal, senior-engineer-approved scope.

## Related Documentation

- [Core Principles Index](../README.md) - All foundational principles
- [Software Engineering Principles](../software-engineering/README.md) - Domain-specific SE principles
- [Content Principles](../content/README.md) - Domain-specific content principles
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model
