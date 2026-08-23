# Delivery Plan: Optimize the Pull Request Process

## Current State

| Evidence                                                                            | State                                                        |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [Repo-grounded] Merged [PR #250](https://github.com/wahidyankf/ose-public/pull/250) | FOUNDATION at `62608547df0d2063d369537e0753f22699456f44`     |
| [Repo-grounded] Merged [PR #251](https://github.com/wahidyankf/ose-public/pull/251) | REQUIREMENTS at `8884ec79437a05af3e8404e63239e079a379d84f`   |
| [Repo-grounded] Merged [PR #252](https://github.com/wahidyankf/ose-public/pull/252) | DESIGN at `3ac2468f534be2faaf0b5a784b04b6411313f49e`         |
| [Repo-grounded] Merged [PR #253](https://github.com/wahidyankf/ose-public/pull/253) | FORECAST at `a46725dba24c4880e7854b0b5504b26dd3bdbb33`       |
| [Repo-grounded] Merged [PR #254](https://github.com/wahidyankf/ose-public/pull/254) | Split forecast at `b4dca85adc9ebc42eb53d69500e5d0475adb1522` |
| [Repo-grounded] CORE-ENTRY                                                          | Active: author lifecycle spine and Phase 0–3 mechanics       |
| [Unverified] Complete assembled plan                                                | Fresh formal gate and grill still precede activation         |

> **AUTHORING-ONLY UNTIL ACTIVATE:** CORE-ENTRY writes templates and runs none. Only the four plan
> docs named below may change; no private worktree, formal gate, idea/rule/agent/code/test work runs.

## Executor Legend and Plain-Language Terms

Tags become executable only after ACTIVATE: `[AI]` means the agent acts and records evidence;
`[HUMAN]` reserves an authority decision; `[AI+HUMAN]` means the agent prepares evidence for it.

| Term               | Meaning                                                                   |
| ------------------ | ------------------------------------------------------------------------- |
| Worktree           | A second checkout reserved for this plan.                                 |
| Delivery unit      | One branch, one PR, and one independently stable result.                  |
| Pin                | An immutable commit SHA used as evidence.                                 |
| File ledger        | The exact admitted path list before and after work.                       |
| Current head       | The exact commit currently under review and checked by CI.                |
| Semantic exit      | The point where scope, checks, review threads, and audit are complete.    |
| Landed-diff proof  | Evidence that merged content equals the reviewed change.                  |
| Resync             | Fetch merged `main`, read what landed, then branch from that `main`.      |
| Sibling obligation | A PR record asking the other repository to adapt or explain a difference. |

## Dormant Boundary

Plan assembly is deliberately **dormant and non-executable**. CORE-ENTRY may change only this plan's
`README.md`, `delivery.md`, `tech-docs.md`, and `learnings.md`. CORE-REVIEW, EXECUTION-WAVES,
EXECUTION-CLOSURE, ideas, indexes, rules, agents, bindings, workflows, code, tests, implementation,
and active-plan indexes remain dormant. The formal gate waits for complete assembly.

## Worktree

Reuse exactly one worktree per repository for this whole plan:

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

Follow the [worktree specification][worktree-spec], [one-worktree cap][worktree-cap], and [path
rule][worktree-path].

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
CORE-SPLIT-FORECAST → CORE-ENTRY → CORE-REVIEW → EXECUTION-WAVES → EXECUTION-CLOSURE →
ACTIVATE/formal-gate/grill → PUB-IDEAS → PRIV-IDEAS → implementation waves
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
| EXECUTION-WAVES   | Numbered PUB/PRIV idea, A1–A3, B, and optional C units with stability and TDD gates; F-035                                              |              280–340 |
| EXECUTION-CLOSURE | Reconciliation/dogfood, knowledge, private terminal proof, public archival, cleanup; F-013, F-018, F-036–F-037                          |              220–300 |
| ACTIVATE          | Clean formal plan-quality gate, post-write grill, and explicit executable-status change                                                 |          at most 400 |

The two CORE slices keep the original 20-finding ownership complete:

- CORE-ENTRY owns the complete lifecycle spine and separate authoring, pushed-head, review, CI,
  merge, landed-proof, resync, and sibling states, plus detailed Phase 0–3 mechanics.
- CORE-REVIEW owns routing, review/fixer cycles, current-head CI, cross-repo correction limits,
  merge/landed proof, and `PLAN-AMENDMENT`.

The other slice names mean:

- EXECUTION-WAVES authors the later checklists for paired public/private units: A1 plan-making rules, A2 review
  routing, A3 PR and reply rules, B legacy-conflict cleanup, and optional C tooling only if evidence
  proves it necessary. Any future code change uses test-driven development: write the failing test
  before the behavior change.
- EXECUTION-CLOSURE authors the later checklist for reconciling the plan with what landed, dogfooding the
  process—using it on its own PRs—capturing knowledge, closing private work, archiving the public
  plan, and safely removing worktrees.
- ACTIVATE runs the formal plan-quality gate and a structured post-write user review (the “grill”)
  before changing the assembled plan from dormant to executable.

Both CORE slices, EXECUTION-WAVES, and EXECUTION-CLOSURE only author checklists; none executes
before ACTIVATE.

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
EXECUTION-WAVES supplies exact unit scope/acceptance and EXECUTION-CLOSURE supplies Phase 6 proof.

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
| 1–6      | CLOSURE     | public/PUB-WT   | `optimize-pr-process-closure`                        | worktree-to-pr | Phase 6 | last unit                   | plan archived and focused |

Repair rows activate only after their baseline fails; each runs Phases 1–5, merges, and reruns that
baseline. Its ordinary successor uses the repair merge SHA; otherwise it uses the normal pin shown.
Optional C becomes a recorded no-change decision when necessity fails. Before each unit, replace
its predecessor with the exact SHA in the task, body, and audit comment. Missing state blocks the
next row.

The exact 20-source classification, owner, retained requirement, and later retirement unit live in
the [idea disposition map](./idea-disposition-map.md). Its public source pin is
`62608547df0d2063d369537e0753f22699456f44`; its private source pin is
`718c20c923707d777a89639f760f98d53740bd70`.

## Audit Ownership Map

The fresh findings are confirmed and remain owned, not waived or deferred forever. Their
[durable PR-native catalog](https://github.com/wahidyankf/ose-public/pull/250#issuecomment-5384375806)
gives every ID a plain-language defect, affected artifact, and REQUIREMENTS, DESIGN, or EXECUTION
owner even after the gitignored source report is cleared.

FOUNDATION through CORE-SPLIT-FORECAST are merged. CORE-ENTRY supplies the reusable spine below but
runs none of it. ACTIVATE may open only after CORE-REVIEW, EXECUTION-WAVES, and EXECUTION-CLOSURE
instantiate every delivery unit as granular, attributable checkboxes and every finding is fixed. A
fresh formal gate and grill must then pass; historic evidence cannot substitute.

## Dormant Lifecycle and Evidence-State Template

The lines below deliberately are not checkboxes. EXECUTION-WAVES must copy every universal action
and gate into separate tagged checkboxes per unit; for a conditional block it copies applicable
actions or one reasoned `N/A` checkbox. EXECUTION-CLOSURE does the same for Phase 6, and CORE-REVIEW
replaces the historical merge placeholders. Before ACTIVATE, checkboxes and live tasks map 1:1.

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
merged and recorded, no ordinary-unit PR is open, and the first unit has an exact pin. **Pause
Safety:** record repository, baseline result, predecessor, and Phase 1 entry command.

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
ledger contains only owned paths. **Pause Safety:** record branch, head, ledger, dirty state, and one
next verification command; do not start another unit.

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
are cohesive, and the full diff was read. **Pause Safety:** record local head and clean tree or
named intended residue; resume with the pre-push command.

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

One draft PR exists at the declared boundary and its human entry point matches the diff. **Pause
Safety:** retain URL, current head, literal payload, and the next review-route command.

## Dormant Common Failure Rules

- Fix every red gate at root cause. If a required pre-existing repair would exceed ownership or
  size, pause and deliver a separate bounded repair PR; never waive or silently absorb it.
- Never reset, force-push shared history, auto-stash an overlay, bypass a gate, dismiss a finding to
  manufacture exit, or treat a comment as authority to expand scope.

## Cross-Repository Order (Dormant)

After activation, PUB-IDEAS merges before PRIV-IDEAS. Later implementation remains sequential:
`PUB-A1 → PRIV-A1 → PUB-A2 → PRIV-A2 → PUB-A3 → PRIV-A3 → PUB-B → PRIV-B → PUB-C? → PRIV-C? →
closure`; C stays a no-change decision unless necessity passes. Public pins and native sibling
obligations keep the repositories semantically “in sync”; private-only deviations stay private.

CORE-ENTRY, CORE-REVIEW, EXECUTION-WAVES, and EXECUTION-CLOSURE must turn this order into a 1:1
runnable checklist and preserve every merge step and its authority. No assembly PR may begin
implementation.

## Preserved Merge Authority (Dormant)

These existing gates remain verbatim and retain their current authority. The dormant boundary makes
them non-executable until assembly and ACTIVATE add every prerequisite; it also places the new
assembly slices before the historical “then” clause below.

- [ ] Mark ready and merge only after semantic exit, then record merge SHA, read the landed diff,
      resync the worktree, and discharge or carry forward the native obligation.
- [ ] Merge/resync PLAN, then deliver PUB-IDEAS and PRIV-IDEAS as separate PRs.

[worktree-spec]: ../../../repo-governance/conventions/structure/plans/worktree-specification.md
[worktree-cap]: ../../../repo-governance/conventions/structure/plans/worktree-cap.md
[worktree-path]: ../../../repo-governance/conventions/structure/worktree-path.md
