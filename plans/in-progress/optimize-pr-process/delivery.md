# Delivery Plan: Optimize the Pull Request Process

## Current State

| Evidence                                                                                           | State                                                                                                          |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [Repo-grounded] Merged [PR #250](https://github.com/wahidyankf/ose-public/pull/250)                | FOUNDATION at `62608547df0d2063d369537e0753f22699456f44`                                                       |
| [Repo-grounded] Merged [PR #251](https://github.com/wahidyankf/ose-public/pull/251)                | REQUIREMENTS at `8884ec79437a05af3e8404e63239e079a379d84f`                                                     |
| [Repo-grounded] Merged [PR #252](https://github.com/wahidyankf/ose-public/pull/252)                | DESIGN at `3ac2468f534be2faaf0b5a784b04b6411313f49e`                                                           |
| [Repo-grounded] Merged [PR #253](https://github.com/wahidyankf/ose-public/pull/253)                | FORECAST at `a46725dba24c4880e7854b0b5504b26dd3bdbb33`                                                         |
| [Repo-grounded] Merged [PR #254](https://github.com/wahidyankf/ose-public/pull/254)                | Split forecast at `b4dca85adc9ebc42eb53d69500e5d0475adb1522`                                                   |
| [Repo-grounded] Merged [PR #255](https://github.com/wahidyankf/ose-public/pull/255)                | CORE-ENTRY at `6e3412576ee32b8a34882c8f5df38019a1825e03`                                                       |
| [Repo-grounded] Merged [PR #256](https://github.com/wahidyankf/ose-public/pull/256)                | CORE-REVIEW at `b872a142a5063ff8d97bc04b89bc090529c932a4`                                                      |
| [Repo-grounded] Merged [PR #257](https://github.com/wahidyankf/ose-public/pull/257)                | WAVES-SPLIT at `aa5f14f768d0a8c4e0877d8aab7135b4d7529135`                                                      |
| [Repo-grounded] Closed [PR #258](https://github.com/wahidyankf/ose-public/pull/258)                | Incomplete WAVES-ENTRY draft; never merged                                                                     |
| [Repo-grounded] Merged [PR #259](https://github.com/wahidyankf/ose-public/pull/259)                | ENTRY split at `e205eca335d62618a206d5c85ebc8e8cdc4fa66e`                                                      |
| [Repo-grounded] Merged [PR #260](https://github.com/wahidyankf/ose-public/pull/260)                | BASE split at `5c61907d9d24718267dae8a2307e3578df1d18c9`                                                       |
| [Repo-grounded] Merged [PR #261](https://github.com/wahidyankf/ose-public/pull/261)                | PUBLIC at `9f1669e14bfed1e900b2ed81bb042d1b5c13ffd8`                                                           |
| [Repo-grounded] Merged [PR #262](https://github.com/wahidyankf/ose-public/pull/262)                | PRIVATE split at `3d9c0d843f877cfa498fe73ff4b321cef677dfb3`                                                    |
| [Repo-grounded] Merged PRs #263–#268                                                               | Assembly and EXECUTION-CLOSURE complete at `f9e96824c`                                                         |
| [Repo-grounded] Merged PRs #269–#271                                                               | Nine mapped public ideas retired before activation                                                             |
| [Repo-grounded] Merged [ACTIVATE PR #274](https://github.com/wahidyankf/ose-public/pull/274)       | ACTIVATE at `f30a9e55b232bb98d26482238ce50dd7a1391817`; its A0.P receipt authorizes PUB-BASE                   |
| [Repo-grounded] Merged [plan amendment PR #275](https://github.com/wahidyankf/ose-public/pull/275) | PUB-IDEAS-4 live-backlink authority at `f87347632e5b40188340339f888dfbb8f8b8f85c`                              |
| [Repo-grounded] Merged [PUB-IDEAS-4 PR #276](https://github.com/wahidyankf/ose-public/pull/276)    | PUB-IDEAS-4 terminal successor evidence at `64dbe6de9607d682f15c9c2edb18e720bafab248`                          |
| [Repo-grounded] Merged [plan amendment PR #277](https://github.com/wahidyankf/ose-public/pull/277) | PUB-IDEAS-5 execution base at `2d2e8208076a6be4e57087ea02f15b1338afb80f`; quality remediation freezes its edit |

> **RECONCILIATION HISTORY AND FREEZE:** PRs #269–#271 are non-authorizing data points. PR #274
> merged with its read-back A0.P receipt, PUB-BASE completed cleanly, PR #275 amended only
> PUB-IDEAS-4's live-backlink authority, PR #276 completed PUB-IDEAS-4, and PR #277 amended only
> PUB-IDEAS-5's live-backlink authority. PUB-IDEAS-5 is the sole candidate successor, but its edit
> remains frozen until this plan-quality remediation merges; it then starts only from that amendment
> merge pin. Private work and every rule/code wave remain frozen until their declared predecessor
> authorizes them.

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

PR #274 has merged, its zero-blocker ACTIVATE record was read back, and PUB-BASE completed cleanly.
PR #275 authorized PUB-IDEAS-4's live-backlink repair, PR #276 completed PUB-IDEAS-4, and PR #277
authorized PUB-IDEAS-5's live-backlink repair. PUB-IDEAS-5 is now the sole candidate successor, but
its edit remains **frozen** until this quality-remediation PR merges and its merge receipt supplies
the new execution-base pin. Both private checklist slices, ENTRY-ADAPTERS, WAVES-A, WAVES-RULES,
EXECUTION-CLOSURE, ideas, indexes, rules, agents, bindings, workflows, code, tests, implementation,
private worktree state, and active-plan indexes remain frozen until their declared predecessors
authorize them.

## Worktree

Reuse exactly one worktree per repository for this whole plan; follow the
[specification][worktree-spec], [cap][worktree-cap], and [path rule][worktree-path]:

- public: `worktrees/optimize-pr-process/` resolves to
  `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process` — active for assembly;
- private: `worktrees/optimize-pr-process/` resolves to
  `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process` — quarantined until terminal
  PUB-IDEAS evidence authorizes PRIV-BASE, and from every other use until its named successor.

For authored provisioning, run this documentation-only harness command from the relevant repository
root before using the fallback below; it does not authorize a second worktree:

```bash
claude --worktree optimize-pr-process
```

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
WAVES-ENTRY-BASE-SPLIT → WAVES-ENTRY-PUBLIC → WAVES-ENTRY-PRIVATE-SPLIT →
WAVES-ENTRY-PRIVATE-BASE-REPAIR → WAVES-ENTRY-PRIVATE-IDEAS → WAVES-ENTRY-ADAPTERS →
WAVES-A → WAVES-RULES → EXECUTION-CLOSURE → non-authorizing PUB-IDEAS-1–3 data points →
RECONCILE → ACTIVATE/equivalence-audit → PUB-IDEAS-4–8 → terminal public proof → PRIV-BASE →
conditional PRIV-REPAIR → PRIV-IDEAS →
implementation waves
```

Each arrow is a separate, unstacked PR from then-current `origin/main`, using the same owned public
worktree. Every assembly slice is at most 400 changed hand-authored lines and 20 hand-authored files.
Forecast each slice before opening it; if any would exceed a bound, record its named cohesive
sub-slices in the prior PR before opening the first split. A unique equivalence-audit blocker may
use one bounded `PLAN-AMENDMENT` PR before ACTIVATE. Final ACTIVATE contains only the PR-native
equivalence record and executable-status change. Merge green and resync before the next PR.

| Slice                           | Contract and audit IDs restored before activation                                                                                       | Target changed lines |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------: |
| CORE-ENTRY                      | Complete Phase 0–5 gate/pause-safe spine and state model, plus Phase 0–3 mechanics; F-005–F-011, F-014–F-016, F-025, F-026, F-028–F-030 |              230–300 |
| CORE-REVIEW                     | Review route, CI, correction firewall, merge and amendment; F-012, F-017, F-031, F-032, F-034                                           |              150–230 |
| WAVES-SPLIT                     | Forecast repair after the original EXECUTION-WAVES draft exceeded the hard cap                                                          |               70–125 |
| WAVES-ENTRY-SPLIT               | Forecast repair after PR #258 proved atomic ENTRY work exceeds its range ceiling                                                        |              100–180 |
| WAVES-ENTRY-BASE-SPLIT          | Forecast repair after the complete BASE probe crossed its forecast and hard cap                                                         |              120–180 |
| WAVES-ENTRY-PUBLIC              | Continuing rules; literal acceptance; public baseline/repair/ideas; F-035 partial                                                       |              200–260 |
| WAVES-ENTRY-PRIVATE-SPLIT       | Forecast repair after the corrected private-entry probe crossed its range ceiling                                                       |              140–180 |
| WAVES-ENTRY-PRIVATE-BASE-REPAIR | Private overlay-safe baseline and conditional repair; F-035 partial                                                                     |              115–160 |
| WAVES-ENTRY-PRIVATE-IDEAS       | Private overlay-safe idea retirement and pair pin; F-035 partial                                                                        |               80–125 |
| WAVES-ENTRY-ADAPTERS            | Single correction and sole PLAN-AMEND adapters; F-035 ENTRY terminal                                                                    |              100–155 |
| WAVES-A                         | PUB/PRIV A1–A2 checklists, acceptance, pair gates, and prior-pair reconciliation; F-035 A partial                                       |              190–250 |
| WAVES-RULES                     | PUB/PRIV A3 and B; optional-C decision/trigger; pair gates and prior-pair reconciliation; F-035 terminal owner                          |              200–270 |
| EXECUTION-CLOSURE               | Reconciliation/dogfood, knowledge, private terminal proof, public archival, cleanup; F-013, F-018, F-036–F-037                          |              220–300 |
| ACTIVATE                        | Bounded plan-gate equivalence record and explicit executable-status change                                                              |          at most 400 |

Closed PR #258 measured 302 changed lines before its six findings. The first complete repair model
expanded that draft by 106 lines to 408, but a BASE-only authoring probe then measured 401 changed
lines and 276 checkboxes: the model under-counted repeated per-unit review, CI, readiness, merge,
resync, and three-state overlay work. Splitting that measured draft repeats 12 status/ownership
lines: 413 total across PUBLIC and PRIVATE.

The corrected private-entry probe then measured 268 changed lines and 165 unique IDs: 19 PRIV-BASE,
75 PRIV-REPAIR, and 71 PRIV-IDEAS. Its [PR-native provenance record](https://github.com/wahidyankf/ose-public/pull/262#issuecomment-5386581220)
pins the inputs, exact compact inventory, measurement, and successor hashes. BASE-REPAIR and IDEAS
therefore become two independently readable checklist slices; they repeat only the private command
key, status, ownership, and terminal handoff needed for each PR to stand alone.

Here, an invariant is an always-on evidence rule, literal acceptance gives the exact command and
expected result, and state-specific overlay proof hashes unstaged, staged, and committed changes
separately. Scaffolding is the status, owner, and acceptance text repeated so each PR stands alone.

| PR #258 Cycle 1 finding                                                                                                   | Local repair owner                         | Required repair                                                                                    | Terminal proof                                                             |
| ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [Compound Git/GitHub transitions](https://github.com/wahidyankf/ose-public/pull/258#discussion_r3838415346)               | PUBLIC, both PRIVATE slices, then ADAPTERS | Separate calculate/gate/push, route/read/review, ready, merge/landed-proof, and resync actions     | ADAPTERS records all four ENTRY checklist merge pins before F-035 advances |
| [Continuing ENTRY rules used as tasks](https://github.com/wahidyankf/ose-public/pull/258#discussion_r3838415349)          | PUBLIC                                     | Keep always-on rules as prose enforced by each unit gate; check only finishable owned actions      | PUBLIC merged pin plus its unit-gate evidence                              |
| [Ambiguous idea acceptance](https://github.com/wahidyankf/ose-public/pull/258#discussion_r3838415350)                     | PUBLIC                                     | Give literal predecessor/reviewed-head commands, expected results, and the post-push rerun         | PUBLIC merged pin plus command/output evidence                             |
| [Worktree may not be on current main](https://github.com/wahidyankf/ose-public/pull/258#discussion_r3838415351)           | PUBLIC for public; PRIVATE for private     | Separate fetch, safe detach, `HEAD == origin/main`, status, and private before/after overlay proof | PRIVATE merged pin verifies both repository-local checklists               |
| [One fingerprint cannot cover three Git states](https://github.com/wahidyankf/ose-public/pull/258#discussion_r3838415352) | PRIVATE                                    | Compare unstaged, staged, and `<unit-base>..HEAD` fingerprints at their real states                | PRIVATE merged pin plus three-state equality evidence                      |
| [Stale assembly state](https://github.com/wahidyankf/ose-public/pull/258#pullrequestreview-5002302877)                    | WAVES-ENTRY-SPLIT                          | Record PR #257 as merged, PR #258 as closed unmerged, and successor slices                         | PR #259 merge pin                                                          |

The ledger is lossless: a row closes only at its terminal proof. Closing PR #258 removes its unsafe
draft from the delivery path but does not itself close any repair row.

PR #259 added one later dogfood lesson. WAVES-ENTRY-BASE-SPLIT owns aligning the shared Phase 5
template on raw input; ENTRY-PUBLIC owns copying that exact command into its continuing rules and
public-unit tasks. The lesson closes only at PUBLIC's merged pin after its checklist and the shared
template use the same `/usr/bin/git diff --binary ... | /usr/bin/shasum -a 256` procedure.

| Complete-preview component           | ENTRY-PUBLIC | ENTRY-PRIVATE (two slices) | ENTRY-ADAPTERS | WAVES-A | WAVES-RULES |
| ------------------------------------ | -----------: | -------------------------: | -------------: | ------: | ----------: |
| Shared rules and literal acceptance  |           52 |                          0 |             18 |      18 |          18 |
| Repository-local units               |          145 |                        165 |             72 |     160 |         176 |
| Status, ownership, and F-035 proof   |           28 |                         43 |             28 |      30 |          34 |
| **Forecast complete-preview total**  |      **225** |                    **208** |        **118** | **208** |     **228** |
| **Repair headroom to range ceiling** |       **35** |                     **77** |         **37** |  **42** |      **42** |

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
  units. The two private slices author the overlay-safe baseline/repair and idea counterparts.
  ENTRY-ADAPTERS owns the single public correction and sole reusable `PLAN-AMENDMENT` adapter.
  WAVES-A owns A1–A2;
  WAVES-RULES owns A3/B/C, and a positive C decision triggers only the ADAPTERS route. F-035 closes
  only after all four ENTRY checklist pins and the A and RULES pins exist.
- EXECUTION-CLOSURE authors the later checklist for reconciling the plan with what landed, dogfooding the
  process—using it on its own PRs—capturing knowledge, closing private work, archiving the public
  plan, and safely removing worktrees.
- ACTIVATE runs the bounded equivalence audit below before changing the assembled plan from dormant to executable.

Both CORE slices, every WAVES forecast repair, all four ENTRY checklist slices, WAVES-A,
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
The six WAVES checklist slices supply exact unit scope/acceptance; EXECUTION-CLOSURE supplies Phase 6.

| Phase(s) | Unit        | Repo/WT         | Branch                                               | Mode           | PR      | Predecessor                                                                                   | Stable result                 |
| -------- | ----------- | --------------- | ---------------------------------------------------- | -------------- | ------- | --------------------------------------------------------------------------------------------- | ----------------------------- |
| 1–5      | ACTIVATE    | public/PUB-WT   | `optimize-pr-process-activate`                       | worktree-to-pr | Phase 3 | RECONCILE / #272 merge, or the sole PLAN-AMENDMENT merge                                      | executable plan record        |
| 0        | PUB-BASE    | public/PUB-WT   | `—`                                                  | no delivery    | no      | ACTIVATE                                                                                      | public baseline recorded      |
| 1–5?     | PUB-REPAIR  | public/PUB-WT   | `optimize-pr-process-public-baseline-repair-<slug>`  | worktree-to-pr | Phase 3 | ACTIVATE                                                                                      | public baseline repaired      |
| 1–5      | PUB-IDEAS-4 | public/PUB-WT   | `optimize-pr-process-pub-ideas-4`                    | worktree-to-pr | Phase 3 | PUB-BASE:P0.10 → PUB-IDEAS-4 clean-direct or PUB-REPAIR:P5.17 → PUB-IDEAS-4 successful-repair | first remaining ideas retired |
| 1–5      | PUB-IDEAS-5 | public/PUB-WT   | `optimize-pr-process-pub-ideas-5`                    | worktree-to-pr | Phase 3 | PUB-IDEAS-4:P5.12                                                                             | next ideas retired            |
| 1–5      | PUB-IDEAS-6 | public/PUB-WT   | `optimize-pr-process-pub-ideas-6`                    | worktree-to-pr | Phase 3 | PUB-IDEAS-5:P5.12                                                                             | next ideas retired            |
| 1–5      | PUB-IDEAS-7 | public/PUB-WT   | `optimize-pr-process-pub-ideas-7`                    | worktree-to-pr | Phase 3 | PUB-IDEAS-6:P5.12                                                                             | next ideas retired            |
| 1–5      | PUB-IDEAS-8 | public/PUB-WT   | `optimize-pr-process-pub-ideas-8`                    | worktree-to-pr | Phase 3 | PUB-IDEAS-7:P5.12                                                                             | terminal public proof         |
| 0        | PRIV-BASE   | private/PRIV-WT | `—`                                                  | no delivery    | no      | terminal PUB-IDEAS proof                                                                      | overlay-safe baseline         |
| 1–5?     | PRIV-REPAIR | private/PRIV-WT | `optimize-pr-process-private-baseline-repair-<slug>` | worktree-to-pr | Phase 3 | evidenced PRIV-BASE failure                                                                   | private baseline repaired     |
| 1–5      | PRIV-IDEAS  | private/PRIV-WT | `optimize-pr-process-priv-ideas`                     | worktree-to-pr | Phase 3 | PRIV-BASE:P0.16 clean/overlay-owned **or PRIV-REPAIR:P5.15 successful-repair**                | private ideas retired         |
| 1–5      | PUB-A1      | public/PUB-WT   | `optimize-pr-process-pub-a1`                         | worktree-to-pr | Phase 3 | PRIV-IDEAS                                                                                    | plan rules coherent           |
| 1–5      | PRIV-A1     | private/PRIV-WT | `optimize-pr-process-priv-a1`                        | worktree-to-pr | Phase 3 | PUB-A1                                                                                        | private A1 adapted            |
| 1–5      | PUB-A2      | public/PUB-WT   | `optimize-pr-process-pub-a2`                         | worktree-to-pr | Phase 3 | PRIV-A1                                                                                       | review routing coherent       |
| 1–5      | PRIV-A2     | private/PRIV-WT | `optimize-pr-process-priv-a2`                        | worktree-to-pr | Phase 3 | PUB-A2                                                                                        | private A2 adapted            |
| 1–5      | PUB-A3      | public/PUB-WT   | `optimize-pr-process-pub-a3`                         | worktree-to-pr | Phase 3 | PRIV-A2                                                                                       | PR/reply rules coherent       |
| 1–5      | PRIV-A3     | private/PRIV-WT | `optimize-pr-process-priv-a3`                        | worktree-to-pr | Phase 3 | PUB-A3                                                                                        | private A3 adapted            |
| 1–5      | PUB-B       | public/PUB-WT   | `optimize-pr-process-pub-b`                          | worktree-to-pr | Phase 3 | PRIV-A3                                                                                       | legacy conflict removed       |
| 1–5      | PRIV-B      | private/PRIV-WT | `optimize-pr-process-priv-b`                         | worktree-to-pr | Phase 3 | PUB-B                                                                                         | private conflict removed      |
| 1–5      | PUB-C?      | public/PUB-WT   | `optimize-pr-process-pub-c`                          | worktree-to-pr | Phase 3 | PRIV-B                                                                                        | necessity-gated mechanism     |
| 1–5      | PRIV-C?     | private/PRIV-WT | `optimize-pr-process-priv-c`                         | worktree-to-pr | Phase 3 | PUB-C                                                                                         | private C adapted             |
| 1–5?     | PUB-CORR?   | public/PUB-WT   | `optimize-pr-process-pub-<wave>-correction-1`        | worktree-to-pr | Phase 3 | portable defect + pin                                                                         | replacement public pin        |
| 1–5?     | PLAN-AMEND? | public/PUB-WT   | `optimize-pr-process-plan-amendment-<slug>`          | worktree-to-pr | Phase 3 | plan defect + frozen pin                                                                      | amended plan pin              |
| 1–6      | CLOSURE     | public/PUB-WT   | `optimize-pr-process-closure`                        | worktree-to-pr | Phase 3 | last unit                                                                                     | plan archived and focused     |

Repair rows activate only after their baseline fails; each runs Phases 1–5, merges, and reruns that
baseline. Its ordinary successor uses the repair merge SHA; otherwise it uses the normal pin shown.
Optional C becomes a recorded no-change decision when necessity fails. Before each unit, replace
its predecessor with the exact SHA in the task, body, and audit comment. Missing state blocks the
next row. CLOSURE opens its one draft PR in inherited Phase 3, completes review/merge/resync in
inherited Phases 4–5, then performs only final evidence, knowledge capture, archive, and cleanup in
Phase 6. A correction resumes its paused private PR from the replacement public pin; an amendment
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

FOUNDATION through EXECUTION-CLOSURE are merged. PRs #269–#271 then retired nine mapped ideas
without the required ACTIVATE pin. They authorize no successor. ACTIVATE may open only after this
reconciliation records their exact effect, freezes the remaining work, and the bounded equivalence
audit passes. Historic evidence may satisfy only a catalog row it directly proves; it cannot stand
in for an uncovered check.

### Reconciliation Ledger — Surviving Source and Rule Changes

The reconciliation range is public `f9e96824c94a8364890ff03c970eaed231f31f64` through
`7e111df8d821e0e147e0009f6bd66c13e7499614`. The rows below are history-only baseline evidence:
they do not modify any listed source, authorize a successor, or broaden this plan. “Current main”
means preserve the landed state unless its separately named owner later changes it.

| Path                                                                                    | Landed semantic effect                                                                                             | Owner                                   | Source pin                                 | Disposition                                                                |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------- |
| `plans/ideas/README.md`                                                                 | Removed the nine retired brief links, leaving the landed index state that later mapped retirements must reconcile. | PUB-IDEAS-4–8 / EXECUTION               | `7e111df8d821e0e147e0009f6bd66c13e7499614` | Preserve as current baseline; retire links only through their mapped unit. |
| `plans/ideas/q1-urgent-important/deletion-authorized-by-absence.md`                     | Replaced a retired-brief link with the retained falsifiable-evidence rationale.                                    | PUB-IDEAS-4 / B                         | `7e111df8d821e0e147e0009f6bd66c13e7499614` | Preserve as current baseline; retire only through its mapped unit.         |
| `plans/ideas/q1-urgent-important/file-naming-convention-rework.md`                      | Replaced the retired ownership-registry link with a short rule-reach explanation.                                  | Current main, outside this control plan | `7e111df8d821e0e147e0009f6bd66c13e7499614` | No action; do not recreate the deleted registry.                           |
| `plans/ideas/q1-urgent-important/plan-checker-forward-reference-detection.md`           | Folded two retired related-brief links into one planning-evidence explanation.                                     | PUB-IDEAS-5 / EXECUTION                 | `7e111df8d821e0e147e0009f6bd66c13e7499614` | Preserve as current baseline; retire only through its mapped unit.         |
| `plans/ideas/q2-not-urgent-important/merge-queue-adoption.md`                           | Removed the retired bot-identity link without changing the no-vendor-adoption boundary.                            | PUB-IDEAS-5 / EXECUTION                 | `7e111df8d821e0e147e0009f6bd66c13e7499614` | Preserve as current baseline; retire only through its mapped unit.         |
| `plans/ideas/q2-not-urgent-important/propagation-checklist-under-coverage.md`           | Replaced the retired acceptance-brief link with the retained falsifiable-evidence rationale.                       | PUB-IDEAS-8 / C                         | `7e111df8d821e0e147e0009f6bd66c13e7499614` | Preserve as current baseline; retire only through its mapped unit.         |
| `plans/ideas/q2-not-urgent-important/vitest-glob-coverage-guard.md`                     | Repointed falsifiability evidence to Trustworthy Measurement Rule 5.                                               | Current main, outside this control plan | `7e111df8d821e0e147e0009f6bd66c13e7499614` | No action; preserve the landed replacement reference.                      |
| `repo-governance/development/quality/pr-review-disciplines/future-work-bot-identity.md` | Made the no-bot/App decision explicit and requires separate evidence before review state can become authoritative. | PUB-A3                                  | `7e111df8d821e0e147e0009f6bd66c13e7499614` | Retain as live rule baseline; no identity tooling in this plan.            |
| `repo-governance/workflows/pr/pr-review-quality-gate/review-state-is-never-the-gate.md` | Requires finding severity, not review state, until a separately proven independent identity exists.                | PUB-A2                                  | `7e111df8d821e0e147e0009f6bd66c13e7499614` | Retain as live rule baseline; A2 must not contradict it.                   |

## Bounded Activation Equivalence Audit

This audit replaces only this plan's redundant iterative run; it neither weakens the pinned catalog
nor changes the durable workflow. At the recorded pin, the ACTIVATE matrix has exactly one independent
row for every numbered rule, bullet, sub-bullet, and conditional check in both catalog documents: no
grouping or inherited evidence. A nonconditional row is never `N/A`: without direct evidence it is
uncovered. Only a catalog-defined conditional whose applicability condition is demonstrably false may
be reasoned `N/A`; its row cites that condition and the evidence. Codebase Alignment remains explicit.

### ACTIVATE Entry Contract

ACTIVATE is a public plan-only PR from `optimize-pr-process-activate`. Its exact predecessor is the
RECONCILE merge or, only when this audit proves one unique blocker, the sole PLAN-AMENDMENT merge.
Its admitted tracked ledger is only `plans/in-progress/optimize-pr-process/README.md` and
`plans/in-progress/optimize-pr-process/delivery.md`; the complete evidence matrix lives in the
AI-marked literal PR body and is read back through GitHub. Before editing, fetch `origin/main`,
create or safely reuse the declared branch from that exact pin, prove `HEAD == origin/main`, and
record the predecessor SHA, two-path ledger, static-document safety, rollback-by-revert, and
400-line/20-file forecast. ACTIVATE never touches the private worktree, ideas, rules, bindings,
code, or tests. PUB-BASE may start only after the read-back AI-marked A0.P comment is verified by
its P0.00 entry check; the tracked PUB-BASE checklist is the sole command authority. An uncovered
row instead follows the single PLAN-AMENDMENT route and keeps every later unit frozen.

- [x] `[ACTIVATE:A0.01][AI]` Record the catalog, original reconciliation pin `6be0dc59dd5453b93a876a85575b7f07f0282169`, amendment merge pin `22bffb9263b020301d4ad9a6ff938c2277deef87`, and one literal PR-body matrix row for every catalog check. **Done:** the complete AI-marked matrix is this PR's GitHub-read-back record.
- [x] `[ACTIVATE:A0.02][AI]` Link direct current evidence for each row, or a catalog-defined inapplicable conditional with its condition and proof. **Done:** every unconditional row has direct evidence; only E01–E03 and A01 were reopened after the amendment.
- [x] `[ACTIVATE:A0.03][AI]` Check only previously uncovered rows and record each blocker, its evidence, total count, and uniqueness without a general re-review. **Done:** E01–E03 and A01 now have direct evidence in the merged ACTIVATE boundary; blocker count is zero.
- [x] `[ACTIVATE:A0.04][AI]` Apply exactly one cardinality transition: zero blockers authorizes ACTIVATE; one unique blocker may use the sole amendment; otherwise freeze. **Done:** B-01 was unique and used the sole amendment route; its merge authorizes ACTIVATE.
- [x] `[ACTIVATE:A0.04a][AI]` After the sole amendment, re-evaluate only affected rows once and freeze for a remaining blocker. **Done:** at `22bffb9263b020301d4ad9a6ff938c2277deef87`, E01–E03 and A01 pass; no second amendment is permitted.
- [x] `[ACTIVATE:A0.05][AI]` Post and read back the complete AI-marked matrix, with direct evidence for all required rows, zero blockers, and no undisposed row. **Done:** this PR body is the complete, read-back equivalence record.
- [x] `[ACTIVATE:A0.G][AI]` Pass exact-pin, full-catalog, evidence-link, uncovered-row, no-duplicate-loop, and zero-blocker checks before executable status. **Done:** this record proves all six; merge makes the plan executable.
- [x] `[ACTIVATE:A0.P][AI]` Post-merge evidence receipt only: the read-back AI-marked PR #274 comment records its reviewed head, equivalence-record URL, final CI result, actual merge pin, and a reference to tracked `PUB-BASE:P0.00`. **Done:** its immutable merge is `f30a9e55b232bb98d26482238ce50dd7a1391817`; the receipt authorizes no different successor and supplies no executable command.

## Dormant Execution-Wave Public Entry Checklist

Every remaining checkbox is inert until ACTIVATE. After activation, copy only the active unit's IDs
into the live task list 1:1; this Markdown remains durable evidence, and only one unit may be active.

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

### Entry Command Key

- Guarded detach: `git switch --detach "$(git rev-parse origin/main)"`; require unchanged admitted status and `HEAD == origin/main`.
- Pre-push: `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`; require exit 0.
- Local gates: use the [Phase 2 list](#dormant-phase-2-template--verify-stage-and-commit); record each pass or owner/evidence/reasoned `N/A`.
- Merge: `gh pr merge --repo <owner/repo> <pr> --squash`; resync with `git fetch origin main` then `git switch --detach <merge-sha>` and prove clean `HEAD == origin/main == <merge-sha>`.

### PUB-BASE — Public Repository Baseline

- [x] `[PUB-BASE:P0.00][AI]` Read-only authorization check completed against PR #274's read-back AI-marked A0.P receipt. **Done:** it named the reviewed head, equivalence record, final CI, merge pin, and tracked `PUB-BASE:P0.00`; GitHub evidence was not treated as executable commands.
- [x] `[PUB-BASE:P0.01][AI]` Verified ACTIVATE's merge pin was an ancestor of public `origin/main`. **Done:** direct route recorded in the PR #274 receipt.
- [x] `[PUB-BASE:P0.02][AI]` Fetched public `origin/main` without advancing a checked-out local branch. **Done:** recorded before baseline commands.
- [x] `[PUB-BASE:P0.03][AI]` Recorded the public worktree and its explained clean state. **Done:** no unadmitted residue entered PUB-BASE.
- [x] `[PUB-BASE:P0.04][AI]` Safely detached this worktree at fetched public `origin/main`. **Done:** baseline used the recorded main pin.
- [x] `[PUB-BASE:P0.05][AI]` Proved `HEAD == origin/main` and recorded both immutable SHAs. **Done:** the evidence is in the A0.P-linked baseline receipt.
- [x] `[PUB-BASE:P0.06][AI]` Ran `npm install`. **Done:** exit 0.
- [x] `[PUB-BASE:P0.07][AI]` Ran plain `npm run doctor`. **Done:** 16/16 checks passed.
- [x] `[PUB-BASE:P0.08][AI]` Ran the repository pre-push surface. **Done:** exit 0; 419 known README-index advisories are recorded as nonblocking baseline diagnostics.
- [x] `[PUB-BASE:P0.09][AI]` Classified failures as pre-existing and rejected ordinary-unit attribution. **Done:** no baseline failure required PUB-REPAIR.
- [x] `[PUB-BASE:P0.10][AI]` Authorized PUB-IDEAS-4 exactly on `optimize-pr-process-pub-ideas-4` and recorded PUB-REPAIR as reasoned `N/A`. **Done:** PUB-IDEAS-4 later landed in PR #276.
- [x] `[PUB-BASE:P0.11][AI]` On evidenced baseline failure, close and authorize only PUB-REPAIR. **N/A:** P0.06–P0.08 were clean.
- [x] `[PUB-BASE:P0.G][AI]` Passed exactly one terminal gate: clean/direct. **Done:** PUB-IDEAS-4 was the only authorized ordinary successor.
- [x] `[PUB-BASE:P0.P][AI]` Recorded result, predecessor pin, authorized successor, and recheck command. **Done:** the immutable receipt is linked from PR #274 and the successor landed in PR #276.

### PUB-REPAIR — Conditional Public Baseline Repair

Open this unit only for a reproduced public baseline failure. Otherwise record it `N/A` at PUB-BASE;
repair an ordinary-unit defect only inside that unit's own scope.

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
- [ ] `[PUB-REPAIR:P4.03][AI]` Run successive exact-head cycles under the five-cycle boundary.
- [ ] `[PUB-REPAIR:P4.04][AI]` Record every finding as fix, reject, defer, or clarify with evidence.
- [ ] `[PUB-REPAIR:P4.05][AI]` Push each bounded fix before claiming it in the native thread.
- [ ] `[PUB-REPAIR:P4.06][AI]` Invalidate every review and CI result from the superseded head.
- [ ] `[PUB-REPAIR:P4.07][AI]` Return the repaired head to P4.03 before any thread resolution.
- [ ] `[PUB-REPAIR:P4.08][AI]` Reply in the original thread with current-head evidence.
- [ ] `[PUB-REPAIR:P4.09][AI]` Read back the persisted reply and its AI marker.
- [ ] `[PUB-REPAIR:P4.10][AI]` Resolve only threads whose terminal evidence is true.
- [ ] `[PUB-REPAIR:P4.11][AI]` Poll applicable current-head CI exactly every 120 seconds until terminal.
- [ ] `[PUB-REPAIR:P4.12][AI]` Prove the five readiness preconditions on one current head.
- [ ] `[PUB-REPAIR:P4.13][AI]` Mark the PR ready only after semantic exit.
- [ ] `[PUB-REPAIR:P4.14][AI]` Read back ready state, current head, merge state, and green CI.
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
- [ ] `[PUB-REPAIR:P5.11][AI]` Record clean status on the resynced landed-main worktree.
- [ ] `[PUB-REPAIR:P5.12][AI]` Run `npm install` on the landed main pin.
- [ ] `[PUB-REPAIR:P5.13][AI]` Run plain `npm run doctor` on the landed main pin.
- [ ] `[PUB-REPAIR:P5.14][AI]` Run the literal pre-push command on the landed main pin.
- [ ] `[PUB-REPAIR:P5.15][AI]` Classify the single allowed repair attempt's landed recheck and keep PUB-IDEAS frozen unless it is clean.
- [ ] `[PUB-REPAIR:P5.16][AI]` Pass one recheck outcome: clean/ideas or evidenced-failure/frozen-human-stop; a failed repair cannot open another PUB-REPAIR.
- [ ] `[PUB-REPAIR:P5.17][AI]` Record recheck evidence; only a clean successful repair authorizes `PUB-IDEAS-4`. An evidenced failed recheck records that the one PUB-REPAIR attempt is spent, keeps PUB-IDEAS frozen, and stops for human judgment without a second repair.
- [ ] `[PUB-REPAIR:P5.G][AI]` Pass merge/landed/fingerprint/resync/baseline/successor gate.
- [ ] `[PUB-REPAIR:P5.P][AI]` Record merge/main SHA, baseline result, and named-successor command.

### PUB-IDEAS — Retire Public Sources in Human-Sized Subdeliveries

The single 19-brief forecast was invalid: it exceeded the 400-line ceiling and the first three
subdeliveries landed before ACTIVATE. Preserve them as evidence and do not retroactively claim they
followed the activation gate. PUB-IDEAS-4 is complete under its immutable ledger below. Only the
remaining PUB-IDEAS-5–8 units may instantiate the unchecked shared checklist by replacing
`PUB-IDEAS` with their exact unit ID and mapped subset.

| Unit                  | State                                                                                | Exact mapped paths                                                                                                                                                                                                                                                                                                  |
| --------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PUB-IDEAS-1 / PR #269 | merged, non-authorizing                                                              | `plans/ideas/q1-urgent-important/acceptance-clause-vacuity.md`; `plans/ideas/q1-urgent-important/plan-decision-integrity-hardening.md`                                                                                                                                                                              |
| PUB-IDEAS-2 / PR #270 | merged, non-authorizing                                                              | `plans/ideas/q2-not-urgent-important/plan-quality-gate-convergence.md`; `plans/ideas/q2-not-urgent-important/repo-rules-quality-gate-convergence.md`; `plans/ideas/q2-not-urgent-important/review-loop-reviews-its-own-record.md`                                                                                   |
| PUB-IDEAS-3 / PR #271 | merged, non-authorizing                                                              | `plans/ideas/q2-not-urgent-important/gate-exclusions-need-a-named-owner.md`; `plans/ideas/q2-not-urgent-important/governance-path-ownership-registry.md`; `plans/ideas/q2-not-urgent-important/pr-review-bot-identity.md`; `plans/ideas/q2-not-urgent-important/pr-review-disciplines-applicability-shard-empty.md` |
| PUB-IDEAS-4 / PR #276 | merged at `64dbe6de9607d682f15c9c2edb18e720bafab248`                                 | `plans/ideas/q1-urgent-important/deletion-authorized-by-absence.md`; `plans/ideas/q2-not-urgent-important/class-sweep-completeness.md`                                                                                                                                                                              |
| PUB-IDEAS-5           | frozen pending this plan-quality remediation; PR #277 is its live-backlink authority | `plans/ideas/q1-urgent-important/plan-checker-forward-reference-detection.md`; `plans/ideas/q2-not-urgent-important/merge-queue-adoption.md`                                                                                                                                                                        |
| PUB-IDEAS-6           | frozen until PUB-IDEAS-5                                                             | `plans/ideas/q2-not-urgent-important/nx-affected-cross-worktree-contamination.md`; `plans/ideas/q2-not-urgent-important/stale-checkout-ref-advance-drift.md`                                                                                                                                                        |
| PUB-IDEAS-7           | frozen until PUB-IDEAS-6                                                             | `plans/ideas/q2-not-urgent-important/cross-repo-governance-link-parity.md`; `plans/ideas/q2-not-urgent-important/plan-archival-in-pr-multi-repo-gap.md`                                                                                                                                                             |
| PUB-IDEAS-8           | frozen until PUB-IDEAS-7                                                             | `plans/ideas/q2-not-urgent-important/propagation-checklist-under-coverage.md`; `plans/ideas/q2-not-urgent-important/recurring-defect-family-escalation.md`                                                                                                                                                          |

The mapped source path, not the shortened table label, is authoritative. Re-read the disposition
map before each unit. PUB-IDEAS-4–7 resync and authorize only the next named public subdelivery;
only PUB-IDEAS-8 may publish the private obligation and authorize PRIV-BASE.
At public `origin/main` `7e111df8d821e0e147e0009f6bd66c13e7499614`, their brief-only deletion forecasts are respectively 283, 293,
320, 227, and 237 lines. Each Phase 1 remeasures index and live-backlink repairs and splits again
before editing if the complete forecast would cross 400 changed hand-authored lines or 20 files.

A **live backlink** is a Markdown link to an active unit's mapped brief from outside `plans/done/**`.
Historical `plans/done/**` references remain unchanged. Before editing, P1.05 must enumerate every
such source path and the minimal unlink/rewording that preserves its surrounding meaning. That
published ledger is **evidence only**, never permission to edit a path. The merged, tracked
amendment table is the sole authority for a live-backlink repair; without an exact table entry, only
the mapped briefs and `plans/ideas/README.md` are admitted. A missing, unexpected, or mismatched
entry—or any repair above either cap—freezes the unit for the bounded split or amendment route.

#### PUB-IDEAS-4 live-backlink amendment ledger

This table supersedes the ambiguous PUB-IDEAS-4 interpretation at
`f30a9e55b232bb98d26482238ce50dd7a1391817`. PUB-IDEAS-4 remains frozen until this plan-only
amendment merges; its resumed entry must use that merge pin.

| Exact live-backlink path                                                           | Mapped target                       | Minimal permitted repair                                                                                               |
| ---------------------------------------------------------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `plans/ideas/q2-not-urgent-important/sdlc-gate-standard-property-bound-lag.md`     | `class-sweep-completeness.md`       | Replace the direct Markdown link with the existing plain-language “separately tracked class-sweep question” reference. |
| `plans/ideas/q2-not-urgent-important/bare-repo-landing-method-step-count-drift.md` | `class-sweep-completeness.md`       | Remove only the standalone direct Markdown-link line; preserve the preceding precedent explanation.                    |
| `plans/ideas/q2-not-urgent-important/recurring-defect-family-escalation.md`        | `deletion-authorized-by-absence.md` | Remove only the standalone direct Markdown-link line; preserve the worked-example explanation.                         |

For PUB-IDEAS-4 after this amendment, retain the clean PUB-BASE/PUB-REPAIR predecessor proof as
**authorization evidence**, but use the merged amendment pin as the sole **execution-base pin**.
The two pins answer different questions: the first proves why this unit is eligible; the second
proves which current `origin/main` it may safely edit from. Missing either pin freezes the unit.

#### PUB-IDEAS-5 live-backlink amendment ledger

This table resolves the pre-edit freeze at
`64dbe6de9607d682f15c9c2edb18e720bafab248`. PUB-IDEAS-5 remains frozen until this plan-only
amendment merges; its resumed entry must use that merge pin.

| Exact live-backlink path                                                                        | Mapped target             | Minimal permitted repair                                                                                                                                                                                    |
| ----------------------------------------------------------------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `repo-governance/development/quality/pr-review-disciplines/future-work-deferred-merge-queue.md` | `merge-queue-adoption.md` | Replace the complete ownership sentence containing the direct link with “The deferred investigation, availability matrix, and adoption path are tracked separately as future work, not by this convention.” |

For PUB-IDEAS-5 after this amendment, retain PUB-IDEAS-4's merged successor proof and PR #277 as
**authorization evidence**. This plan-quality-remediation PR's future merge receipt supplies the
sole **execution-base pin**; it does not alter PR #277's live-backlink authority. No later,
unrelated amendment may replace that pin. Missing the required authorization evidence, PR #277
authority, or this remediation receipt freezes the unit.

#### Immutable Completion Ledger — PUB-IDEAS-4 (Do Not Re-run)

The shared unchecked `PUB-IDEAS:P*` rows below are the executable template for PUB-IDEAS-5–8 only.
They are not open work for PUB-IDEAS-4 and must not be ticked retroactively. PR #276 is the durable,
immutable completion record for PUB-IDEAS-4; this ledger maps the completed state without rewriting
the future units' task IDs.

| PUB-IDEAS-4 state       | Immutable PR #276 evidence                                                                                                                    | Completion criterion                                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| P1.01–P1.13, P1.G, P1.P | [PR #276](https://github.com/wahidyankf/ose-public/pull/276), its route/ledger comments, and merge `64dbe6de9607d682f15c9c2edb18e720bafab248` | The two mapped briefs, index changes, and three #275-authorized live-backlink repairs were scoped and recorded before edit. |
| P2.01–P2.11, P2.G, P2.P | PR #276 commits and local-gate evidence                                                                                                       | The admitted retirement patch was gated, staged, committed, and read in full.                                               |
| P3.01–P3.08, P3.G, P3.P | PR #276 draft body/read-back and pushed head                                                                                                  | One human-readable, AI-marked draft represented the exact public head.                                                      |
| P4.01–P4.14, P4.G, P4.P | PR #276 route, review, reply, CI, and readiness artifacts                                                                                     | The review cycle reached semantic exit on its current head without widening scope.                                          |
| P5.01–P5.12, P5.G, P5.P | PR #276 merge receipt and successor publication                                                                                               | Reviewed and landed fingerprints matched; the public worktree resynced and named PUB-IDEAS-5.                               |

- [ ] `[PUB-IDEAS:P1.01][AI]` For PUB-IDEAS-5, read PUB-IDEAS-4's P5.07 publication and P5.08 read-back record on PR #276; acceptance: it names exact successor `PUB-IDEAS-5`, immutable predecessor/authorization-evidence pin, declared public worktree/branch, and `Generated by AI`. Record that pin, PR #277's immutable live-backlink-authority pin, and this plan-quality-remediation PR's merge-receipt execution-base pin. For PUB-IDEAS-6–8, verify the immediately prior unit's P5.07 publication and P5.08 read-back name this exact active unit and immutable pin.
- [ ] `[PUB-IDEAS:P1.02][AI]` Fetch public `origin/main`.
- [ ] `[PUB-IDEAS:P1.03][AI]` For PUB-IDEAS-5, retain the predecessor proof but require fetched `origin/main` to equal its P1.01 execution-base pin. For PUB-IDEAS-6–8, prove fetched `origin/main` equals the predecessor pin.
- [ ] `[PUB-IDEAS:P1.04][AI]` Enter this active unit's literal branch from the Delivery Boundaries table (`optimize-pr-process-pub-ideas-5`, `-6`, `-7`, or `-8`) from the exact main pin.
- [ ] `[PUB-IDEAS:P1.05][AI]` Publish the active subdelivery's exact mapped-brief, public-index, and every discovered live-backlink-repair path ledger before editing. For each backlink, name its target and minimal unlink/rewording; `plans/done/**` stays excluded and unchanged. This GitHub ledger is evidence only. For PUB-IDEAS-5, verify it exactly matches its merged tracked live-backlink amendment ledger; for every other unit, a discovered live backlink without an exact merged tracked entry freezes the unit. Acceptance: the later `git status` ledger equals the tracked authority, not GitHub prose.
- [ ] `[PUB-IDEAS:P1.06][AI]` Record forecast, static-doc safety, risk, and rollback-by-revert.
- [ ] `[PUB-IDEAS:P1.07][AI]` Record propagation and generated bindings as reasoned `N/A`.
- [ ] `[PUB-IDEAS:P1.08][AI]` Revalidate the active subset's dispositions against the activated plan pin.
- [ ] `[PUB-IDEAS:P1.09][AI]` Run literal predecessor acceptance for every row in the active subset.
- [ ] `[PUB-IDEAS:P1.10][AI]` Delete only the active subset's mapped public briefs.
- [ ] `[PUB-IDEAS:P1.11][AI]` Remove only their exact links from `plans/ideas/README.md`, then apply only the matching merged tracked amendment-table repair; preserve every historical `plans/done/**` reference and all unrelated prose. A P1.05 GitHub ledger cannot supply an edit path.
- [ ] `[PUB-IDEAS:P1.12][AI]` Run reviewed-worktree acceptance for every row in the active subset and verify `rg -n --glob '*.md' '\]\([^)]*<brief-basename>\.md[^)]*\)' . -g '!plans/done/**'` exits `1` with no output for each retired brief basename. The matcher deliberately includes any continuation after `.md` before `)` so fragment, query, and title forms cannot evade the negative check.
- [ ] `[PUB-IDEAS:P1.13][AI]` Reconcile `git status` exactly to the retirement ledger.
- [ ] `[PUB-IDEAS:P1.G][AI]` Pass pin/scope/size/ledger/disposition/acceptance gate.
- [ ] `[PUB-IDEAS:P1.P][AI]` Record branch, head, ledger, dirty state, and negative-read commands.
- [ ] `[PUB-IDEAS:P2.01][AI]` Rerun all reviewed-worktree acceptance commands before staging.
- [ ] `[PUB-IDEAS:P2.02][AI]` Run Markdown formatting and lint checks.
- [ ] `[PUB-IDEAS:P2.03][AI]` Run the public pre-push surface.
- [ ] `[PUB-IDEAS:P2.04][AI]` Calculate actual hand-authored line/file counts.
- [ ] `[PUB-IDEAS:P2.05][AI]` Gate both actual counts against the plan's caps.
- [ ] `[PUB-IDEAS:P2.06][AI]` Stage only the admitted retirement ledger.
- [ ] `[PUB-IDEAS:P2.07][AI]` Read cached paths and prove staged-ledger equality.
- [ ] `[PUB-IDEAS:P2.08][AI]` Inspect cached check, statistics, and complete patch.
- [ ] `[PUB-IDEAS:P2.09][AI]` Commit the cohesive public retirement.
- [ ] `[PUB-IDEAS:P2.10][AI]` Read the complete committed diff.
- [ ] `[PUB-IDEAS:P2.11][AI]` Rerun all reviewed-head acceptance commands after commit.
- [ ] `[PUB-IDEAS:P2.G][AI]` Pass acceptance/formatting/gates/size/staging/commit gate.
- [ ] `[PUB-IDEAS:P2.P][AI]` Record local head and clean tree or named intended residue.
- [ ] `[PUB-IDEAS:P3.01][AI]` Recalculate committed hand-authored counts.
- [ ] `[PUB-IDEAS:P3.02][AI]` Gate committed counts against the plan's caps.
- [ ] `[PUB-IDEAS:P3.03][AI]` Rerun the public pre-push surface on the committed head.
- [ ] `[PUB-IDEAS:P3.04][AI]` Push only the active subdelivery's declared branch.
- [ ] `[PUB-IDEAS:P3.05][AI]` Read back the remote branch head and prove it equals local `HEAD`.
- [ ] `[PUB-IDEAS:P3.06][AI]` Rerun all reviewed-head acceptance commands after push.
- [ ] `[PUB-IDEAS:P3.07][AI]` Open one draft human-readable PR for this subdelivery from a literal AI-marked body.
- [ ] `[PUB-IDEAS:P3.08][AI]` Read back base, head, draft state, body, marker, and statistics.
- [ ] `[PUB-IDEAS:P3.G][AI]` Pass push/remote-head/acceptance/body/readback gate.
- [ ] `[PUB-IDEAS:P3.P][AI]` Record draft URL, current head, and literal body path.
- [ ] `[PUB-IDEAS:P4.01][AI]` Post the exact-head review route and selected/skipped lenses.
- [ ] `[PUB-IDEAS:P4.02][AI]` Read back route, frozen scope, changed probe, and AI marker.
- [ ] `[PUB-IDEAS:P4.03][AI]` Run bounded current-head review cycles under the Phase 4 template.
- [ ] `[PUB-IDEAS:P4.04][AI]` Disposition every finding with evidence and no scope widening.
- [ ] `[PUB-IDEAS:P4.05][AI]` Push each bounded fix before claiming it in the native thread.
- [ ] `[PUB-IDEAS:P4.06][AI]` Invalidate every review and CI result from the superseded head.
- [ ] `[PUB-IDEAS:P4.07][AI]` Return the repaired head to P4.03 before any thread resolution.
- [ ] `[PUB-IDEAS:P4.08][AI]` Reply in the original thread with current-head evidence.
- [ ] `[PUB-IDEAS:P4.09][AI]` Read back the persisted reply and its AI marker.
- [ ] `[PUB-IDEAS:P4.10][AI]` Resolve only threads whose terminal evidence is true.
- [ ] `[PUB-IDEAS:P4.11][AI]` Poll applicable current-head CI exactly every 120 seconds.
- [ ] `[PUB-IDEAS:P4.12][AI]` Prove all five readiness preconditions on the same head.
- [ ] `[PUB-IDEAS:P4.13][AI]` Mark the PR ready after semantic exit.
- [ ] `[PUB-IDEAS:P4.14][AI]` Read back ready state, head, merge state, and green CI.
- [ ] `[PUB-IDEAS:P4.G][AI]` Pass semantic-exit/current-head-CI/frozen-scope gate.
- [ ] `[PUB-IDEAS:P4.P][AI]` Record head, cycles, threads, CI, and the still-frozen successor state.
- [ ] `[PUB-IDEAS:P5.01][AI]` Recheck route, findings, base, head, ready state, and green CI.
- [ ] `[PUB-IDEAS:P5.02][AI]` Run `/usr/bin/git diff --binary <current-main> <reviewed-head> | /usr/bin/shasum -a 256`.
- [ ] `[PUB-IDEAS:P5.03][AI]` Squash-merge by repository-qualified GitHub API.
- [ ] `[PUB-IDEAS:P5.04][AI]` Read back merge SHA and landed path ledger.
- [ ] `[PUB-IDEAS:P5.05][AI]` Run `/usr/bin/git diff --binary <merge-sha>^1 <merge-sha> | /usr/bin/shasum -a 256`.
- [ ] `[PUB-IDEAS:P5.06][AI]` Prove reviewed and landed fingerprints are equal.
- [ ] `[PUB-IDEAS:P5.07][AI]` For PUB-IDEAS-5–7, publish only the next public successor; for PUB-IDEAS-8, publish the pending private obligation from a literal payload.
- [ ] `[PUB-IDEAS:P5.08][AI]` Read back the exact successor, pin, owner, and marker; on PUB-IDEAS-8 also read expected private paths.
- [ ] `[PUB-IDEAS:P5.09][AI]` Fetch public `origin/main` after the merge.
- [ ] `[PUB-IDEAS:P5.10][AI]` Prove fetched `origin/main` equals the merge SHA.
- [ ] `[PUB-IDEAS:P5.11][AI]` Resync this same public worktree to the merge SHA.
- [ ] `[PUB-IDEAS:P5.12][AI]` Authorize only the next named public subdelivery, or PRIV-BASE after PUB-IDEAS-8 terminal proof.
- [ ] `[PUB-IDEAS:P5.G][AI]` Pass merge/landed/fingerprint/resync/exact-successor gate.
- [ ] `[PUB-IDEAS:P5.P][AI]` Record merge/main SHA, successor state, and the next public or PRIV-BASE entry command.

### WAVES-ENTRY-PUBLIC Finding State

This slice fixes PR #258's continuing-rule and idea-acceptance defects and carries PR #259's raw-hash
lesson into both public units. F-035 stays open until both private slices add overlay-safe units and
ENTRY-ADAPTERS records all four ENTRY checklist pins.

## Dormant Execution-Wave Private Entry Checklist

### Private Overlay Command Key

The admitted ledger is `plans/ideas/README.md` plus
`plans/ideas/q2-not-urgent-important/pr-review-governance-reference-defects.md`. Hash output is safe
to record; private patch content is not. Use these literal raw-byte commands at their real states:

- working: `/usr/bin/git diff --binary -- <overlay-ledger> | /usr/bin/shasum -a 256`;
- cached: `/usr/bin/git diff --cached --binary -- <overlay-ledger> | /usr/bin/shasum -a 256`;
- committed: `/usr/bin/git diff --binary <unit-base>..HEAD -- <overlay-ledger> | /usr/bin/shasum -a 256`;
- reviewed/landed: use the two exact Phase 5 raw commands with private base, head, and merge pins.

### PRIV-BASE — Overlay-Safe Private Baseline

Only a terminal PUB-IDEAS proof may authorize this baseline. Clean, non-overlay failure,
overlay-owned failure, and ambiguous attribution are mutually exclusive outcomes: clean and
overlay-owned continue to PRIV-IDEAS; evidenced non-overlay failure opens PRIV-REPAIR; ambiguity
stops with no successor.

- [ ] `[PRIV-BASE:P0.01][AI]` Read back the pending public obligation and every immutable pin, owner, class, successor, and AI marker.
- [ ] `[PRIV-BASE:P0.02][AI]` Prove the obligation's PUB-IDEAS merge pin is an ancestor of public `origin/main`.
- [ ] `[PRIV-BASE:P0.03][AI]` Record private status and prove only the admitted two-path overlay exists.
- [ ] `[PRIV-BASE:P0.04][AI]` Compute the literal raw working-overlay fingerprint before switching.
- [ ] `[PRIV-BASE:P0.05][AI]` Fetch private `origin/main` without advancing a checked-out branch.
- [ ] `[PRIV-BASE:P0.06][AI]` Safely detach this worktree at fetched private `origin/main` without stashing.
- [ ] `[PRIV-BASE:P0.07][AI]` Prove `HEAD == origin/main` and record both immutable SHAs.
- [ ] `[PRIV-BASE:P0.08][AI]` Re-read status and prove it still contains only the admitted overlay.
- [ ] `[PRIV-BASE:P0.09][AI]` Recompute the literal raw working-overlay fingerprint after switching.
- [ ] `[PRIV-BASE:P0.10][AI]` Prove the before/after working-overlay fingerprints are equal.
- [ ] `[PRIV-BASE:P0.11][AI]` Run `npm install`; retain its exact exit state.
- [ ] `[PRIV-BASE:P0.12][AI]` Run plain `npm run doctor`; retain its exact exit state.
- [ ] `[PRIV-BASE:P0.13][AI]` Run the private pre-push surface; retain its exact exit state.
- [ ] `[PRIV-BASE:P0.14][AI]` Classify the result as clean, evidenced non-overlay, overlay-owned, or ambiguous.
- [ ] `[PRIV-BASE:P0.15][AI]` Reject ordinary-unit attribution and keep the public obligation pending.
- [ ] `[PRIV-BASE:P0.16][AI]` Record exactly one authorized successor or the ambiguity stop with no successor.
- [ ] `[PRIV-BASE:P0.17][AI]` Record PRIV-REPAIR as reasoned `N/A` unless evidenced non-overlay failure authorizes it.
- [ ] `[PRIV-BASE:P0.G][AI]` Pass exactly one terminal current-main/overlay/baseline/dependency gate.
- [ ] `[PRIV-BASE:P0.P][AI]` Record result, overlay hash, predecessor pin, one successor, and recheck command.

### PRIV-REPAIR — Conditional Overlay-Safe Private Baseline Repair

- [ ] `[PRIV-REPAIR:P1.01][AI]` Name the failed command and retain its private-safe baseline evidence.
- [ ] `[PRIV-REPAIR:P1.02][AI]` Verify the pending public obligation and exact PUB-IDEAS pin.
- [ ] `[PRIV-REPAIR:P1.03][AI]` Identify the first bad private pin, root-cause owner, and bounded branch slug.
- [ ] `[PRIV-REPAIR:P1.04][AI]` Compute the literal raw working-overlay fingerprint before switching.
- [ ] `[PRIV-REPAIR:P1.05][AI]` Fetch current private `origin/main` and record its SHA.
- [ ] `[PRIV-REPAIR:P1.06][AI]` Enter only the declared repair branch without stashing the overlay.
- [ ] `[PRIV-REPAIR:P1.07][AI]` Prove repair `HEAD == origin/main` before editing.
- [ ] `[PRIV-REPAIR:P1.08][AI]` Recompute the literal raw working-overlay fingerprint after switching.
- [ ] `[PRIV-REPAIR:P1.09][AI]` Prove the before/after working-overlay fingerprints are equal.
- [ ] `[PRIV-REPAIR:P1.10][AI]` Publish exact non-overlay repair paths and the two overlay exclusions.
- [ ] `[PRIV-REPAIR:P1.11][AI]` Publish forecast, stable-main safety, risk, rollback, and preserved hash.
- [ ] `[PRIV-REPAIR:P1.12][AI]` Reproduce the original failure before editing; retain the diagnostic.
- [ ] `[PRIV-REPAIR:P1.13][AI]` Edit only proven non-overlay paths.
- [ ] `[PRIV-REPAIR:P1.14][AI]` Recompute and match the working-overlay fingerprint after editing.
- [ ] `[PRIV-REPAIR:P1.G][AI]` Pass branch/base/pin/scope/ledger/forecast/overlay gate.
- [ ] `[PRIV-REPAIR:P1.P][AI]` Record head, ledger, overlay hash, and reproduction command.
- [ ] `[PRIV-REPAIR:P2.01][AI]` Run the focused regression; retain expected and actual results.
- [ ] `[PRIV-REPAIR:P2.02][AI]` Rerun the original failing baseline command; require success.
- [ ] `[PRIV-REPAIR:P2.03][AI]` Run every applicable private local gate; retain each exit state.
- [ ] `[PRIV-REPAIR:P2.04][AI]` Run the private pre-push surface; retain its exit state.
- [ ] `[PRIV-REPAIR:P2.05][AI]` Calculate actual hand-authored changed lines and files.
- [ ] `[PRIV-REPAIR:P2.06][AI]` Gate both actual counts against the plan's caps before staging.
- [ ] `[PRIV-REPAIR:P2.07][AI]` Reconcile non-overlay working paths exactly to the repair ledger.
- [ ] `[PRIV-REPAIR:P2.08][AI]` Stage only the admitted non-overlay repair ledger.
- [ ] `[PRIV-REPAIR:P2.09][AI]` Read cached paths and prove staged-ledger equality.
- [ ] `[PRIV-REPAIR:P2.10][AI]` Inspect cached check, statistics, and complete private-safe patch.
- [ ] `[PRIV-REPAIR:P2.11][AI]` Prove the authorized overlay is absent from the cached repair diff.
- [ ] `[PRIV-REPAIR:P2.12][AI]` Commit one cohesive non-overlay baseline repair.
- [ ] `[PRIV-REPAIR:P2.13][AI]` Read the complete committed repair diff.
- [ ] `[PRIV-REPAIR:P2.14][AI]` Recompute and match the literal working-overlay fingerprint.
- [ ] `[PRIV-REPAIR:P2.G][AI]` Pass acceptance/size/staging/commit/overlay gate.
- [ ] `[PRIV-REPAIR:P2.P][AI]` Record local head, overlay hash, and intended residue.
- [ ] `[PRIV-REPAIR:P3.01][AI]` Recalculate committed hand-authored line/file counts.
- [ ] `[PRIV-REPAIR:P3.02][AI]` Gate the committed counts against both caps.
- [ ] `[PRIV-REPAIR:P3.03][AI]` Rerun the private pre-push surface on committed head.
- [ ] `[PRIV-REPAIR:P3.04][AI]` Push only the declared private repair branch.
- [ ] `[PRIV-REPAIR:P3.05][AI]` Read back and match the remote branch head to local `HEAD`.
- [ ] `[PRIV-REPAIR:P3.06][AI]` Open one private-safe draft PR from a literal AI-marked body.
- [ ] `[PRIV-REPAIR:P3.07][AI]` Read back boundary, body, marker, and safe statistics.
- [ ] `[PRIV-REPAIR:P3.G][AI]` Pass push/remote-head/private-safe-body/readback gate.
- [ ] `[PRIV-REPAIR:P3.P][AI]` Record draft URL, current head, body path, and overlay hash.
- [ ] `[PRIV-REPAIR:P4.01][AI]` Post the exact-head private-safe route and selected/skipped review lenses.
- [ ] `[PRIV-REPAIR:P4.02][AI]` Read back route, frozen scope, changed probe, and AI marker.
- [ ] `[PRIV-REPAIR:P4.03][AI]` Run successive exact-head cycles under the five-cycle boundary.
- [ ] `[PRIV-REPAIR:P4.04][AI]` Classify each concern before any cross-repository handoff.
- [ ] `[PRIV-REPAIR:P4.05][AI]` Keep local adaptations, deviations, and unrelated follow-ups out of public correction.
- [ ] `[PRIV-REPAIR:P4.06][AI]` For a proven portable or plan defect, record the paused private head; freeze push, review, readiness, and merge; then hand the required replacement public or amended-plan pin only to ADAPTERS.
- [ ] `[PRIV-REPAIR:P4.07][AI]` Gate P4.08–P4.16 to the no-handoff path or an ADAPTERS-recorded replacement pin and resumption; record every finding as fix, reject, defer, or clarify with evidence.
- [ ] `[PRIV-REPAIR:P4.08][AI]` Push each bounded fix before claiming it in the native thread.
- [ ] `[PRIV-REPAIR:P4.09][AI]` Invalidate every review and CI result from the superseded head.
- [ ] `[PRIV-REPAIR:P4.10][AI]` Return the repaired head to P4.03 before thread resolution.
- [ ] `[PRIV-REPAIR:P4.11][AI]` Reply in the original thread with current-head evidence.
- [ ] `[PRIV-REPAIR:P4.12][AI]` Read back the persisted reply and its AI marker.
- [ ] `[PRIV-REPAIR:P4.13][AI]` Resolve only threads whose terminal evidence is true.
- [ ] `[PRIV-REPAIR:P4.14][AI]` Poll applicable current-head CI exactly every 120 seconds.
- [ ] `[PRIV-REPAIR:P4.15][AI]` Recompute and match the literal working-overlay fingerprint.
- [ ] `[PRIV-REPAIR:P4.16][AI]` Prove readiness, mark ready, and read back the same current head.
- [ ] `[PRIV-REPAIR:P4.G][AI]` Pass semantic-exit/CI/frozen-scope/firewall/overlay readiness gate.
- [ ] `[PRIV-REPAIR:P4.P][AI]` Record head, cycles, threads, CI, overlay hash, and obligation state.
- [ ] `[PRIV-REPAIR:P5.01][AI]` Recheck route completion and zero unresolved blocker findings.
- [ ] `[PRIV-REPAIR:P5.02][AI]` Recheck current base, reviewed head, ready state, and green CI.
- [ ] `[PRIV-REPAIR:P5.03][AI]` Run `/usr/bin/git diff --binary <current-main> <reviewed-head> | /usr/bin/shasum -a 256`.
- [ ] `[PRIV-REPAIR:P5.04][AI]` Squash-merge by repository-qualified GitHub API.
- [ ] `[PRIV-REPAIR:P5.05][AI]` Read back the immutable merge SHA and landed non-overlay ledger.
- [ ] `[PRIV-REPAIR:P5.06][AI]` Run `/usr/bin/git diff --binary <merge-sha>^1 <merge-sha> | /usr/bin/shasum -a 256`.
- [ ] `[PRIV-REPAIR:P5.07][AI]` Prove reviewed and landed fingerprints are equal.
- [ ] `[PRIV-REPAIR:P5.08][AI]` Fetch private `origin/main` after the merge.
- [ ] `[PRIV-REPAIR:P5.09][AI]` Prove fetched `origin/main` equals the merge SHA.
- [ ] `[PRIV-REPAIR:P5.10][AI]` Resync this private worktree without stashing the overlay.
- [ ] `[PRIV-REPAIR:P5.11][AI]` Recompute and match the literal working-overlay fingerprint.
- [ ] `[PRIV-REPAIR:P5.12][AI]` Run `npm install` on landed private main.
- [ ] `[PRIV-REPAIR:P5.13][AI]` Run plain `npm run doctor` on landed private main.
- [ ] `[PRIV-REPAIR:P5.14][AI]` Run the literal private pre-push command on landed private main.
- [ ] `[PRIV-REPAIR:P5.15][AI]` Classify and record exactly one outcome: a clean landed repair authorizes PRIV-IDEAS; an evidenced failed recheck keeps PRIV-IDEAS frozen and names only its bounded new repair or human-escalation path; ambiguity names no successor, keeps PRIV-IDEAS frozen, and stops for human judgment.
- [ ] `[PRIV-REPAIR:P5.G][AI]` Pass merge/landed/fingerprint/resync/baseline/overlay/successor gate.
- [ ] `[PRIV-REPAIR:P5.P][AI]` Record merge/main SHA, overlay hash, result, and named-successor command.

### PRIV-IDEAS — Preserve the Overlay and Retire Its One Source

Entry accepts only a terminal baseline/repair proof naming PRIV-IDEAS. Cross-repo byte identity is
`N/A` for these idea paths; semantic retirement is proved against the disposition map. Before
staging, every index hunk must belong to retirement/index maintenance or remain excluded residue.

- [ ] `[PRIV-IDEAS:P1.01][AI]` Verify the terminal private proof names PRIV-IDEAS and reject every other successor.
- [ ] `[PRIV-IDEAS:P1.02][AI]` Read back the exact pending public obligation and activated-plan pin.
- [ ] `[PRIV-IDEAS:P1.03][AI]` Fetch current private `origin/main`.
- [ ] `[PRIV-IDEAS:P1.04][AI]` Prove fetched `origin/main` equals the predecessor pin.
- [ ] `[PRIV-IDEAS:P1.05][AI]` Compute the literal raw working-overlay fingerprint before branching.
- [ ] `[PRIV-IDEAS:P1.06][AI]` Enter `optimize-pr-process-priv-ideas` without stashing.
- [ ] `[PRIV-IDEAS:P1.07][AI]` Prove branch `HEAD` equals current private `origin/main`.
- [ ] `[PRIV-IDEAS:P1.08][AI]` Recompute and match the literal working-overlay fingerprint.
- [ ] `[PRIV-IDEAS:P1.09][AI]` Prove status contains only the admitted two-path overlay.
- [ ] `[PRIV-IDEAS:P1.10][AI]` Publish ledger, forecast, dormant safety, risk, and rollback.
- [ ] `[PRIV-IDEAS:P1.11][AI]` Record propagation, bindings, and cross-repo byte identity as reasoned `N/A`.
- [ ] `[PRIV-IDEAS:P1.12][AI]` Revalidate the private disposition against the activated plan pin.
- [ ] `[PRIV-IDEAS:P1.13][AI]` Run literal predecessor acceptance for the mapped private row.
- [ ] `[PRIV-IDEAS:P1.14][AI]` Attribute every index hunk to retirement maintenance or excluded residue.
- [ ] `[PRIV-IDEAS:P1.G][AI]` Pass pin/scope/size/ledger/overlay/disposition/provenance gate.
- [ ] `[PRIV-IDEAS:P1.P][AI]` Record branch, head, ledger, original hash, and safe negative reads.
- [ ] `[PRIV-IDEAS:P2.01][AI]` Run reviewed-worktree acceptance before staging.
- [ ] `[PRIV-IDEAS:P2.02][AI]` Run private Markdown formatting and lint checks.
- [ ] `[PRIV-IDEAS:P2.03][AI]` Run the private pre-push surface.
- [ ] `[PRIV-IDEAS:P2.04][AI]` Calculate actual hand-authored changed lines and files.
- [ ] `[PRIV-IDEAS:P2.05][AI]` Gate both actual counts against the plan's caps.
- [ ] `[PRIV-IDEAS:P2.06][AI]` Compute the literal raw working-overlay fingerprint.
- [ ] `[PRIV-IDEAS:P2.07][AI]` Stage only the authorized two-path content.
- [ ] `[PRIV-IDEAS:P2.08][AI]` Read cached paths and prove staged-ledger equality.
- [ ] `[PRIV-IDEAS:P2.09][AI]` Compute the literal raw cached-overlay fingerprint.
- [ ] `[PRIV-IDEAS:P2.10][AI]` Prove cached and original working-overlay fingerprints are equal.
- [ ] `[PRIV-IDEAS:P2.11][AI]` Inspect cached check, statistics, and complete private-safe patch.
- [ ] `[PRIV-IDEAS:P2.12][AI]` Commit the cohesive private retirement without rewriting its bytes.
- [ ] `[PRIV-IDEAS:P2.13][AI]` Read the complete committed diff.
- [ ] `[PRIV-IDEAS:P2.14][AI]` Compute the literal raw `<unit-base>..HEAD` overlay fingerprint.
- [ ] `[PRIV-IDEAS:P2.15][AI]` Prove committed and original working-overlay fingerprints are equal.
- [ ] `[PRIV-IDEAS:P2.16][AI]` Rerun reviewed-head acceptance after commit.
- [ ] `[PRIV-IDEAS:P2.G][AI]` Pass acceptance/gates/size/staging/commit/three-state fingerprint gate.
- [ ] `[PRIV-IDEAS:P2.P][AI]` Record local head, committed hash, and clean tree or authorized residue.
- [ ] `[PRIV-IDEAS:P3.01][AI]` Recalculate committed hand-authored counts.
- [ ] `[PRIV-IDEAS:P3.02][AI]` Gate committed counts against the plan's caps.
- [ ] `[PRIV-IDEAS:P3.03][AI]` Rerun the private pre-push surface on committed head.
- [ ] `[PRIV-IDEAS:P3.04][AI]` Push only `optimize-pr-process-priv-ideas`.
- [ ] `[PRIV-IDEAS:P3.05][AI]` Read back and match remote branch head to local `HEAD`.
- [ ] `[PRIV-IDEAS:P3.06][AI]` Rerun reviewed-head acceptance after push.
- [ ] `[PRIV-IDEAS:P3.07][AI]` Open one private-safe draft PR from a literal AI-marked body.
- [ ] `[PRIV-IDEAS:P3.08][AI]` Read back base, head, draft, body, marker, and safe statistics.
- [ ] `[PRIV-IDEAS:P3.G][AI]` Pass push/remote-head/acceptance/private-safe-body/readback gate.
- [ ] `[PRIV-IDEAS:P3.P][AI]` Record draft URL, current head, and literal body path.
- [ ] `[PRIV-IDEAS:P4.01][AI]` Post the exact-head private-safe route and selected/skipped review lenses.
- [ ] `[PRIV-IDEAS:P4.02][AI]` Read back route, frozen scope, changed probe, and AI marker.
- [ ] `[PRIV-IDEAS:P4.03][AI]` Run successive exact-head cycles under the five-cycle boundary.
- [ ] `[PRIV-IDEAS:P4.04][AI]` Classify each concern before any cross-repository handoff.
- [ ] `[PRIV-IDEAS:P4.05][AI]` For a proven portable or plan defect, record the paused private head; freeze push, review, readiness, and merge; then hand the required replacement public or amended-plan pin only to ADAPTERS.
- [ ] `[PRIV-IDEAS:P4.06][AI]` Gate P4.07–P4.14 to the no-handoff path or an ADAPTERS-recorded replacement pin and resumption; record every finding as fix, reject, defer, or clarify with evidence.
- [ ] `[PRIV-IDEAS:P4.07][AI]` Push each bounded fix before claiming it in the native thread.
- [ ] `[PRIV-IDEAS:P4.08][AI]` Invalidate every review and CI result from the superseded head.
- [ ] `[PRIV-IDEAS:P4.09][AI]` Return the repaired head to P4.03 before thread resolution.
- [ ] `[PRIV-IDEAS:P4.10][AI]` Reply in the original thread with current-head evidence.
- [ ] `[PRIV-IDEAS:P4.11][AI]` Read back the persisted reply and its AI marker.
- [ ] `[PRIV-IDEAS:P4.12][AI]` Resolve only threads whose terminal evidence is true.
- [ ] `[PRIV-IDEAS:P4.13][AI]` Poll applicable current-head CI exactly every 120 seconds.
- [ ] `[PRIV-IDEAS:P4.14][AI]` Prove readiness, mark ready, and read back the same current head.
- [ ] `[PRIV-IDEAS:P4.G][AI]` Pass semantic-exit/current-head-CI/frozen-scope/firewall/obligation gate.
- [ ] `[PRIV-IDEAS:P4.P][AI]` Record head, cycles, threads, CI, and obligation state.
- [ ] `[PRIV-IDEAS:P5.01][AI]` Recheck route, findings, base, head, ready state, and green CI.
- [ ] `[PRIV-IDEAS:P5.02][AI]` Run `/usr/bin/git diff --binary <current-main> <reviewed-head> | /usr/bin/shasum -a 256`.
- [ ] `[PRIV-IDEAS:P5.03][AI]` Squash-merge by repository-qualified GitHub API.
- [ ] `[PRIV-IDEAS:P5.04][AI]` Read back merge SHA and landed two-path ledger.
- [ ] `[PRIV-IDEAS:P5.05][AI]` Run `/usr/bin/git diff --binary <merge-sha>^1 <merge-sha> | /usr/bin/shasum -a 256`.
- [ ] `[PRIV-IDEAS:P5.06][AI]` Prove reviewed and landed fingerprints are equal.
- [ ] `[PRIV-IDEAS:P5.07][AI]` Publish exactly one terminal obligation state from a literal AI-marked payload.
- [ ] `[PRIV-IDEAS:P5.08][AI]` Read back terminal state, immutable private pin, owner, reason/action, and AI marker.
- [ ] `[PRIV-IDEAS:P5.09][AI]` Fetch private `origin/main` after the merge.
- [ ] `[PRIV-IDEAS:P5.10][AI]` Prove fetched `origin/main` equals the merge pin.
- [ ] `[PRIV-IDEAS:P5.11][AI]` Resync this private worktree without stashing the overlay.
- [ ] `[PRIV-IDEAS:P5.12][AI]` Authorize only PUB-A1 from the resynced landed main.
- [ ] `[PRIV-IDEAS:P5.G][AI]` Pass merge/landed/fingerprint/obligation/resync/sibling gate.
- [ ] `[PRIV-IDEAS:P5.P][AI]` Record private merge/main SHA, terminal obligation, and PUB-A1 command.

### WAVES-ENTRY-PRIVATE Finding State

PR #263 fixed the baseline/repair checklist at `339f464e4aca08e29a93a844e2c194c358d52a94`. This
slice owns the overlay-safe private-idea unit and keeps F-035 partial. ENTRY-ADAPTERS must still
instantiate the freeze/replacement/abandonment/rollback transitions, record all four ENTRY pins,
and close the ENTRY gate.

### ENTRY-ADAPTERS — Bounded Cross-Repository Correction and Amendment

One native obligation is the public record for one active public/private pair. Before public merge,
its public PR carries a **prepared** note with the reviewed head, rule class, expected private paths,
safe public summary, owner, stable `defect-lineage-id`, and `correction-count: 0`; after merge it
becomes **pending-private** by adding the immutable merge SHA and private entry command. It never
copies private patch content. Supersession, relabeling, or late discovery of the same root cause
retains both the lineage ID and its correction count.

| Event                          | Required pair state                   | What remains frozen                  | Terminal evidence                    |
| ------------------------------ | ------------------------------------- | ------------------------------------ | ------------------------------------ |
| Unrelated private-main advance | pending-private after base inspection | no pair work                         | inspection and current private pin   |
| Compatible public follow-up    | pending-private                       | no private churn                     | public note and unchanged obligation |
| Portable/plan defect           | correction-pending                    | paused private PR and all successors | replacement public/amendment pin     |
| Second reversal                | human-stop                            | pair and successors                  | human-readable escalation            |
| Completed pair, late defect    | sealed                                | completed pair stays closed          | linked repair retaining lineage      |

- [ ] `[ENTRY-ADAPTERS:A1.01][AI]` Before allocating a defect-lineage ID, compare candidate root cause read-only against sealed/correction-pending native records and record compared URLs and evidence. A no-match allocates count 0; one unambiguous match reuses its exact ID/current count; ambiguity freezes the pair, records only comparison and human escalation, and ambiguity stops without a prepared obligation. Only the first two outcomes record the prepared obligation.
- [ ] `[ENTRY-ADAPTERS:A1.02][AI]` After merge, update that same note to pending-private with immutable merge SHA, landed fingerprint, and literal private entry command.
- [ ] `[ENTRY-ADAPTERS:A1.03][AI]` Prove only one public/private pair is active and freeze every later pair before private work starts.
- [ ] `[ENTRY-ADAPTERS:A1.04][AI]` On unrelated private-main advance, inspect the full base delta, record the new private pin, rerun affected checks, and keep the obligation pending-private.
- [ ] `[ENTRY-ADAPTERS:A1.05][AI]` On a compatible public follow-up, record nonblocking compatibility without creating private churn or replacing the obligation.
- [ ] `[ENTRY-ADAPTERS:A1.06][AI]` Classify a private finding as local adaptation, reasoned deviation, unrelated follow-up, portable defect, or plan defect before any handoff.
- [ ] `[ENTRY-ADAPTERS:A1.07][AI]` For a portable or plan defect, freeze the paused private PR's push, review, readiness, merge, and successors; record its exact head and cited defect boundary.
- [ ] `[ENTRY-ADAPTERS:A1.08][AI]` Before any replacement PR, read the original obligation and write `correction-kind: correction` or `correction-kind: plan-amendment` in its same native record. Acceptance: this existing lineage has reconciled `correction-count: 0`, one cited portable/plan defect, and no other pair becomes active; at count 1 neither replacement type may start.
- [ ] `[ENTRY-ADAPTERS:A1.09][AI]` Keep the originating private review thread unresolved; reply there with the replacement pin, frozen state, and resumption condition.
- [ ] `[ENTRY-ADAPTERS:A1.10][AI]` Supersede the old obligation in its original native note; preserve lineage ID, `correction-kind`, and the `0 → 1` correction count, and create no second obligation for the same pair. Acceptance: a PR reader can trace original pin, replacement pin, paused private head, and resumption condition from that note alone.
- [ ] `[ENTRY-ADAPTERS:A1.11][AI]` Treat the correction PR as its own bounded review, while the resumed private PR retains—not resets—its existing Cycle 1–5 count.
- [ ] `[ENTRY-ADAPTERS:A1.12][AI]` Stop before a second public reversal, leave a human-readable escalation, and preserve the frozen pair and original thread.
- [ ] `[ENTRY-ADAPTERS:A1.13][AI]` Resume only after the named replacement pin is merged, inspected, and recorded in the original obligation and private thread.
- [ ] `[ENTRY-ADAPTERS:A1.14][AI]` Close a pair only with a terminal `satisfied`, `reasoned-deviation`, or `N/A` state, exact public/private pins, and evidence links.
- [ ] `[ENTRY-ADAPTERS:A1.15][AI]` Seal the terminal pair in its native record; a later defect opens a linked repair pair without reopening the sealed pair, but the same root cause retains its lineage ID and cannot reset the shared correction budget across either `correction-kind`.
- [ ] `[ENTRY-ADAPTERS:A1.16][AI]` Use only disclosure-safe public summaries and links; retain private task evidence solely in the private PR artifact.
- [ ] `[ENTRY-ADAPTERS:A1.17][AI]` For this public control plan, record the explicit override of the legacy per-repo/three-grill and iterative formal-gate composite: one control plan, one bounded equivalence audit, and no separate post-plan grill.
- [ ] `[ENTRY-ADAPTERS:A1.18][AI]` Instantiate the sole `PLAN-AMENDMENT` route with exact superseded section/pin, frozen units, single-purpose scope, and resumption pin.
- [ ] `[ENTRY-ADAPTERS:A1.G][AI]` Pass pair-state, freeze, replacement, cycle-budget, disclosure, terminal-seal, and amendment gate.
- [ ] `[ENTRY-ADAPTERS:A1.P][AI]` Record pair URL, prepared/pending/terminal state, pins, correction count, private-thread URL, and named successor.

## Dormant A-Wave Checklist

### A/Rules Atomic Execution References

Every A/Rules checkbox below is one atomic state transition, not optional background. Before a row
uses an `AR-*` reference, its unit heading declares a literal `UNIT`, `REPO`, `BRANCH`, and
`RECORD` in the parameter table below. Write the resolved values and the exact admitted source paths
to that `RECORD`, read it back with `sed -n '1,$p' "$RECORD"`, and stop if a required value is blank.
`RECORD` is local preparation only; the same resolved values and read-back result must appear in the
unit's PR route/reply artifact before the associated gate passes.

| Unit    | `REPO`                   | `BRANCH`                      | `RECORD`                                          |
| ------- | ------------------------ | ----------------------------- | ------------------------------------------------- |
| PUB-A1  | `wahidyankf/ose-public`  | `optimize-pr-process-pub-a1`  | `local-tmp/optimize-pr-process/pub-a1-record.md`  |
| PRIV-A1 | `wahidyankf/ose-private` | `optimize-pr-process-priv-a1` | `local-tmp/optimize-pr-process/priv-a1-record.md` |
| PUB-A2  | `wahidyankf/ose-public`  | `optimize-pr-process-pub-a2`  | `local-tmp/optimize-pr-process/pub-a2-record.md`  |
| PRIV-A2 | `wahidyankf/ose-private` | `optimize-pr-process-priv-a2` | `local-tmp/optimize-pr-process/priv-a2-record.md` |
| PUB-A3  | `wahidyankf/ose-public`  | `optimize-pr-process-pub-a3`  | `local-tmp/optimize-pr-process/pub-a3-record.md`  |
| PRIV-A3 | `wahidyankf/ose-private` | `optimize-pr-process-priv-a3` | `local-tmp/optimize-pr-process/priv-a3-record.md` |
| PUB-B   | `wahidyankf/ose-public`  | `optimize-pr-process-pub-b`   | `local-tmp/optimize-pr-process/pub-b-record.md`   |
| PRIV-B  | `wahidyankf/ose-private` | `optimize-pr-process-priv-b`  | `local-tmp/optimize-pr-process/priv-b-record.md`  |
| PUB-C   | `wahidyankf/ose-public`  | `optimize-pr-process-pub-c`   | `local-tmp/optimize-pr-process/pub-c-record.md`   |
| PRIV-C  | `wahidyankf/ose-private` | `optimize-pr-process-priv-c`  | `local-tmp/optimize-pr-process/priv-c-record.md`  |

| Reference        | Exact input, command, and output record                                                                                                                                                                                                                                                                                                                                                                                                 | Pass/fail condition                                                                                                                                                                                          |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `AR-ENTRY`       | Input: the unit's literal `RECORD` with predecessor pin, amendment URL, exact admitted paths, and cap forecast. Run `git fetch origin main && git status --short --branch && git worktree list --porcelain && git branch --show-current && git rev-parse HEAD && git rev-parse origin/main`. Output: the resolved values plus command output in `RECORD`.                                                                               | `RECORD` names one predecessor, one exact source set already admitted by a merged amendment, and `HEAD` equals `origin/main` before edit; missing admission or a nonzero command fails and freezes the unit. |
| `AR-PROPAGATE`   | Input: `RECORD`'s exact normalized rules and admitted source paths. Read `repo-governance/workflows/repo/repo-rules-propagation.md`, invoke it with `mode=strict` and `isolation=current`, then write its `generated-reports/repo-rules-propagation__*__manifest.md` path and sibling obligation URL into `RECORD`.                                                                                                                     | The read-back manifest names only the pre-admitted paths and owners. A new path is fail/stop for a plan amendment, not permission to edit it.                                                                |
| `AR-BIND`        | Input: exact hand-authored paths in `RECORD`. Run `npm run generate:bindings && npm run validate:sync && npm run generate:bindings && git status --short`; append source/generated path sets and output to `RECORD`.                                                                                                                                                                                                                    | All commands exit 0; second generation has no tracked change and no generated file was hand-edited.                                                                                                          |
| `AR-LOCAL`       | Input: unit acceptance commands and hand-authored paths in `RECORD`. Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`, `git diff --numstat "$UNIT_BASE" -- $HAND_AUTHORED_PATHS \| awk '{a+=$1; d+=$2} END {print a+d}'`, and `git diff --name-only "$UNIT_BASE" -- $HAND_AUTHORED_PATHS \| wc -l`; append each result to `RECORD`.                                                                                | Gate exits 0 or the record has an explicit reasoned `N/A`; size is at most 400 lines and 20 files.                                                                                                           |
| `AR-STAGE`       | Input: admitted path list in `RECORD`. Run `git add -- $ADMITTED_PATHS && git diff --cached --name-only && git diff --cached --check && git diff --cached --stat && git diff --cached --patch`; record cached paths and full-diff read-back in `RECORD`.                                                                                                                                                                                | Cached paths equal the admitted list in both directions, check exits 0, and one cohesive commit is created/read.                                                                                             |
| `AR-PUSH`        | Input: literal `REPO`, `BRANCH`, and local `HEAD` in `RECORD`. Run `git push --set-upstream origin "$BRANCH" && git ls-remote origin "refs/heads/$BRANCH"`; append both SHAs to `RECORD`.                                                                                                                                                                                                                                               | Remote SHA equals local `HEAD`; no other branch is pushed.                                                                                                                                                   |
| `AR-DRAFT`       | Input: literal AI-marked body at `local-tmp/optimize-pr-process/$UNIT-pr-body.md`, plus `REPO`/`BRANCH` in `RECORD`. Run `gh pr create --repo "$REPO" --draft --base main --head "$BRANCH" --title "<resolved-title>" --body-file "local-tmp/optimize-pr-process/$UNIT-pr-body.md"` then `gh pr view --repo "$REPO" --json url,isDraft,baseRefOid,headRefOid,body,additions,deletions,changedFiles`; copy read-back JSON into `RECORD`. | Exactly one draft has the resolved base/head, readable body ending `Generated by AI`, and separately recorded whole-PR totals.                                                                               |
| `AR-ROUTE`       | Input: PR URL/current head and literal route payload path in `RECORD`. Post the reviewed payload with `gh pr comment --repo "$REPO" --body-file "$ROUTE_PAYLOAD"`, then run `gh pr view --repo "$REPO" --comments`; append the returned comment URL/head to `RECORD`.                                                                                                                                                                   | The read-back route names classification, frozen scope, selected/skipped lenses, changed probe, and `Generated by AI`; a mismatch fails before review starts.                                                |
| `AR-REVIEW`      | Input: route URL/current head in `RECORD`. Invoke the selected review cycle once, then read its consolidated review with `gh pr view --repo "$REPO" --json reviews`; append cycle number, review URL, and finding IDs to `RECORD`.                                                                                                                                                                                                      | One current-head cycle is recorded; target is Cycles 1–3, cycles 4–5 require a new probe/failure-family record, and Cycle 6 is never started.                                                                |
| `AR-REPLY`       | Input: each finding's native thread URL and disposition evidence in `RECORD`. For each fix/reject/defer/clarify, post a literal AI-marked same-thread reply and read it back with `gh pr view --repo "$REPO" --comments`; append reply URL, current head, and terminal state to `RECORD`.                                                                                                                                               | Every finding has exactly one evidence-backed disposition; only a true terminal record is resolved and a fix cites a pushed SHA.                                                                             |
| `AR-CI`          | Input: current head and PR URL in `RECORD`. Run `gh pr checks --repo "$REPO" --required` after each changed head, at 120-second intervals while pending; append timestamp, head, and result to `RECORD`.                                                                                                                                                                                                                                | Required/current-head checks are green; a push invalidates earlier CI entries and a failure returns to the review route.                                                                                     |
| `AR-READY`       | Input: route, thread, CI, and branch-current evidence in `RECORD`. Run `gh pr ready --repo "$REPO"` then `gh pr view --repo "$REPO" --json isDraft,headRefOid,mergeStateStatus,statusCheckRollup`; append JSON to `RECORD`.                                                                                                                                                                                                             | All five readiness preconditions are listed against the same head and `isDraft` is `false`.                                                                                                                  |
| `AR-FINGERPRINT` | Input: `CURRENT_MAIN` and reviewed head recorded in `RECORD`. Run `/usr/bin/git diff --binary "$CURRENT_MAIN" "$REVIEWED_HEAD" \| /usr/bin/shasum -a 256`; append the hash to `RECORD`.                                                                                                                                                                                                                                                 | The reviewed-patch hash is present before merge; an unreadable/mismatched head fails.                                                                                                                        |
| `AR-MERGE`       | Input: ready PR URL and zero-unresolved finding/thread evidence in `RECORD`. Run `gh pr merge --repo "$REPO" --squash` then `gh pr view --repo "$REPO" --json mergeCommit,mergedAt,state,headRefOid`; append JSON to `RECORD`.                                                                                                                                                                                                          | The PR is merged once under its existing merge gate; no merge-step wording or authority is changed by this reference.                                                                                        |
| `AR-LANDED`      | Input: merge SHA from `RECORD`. Run `/usr/bin/git diff --binary "$MERGE_SHA^1" "$MERGE_SHA" \| /usr/bin/shasum -a 256`; append the landed hash to `RECORD`.                                                                                                                                                                                                                                                                             | Landed and reviewed hashes match exactly; inequality stops the unit.                                                                                                                                         |
| `AR-RESYNC`      | Input: merge SHA and literal successor state in `RECORD`. Run `git fetch origin main && test "$(git rev-parse origin/main)" = "$MERGE_SHA" && git status --short --branch`; append output and sibling-obligation URL/state to `RECORD`.                                                                                                                                                                                                 | `origin/main` equals the merge, the same worktree is clean or has only named private overlay, and exactly one successor/terminal state is published.                                                         |

### PUB-A1 — Plan-Making Rules

- [ ] `[PUB-A1:P1.01][AI]` Execute `AR-ENTRY` for the `A1 public/private` row in `tech-docs.md`; read the terminal PRIV-IDEAS obligation and record its exact predecessor pin. Acceptance: current public `origin/main` contains that pin.
- [ ] `[PUB-A1:P1.02][AI]` Run only `AR-PROPAGATE` for normalized plan-making rules. Acceptance: the strict manifest names the authoritative source, consumer, and private sibling obligation.
- [ ] `[PUB-A1:P1.03][AI]` Edit only public paths listed in the `AR-PROPAGATE` manifest. Acceptance: `git status --short` contains no unlisted path.
- [ ] `[PUB-A1:P1.04][AI]` Run only `AR-BIND`. Acceptance: generated paths and second-generation stability are recorded separately from source paths.
- [ ] `[PUB-A1:P2.01][AI]` Run only `AR-LOCAL`. Acceptance: each unit gate has its exit result or recorded reasoned `N/A`.
- [ ] `[PUB-A1:P2.02][AI]` Run only `AR-STAGE`. Acceptance: the cached ledger is exactly the before-ledger and one cohesive commit is read in full.
- [ ] `[PUB-A1:P3.01][AI]` Run only `AR-DRAFT`. Acceptance: the public draft body is readable, exact-head, and AI-marked.
- [ ] `[PUB-A1:P4.01][AI]` Run only `AR-ROUTE` with `UNIT=pub-a1` and `RECORD=local-tmp/optimize-pr-process/pub-a1-record.md`. Acceptance: its read-back route is frozen before reviewer work.
- [ ] `[PUB-A1:P4.02][AI]` Run only `AR-REVIEW` with that same resolved record. Acceptance: the consolidated review URL, cycle, and changed probe are read back.
- [ ] `[PUB-A1:P4.03][AI]` Run only `AR-REPLY` with that same resolved record. Acceptance: every finding has a same-thread, AI-marked evidence disposition.
- [ ] `[PUB-A1:P4.04][AI]` Run only `AR-CI` with that same resolved record. Acceptance: the stored check result is green for the current head.
- [ ] `[PUB-A1:P4.05][AI]` Run only `AR-READY` with that same resolved record. Acceptance: the read-back is non-draft after all five preconditions.
- [ ] `[PUB-A1:P5.01][AI]` Run only `AR-FINGERPRINT` with `UNIT=pub-a1`. Acceptance: the reviewed-patch hash is stored before merge.
- [ ] `[PUB-A1:P5.02][AI]` Run only `AR-MERGE` with the ready public PR record. Acceptance: the existing merge gate is satisfied and merge JSON is stored.
- [ ] `[PUB-A1:P5.03][AI]` Run only `AR-LANDED` with the merge SHA. Acceptance: the landed hash matches P5.01.
- [ ] `[PUB-A1:P5.04][AI]` Run only `AR-RESYNC` with the same record. Acceptance: `origin/main` equals the merge and the prepared PRIV-A1 obligation identifies the exact successor.
- [ ] `[PUB-A1:P1.G][AI]` Pass propagated-rule, binding, current-head, sibling-obligation, and landed-proof gate.
- [ ] `[PUB-A1:P1.P][AI]` Record public merge pin and prepared PRIV-A1 obligation.

### PRIV-A1 — Private Plan-Making Adaptation

- [ ] `[PRIV-A1:P1.01][AI]` Execute `AR-ENTRY` in the declared private worktree and read the PUB-A1 immutable obligation. Acceptance: the authorized overlay fingerprint is recorded before branch entry and the public merge pin is the predecessor.
- [ ] `[PRIV-A1:P1.02][AI]` Classify the private destination as satisfied, reasoned deviation, `N/A`, or portable defect before editing. Acceptance: the private PR artifact contains one class and supporting private-safe evidence.
- [ ] `[PRIV-A1:P1.03][AI]` Run only `AR-PROPAGATE` for the admitted private semantic counterpart. Acceptance: the manifest and sibling record exclude the authorized overlay.
- [ ] `[PRIV-A1:P1.04][AI]` Edit only manifest-admitted private source paths. Acceptance: private evidence remains in the private PR and `git status --short` excludes the overlay.
- [ ] `[PRIV-A1:P1.05][AI]` Run only `AR-BIND`. Acceptance: second-generation stability is recorded without hand-editing generated mirrors.
- [ ] `[PRIV-A1:P2.01][AI]` Run only `AR-LOCAL`. Acceptance: local gate results and the overlay exclusion are separate records.
- [ ] `[PRIV-A1:P2.02][AI]` Run only `AR-STAGE`. Acceptance: cached paths equal the private ledger and omit the overlay.
- [ ] `[PRIV-A1:P3.01][AI]` Run only `AR-DRAFT`. Acceptance: the private-safe AI-marked draft and safe statistics are read back.
- [ ] `[PRIV-A1:P4.01][AI]` Run only `AR-ROUTE` with `UNIT=priv-a1` and `RECORD=local-tmp/optimize-pr-process/priv-a1-record.md`. Acceptance: its read-back route preserves the inherited cycle count.
- [ ] `[PRIV-A1:P4.02][AI]` Run only `AR-REVIEW` with that same record. Acceptance: the review URL/cycle and changed probe are read back.
- [ ] `[PRIV-A1:P4.03][AI]` Run only `AR-REPLY` with that same record. Acceptance: same-thread evidence has no private leakage.
- [ ] `[PRIV-A1:P4.04][AI]` Run only `AR-CI` with that same record. Acceptance: current-head CI is green in the stored result.
- [ ] `[PRIV-A1:P4.05][AI]` Run only `AR-READY` with that same record. Acceptance: readiness is read back without reopening the overlay.
- [ ] `[PRIV-A1:P5.01][AI]` Run only `AR-FINGERPRINT` with `UNIT=priv-a1`. Acceptance: the reviewed hash is stored before merge.
- [ ] `[PRIV-A1:P5.02][AI]` Run only `AR-MERGE` with the ready private PR record. Acceptance: merge JSON is stored under the existing merge gate.
- [ ] `[PRIV-A1:P5.03][AI]` Run only `AR-LANDED` with the merge SHA. Acceptance: landed and reviewed hashes match.
- [ ] `[PRIV-A1:P5.04][AI]` Run only `AR-RESYNC` with the same record. Acceptance: overlay-safe resync and one terminal obligation state are recorded.
- [ ] `[PRIV-A1:P1.06][AI]` On a portable or plan defect, perform only the `ENTRY-ADAPTERS:A1.06` classification/handoff. Acceptance: no second obligation or private mutation starts.
- [ ] `[PRIV-A1:P1.G][AI]` Pass semantic-correspondence, overlay, current-head, and terminal-obligation gate.
- [ ] `[PRIV-A1:P1.P][AI]` Record private merge pin and prepared PUB-A2 obligation.

### PUB-A2 — Public Review-Routing Rules

- [ ] `[PUB-A2:P1.01][AI]` Execute `AR-ENTRY` from the terminal PRIV-A1 pin. Acceptance: the exact public review-routing source/generated candidate ledger and forecast are in the route record.
- [ ] `[PUB-A2:P1.02][AI]` Run only `AR-PROPAGATE` for selected-risk, applicability, changed-probe, and bootcamp-readable route rules. Acceptance: every admitted public consumer appears in the strict manifest.
- [ ] `[PUB-A2:P1.03][AI]` Edit only manifest-admitted source paths. Acceptance: no generated mirror is hand-edited and unlisted status paths fail scope.
- [ ] `[PUB-A2:P1.04][AI]` Run only `AR-BIND`. Acceptance: `npm run validate:sync` passes and the second generation leaves tracked bytes unchanged.
- [ ] `[PUB-A2:P2.01][AI]` Run only `AR-LOCAL`. Acceptance: local quality and cap results are recorded before staging.
- [ ] `[PUB-A2:P2.02][AI]` Run only `AR-STAGE`. Acceptance: cached and committed full diffs were read and the exact ledger matches.
- [ ] `[PUB-A2:P3.01][AI]` Run only `AR-DRAFT`. Acceptance: the human-readable public draft is read back at its current head.
- [ ] `[PUB-A2:P4.01][AI]` Run only `AR-ROUTE` with `UNIT=pub-a2` and `RECORD=local-tmp/optimize-pr-process/pub-a2-record.md`. Acceptance: risk-selected/skipped lenses are read back.
- [ ] `[PUB-A2:P4.02][AI]` Run only `AR-REVIEW` with that same record. Acceptance: synthesis, cycle, and changed probe are read back; no Cycle 6 starts.
- [ ] `[PUB-A2:P4.03][AI]` Run only `AR-REPLY` with that same record. Acceptance: every disposition has native current-head evidence.
- [ ] `[PUB-A2:P4.04][AI]` Run only `AR-CI` with that same record. Acceptance: required CI is green for the record's current head.
- [ ] `[PUB-A2:P4.05][AI]` Run only `AR-READY` with that same record. Acceptance: ready-state JSON is read back.
- [ ] `[PUB-A2:P5.01][AI]` Run only `AR-FINGERPRINT` with `UNIT=pub-a2`. Acceptance: reviewed hash is stored before merge.
- [ ] `[PUB-A2:P5.02][AI]` Run only `AR-MERGE` with the ready public PR record. Acceptance: merge JSON is stored under the existing merge gate.
- [ ] `[PUB-A2:P5.03][AI]` Run only `AR-LANDED` with the merge SHA. Acceptance: matching landed fingerprint is recorded.
- [ ] `[PUB-A2:P5.04][AI]` Run only `AR-RESYNC` with the same record. Acceptance: resync prepares exactly one PRIV-A2 obligation.
- [ ] `[PUB-A2:P1.G][AI]` Pass routing, binding, five-cycle, scope-freeze, and landed-proof gate.
- [ ] `[PUB-A2:P1.P][AI]` Record public merge pin and prepared PRIV-A2 obligation.

### PRIV-A2 — Private Review-Routing Adaptation

- [ ] `[PRIV-A2:P1.01][AI]` Execute `AR-ENTRY` with PUB-A2's immutable obligation. Acceptance: the before/after overlay fingerprints match and the private routing ledger is explicit.
- [ ] `[PRIV-A2:P1.02][AI]` Classify the private routing result before edit. Acceptance: the private-safe PR records satisfaction, deviation, `N/A`, or portable defect with its evidence.
- [ ] `[PRIV-A2:P1.03][AI]` Run only `AR-PROPAGATE`. Acceptance: admitted private destinations are in the manifest and public summaries contain no private evidence.
- [ ] `[PRIV-A2:P1.04][AI]` Run only `AR-BIND`. Acceptance: generated parity succeeds without changing the authorized overlay.
- [ ] `[PRIV-A2:P2.01][AI]` Run only `AR-LOCAL`. Acceptance: private local gates and cap results are recorded separately from overlay proof.
- [ ] `[PRIV-A2:P2.02][AI]` Run only `AR-STAGE`. Acceptance: cached paths equal the ledger and omit the overlay.
- [ ] `[PRIV-A2:P3.01][AI]` Run only `AR-DRAFT`. Acceptance: the declared branch's private-safe draft is read back.
- [ ] `[PRIV-A2:P4.01][AI]` Run only `AR-ROUTE` with `UNIT=priv-a2` and `RECORD=local-tmp/optimize-pr-process/priv-a2-record.md`. Acceptance: exact-head route read-back is stored.
- [ ] `[PRIV-A2:P4.02a][AI]` Run only `AR-REVIEW` with that same record. Acceptance: review cycle and changed probe are separately stored.
- [ ] `[PRIV-A2:P4.03][AI]` Run only `AR-REPLY` with that same record. Acceptance: every same-thread disposition is read back.
- [ ] `[PRIV-A2:P4.04][AI]` Run only `AR-CI` with that same record. Acceptance: current-head CI result is stored and green.
- [ ] `[PRIV-A2:P4.05][AI]` Run only `AR-READY` with that same record. Acceptance: ready state is read back before merge.
- [ ] `[PRIV-A2:P4.02][AI]` Perform only the stop condition. Acceptance: before Cycle 6 or a second shared-budget reversal, the private PR/pair is frozen with its cycle count and native thread preserved.
- [ ] `[PRIV-A2:P5.01][AI]` Run only `AR-FINGERPRINT` with `UNIT=priv-a2`. Acceptance: reviewed hash is stored before merge.
- [ ] `[PRIV-A2:P5.02][AI]` Run only `AR-MERGE` with the ready private PR record. Acceptance: merge JSON is stored under the existing merge gate.
- [ ] `[PRIV-A2:P5.03][AI]` Run only `AR-LANDED` with the merge SHA. Acceptance: matching landed hash is stored.
- [ ] `[PRIV-A2:P5.04][AI]` Run only `AR-RESYNC` with the same record. Acceptance: overlay-safe resync keeps one terminal obligation.
- [ ] `[PRIV-A2:P1.05][AI]` On portable/plan defect, execute only `ENTRY-ADAPTERS:A1.06`–`A1.12`. Acceptance: the shared correction budget and private cycle count are retained.
- [ ] `[PRIV-A2:P1.G][AI]` Pass semantic-correspondence, scope, cycle, overlay, and obligation gate.
- [ ] `[PRIV-A2:P1.P][AI]` Record private merge pin and prepare PUB-A3 only after terminal state.

## Dormant Rules-Wave Checklist

### PUB-A3 / PRIV-A3 — Human PRs and Native Review Conversations

- [ ] `[PUB-A3:P1.01][AI]` Publish the exact public PR-body and source/generated ledger from the PRIV-A2 pin.
- [ ] `[PUB-A3:P1.02][AI]` Update only admitted public body, synthesis, fixer, and skill sources.
- [ ] `[PUB-A3:P1.03][AI]` Require outcome, why, scope, non-goals, reading order, verification, risk, safety, and rollback in plain language.
- [ ] `[PUB-A3:P1.04][AI]` Require blocking findings to explain evidence, impact, bounded remedy, and refutation for bootcamp-graduate readers.
- [ ] `[PUB-A3:P1.05][AI]` Require same-thread four-way dispositions and `Generated by AI` on every AI-authored artifact.
- [ ] `[PUB-A3:P1.06][AI]` Require frozen scope, changed probes, target Cycles 1–3, recovery 4–5, and stop before Cycle 6.
- [ ] `[PUB-A3:P1.07][AI]` Inventory the exact canonical plan-maker, skill, and workflow sentences that require a post-write or post-plan grill.
- [ ] `[PUB-A3:P1.08][AI]` Remove that separate plan-making requirement from admitted canonical sources without removing ordinary grilling or escalation for a genuinely unresolved decision.
- [ ] `[PUB-A3:P1.09][AI]` State that one bounded equivalence audit reuses stronger PR evidence, checks only uncovered plan-specific surfaces, and replaces both a separate grill and this plan's former full iterative workflow; record the rationale in plain language.
- [ ] `[PUB-A3:P2.01][AI]` Run only `AR-PROPAGATE` for the exact admitted PR-body/synthesis/fixer source set. Acceptance: placement manifest is read before any binding generation.
- [ ] `[PUB-A3:P2.02][AI]` Run only `AR-BIND`. Acceptance: source/generated paths and stable second generation are distinct evidence records.
- [ ] `[PUB-A3:P2.03][AI]` Run only `AR-LOCAL`. Acceptance: every applicable local command has result or reasoned `N/A` before staging.
- [ ] `[PUB-A3:P2.04][AI]` Run only `AR-STAGE`. Acceptance: staged source/generated paths equal the manifest-derived ledger.
- [ ] `[PUB-A3:P3.01][AI]` Run only `AR-DRAFT`. Acceptance: the public body is read back at exact current head.
- [ ] `[PUB-A3:P4.01][AI]` Run only `AR-ROUTE` with `UNIT=pub-a3` and `RECORD=local-tmp/optimize-pr-process/pub-a3-record.md`. Acceptance: the public route is read back with frozen scope and selected lenses.
- [ ] `[PUB-A3:P4.02][AI]` Run only `AR-REVIEW` with that same record. Acceptance: the current-head review URL, cycle, and changed probe are recorded.
- [ ] `[PUB-A3:P4.03][AI]` Run only `AR-REPLY` with that same record. Acceptance: every finding has an AI-marked same-thread disposition.
- [ ] `[PUB-A3:P4.04][AI]` Run only `AR-CI` with that same record. Acceptance: required checks are green for the recorded current head.
- [ ] `[PUB-A3:P4.05][AI]` Run only `AR-READY` with that same record. Acceptance: read-back confirms all readiness preconditions on that head.
- [ ] `[PUB-A3:P5.01][AI]` Run only `AR-FINGERPRINT` with `UNIT=pub-a3` and that same record. Acceptance: the reviewed-patch hash is stored before merge.
- [ ] `[PUB-A3:P5.02][AI]` Run only `AR-MERGE` with that same record. Acceptance: the existing merge gate is satisfied and merge JSON is stored.
- [ ] `[PUB-A3:P5.03][AI]` Run only `AR-LANDED` with that same record. Acceptance: landed and reviewed hashes match exactly.
- [ ] `[PUB-A3:P5.04][AI]` Run only `AR-RESYNC` with that same record. Acceptance: `origin/main` equals the merge and one PRIV-A3 obligation is prepared.
- [ ] `[PUB-A3:P1.G][AI]` Pass body, review, reply, AI-marker, scope, cycle, binding, and landed-proof gate.
- [ ] `[PUB-A3:P1.P][AI]` Record public merge pin and prepared PRIV-A3 obligation.
- [ ] `[PRIV-A3:P1.01][AI]` Read PUB-A3's immutable obligation and preserve the private overlay before adaptation.
- [ ] `[PRIV-A3:P1.02][AI]` Adapt only admitted private PR/review sources and keep private evidence in the private PR.
- [ ] `[PRIV-A3:P1.03][AI]` Apply the same body, native-thread, AI-marker, scope, and five-cycle intent semantically.
- [ ] `[PRIV-A3:P1.04][AI]` Remove only the private semantic equivalent of the obsolete post-plan grill; keep ordinary grilling and unresolved-decision escalation intact.
- [ ] `[PRIV-A3:P1.05][AI]` Record the private source/generated ledger and private-safe rationale for the bounded equivalence audit that replaces this plan's iterative gate run.
- [ ] `[PRIV-A3:P2.01][AI]` Run only `AR-PROPAGATE` for admitted private canonical sources. Acceptance: manifest excludes the overlay and names one semantic counterpart/deviation.
- [ ] `[PRIV-A3:P2.02][AI]` Run only `AR-BIND`. Acceptance: sync and second-generation proof leave the private overlay unchanged.
- [ ] `[PRIV-A3:P3.01][AI]` Run only `AR-STAGE`. Acceptance: one reconciled private source/generated commit excludes the overlay.
- [ ] `[PRIV-A3:P4.01][AI]` Run only `AR-DRAFT`. Acceptance: the private-safe body is read back at its exact current head.
- [ ] `[PRIV-A3:P4.02][AI]` Run only `AR-ROUTE` with `UNIT=priv-a3` and `RECORD=local-tmp/optimize-pr-process/priv-a3-record.md`. Acceptance: the private-safe route is read back with frozen scope and selected lenses.
- [ ] `[PRIV-A3:P4.03][AI]` Run only `AR-REVIEW` with that same record. Acceptance: the current-head review URL, cycle, and changed probe are recorded.
- [ ] `[PRIV-A3:P4.04][AI]` Run only `AR-REPLY` with that same record. Acceptance: every finding has an AI-marked same-thread disposition without private leakage.
- [ ] `[PRIV-A3:P4.05][AI]` Run only `AR-CI` with that same record. Acceptance: required checks are green for the recorded current head.
- [ ] `[PRIV-A3:P4.06][AI]` Run only `AR-READY` with that same record. Acceptance: read-back confirms all readiness preconditions on that head.
- [ ] `[PRIV-A3:P5.01][AI]` Run only `AR-FINGERPRINT` with `UNIT=priv-a3` and that same record. Acceptance: the reviewed-patch hash is stored before merge.
- [ ] `[PRIV-A3:P5.02][AI]` Run only `AR-MERGE` with that same record. Acceptance: the existing merge gate is satisfied and merge JSON is stored.
- [ ] `[PRIV-A3:P5.03][AI]` Run only `AR-LANDED` with that same record. Acceptance: landed and reviewed hashes match exactly.
- [ ] `[PRIV-A3:P5.04][AI]` Run only `AR-RESYNC` with that same record. Acceptance: overlay-safe resync records one terminal obligation state.
- [ ] `[PRIV-A3:P5.02][AI]` Freeze portable or plan defects through ENTRY-ADAPTERS without resetting the active private cycle count.
- [ ] `[PRIV-A3:P1.G][AI]` Pass semantic-correspondence, disclosure, overlay, cycle, and terminal-obligation gate.
- [ ] `[PRIV-A3:P1.P][AI]` Record private merge pin and prepare PUB-B only after terminal state.

### PUB-B / PRIV-B — Remove Conflicting Legacy Review Rules

- [ ] `[PUB-B:P1.01][AI]` Read the terminal PRIV-A3 pin and publish the exact public legacy-rule inventory with source, mirror, and historical-evidence classifications.
- [ ] `[PUB-B:P1.02][AI]` Distinguish live normative “one of seven”, seven-cycle, mandatory-three-cycle, and two-clean wording from immutable historical PR evidence.
- [ ] `[PUB-B:P1.03][AI]` Edit only admitted live canonical sources so they defer to the target 1–3, recovery 4–5, stop-before-6 policy.
- [ ] `[PUB-B:P1.04][AI]` Preserve historical evidence as history rather than rewriting a past PR or hiding why the policy changed.
- [ ] `[PUB-B:P1.05][AI]` Remove scope-expanding, automatic-agreement, or agent-only-review wording that conflicts with the frozen-scope and four-disposition rules.
- [ ] `[PUB-B:P1.06][AI]` Record every retained exception, its exact authority, and why it does not reintroduce an unbounded or conflicting review loop.
- [ ] `[PUB-B:P2.01][AI]` Run only `AR-PROPAGATE`. Acceptance: every affected public destination appears in the retained manifest.
- [ ] `[PUB-B:P2.02][AI]` Run only `AR-BIND`. Acceptance: sync passes and second generation creates no tracked change.
- [ ] `[PUB-B:P2.03][AI]` Run only `AR-LOCAL`. Acceptance: cap statistics are within bounds before staging.
- [ ] `[PUB-B:P2.03a][AI]` Run only `AR-STAGE`. Acceptance: staged paths equal the source/generated ledger before commit.
- [ ] `[PUB-B:P3.01][AI]` Read the complete committed diff from `AR-STAGE`. Acceptance: legacy cleanup is one cohesive commit.
- [ ] `[PUB-B:P4.01][AI]` Run only `AR-DRAFT`. Acceptance: the human-readable draft is read back at its exact head.
- [ ] `[PUB-B:P4.02][AI]` Run only `AR-ROUTE` with `UNIT=pub-b` and `RECORD=local-tmp/optimize-pr-process/pub-b-record.md`. Acceptance: the route is read back with frozen A3 scope and selected lenses.
- [ ] `[PUB-B:P4.03][AI]` Run only `AR-REVIEW` with that same record. Acceptance: the current-head review URL, cycle, and changed probe are recorded.
- [ ] `[PUB-B:P4.04][AI]` Run only `AR-REPLY` with that same record. Acceptance: every finding has an AI-marked same-thread disposition.
- [ ] `[PUB-B:P4.05][AI]` Run only `AR-CI` with that same record. Acceptance: required checks are green for the recorded current head.
- [ ] `[PUB-B:P4.06][AI]` Run only `AR-READY` with that same record. Acceptance: read-back confirms all readiness preconditions on that head.
- [ ] `[PUB-B:P5.01][AI]` Run only `AR-FINGERPRINT` with `UNIT=pub-b` and that same record. Acceptance: the reviewed-patch hash is stored before merge.
- [ ] `[PUB-B:P5.02][AI]` Run only `AR-MERGE` with that same record. Acceptance: the existing merge gate is satisfied and merge JSON is stored.
- [ ] `[PUB-B:P5.03][AI]` Run only `AR-LANDED` with that same record. Acceptance: landed and reviewed hashes match exactly.
- [ ] `[PUB-B:P5.04][AI]` Run only `AR-RESYNC` with that same record. Acceptance: `origin/main` equals the merge and one PRIV-B obligation is prepared.
- [ ] `[PUB-B:P1.G][AI]` Pass the legacy-inventory, historical-preservation, scope, cycle, binding, review, and landed-proof gate.
- [ ] `[PUB-B:P1.P][AI]` Record public merge pin and prepare PRIV-B only after terminal state.
- [ ] `[PRIV-B:P1.01][AI]` Read PUB-B's immutable obligation and preserve the authorized private overlay before inspecting private legacy wording.
- [ ] `[PRIV-B:P1.02][AI]` Classify private occurrences as a semantic counterpart, a private-only historical record, or a reasoned private deviation.
- [ ] `[PRIV-B:P1.03][AI]` Remove only conflicting live private wording while preserving accurate private history and disclosure boundaries.
- [ ] `[PRIV-B:P1.04][AI]` Record retained private exceptions and prove they neither reset cycle count nor widen the active public/private pair.
- [ ] `[PRIV-B:P2.01][AI]` Run only `AR-PROPAGATE`. Acceptance: the strict manifest names every private destination and excludes the overlay.
- [ ] `[PRIV-B:P2.01a][AI]` Run only `AR-BIND`. Acceptance: parity result and overlay-safe ledger are separate records.
- [ ] `[PRIV-B:P3.01][AI]` Run only `AR-STAGE`. Acceptance: one reconciled private source/generated commit has a read full diff.
- [ ] `[PRIV-B:P4.01][AI]` Run only `AR-DRAFT`. Acceptance: the private-safe body is individually read back.
- [ ] `[PRIV-B:P4.02][AI]` Run only `AR-ROUTE` with `UNIT=priv-b` and `RECORD=local-tmp/optimize-pr-process/priv-b-record.md`. Acceptance: the private-safe route is read back with frozen scope and selected lenses.
- [ ] `[PRIV-B:P4.03][AI]` Run only `AR-REVIEW` with that same record. Acceptance: the current-head review URL, cycle, and changed probe are recorded.
- [ ] `[PRIV-B:P4.04][AI]` Run only `AR-REPLY` with that same record. Acceptance: every finding has an AI-marked same-thread disposition without private leakage.
- [ ] `[PRIV-B:P4.05][AI]` Run only `AR-CI` with that same record. Acceptance: required checks are green for the recorded current head.
- [ ] `[PRIV-B:P4.06][AI]` Run only `AR-READY` with that same record. Acceptance: read-back confirms all readiness preconditions on that head.
- [ ] `[PRIV-B:P5.01][AI]` Run only `AR-FINGERPRINT` with `UNIT=priv-b` and that same record. Acceptance: the reviewed-patch hash is stored before merge.
- [ ] `[PRIV-B:P5.02][AI]` Run only `AR-MERGE` with that same record. Acceptance: the existing merge gate is satisfied and merge JSON is stored.
- [ ] `[PRIV-B:P5.03][AI]` Run only `AR-LANDED` with that same record. Acceptance: landed and reviewed hashes match exactly.
- [ ] `[PRIV-B:P5.04][AI]` Run only `AR-RESYNC` with that same record. Acceptance: overlay-safe resync records one terminal pair state.
- [ ] `[PRIV-B:P1.G][AI]` Pass semantic correspondence, historical preservation, disclosure, scope, cycle, and terminal-obligation gate.
- [ ] `[PRIV-B:P1.P][AI]` Record private merge pin and authorize the Wave C necessity decision.

### Wave C — Necessity-Gated Mechanism Decision

- [ ] `[PUB-C:P1.01][AI]` Read the terminal PRIV-B pin and inventory the remaining PR-review evidence gap, if any, using only current native artifacts and delivery evidence.
- [ ] `[PUB-C:P1.02][AI]` Prove whether existing prose, GitHub comments/replies, current gates, and the admitted rules can or cannot close that exact gap.
- [ ] `[PUB-C:P1.03][AI]` Record `N/A` and continue to closure when no narrow, repeatable gap remains; do not create tooling merely to make the process look enforced.
- [ ] `[PUB-C:P1.04][AI]` If a gap remains, write a bounded necessity case: affected readers, exact failure, expected benefit, maintenance cost, alternatives rejected, public/private impact, rollback, and why the lightest non-tooling option fails.
- [ ] `[PUB-C:P1.05][AI+HUMAN]` Freeze all optional-C implementation until a human approves the necessity case in its native GitHub thread; only then may a PLAN-AMENDMENT change the approved scope.
- [ ] `[PUB-C:P1.G][AI]` Pass the evidence-first, no-mechanism-by-default, scope, pair-state, and `N/A`-or-approved-case gate.
- [ ] `[PUB-C:P1.P][AI]` Record either the no-change decision with PRIV-C `N/A`, or the human-approved public-C successor and paired private obligation.
- [ ] `[PRIV-C:P1.01][AI]` On public C `N/A`, record private C `N/A` from the immutable PUB-C decision without opening a needless private PR.
- [ ] `[PRIV-C:P1.02][AI]` On human-approved public C, inspect the immutable public mechanism obligation and preserve the authorized private overlay before adaptation.
- [ ] `[PRIV-C:P1.03][AI]` Apply only the approved semantic counterpart, or record a reasoned private deviation with evidence, owner, and disclosure-safe rationale.
- [ ] `[PRIV-C:P1.04][AI]` If a private C PR is necessary, run only `AR-PROPAGATE`. Acceptance: the strict manifest names only approved private paths; otherwise record the explicit `N/A` from P1.01.
- [ ] `[PRIV-C:P1.05][AI]` Run only `AR-BIND` when a private C PR is necessary. Acceptance: source/generated paths and stable second generation are separately recorded.
- [ ] `[PRIV-C:P2.01][AI]` Run only `AR-LOCAL` when a private C PR is necessary. Acceptance: every applicable local result or reasoned `N/A` is recorded before staging.
- [ ] `[PRIV-C:P2.02][AI]` Run only `AR-STAGE` when a private C PR is necessary. Acceptance: cached paths equal the manifest-derived ledger.
- [ ] `[PRIV-C:P3.01][AI]` Run only `AR-DRAFT` when a private C PR is necessary. Acceptance: the private-safe, AI-marked draft is read back at its exact head.
- [ ] `[PRIV-C:P4.01][AI]` Run only `AR-ROUTE` with `UNIT=priv-c` and `RECORD=local-tmp/optimize-pr-process/priv-c-record.md` when a private C PR is necessary. Acceptance: the private-safe route is read back with frozen scope and selected lenses.
- [ ] `[PRIV-C:P4.02][AI]` Run only `AR-REVIEW` with that same record when a private C PR is necessary. Acceptance: the current-head review URL, cycle, and changed probe are recorded.
- [ ] `[PRIV-C:P4.03][AI]` Run only `AR-REPLY` with that same record when a private C PR is necessary. Acceptance: every finding has an AI-marked same-thread disposition without private leakage.
- [ ] `[PRIV-C:P4.04][AI]` Run only `AR-CI` with that same record when a private C PR is necessary. Acceptance: required checks are green for the recorded current head.
- [ ] `[PRIV-C:P4.05][AI]` Run only `AR-READY` with that same record when a private C PR is necessary. Acceptance: read-back confirms all readiness preconditions on that head.
- [ ] `[PRIV-C:P5.01][AI]` Run only `AR-FINGERPRINT` with `UNIT=priv-c` and that same record when a private C PR is necessary. Acceptance: the reviewed-patch hash is stored before merge.
- [ ] `[PRIV-C:P5.02][AI]` Run only `AR-MERGE` with that same record when a private C PR is necessary. Acceptance: the existing merge gate is satisfied and merge JSON is stored.
- [ ] `[PRIV-C:P5.03][AI]` Run only `AR-LANDED` with that same record when a private C PR is necessary. Acceptance: landed and reviewed hashes match exactly.
- [ ] `[PRIV-C:P5.04][AI]` Run only `AR-RESYNC` with that same record when a private C PR is necessary. Acceptance: overlay-safe resync records one terminal C state.
- [ ] `[PRIV-C:P1.G][AI]` Pass private semantic-correspondence, overlay, disclosure, necessity, and terminal-obligation gate.
- [ ] `[PRIV-C:P1.P][AI]` Record the terminal C state and authorize EXECUTION-CLOSURE.

## Dormant Execution-Closure Checklist

### CLOSURE — Final Audit, Knowledge Capture, Archive, and Worktree Removal

#### Pre-merge closure evidence (Phase 5)

Before the CLOSURE PR is made ready, record `CLOSURE_PR` (its immutable number/URL) in the
closure PR body and perform every permitted knowledge-capture, archive, and index mutation in that
same reviewed PR. A candidate learning may name an existing durable destination or a proposed
follow-up only; it never creates a new `plans/backlog/**` or `plans/ideas/**` path in this unit.

- [ ] `[CLOSURE:P5.13][AI]` Before ready state, triage `plans/in-progress/optimize-pr-process/learnings.md`: retain a safe, repository-relevant learning only with one existing named durable destination; otherwise add a discard reason. Acceptance: no private value enters public text and no new path is created.
- [ ] `[CLOSURE:P5.14][AI]` Before ready state, run `rg -ni --glob '*.md' "$idea_search" plans/ideas/README.md plans/ideas/q1-urgent-important plans/ideas/q2-not-urgent-important` for every ideas candidate and record its result in the CLOSURE PR. Acceptance: a match reuses the existing brief; no match becomes a proposed follow-up requiring a separate exact-path amendment.
- [ ] `[CLOSURE:P5.15][AI]` Before ready state, move the completed control plan and update only its admitted archive/index paths in the CLOSURE PR. Acceptance: the full staged ledger stays within the file-impact tree and the closure PR contains every mutation for review.

- [ ] `[CLOSURE:P6.01][AI]` Read the terminal public C state and enumerate every public unit plus each optional route.
- [ ] `[CLOSURE:P6.02][AI]` Read the terminal private C state and enumerate every private unit plus each terminal `N/A` decision.
- [ ] `[CLOSURE:P6.03][AI]` Enumerate every correction and PLAN-AMENDMENT with its immutable predecessor and terminal pin.
- [ ] `[CLOSURE:P6.04][AI]` Reconcile each live task-list item to exactly one Markdown ID.
- [ ] `[CLOSURE:P6.05][AI]` Record the durable PR artifact and accountable owner for every completed, deferred, rejected, `N/A`, or blocked item.
- [ ] `[CLOSURE:P6.06][AI]` Verify the exact public and private merge pins for each required pair.
- [ ] `[CLOSURE:P6.07][AI]` Verify one terminal sibling-obligation state for each required pair.
- [ ] `[CLOSURE:P6.08][AI]` Prove no active or frozen successor remains after a pair reaches its recorded terminal state.
- [ ] `[CLOSURE:P6.09][AI]` Verify every merged delivery PR has a readable human-facing body.
- [ ] `[CLOSURE:P6.10][AI]` Verify every AI-authored body, route, review, and reply ends with `Generated by AI`.
- [ ] `[CLOSURE:P6.11][AI]` Verify each eligible PR has a route, cycle count, and same-thread disposition evidence.
- [ ] `[CLOSURE:P6.12][AI]` Verify each merged PR has current-head CI and landed-diff fingerprint evidence.
- [ ] `[CLOSURE:P6.13][AI]` Compare every public/private rule pair for semantic correspondence.
- [ ] `[CLOSURE:P6.14][AI]` Record byte-identical pairs only where an existing contract requires byte identity.
- [ ] `[CLOSURE:P6.15][AI]` Verify public audit records contain no private evidence or private-only deviation detail.
- [ ] `[CLOSURE:P6.16][AI]` Verify every portable defect consumed no more than one public correction.
- [ ] `[CLOSURE:P6.17][AI]` Verify every second portable-source reversal stopped for a human decision.
- [ ] `[CLOSURE:P6.18][AI]` Verify no private review resumed with a reset cycle budget.
- [ ] `[CLOSURE:P6.19][AI]` Verify Wave C is a durable no-change decision, or link its separately human-approved amendment.
- [ ] `[CLOSURE:P6.20][AI]` Reject and record any tooling or enforcement surface not declared by a Wave C decision.
- [ ] `[CLOSURE:P6.21][AI]` Read-only validation: read `CLOSURE_PR` from the merged closure PR body, then run `gh pr view "$CLOSURE_PR" --repo wahidyankf/ose-public --json url,baseRefOid,headRefOid,body,additions,deletions,changedFiles,mergeCommit,state`. Acceptance: its immutable URL, base/head, readable AI-marked body, statistics, state, and merge SHA equal the pre-merge Phase 3 and Phase 5 records; this step creates no PR mutation.
- [ ] `[CLOSURE:P6.22][AI]` Read-only validation: run `gh pr view "$CLOSURE_PR" --repo wahidyankf/ose-public --json reviews,comments` and compare returned URLs with the Phase 4 evidence. Acceptance: every recorded review/disposition is present and no new review or reply is posted in Phase 6.
- [ ] `[CLOSURE:P6.23][AI]` Read-only validation: run `gh pr checks "$CLOSURE_PR" --repo wahidyankf/ose-public --required`. Acceptance: the pre-merge recorded current-head CI is green and names the reviewed head; Phase 6 does not poll, repair, or restart CI.
- [ ] `[CLOSURE:P6.24][AI]` Read-only validation: run `gh pr view "$CLOSURE_PR" --repo wahidyankf/ose-public --json isDraft,headRefOid,mergeStateStatus,statusCheckRollup`. Acceptance: it confirms the Phase 4 ready-state record; Phase 6 does not transition readiness.
- [ ] `[CLOSURE:P6.25][AI]` Read-only validation: run `gh pr view "$CLOSURE_PR" --repo wahidyankf/ose-public --comments` and compare Phase 5's recorded raw-patch hashes. Acceptance: both hashes are present and identical; Phase 6 calculates no replacement fingerprint.
- [ ] `[CLOSURE:P6.26][AI]` Read-only validation: run `git fetch origin main && git status --short --branch` in the declared public worktree and compare `origin/main` with the merge SHA read in P6.21. Acceptance: `origin/main` contains that merge and the Phase 5 resync record is present; Phase 6 does not merge, switch branches, or resync again.
- [ ] `[CLOSURE:P6.27][AI]` Read-only validation: compare the merged CLOSURE PR's measured PR sizes, cycle counts, corrections, amendments, and terminal states with its pre-merge evidence record.
- [ ] `[CLOSURE:P6.28][AI]` Read-only validation: verify every exception/follow-up in the merged CLOSURE PR has an owner, evidence, next action, and no undeclared path mutation.
- [ ] `[CLOSURE:P6.29][AI]` Read-only validation: verify Phase 5 performed public-safe knowledge capture before merge.
- [ ] `[CLOSURE:P6.29a][AI]` Read `plans/done/YYYY-MM-DD__optimize-pr-process/learnings.md` and verify every entry is retained with one existing durable destination or discarded with a reason.
- [ ] `[CLOSURE:P6.29b][AI]` Run `rg -ni --glob '*.md' '(secret|credential|token|private hostname)' plans/done/YYYY-MM-DD__optimize-pr-process/learnings.md`. Acceptance: any match is a documented placeholder or discard; Phase 6 changes nothing.
- [ ] `[CLOSURE:P6.29c][AI]` Verify a proposed code/test follow-up is only a named candidate in the merged CLOSURE PR, awaiting its own exact-path plan/amendment; no `plans/backlog/**` path was created here.
- [ ] `[CLOSURE:P6.29d][AI]` Verify each ideas candidate has the Phase 5 search result and either an existing reused brief or a proposed separate exact-path amendment; no new idea path was created here.
- [ ] `[CLOSURE:P6.29e][AI]` Verify Phase 5 wrote the explicit none outcome when no generalizable learning survived; otherwise verify every entry has a terminal evidence link.
- [ ] `[CLOSURE:P6.30][AI]` Verify the repository-approved archive location and its required public indexes.
- [ ] `[CLOSURE:P6.31][AI]` Move the completed public plan only after all audit and archive checks pass.
- [ ] `[CLOSURE:P6.32][AI]` Update only the required plan indexes and read them back after archive.
- [ ] `[CLOSURE:P6.33][AI]` Fetch public `origin/main` and record its immutable tip before cleanup.
- [ ] `[CLOSURE:P6.34][AI]` Fetch private `origin/main` and record its immutable tip before cleanup.
- [ ] `[CLOSURE:P6.35][AI]` Prove public main contains every recorded public merge pin.
- [ ] `[CLOSURE:P6.36][AI]` Prove private main contains every recorded private merge pin.
- [ ] `[CLOSURE:P6.37][AI]` From the public repository root, list registered worktrees and record the explicit public plan path.
- [ ] `[CLOSURE:P6.38][AI]` Prove the public plan worktree is clean and no longer owns an active branch.
- [ ] `[CLOSURE:P6.39][AI]` From the private repository root, list registered worktrees and record the explicit private plan path.
- [ ] `[CLOSURE:P6.40][AI]` Prove the private plan worktree is clean and its authorized overlay has been resolved by the planned private work.
- [ ] `[CLOSURE:P6.41][AI]` Remove only the explicit public plan worktree using the repository's worktree procedure.
- [ ] `[CLOSURE:P6.42][AI]` Remove only the explicit private plan worktree using the repository's worktree procedure.
- [ ] `[CLOSURE:P6.43][AI]` Prune stale public worktree registrations and list the registry again.
- [ ] `[CLOSURE:P6.44][AI]` Prune stale private worktree registrations and list the registry again.
- [ ] `[CLOSURE:P6.45][AI]` Prove neither explicit plan worktree path remains registered or on disk.
- [ ] `[CLOSURE:P6.46][AI]` Return the active working directory and final status report to ose-public after cleanup evidence is complete.
- [ ] `[CLOSURE:P6.G][AI]` Pass complete task/evidence reconciliation, pair terminality, auditability, public/private disclosure, no-tooling, dogfood, archive, main-branch, and worktree-removal gate.
- [ ] `[CLOSURE:P6.P][AI]` Record final public/private main pins, archive location, removed worktree paths, retained follow-ups, and the ose-public focus state.

## Dormant Lifecycle and Evidence-State Template

The lines below deliberately are not checkboxes. The six WAVES checklist slices must copy every
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
PR records a pending sibling obligation with wave, public URL, reviewed head, rule class, stable
defect-lineage ID, expected private paths, byte-identity class, reconciled `correction-count`
(`0` only on no match), `correction-kind: correction|plan-amendment`, successor, and one accountable
owner. The native record is human-readable PR evidence, not an automated synchronization mechanism.

Private review classifies each concern as local adaptation, private deviation, unrelated follow-up,
or portable defect, using the glossary above. Only the last may request upstream correction, citing
the public line, private evidence, and why local adaptation would be wrong. Freeze the private PR:
it may remain open, but receives no push, review cycle, readiness transition, or merge.

Before allocating a lineage ID, compare candidate root cause read-only with every sealed or
correction-pending native lineage record. Record the compared PR/thread URLs, the evidence used, and
one outcome: no match allocates a new ID at count 0; an unambiguous match reuses its ID and current
count; an ambiguous comparison freezes the pair and stops for human judgment without allocating,
preparing, or correcting—ambiguity stops without a prepared obligation. This makes relabeling a
reconciliation decision rather than a fresh budget.

At most one fresh, unstacked `optimize-pr-process-pub-<wave>-correction-1` PR **or** one
single-purpose cross-repository `PLAN-AMENDMENT` may merge per defect lineage **only when the
reconciled count is 0**. A PLAN-AMENDMENT for an existing lineage is that correction, never a reset
or parallel escape. Its native record links both public pins/heads and the paused private PR/head,
supersedes the old obligation, preserves the reconciled lineage ID, records the applicable
`correction-kind`, and changes `correction-count: 0 → 1`; private review restarts from the
replacement pin. A late finding or a new repair-pair URL must first complete the same reconciliation
and cannot reset the count. At reconciled count 1, neither correction type may start: stop for a
human with the pair frozen. Downstream remains frozen until the obligation is
`satisfied`, `reasoned-deviation`, or `N/A`. “In sync” means semantic correspondence with explicit
deviations; byte identity applies only to an existing contract.

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

After activation, PUB-IDEAS-4–8 merge sequentially before PRIV-IDEAS. Later implementation remains sequential:
`PUB-A1 → PRIV-A1 → PUB-A2 → PRIV-A2 → PUB-A3 → PRIV-A3 → PUB-B → PRIV-B → PUB-C? → PRIV-C? →
closure`; C stays a no-change decision unless necessity passes. Public pins and native sibling
obligations keep the repositories semantically “in sync”; private-only deviations stay private.

CORE-ENTRY, CORE-REVIEW, all four WAVES-ENTRY checklist slices, WAVES-A, WAVES-RULES, and
EXECUTION-CLOSURE must
turn this order into a 1:1 runnable checklist and preserve every merge step and its authority. No
assembly PR may begin implementation.

## Dormant Authority Mapping

This mapping replaces the two historical shortcut checkboxes; it is not executable work.
The six WAVES checklist slices must instantiate each applicable Phase 4–5 action and gate per owned unit,
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
