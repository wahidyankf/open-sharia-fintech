---
name: repo-harness-compatibility-quality-gate
title: "repo-harness-compatibility-quality-gate"
description: "Validates internal cross-vendor parity and external harness-conformance drift, then fixes iteratively until zero findings."
when_to_use: "Use after modifying agents, governance prose, or binding-sync logic; after a harness breaking change; or as a scheduled hygiene audit."
goal: "Validate internal cross-vendor parity invariants and external harness-conformance drift, then fix iteratively until zero findings achieved"
termination: "Zero findings on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: scope
    type: string
    description: 'Subset of harnesses to validate: "all", or one of "claude-code", "opencode", "codex".'
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
  - name: iterations-completed
    type: number
    description: Number of check-fix cycles executed
  - name: final-report
    type: file
    pattern: generated-reports/harness-compat__*__*__audit.md
    description: Final audit report (4-part format with UUID chain)
---

# Repository Harness Compatibility Quality Gate Workflow

**Purpose**: Validate two dimensions of binding-file health, then fix iteratively until zero
findings: **internal cross-vendor parity** (five deterministic invariants keeping `.claude/` and
its generated mirrors consistent) and **external harness conformance** (web-research-backed checks that
the platform-bindings catalog and binding files match each harness's upstream conventions).

**Distinct from the pre-push guard**: `harness bindings validate` checks byte-drift; this
workflow's Phase 0 checks parity semantically, Phase 1 checks drift via web research.

**When to use**: after modifying agents/governance prose/binding-sync logic, after a harness
breaking change, as a scheduled hygiene audit, or when onboarding a new harness.

## Contents

- [Execution Mode](./repo-harness-compatibility-quality-gate/execution-mode.md) — invocation.
- [Complementary Anti-Drift Gates](./repo-harness-compatibility-quality-gate/complementary-anti-drift-gates.md) — gates vs. workflow.
- [Research Delegation](./repo-harness-compatibility-quality-gate/research-delegation.md) — web-researcher use.
- [Step 1: Initial Validation](./repo-harness-compatibility-quality-gate/step-1-initial-validation.md) — Phase 0/1 checks.
- [Step 2: Check for Findings](./repo-harness-compatibility-quality-gate/step-2-check-for-findings.md) — threshold counting.
- [Step 3: Apply Fixes](./repo-harness-compatibility-quality-gate/step-3-apply-fixes.md) — auto vs. human scope.
- [Step 4: Re-Validate](./repo-harness-compatibility-quality-gate/step-4-re-validate.md) — confirms fixes.
- [Step 5: Iteration Control](./repo-harness-compatibility-quality-gate/step-5-iteration-control.md) — loop logic.
- [Step 6: Finalization](./repo-harness-compatibility-quality-gate/step-6-finalization.md) — status reporting.
- [Termination Criteria](./repo-harness-compatibility-quality-gate/termination-criteria.md) — pass/partial/fail.
- [Success Criteria — Part 1](./repo-harness-compatibility-quality-gate/success-criteria-gherkin.md) — Phase 0/1, sync fix.
- [Success Criteria — Part 2](./repo-harness-compatibility-quality-gate/success-criteria-gherkin-continued.md) — escalation, budget.
- [Example Usage](./repo-harness-compatibility-quality-gate/example-usage.md) — invocation examples.
- [Iteration Example](./repo-harness-compatibility-quality-gate/iteration-example.md) — worked traces.
- [Safety Features](./repo-harness-compatibility-quality-gate/safety-features.md) — loop and fix safeguards.
- [Related Workflows](./repo-harness-compatibility-quality-gate/related-workflows.md) — Repository Rules Validation.
- [Notes](./repo-harness-compatibility-quality-gate/notes.md) — cadence, guard distinction.
- [Principles Implemented/Respected](./repo-harness-compatibility-quality-gate/principles-implemented-respected.md) — traceability.
- [Conventions Implemented/Respected](./repo-harness-compatibility-quality-gate/conventions-implemented-respected.md) — traceability.
- [Agents](./repo-harness-compatibility-quality-gate/agents.md) — checker and fixer definitions.
