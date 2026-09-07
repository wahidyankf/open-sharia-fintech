---
name: ui-quality-gate
title: "ui-quality-gate"
description: Validates UI component quality through one discovery pass, an optional fix pass, and one scoped verification pass.
when_to_use: Use when auditing or fixing UI components for token compliance, accessibility, dark mode, and responsive design.
goal: Validate UI component quality, apply one bounded fix pass when needed, and verify the original findings without regressions
termination: "Pass after a clean discovery or successful scoped verification; partial for unresolved findings or regressions; fail for technical validation errors"
inputs:
  - name: scope
    type: string
    description: Files or directories to validate (e.g., "libs/web-ui/", "apps/organiclever-app-web/src/components/")
    required: false
    default: all frontend components
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
    required: false
    default: strict
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
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
  - name: final-report
    type: file
    pattern: local-tmp/swe-ui/swe-ui__*__audit.md
    description: Final audit report
---

# UI Quality Gate Workflow

**Purpose**: Run
[`swe-ui-checker`](../../../.claude/agents/swe/swe-ui-checker.md), apply at most one
[`swe-ui-fixer`](../../../.claude/agents/swe/swe-ui-fixer.md) pass, and verify the original UI
findings plus an affected-component regression smoke.

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode](./ui-quality-gate/execution-mode.md) — preferred/fallback execution, how to invoke.
- [Steps](./ui-quality-gate/steps.md) — the bounded discovery, fix, verification, and finalization flow.
- [Bounded Run](./ui-quality-gate/bounded-run.md) — scope and termination safeguards.
- [Example Usage](./ui-quality-gate/example-usage.md) — a worked end-to-end transcript.

## Success Criteria

```gherkin
Scenario: Clean discovery passes immediately
  Given the discovery check completes without in-threshold findings
  When the workflow evaluates the domain result
  Then final-status is pass
  And the workflow does not invoke the fixer or a verification pass

Scenario: One fix pass verifies cleanly
  Given discovery reports in-threshold findings
  When one fixer pass addresses validated findings
  And scoped verification resolves every original finding without regression
  Then final-status is pass

Scenario: Verification does not converge
  Given scoped verification finds an unresolved original finding or an affected-component regression
  When the workflow finalizes
  Then final-status is partial
  And the workflow does not start another fix or verification pass

Scenario: Lifecycle evidence remains independently blocking
  Given final-status is pass
  And lifecycle-status is pending
  When merge readiness is evaluated
  Then the owning lifecycle gate still blocks delivery
```

## Related Documentation

- [swe-ui-checker](../../../.claude/agents/swe/swe-ui-checker.md) — Validation agent
- [swe-ui-fixer](../../../.claude/agents/swe/swe-ui-fixer.md) — Fix application agent
- [swe-ui-maker](../../../.claude/agents/swe/swe-ui-maker.md) — Component creation agent
- [Frontend Conventions](../../development/frontend/README.md) — Standards enforced by this workflow
