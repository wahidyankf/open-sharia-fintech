---
title: "PR-Review Quality Gate — Route-Specific Done-Definition"
description: "The five items that must hold for a PR to be 'done': eligible/noneligible route completion, comments answered AND fixes committed+pushed, gates green, and archival-in-PR when applicable."
when_to_use: "Use when checking whether a PR meets this workflow's done-definition before considering merge preconditions."
---

# Route-Specific Done-Definition

Every PR is **done** only when its classifier route's requirements hold:

Before either route begins, the PR body must contain a human-readable review-route record for its
current head. It names the frozen outcome/scope, classification evidence, risk, selected and
skipped lenses with reasons, current checks, settled prior threads, and this cycle's changed probe.
The record makes the route auditable; it does not replace reviewer judgment or add a tool.

1. **Eligible route** — the specialist loop reached [its clean exit](./probe-variation-and-exit.md) —
   two consecutive clean cycles, each under a probe class not previously used on this PR, neither
   leaving **any code-related MEDIUM/HIGH/CRITICAL finding outstanding** —
   counting a scope-deferred finding as outstanding until its follow-up is filed and linked on the
   thread, per the
   [Scope Guard](./scope-deferral-exit.md). The
   default ceiling is five cycles; an authenticated bounded per-PR human extension may raise it.
   Reaching the configured ceiling with any such finding is `blocked`, never done. LOW findings are
   captured and deduplicated into `plans/ideas` but do not prevent this exit.
   At the configured ceiling, freeze the blocked reviewed head, authenticate its non-convergence
   record, and deliver sanitized learning plus one deduplicated improvement idea through the
   separate bounded follow-up defined by [Loop-Exit and Block Rules](./loop-exit-and-block-rules.md).
2. **Noneligible route** — the classifier evidence shows that the full diff is non-executing, and
   `.github/workflows/pr-quality-gate.yml` succeeded for the current PR head. No specialist cycle is
   required or credited for this route.
3. **Every inline review comment is answered AND every accepted fix is COMMITTED AND PUSHED** —
   thread state is not fix state. A thread may be legitimately replied to and resolved while the
   corresponding fix sits uncommitted in the working tree; GitHub then reports zero unresolved
   threads on a PR that still carries the blocking defect. Before this item is satisfied, verify
   against the PR's head commit — not against the resolved-thread count:

   ```bash
   git status --porcelain          # MUST be empty of fix-related paths
   git log origin/<pr-branch> -1   # the fix commit MUST be present on the pushed branch
   gh pr diff <PR>                 # the fix MUST appear in the PR's own diff
   ```

   "All threads resolved" is never sufficient evidence that all findings are fixed.

4. **All applicable PR quality gates are GREEN** — both the local gates and CI on the PR, as of the PR's current
   head commit.
5. **Archival-in-PR is committed** _(applicable when this workflow is invoked from
   `plan-execution.md` Step 8)_ — the plan-to-done archival move
   (`git mv plans/in-progress/<plan> plans/done/YYYY-MM-DD__<plan>` plus README index updates) is
   committed inside the delivering PR itself. This item is N/A for invocations that do not carry a
   plan folder (see the three-repo nuance below).

See [Hardened Merge Preconditions](./hardened-merge-preconditions-a-e.md) for what merges on top of "done".
