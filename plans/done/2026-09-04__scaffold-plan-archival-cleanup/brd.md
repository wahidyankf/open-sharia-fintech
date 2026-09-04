# Business Requirements — Scaffold Plan-Archival Cleanup Steps

## Business Goal

Close the gap between what the governance layer requires at plan completion and what the plan
document actually shows, so cleanup is reviewable rather than merely obligatory.

## The Problem, Stated Concretely

Three surfaces state the obligation:

| Surface                                                           | What it says                                                           |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `worktree-and-artifact-cleanup/branch-cleanup.md`                 | The proof-gated procedure for deleting local and remote branches       |
| `plan-execution/finalization-worktree-cleanup-and-pr-archival.md` | Remove the worktree, complete branch cleanup, run `git worktree prune` |
| `plans/worktree-specification-continued.md`                       | The same sequence at the convention layer                              |

One surface does not:

| Surface                                                  | What it says about branches |
| -------------------------------------------------------- | --------------------------- |
| `plan-creating-project-plans/reference/plan-archival.md` | Nothing — zero mentions     |

That last file is the template every new plan's archival section is authored from. `plan-checker`
does not compensate: `plan-validating-quality` has 21 numbered rules and none of them checks for a
cleanup step.

## Business Impact

- **Cleanup becomes unreviewable.** A reviewer reads `delivery.md`, not `plan-execution`. If the
  document has no cleanup line, there is nothing to check and nothing to catch when it is skipped.
- **The branch inventory dangles.** Every plan records a `Delivery Branch Inventory` and is told to
  classify each entry as delivered, unused, or retained before cleanup. No archival step then
  consumes that classification, so the inventory is produced and never used.
- **Demonstrated, not hypothetical.** The `update-tmp-folders` plan was authored from this template
  and shipped an archival section with worktree removal but no branch deletion. It was caught by a
  maintainer asking, not by any gate.

## Affected Roles

| Role                       | Effect                                                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------------------------- |
| Plan author (`plan-maker`) | Emits two more archival steps from the template. No judgement added — the steps are fixed text.          |
| `plan-checker`             | Gains one presence check inside an existing rule.                                                        |
| `plan-fixer`               | Gains one repair recipe for the finding that check produces.                                             |
| Plan executor              | Sees the cleanup obligation on the checklist it is working from, not only in a workflow it may not open. |
| Reviewer                   | Can verify cleanup was planned by reading the PR's own `delivery.md`.                                    |

## Success Metrics

1. `plan-archival.md` emits a worktree-removal step and a branch-cleanup step that routes to the
   canonical procedure.
2. `plan-checker` produces a finding for a plan whose archival section lacks either step, and
   produces no finding for one that has both — verified in both directions.
3. `plan-fixer` has a recipe that adds the missing steps.
4. Both repositories carry the same scaffolding; the Skill mirrors match their sources.
5. A plan authored after this lands contains both steps without the author having to know the rule.

## Business-Scope Non-Goals

- **No change to the cleanup procedure itself.** `branch-cleanup.md` was hardened in PRs #466 and
  #467 and is correct. Touching it would risk a working thing to fix a documentation gap.
- **No retrofit of archived plans.** `plans/done/` records history.
- **No new rule number** if an existing rule already owns the subject — see `tech-docs.md`.

## Business Risks

| Risk                                                                                            | Severity | Mitigation                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The new check fires on the many existing in-progress and backlog plans, blocking unrelated work | Medium   | Verify the check against every live plan before landing; if it fires broadly, fix those plans in this delivery or scope the check to newly authored plans. |
| Duplicating the cleanup procedure into the template, so two copies drift                        | Medium   | The template routes to `branch-cleanup.md` by link and states only the plan-specific parts.                                                                |
| A new rule number is minted where an existing rule already owns the subject                     | Low      | Placement is decided at the propagation run's Step 4, with extending Rule 10 as the stated preference.                                                     |
| Skill mirrors hand-edited instead of regenerated                                                | Low      | Regeneration is an explicit step; `validate:sync` gates it.                                                                                                |
