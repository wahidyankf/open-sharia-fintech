# Business Requirements — oxlint Upgrade and Lint-Toolchain Reproducibility

## The problem in one line

A third party's release schedule could stop this repository from merging, at any moment, with no
change on our side.

## What actually happened

| Time (2026-08-18) | Event                                                         |
| ----------------- | ------------------------------------------------------------- |
| 13:48             | PR #227 head `bd55b19c7` — TypeScript quality gate **passes** |
| 15:10:39          | oxlint 1.79.0 published, adding `react(set-state-in-effect)`  |
| 15:47             | PR #227 head `a652996e6` — same gate **fails**                |

Between those two runs, the PR changed nothing under `apps/ose-www/src`. The failing file was last
edited by an unrelated commit. The diff was innocent; the toolchain moved.

## Cost of doing nothing

**Delivery stalls are unbounded and unpredictable.** 21 projects in `ose-public` and 1 in `ose-private`
each resolved a linter at run time. A release on any day could redden CI on every open PR
simultaneously, with the failure pointing at code nobody touched — the most expensive kind of failure
to diagnose, because every instinct says "look at the diff".

**Diagnosis cost is paid repeatedly.** Establishing that this failure was upstream drift required
correlating the npm publish timestamp against two CI run timestamps and proving the diff was empty for
the named tree. That is not a cheap investigation, and nothing prevents it recurring.

**The pin is a debt, not a fix.** 1.78.0 is now frozen. Every future oxlint improvement — including
genuinely valuable rules — is invisible until someone deliberately upgrades. A pin nobody revisits
silently becomes an abandoned toolchain.

**One real defect is currently unaddressed.** `set-state-in-effect` flags a pattern that causes
cascading re-renders. oxlint found a real problem in production code, and the immediate response was
to stop asking the question.

## Success criteria

1. `search-dialog.tsx` no longer triggers `set-state-in-effect`, and a spec records the intended
   behaviour so a regression is caught.
2. Both repositories run the same current oxlint, pinned, upgraded deliberately.
3. Every rule finding surfaced by the upgrade is either fixed or disabled with a written reason —
   none silently avoided.
4. An enumeration exists of what else the toolchain resolves unpinned, with a verdict per item.

## Non-goals

Replacing oxlint. Removing the eslint pairing. Adopting automated dependency-update bots — that is a
candidate WS-O3 outcome, not a premise.
