# Delivery Plan: Optimize the Pull Request Process

## Current State

| Evidence                                                                            | State                                                      |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [Repo-grounded] Merged [PR #250](https://github.com/wahidyankf/ose-public/pull/250) | FOUNDATION at `62608547df0d2063d369537e0753f22699456f44`   |
| [Repo-grounded] Merged [PR #251](https://github.com/wahidyankf/ose-public/pull/251) | REQUIREMENTS at `8884ec79437a05af3e8404e63239e079a379d84f` |
| [Repo-grounded] Merged [PR #252](https://github.com/wahidyankf/ose-public/pull/252) | DESIGN at `3ac2468f534be2faaf0b5a784b04b6411313f49e`       |
| [Repo-grounded] EXECUTION-FORECAST                                                  | Active: name human-sized checklist-authoring boundaries    |
| [Unverified] Complete assembled plan                                                | Fresh formal gate and grill still precede activation       |

## Dormant Boundary

Plan assembly is deliberately **dormant and non-executable**. EXECUTION-FORECAST may change only
this plan's `README.md`, `delivery.md`, and `learnings.md`. CORE, WAVES, and CLOSURE remain dormant;
so do all idea, index, routing-reference, rule, agent, binding, workflow, code, test, implementation,
and active-plan-index surfaces. The formal plan-quality gate does not run before complete assembly.

## Sequential Plan Assembly

```text
FOUNDATION (#250) → REQUIREMENTS (#251) → DESIGN (#252) → EXECUTION-FORECAST →
EXECUTION-CORE → EXECUTION-WAVES → EXECUTION-CLOSURE → ACTIVATE/formal-gate/grill →
PUB-IDEAS → PRIV-IDEAS → implementation waves
```

Each arrow is a separate, unstacked PR from then-current `origin/main`, using the same owned public
worktree. Every assembly slice is at most 400 changed hand-authored lines and 20 hand-authored files.
Forecast each slice before opening it; if any would exceed a bound, record its named cohesive
sub-slices in the prior PR before opening the first split. Gate findings use bounded
`ACTIVATE-REPAIR-*` PRs. Final ACTIVATE contains only the clean formal gate, post-write grill, and
executable-status change. Merge green and resync before the next PR.

| Slice             | Contract and audit IDs restored before activation                                                                                     | Target changed lines |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------- | -------------------: |
| EXECUTION-CORE    | Legend, worktrees, mode, boundaries, entry/unit/review/merge transactions; F-005–F-012, F-014–F-017, F-025, F-026, F-028–F-032, F-034 |              260–330 |
| EXECUTION-WAVES   | Numbered PUB/PRIV idea, A1–A3, B, and optional C units with stability and TDD gates; F-035                                            |              280–340 |
| EXECUTION-CLOSURE | Reconciliation/dogfood, knowledge, private terminal proof, public archival, cleanup; F-013, F-018, F-036–F-037                        |              220–300 |
| ACTIVATE          | Clean formal plan-quality gate, post-write grill, and explicit executable-status change                                               |          at most 400 |

CORE groups its 20 findings so a reader can check the allocation without decoding one long row:

- Phases, boundaries, worktrees, executor tags, delivery mode, and review routing: F-005–F-012.
- Failure handling, commits, local verification, and CI: F-014–F-017.
- Current-state, entry, staging, push, PR-body, review, and merge transactions: F-025, F-026, and
  F-028–F-032.
- Plan-amendment escape hatch: F-034.

The other slice names mean:

- WAVES authors the later checklists for paired public/private units: A1 plan-making rules, A2 review
  routing, A3 PR and reply rules, B legacy-conflict cleanup, and optional C tooling only if evidence
  proves it necessary. Any future code change uses test-driven development: write the failing test
  before the behavior change.
- CLOSURE authors the later checklist for reconciling the plan with what landed, dogfooding the
  process—using it on its own PRs—capturing knowledge, closing private work, archiving the public
  plan, and safely removing worktrees.
- ACTIVATE runs the formal plan-quality gate and a structured post-write user review (the “grill”)
  before changing the assembled plan from dormant to executable.

CORE, WAVES, and CLOSURE only author these checklists; none of their described delivery or closure
actions executes before ACTIVATE.

The targets reserve repair headroom below the 400-line ceiling. Each slice is a separate unstacked
PR from then-current `origin/main`, merges green, records its exact pin, and resyncs this same public
worktree before the next slice. If a slice forecast crosses 400 lines or 20 files, split that slice
again in its immediately preceding PR; never rely on a later explanation of an already-large diff.

The exact 20-source classification, owner, retained requirement, and later retirement unit live in
the [idea disposition map](./idea-disposition-map.md). Its public source pin is
`62608547df0d2063d369537e0753f22699456f44`; its private source pin is
`718c20c923707d777a89639f760f98d53740bd70`.

## Audit Ownership Map

The fresh findings are confirmed and remain owned, not waived or deferred forever. Their
[durable PR-native catalog](https://github.com/wahidyankf/ose-public/pull/250#issuecomment-5384375806)
gives every ID a plain-language defect, affected artifact, and REQUIREMENTS, DESIGN, or EXECUTION
owner even after the gitignored source report is cleared.

FOUNDATION, REQUIREMENTS, and DESIGN fixed their assigned defects. The 25 EXECUTION findings remain
open and are allocated above; no forecast claim closes them. ACTIVATE may open only after CORE,
WAVES, and CLOSURE merge and every mapped finding is fixed readably. A fresh formal gate must then
pass semantic exit, followed by the required grill. Historic audit evidence cannot substitute.

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
