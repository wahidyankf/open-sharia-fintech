---
name: ui-quality-gate
title: "ui-quality-gate"
description: Validates UI component quality against frontend conventions and applies fixes iteratively until zero findings are confirmed twice.
when_to_use: Use when auditing or fixing UI components for token compliance, accessibility, dark mode, and responsive design.
goal: Validate UI component quality against frontend conventions, apply fixes iteratively until zero findings achieved
termination: "Zero findings on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
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
  - name: min-iterations
    type: number
    description: Minimum check-fix cycles before allowing zero-finding termination
    required: false
  - name: max-iterations
    type: number
    description: Maximum check-fix cycles to prevent infinite loops
    required: false
    default: 7
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
  - name: iterations-completed
    type: number
    description: Number of check-fix cycles executed
  - name: final-report
    type: file
    pattern: generated-reports/swe-ui__*__audit.md
    description: Final audit report
---

# UI Quality Gate Workflow

**Purpose**: Validate UI component quality (token compliance, accessibility, component patterns, dark mode, responsive design), then apply fixes iteratively until all issues are resolved.

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode](./ui-quality-gate/execution-mode.md) — preferred/fallback execution, how to invoke.
- [Steps](./ui-quality-gate/steps.md) — the six-step check-fix-recheck loop.
- [Safety Features](./ui-quality-gate/safety-features.md) — the four loop safeguards.
- [Example Usage](./ui-quality-gate/example-usage.md) — a worked end-to-end transcript.
- [Related Documentation](./ui-quality-gate/related-documentation.md) — the checker/fixer/maker agents, frontend conventions.
