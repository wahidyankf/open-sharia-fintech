---
name: docs-software-engineering-separation-quality-gate
title: "docs-software-engineering-separation-quality-gate"
description: "Validates separation between OSE Platform style guides and AyoKoding educational content, then fixes violations iteratively."
when_to_use: "Use after adding/updating prerequisite relationships or style-guide/AyoKoding content, or periodically for compliance."
goal: Validate software engineering documentation separation between OSE Platform style guides and AyoKoding educational content, apply fixes iteratively until zero findings achieved
termination: "Zero findings on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: scope
    type: string
    description: Documentation scope to validate (e.g., "all", "programming-languages/java", "platform-web/tools/jvm-spring")
    required: false
    default: all
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
    required: false
    default: strict
  - name: min-iterations
    type: number
    description: Minimum check-fix cycles before allowing zero-finding termination (prevents premature success)
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
  - name: iterations-completed
    type: number
    description: Number of check-fix cycles executed
  - name: final-report
    type: file
    pattern: generated-reports/docs-swe-sep__*__audit.md
    description: Final audit report
---

# Software Engineering Documentation Separation Quality Gate Workflow

**Purpose**: Automatically validate separation between OSE Platform style guides
(docs/explanation/software-engineering/) and AyoKoding educational content (apps/ayokoding-www/),
then apply fixes iteratively until all separation violations are resolved.

**IMPORTANT — Validation Scope**: this workflow validates **ONLY** explicit relationships listed
in the Software Design Reference prerequisite table (currently Java, Golang, Elixir, JVM Spring,
JVM Spring Boot). Languages/frameworks not in that table (TypeScript, Python, etc.) are skipped,
enabling incremental migration.

**When to use**: after adding prerequisite relationships to the Software Design Reference, after
updating style guide or AyoKoding content, before major releases, or periodically for compliance.

## Contents

- [Execution Mode](./docs-software-engineering-separation-quality-gate/execution-mode.md) — delegation vs. manual mode.

### Steps

- [Step 1: Initial Validation](./docs-software-engineering-separation-quality-gate/step-1-initial-validation.md) — checker run.
- [Step 2: Check for Findings](./docs-software-engineering-separation-quality-gate/step-2-check-for-findings.md) — threshold decision.
- [Step 3: Apply Fixes](./docs-software-engineering-separation-quality-gate/step-3-apply-fixes.md) — fixer run.
- [Step 4: Re-validate](./docs-software-engineering-separation-quality-gate/step-4-revalidate.md) — confirmation check.
- [Step 5: Iteration Control](./docs-software-engineering-separation-quality-gate/step-5-iteration-control.md) — loop logic.
- [Step 6: Finalization](./docs-software-engineering-separation-quality-gate/step-6-finalization.md) — final status.

### Criteria and Examples

- [Termination Criteria](./docs-software-engineering-separation-quality-gate/termination-criteria.md) — pass/partial/fail rules.
- [Example Usage](./docs-software-engineering-separation-quality-gate/example-usage.md) — invocation scenarios.
- [Iteration Example](./docs-software-engineering-separation-quality-gate/iteration-example.md) — worked trace.

### Reference

- [Safety Features](./docs-software-engineering-separation-quality-gate/safety-features.md) — convergence safeguards.
- [Validation Focus](./docs-software-engineering-separation-quality-gate/validation-focus.md) — what the checker validates.
- [Related Workflows](./docs-software-engineering-separation-quality-gate/related-workflows.md) — composable workflows.
- [Success Metrics](./docs-software-engineering-separation-quality-gate/success-metrics.md) — operational tracking.
- [Notes](./docs-software-engineering-separation-quality-gate/notes.md) — key operating characteristics.
- [Principles Respected](./docs-software-engineering-separation-quality-gate/principles-implemented-respected.md) — governance.
- [Conventions Respected](./docs-software-engineering-separation-quality-gate/conventions-implemented-respected.md) — governance.
- [Agents](./docs-software-engineering-separation-quality-gate/agents.md) — checker/fixer agent links.
