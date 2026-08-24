# The review loop has no escalation when one defect family recurs

One-line summary: four consecutive PR-review cycles each found a CRITICAL, and all four were the
same root cause wearing a new shape — the loop caught every instance and never once asked whether
the _design_ was wrong, because each specialist is chartered to the delta and its SUPPRESS rules
explicitly forbid the restructuring finding that would have ended it in one cycle.

> Surfaced 2026-08-19/20 during `update-harness-support` (ose-public #232 / ose-private #56).
> Cycles 4, 5, 6, 7 — the review budget is seven.

## Problem / context

The measured outcome, one plan, one PR pair:

| Cycle | CRITICAL found | Shape                                                        | Fix applied                                 |
| ----- | -------------- | ------------------------------------------------------------ | ------------------------------------------- |
| 4     | yes            | empty `vendored[]` value flips fail-safe to fail-destructive | added an empty-dir guard                    |
| 5     | yes            | same, via `""` and `/`                                       | rejected those two literals                 |
| 6     | yes            | same, via four whitespace paddings                           | rejected `value != value.trim()`            |
| 7     | yes            | same, via a typo'd entry and a trailing separator            | bidirectional check, component-wise compare |

Read one row at a time this is a healthy gate: four real data-loss defects caught before merge, each
reproduced live, none shipped. Read as a column it is a process defect — the loop converged on
shapes, never on the rule that turned shapes into deletions, and consumed the entire seven-cycle
budget doing it.

Three mechanisms produced that, and none of them is anyone behaving badly:

- **The specialists are chartered to the delta, and their SUPPRESS blocks forbid the finding that
  would have ended it.** `pr-review-architecture-maker` suppresses "defense-in-depth restructuring"
  and "restructuring when the PR's declared scope doesn't touch X". In cycle 6 it recorded, in its
  own report, that it _considered_ filing the design concern and concluded "on balance this falls
  inside the SUPPRESS block". Those rules exist for a good reason — they are what stops review
  turning into unbounded redesign — but they are unconditional, so the one finding that could break
  a recurrence is exactly the one the process is tuned to discard.
- **Cross-cycle memory carries findings, not families.** The scout brief propagates a _settled
  issues_ list — what must not be re-litigated. There is no inverse channel: nothing says "this is
  the third cycle touching this function; treat the design as suspect." Each cycle re-approaches the
  delta as though it were the first.
- **The fixer is briefed with sites, and fixes sites.** Cycle 6's brief said, in bold, _fix the
  class, not the shapes_. The fixer did — at the validation layer, which is where the named shapes
  lived. "Class" resolved to "all whitespace shapes", not "all inputs that can defeat the rule",
  because the brief named whitespace and the rule was never the subject.

A fourth contributor sits in development rather than review: TDD as practised here produced one
test per shape, each falsifiable in both directions, all passing — and no test ever stated the
invariant (_no registry content may delete a file the emitter did not generate_). A property or
fuzz test over the `vendored[]` value would have surfaced all six shapes at once, in cycle 4.

## Why now

The seven-cycle cap assumes cycles converge. A recurring family does not converge — it consumes the
budget one shape at a time, and the cap then expires with the class still open, which is exactly
what happened here (cycle 7 produced a CRITICAL and there was no cycle 8; closure required stepping
outside the workflow). The cost is measurable: roughly three hours of wall clock in this plan alone,
two full fixer runs at ~45 minutes each, and a defect family that reached cycle 7 rather than being
named in cycle 4.

This will recur wherever a plan introduces a destructive operation, which is not rare here — the
harness-binding emitters, the mirror cleanups, and the parity machinery all delete files.

## Prior art / precedents

- **PR-Review Maker-Fixer Cycle** — where the escalation rule and the cross-cycle family ledger
  would land; the scout already owns cross-cycle state, so the channel exists and is one-directional.
  [pr-review-quality-gate](../../../repo-governance/workflows/pr/pr-review-quality-gate.md)
- **`pr-review-scout-maker` / `pr-review-synthesis-maker`** — the two stages that already read prior
  cycles; either could own family detection.
  [agent catalog](../../../.claude/agents/README.md)
- **Root Cause Orientation principle** — the repo already asserts this as a first-class principle;
  the review workflow is where it is structurally hardest to honour, and currently does not.
  [principles](../../../repo-governance/principles/README.md)
- **`deletion-authorized-by-absence`** — the sibling brief: the concrete design defect this loop
  took four cycles to name. Useful as the worked example for whatever rule comes out of this.
- **Five Whys / Andon cord** — the manufacturing analogue: a repeated defect stops the line and
  triggers a root-cause investigation rather than a fourth rework.

## Proposed direction (sketch)

- **Recurrence trigger, early not late.** When a cycle's finding lands in the same function, file, or
  named invariant as the previous cycle's, the _next_ cycle must charter a root-cause pass whose
  question is "is this design correct?" rather than "is this delta correct?" — and that pass is
  explicitly exempt from the incrementalism SUPPRESS clauses. Trigger on the second occurrence, not
  on budget exhaustion.
- **Carry a defect-family ledger, not only a settled-issues list.** The scout brief already
  propagates what must not be re-raised; add what _has_ recurred, with the anchors, so a specialist
  can see it is standing in a repeat.
- **Brief the fixer with the invariant, not the sites.** State the property that must hold, require
  the fixer to answer "what class of input could still violate this?", and treat an unanswered
  version of that question as an incomplete fix.
- **Invariant tests for destructive operations.** Where a code path deletes or overwrites, require a
  property/fuzz test asserting the invariant, in addition to the per-case regression tests. This is a
  development-side rule, not a review-side one, and is probably the highest-leverage of the four.

## Rough scope & non-goals

In scope: the recurrence trigger and its SUPPRESS exemption; the family ledger in the scout brief;
the fixer briefing convention; the invariant-test requirement for destructive paths.

Out of scope (for now): raising or removing the seven-cycle cap — the cap is not the defect, and
raising it would have bought a fifth shape rather than a root cause; rewriting the specialists'
SUPPRESS blocks generally, which earn their keep in the ordinary case.

## Risks & open questions

- A root-cause pass exempt from SUPPRESS is exactly the unbounded-redesign failure the SUPPRESS
  rules were written to prevent. It needs a bound — probably "name the invariant and the minimal
  change that restores it", not "propose an architecture". Unresolved. (open)
- "Same function, file, or invariant" is a crude recurrence signal; two genuinely unrelated defects
  can share a file. Whether detection should be mechanical (anchor overlap) or a synthesis judgement
  is open — mechanical is cheap and will over-trigger. (open)
- The invariant-test requirement collides with the repo's existing Gherkin-and-unit conventions; a
  property test fits neither tier cleanly, and where it lives needs an answer.
- Counter-evidence worth stating plainly: the loop _did_ catch every instance before merge, and a
  process change that trades away that reliability for speed is a bad trade. Any rule here must be
  additive.

## What success looks like + promotion signal

Success: a defect family that recurs across two cycles triggers a chartered root-cause pass, and the
resulting finding names a rule or design rather than a shape. Measured crudely: no future plan
spends more than two review cycles on one root cause.

Ready to promote once the bound on the root-cause pass is settled — without it the rule trades one
failure mode for a worse one.
