# Delivery Plan: Optimize the Pull Request Process

## Current State

| Evidence                                                                            | State                                                        |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [Repo-grounded] Merged [PR #250](https://github.com/wahidyankf/ose-public/pull/250) | FOUNDATION at `62608547df0d2063d369537e0753f22699456f44`     |
| [Repo-grounded] Merged [PR #251](https://github.com/wahidyankf/ose-public/pull/251) | REQUIREMENTS at `8884ec79437a05af3e8404e63239e079a379d84f`   |
| [Repo-grounded] Merged [PR #252](https://github.com/wahidyankf/ose-public/pull/252) | DESIGN at `3ac2468f534be2faaf0b5a784b04b6411313f49e`         |
| [Repo-grounded] Merged [PR #253](https://github.com/wahidyankf/ose-public/pull/253) | FORECAST at `a46725dba24c4880e7854b0b5504b26dd3bdbb33`       |
| [Repo-grounded] Merged [PR #254](https://github.com/wahidyankf/ose-public/pull/254) | Split forecast at `b4dca85adc9ebc42eb53d69500e5d0475adb1522` |
| [Repo-grounded] Merged [PR #255](https://github.com/wahidyankf/ose-public/pull/255) | CORE-ENTRY at `6e3412576ee32b8a34882c8f5df38019a1825e03`     |
| [Repo-grounded] Merged [PR #256](https://github.com/wahidyankf/ose-public/pull/256) | CORE-REVIEW at `b872a142a5063ff8d97bc04b89bc090529c932a4`    |
| [Repo-grounded] Merged [PR #257](https://github.com/wahidyankf/ose-public/pull/257) | WAVES-SPLIT at `aa5f14f768d0a8c4e0877d8aab7135b4d7529135`    |
| [Repo-grounded] WAVES-ENTRY                                                         | Active: author entry, ideas, and exception checklists        |
| [Unverified] Complete assembled plan                                                | Fresh formal gate and grill still precede activation         |

> **AUTHORING-ONLY UNTIL ACTIVATE:** WAVES-ENTRY changes plan docs only; it runs no gate or implementation.

## Executor Legend and Plain-Language Terms

After ACTIVATE: `[AI]` acts, `[HUMAN]` decides, and `[AI+HUMAN]` means agent prep plus human action.

| Term                 | Meaning                                                                   |
| -------------------- | ------------------------------------------------------------------------- |
| Worktree             | A second checkout reserved for this plan.                                 |
| Delivery unit        | One branch, one PR, and one independently stable result.                  |
| Pin                  | An immutable commit SHA used as evidence.                                 |
| File ledger          | The exact admitted path list before and after work.                       |
| Current head         | The exact commit currently under review and checked by CI.                |
| Review-route record  | A PR comment naming risk, review lenses, frozen scope, and exact head.    |
| Review lens          | One review area, such as logic, security, or documentation.               |
| Eligible route       | The diff can execute/change behavior, or touches `plans/**`; review runs. |
| Noneligible route    | The whole diff is non-executing; only its required quality gate runs.     |
| Semantic exit        | The point where scope, checks, review threads, and audit are complete.    |
| Landed-diff proof    | Evidence that merged content equals the reviewed change.                  |
| Resync               | Fetch merged `main`, read what landed, then branch from that `main`.      |
| Sibling obligation   | A PR record asking the other repository to adapt or explain a difference. |
| Changed probe        | A different focused check used after a review method misses a defect.     |
| Patch fingerprint    | A stable content hash proving reviewed and landed patches are equal.      |
| `PLAN-AMENDMENT`     | A plan-only repair PR that freezes dependent work until it merges.        |
| Local adaptation     | Private wording/path changes that preserve the public rule's intent.      |
| Private deviation    | An intentional private-only difference, recorded with its reason.         |
| Unrelated follow-up  | A real defect outside this wave, filed separately without widening it.    |
| Portable defect      | A public-source mistake proven by private evidence and wrong to adapt.    |
| `satisfied`          | Private work implements the obligation.                                   |
| `reasoned-deviation` | Private records why a deliberate difference is correct.                   |
| `N/A`                | Evidence proves that this obligation does not apply.                      |

## Dormant Boundary

Plan assembly is deliberately **dormant and non-executable**. WAVES-ENTRY may change only this
plan's `README.md`, `delivery.md`, and `learnings.md`. WAVES-A, WAVES-RULES, EXECUTION-CLOSURE,
ideas, indexes, rules, agents, bindings, workflows, code, tests, implementation, and active-plan
indexes remain dormant. The formal gate waits for complete assembly.

## Worktree

Reuse exactly one worktree per repository for this whole plan; follow the
[specification][worktree-spec], [cap][worktree-cap], and [path rule][worktree-path]:

- public: `worktrees/optimize-pr-process/` resolves to
  `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process` — active for assembly;
- private: `worktrees/optimize-pr-process/` resolves to
  `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process` — quarantined until PRIV-IDEAS.

Both already exist. Never add a second. If one is later proven absent, run from that repository root:

```bash
git fetch origin main
git show-ref --verify refs/heads/optimize-pr-process-base
git worktree add worktrees/optimize-pr-process optimize-pr-process-base # branch exists
git worktree add -b optimize-pr-process-base worktrees/optimize-pr-process origin/main # branch absent
git worktree prune # stale registration only; retry the applicable add once
```

The private worktree intentionally carries a modified `plans/ideas/README.md` and deleted
`plans/ideas/q2-not-urgent-important/pr-review-governance-reference-defects.md`. Do not stash,
discard, reset, or mix that overlay. PRIV-IDEAS must compare its full diff with the disposition map.

## Delivery Mode

Both repositories use `worktree-to-pr`: every delivery unit is a fresh branch from then-current
`origin/main`, one draft PR to `main`, and one independently stable result. No direct-to-main push,
stacked dependency, or concurrent mutation is allowed. CORE-REVIEW adds the route and cycle rules.

## Sequential Plan Assembly

```text
FOUNDATION (#250) → REQUIREMENTS (#251) → DESIGN (#252) → FORECAST (#253) →
CORE-SPLIT-FORECAST → CORE-ENTRY → CORE-REVIEW → WAVES-SPLIT → WAVES-ENTRY → WAVES-A →
WAVES-RULES → EXECUTION-CLOSURE → ACTIVATE/formal-gate/grill → PUB-IDEAS → PRIV-IDEAS →
implementation waves
```

Each arrow is a separate, unstacked PR from then-current `origin/main`, using the same owned public
worktree. Every assembly slice is at most 400 changed hand-authored lines and 20 hand-authored files.
Forecast each slice before opening it; if any would exceed a bound, record its named cohesive
sub-slices in the prior PR before opening the first split. Gate findings use bounded
`ACTIVATE-REPAIR-*` PRs. Final ACTIVATE contains only the clean formal gate, post-write grill, and
executable-status change. Merge green and resync before the next PR.

| Slice             | Contract and audit IDs restored before activation                                                                                       | Target changed lines |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------: |
| CORE-ENTRY        | Complete Phase 0–5 gate/pause-safe spine and state model, plus Phase 0–3 mechanics; F-005–F-011, F-014–F-016, F-025, F-026, F-028–F-030 |              230–300 |
| CORE-REVIEW       | Review route, CI, correction firewall, merge and amendment; F-012, F-017, F-031, F-032, F-034                                           |              150–230 |
| WAVES-SPLIT       | Forecast-only repair after missing task classes pushed the complete EXECUTION-WAVES forecast above the hard cap                         |               70–125 |
| WAVES-ENTRY       | Contract; baselines/repairs; ideas; correction and sole PLAN-AMEND adapters; F-035 ENTRY partial                                        |              285–330 |
| WAVES-A           | PUB/PRIV A1–A2 checklists, acceptance, pair gates, and prior-pair reconciliation; F-035 A partial                                       |              190–250 |
| WAVES-RULES       | PUB/PRIV A3 and B; optional-C decision/trigger; pair gates and prior-pair reconciliation; F-035 terminal owner                          |              200–270 |
| EXECUTION-CLOSURE | Reconciliation/dogfood, knowledge, private terminal proof, public archival, cleanup; F-013, F-018, F-036–F-037                          |              220–300 |
| ACTIVATE          | Clean formal plan-quality gate, post-write grill, and explicit executable-status change                                                 |          at most 400 |

The complete-preview accounting below uses the 350-line authoring measurement recorded in this PR
as source evidence, then counts one forecast changed line per separately tagged action, gate, and
pause record. Its 734-line cross-PR sum is intentionally larger: each independent slice repeats its
own status/ownership/acceptance scaffolding, and the first draft omitted conditional and pause tasks.

| Complete-preview component           | WAVES-ENTRY | WAVES-A | WAVES-RULES |
| ------------------------------------ | ----------: | ------: | ----------: |
| Status, ownership, and formatting    |          24 |      18 |          18 |
| Contract, acceptance, and path data  |          28 |      18 |          18 |
| Two Phase 0 baselines                |          14 |       0 |           0 |
| Two conditional baseline repairs     |          64 |       0 |           0 |
| Owned ordinary-unit tasks            |          86 |     120 |         104 |
| Separate phase gates/pause records   |          18 |      40 |          40 |
| Public-correction adapter            |          32 |       0 |           0 |
| Sole `PLAN-AMENDMENT` adapter        |          32 |       0 |           0 |
| Prior-pair reconciliation            |           0 |      12 |          16 |
| C decision/trigger                   |           0 |       0 |          32 |
| **Forecast complete-preview total**  |     **298** | **208** |     **228** |
| **Repair headroom to range ceiling** |      **32** |  **42** |      **42** |

Every preview includes all conditional routes assigned to that slice. If actual authoring crosses
its range ceiling, the preceding merged PR must forecast another split before the oversized slice
opens; a checklist may not reclaim headroom by bundling independent actions.

Prior-pair reconciliation means that, after a private PR merges, the next public slice compares the
immutable public/private merge pins, copies completed task evidence into the public plan, and checks
the sibling obligation. A missing pin, unchecked prior task, or unresolved obligation blocks entry.

The two CORE slices keep the original 20-finding ownership complete:

- CORE-ENTRY owns the complete lifecycle spine and separate authoring, pushed-head, review, CI,
  merge, landed-proof, resync, and sibling states, plus detailed Phase 0–3 mechanics.
- CORE-REVIEW owns routing, review/fixer cycles, current-head CI, cross-repo correction limits,
  merge/landed proof, and `PLAN-AMENDMENT`.

The other slice names mean:

- WAVES-ENTRY authors the task/evidence contract, baselines/repairs, idea retirement, public
  correction, and the sole reusable `PLAN-AMENDMENT` task adapter. WAVES-A owns A1 plan-making and
  A2 review-routing units. WAVES-RULES owns A3 PR/reply rules, B legacy cleanup, and the C decision;
  a positive C decision only triggers the ENTRY-owned adapter. F-035 closes after all three pins.
- EXECUTION-CLOSURE authors the later checklist for reconciling the plan with what landed, dogfooding the
  process—using it on its own PRs—capturing knowledge, closing private work, archiving the public
  plan, and safely removing worktrees.
- ACTIVATE runs the formal plan-quality gate and a structured post-write user review (the “grill”)
  before changing the assembled plan from dormant to executable.

Both CORE slices, WAVES-SPLIT, WAVES-ENTRY, WAVES-A, WAVES-RULES, and EXECUTION-CLOSURE only author
plan text or checklists; none executes before ACTIVATE.

The targets reserve repair headroom below the 400-line ceiling. Each slice is a separate unstacked
PR from then-current `origin/main`, merges green, records its exact pin, and resyncs this same public
worktree before the next slice. If a slice forecast crosses 400 lines or 20 files, split that slice
again in its immediately preceding PR; never rely on a later explanation of an already-large diff.

## Parallelization Model

Delivery is sequential. A successor starts only from its predecessor's merged pin. Reviewers may
fan out within one cycle; cycles, mutations, units, and merges do not overlap. CORE-REVIEW defines
the narrow frozen-PR exception used during one public correction.

### Delivery Boundaries

Every unit repeats Phases 1–5 below. `PUB-WT` and `PRIV-WT` mean the declared worktrees;
The three WAVES checklist slices supply exact unit scope/acceptance; EXECUTION-CLOSURE supplies Phase 6.

| Phase(s) | Unit        | Repo/WT         | Branch                                               | Mode           | PR      | Predecessor                 | Stable result             |
| -------- | ----------- | --------------- | ---------------------------------------------------- | -------------- | ------- | --------------------------- | ------------------------- |
| 0        | PUB-BASE    | public/PUB-WT   | `—`                                                  | no delivery    | no      | ACTIVATE                    | public baseline recorded  |
| 1–5?     | PUB-REPAIR  | public/PUB-WT   | `optimize-pr-process-public-baseline-repair-<slug>`  | worktree-to-pr | Phase 3 | ACTIVATE                    | public baseline repaired  |
| 1–5      | PUB-IDEAS   | public/PUB-WT   | `optimize-pr-process-pub-ideas`                      | worktree-to-pr | Phase 3 | PUB-REPAIR? else ACTIVATE   | public ideas retired      |
| 0        | PRIV-BASE   | private/PRIV-WT | `—`                                                  | no delivery    | no      | PUB-IDEAS                   | overlay-safe baseline     |
| 1–5?     | PRIV-REPAIR | private/PRIV-WT | `optimize-pr-process-private-baseline-repair-<slug>` | worktree-to-pr | Phase 3 | PUB-IDEAS                   | private baseline repaired |
| 1–5      | PRIV-IDEAS  | private/PRIV-WT | `optimize-pr-process-priv-ideas`                     | worktree-to-pr | Phase 3 | PRIV-REPAIR? else PUB-IDEAS | private ideas retired     |
| 1–5      | PUB-A1      | public/PUB-WT   | `optimize-pr-process-pub-a1`                         | worktree-to-pr | Phase 3 | PRIV-IDEAS                  | plan rules coherent       |
| 1–5      | PRIV-A1     | private/PRIV-WT | `optimize-pr-process-priv-a1`                        | worktree-to-pr | Phase 3 | PUB-A1                      | private A1 adapted        |
| 1–5      | PUB-A2      | public/PUB-WT   | `optimize-pr-process-pub-a2`                         | worktree-to-pr | Phase 3 | PRIV-A1                     | review routing coherent   |
| 1–5      | PRIV-A2     | private/PRIV-WT | `optimize-pr-process-priv-a2`                        | worktree-to-pr | Phase 3 | PUB-A2                      | private A2 adapted        |
| 1–5      | PUB-A3      | public/PUB-WT   | `optimize-pr-process-pub-a3`                         | worktree-to-pr | Phase 3 | PRIV-A2                     | PR/reply rules coherent   |
| 1–5      | PRIV-A3     | private/PRIV-WT | `optimize-pr-process-priv-a3`                        | worktree-to-pr | Phase 3 | PUB-A3                      | private A3 adapted        |
| 1–5      | PUB-B       | public/PUB-WT   | `optimize-pr-process-pub-b`                          | worktree-to-pr | Phase 3 | PRIV-A3                     | legacy conflict removed   |
| 1–5      | PRIV-B      | private/PRIV-WT | `optimize-pr-process-priv-b`                         | worktree-to-pr | Phase 3 | PUB-B                       | private conflict removed  |
| 1–5      | PUB-C?      | public/PUB-WT   | `optimize-pr-process-pub-c`                          | worktree-to-pr | Phase 3 | PRIV-B                      | necessity-gated mechanism |
| 1–5      | PRIV-C?     | private/PRIV-WT | `optimize-pr-process-priv-c`                         | worktree-to-pr | Phase 3 | PUB-C                       | private C adapted         |
| 1–5?     | PUB-CORR?   | public/PUB-WT   | `optimize-pr-process-pub-<wave>-correction-1`        | worktree-to-pr | Phase 3 | portable defect + pin       | replacement public pin    |
| 1–5?     | PLAN-AMEND? | public/PUB-WT   | `optimize-pr-process-plan-amendment-<slug>`          | worktree-to-pr | Phase 3 | plan defect + frozen pin    | amended plan pin          |
| 1–6      | CLOSURE     | public/PUB-WT   | `optimize-pr-process-closure`                        | worktree-to-pr | Phase 6 | last unit                   | plan archived and focused |

Repair rows activate only after their baseline fails; each runs Phases 1–5, merges, and reruns that
baseline. Its ordinary successor uses the repair merge SHA; otherwise it uses the normal pin shown.
Optional C becomes a recorded no-change decision when necessity fails. Before each unit, replace
its predecessor with the exact SHA in the task, body, and audit comment. Missing state blocks the
next row. A correction resumes its paused private PR from the replacement public pin; an amendment
resumes its frozen unit from the amended plan pin.

The exact 20-source classification, owner, retained requirement, and later retirement unit live in
the [idea disposition map](./idea-disposition-map.md). Its public source pin is
`62608547df0d2063d369537e0753f22699456f44`; its private source pin is
`718c20c923707d777a89639f760f98d53740bd70`.

## Audit Ownership Map

The fresh findings are confirmed and remain owned, not waived or deferred forever. Their
[durable PR-native catalog](https://github.com/wahidyankf/ose-public/pull/250#issuecomment-5384375806)
gives every ID a plain-language defect, affected artifact, and REQUIREMENTS, DESIGN, or EXECUTION
owner even after the gitignored source report is cleared.

FOUNDATION through CORE-REVIEW are merged. ACTIVATE may open only after WAVES-ENTRY, WAVES-A,
WAVES-RULES, and EXECUTION-CLOSURE instantiate every delivery unit as granular, attributable
checkboxes and every finding is fixed. A fresh formal gate and grill must then pass; historic
evidence cannot substitute.

## Dormant Execution-Wave Entry Checklist

Every checkbox below is inert until ACTIVATE merges. It describes later work; this assembly PR does
not run a command, edit an idea, touch the private overlay, change a rule, or open an implementation
PR. After activation, copy only the active unit's unchecked IDs into the harness-native task list
1:1. Keep this Markdown as the durable evidence index and allow only one active unit at a time.

### Task and Evidence Contract

- [ ] `[ENTRY:C.01][AI]` Verify ACTIVATE's merge SHA before copying the first active unit.
- [ ] `[ENTRY:C.02][AI]` Copy every active Markdown ID into the live task list without combining it.
- [ ] `[ENTRY:C.03][AI]` Record repository, worktree, branch, predecessor pin, and current main pin.
- [ ] `[ENTRY:C.04][AI]` Publish the exact admitted source/generated path ledger before editing.
- [ ] `[ENTRY:C.05][AI]` Record hand-authored line/file forecast, safety choice, risk, and rollback.
- [ ] `[ENTRY:C.06][AI]` Keep later units frozen and record the one authorized successor.
- [ ] `[ENTRY:C.07][AI]` Link each completion to command/observation, expected result, and actual result.
- [ ] `[ENTRY:C.08][AI]` Give each `N/A` an artifact owner, evidence, reason, and remaining action.
- [ ] `[ENTRY:C.09][AI]` Keep local, pushed-head, reviewed-head, CI, merge, and resync states separate.
- [ ] `[ENTRY:C.10][AI]` Read back every AI-authored GitHub artifact and its `Generated by AI` marker.
- [ ] `[ENTRY:C.11][AI]` Reconcile live tasks, Markdown IDs, file ledger, and `git status` at each gate.
- [ ] `[ENTRY:C.12][AI]` Stop on a missing pin, unexpected path, unresolved obligation, or failed gate.
- [ ] `[ENTRY:C.13][AI]` Record the phase's exact pause-safe state before switching activities.
- [ ] `[ENTRY:C.14][AI]` Use a separate bounded repair or amendment; never widen the active unit.

Idea retirement accepts only the paths in the [idea disposition map](./idea-disposition-map.md).
For each mapped brief, `test ! -e <brief>` and an index `rg` must fail on the predecessor and pass
on the reviewed head. Retain commands, pins, outputs, and the disposition link. If the negative
reading cannot be reproduced, stop rather than interpreting an unexplained pass as success.

### PUB-BASE — Public Repository Baseline

- [ ] `[PUB-BASE:P0.1][AI]` Verify ACTIVATE is an ancestor of current public `origin/main`.
- [ ] `[PUB-BASE:P0.2][AI]` Record public worktree, branch, head, and clean-or-explained status.
- [ ] `[PUB-BASE:P0.3][AI]` Run `npm install` and retain its exit state.
- [ ] `[PUB-BASE:P0.4][AI]` Run plain `npm run doctor` and retain its exit state.
- [ ] `[PUB-BASE:P0.5][AI]` Run the repository pre-push gate and retain its exit state.
- [ ] `[PUB-BASE:P0.6][AI]` If any result fails, open only PUB-REPAIR; otherwise record its `N/A`.
- [ ] `[PUB-BASE:P0.G][AI]` Pass Phase 0 and record PUB-IDEAS' exact predecessor and entry command.
- [ ] `[PUB-BASE:P0.P][AI]` Record repository, result, predecessor, and re-verification command.

### PUB-REPAIR — Conditional Public Baseline Repair

Open this unit only for a reproduced pre-existing public baseline failure. The failure and repair
must be unrelated to PUB-IDEAS' retirement; otherwise repair the ordinary unit within its scope.

- [ ] `[PUB-REPAIR:P1.1][AI]` Name the failed command, first bad pin, root-cause owner, and bounded slug.
- [ ] `[PUB-REPAIR:P1.2][AI]` Enter the declared repair branch from current public `origin/main`.
- [ ] `[PUB-REPAIR:P1.3][AI]` Publish exact repair paths, forecast, stable-main safety, and rollback.
- [ ] `[PUB-REPAIR:P1.4][AI]` Reproduce the failure before editing and retain the full diagnostic.
- [ ] `[PUB-REPAIR:P1.5][AI]` Edit only the proven repair paths; keep PUB-IDEAS frozen.
- [ ] `[PUB-REPAIR:P1.G][AI]` Pass the Phase 1 branch/base/pin/scope/ledger gate.
- [ ] `[PUB-REPAIR:P1.P][AI]` Record branch, head, ledger, dirty state, and reproduction command.
- [ ] `[PUB-REPAIR:P2.1][AI]` Run the focused regression and the original failing baseline command.
- [ ] `[PUB-REPAIR:P2.2][AI]` Run applicable local gates and the public pre-push gate.
- [ ] `[PUB-REPAIR:P2.3][AI]` Prove actual hand-authored size and ledger stay within both caps.
- [ ] `[PUB-REPAIR:P2.4][AI]` Stage only the repair ledger; inspect cached paths, checks, stat, and patch.
- [ ] `[PUB-REPAIR:P2.5][AI]` Commit one cohesive repair and read its complete committed diff.
- [ ] `[PUB-REPAIR:P2.G][AI]` Pass the Phase 2 acceptance/staging/commit gate.
- [ ] `[PUB-REPAIR:P2.P][AI]` Record local head and clean tree or named intended residue.
- [ ] `[PUB-REPAIR:P3.1][AI]` Recompute caps, rerun pre-push, and push only the repair branch.
- [ ] `[PUB-REPAIR:P3.2][AI]` Open one draft human-readable repair PR with the AI marker.
- [ ] `[PUB-REPAIR:P3.3][AI]` Read back base, head, draft state, body, and whole-PR statistics.
- [ ] `[PUB-REPAIR:P3.G][AI]` Pass the Phase 3 exact-boundary and human-entry-point gate.
- [ ] `[PUB-REPAIR:P3.P][AI]` Record draft URL, current head, and literal body path.
- [ ] `[PUB-REPAIR:P4.1][AI]` Post/read back the exact-head route; run its bounded review cycle.
- [ ] `[PUB-REPAIR:P4.2][AI]` Disposition findings natively and resolve only evidenced outcomes.
- [ ] `[PUB-REPAIR:P4.3][AI]` Prove current-head CI and all five readiness preconditions; mark ready.
- [ ] `[PUB-REPAIR:P4.G][AI]` Pass Phase 4 with semantic exit, green CI, and frozen scope.
- [ ] `[PUB-REPAIR:P4.P][AI]` Record reviewed head, cycle/thread/CI state, and sibling `N/A`.
- [ ] `[PUB-REPAIR:P5.1][AI]` Recheck readiness and compute the reviewed patch fingerprint.
- [ ] `[PUB-REPAIR:P5.2][AI]` Squash-merge by repository-qualified API; read the landed diff.
- [ ] `[PUB-REPAIR:P5.3][AI]` Match fingerprints, fetch main, and resync the worktree to the merge SHA.
- [ ] `[PUB-REPAIR:P5.4][AI]` Rerun PUB-BASE there; on success authorize only PUB-IDEAS.
- [ ] `[PUB-REPAIR:P5.G][AI]` Pass Phase 5 with merge, landed proof, resync, and successor pin.
- [ ] `[PUB-REPAIR:P5.P][AI]` Record merge/main SHA, baseline result, and PUB-IDEAS entry command.

### PUB-IDEAS — Retire the 19 Public Sources

- [ ] `[PUB-IDEAS:P1.1][AI]` Verify PUB-BASE or PUB-REPAIR and current public `origin/main`.
- [ ] `[PUB-IDEAS:P1.2][AI]` Enter `optimize-pr-process-pub-ideas` from that exact main pin.
- [ ] `[PUB-IDEAS:P1.3][AI]` Publish the 19-brief/index ledger and admit no other path.
- [ ] `[PUB-IDEAS:P1.4][AI]` Record forecast, static-doc safety, risk, and rollback-by-revert.
- [ ] `[PUB-IDEAS:P1.5][AI]` Record propagation and generated bindings as reasoned `N/A`.
- [ ] `[PUB-IDEAS:P1.6][AI]` Revalidate every disposition against the activated plan pin.
- [ ] `[PUB-IDEAS:P1.7][AI]` Delete only the 19 mapped public briefs.
- [ ] `[PUB-IDEAS:P1.8][AI]` Remove only their live entries from `plans/ideas/README.md`.
- [ ] `[PUB-IDEAS:P1.9][AI]` Reconcile `git status` exactly to the retirement ledger.
- [ ] `[PUB-IDEAS:P1.G][AI]` Pass the Phase 1 pin/scope/size/ledger gate.
- [ ] `[PUB-IDEAS:P1.P][AI]` Record branch, head, ledger, dirty state, and negative-read commands.
- [ ] `[PUB-IDEAS:P2.1][AI]` Run predecessor/new-head IDEAS acceptance and retain outputs.
- [ ] `[PUB-IDEAS:P2.2][AI]` Run Markdown checks and the repository pre-push gate.
- [ ] `[PUB-IDEAS:P2.3][AI]` Prove hand-authored changed lines/files remain inside both caps.
- [ ] `[PUB-IDEAS:P2.4][AI]` Stage only admitted paths; inspect cached names, check, stat, and patch.
- [ ] `[PUB-IDEAS:P2.5][AI]` Commit the cohesive retirement and read the complete committed diff.
- [ ] `[PUB-IDEAS:P2.G][AI]` Pass the Phase 2 acceptance/staging/commit gate.
- [ ] `[PUB-IDEAS:P2.P][AI]` Record local head and clean tree or named intended residue.
- [ ] `[PUB-IDEAS:P3.1][AI]` Recompute caps, rerun pre-push, and push only the declared branch.
- [ ] `[PUB-IDEAS:P3.2][AI]` Open one draft human-readable PR ending `Generated by AI`.
- [ ] `[PUB-IDEAS:P3.3][AI]` Read back base, head, draft state, literal body, and PR statistics.
- [ ] `[PUB-IDEAS:P3.G][AI]` Pass the Phase 3 boundary and human-entry-point gate.
- [ ] `[PUB-IDEAS:P3.P][AI]` Record draft URL, current head, and literal body path.
- [ ] `[PUB-IDEAS:P4.1][AI]` Post/read back the exact-head route; run bounded review cycles.
- [ ] `[PUB-IDEAS:P4.2][AI]` Disposition every finding natively and resolve proven outcomes only.
- [ ] `[PUB-IDEAS:P4.3][AI]` Prove current-head CI and all five preconditions; mark/read ready.
- [ ] `[PUB-IDEAS:P4.G][AI]` Pass Phase 4 with semantic exit, green CI, and frozen scope.
- [ ] `[PUB-IDEAS:P4.P][AI]` Record reviewed head, cycle/thread/CI state, and pending private obligation.
- [ ] `[PUB-IDEAS:P5.1][AI]` Recheck readiness and compute the reviewed patch fingerprint.
- [ ] `[PUB-IDEAS:P5.2][AI]` Squash-merge by repository-qualified API; read the landed diff.
- [ ] `[PUB-IDEAS:P5.3][AI]` Match fingerprints and record the immutable merge SHA.
- [ ] `[PUB-IDEAS:P5.4][AI]` Publish/read the private obligation with expected paths and owner.
- [ ] `[PUB-IDEAS:P5.5][AI]` Resync public; authorize only PRIV-BASE in the quarantined worktree.
- [ ] `[PUB-IDEAS:P5.G][AI]` Pass Phase 5 with merge, landed proof, resync, and sibling state.
- [ ] `[PUB-IDEAS:P5.P][AI]` Record merge/main SHA, obligation state, and PRIV-BASE entry command.

### PRIV-BASE — Overlay-Safe Private Baseline

Here, overlay fingerprint means the output of `git diff --binary -- plans/ideas/README.md
plans/ideas/q2-not-urgent-important/pr-review-governance-reference-defects.md | shasum -a 256`;
hashing the diff represents the authorized deletion without pretending its worktree file has bytes.

- [ ] `[PRIV-BASE:P0.1][AI]` Verify PUB-IDEAS' merge pin and current private `origin/main`.
- [ ] `[PRIV-BASE:P0.2][AI]` Hash and record the authorized two-path overlay diff before switching.
- [ ] `[PRIV-BASE:P0.3][AI]` Prove private status contains only that overlay; do not stash it.
- [ ] `[PRIV-BASE:P0.4][AI]` Run `npm install` and plain `npm run doctor`; retain exit states.
- [ ] `[PRIV-BASE:P0.5][AI]` Run the private pre-push gate and retain its exit state.
- [ ] `[PRIV-BASE:P0.6][AI]` Re-hash that overlay diff; open only PRIV-REPAIR on baseline failure.
- [ ] `[PRIV-BASE:P0.G][AI]` Pass Phase 0 and record PRIV-IDEAS' exact predecessor and entry command.
- [ ] `[PRIV-BASE:P0.P][AI]` Record overlay fingerprint, result, predecessor, and recheck command.

### PRIV-REPAIR — Conditional Overlay-Safe Private Baseline Repair

Open this unit only for a reproduced private baseline failure outside the authorized overlay. Keep
the overlay byte-identical and keep PRIV-IDEAS frozen until the repair merges and baseline reruns.

- [ ] `[PRIV-REPAIR:P1.1][AI]` Name the failed command, first bad pin, root-cause owner, and slug.
- [ ] `[PRIV-REPAIR:P1.2][AI]` Enter the repair branch from private main without stashing the overlay.
- [ ] `[PRIV-REPAIR:P1.3][AI]` Publish exact paths, forecast, safety, rollback, and overlay fingerprint.
- [ ] `[PRIV-REPAIR:P1.4][AI]` Reproduce the failure before editing and retain the full diagnostic.
- [ ] `[PRIV-REPAIR:P1.5][AI]` Edit only proven repair paths and re-prove overlay byte identity.
- [ ] `[PRIV-REPAIR:P1.G][AI]` Pass the Phase 1 branch/base/pin/scope/ledger/overlay gate.
- [ ] `[PRIV-REPAIR:P1.P][AI]` Record head, ledger, overlay fingerprint, and reproduction command.
- [ ] `[PRIV-REPAIR:P2.1][AI]` Run the focused regression and original failing baseline command.
- [ ] `[PRIV-REPAIR:P2.2][AI]` Run applicable local gates and the private pre-push gate.
- [ ] `[PRIV-REPAIR:P2.3][AI]` Prove caps, staged-ledger equality, and overlay exclusion.
- [ ] `[PRIV-REPAIR:P2.4][AI]` Inspect cached names/check/stat/patch; commit one cohesive repair.
- [ ] `[PRIV-REPAIR:P2.5][AI]` Read the complete committed diff and re-hash the overlay.
- [ ] `[PRIV-REPAIR:P2.G][AI]` Pass the Phase 2 acceptance/staging/commit/overlay gate.
- [ ] `[PRIV-REPAIR:P2.P][AI]` Record local head, overlay fingerprint, and intended residue.
- [ ] `[PRIV-REPAIR:P3.1][AI]` Recompute caps, rerun pre-push, and push only the repair branch.
- [ ] `[PRIV-REPAIR:P3.2][AI]` Open one private-safe draft PR ending `Generated by AI`.
- [ ] `[PRIV-REPAIR:P3.3][AI]` Read back boundary/body/stats without exposing private content.
- [ ] `[PRIV-REPAIR:P3.G][AI]` Pass the Phase 3 exact-boundary and safe-entry-point gate.
- [ ] `[PRIV-REPAIR:P3.P][AI]` Record draft URL, current head, literal body, and overlay fingerprint.
- [ ] `[PRIV-REPAIR:P4.1][AI]` Post/read the exact-head route; run its bounded review cycle.
- [ ] `[PRIV-REPAIR:P4.2][AI]` Disposition findings natively; invoke firewall only if portable.
- [ ] `[PRIV-REPAIR:P4.3][AI]` Prove current-head CI/five preconditions and read back ready.
- [ ] `[PRIV-REPAIR:P4.G][AI]` Pass Phase 4 with semantic exit, green CI, and frozen scope.
- [ ] `[PRIV-REPAIR:P4.P][AI]` Record reviewed head, review/CI state, and overlay fingerprint.
- [ ] `[PRIV-REPAIR:P5.1][AI]` Recheck readiness and compute the reviewed patch fingerprint.
- [ ] `[PRIV-REPAIR:P5.2][AI]` Squash-merge by repository-qualified API; read landed diff.
- [ ] `[PRIV-REPAIR:P5.3][AI]` Match fingerprints; resync to the merge SHA without stashing.
- [ ] `[PRIV-REPAIR:P5.4][AI]` Rerun PRIV-BASE there; on success authorize only PRIV-IDEAS.
- [ ] `[PRIV-REPAIR:P5.G][AI]` Pass Phase 5 with merge, baseline, overlay, and successor proof.
- [ ] `[PRIV-REPAIR:P5.P][AI]` Record merge/main SHA, overlay fingerprint, and PRIV-IDEAS command.

### PRIV-IDEAS — Preserve the Overlay and Retire Its One Source

- [ ] `[PRIV-IDEAS:P1.1][AI]` Verify PRIV-BASE/REPAIR and the public obligation pin.
- [ ] `[PRIV-IDEAS:P1.2][AI]` Enter `optimize-pr-process-priv-ideas` without stashing.
- [ ] `[PRIV-IDEAS:P1.3][AI]` Prove the overlay is only the authorized deletion and index edit.
- [ ] `[PRIV-IDEAS:P1.4][AI]` Publish that ledger, forecast, dormant safety, risk, and rollback.
- [ ] `[PRIV-IDEAS:P1.5][AI]` Record propagation and generated bindings as reasoned `N/A`.
- [ ] `[PRIV-IDEAS:P1.6][AI]` Revalidate the private disposition against the public plan pin.
- [ ] `[PRIV-IDEAS:P1.7][AI]` Reconcile the existing overlay without rewriting its bytes.
- [ ] `[PRIV-IDEAS:P1.8][AI]` Reconcile `git status` exactly to the two-path ledger.
- [ ] `[PRIV-IDEAS:P1.G][AI]` Pass the Phase 1 pin/scope/size/ledger/overlay gate.
- [ ] `[PRIV-IDEAS:P1.P][AI]` Record branch, head, ledger, overlay fingerprint, and negative reads.
- [ ] `[PRIV-IDEAS:P2.1][AI]` Run predecessor/new-head IDEAS acceptance and retain safe outputs.
- [ ] `[PRIV-IDEAS:P2.2][AI]` Run private Markdown checks and the pre-push gate.
- [ ] `[PRIV-IDEAS:P2.3][AI]` Prove hand-authored caps and staged-ledger equality.
- [ ] `[PRIV-IDEAS:P2.4][AI]` Inspect cached names/check/stat/patch without exposing content.
- [ ] `[PRIV-IDEAS:P2.5][AI]` Commit the retirement; read full diff and re-hash overlay.
- [ ] `[PRIV-IDEAS:P2.G][AI]` Pass the Phase 2 acceptance/staging/commit gate.
- [ ] `[PRIV-IDEAS:P2.P][AI]` Record local head and clean tree or authorized residue.
- [ ] `[PRIV-IDEAS:P3.1][AI]` Recompute caps, rerun pre-push, and push only declared branch.
- [ ] `[PRIV-IDEAS:P3.2][AI]` Open one private-safe draft PR ending `Generated by AI`.
- [ ] `[PRIV-IDEAS:P3.3][AI]` Read back base/head/draft/body and safe PR statistics.
- [ ] `[PRIV-IDEAS:P3.G][AI]` Pass the Phase 3 boundary and private-safe entry-point gate.
- [ ] `[PRIV-IDEAS:P3.P][AI]` Record draft URL, current head, and literal body path.
- [ ] `[PRIV-IDEAS:P4.1][AI]` Post/read the exact-head route; run bounded review cycles.
- [ ] `[PRIV-IDEAS:P4.2][AI]` Disposition findings; invoke firewall only for a portable defect.
- [ ] `[PRIV-IDEAS:P4.3][AI]` Prove current-head CI/five preconditions and mark/read ready.
- [ ] `[PRIV-IDEAS:P4.G][AI]` Pass Phase 4 with semantic exit, green CI, and frozen scope.
- [ ] `[PRIV-IDEAS:P4.P][AI]` Record reviewed head, review/CI state, and obligation state.
- [ ] `[PRIV-IDEAS:P5.1][AI]` Recheck readiness and compute reviewed patch fingerprint.
- [ ] `[PRIV-IDEAS:P5.2][AI]` Squash-merge by repository-qualified API; read landed diff.
- [ ] `[PRIV-IDEAS:P5.3][AI]` Match fingerprints and record immutable private merge SHA.
- [ ] `[PRIV-IDEAS:P5.4][AI]` Close public obligation as `satisfied` and read it back.
- [ ] `[PRIV-IDEAS:P5.5][AI]` Resync private and authorize only PUB-A1 in public.
- [ ] `[PRIV-IDEAS:P5.G][AI]` Pass Phase 5 with merge, landed proof, resync, and sibling state.
- [ ] `[PRIV-IDEAS:P5.P][AI]` Record merge/main SHA, terminal obligation, and PUB-A1 command.

### PUB-CORR — Single Public Correction Adapter

This adapter activates only when private review proves a portable public defect. Freeze the private
PR at its recorded head and keep every later unit frozen. A second reversal stops for human help.

- [ ] `[PUB-CORR:P1.1][AI]` Link private evidence, paused head, public source line, and old public pin.
- [ ] `[PUB-CORR:P1.2][AI]` Prove `correction-count: 0`; reject local/private-only concerns.
- [ ] `[PUB-CORR:P1.3][AI]` Enter the single `correction-1` branch from public `origin/main`.
- [ ] `[PUB-CORR:P1.4][AI]` Publish exact public paths, forecast, safety, risk, and rollback.
- [ ] `[PUB-CORR:P1.5][AI]` Edit only the portable defect; keep private and downstream frozen.
- [ ] `[PUB-CORR:P1.G][AI]` Pass Phase 1 with scope, ledger, paused-head, and count proof.
- [ ] `[PUB-CORR:P1.P][AI]` Record branch/head/ledger, both pins, and private resume command.
- [ ] `[PUB-CORR:P2.1][AI]` Run affected acceptance, local gates, and public pre-push.
- [ ] `[PUB-CORR:P2.2][AI]` Prove caps and staged-ledger equality; inspect cached full patch.
- [ ] `[PUB-CORR:P2.3][AI]` Commit the cohesive correction and read its complete diff.
- [ ] `[PUB-CORR:P2.G][AI]` Pass the Phase 2 acceptance/staging/commit gate.
- [ ] `[PUB-CORR:P2.P][AI]` Record local head and clean tree or named intended residue.
- [ ] `[PUB-CORR:P3.1][AI]` Recompute caps, rerun pre-push, and push only correction branch.
- [ ] `[PUB-CORR:P3.2][AI]` Open/read one draft body linking both pins and paused private PR.
- [ ] `[PUB-CORR:P3.G][AI]` Pass Phase 3 exact-boundary/body/readback gate.
- [ ] `[PUB-CORR:P3.P][AI]` Record draft URL, current head, and literal body path.
- [ ] `[PUB-CORR:P4.1][AI]` Post/read route, run bounded review, and disposition every finding.
- [ ] `[PUB-CORR:P4.2][AI]` Prove current-head CI/five preconditions and mark/read ready.
- [ ] `[PUB-CORR:P4.G][AI]` Pass Phase 4 with semantic exit and private still frozen.
- [ ] `[PUB-CORR:P4.P][AI]` Record reviewed head, review/CI state, and supersession draft.
- [ ] `[PUB-CORR:P5.1][AI]` Recheck readiness and compute reviewed patch fingerprint.
- [ ] `[PUB-CORR:P5.2][AI]` Squash-merge by repository-qualified API; read landed diff.
- [ ] `[PUB-CORR:P5.3][AI]` Match fingerprints and supersede the old obligation with merge SHA.
- [ ] `[PUB-CORR:P5.4][AI]` Change count to one; resync public and retain all later freezes.
- [ ] `[PUB-CORR:P5.5][AI]` Resume private review from replacement pin, not its old evidence.
- [ ] `[PUB-CORR:P5.G][AI]` Pass Phase 5 with landed proof and replacement obligation.
- [ ] `[PUB-CORR:P5.P][AI]` Record new main/pin/count and exact private resume command.

### PLAN-AMEND — Sole Plan-Amendment Adapter

Any proven plan defect freezes its dependent unit. This adapter owns the only amendment route;
WAVES-A and WAVES-RULES may trigger it but may not copy or invent another amendment checklist.

- [ ] `[PLAN-AMEND:P1.1][AI]` Link the defective section/pin, evidence, frozen unit/head, and owner.
- [ ] `[PLAN-AMEND:P1.2][AI]` Prove the defect cannot be safely handled inside the active unit.
- [ ] `[PLAN-AMEND:P1.3][AI]` Enter the named amendment branch from public `origin/main`.
- [ ] `[PLAN-AMEND:P1.4][AI]` Publish plan-only paths, forecast, dormant safety, and rollback.
- [ ] `[PLAN-AMEND:P1.5][AI]` Edit only this plan and state exactly what the new text supersedes.
- [ ] `[PLAN-AMEND:P1.G][AI]` Pass Phase 1 with frozen-unit, pin, scope, and ledger proof.
- [ ] `[PLAN-AMEND:P1.P][AI]` Record branch/head/ledger, frozen state, and resume condition.
- [ ] `[PLAN-AMEND:P2.1][AI]` Run plan acceptance, formatting, Markdown, and pre-push gates.
- [ ] `[PLAN-AMEND:P2.2][AI]` Prove caps/staged-ledger equality and inspect cached full patch.
- [ ] `[PLAN-AMEND:P2.3][AI]` Commit one cohesive amendment and read its complete diff.
- [ ] `[PLAN-AMEND:P2.G][AI]` Pass the Phase 2 acceptance/staging/commit gate.
- [ ] `[PLAN-AMEND:P2.P][AI]` Record local head and clean tree or named intended residue.
- [ ] `[PLAN-AMEND:P3.1][AI]` Recompute caps, rerun pre-push, and push only amendment branch.
- [ ] `[PLAN-AMEND:P3.2][AI]` Open/read one draft body linking superseded pin and frozen unit.
- [ ] `[PLAN-AMEND:P3.G][AI]` Pass Phase 3 exact-boundary/body/readback gate.
- [ ] `[PLAN-AMEND:P3.P][AI]` Record draft URL, current head, and literal body path.
- [ ] `[PLAN-AMEND:P4.1][AI]` Post/read route, run bounded review, and disposition findings.
- [ ] `[PLAN-AMEND:P4.2][AI]` Prove current-head CI/five preconditions and mark/read ready.
- [ ] `[PLAN-AMEND:P4.G][AI]` Pass Phase 4 with semantic exit and dependent unit frozen.
- [ ] `[PLAN-AMEND:P4.P][AI]` Record reviewed head, review/CI state, and resume condition.
- [ ] `[PLAN-AMEND:P5.1][AI]` Recheck readiness and compute reviewed patch fingerprint.
- [ ] `[PLAN-AMEND:P5.2][AI]` Squash-merge by repository-qualified API; read landed diff.
- [ ] `[PLAN-AMEND:P5.3][AI]` Match fingerprints and record the amended plan merge SHA.
- [ ] `[PLAN-AMEND:P5.4][AI]` Resync this worktree; do not add rule/code changes.
- [ ] `[PLAN-AMEND:P5.5][AI]` Resume only the frozen unit from the amendment pin.
- [ ] `[PLAN-AMEND:P5.G][AI]` Pass Phase 5 with landed proof, resync, and one successor.
- [ ] `[PLAN-AMEND:P5.P][AI]` Record new main/amendment pin and exact resume command.

### WAVES-ENTRY Finding State

WAVES-ENTRY supplies F-035's task/evidence contract, idea units, two baselines and conditional
repairs, single-correction firewall adapter, and sole plan-amendment adapter. F-035 remains
partially open until WAVES-A and WAVES-RULES merge and the latter records all three immutable pins;
neither later slice may duplicate ENTRY-owned tasks.

## Dormant Lifecycle and Evidence-State Template

The lines below deliberately are not checkboxes. The three WAVES checklist slices must copy every
universal action and gate into separate tagged checkboxes per owned unit; conditional blocks copy
applicable actions or one reasoned `N/A` checkbox. EXECUTION-CLOSURE does the same for Phase 6.
After ACTIVATE, each active unit copies its Markdown IDs into the live task list 1:1.

For each unit, keep separate evidence states for local authoring/gates, pushed commit, PR current
head, current-head CI, review semantic exit, merge proof, landed-diff proof, worktree resync, and
sibling obligation. Completing one never implies another.

| Phase | Purpose                             | Gate                                                   | Pause-safe record                   |
| ----: | ----------------------------------- | ------------------------------------------------------ | ----------------------------------- |
|     0 | Repository-local baseline           | dependencies, doctor, and pre-push baseline pass       | no PR; evidence rides first unit    |
|     1 | Entry and bounded authoring         | pin, scope, size, ledger, ownership, and safety pass   | branch/head/ledger/next command     |
|     2 | Local gates, staging, and commit    | staged ledger equals admitted ledger; local gates pass | cohesive local head                 |
|     3 | Push and draft human-readable PR    | exact base/head/draft/body readback passes             | draft URL and current head          |
|     4 | Review, repair, and current-head CI | semantic exit and current-head CI pass                 | threads, cycle, and check state     |
|     5 | Merge, landed proof, and resync     | merge, landed-content, resync, and sibling state pass  | merged main and next branch command |
|     6 | Final evidence and cleanup          | EXECUTION-CLOSURE terminal proof passes                | public archive is durable record    |

## Dormant Phase 0 Template — Repository-Local Baseline

Run public baseline after ACTIVATE. Keep private quarantined until its own baseline immediately
before PRIV-IDEAS; record and preserve its authorized overlay. Phase 0 itself opens no PR.

- **Template `[AI]`:** Record `git status --short --branch`; preserve any authorized overlay.
- **Template `[AI]`:** Run `npm install`, `npm run doctor`, and
  `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`. Use
  `npm run doctor -- --fix` only for recorded remediation, then rerun plain doctor.
- **Template `[AI]`:** If a gate fails, record it and pause. Deliver a separate
  `optimize-pr-process-<repo>-baseline-repair-<slug>` through Phases 1–5, then rerun this baseline;
  never widen PUB-IDEAS. Record the first ordinary unit's exact predecessor pin.

### Phase 0 Gate

All commands pass, authorized dirty paths are named, Phase 0 itself created no PR, any repair PR is
merged and recorded, no ordinary-unit PR is open, and the first unit has an exact pin.

> **Pause Safety**: The repository, baseline result, predecessor, and Phase 1 entry command are recorded. Safe to stop. To re-verify: `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`.

## Dormant Phase 1 Template — Entry and Bounded Authoring

Each instantiated unit begins with these checks. If already on the declared branch, reuse it. If a
safe local branch exists, attach it; create only when absent. Stop on a different shared branch,
unexpected path, or base mismatch. Preserve and recheck the private overlay in every case.

```bash
git fetch origin main
git status --short --branch
git worktree list --porcelain
git branch --show-current
git show-ref --verify refs/heads/<declared-unit-branch>
git switch <declared-unit-branch> # existing safe branch; omit when already current
git switch -c <declared-unit-branch> origin/main # only when show-ref proves absent
test "$(git branch --show-current)" = "<declared-unit-branch>"
git rev-parse HEAD
git rev-parse origin/main
git merge-base --is-ancestor <predecessor-pin> origin/main
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Record repository, worktree, predecessor pin, current `origin/main`, owned hand-authored/generated
paths, projected changed lines/files, rollback, and the lightest stable-main safety choice. For
PRIV-IDEAS, prove the authorized overlay is unchanged before and after switching. Stop on a wrong
worktree, unexpected path, missing pin/ownership, stacked dependency, or forecast above 400 changed
hand-authored lines or 20 hand-authored files.

Every rule unit then performs these authoring steps:

- **Template `[AI]`:** Copy the merged dependency pin and exact source boundary from the
  [bounded delivery ledger](./tech-docs.md#bounded-delivery-ledger).
- **Template `[AI]`:** Run
  `repo-governance/workflows/repo/repo-rules-propagation.md` with `mode=strict`,
  `isolation=current`, and normalized rules; retain its placement manifest and sibling obligation.
- **Template `[AI]`:** Publish the before-ledger, edit only admitted source paths, then run
  `npm run generate:bindings` once. A discovered path forces a scope/size recheck.
- **Template `[AI]`:** Run `npm run validate:sync`, capture tracked source/generated content, rerun
  generation, and prove tracked bytes plus the file ledger are unchanged on the second run.
- **Template `[AI]`:** Reconcile the ledger to `git status --short`; record exact source/generated
  paths, parity result, and private obligation. Missing or unexplained state fails the unit.

### Phase 1 Gate

Branch/base/pin evidence is exact, scope is frozen, forecast is within bounds, and the before/after
ledger contains only owned paths.

> **Pause Safety**: Branch, head, ledger, and dirty state are recorded; no other unit has started. Safe to stop. To re-verify: `git status --short --branch`.

## Dormant Phase 2 Template — Verify, Stage, and Commit

- **Template `[AI]`:** Run unit acceptance and the pre-push gate. When applicable, also run
  `npx nx affected -t test:integration`, `npx nx affected -t test:e2e`, and named manual UI/API
  assertions. Record a reasoned `N/A`; never silently skip a gate.
- **Template `[AI]`:** Classify generated paths from repository ownership. Use
  `git diff --numstat <unit-base> -- <hand-authored-paths> | awk '{a+=$1; d+=$2} END {print a+d}'`
  for additions plus deletions and
  `git diff --name-only <unit-base> -- <hand-authored-paths> | wc -l` for files. Stop and split
  above 400 or 20; repeat before push. Keep these cap-counted statistics separate from PR totals.
- **Template `[AI]`:** Stage only explicit ledger paths with `git add -- <path>...`; run
  `git diff --cached --name-only`, `git diff --cached --check`, `git diff --cached --stat`, and
  `git diff --cached --patch`. Staged paths must equal the admitted ledger in both directions.
- **Template `[AI]`:** Split independent domains or commit types. Commit each cohesive concern with
  `git commit -m "<type>(<scope>): <imperative summary>"`; then read the full commit diff.

### Phase 2 Gate

Acceptance/local gates pass, actual size is within bounds, staged paths equal the ledger, commits
are cohesive, and the full diff was read.

> **Pause Safety**: The local head and clean tree or named intended residue are recorded. Safe to stop. To re-verify: `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`.

## Dormant Phase 3 Template — Push and Draft Human Entry Point

- **Template `[AI]`:** Recompute the hand-authored cap statistics and rerun the pre-push gate.
- **Template `[AI]`:** Push only the declared branch with
  `git push --set-upstream origin <branch>`; record the pushed commit.
- **Template `[AI]`:** Lead the body with outcome and why; then scope/non-goals with reasons, reading
  order and generated paths to skip, verification, focus, predecessor pin, risk, safety, rollback,
  and exact size. Use Mermaid plus prose only when it clarifies at least three relationships. End
  with `Generated by AI`.
- **Template `[AI]`:** Open one draft from that reviewed literal file:
  `gh pr create --repo <owner/repo> --draft --base main --head <branch> --title "<title>"
--body-file local-tmp/<unit>-pr-body.md`.
- **Template `[AI]`:** Run
  `gh pr view --repo <owner/repo> <pr> --json isDraft,baseRefOid,headRefOid,body,additions,deletions,changedFiles`.
  Verify base/head/draft/body and record whole-PR totals separately from the hand-authored cap set;
  compare only like-for-like claims.

### Phase 3 Gate

One draft PR exists at the declared boundary and its human entry point matches the diff.

> **Pause Safety**: The draft URL, current head, and literal body are recorded. Safe to stop. To re-verify: `gh pr view --repo <owner/repo> <pr> --json isDraft,baseRefOid,headRefOid,body,additions,deletions,changedFiles`.

## Dormant Phase 4 Template — Review, Repair, Firewall, and CI

- **Template `[AI]`:** For every AI-authored PR write—body, route, review, reply,
  sibling/correction record, or summary—use a reviewed literal payload when multiline, end with
  `Generated by AI`, and read back the stored artifact before its gate may pass.
- **Template `[AI]`:** Keep the PR draft and classify the complete current-head diff. Record
  `eligible` when any artifact can execute/change reachable behavior, when `plans/**` changes, or
  when evidence is ambiguous; record `noneligible` only for wholly non-executing prose/governance.
  Record the secret-exposure check on either route; suspicion stops normal review.
- **Template `[AI]`:** Post the review-route record with classification, exact base/head/statistics,
  plain risk, selected/skipped lenses with reasons, paths to skip, frozen scope, and changed probe.
  Link each settled prior thread or human dismissal and name its terminal reason.
- **Template `[AI]`:** On `noneligible`, skip specialist fan-out and fixing cycles. Prove the
  classifier from the full diff and require current-head `.github/workflows/pr-quality-gate.yml`.
- **Template `[AI]`:** On `eligible`, run one cycle at a time. Selected reviewers inspect the full
  current-head PR and repair delta; synthesis posts one consolidated native review with line
  findings. Each blocker teaches evidence, impact, bounded remedy, and safe refutation.
- **Template `[AI]`:** On `eligible`, independently disposition every finding as `fix`, `reject-with-reason`,
  `defer-with-reason`, or `clarify`. Link fixes to a pushed commit; cite contrary evidence for a
  rejection and a real follow-up for a deferral. Reply in the same thread, read back the reply, and
  resolve only when its evidence is true.
- **Template `[AI]`:** After each push, discard prior-head CI evidence. Poll
  `gh pr checks --repo <owner/repo> <pr>` exactly every 120 seconds; never use `gh run watch`.
  Require `pr-quality-gate.yml`, `validate-env`, applicable jobs, and the aggregate gate. On failure,
  inspect `gh run view <run-id> --log-failed`, repair root cause, push, and restart current-head proof.
- **Template `[AI]`:** On `eligible`, target Cycles 1–3: Cycle 1 checks the whole promised outcome; later cycles
  refute repairs and vary the probe. Cycles 4–5 are recovery only: name the remaining defect family
  and failed reasoning method, then use a genuinely different probe. Stop before Cycle 6 and ask a
  human only if still unsafe. No routine human checkpoint before then and no extra clean cycle.
- **Template `[AI]`:** Before readiness, surface all five preconditions: route-specific completion;
  zero unresolved CRITICAL/HIGH/MEDIUM findings; branch current with `origin/main`; green applicable
  local/current-head CI; and resolved surface-tester findings—or explicit no-reachable-behavior
  evidence. Then run `gh pr ready --repo <owner/repo> <pr>` and read back `isDraft: false`. This
  five-cycle eligible-route authority applies after ACTIVATE until durable A2/B rules supersede it.

### Cross-Repository Correction Firewall

Only one public/private pair is active; every later unit is frozen. Before a public wave merges, its
PR records a pending sibling obligation with wave, public URL, reviewed head, rule class, expected
private paths, byte-identity class, `correction-count: 0`, successor, and one accountable owner.

Private review classifies each concern as local adaptation, private deviation, unrelated follow-up,
or portable defect, using the glossary above. Only the last may request upstream correction, citing
the public line, private evidence, and why local adaptation would be wrong. Freeze the private PR:
it may remain open, but receives no push, review cycle, readiness transition, or merge.

At most one fresh, unstacked `optimize-pr-process-pub-<wave>-correction-1` PR may merge. Its native
record links both public pins/heads and the paused private PR/head, supersedes the old obligation,
and changes `correction-count: 0 → 1`; private review restarts from the correction pin. A second
portable-source reversal stops before another correction and asks a human. Downstream remains
frozen until the obligation is `satisfied`, `reasoned-deviation`, or `N/A`. “In sync” means semantic
correspondence with explicit deviations; byte identity applies only to an existing contract.

### Phase 4 Gate

Eligible semantic exit holds within five cycles, or noneligible classifier evidence plus its gate
passes. Every artifact is read back, all five readiness preconditions pass, no correction loop or
unresolved thread remains, scope is frozen, and readiness is true.

> **Pause Safety**: Reviewed head, cycle/thread/CI state, and sibling state are recorded. Safe to
> stop. To re-verify: `gh pr view --repo <owner/repo> <pr> --json isDraft,headRefOid,mergeStateStatus,statusCheckRollup`.

## Dormant Phase 5 Template — Merge, Prove Landed Content, and Resync

- **Template `[AI]`:** Recheck route completeness, zero unresolved CRITICAL/HIGH/MEDIUM findings,
  zero unresolved threads, branch currency with `origin/main`, green local/current-head CI, and any
  applicable surface-test findings. A failed precondition returns to Phase 4.
- **Template `[AI]`:** Use a patch fingerprint because a squash merge changes commit ancestry. Run
  the repository-qualified API-side merge and keep local cleanup separate:

  ```bash
  git diff --binary <current-main> <reviewed-head> | git patch-id --stable
  gh pr merge --repo <owner/repo> <pr> --squash
  gh pr view --repo <owner/repo> <pr> --json headRefOid,mergeCommit,mergedAt,state
  git fetch origin main
  git show --first-parent --format=fuller --patch <merge-sha>
  git diff --binary <merge-sha>^1 <merge-sha> | git patch-id --stable
  git status --short --branch
  ```

  Read the full landed diff and compare fingerprints exactly. Stop on inequality. Verify remote
  branch state before optional deletion; a merge must not trigger an implicit checkout of `main`.

- **Template `[AI]`:** Update and read back the sibling obligation with merge SHA, reviewed head,
  landed fingerprint, and `pending`, `satisfied`, `reasoned-deviation`, or `N/A`. In this same
  worktree, use the Phase 1 safe-existing/absent decision for the next unstacked branch, then prove:

  ```bash
  git branch --list <next-branch>
  git switch <next-branch> # existing safe branch; omit when absent
  git switch -c <next-branch> origin/main # only when absent
  test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
  ```

  Never reset or force-push to imitate resync. For the final unit, record a reasoned `N/A` instead
  of inventing a successor.

### Phase 5 Gate

The PR is merged, landed diff and fingerprint match, `origin/main` contains the merge, the worktree
is resynced, and the sibling obligation has one owner, state, and immutable pin.

> **Pause Safety**: Merge/new-main SHA, sibling state, and next branch are recorded. Safe to stop.
> To re-verify: `git status --short --branch`.

## Dormant Common Failure Rules

- Fix every red gate at root cause. If a required pre-existing repair would exceed ownership or
  size, pause and deliver a separate bounded repair PR; never waive or silently absorb it.
- Never reset, force-push shared history, auto-stash an overlay, bypass a gate, dismiss a finding to
  manufacture exit, or treat a comment as authority to expand scope.
- A plan defect freezes dependent work. Create
  `optimize-pr-process-plan-amendment-<slug>` from current `origin/main` in this public worktree.
  Its plan-only PR links the exact section/pin it supersedes and frozen unit, then runs Phases 1–5.
  Resume only from its merge pin; rule or code changes never ride inside `PLAN-AMENDMENT`.

## Cross-Repository Order (Dormant)

After activation, PUB-IDEAS merges before PRIV-IDEAS. Later implementation remains sequential:
`PUB-A1 → PRIV-A1 → PUB-A2 → PRIV-A2 → PUB-A3 → PRIV-A3 → PUB-B → PRIV-B → PUB-C? → PRIV-C? →
closure`; C stays a no-change decision unless necessity passes. Public pins and native sibling
obligations keep the repositories semantically “in sync”; private-only deviations stay private.

CORE-ENTRY, CORE-REVIEW, WAVES-ENTRY, WAVES-A, WAVES-RULES, and EXECUTION-CLOSURE must turn this order into a 1:1
runnable checklist and preserve every merge step and its authority. No assembly PR may begin
implementation.

## Dormant Authority Mapping

This mapping replaces the two historical shortcut checkboxes; it is not executable work.
The three WAVES checklist slices must instantiate each applicable Phase 4–5 action and gate per owned unit,
and EXECUTION-CLOSURE must prove the terminal state without adding a shorter merge route.

| Authority        | Sole owner after ACTIVATE                                          |
| ---------------- | ------------------------------------------------------------------ |
| Review/readiness | Phase 4 checkboxes instantiated per unit by its owning WAVES slice |
| Merge/resync     | Phase 5 checkboxes instantiated per unit by its owning WAVES slice |
| Final proof      | Phase 6 checkboxes instantiated by EXECUTION-CLOSURE               |
| Assembly order   | PLAN merges/resyncs before separate PUB-IDEAS and PRIV-IDEAS PRs   |

[worktree-spec]: ../../../repo-governance/conventions/structure/plans/worktree-specification.md
[worktree-cap]: ../../../repo-governance/conventions/structure/plans/worktree-cap.md
[worktree-path]: ../../../repo-governance/conventions/structure/worktree-path.md
