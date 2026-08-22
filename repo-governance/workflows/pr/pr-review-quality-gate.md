---
name: pr-review-quality-gate
title: "pr-review-quality-gate"
description: "Classify every PR by changed-artifact behavior, then run up to seven sequential specialist-review cycles only for an eligible PR, CI-green gated between cycles."
when_to_use: "Use for every open PR before merge, to decide whether the specialist review loop applies and drive it to done or blocked."
goal: "Classify every pull request by changed-artifact behavior, then run up to seven strictly sequential specialist-review cycles only when the PR is eligible"
termination: every PR has a recorded behavior classification; eligible PRs stop at the first completed cycle with no code-related MEDIUM/HIGH/CRITICAL findings or are blocked after seven cycles; noneligible PRs pass pr-quality-gate and merge without the specialist cycle
inputs:
  - name: pr
    type: string
    description: PR number or URL identifying the pull request under review
    required: true
  - name: cycles
    type: number
    description: "Maximum sequential fan-out to synthesis to fixer cycles for an eligible PR; use a lower value only when the caller explicitly requests it"
    required: false
    default: 7
outputs:
  - name: final-status
    type: enum
    values: [done, blocked, not-applicable]
    description: Whether the PR met its route-specific done-definition, is blocked by unresolved code-related findings, or does not need the specialist cycle
  - name: cycles-completed
    type: number
    description: Number of fan-out-to-fixer cycles actually executed
  - name: unresolved-threads
    type: number
    description: Count of review threads still unresolved when the loop stopped
---

# PR-Review Maker→Fixer Cycle Workflow

**Purpose**: Classify every pull request by the behavior changed in its diff, then run a strictly
sequential, bounded review loop only for an eligible PR: tier-selected specialists fan out, a
coordinator consolidates their findings into ONE posted review, and a fixer resolves them, with a
hard CI-green gate between cycles.

## Contents

### Core Flow

- [Purpose, Execution Mode, and Classifier](./pr-review-quality-gate/purpose-execution-mode-and-classifier.md) — purpose, sequencing rule, eligibility classifier.
- [Participants](./pr-review-quality-gate/participants.md) — the eleven pipeline agents and the trivial-tier branch.
- [Loop Algorithm](./pr-review-quality-gate/loop-algorithm.md) — the review_pr pseudocode and its governing rules.
- [Pipeline Diagrams](./pr-review-quality-gate/pipeline-diagrams.md) — participants flowchart and one-cycle sequence diagram.

### Steps

- [Steps 0-1 — Classify and Scout Pass](./pr-review-quality-gate/steps-0-1-classify-and-scout.md) — resolve inputs, then the scout.
- [Step 2 — Fan-Out + Synthesis](./pr-review-quality-gate/step-2-fan-out-and-synthesis.md) — specialists into one consolidated review.
- [Steps 3-5 — Fixer, CI Gate, Done-Check](./pr-review-quality-gate/steps-3-5-fixer-ci-gate-done-check.md) — triage/push, the hard gate, final status.

### API Mechanics and Done-Definition

- [GitHub Reviews API Mechanics — Part 1](./pr-review-quality-gate/github-reviews-api-mechanics-part-1.md) — pinning the SHA, posting one review.
- [GitHub Reviews API Mechanics — Part 2](./pr-review-quality-gate/github-reviews-api-mechanics-part-2.md) — reply/resolve, untrusted-input filtering.
- [Route-Specific Done-Definition](./pr-review-quality-gate/route-specific-done-definition.md) — the five items that make a PR "done".
- [Merge Preconditions — (a)-(e)](./pr-review-quality-gate/hardened-merge-preconditions-a-e.md) — the normative merge gate.
- [Merge Preconditions — Notes](./pr-review-quality-gate/hardened-merge-preconditions-notes.md) — merge command, done-boundary diagram.

### Rules and Reference

- [Loop-Exit and Block Rules](./pr-review-quality-gate/loop-exit-and-block-rules.md) — exit, learn, block.
- [What Code-Related Means](./pr-review-quality-gate/what-code-related-means.md) — the qualifier.
- [Scope Guard](./pr-review-quality-gate/scope-guard-no-scope-creep.md) — no scope creep.
- [Applicability](./pr-review-quality-gate/applicability.md) — mandatory scope; why Phase 0/non-boundary phases are excluded.
- [Related Workflows and Success Metrics](./pr-review-quality-gate/related-workflows-and-success-metrics.md) — composition and tracked metrics.
- [Notes](./pr-review-quality-gate/notes.md) — operating notes, including sibling-PR staleness.
- [Principles and Conventions](./pr-review-quality-gate/principles-and-conventions.md) — compliance summary.
