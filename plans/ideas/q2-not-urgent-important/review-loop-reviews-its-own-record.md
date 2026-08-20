# Review loops that review their own record

One-line summary: when a PR-review loop's scope includes the correction record the loop itself
writes, each fix adds new falsifiable prose, so the surface under review grows at roughly the rate
it is cleaned and a "zero-finding cycle" termination condition becomes nearly unreachable.

> Surfaced 2026-08-20/21 during `repository-onboarding-readme-refresh` iteration `@01` (PR #239),
> which ran nineteen review cycles where three would have satisfied the governance bar.

## Problem / context

Iteration `@01` opened to fix cross-document defects in five reader-facing onboarding documents. The
`pr-review-quality-gate` loop terminates on a cycle where every specialist returns zero. Nineteen
cycles ran. The shipping surface stopped changing at cycle 14:

| File                                                | Last changed | Cycle |
| --------------------------------------------------- | ------------ | ----- |
| `docs/reference/related-repositories.md`            | `cb489b874`  | 1     |
| `docs/tutorials/getting-started-with-ose-public.md` | `14e58716e`  | 2     |
| `README.md`                                         | `9529a117d`  | 3     |
| `CONTRIBUTING.md`                                   | `afb850f43`  | 5     |
| `docs/how-to/setup-development-environment.md`      | `2be98caac`  | 14    |

The last five commits on the branch — `d805edee1`, `1d89d5f92`, `3d23ad1f9`, `caabf7a02`,
`1e74e33bf` — changed no file outside `plans/`. Every finding from `C-72` onward is the correction
record making a checkable claim about itself, and getting it wrong.

- **The fix is the next defect.** Three consecutive corrections each introduced the finding the next
  cycle returned. `C-74`'s fix wrote an evidence-file split of "eight PNGs and four transcripts"
  copied from a reviewer without counting — it is nine and three, filed as `C-76`. `C-75`'s fix
  wrote that `md-links` "exits 1 on a repository-wide baseline of 312 broken links", implying a red
  gate, when the registered gate carries `args.exclude: [plans/done]` and exits 0 — filed as `C-77`.
  `C-78`'s fix cited the stale count as living in a `P3-013A` item that does not exist in
  `delivery.md` — filed as `C-80`. A loop whose repair step reliably manufactures its next input is
  not converging on anything; it is oscillating.
- **The termination condition was written against a moving surface.** "Zero findings this cycle" is
  a sound stopping rule when the artifact is fixed and the reviewers vary. It is close to
  unreachable when the artifact grows by several hundred words of new, specific, falsifiable prose
  on every iteration — precisely because the reviewers are good. Each `C-nn` row states a count, a
  commit SHA, a gate name, or an item ID, and each of those is something the next cycle can resolve
  and refute.
- **Diagnosing it is not the same as fixing it.** Cycle 13 reached this conclusion in the record's
  own words — the narration "has become a surface that generates defects faster than it retires
  them, at no benefit to any shipped document" — and closed the narrative section as historical.
  The tables, markers, and per-row dispositions stayed in scope, so cycles 14 through 19 kept
  finding defects in them at the same rate. Closing part of a self-referential surface leaves the
  loop self-referential.
- **The governance bar was met at cycle 3.** Three review cycles plus green gates is the documented
  requirement. Cycles 6–19 were not required by any rule; they were the consequence of a stopping
  rule chosen at execution time and never re-examined against its own cost.

## Why now

The cost is concrete and was paid in full: sixteen cycles of two specialist agents each, plus a
correction commit per cycle, to retire defects in an artifact that ships to no reader and is deleted
at plan archival. Meanwhile the reviewers' attention was spent on the record rather than on the five
documents that do ship, which had already been clean for fourteen cycles — the loop was most
expensive exactly where it was least useful. Every plan that keeps an execution or correction record
inside its own review scope inherits this, and the rules currently encourage keeping such a record.

## Prior art / precedents

- **PR Review Quality Gate workflow** — where the termination condition lives, and where a
  scope-exclusion rule would go.
  [pr-review-quality-gate](../../../repo-governance/workflows/pr/pr-review-quality-gate.md)
- **`plan-quality-gate-convergence`** and **`repo-rules-quality-gate-convergence`** — the two
  existing convergence briefs. Both attack the number of iterations needed to reach a first zero by
  running better lenses. This brief is a different failure: no lens improvement helps when the
  artifact under review is written by the loop's own repair step.
  [plan brief](./plan-quality-gate-convergence.md) ·
  [repo-rules brief](./repo-rules-quality-gate-convergence.md)
- **`recurring-defect-family-escalation`** — the closest sibling. There, four cycles found four
  shapes of one root cause and the loop had no trigger to escalate from delta review to root-cause
  review. Same family, adjacent mechanism.
  [brief](./recurring-defect-family-escalation.md)
- **`acceptance-clause-vacuity`** — the counterweight. Any bound on cycles must not become a way to
  stop before the shipping surface is actually clean.
  [brief](../q1-urgent-important/acceptance-clause-vacuity.md)
- **Maker-Checker-Fixer pattern** — the general shape whose fixer step, here, was also an author.
  [maker-checker-fixer](../../../repo-governance/development/pattern/maker-checker-fixer.md)

## Proposed direction (sketch)

- **Separate the shipping surface from the record, and terminate on the shipping surface.** The
  review scope names what merges and affects a reader. The plan's own execution and correction
  records are reviewed once, at the end, not once per cycle. A defect in a record that is archived
  and deleted does not gate a merge.
- **Make the record's growth visible to the stopping rule.** A cycle that produced no change outside
  the plan's own directory is evidence of convergence, not of continued work. "N consecutive cycles
  with no shipping-surface change" is a bounded, falsifiable stopping condition, unlike "zero
  findings" over a surface the loop keeps extending.
- **Cap cycles explicitly, and require a reason to exceed the cap.** State the governance bar at the
  top of the loop and require a named, recorded justification to run past it — the same discipline
  the plans convention already applies to scope.
- **When a correction records itself, prefer the shortest true statement.** Much of the `C-72`…`C-80`
  family exists because rows narrated _why_ a fix was made, in figures. A row that states what
  changed and pins any number to a revision is far harder to falsify than one that also explains
  itself. See the `C-30`/`C-35`/`C-78` chain: one unpinned word count went stale three separate
  times, including inside its own fix.

## Rough scope & non-goals

In scope: the termination condition and scope definition in the PR-review quality-gate workflow; the
guidance on what an execution or correction record should assert about itself; a stated cycle cap
with an escape hatch.

Out of scope (for now): changing what the specialists check or how they are prompted — they behaved
correctly throughout and found real defects every time; removing execution records, which serve a
real audit purpose at archival; anything about the plan-quality-gate loop, which runs before
execution and against a static plan.

## Risks & open questions

- "Terminate on the shipping surface" is wrong for a plan whose deliverable _is_ a record — a
  governance or documentation plan may have no other surface. Where the boundary sits for those is
  unresolved. (open)
- A cycle cap risks the opposite failure: stopping at three while a real reader-facing defect is
  still live. The cap must bind the record, not the shipping surface, and `acceptance-clause-vacuity`
  is the standard it has to clear. (open)
- Reviewing the record once at the end concentrates its defects into a single pass that has no
  follow-up cycle to catch what that pass misses. Whether "once" should be "twice, by different
  disciplines" is a real question. (open)
- This brief is itself a record making claims about a review loop, which is the thing it warns
  about. The counts above are pinned to commits for exactly that reason.

## What success looks like + promotion signal

Success: the next plan that runs a correction iteration reaches merge in a number of cycles close to
the governance bar, with the shipping surface verified clean by at least two independent
disciplines, and its execution record reviewed once rather than nineteen times — measured as "cycles
run after the last shipping-surface change", which was five on this plan and should be at most one.

Ready to promote once the boundary question is settled: which plans have a shipping surface distinct
from their record, and what the rule says for the ones that do not.
