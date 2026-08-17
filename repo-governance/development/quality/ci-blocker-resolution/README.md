---
title: "CI Blocker Resolution Convention"
description: "Practice mandating that preexisting CI blockers are investigated at the root cause and fixed properly, never bypassed"
when_to_use: "Read this index to find the right CI Blocker Resolution Convention child document."
---

# CI Blocker Resolution Convention

- [Principles and Conventions Implemented/Respected](./01-principles-and-conventions-implemented-respected.md) — Principles/conventions implemented. Use to trace this convention's rationale.
- [The Rule](./02-the-rule.md) — The rule mandating preexisting CI blockers be root-caused, never bypassed. Use for the exact wording of the CI-blocker-resolution rule.
- [Forbidden Actions](./03-forbidden-actions.md) — Actions forbidden when resolving a CI blocker. Use before skipping, disabling, or bypassing a CI check.
- [The Investigation Process (Steps 1-4)](./04-the-investigation-process-steps-1-4.md) — Steps 1-4: read the error, blast radius, reproduce, trace to root cause. Use when starting to investigate a CI blocker.
- [The Investigation Process (Steps 5-7)](./05-the-investigation-process-steps-5-7.md) — Steps 5-7: apply the fix, verify, audit an existing mitigation. Use when applying and verifying a fix for a CI blocker.
- [Commit Separation](./06-commit-separation.md) — Why a CI-blocker fix must be its own commit. Use when a CI-blocker fix is bundled with unrelated changes.
- [Examples](./07-examples.md) — Worked examples of resolving a CI blocker correctly. Use for a concrete example of a proper CI-blocker fix.
- [Scope](./08-scope.md) — What this convention applies to. Use when checking whether this convention applies to a CI failure.
- [Operational CI-Availability Exceptions](./09-operational-ci-availability-exceptions.md) — The narrow exceptions for CI-availability outages, not code defects. Use when CI itself is unavailable, not merely reporting a failure.
- [Related Documentation](./10-related-documentation.md) — Related quality-gate and debugging conventions. Use when you need a related convention on quality gates.
