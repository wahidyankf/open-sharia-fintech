# Learnings: ayokoding-learning-path-11-course-authoring-capstones

Transient running log of generalizable learnings accrued during execution. Append the moment an
executor notices something worth keeping — do not reconstruct from memory afterward. This file is
drained by the Phase 6 Knowledge Capture step before archival and is never the system of record; see
the [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md).

## Authoring-time note (recorded at plan creation, 2026-08-01)

Two cross-plan documentation discrepancies were found while verifying this plan's dependency map
against sibling plans' own `README.md` files (both already flagged with full evidence in
[tech-docs.md §Two flagged cross-plan documentation discrepancies](./tech-docs.md#two-cross-plan-documentation-discrepancies--found-and-now-reconciled-upstream)):

1. `ayokoding-learning-path-08-course-authoring-security-and-ops`'s README asserts a Band-7 dependency
   for `capstone-data-pipeline` that this plan's direct syllabus-spec read does not support.
2. `ayokoding-learning-path-05-course-authoring-platform-and-concurrency`'s README attributes its own
   downstream capstone dependency to `ayokoding-learning-path-10-...` instead of this plan (`11-...`).

Neither was corrected in the other plans' files (out of this plan's scope — "do not touch any other
plan folder"). If a future pass reconciles these, route it through each affected plan's own
`delivery.md`, not a direct edit from outside.

**Update (2026-08-01)**: both discrepancies were subsequently reconciled directly in the two
sibling plans' own `README.md` files as part of this plan's own fix pass; see `tech-docs.md`
§Two cross-plan documentation discrepancies for the final state.
