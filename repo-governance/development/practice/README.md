---
title: "Development Practices"
description: Day-to-day practices for solving repository work carefully and collaboratively
category: explanation
subcategory: development
tags: []
created: 2026-05-12
---

# Development Practices

Use these practices when the work is ambiguous, shared, or already in motion. They help contributors and AI agents make careful progress without losing sight of the product or each other.

## Purpose

These practices define **HOW developers and AI agents should behave** when encountering common development situations, covering proactive error resolution and quality-preserving habits that go beyond patterns and tooling.

## Scope

**Belongs Here:**

- Behavioral practices for developers and AI agents
- Proactive quality habits
- Error resolution approaches
- Day-to-day development decision-making guidance

**Does NOT Belong:**

- Reusable code patterns (that's pattern/)
- Tool configuration (that's infra/)
- Testing standards (that's quality/)
- Why we value practices (that's a principle)

## Documents

- [Proactive Preexisting Error Resolution](./proactive-preexisting-error-resolution.md) - When encountering preexisting errors during any work, fix the root cause rather than ignoring, monkey-patching, or passively mentioning the problem
- [Parallel-by-Default Practice](./parallel-by-default.md) - Default to running independent units of work (tool calls, file reads, searches, delegated agents) in parallel rather than serially, capped at three concurrent units
- [Task List Discipline](./task-list-discipline.md) - For any non-trivial multi-step work (3+ steps or spanning multiple files/phases), maintain a live task list from the start and keep it continuously in sync with actual progress
- [File-Touch Discipline](./file-touch-discipline.md) - Keep a deliberate, append-only record of every file you touch, carry it intact through every compaction and handoff, and treat any path not on it as another actor's in-flight work; covers the ledger standards, degraded mode when the ledger is lost, and the rule that generated harness mirrors ship in the same commit as their source
- [Mechanize Cross-File Invariants](./mechanize-cross-file-invariants.md) - When a rule must hold across more than one file, generate the dependent file(s) from a single declared source and validate the result, rather than stating the rule in prose and trusting hand-sync
- [Trustworthy Measurement](./trustworthy-measurement.md) - Before a number justifies a decision, prove the command ran, prove it measured the path that actually executes, and prove the metric can respond to the change; covers false-zero timing harnesses, isolated-vs-batched benchmarks, and critical-path reasoning for max-type metrics

## Related Documentation

- [Development Index](../README.md) - All development practices
- [Development Patterns](../pattern/README.md) - Reusable software development patterns
- [Root Cause Orientation Principle](../../principles/general/root-cause-orientation.md) - The foundational principle this category extends
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model

## Principles Implemented/Respected

This set of development practices implements/respects the following core principles:

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: Practices in this category operationalize root cause analysis into daily development behavior, ensuring errors are fixed at their source rather than worked around.

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Development practices require understanding problems before acting, preventing hasty workarounds that accumulate technical debt.

## Conventions Implemented/Respected

This set of development practices respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: Practice documentation follows active voice, clear structure, and proper formatting standards.
