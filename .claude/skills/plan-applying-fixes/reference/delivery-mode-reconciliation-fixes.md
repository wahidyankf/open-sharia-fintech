# Delivery-Mode Reconciliation Fixes

Per
[Plans Organization Convention §Delivery Mode](../../../../repo-governance/conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode):
when a HIGH finding flags a PR step under a direct-push mode, reconcile mode and step rather than
reflexively deleting:

- Resolved mode is `worktree-to-origin-main`/`main-to-origin-main` and a PR-creation step (`Create
PR`, `Open PR`, `Submit PR`, or equivalent) is present with no explicit PR requirement documented →
  remove the line (HIGH confidence) and verify the checklist remains sequential.
- If the PR step is actually wanted, correct the declared mode instead: rewrite `## Delivery Mode:`
  to `worktree-to-pr`/`main-to-pr` and scaffold exact-head/base PR-CI steps (see
  `12-worktree-and-delivery-mode-scaffolding-fixes.md`) rather than stripping the step and leaving the plan
  mode-inconsistent.
- A `*-to-pr` plan's PR step is never itself a finding — only its absence or a mismatched mode is.
- **Never apply "remove the line" to a merge step, under any Delivery Mode.** "PR creation step"
  means the step that opens the PR — never the step that merges it; a merge step is out of scope for
  this recipe entirely and stays governed exclusively by
  [How to Fix a Merge-Tag Mismatch](./pr-ci-and-merge-tag-fixes.md#how-to-fix-a-merge-tag-mismatch).
  "Or equivalent" resolves only to other PR-_creation_ phrasings — never a merge phrasing — and a
  direct-push mode does not loosen that boundary: a stray merge step under a direct-push mode is a
  separate finding to surface, not license to delete it here.

## Per-Repository Delivery Mode Restriction

Per
[Plans Organization Convention §Per-Repository Delivery Mode Restrictions (HARD RULE)](../../../../repo-governance/conventions/structure/plans/per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule):
when `plan-checker` item 9's HIGH finding flags a resolved direct-push mode in `ose-public`
(no executable path there), this is a **different finding class** from PR Step/Delivery
Mode Reconciliation above and takes a different fix:

- Always rewrite the resolved mode to `worktree-to-pr` (or `main-to-pr` if the plan's work location
  genuinely requires the primary checkout). Never merely delete the offending step — the mode itself
  is illegal for the repo, not the step.
- After rewriting, scaffold the missing exact-head/base PR-CI steps so the plan is executable
  under the corrected mode.
- **One narrow exception**: a genuine infrastructure-as-code or CI-IaC plan targeting
  `ose-private` may keep only `main-to-origin-main`. Verify that scope before applying the
  exception. `worktree-to-origin-main` is unavailable in both OSE repositories.
- Never silently coerce an author's explicit mode choice without recording why in the fix report.

Verify by re-running `plan-checker`'s item 9 detection and confirming the resolved mode no longer
resolves to a direct-push mode in a restricted repo.
