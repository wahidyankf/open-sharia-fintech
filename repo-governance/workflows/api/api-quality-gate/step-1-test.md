---
title: "Step 1: Test (Agent Delegation)"
description: How the API quality gate invokes api-exploratory-tester and what it exercises against the live API.
when_to_use: Use when running the first step of the API quality gate loop.
---

# Step 1: Test (Agent Delegation)

Before invoking the tester, apply the
[lifecycle validation ownership filter](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md).
Pass any exact `delegated-gate-ids` and the resulting evidence ledger to the tester. The filter may
delegate repository mechanics; it never delegates the live API contract, authorization, boundary,
or runtime behaviours exercised here.

Invoke `api-exploratory-tester` with the `scope` input and `output-mode: delivery` when running
inside a plan, or `local-tmp` for a throwaway pass. The tester must omit only predicates identified
by an exact delegated gate ID or its declared `verifies` relationship.

The tester exercises, at minimum: contract conformance (status codes, response shapes, error
envelopes), auth/authz boundaries, pagination, idempotency, boundary and edge-case payloads, and —
for GraphQL — nullability, partial errors, and query depth. It compares observed behaviour against
both the contract and existing `specs/**` Gherkin.

**Output**: `AET-###` findings, written to the destination the selected `output-mode` directs — an
existing plan's `delivery.md` under `delivery`, or `local-tmp/<slug>/findings.md` under
`local-tmp`. The tester writes nowhere else; in particular it does not emit to `generated-reports/`.
