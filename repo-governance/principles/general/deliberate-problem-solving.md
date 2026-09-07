---
title: "Deliberate Problem-Solving"
description: Think before coding - surface assumptions, tradeoffs, and confusion rather than hiding them
category: explanation
subcategory: principles
tags:
  - problem-solving
  - communication
  - decision-making
  - clarity
created: 2026-01-29
when_to_use: Use when about to implement a solution and need to check whether assumptions, alternatives, or confusion have been surfaced first.
---

# Deliberate Problem-Solving

- [Vision Supported](./deliberate-problem-solving/vision-supported.md) — Explains how deliberate problem-solving serves the Open Sharia Enterprise vision of trustworthy, transparent, and educational Shariah-compliant systems. Use when explaining why deliberate problem-solving matters to the project's mission, not just as a technical practice.
- [Why This Matters](./deliberate-problem-solving/why-this-matters.md) — Explains the consequences of rushing to implementation without clarity, and what deliberate problem-solving ensures instead. Use when justifying why deliberate analysis is required before writing a solution.
- [Core Practices](./deliberate-problem-solving/core-practices.md) — Lists the four core practices of deliberate problem-solving - stating assumptions, presenting interpretations, suggesting simpler approaches, and stopping when unclear. Use when looking for the concrete Do/Don't practices that operationalize deliberate problem-solving.
- [Application Examples](./deliberate-problem-solving/application-examples.md) — Walks through three worked examples (API integration, database choice, feature implementation) contrasting hidden-assumption failures with deliberate approaches. Use when you need a worked example of applying deliberate problem-solving to a realistic task.
- [Relationship to Other Principles](./deliberate-problem-solving/relationship-to-other-principles.md) — Cross-references deliberate problem-solving to explicit-over-implicit, simplicity-over-complexity, automation-over-manual, and root-cause-orientation. Use when tracing how deliberate problem-solving connects to the repo's other governing principles.
- [Verification Checklist](./deliberate-problem-solving/verification-checklist.md) — A pre-implementation checklist for confirming assumptions, alternatives, and tradeoffs have been surfaced before coding. Use as a checklist immediately before starting implementation on any nontrivial task.
- [For AI Agents](./deliberate-problem-solving/for-ai-agents.md) — States the five agent-specific obligations for deliberate problem-solving, including verification tools and stating limitations. Use when defining or auditing how an AI agent must apply deliberate problem-solving in its own behaviour.
- [Common Violations](./deliberate-problem-solving/common-violations.md) — Three short before/after examples of assuming without verification, choosing silently, and proceeding despite confusion. Use when identifying whether a specific behaviour is a known violation of deliberate problem-solving.

## Summary

Deliberate problem-solving means:

- **Verify** rather than assume
- **Present** rather than choose silently
- **Simplify** rather than over-engineer
- **Ask** rather than guess

This principle ensures correct, maintainable, and appropriate solutions through transparent communication and thoughtful analysis.

## Principle

**Think before coding. Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing any solution, deliberately analyze the problem space, make assumptions explicit, and communicate uncertainties rather than proceeding with hidden confusion.
