# Content-Placement, File-Impact, and Delivery-Mode Reconciliation Fixes

## BRD/PRD Content-Placement Fixes

When the audit reports misplaced content per the
[Content-Placement Rules](../../../../repo-governance/conventions/structure/plans/14-content-placement-rules.md#content-placement-rules-brdmd-vs-prdmd),
apply (HIGH confidence — mechanical, unambiguous):

- **Business framing in `prd.md`** (sign-off language, sponsors, stakeholders, KPIs, ceremony
  language) → move to `brd.md` (typically Business Impact or Affected Roles). If sign-off/
  approval-gate language is present at all, strip it — this repo is single-maintainer with
  code-review as the only gate.
- **User stories or Gherkin in `brd.md`** → move to `prd.md` (User Stories or Acceptance Criteria).
- **Personas in `brd.md`** → move to `prd.md`.
- **Affected Roles in `prd.md`** → move to `brd.md`.
- **Fabricated numeric targets in BRD** (presented as measured, no baseline) → rewrite as one of:
  observable fact (grep/git/agent round-trip), cited measurement (inline excerpt + URL + access
  date), qualitative reasoning (drop the number), or explicitly labeled `_Judgment call:_ …`. Never
  invent a plausible-sounding number.
- **URL-only citation** → fetch and quote the specific figure/table/excerpt, include it alongside the
  URL and access date. If unable to fetch, classify MEDIUM and flag for manual authoring rather than
  a half-fix.

After moving content, update cross-references pointing at the old location and verify both files
still satisfy their per-file required-sections list.

## File-Impact Tree Repairs

Per
[Plans Organization Convention §File-Impact Analysis Format](../../../../repo-governance/conventions/structure/plans/12-file-impact-analysis-format.md#file-impact-analysis-format-hard-rule):
when a missing/malformed file-impact tree is flagged, reconstruct `## File-Impact Analysis` as a
root-relative fenced `text` tree before editing supporting prose. Preserve every repo-grounded target
already named, give each `[E]`/`[N]`/`[D]`/`[G]`, retain a bounded pattern only when the plan states
how its members are discovered. Non-obvious mechanics go in `### More Detail` immediately below the
tree — never a prose-bullet primary view, invented paths, or delivery checkboxes moved out of
`delivery.md`.

HIGH confidence only when existing targets are repo-grounded and mechanically mappable. If the
footprint is genuinely ambiguous, preserve the finding as MEDIUM for author clarification.

## PR Step / Delivery Mode Reconciliation

Per
[Plans Organization Convention §Delivery Mode](../../../../repo-governance/conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode):
when a HIGH finding flags a PR step under a direct-push mode, reconcile mode and step rather than
reflexively deleting:

- Resolved mode is `worktree-to-origin-main`/`main-to-origin-main` and a PR-creation step (`Create
PR`, `Open PR`, `Submit PR`, or equivalent) is present with no explicit PR requirement documented →
  remove the line (HIGH confidence) and verify the checklist remains sequential.
- If the PR step is actually wanted, correct the declared mode instead: rewrite `## Delivery Mode:`
  to `worktree-to-pr`/`main-to-pr` and scaffold the missing PR-Review Maker→Fixer Cycle steps (see
  `06-worktree-delivery-mode-clarity-fixes.md`) rather than stripping the step and leaving the plan
  mode-inconsistent.
- A `*-to-pr` plan's PR step is never itself a finding — only its absence or a mismatched mode is.
- **Never apply "remove the line" to a merge step, under any Delivery Mode.** "PR creation step"
  means the step that opens the PR — never the step that merges it; a merge step is out of scope for
  this recipe entirely and stays governed exclusively by
  [How to Fix a Merge-Tag Mismatch](./06-worktree-delivery-mode-clarity-fixes.md#how-to-fix-a-merge-tag-mismatch).
  "Or equivalent" resolves only to other PR-_creation_ phrasings — never a merge phrasing — and a
  direct-push mode does not loosen that boundary: a stray merge step under a direct-push mode is a
  separate finding to surface, not license to delete it here.

## Per-Repository Delivery Mode Restriction

Per
[Plans Organization Convention §Per-Repository Delivery Mode Restrictions (HARD RULE)](../../../../repo-governance/conventions/structure/plans/35-per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule):
when `plan-checker` item 9's HIGH finding flags a resolved direct-push mode in `ose-public`/
`ose-primer` (no executable path there), this is a **different finding class** from PR Step/Delivery
Mode Reconciliation above and takes a different fix:

- Always rewrite the resolved mode to `worktree-to-pr` (or `main-to-pr` if the plan's work location
  genuinely requires the primary checkout). Never merely delete the offending step — the mode itself
  is illegal for the repo, not the step.
- After rewriting, scaffold the missing PR-Review Maker→Fixer Cycle steps so the plan is executable
  under the corrected mode.
- **One narrow exception**: a genuinely infrastructure-as-code plan targeting `ose-private` may keep
  a direct-push mode — verify the plan's stated scope actually is infrastructure-as-code before
  treating this as the exception.
- Never silently coerce an author's explicit mode choice without recording why in the fix report.

Verify by re-running `plan-checker`'s item 9 detection and confirming the resolved mode no longer
resolves to a direct-push mode in a restricted repo.

## Phase 0 PR/Push Step Removal

Per
[Plans Organization Convention §Phase 0 Opens No PR](../../../../repo-governance/conventions/structure/plans/23-phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule):
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
