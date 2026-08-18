---
name: repo-dependency-bump-planning
title: "repo-dependency-bump-planning"
description: "Surveys monorepo dependency manifests, classifies bumps per the Dependency Bump Policy, and produces a validated backlog plan — never edits a manifest itself."
when_to_use: "Use for a dependency-hygiene sweep, a pre-release bump snapshot, or an LTS-line upgrade."
goal: >
  Survey every dependency manifest across the monorepo — apps/, libs/, workspace-root pins,
  infra/, and CI toolchain pins under .github/ — classify each candidate bump per the Dependency
  Bump Stability & Safety Policy, and produce a validated backlog plan. The deliverable is the
  plan, never the dependency edits.
termination: >
  A grill-validated plan exists at plans/backlog/<identifier>/, passes plan-quality-gate at
  strict mode, and a dependency clearance report is written to generated-reports/. No manifest
  or lockfile is modified by this workflow.
inputs:
  - name: scope-filter
    type: string
    description: >
      Optional comma-separated glob filter limiting which manifests are inventoried. Default:
      every dependency-bearing manifest in the monorepo (see Phase 1: Inventory).
    required: false
  - name: ecosystems
    type: string
    description: >
      Optional comma-separated filter of ecosystems (npm, cargo, dotnet, go, docker,
      github-actions). Default: all ecosystems present in the inventory.
    required: false
  - name: as-of-date
    type: string
    description: >
      The "today" used for the Path B 60-day cutoff computation (YYYY-MM-DD). Defaults to the
      current date; recorded verbatim in the clearance report.
    required: false
  - name: plan-identifier
    type: string
    description: "Slug for the backlog plan folder. Default: dependency-bump."
    required: false
    default: dependency-bump
  - name: push-target
    type: string
    description: "Git push destination for the backlog plan. Forwarded to plan-planning."
    required: false
    default: "origin main"
outputs:
  - name: clearance-report
    type: file
    pattern: generated-reports/repo-dependency-bump-planning__*__report.md
    description: Inventory + Security & Functional Clearance Status table + cutoff computation. Always written.
  - name: plan-path
    type: string
    description: Path to the created backlog plan in plans/backlog/<identifier>/
  - name: final-status
    type: enum
    values: [pass, partial, fail]
    description: Final status after the backlog plan's quality gate
---

# Repository Dependency Bump Planning Workflow

**Purpose**: Turn the [Dependency Bump Stability & Safety Policy](../../development/workflow/dependency-bump-policy.md)
into a validated **backlog plan** for updating dependencies across the whole monorepo — survey,
classify, and hand off to `plan-planning` to author the plan.

**The outcome is the plan, not the implementation** — this single-pass `planning`-type workflow
never edits a manifest, updates a lockfile, or runs a bump. The
[Plan Execution workflow](../plan/plan-execution.md)'s own Step 0 promotes the plan to
`plans/in-progress/` later; the policy's Application Workflow steps 8–12 become that plan's
delivery checklist.

## Contents

- [Execution Mode](./repo-dependency-bump-planning/execution-mode.md) — Direct Orchestration.
- [When to Use](./repo-dependency-bump-planning/when-to-use.md) — the three trigger scenarios.
- [Phase 0: Pre-flight](./repo-dependency-bump-planning/phase-0-pre-flight.md) — clean tree, cutoff, scope.
- [Phase 1: Inventory](./repo-dependency-bump-planning/phase-1-inventory.md) — enumerate every manifest.
- [Phase 2: Candidate Discovery](./repo-dependency-bump-planning/phase-2-candidate-discovery-and-classification.md) — path/CVE/KEV/EPSS research.
- [Phase 3: Clearance Table](./repo-dependency-bump-planning/phase-3-clearance-table-and-decisions.md) — assemble and write the report.
- [Phase 4: Human Checkpoint](./repo-dependency-bump-planning/phase-4-human-checkpoint.md) — the hard approval gate.
- [Phase 5: Backlog Plan Establishment](./repo-dependency-bump-planning/phase-5-backlog-plan-establishment.md) — invoke plan-planning.
- [Phase 6: Hand-back](./repo-dependency-bump-planning/phase-6-hand-back.md) — final summary, re-run reminder.
- [Gherkin Success Criteria](./repo-dependency-bump-planning/gherkin-success-criteria.md) — the three scenarios.
- [Related Documents](./repo-dependency-bump-planning/related-documents.md) — policy, workflows, agents, registers.
- [Principles Implemented/Respected](./repo-dependency-bump-planning/principles-implemented-respected.md) — traceability.
- [Conventions Implemented/Respected](./repo-dependency-bump-planning/conventions-implemented-respected.md) — traceability.
