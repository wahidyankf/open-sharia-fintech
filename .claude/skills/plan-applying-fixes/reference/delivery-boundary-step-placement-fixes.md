# Delivery-Boundary Step-Placement Fixes

Per
[Plans Organization Convention §Phase 0 Opens No PR](../../../../repo-governance/conventions/structure/plans/phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule):
when a PR-creation/branch-push/PR-Review-Cycle/merge/`gh pr ready`/post-push-CI-verification step is
flagged **inside `## Phase 0`**, the fix is mode-independent — the mode-reconciliation recipe above
does NOT apply here:

- **HIGH confidence → delete the offending Phase 0 line(s)**, including a Phase 0 gate line
  asserting a PR was opened/reviewed/merged. Deleting a Phase 0 merge line is the ONE sanctioned
  exception to the "never delete a merge step" guard, because the merge it asserts must not happen at
  all — it is not a human gate being weakened, it is a phase that has nothing to merge.
- If Phase 0 wrote evidence artifacts, add a sentence to Phase 1 stating the evidence lands in the
  Phase 1 PR — don't leave them orphaned.
- If Phase 0 genuinely produces reviewable changes, do NOT restore the PR step — surface it as a
  mis-scoped Phase 0 (MEDIUM, grill first); the correct resolution is moving that work into Phase 1.
- If a Per-Phase Integration Protocol block is unscoped, add "Phase 1 onward" to its heading/lead
  sentence and state Phase 0 is excluded — don't delete the block; prefer retitling it
  **Delivery-Boundary Integration Protocol**.

Verify by re-running the checker's Phase 0 detection command and reading `0`.

## PR Steps Outside a Delivery Boundary

When a PR-creation/PR-Review-Cycle/`gh pr ready`/merge/post-push-CI-verification step is flagged in a
phase not declared a delivery boundary, the work is **relocated**, not deleted — a PR opens once per
delivery unit, at the unit's boundary.

- **HIGH confidence → move the integration steps down to the delivery unit's boundary phase**,
  merging into that phase's existing integration block. The intermediate phase keeps its own gate and
  Pause Safety note; it simply integrates nothing.
- If the intermediate phase genuinely satisfies the four-part boundary test (coherent / green
  standalone / defensible on `main` / reviewable whole), promote it to a boundary and add its table
  row instead — MEDIUM confidence, grill the author first.
- If `### Delivery Boundaries` is missing, add it with one row per delivery unit, derived from where
  existing integration steps already sit — never invent boundaries the checklist doesn't support.
- If a change-producing phase appears in no row, add it to the unit it belongs to (or its own unit if
  genuinely DAG-independent — the worktree stays the plan's single per-repo instance, reused across
  every delivery unit landed there).
- If the last change-producing phase is not a boundary, make it one.
- Never fold two independent DAG nodes into one delivery unit to silence a finding.

Verify by re-running the checker's two delivery-boundary detection commands and confirming
integration-step phases are a subset of declared boundaries.
