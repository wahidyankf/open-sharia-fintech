# Delivery Plan: Optimize the Pull Request Process

## Current State

| Evidence                                                                           | State                                                       |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [Repo-grounded] Draft [PR #250](https://github.com/wahidyankf/ose-public/pull/250) | Foundation only; Cycle 1 fixes completed                    |
| [Repo-grounded] Historic audit `378d66`                                            | Invalidated by material compaction; not activation evidence |
| [Repo-grounded] Fresh strict audit `ced0ed`                                        | Failed with F-001–F-037; activation remains closed          |
| [Unverified] Complete assembled plan                                               | Must pass a fresh formal gate and grill before activation   |

## Dormant Boundary

This foundation is deliberately **dormant and non-executable**. Before ACTIVATE, only a planning
artifact inside plan documentation may inventory each idea and record its intended integrate/discard
owner and reason. All idea-brief, idea-index, and idea-routing-reference edits, moves, deletions, and
retirements wait for PUB-IDEAS or PRIV-IDEAS after ACTIVATE. `plans/in-progress/README.md`, the
active-plan index changed by FOUNDATION, is allowed; no rule, agent, binding, workflow, code, or test
may change.

## Sequential Plan Assembly

```text
FOUNDATION (#250) → REQUIREMENTS/idea-disposition-map → DESIGN/file-impact/cross-repo diagrams →
EXECUTION/worktree/mode/boundaries/phases/commands/gates/knowledge/archival →
ACTIVATE/formal-gate/grill → PUB-IDEAS → PRIV-IDEAS → implementation waves
```

Each arrow is a separate, unstacked PR from then-current `origin/main`, using the same owned public
worktree. Every assembly slice is at most 400 changed hand-authored lines and 20 hand-authored files.
Forecast each slice before opening it; if any would exceed a bound, record its named cohesive
sub-slices in the prior PR before opening the first split. Gate findings use bounded
`ACTIVATE-REPAIR-*` PRs. Final ACTIVATE contains only the clean formal gate, post-write grill, and
executable-status change. Merge green and resync before the next PR.

| Slice        | Contract restored before activation                                                                 |
| ------------ | --------------------------------------------------------------------------------------------------- |
| REQUIREMENTS | Business/product structure plus the planning-only public/private idea-disposition map               |
| DESIGN       | File-impact tree, public/private obligation design, propagation/correction and rollback diagrams    |
| EXECUTION    | Worktree/mode/boundaries, phases, commands, gates, review transaction, knowledge, archival, cleanup |
| ACTIVATE     | Clean formal plan-quality gate, post-write grill, and explicit executable-status change             |

## Confirmed Open Audit Map

The 33 findings are **CONFIRMED and intentionally OPEN**, not waived or deferred forever. Their
[durable PR-native catalog](https://github.com/wahidyankf/ose-public/pull/250#issuecomment-5384375806)
gives every ID a plain-language defect, affected artifact, and REQUIREMENTS, DESIGN, or EXECUTION
owner even after the gitignored source report is cleared.

FOUNDATION fixes F-003, F-023, and F-024 in tracked plan text; its PR body fixes F-022. ACTIVATE may
open only after every mapped finding is fixed readably. A fresh formal gate must then pass its full
semantic exit, followed by the required grill. Historic audit evidence cannot substitute.

## Worktree and Cross-Repository Order

[Judgment call] Reuse only the owned public
`/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process` through assembly and later public
waves. Reuse the corresponding private worktree only when PRIV-IDEAS and private waves become
eligible. Never create stacked dependent PRs or force-reset a branch to imitate synchronization.

After activation, PUB-IDEAS merges before PRIV-IDEAS. Later implementation remains sequential:
`PUB-A1 → PRIV-A1 → PUB-A2 → PRIV-A2 → PUB-A3 → PRIV-A3 → PUB-B → PRIV-B → PUB-C? → PRIV-C? →
closure`; C stays a no-change decision unless necessity passes. Public pins and native sibling
obligations keep the repositories semantically “in sync”; private-only deviations stay private.

The EXECUTION slice must turn this order into a 1:1 runnable checklist and preserve every existing
merge step and its authority. No assembly PR may weaken merge gates or begin implementation.

## Preserved Merge Authority (Dormant)

These existing gates remain verbatim and retain their current authority. The dormant boundary makes
them non-executable until assembly and ACTIVATE add every prerequisite; it also places the new
assembly slices before the historical “then” clause below.

- [ ] Mark ready and merge only after semantic exit, then record merge SHA, read the landed diff,
      resync the worktree, and discharge or carry forward the native obligation.
- [ ] Merge/resync PLAN, then deliver PUB-IDEAS and PRIV-IDEAS as separate PRs.
