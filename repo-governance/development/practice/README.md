---
description: Day-to-day practices for solving repository work carefully and collaboratively
when_to_use: Use when the work is ambiguous, shared, or already in motion, and you need a behavioural practice rather than a code pattern or tool configuration.
---

# Development Practices

Use these practices when the work is ambiguous, shared, or already in motion. They help contributors and AI agents make careful progress without losing sight of the product or each other.

## Purpose

These practices define **HOW developers and AI agents should behave** when encountering common development situations, covering proactive error resolution and quality-preserving habits that go beyond patterns and tooling.

## Scope

**Belongs Here:**

- Behavioural practices for developers and AI agents
- Proactive quality habits
- Error resolution approaches
- Day-to-day development decision-making guidance

**Does NOT Belong:**

- Reusable code patterns (that's pattern/)
- Tool configuration (that's infra/)
- Testing standards (that's quality/)
- Why we value practices (that's a principle)

## Documents

- [Proactive Preexisting Error Resolution](./proactive-preexisting-error-resolution.md) — When encountering preexisting errors, bugs, or broken state during any work, fix the root cause rather than ignoring, monkey-patching, or passively mentioning the problem. Use whenever you encounter a preexisting error, broken test, incorrect configuration, or degraded code while doing other work.
- [Parallel-by-Default Practice](./parallel-by-default.md) — Run independent work in parallel within the declared agent budget while routing compute through capacity-controlled admission and preserving logical/correctness edges. Use when scheduling independent work or a multi-repository plan.
- [Resource-Aware Development](./resource-aware-development.md) — Coordinate local compute through the checksum-pinned HIPPO consumer, shared CPU/memory reservations, workload classes, fixed worker mappings, and bounded recovery. Use before running or wiring compute-bearing development work.
- [Task List Discipline](./task-list-discipline.md) — Before any task, including a purely conversational one, open the harness's native task list and keep it continuously in sync with actual progress. Use whenever you are about to start any piece of work.
- [File-Touch Discipline](./file-touch-discipline.md) — Every actor keeps a deliberate, append-only record of the files it touched, carries that record intact across context compaction, and treats every file not on the record as another actor's in-flight work. Use whenever you are about to mutate any file in a shared repository, and always before staging or committing.
- [Mechanize Cross-File Invariants](./mechanize-cross-file-invariants.md) — When a rule must hold across more than one file, generate the dependent file(s) from a single declared source and validate the result, rather than stating the rule in prose and trusting hand-sync. Use when a rule must stay identical across two or more files.
- [Trustworthy Measurement](./trustworthy-measurement.md) — Before a number is allowed to justify a decision, prove the command produced it, prove it measures the path that actually runs, and prove the metric responds to the thing being changed. Use before any benchmark timing or CI metric is used to justify a decision.
- [Code as Liability](./code-as-liability.md) — Every line of code is a maintenance liability, so a pull request that adds code states what it buys, what it costs to maintain, and which simpler alternative was rejected; scrutiny scales with blast radius and tests are exempt. Use when adding code, or deciding whether to solve a problem by writing code at all.

## Related Documentation

- [Development Index](../README.md) - All development practices
- [Development Patterns](../pattern/README.md) - Reusable software development patterns
- [Root Cause Orientation Principle](../../principles/general/root-cause-orientation.md) - The foundational principle this category extends
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model

## Principles Implemented/Respected

This set of development practices implements/respects the following core principles:

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: Practices in this category operationalize root cause analysis into daily development behaviour, ensuring errors are fixed at their source rather than worked around.

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Development practices require understanding problems before acting, preventing hasty workarounds that accumulate technical debt.

## Conventions Implemented/Respected

This set of development practices respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: Practice documentation follows active voice, clear structure, and proper formatting standards.
