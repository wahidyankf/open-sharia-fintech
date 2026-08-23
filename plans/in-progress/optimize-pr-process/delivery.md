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
| [Repo-grounded] Closed [PR #258](https://github.com/wahidyankf/ose-public/pull/258) | Incomplete WAVES-ENTRY draft; never merged                   |
| [Repo-grounded] Merged [PR #259](https://github.com/wahidyankf/ose-public/pull/259) | ENTRY split at `e205eca335d62618a206d5c85ebc8e8cdc4fa66e`    |
| [Repo-grounded] Merged [PR #260](https://github.com/wahidyankf/ose-public/pull/260) | BASE split at `5c61907d9d24718267dae8a2307e3578df1d18c9`     |
| [Repo-grounded] WAVES-ENTRY-PUBLIC                                                  | Active: author public baseline, repair, and ideas checklist  |
| [Unverified] Complete assembled plan                                                | Fresh formal gate and grill still precede activation         |

> **AUTHORING-ONLY UNTIL ACTIVATE:** WAVES-ENTRY-PUBLIC changes plan docs only; it runs no gate or implementation.

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

Plan assembly is deliberately **dormant and non-executable**. WAVES-ENTRY-PUBLIC may change only this
plan's `README.md`, `delivery.md`, and `learnings.md`. ENTRY-PRIVATE, ENTRY-ADAPTERS, WAVES-A,
WAVES-RULES, EXECUTION-CLOSURE, ideas, indexes, rules, agents, bindings, workflows, code, tests,
implementation, and active-plan indexes remain dormant. The formal gate waits for assembly.

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
CORE-SPLIT-FORECAST → CORE-ENTRY → CORE-REVIEW → WAVES-SPLIT → WAVES-ENTRY-SPLIT →
WAVES-ENTRY-BASE-SPLIT → WAVES-ENTRY-PUBLIC → WAVES-ENTRY-PRIVATE → WAVES-ENTRY-ADAPTERS →
WAVES-A → WAVES-RULES → EXECUTION-CLOSURE → ACTIVATE/formal-gate/grill → PUB-IDEAS →
PRIV-IDEAS → implementation waves
```

Each arrow is a separate, unstacked PR from then-current `origin/main`, using the same owned public
worktree. Every assembly slice is at most 400 changed hand-authored lines and 20 hand-authored files.
Forecast each slice before opening it; if any would exceed a bound, record its named cohesive
sub-slices in the prior PR before opening the first split. Gate findings use bounded
`ACTIVATE-REPAIR-*` PRs. Final ACTIVATE contains only the clean formal gate, post-write grill, and
executable-status change. Merge green and resync before the next PR.

| Slice                  | Contract and audit IDs restored before activation                                                                                       | Target changed lines |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------: |
| CORE-ENTRY             | Complete Phase 0–5 gate/pause-safe spine and state model, plus Phase 0–3 mechanics; F-005–F-011, F-014–F-016, F-025, F-026, F-028–F-030 |              230–300 |
| CORE-REVIEW            | Review route, CI, correction firewall, merge and amendment; F-012, F-017, F-031, F-032, F-034                                           |              150–230 |
| WAVES-SPLIT            | Forecast repair after the original EXECUTION-WAVES draft exceeded the hard cap                                                          |               70–125 |
| WAVES-ENTRY-SPLIT      | Forecast repair after PR #258 proved atomic ENTRY work exceeds its range ceiling                                                        |              100–180 |
| WAVES-ENTRY-BASE-SPLIT | Forecast repair after the complete BASE probe crossed its forecast and hard cap                                                         |              120–180 |
| WAVES-ENTRY-PUBLIC     | Continuing rules; literal acceptance; public baseline/repair/ideas; F-035 partial                                                       |              200–260 |
| WAVES-ENTRY-PRIVATE    | Private overlay-safe baseline/repair/ideas; F-035 BASE pair pin                                                                         |              170–230 |
| WAVES-ENTRY-ADAPTERS   | Single correction and sole PLAN-AMEND adapters; F-035 ENTRY terminal                                                                    |              100–155 |
| WAVES-A                | PUB/PRIV A1–A2 checklists, acceptance, pair gates, and prior-pair reconciliation; F-035 A partial                                       |              190–250 |
| WAVES-RULES            | PUB/PRIV A3 and B; optional-C decision/trigger; pair gates and prior-pair reconciliation; F-035 terminal owner                          |              200–270 |
| EXECUTION-CLOSURE      | Reconciliation/dogfood, knowledge, private terminal proof, public archival, cleanup; F-013, F-018, F-036–F-037                          |              220–300 |
| ACTIVATE               | Clean formal plan-quality gate, post-write grill, and explicit executable-status change                                                 |          at most 400 |

Closed PR #258 measured 302 changed lines before its six findings. The first complete repair model
expanded that draft by 106 lines to 408, but a BASE-only authoring probe then measured 401 changed
lines and 276 checkboxes: the model under-counted repeated per-unit review, CI, readiness, merge,
resync, and three-state overlay work. Splitting that measured draft repeats 12 status/ownership
lines: 413 total across PUBLIC and PRIVATE.

Here, an invariant is an always-on evidence rule, literal acceptance gives the exact command and
expected result, and state-specific overlay proof hashes unstaged, staged, and committed changes
separately. Scaffolding is the status, owner, and acceptance text repeated so each PR stands alone.

| PR #258 Cycle 1 finding                                                                                                   | Local repair owner                                 | Required repair                                                                                    | Terminal proof                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [Compound Git/GitHub transitions](https://github.com/wahidyankf/ose-public/pull/258#discussion_r3838415346)               | PUBLIC, PRIVATE, then ADAPTERS for their own units | Separate calculate/gate/push, route/read/review, ready, merge/landed-proof, and resync actions     | ADAPTERS records all three merged ENTRY pins and verifies every local checklist before F-035 advances |
| [Continuing ENTRY rules used as tasks](https://github.com/wahidyankf/ose-public/pull/258#discussion_r3838415349)          | PUBLIC                                             | Keep always-on rules as prose enforced by each unit gate; check only finishable owned actions      | PUBLIC merged pin plus its unit-gate evidence                                                         |
| [Ambiguous idea acceptance](https://github.com/wahidyankf/ose-public/pull/258#discussion_r3838415350)                     | PUBLIC                                             | Give literal predecessor/reviewed-head commands, expected results, and the post-push rerun         | PUBLIC merged pin plus command/output evidence                                                        |
| [Worktree may not be on current main](https://github.com/wahidyankf/ose-public/pull/258#discussion_r3838415351)           | PUBLIC for public; PRIVATE for private             | Separate fetch, safe detach, `HEAD == origin/main`, status, and private before/after overlay proof | PRIVATE merged pin verifies both repository-local checklists                                          |
| [One fingerprint cannot cover three Git states](https://github.com/wahidyankf/ose-public/pull/258#discussion_r3838415352) | PRIVATE                                            | Compare unstaged, staged, and `<unit-base>..HEAD` fingerprints at their real states                | PRIVATE merged pin plus three-state equality evidence                                                 |
| [Stale assembly state](https://github.com/wahidyankf/ose-public/pull/258#pullrequestreview-5002302877)                    | WAVES-ENTRY-SPLIT                                  | Record PR #257 as merged, PR #258 as closed unmerged, and successor slices                         | PR #259 merge pin                                                                                     |

The ledger is lossless: a row closes only at its terminal proof. Closing PR #258 removes its unsafe
draft from the delivery path but does not itself close any repair row.

PR #259 added one later dogfood lesson. WAVES-ENTRY-BASE-SPLIT owns aligning the shared Phase 5
template on raw input; ENTRY-PUBLIC owns copying that exact command into its continuing rules and
public-unit tasks. The lesson closes only at PUBLIC's merged pin after its checklist and the shared
template use the same `/usr/bin/git diff --binary ... | /usr/bin/shasum -a 256` procedure.

| Complete-preview component           | ENTRY-PUBLIC | ENTRY-PRIVATE | ENTRY-ADAPTERS | WAVES-A | WAVES-RULES |
| ------------------------------------ | -----------: | ------------: | -------------: | ------: | ----------: |
| Shared rules and literal acceptance  |           52 |             0 |             18 |      18 |          18 |
| Repository-local units               |          145 |           160 |             72 |     160 |         176 |
| Status, ownership, and F-035 proof   |           28 |            28 |             28 |      30 |          34 |
| **Forecast complete-preview total**  |      **225** |       **188** |        **118** | **208** |     **228** |
| **Repair headroom to range ceiling** |       **35** |        **42** |         **37** |  **42** |      **42** |

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

- WAVES-ENTRY-PUBLIC authors continuing rules, literal acceptance, and public baseline/repair/idea
  units. WAVES-ENTRY-PRIVATE authors the private overlay-safe counterparts. ENTRY-ADAPTERS owns the
  single public correction and sole reusable `PLAN-AMENDMENT` adapter. WAVES-A owns A1–A2;
  WAVES-RULES owns A3/B/C, and a positive C decision triggers only the ADAPTERS route. F-035 closes
  only after all three ENTRY pins and the A and RULES pins exist.
- EXECUTION-CLOSURE authors the later checklist for reconciling the plan with what landed, dogfooding the
  process—using it on its own PRs—capturing knowledge, closing private work, archiving the public
  plan, and safely removing worktrees.
- ACTIVATE runs the formal plan-quality gate and a structured post-write user review (the “grill”)
  before changing the assembled plan from dormant to executable.

Both CORE slices, all three WAVES forecast repairs, all three ENTRY checklist slices, WAVES-A,
WAVES-RULES, and EXECUTION-CLOSURE author only plan text or checklists; none executes before ACTIVATE.

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
The five WAVES checklist slices supply exact unit scope/acceptance; EXECUTION-CLOSURE supplies Phase 6.

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

FOUNDATION through WAVES-ENTRY-BASE-SPLIT are merged; WAVES-ENTRY-PUBLIC is active. ACTIVATE may open
only after PUBLIC, PRIVATE, ADAPTERS, WAVES-A, WAVES-RULES, and EXECUTION-CLOSURE instantiate every
delivery unit as granular, attributable checkboxes and every finding is fixed. A fresh formal gate
and grill must then pass; historic evidence cannot substitute.

## Dormant Execution-Wave Public Entry Checklist

Every checkbox below is inert until ACTIVATE merges. It describes later work; this assembly PR does
not run a baseline command, edit an idea, touch the private overlay, change a rule, or open an
implementation PR. After activation, copy only the active unit's unchecked IDs into the live task
list 1:1. Keep this Markdown as the durable evidence index and allow only one active unit at a time.

### Continuing Evidence Rules

These are always-on rules, not finish-once tasks. Every active unit's phase gate enforces them:

- One Markdown ID maps to one live task and one accountable executor; record repository, worktree,
  branch, predecessor pin, and current-main pin without combining transitions.
- Publish the exact admitted source/generated path ledger, size forecast, stability choice, risk,
  and rollback before editing; keep later units frozen and name exactly one successor.
- Link every completion to the command or observation, expected result, and actual result. A reasoned
  `N/A` names its artifact owner, evidence, reason, and remaining action.
- Keep authoring, local gates, staging, commit, push, PR readback, review, CI, readiness, merge,
  landed-content proof, resync, and sibling state independently observable.
- Hash raw patch bytes with `/usr/bin/git diff --binary ... | /usr/bin/shasum -a 256`; output compactors
  are for human reading and must never feed a content fingerprint.
- Read back every AI-authored GitHub artifact and its `Generated by AI` marker. Reconcile live tasks,
  Markdown IDs, file ledger, and `git status` at every gate.
- Stop on a missing pin, unexpected path, unresolved obligation, failed gate, or fingerprint mismatch.
  Record the exact pause-safe state before switching activities; use a separate bounded repair or
  amendment instead of widening the active unit.

### Literal Idea-Retirement Acceptance

For every row owned by PUB-IDEAS or PRIV-IDEAS, substitute the exact `<unit-base>`, the full mapped
`<brief>` path, and `<index-link>` as `./` plus `<brief>` relative to `plans/ideas/`. Retain command,
pin, exit status, and output. These commands distinguish absence from an unreadable or missing index:

```bash
/usr/bin/git cat-file -e "<unit-base>:<brief>" # predecessor: exit 0
/usr/bin/git grep -n -F -- "<index-link>" "<unit-base>" -- plans/ideas/README.md # exit 0, one line
test ! -e "<brief>" # reviewed worktree: exit 0
test -f plans/ideas/README.md # reviewed worktree: exit 0
set +e
rg -n -F -- "<index-link>" plans/ideas/README.md # expected exit 1 and no output
idea_index_exit=$?
set -e
test "$idea_index_exit" -eq 1
```

Run the predecessor pair before editing and the reviewed-worktree set after deletion, after commit,
and again after pushing and reading back the PR head. A predecessor exit other than 0, more or fewer
than one index line, reviewed `rg` exit other than 1, or unexpected output blocks the unit. Private
evidence stays local; its PR records only safe counts, hashes, paths already authorized for disclosure,
and pass/fail states.

### PUB-BASE — Public Repository Baseline

- [ ] `[PUB-BASE:P0.01][AI]` Verify ACTIVATE's exact merge pin is an ancestor of public `origin/main`.
- [ ] `[PUB-BASE:P0.02][AI]` Fetch public `origin/main` without advancing a checked-out local branch.
- [ ] `[PUB-BASE:P0.03][AI]` Record the public worktree and prove its status is clean or fully explained.
- [ ] `[PUB-BASE:P0.04][AI]` Safely detach this worktree at fetched public `origin/main`.
- [ ] `[PUB-BASE:P0.05][AI]` Prove `HEAD == origin/main` and record both immutable SHAs.
- [ ] `[PUB-BASE:P0.06][AI]` Run `npm install`; retain its exact exit state.
- [ ] `[PUB-BASE:P0.07][AI]` Run plain `npm run doctor`; retain its exact exit state.
- [ ] `[PUB-BASE:P0.08][AI]` Run the repository pre-push surface; retain its exact exit state.
- [ ] `[PUB-BASE:P0.09][AI]` Classify each failure as pre-existing baseline or ordinary-unit scope.
- [ ] `[PUB-BASE:P0.10][AI]` Authorize only PUB-REPAIR on baseline failure; otherwise record its reasoned `N/A`.
- [ ] `[PUB-BASE:P0.G][AI]` Pass the no-PR/current-main/status/dependency/doctor/pre-push gate.
- [ ] `[PUB-BASE:P0.P][AI]` Record result, predecessor pin, authorized successor, and recheck command.

### PUB-REPAIR — Conditional Public Baseline Repair

Open this unit only for a reproduced pre-existing public baseline failure unrelated to PUB-IDEAS.
Otherwise record the unit `N/A` at PUB-BASE and repair an ordinary unit only inside its own scope.

- [ ] `[PUB-REPAIR:P1.01][AI]` Name the failed command and retain its complete baseline evidence.
- [ ] `[PUB-REPAIR:P1.02][AI]` Identify the first bad pin, root-cause owner, and bounded branch slug.
- [ ] `[PUB-REPAIR:P1.03][AI]` Fetch current public `origin/main` and record its SHA.
- [ ] `[PUB-REPAIR:P1.04][AI]` Create or reuse only the declared repair branch from that exact SHA.
- [ ] `[PUB-REPAIR:P1.05][AI]` Prove repair `HEAD == origin/main` before the first edit.
- [ ] `[PUB-REPAIR:P1.06][AI]` Publish the exact admitted repair path ledger.
- [ ] `[PUB-REPAIR:P1.07][AI]` Publish line/file forecast, stable-main safety, risk, and rollback.
- [ ] `[PUB-REPAIR:P1.08][AI]` Reproduce the original failure before editing; retain the diagnostic.
- [ ] `[PUB-REPAIR:P1.09][AI]` Edit only proven repair paths while PUB-IDEAS stays frozen.
- [ ] `[PUB-REPAIR:P1.G][AI]` Pass the branch/base/pin/scope/ledger/forecast gate.
- [ ] `[PUB-REPAIR:P1.P][AI]` Record branch, head, ledger, dirty state, and reproduction command.
- [ ] `[PUB-REPAIR:P2.01][AI]` Run the focused regression; retain expected and actual results.
- [ ] `[PUB-REPAIR:P2.02][AI]` Rerun the original failing baseline command; require success.
- [ ] `[PUB-REPAIR:P2.03][AI]` Run every applicable local gate; retain each exit state.
- [ ] `[PUB-REPAIR:P2.04][AI]` Run the public pre-push surface; retain its exit state.
- [ ] `[PUB-REPAIR:P2.05][AI]` Calculate actual hand-authored changed lines and files.
- [ ] `[PUB-REPAIR:P2.06][AI]` Gate both actual counts against the plan's caps before staging.
- [ ] `[PUB-REPAIR:P2.07][AI]` Reconcile working-tree paths exactly to the admitted ledger.
- [ ] `[PUB-REPAIR:P2.08][AI]` Stage only the admitted repair ledger.
- [ ] `[PUB-REPAIR:P2.09][AI]` Read back cached path names and prove staged-ledger equality.
- [ ] `[PUB-REPAIR:P2.10][AI]` Inspect cached check, statistics, and complete patch.
- [ ] `[PUB-REPAIR:P2.11][AI]` Commit one cohesive repair.
- [ ] `[PUB-REPAIR:P2.12][AI]` Read the complete committed diff and verify no hidden path.
- [ ] `[PUB-REPAIR:P2.G][AI]` Pass the acceptance/size/staging/commit gate.
- [ ] `[PUB-REPAIR:P2.P][AI]` Record local head and clean tree or named intended residue.
- [ ] `[PUB-REPAIR:P3.01][AI]` Recalculate committed hand-authored line/file counts.
- [ ] `[PUB-REPAIR:P3.02][AI]` Gate the committed counts against both caps.
- [ ] `[PUB-REPAIR:P3.03][AI]` Rerun the public pre-push surface on the committed head.
- [ ] `[PUB-REPAIR:P3.04][AI]` Push only the declared repair branch.
- [ ] `[PUB-REPAIR:P3.05][AI]` Open one draft human-readable repair PR from a literal body file.
- [ ] `[PUB-REPAIR:P3.06][AI]` Read back base, head, draft state, body, and AI marker.
- [ ] `[PUB-REPAIR:P3.07][AI]` Read back whole-PR additions, deletions, files, and admitted paths.
- [ ] `[PUB-REPAIR:P3.G][AI]` Pass the pushed-boundary/body/readback gate.
- [ ] `[PUB-REPAIR:P3.P][AI]` Record draft URL, current head, and literal body path.
- [ ] `[PUB-REPAIR:P4.01][AI]` Post the exact-head risk route and selected/skipped review lenses.
- [ ] `[PUB-REPAIR:P4.02][AI]` Read back the route, frozen scope, changed probe, and AI marker.
- [ ] `[PUB-REPAIR:P4.03][AI]` Run one bounded review cycle on the exact current head.
- [ ] `[PUB-REPAIR:P4.04][AI]` Record every finding as fix, reject, defer, or clarify with evidence.
- [ ] `[PUB-REPAIR:P4.05][AI]` Push each bounded fix before claiming it in the native thread.
- [ ] `[PUB-REPAIR:P4.06][AI]` Reply in the same thread and read back the persisted reply.
- [ ] `[PUB-REPAIR:P4.07][AI]` Resolve only threads whose terminal evidence is true.
- [ ] `[PUB-REPAIR:P4.08][AI]` Poll applicable current-head CI exactly every 120 seconds until terminal.
- [ ] `[PUB-REPAIR:P4.09][AI]` Prove the five readiness preconditions on one current head.
- [ ] `[PUB-REPAIR:P4.10][AI]` Mark the PR ready only after semantic exit.
- [ ] `[PUB-REPAIR:P4.11][AI]` Read back ready state, current head, merge state, and green CI.
- [ ] `[PUB-REPAIR:P4.G][AI]` Pass semantic-exit/current-head-CI/frozen-scope readiness gate.
- [ ] `[PUB-REPAIR:P4.P][AI]` Record reviewed head, cycles, threads, CI, and sibling `N/A`.
- [ ] `[PUB-REPAIR:P5.01][AI]` Recheck route completion and zero unresolved blocker findings.
- [ ] `[PUB-REPAIR:P5.02][AI]` Recheck current base, reviewed head, ready state, and green CI.
- [ ] `[PUB-REPAIR:P5.03][AI]` Run `/usr/bin/git diff --binary <current-main> <reviewed-head> | /usr/bin/shasum -a 256`.
- [ ] `[PUB-REPAIR:P5.04][AI]` Squash-merge by repository-qualified GitHub API.
- [ ] `[PUB-REPAIR:P5.05][AI]` Read back the immutable merge SHA and landed path ledger.
- [ ] `[PUB-REPAIR:P5.06][AI]` Run `/usr/bin/git diff --binary <merge-sha>^1 <merge-sha> | /usr/bin/shasum -a 256`.
- [ ] `[PUB-REPAIR:P5.07][AI]` Prove reviewed and landed fingerprints are equal.
- [ ] `[PUB-REPAIR:P5.08][AI]` Fetch public `origin/main` after the merge.
- [ ] `[PUB-REPAIR:P5.09][AI]` Prove fetched `origin/main` equals the merge SHA.
- [ ] `[PUB-REPAIR:P5.10][AI]` Resync this same worktree to the merge SHA without switching worktrees.
- [ ] `[PUB-REPAIR:P5.11][AI]` Rerun PUB-BASE on the landed main pin.
- [ ] `[PUB-REPAIR:P5.12][AI]` Authorize only PUB-IDEAS after the rerun passes.
- [ ] `[PUB-REPAIR:P5.G][AI]` Pass merge/landed/fingerprint/resync/baseline/successor gate.
- [ ] `[PUB-REPAIR:P5.P][AI]` Record merge/main SHA, baseline result, and PUB-IDEAS entry command.

### PUB-IDEAS — Retire the 19 Public Sources

- [ ] `[PUB-IDEAS:P1.01][AI]` Verify PUB-BASE or PUB-REPAIR terminal proof and its exact pin.
- [ ] `[PUB-IDEAS:P1.02][AI]` Fetch public `origin/main` and prove it equals that predecessor.
- [ ] `[PUB-IDEAS:P1.03][AI]` Enter `optimize-pr-process-pub-ideas` from the exact main pin.
- [ ] `[PUB-IDEAS:P1.04][AI]` Publish the exact 19-brief plus public-index path ledger.
- [ ] `[PUB-IDEAS:P1.05][AI]` Record forecast, static-doc safety, risk, and rollback-by-revert.
- [ ] `[PUB-IDEAS:P1.06][AI]` Record propagation and generated bindings as reasoned `N/A`.
- [ ] `[PUB-IDEAS:P1.07][AI]` Revalidate all 19 dispositions against the activated plan pin.
- [ ] `[PUB-IDEAS:P1.08][AI]` Run literal predecessor acceptance for every mapped public row.
- [ ] `[PUB-IDEAS:P1.09][AI]` Delete only the 19 mapped public briefs.
- [ ] `[PUB-IDEAS:P1.10][AI]` Remove only their exact links from `plans/ideas/README.md`.
- [ ] `[PUB-IDEAS:P1.11][AI]` Run reviewed-worktree acceptance for every mapped public row.
- [ ] `[PUB-IDEAS:P1.12][AI]` Reconcile `git status` exactly to the retirement ledger.
- [ ] `[PUB-IDEAS:P1.G][AI]` Pass pin/scope/size/ledger/disposition/acceptance gate.
- [ ] `[PUB-IDEAS:P1.P][AI]` Record branch, head, ledger, dirty state, and negative-read commands.
- [ ] `[PUB-IDEAS:P2.01][AI]` Rerun all reviewed-worktree acceptance commands before staging.
- [ ] `[PUB-IDEAS:P2.02][AI]` Run Markdown formatting and lint checks.
- [ ] `[PUB-IDEAS:P2.03][AI]` Run the public pre-push surface.
- [ ] `[PUB-IDEAS:P2.04][AI]` Calculate and gate actual hand-authored line/file counts.
- [ ] `[PUB-IDEAS:P2.05][AI]` Stage only the admitted retirement ledger.
- [ ] `[PUB-IDEAS:P2.06][AI]` Read cached paths and prove staged-ledger equality.
- [ ] `[PUB-IDEAS:P2.07][AI]` Inspect cached check, statistics, and complete patch.
- [ ] `[PUB-IDEAS:P2.08][AI]` Commit the cohesive public retirement.
- [ ] `[PUB-IDEAS:P2.09][AI]` Read the complete committed diff.
- [ ] `[PUB-IDEAS:P2.10][AI]` Rerun all reviewed-head acceptance commands after commit.
- [ ] `[PUB-IDEAS:P2.G][AI]` Pass acceptance/formatting/gates/size/staging/commit gate.
- [ ] `[PUB-IDEAS:P2.P][AI]` Record local head and clean tree or named intended residue.
- [ ] `[PUB-IDEAS:P3.01][AI]` Recalculate and gate committed hand-authored counts.
- [ ] `[PUB-IDEAS:P3.02][AI]` Rerun the public pre-push surface on the committed head.
- [ ] `[PUB-IDEAS:P3.03][AI]` Push only `optimize-pr-process-pub-ideas`.
- [ ] `[PUB-IDEAS:P3.04][AI]` Read back the remote branch head and prove it equals local `HEAD`.
- [ ] `[PUB-IDEAS:P3.05][AI]` Rerun all reviewed-head acceptance commands after push.
- [ ] `[PUB-IDEAS:P3.06][AI]` Open one draft human-readable PR from a literal AI-marked body.
- [ ] `[PUB-IDEAS:P3.07][AI]` Read back base, head, draft state, body, marker, and statistics.
- [ ] `[PUB-IDEAS:P3.G][AI]` Pass push/remote-head/acceptance/body/readback gate.
- [ ] `[PUB-IDEAS:P3.P][AI]` Record draft URL, current head, and literal body path.
- [ ] `[PUB-IDEAS:P4.01][AI]` Post the exact-head review route and selected/skipped lenses.
- [ ] `[PUB-IDEAS:P4.02][AI]` Read back route, frozen scope, changed probe, and AI marker.
- [ ] `[PUB-IDEAS:P4.03][AI]` Run bounded current-head review cycles under the Phase 4 template.
- [ ] `[PUB-IDEAS:P4.04][AI]` Disposition every finding with evidence and no scope widening.
- [ ] `[PUB-IDEAS:P4.05][AI]` Reply/read/resolve each native thread only at a true terminal state.
- [ ] `[PUB-IDEAS:P4.06][AI]` Poll applicable current-head CI exactly every 120 seconds.
- [ ] `[PUB-IDEAS:P4.07][AI]` Prove all five readiness preconditions on the same head.
- [ ] `[PUB-IDEAS:P4.08][AI]` Mark the PR ready after semantic exit.
- [ ] `[PUB-IDEAS:P4.09][AI]` Read back ready state, head, merge state, and green CI.
- [ ] `[PUB-IDEAS:P4.G][AI]` Pass semantic-exit/current-head-CI/frozen-scope gate.
- [ ] `[PUB-IDEAS:P4.P][AI]` Record head, cycles, threads, CI, and pending private obligation.
- [ ] `[PUB-IDEAS:P5.01][AI]` Recheck route, findings, base, head, ready state, and green CI.
- [ ] `[PUB-IDEAS:P5.02][AI]` Run `/usr/bin/git diff --binary <current-main> <reviewed-head> | /usr/bin/shasum -a 256`.
- [ ] `[PUB-IDEAS:P5.03][AI]` Squash-merge by repository-qualified GitHub API.
- [ ] `[PUB-IDEAS:P5.04][AI]` Read back merge SHA and landed path ledger.
- [ ] `[PUB-IDEAS:P5.05][AI]` Run `/usr/bin/git diff --binary <merge-sha>^1 <merge-sha> | /usr/bin/shasum -a 256`.
- [ ] `[PUB-IDEAS:P5.06][AI]` Prove reviewed and landed fingerprints are equal.
- [ ] `[PUB-IDEAS:P5.07][AI]` Publish the pending private obligation from a literal payload.
- [ ] `[PUB-IDEAS:P5.08][AI]` Read back its public pin, expected private paths, owner, and marker.
- [ ] `[PUB-IDEAS:P5.09][AI]` Fetch public `origin/main` and prove it equals the merge SHA.
- [ ] `[PUB-IDEAS:P5.10][AI]` Resync this same public worktree to the merge SHA.
- [ ] `[PUB-IDEAS:P5.11][AI]` Authorize only PRIV-BASE in the quarantined private worktree.
- [ ] `[PUB-IDEAS:P5.G][AI]` Pass merge/landed/fingerprint/obligation/resync/sibling gate.
- [ ] `[PUB-IDEAS:P5.P][AI]` Record merge/main SHA, obligation state, and PRIV-BASE entry command.

### WAVES-ENTRY-PUBLIC Finding State

This slice repairs the continuing-rule and literal idea-acceptance findings from PR #258, instantiates
the public half of current-main baseline handling, and carries PR #259's raw-fingerprint lesson into
both public units. Its merge pin is necessary but does not close F-035: ENTRY-PRIVATE must add the
overlay-safe units, and ENTRY-ADAPTERS must record all three ENTRY pins before advancing that finding.

## Dormant Lifecycle and Evidence-State Template

The lines below deliberately are not checkboxes. The five WAVES checklist slices must copy every
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
- **Template `[AI]`:** Use a raw patch fingerprint because a squash merge changes commit ancestry.
  Call `/usr/bin/git` directly so display compaction cannot rewrite the bytes being hashed. Run the
  repository-qualified API-side merge and keep local cleanup separate:

  ```bash
  /usr/bin/git diff --binary <current-main> <reviewed-head> | /usr/bin/shasum -a 256
  gh pr merge --repo <owner/repo> <pr> --squash
  gh pr view --repo <owner/repo> <pr> --json headRefOid,mergeCommit,mergedAt,state
  git fetch origin main
  git show --first-parent --format=fuller --patch <merge-sha>
  /usr/bin/git diff --binary <merge-sha>^1 <merge-sha> | /usr/bin/shasum -a 256
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

CORE-ENTRY, CORE-REVIEW, all three WAVES-ENTRY slices, WAVES-A, WAVES-RULES, and EXECUTION-CLOSURE must
turn this order into a 1:1 runnable checklist and preserve every merge step and its authority. No
assembly PR may begin implementation.

## Dormant Authority Mapping

This mapping replaces the two historical shortcut checkboxes; it is not executable work.
The five WAVES checklist slices must instantiate each applicable Phase 4–5 action and gate per owned unit,
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
