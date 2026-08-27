---
name: specs-quality-gate
title: "specs-quality-gate"
description: "Validate explicitly listed specs/ folders for structural completeness, content accuracy, internal consistency, and cross-folder coherence, then apply fixes iteratively until zero findings."
when_to_use: "Use after creating or restructuring spec areas, before major spec refactors, after bulk feature-file changes, or after adding a new app/library to the monorepo."
goal: "Validate explicitly listed specs/ folders for structural completeness, content accuracy, internal consistency, and cross-folder coherence, then apply fixes iteratively until zero findings achieved"
termination: "Zero findings at the configured mode threshold on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: folders
    type: file-list
    description: "Explicit list of spec folders to validate (e.g., [specs/apps/organiclever-be, specs/apps/organiclever]). Each folder and its subfolders are validated. Cross-folder consistency is checked between listed folders."
    required: true
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
    required: false
    default: strict
  - name: min-iterations
    type: number
    description: "Minimum check-fix cycles before allowing zero-finding termination (prevents premature success)"
    required: false
  - name: max-iterations
    type: number
    description: "Maximum check-fix cycles to prevent infinite loops"
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
    description: "Final validation status"
  - name: lifecycle-status
    type: enum
    values: [verified, pending, not-applicable]
    description: Lifecycle evidence state, separate from final-status
  - name: iterations-completed
    type: number
    description: "Number of check-fix cycles executed"
  - name: final-report
    type: file
    pattern: "generated-reports/specs__*__*__audit.md"
    description: "Final audit report (4-part format with UUID chain)"
  - name: execution-scope
    type: string
    description: "Scope identifier for UUID chain tracking (default 'specs')"
    required: false
---

# Specs Validation Workflow

**Purpose**: Validate **explicitly listed** specs/ folders (and their subfolders) for structural
completeness, content accuracy, internal consistency, and cross-folder coherence, then apply
fixes iteratively until all issues are resolved.

**When to use**:

- After creating or restructuring spec areas (e.g., adding demo-fe, consolidating demo specs)
- Before major spec refactors or migrations
- After bulk feature file additions or modifications
- To verify consistency between related spec areas (e.g., demo-be and demo-fe)
- After adding a new app or library to the monorepo

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode and Scope](./specs-quality-gate/execution-mode-and-scope.md) — agent delegation, how to invoke, and what this workflow does/doesn't validate.
- [Validation Dimensions](./specs-quality-gate/validation-dimensions.md) — the nine categories and deterministic rhino-cli offload.
- [Steps — Initial Validation and Fixes](./specs-quality-gate/steps-initial-validation-and-fixes.md) — steps 1-3 of the check-fix loop.
- [Steps — Re-validate Through Termination](./specs-quality-gate/steps-revalidate-through-termination.md) — steps 4-6 and termination criteria.
- [Example and Iteration Usage](./specs-quality-gate/example-and-iteration-usage.md) — worked usage examples and a traced iteration.
- [Safety, Related Workflows, and Conventions](./specs-quality-gate/safety-related-and-conventions.md) — safeguards, related workflows, notes, principles, conventions, and agents.
