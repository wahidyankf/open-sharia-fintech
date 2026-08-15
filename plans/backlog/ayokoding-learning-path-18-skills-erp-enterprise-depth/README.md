# Plan: Skills Path — ERP Enterprise Depth (Stage B + Stage C)

## Delivery amendment — one final PR

All 15 courses remain within one plan branch and one delivery unit. The sole draft PR opens only in
Phase 9, after verification and Knowledge Capture, and carries the archival move, CI,
merge, and deploy. No earlier stage or delivery boundary opens a PR.

## Overview

Authors Stage B — Conventional Enterprise Depth (12 courses) and Stage C — Sharia-Compliant Design (3 courses), growing the `skills/conventional-erp` and `skills/sharia-erp` JSON manifests from the Stage-A corpus published by plan 17. The retired ERP-programme draft is historical design context only; this plan's execution prerequisite is stated solely below.

## Course-level input context

Several Stage B/C course frontmatter entries cite Stage-A and accounting course ids. Verify those concrete course ids exist in the repository before authoring each affected course. Such artifact checks are not plan prerequisites: the sole plan-level gate is plan 17's archival on `origin/main`.

## Depends-on

| Relation      | Plan (full folder name)                             | Nature                                                                                                                                                                                                                         |
| ------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **blockedBy** | `ayokoding-learning-path-17-skills-erp-foundations` | **Hard; sole direct execution prerequisite.** It must be fully merged and archived on `origin/main` before Phase 0. All earlier completion and repository-baseline facts are transitive context, not extra plan prerequisites. |

**Phase 0 start check:** `git ls-tree -r --name-only origin/main plans/done | rg -q "__ayokoding-learning-path-17-skills-erp-foundations/README\.md` exits 0. This is this plan's only plan-level start gate.

## Course count and stage structure (this plan's slice)

| Stage                                           | Courses | Accounting precondition                      | Boundary reached                                                                         |
| ----------------------------------------------- | ------: | -------------------------------------------- | ---------------------------------------------------------------------------------------- |
| B — Conventional Enterprise Depth               |      12 | plan 15 (`conventional-accounting` complete) | Dangerous 2 (course 16 of 27/30), Dangerous 3 (course 27 — `conventional-erp` ENDS HERE) |
| C — Sharia-Compliant Design (`sharia-erp` only) |       3 | plan 16 (`sharia-accounting` complete)       | Dangerous 4 (course 30 — `sharia-erp` ENDS HERE)                                         |

**Total this plan authors**: 15 courses (10 By Example, 5 Annotated-concept). Combined with plan 17's
15 (8 By Example, 7 Annotated-concept), the full 30-course corpus (18 By Example, 12
Annotated-concept) is complete once this plan merges.

## Manifest growth this plan performs

`<CONVMAN>` (15 → 27, terminal) and `<SHARMAN>` (15 → 27 → 30, terminal) — see
[tech-docs.md §courseOrder arrays at each growth boundary](./tech-docs.md#courseorder-arrays-at-each-growth-boundary)
for the exact insertion positions, carried forward verbatim from the retired source plan.

## Licensing (A8)

General ERP licensing posture is **inherited by consumer echo** from plan 17 (this plan's Stage B
courses cite the same per-project licence table; see
[tech-docs.md §Corpus Custody](./tech-docs.md#corpus-custody)). This plan's **own** first-class
addition is the **Sharia-specific licensing sub-section** for Stage C — the AAOIFI FAS
verbatim-reproduction rule and the PSAK-numbering carry-forward. See
[tech-docs.md §Licensing and IP Compliance — Stage C addendum](./tech-docs.md#licensing-and-ip-compliance--stage-c-addendum-a8).

## Rule-15 retest decision

This plan runs its **own** three-tester Rule-15 retest at its own terminal checkpoint (both manifests
at their final 27/30-id state) — this is **not** redundant with plan 17's own Stage A retest, since
each verifies a distinct, independently-shipped state of the same two landings. See plan 17's
[tech-docs.md §Rule-15 retest split decision](../../in-progress/ayokoding-learning-path-17-skills-erp-foundations/tech-docs.md#rule-15-retest-split-decision)
for the shared reasoning.

## Delivery Mode: worktree-to-pr

This plan has exactly one dedicated worktree, one persistent final-delivery branch, and one PR.
All authoring, verification, and Knowledge Capture phases commit on that branch without a push, PR, merge, or deployment. In Phase 9, the executor commits the archival move and
any index updates, opens the sole draft PR, completes the secret scan, local quality checks, and PR quality-gate verification and CI gates,
marks it ready, and performs the normal AI merge/deploy after the hardened preconditions hold.
No per-course, cohort, stage, or phase worktree/branch/PR is permitted.

## Related documents

- [brd.md](./brd.md) — business rationale, risks.
- [prd.md](./prd.md) — product spec, personas, Gherkin scenarios.
- [tech-docs.md](./tech-docs.md) — the 15-course slice, the accounting-gate re-pointing, prerequisite
  graph, licensing addendum, and every Design Decision.
- [delivery.md](./delivery.md) — the phased execution checklist.
- [syllabus/](./syllabus/README.md) — this plan's own 15 per-course syllabus specs and two
  path-manifest mirrors (full 27/30-id orderings; the first 15 ids in each are references into plan
  17's corpus, not copies).

## Predecessor plan

[`ayokoding-learning-path-17-skills-erp-foundations`](../../in-progress/ayokoding-learning-path-17-skills-erp-foundations/README.md)
— Stage A (15 courses), historical source context nothing accounting-related, already published both manifests at
15 ids before this plan starts.
