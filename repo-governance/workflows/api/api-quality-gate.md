---
name: api-quality-gate
title: "api-quality-gate"
description: Exercises a running REST or GraphQL API against its contract and Gherkin specs, fixing every defect via a tester-driven loop until none remain.
when_to_use: Use when a plan ships an API/backend surface needing contract, functional, and security validation against a live deployment.
goal: Validate a live REST or GraphQL API against its contract and existing Gherkin specs, then fix every defect the tester finds and re-test until the defect set is empty
termination: "Zero outstanding in-threshold AET-### findings on two consecutive re-tests against the current deployed build — the double-zero confirmation (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: scope
    type: string
    description: 'Base URL or endpoint set to exercise, plus the contract to test against (e.g., "http://localhost:8302 with apps/ose-be/openapi.yaml")'
    required: true
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
    required: false
    default: strict
  - name: min-iterations
    type: number
    description: Minimum test-fix cycles before allowing zero-finding termination
    required: false
  - name: max-iterations
    type: number
    description: Maximum test-fix cycles to prevent infinite loops
    required: false
    default: 7
  - name: max-concurrency
    type: number
    description: "N+1 background-agent cap. Raise only for independent work with capacity and budget; lower under pressure; never self-promote."
    required: false
    default: 3
outputs:
  - name: final-status
    type: enum
    values: [pass, partial, fail]
    description: Final validation status
  - name: lifecycle-status
    type: enum
    values: [verified, pending, not-applicable]
    description: Lifecycle evidence state, separate from final-status
  - name: iterations-completed
    type: number
    description: Number of test-fix cycles executed
  - name: final-report
    type: file
    pattern: "the destination selected by the tester's output-mode: the plan folder (plan), the plan's delivery.md (delivery), or local-tmp/<slug>/findings.md (local-tmp)"
    description: Final findings record, written wherever the invoked output-mode directs
---

# API Quality Gate Workflow

**Purpose**: Exercise a **running** REST or GraphQL API against its contract (OpenAPI 3.x or
GraphQL SDL) and existing `specs/**` Gherkin, then fix every defect found and re-test until none
remain.

This gate is the API counterpart of the [UI Quality Gate](../ui/ui-quality-gate.md): the UI gate is
a **static** checker/fixer loop over component source, while this gate is a **tester-driven** loop
against a live deployment — every finding originates in an actual HTTP response.

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Shape: Tester-Driven, Not Checker/Fixer](./api-quality-gate/shape-tester-driven-not-checker-fixer.md) — no checker/fixer pair; the loop and its agents.
- [Execution Mode](./api-quality-gate/execution-mode.md) — preferred/fallback execution, how to invoke.
- [Preconditions](./api-quality-gate/preconditions.md) — reachability, contract, non-destructive scope.
- [Step 1: Test](./api-quality-gate/step-1-test.md) — invoke the tester, what it exercises.
- [Step 2: Triage Against Mode](./api-quality-gate/step-2-triage-against-mode.md) — severity-to-threshold mapping.
- [Step 3: Fix](./api-quality-gate/step-3-fix.md) — route findings to the matching `swe-*-dev` agent.
- [Step 4: Re-Test](./api-quality-gate/step-4-re-test.md) — rebuild, redeploy, re-run.
- [Step 5: Double-Zero Confirmation](./api-quality-gate/step-5-double-zero-confirmation.md) — why one zero pass doesn't terminate.
- [Step 6: Iteration Control](./api-quality-gate/step-6-iteration-control.md) — pass/partial/fail, escalation.
- [Relationship to Other Gates](./api-quality-gate/relationship-to-other-gates.md) — surface-conditional applicability, merge precondition.
- [Related Documentation](./api-quality-gate/related-documentation.md) — links to the workflows index, related conventions.
