# Correction-Record Freeze (Cycle 2 Onward)

From cycle 2 the brief
OMITS `plans/**` (including `delivery.md` and `learnings.md`): the loop stops reviewing prose it
authored last cycle. Keep the **PR body** in the brief every cycle — a human reads it first. This
is not generated-file filtering — those files are excluded because the loop **wrote** them, not
because a tool emitted them, and cycle 1 still carries them in full. Record the omission.

**Why the freeze exists.** A loop whose scope contains its own correction record reviews the
falsifiable claims it wrote last cycle, so the surface grows about as fast as it is cleaned and a
zero-finding cycle becomes unreachable. On PR #239 the shipping files stopped changing at cycle 14
while the loop ran to 19, and every finding from `C-72` onward was the record making a claim about
itself and getting it wrong. Cycle 1 still reviews the record, so a plan document that misstates the
change is caught once.

Two carve-outs, both narrower than the freeze:

- **Plans-only PR** — the plan is the shipping surface, so `plans/**` stays in the brief. Recompute
  this status **every cycle**, exactly as the tier is recomputed: a fixer commit adding a
  `specs/**` file turns a plans-only PR into a mixed one mid-loop, and the carve-out lapses from
  that cycle on.
- **Security-sensitive content** — a `plans/**` hunk falling anywhere in
  `pr-review-security-maker`'s charter stays in the **shared** brief regardless of cycle — the
  scout hands every specialist one identical brief, so there is no per-specialist copy to add it
  to.
  That is the **whole** charter as stated in
  [`pr-review-security-maker`'s own Owns section](../../../agents/pr-review/pr-review-security-maker.md),
  read by reference and never copied here — a copy drifts, and a drifted copy silently narrows or
  widens what stays reviewable. Naming a shortlist would leave the rest reviewed once and then
  frozen out. The freeze is a noise-control device and never narrows a security charter.
