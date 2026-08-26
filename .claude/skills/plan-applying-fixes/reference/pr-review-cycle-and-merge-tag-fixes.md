# PR-Review Cycle and Merge-Tag Fixes

## How to Fix a `*-to-pr` Plan Missing the PR-Review Maker→Fixer Cycle

Insert the cycle steps (strictly sequential scout→fan-out→synthesis→fixer; target 1–3, focused
recovery in 4–5, later ordinals only within an authenticated per-PR configured-ceiling extension;
each cycle CI-green-gated) immediately before the PR-merge step, sourced
verbatim in structure from the
[PR Review Quality Gate workflow](../../../../repo-governance/workflows/pr/pr-review-quality-gate.md):
one `- [ ] [AI] Invoke pr-review-scout-maker on $PR` / `- [ ] [AI] Invoke pr-review-synthesis-maker on $PR` /
`- [ ] [AI] Invoke pr-review-fixer on $PR` triple per cycle, the loop-exit condition (**clean
exit** — stop after two consecutive clean current-head cycles under probe classes unused earlier
on that PR; failure to reach that exit at the configured ceiling requires human direction, so
scaffolding every possible cycle is wrong),
and — where the plan folder is tracked in this repo — an archival-in-PR step (`git mv` to
`plans/done/` + README updates) committed inside the same PR, before the final merge step — whatever
tag it already carries. Never retag it while scaffolding.

### How to Fix a Merge-Tag Mismatch

**This recipe is bound by the merge-step structural guard in
`01-merge-step-guard.md` — read that guard before applying anything here.**
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
