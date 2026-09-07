---
description: How the API quality gate invokes api-exploratory-tester for one full live API discovery sweep.
when_to_use: Use when starting an API quality gate run.
---

# Step 1: Discovery (Agent Delegation)

Before invoking the tester, apply the
[lifecycle validation ownership filter](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md).
Pass any exact `delegated-gate-ids` and the resulting evidence ledger to the tester. The filter may
delegate repository mechanics; it never delegates the live API contract, authorization, boundary,
or runtime behaviours exercised here.

Invoke `api-exploratory-tester` with the `scope` input and `output-mode: delivery` when running
inside a plan, or `local-tmp` for a throwaway pass. The tester must omit only predicates identified
by an exact delegated gate ID or its declared `verifies` relationship.

Set `quality-gate-phase: discovery` for this invocation.

Run the full discovery exactly once. The tester exercises, at minimum: contract conformance (status codes, response shapes, error
envelopes), auth/authz boundaries, pagination, idempotency, boundary and edge-case payloads, and —
for GraphQL — nullability, partial errors, and query depth. It compares observed behaviour against
both the contract and existing `specs/**` Gherkin.

**Output**: `AET-###` findings, written to the destination the selected `output-mode` directs — an
existing plan's `delivery.md` under `delivery`, or `local-tmp/<slug>/findings.md` under
`local-tmp`. The tester writes nowhere else; in particular it does not emit to `generated-reports/`.

An unreachable service, unresolved contract, tester crash, or unusable findings record ends the run
with `final-status: fail`. Zero in-threshold findings ends the domain run immediately with
`final-status: pass`; do not invoke the fixer or verification.
