## Outcome and Why

<!--
The intended result and problem this PR solves, in enough detail to judge whether the change answers it.
Required on every PR, including prose-only ones. A list of edits is not a reason.
This statement also bounds review scope — the cycle may not widen it.
See repo-governance/conventions/structure/plans/prs-open-at-delivery-boundaries-pr-body.md
-->

## Scope

<!-- Both halves required. A non-goal without a reason reads as an oversight. -->

- **In scope:**
- **Deliberately not in scope, and why:**

## Summary

<!-- What changed. -->

## Reading Guide

- **Start here:**
- **Skip these paths:** <!-- e.g. generated mirrors: .agents/, .opencode/, .codex/ -->

## Delivery Seam and Deployable State

- **Natural seam:** <!-- Name the cohesive purpose, why these artifacts must land together, and why no unrelated purpose is included. LOC and file counts do not define this boundary. -->
- **Production-deployable state:** <!-- Confirm the exact resulting main state is safe to deploy immediately. Say whether user-reachable behaviour is complete and active or incomplete and inert behind a temporary production-disabled flag. -->
- **Feature flag lifecycle:** <!-- If applicable: flag/default, enabled and disabled tests, rollout, rollback, and removal record. Otherwise: Not applicable, with reason. -->

## Cost/Benefit of Added Code

<!--
Required when this PR adds code — non-Markdown files under apps/, libs/, or scripts/.
Tests, Gherkin specs, and their fixtures are exempt.
Delete this section only if the PR adds no such code.
See repo-governance/development/practice/code-as-liability.md
-->

- **What it buys:**
- **What it costs to maintain:**
- **Simpler alternative rejected, and why:**

## Verification

<!-- Gates run and their results. Name commands, not intentions. -->

## Risk and Rollback

<!-- What could go wrong, how the change is contained, and how to return safely. Keep it brief. -->
