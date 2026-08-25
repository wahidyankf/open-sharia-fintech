---
title: "PR-Review Quality Gate — Purpose, Execution Mode, Classifier"
description: "States the workflow's purpose, sequential execution mode, and five-rule PR eligibility classifier."
when_to_use: "Use to determine PR eligibility for the specialist loop, or check the concurrency rule."
---

# Purpose, Execution Mode, and PR Applicability Classifier

**Purpose**: classify changed behavior, then use a bounded sequential loop for eligible PRs:
route-selected specialists fan out, synthesis posts one verified review, the fixer resolves, and
current-head CI gates the next cycle. Suspected secrets use the incident procedure.

## Execution Mode

Cycles are sequential, with concurrent route-selected fan-out and a full CI-green gate. Before
fan-out, the PR body states the exact head and frozen
outcome/scope, risk tier, selected and skipped lenses with reasons, current evidence, settled
history, and changed probe. This lets a human reader understand the review route without treating
the route as mechanical enforcement.

For a public/private pair, review the source PR to a settled current-head state first, then publish
one terminal successor handoff before a sibling cycle starts. The successor records semantic
correspondence or a reasoned deviation from the immutable source pin; it never assumes byte
identity or creates a concurrent review chain reaction.

## PR Applicability Classifier

Record the current-head classification evidence before specialist review.

1. Inspect the full diff, including generated artifacts and workflow configuration; never classify
   by branch, author, delivery mode, or file count alone.
2. Mark a PR **eligible** when any changed artifact can affect reachable runtime or CI behavior.
3. Mark it **noneligible** only when the full diff is non-executing prose/static governance. A PR
   touching plans is always eligible and PR text cannot waive that route.
4. If evidence is ambiguous or mixed, mark it **eligible**.
5. Check both routes for secrets and invoke history remediation when exposure is suspected.

For a noneligible PR, verify current-head quality gates and ordinary merge preconditions. Eligible
PRs use the bounded loop.
