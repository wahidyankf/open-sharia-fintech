---
title: "CI Blocker Resolution Convention"
description: Practice mandating that preexisting CI blockers are investigated at the root cause and fixed properly, never bypassed
category: explanation
subcategory: development
tags:
  - ci
  - quality-gates
  - root-cause
  - debugging
  - anti-pattern
  - preexisting-issues
created: 2026-04-04
when_to_use: "Use when a CI check fails and you need to resolve it without bypassing the gate."
---

# CI Blocker Resolution Convention

This convention mandates that a preexisting CI blocker is investigated to its root cause and fixed properly -- never skipped, disabled, or worked around.

## Documents

- [Principles and Conventions Implemented/Respected](./ci-blocker-resolution/principles-and-conventions-implemented-respected.md) — Principles/conventions implemented. Use to trace this convention's rationale.
- [The Rule](./ci-blocker-resolution/the-rule.md) — The rule mandating preexisting CI blockers be root-caused, never bypassed. Use for the exact wording of the CI-blocker-resolution rule.
- [Forbidden Actions](./ci-blocker-resolution/forbidden-actions.md) — Actions forbidden when resolving a CI blocker. Use before skipping, disabling, or bypassing a CI check.
- [The Investigation Process (Steps 1-4)](./ci-blocker-resolution/the-investigation-process-steps-1-4.md) — Steps 1-4: read the error, blast radius, reproduce, trace to root cause. Use when starting to investigate a CI blocker.
- [The Investigation Process (Steps 5-7)](./ci-blocker-resolution/the-investigation-process-steps-5-7.md) — Steps 5-7: apply the fix, verify, audit an existing mitigation. Use when applying and verifying a fix for a CI blocker.
- [Commit Separation](./ci-blocker-resolution/commit-separation.md) — Why a CI-blocker fix must be its own commit. Use when a CI-blocker fix is bundled with unrelated changes.
- [Examples](./ci-blocker-resolution/examples.md) — Worked examples of resolving a CI blocker correctly. Use for a concrete example of a proper CI-blocker fix.
- [Scope](./ci-blocker-resolution/scope.md) — What this convention applies to. Use when checking whether this convention applies to a CI failure.
- [Operational CI-Availability Exceptions](./ci-blocker-resolution/operational-ci-availability-exceptions.md) — The narrow exceptions for CI-availability outages, not code defects. Use when CI itself is unavailable, not merely reporting a failure.
- [Related Documentation](./ci-blocker-resolution/related-documentation.md) — Related quality-gate and debugging conventions. Use when you need a related convention on quality gates.
