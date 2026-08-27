---
title: "Step 3: Fix (Agent Delegation)"
description: How in-threshold findings are routed to the matching swe-*-dev agent and what every fix must ship with.
when_to_use: Use when applying fixes for findings surfaced by the API quality gate tester.
---

# Step 3: Fix (Agent Delegation)

Route each in-threshold finding to the `swe-*-dev` agent matching the service's language. Every fix
lands with a **reproducing test** that fails before the fix and passes after, per the
[Regression Test Mandate](../../../development/quality/regression-test-mandate.md).

Do not create fixes for delegated lifecycle predicates. After changing files, apply the shared
policy's scope-intersection rule to invalidate affected ledger evidence while preserving unrelated
entries.

Where the tester proposes Gherkin for behaviour that is correct but unspecified, add those scenarios
to `specs/**` — a missing spec is a real gap, not a false positive.
