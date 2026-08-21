---
name: repo-rules-propagation
title: "repo-rules-propagation"
description: "Places newly-stated rules on the correct surface — instruction surface first, governance layers below — de-conflicting, deduplicating, arming enforcement."
when_to_use: "Use when a decided rule must be written into the repository, or an existing rule superseded."
goal: Land every stated rule on the correct surface, contradicting nothing, duplicating nothing, carrying an enforcement disposition
termination: "PR green, quality gate converged, every rule placed and dispositioned; halts on an unfalsifiable rule or a higher-layer conflict"
inputs:
  - name: rules
    type: string
    description: "Rules as free prose, normalized at Step 0"
    required: true
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Threshold for the Step 8 quality gate"
    required: false
    default: strict
  - name: max-concurrency
    type: number
    description: "Concurrent background agents — the N in the N+1 model"
    required: false
    default: 3
  - name: isolation
    type: enum
    values: [current, dedicated]
    description: "Use the caller's tree, or create a worktree for the run"
    required: false
    default: current
  - name: dry-run
    type: boolean
    description: "Emit the manifest and conflict report, write nothing"
    required: false
    default: false
outputs:
  - name: placement-manifest
    type: file
    pattern: generated-reports/repo-rules-propagation__*__manifest.md
    description: "Per rule — surface, layer, disposition, supersessions"
  - name: final-status
    type: enum
    values: [landed, halted, partial]
    description: Terminal state of the run
  - name: pr-url
    type: string
    description: PR opened by the run
  - name: sibling-obligation
    type: string
    description: "Obligation naming the sibling repository, or an explicit none"
---

# Repository Rules Propagation Workflow

Rules arrive as free prose. They are normalized into falsifiable statements, routed to the
narrowest surface that binds, checked against existing rules under layer-aware precedence, tidied
within their subject, and dispositioned for enforcement before delivery. The run works in the
caller's current tree by default.

The instruction surface is a **fixed-size cache**: admission requires eviction, because the
canonical instruction file and its binding shim both sit within single-digit words of their budget
ceiling. A threshold is never raised to make room.

Agents composed: `.claude/agents/repo/repo-rules-maker.md`, `repo-rules-checker`,
`repo-rules-fixer`. `repo-rules-quality-gate` verifies at Step 8.

## Contents

- [Purpose and Scope](./repo-rules-propagation/purpose-and-scope.md) — what it places, what it refuses.
- [Execution Mode](./repo-rules-propagation/execution-mode.md) — delegation and invocation.
- [Step 0: Intake](./repo-rules-propagation/step-0-intake-and-normalization.md) — prose to falsifiable rule.
- [Step 1: Working Tree](./repo-rules-propagation/step-1-worktree-and-branch.md) — where the run writes.
- [Step 2: Classification](./repo-rules-propagation/step-2-classification.md) — subject, layer, neutrality.
- [Step 3: Conflict Scan](./repo-rules-propagation/step-3-conflict-scan.md) — precedence, supersession.
- [Step 4: Placement](./repo-rules-propagation/step-4-placement-decision.md) — admission test, home table.
- [Step 5: Eviction](./repo-rules-propagation/step-5-eviction-protocol.md) — making room on a full surface.
- [Step 6: Write and Tidy](./repo-rules-propagation/step-6-write-and-tidy.md) — dedupe, retire, reindex.
- [Step 7: Enforcement](./repo-rules-propagation/step-7-enforcement-disposition.md) — the mandatory three-way outcome.
- [Step 8: Verification](./repo-rules-propagation/step-8-verification.md) — bindings, gates, quality gate.
- [Step 9: Delivery](./repo-rules-propagation/step-9-delivery-and-sibling-obligation.md) — PR, recorded obligation.
- [Termination Criteria](./repo-rules-propagation/termination-criteria.md) — landed, halted, partial.
- [Success Criteria](./repo-rules-propagation/success-criteria.md) — Gherkin.
- [Safety Features](./repo-rules-propagation/safety-features.md) — guards on destructive authority.
- [Example Usage](./repo-rules-propagation/example-usage.md) — worked invocations.
- [Related Workflows](./repo-rules-propagation/related-workflows.md) — what runs before and after it.
- [Principles Implemented/Respected](./repo-rules-propagation/principles-implemented-respected.md) — traceability.
- [Conventions Implemented/Respected](./repo-rules-propagation/conventions-implemented-respected.md) — traceability.
