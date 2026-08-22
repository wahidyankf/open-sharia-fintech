# Correction-Record Freeze (Cycle 2 Onward)

From cycle 2 the brief
OMITS `plans/**` (including `delivery.md` and `learnings.md`): the loop stops reviewing prose it
authored last cycle. Keep the **PR body** in the brief every cycle — a human reads it first. This
is not generated-file filtering — those files are excluded because the loop **wrote** them, not
because a tool emitted them, and cycle 1 still carries them in full. Record the omission.

Two carve-outs, both narrower than the freeze:

- **Plans-only PR** — the plan is the shipping surface, so `plans/**` stays in the brief. Recompute
  this status **every cycle**, exactly as the tier is recomputed: a fixer commit adding a
  `specs/**` file turns a plans-only PR into a mixed one mid-loop, and the carve-out lapses from
  that cycle on.
- **Security-sensitive content** — a `plans/**` hunk touching secrets, `.env`, or git identity
  stays in the brief for `pr-review-security-maker` regardless of cycle. The freeze is a
  noise-control device and never overrides the no-secrets iron rule, which no tier or scope
  decision may weaken.
