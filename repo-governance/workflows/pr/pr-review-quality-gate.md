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

**Purpose**: Classify every pull request by the behavior its diff changes, then run a bounded,
sequential review loop only for an eligible PR: specialists fan out, a coordinator consolidates
their findings into ONE posted review, a fixer resolves them, CI must be green between cycles.

## Contents

### Core Flow

- [Purpose, Execution Mode, and Classifier](./pr-review-quality-gate/purpose-execution-mode-and-classifier.md) — sequencing rule, eligibility classifier.
- [Participants](./pr-review-quality-gate/participants.md) — the eleven agents, and the trivial-tier branch.
- [Loop Algorithm](./pr-review-quality-gate/loop-algorithm.md) — the review_pr pseudocode and its rules.
- [Pipeline Diagrams](./pr-review-quality-gate/pipeline-diagrams.md) — participants and one-cycle diagrams.

### Steps

- [Steps 0-1 — Classify and Scout Pass](./pr-review-quality-gate/steps-0-1-classify-and-scout.md) — resolve inputs, run the scout.
- [Step 2 — Fan-Out + Synthesis](./pr-review-quality-gate/step-2-fan-out-and-synthesis.md) — specialists into one review.
- [Steps 3-5 — Fixer, CI Gate, Done-Check](./pr-review-quality-gate/steps-3-5-fixer-ci-gate-done-check.md) — triage, the hard gate, final status.

### API Mechanics and Done-Definition

- [GitHub Reviews API Mechanics — Part 1](./pr-review-quality-gate/github-reviews-api-mechanics-part-1.md) — the pinned SHA and its anchors.
- [GitHub Reviews API Mechanics — Part 2](./pr-review-quality-gate/github-reviews-api-mechanics-part-2.md) — reply/resolve, untrusted input.
- [Route-Specific Done-Definition](./pr-review-quality-gate/route-specific-done-definition.md) — the five items making a PR "done".
- [Merge Preconditions — (a)-(e)](./pr-review-quality-gate/hardened-merge-preconditions-a-e.md) — the normative merge gate.
- [Merge Preconditions — Notes](./pr-review-quality-gate/hardened-merge-preconditions-notes.md) — merge command, done-boundary.

### Rules and Reference

- [Loop-Exit and Block Rules](./pr-review-quality-gate/loop-exit-and-block-rules.md) — exit, learn, block.
- [What Code-Related Means](./pr-review-quality-gate/what-code-related-means.md) — the qualifier.
- [Scope Guard](./pr-review-quality-gate/scope-guard-no-scope-creep.md) — no scope creep.
- [Scope-Deferral Exit](./pr-review-quality-gate/scope-deferral-exit.md) — file the follow-up.
- [Review STATE Is Never the Gate](./pr-review-quality-gate/review-state-is-never-the-gate.md) — parse severity.
- [Applicability](./pr-review-quality-gate/applicability.md) — mandatory scope; the Phase 0 exclusion.
- [Related Workflows and Success Metrics](./pr-review-quality-gate/related-workflows-and-success-metrics.md) — composition, tracked metrics.
- [Notes](./pr-review-quality-gate/notes.md) — operating notes, sibling-PR staleness.
- [Principles and Conventions](./pr-review-quality-gate/principles-and-conventions.md) — compliance summary.
