# PR CI and Merge-Tag Fixes

## How to Fix a `*-to-pr` Plan Missing Exact-Head PR CI

Insert a step before merge that verifies `.github/workflows/pr-quality-gate.yml`'s `Quality gate`
is green for the PR's exact current head and base. Add applicable finite surface-gate steps and,
where the plan folder is tracked, archival-in-PR before that final CI verification. Add one focused
`pr-leak-review` step requiring authenticated current-head `pass` evidence; a changed head gets one
replacement pass. Never scaffold broad semantic review by default. Add `pr-review` or
`pr-review-cycle` only from a direct user request and
only at that PR boundary. Never retag the existing merge step while scaffolding.

### How to Fix a Merge-Tag Mismatch

**This recipe is bound by the merge-step structural guard in
`merge-step-guard.md` — read that guard before applying anything here.**
Concretely:

- `*-to-pr` mode with the merge step carrying a tag other than `[AI]`/`[HUMAN]`/`[AI+HUMAN]` → do
  NOT retag it. Follow the Grilling Interaction Contract with all three valid tags and apply only the
  resolved tag. An unrecognized tag may carry human-actor semantics this agent must not silently
  strip — never assume it is safe to overwrite.
- **Never retag, delete, or otherwise remove a `[HUMAN]`- or `[AI+HUMAN]`-tagged merge step, in any
  Delivery Mode.** The tag on the merge step IS the plan's opt-in — there is no separate "explicit
  opt-in" declaration to check for. This is not limited to `*-to-pr` mode: a direct-push mode plan
  with a `[HUMAN]`-tagged merge step (or any recipe that would delete a merge step as a side effect
  of an unrelated fix) is exactly as unsafe as retagging one under `*-to-pr` — the observable
  outcome, the gate is gone, is identical either way. There is no fix action for a `[HUMAN]`- or
  `[AI+HUMAN]`-tagged merge step — leave it alone unconditionally.
- `*-to-origin-main` mode with the final push gated behind an unrequested `[HUMAN]` approval step →
  retag `[AI]` and remove the approval-gate framing (the push itself needs no sign-off under a
  direct-push mode). This is the push, not the merge, so the merge-step guard does not apply here.
