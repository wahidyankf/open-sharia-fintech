---
description: Defines the smallest-responsible-change rule, its stop condition, mandatory safeguards, and pass/fail observations.
when_to_use: Use before adding a lasting mechanism, expanding scope, or deciding whether work is complete.
---

# Minimal Sufficiency Test

Choose the smallest responsible change that fully satisfies the requested outcome and every
applicable repository rule. Add code, dependencies, abstractions, validators, automation,
infrastructure, or another lasting mechanism only when existing mechanisms cannot satisfy a
concrete requirement, correctness or safety obligation, or demonstrated recurring risk.

Keep verification proportional to risk and stop when the outcome is achieved and all required
checks pass. Minimal sufficiency never waives TDD, specifications, regression tests,
accessibility, security, documentation, governance propagation, or required quality gates; those
obligations are part of sufficiency.

## Pass and Violation Observations

A change passes when its outcome and applicable rules are satisfied without an unnecessary lasting
mechanism, and every new mechanism names the concrete need it addresses.

A change violates this principle when:

- An existing mechanism satisfies the need but a new one is added
- Work continues beyond the achieved outcome and required checks
- Minimal sufficiency is used to skip a mandatory safeguard

## Enforcement Disposition

**Unenforced by decision.** Whether a mechanism is necessary and verification is proportional
depends on the change's context, so no deterministic gate can decide it reliably. Plan-quality and
pull-request architecture reviews apply this test as a judgment-based check; deterministic gates
continue to enforce the mandatory safeguards listed above.
