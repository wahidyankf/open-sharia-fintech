# Delivery Plan: Optimize the Pull Request Process

## Current State

| Evidence                                                                            | State                                                       |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [Repo-grounded] Merged [PR #250](https://github.com/wahidyankf/ose-public/pull/250) | FOUNDATION at `62608547df0d2063d369537e0753f22699456f44`    |
| [Repo-grounded] Merged [PR #251](https://github.com/wahidyankf/ose-public/pull/251) | REQUIREMENTS at `8884ec79437a05af3e8404e63239e079a379d84f`  |
| [Repo-grounded] DESIGN                                                              | Active: file impact, propagation, transaction, and rollback |
| [Repo-grounded] EXECUTION                                                           | Dormant; no implementation or formal gate in this slice     |
| [Unverified] Complete assembled plan                                                | Must pass a fresh formal gate and grill before activation   |

## Dormant Boundary

Plan assembly is deliberately **dormant and non-executable**. DESIGN may repair only this plan's
`README.md`, `delivery.md`, `learnings.md`, and `tech-docs.md`; REQUIREMENTS already added the
planning-only [idea disposition map](./idea-disposition-map.md). All idea-brief, idea-index, and
idea-routing-reference edits, moves, deletions, and retirements wait for PUB-IDEAS or PRIV-IDEAS
after ACTIVATE. `plans/in-progress/README.md`, the active-plan index changed by FOUNDATION, remains
allowed. No rule, agent, binding, workflow, code, test, implementation, or formal plan gate may
change or run in DESIGN.

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

The exact 20-source classification, owner, retained requirement, and later retirement unit live in
the [idea disposition map](./idea-disposition-map.md). Its public source pin is
`62608547df0d2063d369537e0753f22699456f44`; its private source pin is
`718c20c923707d777a89639f760f98d53740bd70`.

## Audit Ownership Map

The fresh findings are confirmed and remain owned, not waived or deferred forever. Their
[durable PR-native catalog](https://github.com/wahidyankf/ose-public/pull/250#issuecomment-5384375806)
gives every ID a plain-language defect, affected artifact, and REQUIREMENTS, DESIGN, or EXECUTION
owner even after the gitignored source report is cleared.

FOUNDATION and REQUIREMENTS fixed their assigned defects. DESIGN owns F-004, F-019, F-020, and
F-027; its [technical design](./tech-docs.md) now supplies the bounded tree/ledger, propagation and
parity contract, cross-repo transaction, and reverse-order rollback DAG. EXECUTION findings remain
dormant and open. ACTIVATE may open only after every mapped finding is fixed readably. A fresh
formal gate must then pass its full semantic exit, followed by the required grill. Historic audit
evidence cannot substitute.

## Dormant Unit-Edit Contract

After ACTIVATE, every rule unit performs this transaction in its already-owned worktree:

1. Read the unit's merged dependency pin and copy its exact source boundary from the
   [bounded delivery ledger](./tech-docs.md#bounded-delivery-ledger).
2. Run `repo-governance/workflows/repo/repo-rules-propagation.md` with `mode=strict`,
   `isolation=current`, and the unit's normalized rules; retain its placement manifest and sibling
   obligation.
3. Publish the exact hand-authored before-ledger, edit only admitted source paths, then run
   `npm run generate:bindings` once. Treat newly discovered paths as a ledger change requiring a
   scope and size recheck, not silent permission.
4. Run `npm run validate:sync`, capture the tracked source/generated content, rerun
   `npm run generate:bindings`, and prove the tracked content is byte-identical before and after the
   second run. Also prove the file ledger is unchanged and reconcile it to `git status --short`.
5. Record the exact source paths, generated paths, parity result, and private obligation in the PR.
   A missing mirror, unexplained path, or changed second-run ledger fails the unit.

These are design constraints, not authorization to execute a rule wave during plan assembly.

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
