# Delivery Plan: Optimize the Pull Request Process

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]` for
> compatibility, but this plan marks every item). `[HUMAN]`: only a human can perform the step.
> `[AI+HUMAN]`: an agent prepares the evidence or draft and a human makes the authority-bearing
> decision.

## How to Make and Execute a Large Plan

> **Current state: AUTHORIZED ON 2026-08-23 FOR THE FORMAL PLAN GATE, PLAN AND PRIV-IDEAS DELIVERY,
> AND FULL EXECUTION.** The authorization ledger is satisfied for those transitions. This plan-edit
> turn remains document-only: do not run the gate, stage, commit, push, open PRs, or implement while
> revising this file. The root executor may begin the authorized lifecycle only after this revision
> is handed back.

The operator follows this lifecycle without skipping or combining states:

1. **Make and iterate the plan in the existing repo-scoped worktrees.** Use
   `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process` from initial plan authoring
   through plan-only delivery and every later public PR. Ground the six documents in repository
   evidence, prior PR artifacts, current web sources, and resolved user decisions. During this
   state, edit no rule, binding, workflow, application, library, or other implementation file. The
   explicitly authorized idea retirement uses the one private plan worktree too; that earlier
   authority granted no implementation by itself, while the later 2026-08-23 instruction grants the
   separately bounded full execution recorded below.
2. **Run the authorized plan gate and deliver the authorized plan-document boundaries.** The
   2026-08-23 instruction authorizes the formal plan gate, PLAN delivery, and PRIV-IDEAS delivery.
   PLAN and PRIV-IDEAS remain separate repository PRs: PLAN lands first, then PRIV-IDEAS links the
   merged PLAN disposition. Their delivery remains distinct from rule implementation even though
   full execution is now also authorized.
3. **After the authorized plan-only PR merges, reuse and synchronize the same public worktree.**
   Prove it is clean, fetch `origin`, read the landed diff, and align the worktree with current
   `origin/main`. Never replace it and never create a worktree per PR. Stop in the synchronized state
   before starting the first already-authorized implementation wave.
4. **Select exactly one fixed public/private wave.** Start its public unit from current public
   `origin/main`, then start the matching private discharge only after the public PR is merged and
   green. Confirm each unit's predecessor, source pin, bounded problem/non-goals, ledger paths,
   integration-safety/feature-flag strategy, rollback, and current-head validation before editing.
   Do not improvise a unit or stack dependent work on an unmerged branch.
5. **Reassess before opening the unit PR.** Measure review-relevant hand-authored lines/files and
   reread the conceptual diff. If the unit is oversized or no longer one problem, stop. Amend and
   re-review these plan documents in the same worktree, without invoking the formal plan quality
   gate unless the user separately authorizes it; split only at a boundary that leaves `main`
   coherent, green, reversible, and independently useful. Do not improvise or stack the overflow.
6. **Complete one paired wave before beginning the next.** Review/fix/merge and record evidence for
   the public unit, synchronize its worktree, pin the merged green PR/SHA, then perform the matching
   private discharge and synchronize the private worktree. Dependent PRs are sequential and
   unstacked by default; unrelated already-merged units stay valid when one obligation is corrected.
7. **Protect scope during review.** Adjacent feedback becomes a linked follow-up from its original
   thread. Expansion across the same defect class remains eligible only after reassessing the unit's
   boundary, cohesion, integration safety, rollback, and size; split and amend the plan when those
   proofs no longer hold.
8. **Reuse the authorized private worktree for the interleaved waves.** The user explicitly
   authorized cross-repo idea consolidation and full execution on 2026-08-23, so
   `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process` was provisioned once from
   private `origin/main`. Deliver its idea-retirement/index/link edits as PRIV-IDEAS, then reuse it
   for each private discharge immediately after the matching public wave merges green. Private
   never consumes a draft or stacked public branch.
9. **Leave every pause safe.** At any stop, each repository's merged state is coherent and green,
   the active change is bounded and recoverable, rollback is known, the owned worktree is clean or
   its exact residue is recorded, and the PR artifact explains the next authorized action.

### Claim-confidence key

Existing paths, commands, agents, workflows, worktree locations, and repository behaviors named in
this checklist were verified in the two plan worktrees on 2026-08-23 and are `[Repo-grounded]`.
Fixed branch order, size heuristics, one-open-wave policy, correction budget, and conditional
delivery design are `[Judgment call]` decisions authorized by this plan. A conditional path marked
`reserved` is repo-grounded as an existing surface but remains untouched until its necessity gate
passes; a branch or PR described as conditional does not exist until its triggering evidence does.

### Authorization ledger

Record the user instruction and evidence for each transition before taking it. A later authorization
does not retroactively authorize an earlier or different action.

| Transition                               | Recorded authority and status                                                         | State after transition                                                             |
| ---------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Plan making → formal plan gate           | Authorized by the user on 2026-08-23                                                  | Formal gate may run; findings may amend only plan/authorized idea-retirement paths |
| Plan making → cross-repo idea retirement | Authorized by the user on 2026-08-23                                                  | Existing private worktree may deliver bounded idea/index/link edits                |
| Plan making → plan-document delivery     | PLAN and PRIV-IDEAS delivery authorized by the user on 2026-08-23                     | PLAN lands first; PRIV-IDEAS then links merged PLAN                                |
| Merged PLAN → full implementation        | Full execution authorized by the user on 2026-08-23                                   | Same repo worktrees execute one interleaved wave at a time                         |
| Public wave → matching private discharge | Covered by full execution authority; public source must first be merged and green     | Private may consume the pinned public PR/SHA, never its draft                      |
| One wave → next wave                     | Prior public/private pair is merged and evidenced; execution authority remains active | Both worktrees synchronize before the next fixed wave                              |

## Worktree

### `ose-public`

Worktree path: `worktrees/optimize-pr-process/`

Absolute path: `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process/`

The worktree was provisioned before this plan was written and is reused across every public
delivery boundary. It is removed only after the final public PR merges and the safety checks prove
there is no uncommitted or unpushed work.

Canonical provisioning command, run from the `ose-public` repository root:

```bash
claude --worktree optimize-pr-process
```

### `ose-private`

Worktree path: `worktrees/optimize-pr-process/`

Absolute path:
`/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process/`

This worktree was provisioned from private `origin/main` on 2026-08-23 under explicit authority to
retire the private PR-review idea and update its index/links. That action does not authorize private
rule implementation by itself; the later 2026-08-23 full-execution authorization does. Preserve and
reuse this same worktree across every later private delivery boundary, then remove it only after
private closure and safety checks.

Canonical provisioning command, run from the `ose-private` repository root:

```bash
claude --worktree optimize-pr-process
```

The one-public-control-plan shape is a deliberate deviation from the current one-plan-per-repo
workflow. It does not relax the one-worktree-per-repository cap. Exactly one worktree is reused per
repo for the whole plan; no delivery PR creates or owns another worktree.

See the [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
and [Plans Organization Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md).

## Delivery Mode: worktree-to-pr

Both repositories use `worktree-to-pr`:

- integration target: each repository's own `main`;
- one branch and PR per delivery boundary, executed sequentially from the same repo worktree;
- PR branches are pushed by `[AI]`;
- merge is performed by `[AI]` when the hardened current-head preconditions hold, unless the agent
  reaches a decision requiring human authority; every merged PR remains a complete human-readable
  record for later inspection;
- no direct push to `main`; and
- Phase 0 creates no commit, push, or PR.

## Parallelization Model

Read-only evidence probes and independent local checks inside the **same active delivery unit** may
run in parallel when they write no shared path. Branch creation, canonical edits, commit, push, PR
review, merge, and cross-repository propagation remain sequential. At most one PR-producing unit is
active at a time; no dependent PR is stacked on an unmerged head. The matching private unit starts
only after its public source is merged and green, and its paired-wave gate must pass before the next
public unit starts. This preserves one reusable worktree per repository and makes every pause a
stable-main boundary.

### Delivery Boundaries

| Phase | Unit          | Repository    | Branch                                     | Reused worktree                                                      | Exact boundary / exit                                                                  |
| ----- | ------------- | ------------- | ------------------------------------------ | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 0     | Baseline      | Both          | Existing plan branches                     | Each repo's `worktrees/optimize-pr-process/`                         | Formal plan gate and baselines recorded; no commit, push, PR, or implementation        |
| 1     | PLAN          | `ose-public`  | `optimize-pr-process`                      | `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process/`  | Public plan-only PR merged, evidenced, and public worktree synchronized                |
| 2     | PRIV-IDEAS    | `ose-private` | `optimize-pr-process`                      | `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process/` | Private idea-retirement PR merged, linked to PLAN, evidenced, and synchronized         |
| 3     | Scope freeze  | Both          | No new branch                              | Each repo's `worktrees/optimize-pr-process/`                         | Evidence, source claims, delivery ledger, and fixed boundaries frozen; no PR           |
| 4     | PUB-A1        | `ose-public`  | `optimize-pr-process-public-authoring`     | `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process/`  | Public authoring source merged green and pinned; private discharge is the only next PR |
| 5     | PRIV-A1       | `ose-private` | `optimize-pr-process-private-authoring`    | `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process/` | A1 obligation discharged and paired-wave gate passed                                   |
| 6     | PUB-A2        | `ose-public`  | `optimize-pr-process-public-conversation`  | `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process/`  | Public conversation source merged green and pinned; private discharge is next          |
| 7     | PRIV-A2       | `ose-private` | `optimize-pr-process-private-conversation` | `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process/` | A2 obligation discharged and paired-wave gate passed                                   |
| 8     | PUB-A3        | `ose-public`  | `optimize-pr-process-public-loop`          | `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process/`  | Public bounded-loop source merged green and pinned; private discharge is next          |
| 9     | PRIV-A3       | `ose-private` | `optimize-pr-process-private-loop`         | `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process/` | A3 obligation discharged and paired-wave gate passed                                   |
| 10    | PUB-B         | `ose-public`  | `optimize-pr-process-public-planning`      | `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process/`  | Public planning source merged green and pinned; private discharge is next              |
| 11    | PRIV-B        | `ose-private` | `optimize-pr-process-private-planning`     | `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process/` | B obligation discharged and paired-wave gate passed                                    |
| 12    | PUB-C         | `ose-public`  | `optimize-pr-process-public-ci`            | `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process/`  | Conditional public repair merged green and pinned, or public no-change pin recorded    |
| 13    | PRIV-C        | `ose-private` | `optimize-pr-process-private-ci`           | `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process/` | Conditional private repair merged or no-change discharge recorded; C gate passed       |
| 14    | Reconcile     | Both          | No new branch                              | Each repo's `worktrees/optimize-pr-process/`                         | All paired obligations, deviations, corrections, and final pins reconcile              |
| 15    | Private close | `ose-private` | No new branch                              | `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process/` | Private closure artifact complete and private worktree synchronized                    |
| 16    | Verify        | Both          | No new branch                              | Each repo's `worktrees/optimize-pr-process/`                         | Cross-repo evidence and process dogfood complete                                       |
| 17    | Knowledge     | `ose-public`  | `optimize-pr-process-public-closure`       | `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process/`  | Learnings terminally routed on the final closure branch; no PR opens yet               |
| 18    | Final closure | `ose-public`  | `optimize-pr-process-public-closure`       | `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process/`  | Closure/archival PR merged, evidenced, then both owned worktrees safely removed        |

Every PR-producing row above owns exactly one branch and at most one PR. Conditional no-change
rows produce no empty PR. A public row's gate blocks all later work except its matching private
row; a private row's gate blocks the next public row until the pair is terminal.

## Execution Rules

- Keep a live harness task list and a file-touch ledger for both repositories.
- Re-read every foreign commit after merge before continuing from the reused worktree.
- Do not hand-edit `.agents/`, `.opencode/`, or `.codex/`; edit `.claude/` and run
  `npm run generate:bindings`.
- Fix all quality-gate failures at their root cause. If a failure is unrelated and fixing it would
  widen this plan, stop and obtain an explicit scope decision rather than smuggling it into a PR.
- Measure each proposed PR before opening it. Prefer 200/10 and respect the 400/20 local ceiling;
  use a declared atomicity exception only when splitting would make `main` self-contradictory.
- Every delivery PR uses the comment-and-reply contract and bounded cycle policy defined in
  [tech-docs.md](./tech-docs.md).
- Findings and replies target an engineer with bootcamp training and practical coding experience,
  without assuming university/CS coursework; they remain concise, connect evidence to an
  observable consequence, include a reproduction or inspection path, and define only concepts
  needed for the disposition.
- Every delivery PR body names its predecessor/dependency, bounded scope/non-goals, lightest-fit
  feature-flag strategy, proof that the merged intermediate `main` remains coherent, and rollback.
- A PR-body Mermaid diagram is optional only when it materially clarifies architecture, dependency,
  state, or sequence; it must use accessible labels/palette and include adjacent equivalent prose.
  Omit decorative diagrams.
- PR descriptions use progressive disclosure: problem/outcome first; brief reasoned scope and
  non-goals; conceptual summary rather than file inventory; ordered reading and skip paths;
  current-head verification; and deep evidence linked to this plan or canonical governance. Keep
  length proportionate, use headings/bullets/tables sparingly, and omit methodology dumps and
  hidden-schema-first bodies.
- Do not implement or copy a repository rule ad hoc. Invoke
  `repo-governance/workflows/repo/repo-rules-propagation.md` with `isolation=current` inside the
  active repository's sole plan worktree. One run touches one repository.
- Execute portable work as paired waves: PUB-A1 → PRIV-A1, PUB-A2 → PRIV-A2, PUB-A3 → PRIV-A3,
  PUB-B → PRIV-B, then conditional PUB-C → PRIV-C. The private unit begins only from its matching
  merged-green public PR/SHA and records semantic adaptation rather than byte equality.
- Do not create a sixth AI review cycle. A cycle-5 unsafe state becomes an `[AI+HUMAN]` terminal
  decision, not an automatic merge.

## Fixed Delivery Boundaries

The current `optimize-pr-process` plan-only work is the **PLAN establishment boundary**. It contains
the six plan documents plus the explicitly authorized public idea retirement, idea-index update,
and inbound-link cleanup. The deleted briefs are review-skippable only after the human verifies
their disposition table in `README.md`; that table and the deletion are one atomic concern. PLAN may
be staged, committed, pushed, formally validated, and opened as a PR under the user's 2026-08-23
authorization. The later implementation waves are authorized by the same instruction but remain
separate boundaries. PLAN and every public unit use the existing public worktree; Phase 0 opens no
replacement plan PR.

The private idea deletion is a separate **PRIV-IDEAS** plan-document boundary in the already-created
private worktree. Its delivery is authorized by the 2026-08-23 instruction. It depends on merged
PLAN so its short body can link the authoritative disposition; rule implementation remains in the
later separately bounded waves covered by the same full-execution authorization.

Each boundary starts from the latest merged `origin/main` in the existing repo worktree by running
`git switch -C <branch> origin/main`. After merge, fetch, read the full foreign diff, and confirm a
clean worktree before switching to the next named branch.

| Boundary     | Branch                                     | Human-readable concern                                                                            |
| ------------ | ------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| PLAN         | `optimize-pr-process`                      | Six control-plan documents plus public idea retirement/index/link cleanup; no rule implementation |
| PRIV-IDEAS   | `optimize-pr-process`                      | Private idea retirement/index/link cleanup linked to merged PLAN; no rule implementation          |
| PUB-A1       | `optimize-pr-process-public-authoring`     | Wave A1 source: PR body, reading guide, size, atomicity, template                                 |
| PRIV-A1      | `optimize-pr-process-private-authoring`    | Private semantic adaptation of PUB-A1                                                             |
| PUB-A2       | `optimize-pr-process-public-conversation`  | Wave A2 source: teaching findings, replies, audit, AI marker, bindings                            |
| PRIV-A2      | `optimize-pr-process-private-conversation` | Private semantic adaptation of PUB-A2                                                             |
| PUB-A3       | `optimize-pr-process-public-loop`          | Wave A3 source: readiness, scope, bounded cycles, recovery notes, merge exit, bindings            |
| PRIV-A3      | `optimize-pr-process-private-loop`         | Private semantic adaptation of PUB-A3                                                             |
| PUB-B        | `optimize-pr-process-public-planning`      | Wave B source: plan stage ownership, PR delivery, archival, cleanup, bindings                     |
| PRIV-B       | `optimize-pr-process-private-planning`     | Private semantic adaptation of PUB-B                                                              |
| PUB-C        | `optimize-pr-process-public-ci`            | Conditional wave C source: surgical repair of existing CI only                                    |
| PRIV-C       | `optimize-pr-process-private-ci`           | Conditional independent private CI repair                                                         |
| Final public | `optimize-pr-process-public-closure`       | Cross-repo closure, knowledge capture, plan archival                                              |

### Boundary integration-safety record

| Boundary     | Dependency                          | Feature-flag strategy                                                     | Rollback boundary       |
| ------------ | ----------------------------------- | ------------------------------------------------------------------------- | ----------------------- |
| PLAN         | Resolved user decisions             | Dormant non-executable plan                                               | Revert PLAN             |
| PRIV-IDEAS   | Merged PLAN                         | Dormant documentation cleanup; no process activation                      | Revert PRIV-IDEAS       |
| PUB-A1       | Merged PLAN and PRIV-IDEAS          | Ordered activation; old PR bodies remain readable                         | Revert PUB-A1           |
| PRIV-A1      | Merged-green PUB-A1 PR/SHA          | Semantic discharge against the pinned source                              | Revert PRIV-A1          |
| PUB-A2       | Merged PRIV-A1 discharge            | Compatibility bridge for legacy/new replies; rule and binding atomic      | Revert PUB-A2           |
| PRIV-A2      | Merged-green PUB-A2 PR/SHA          | Semantic discharge against the pinned source                              | Revert PRIV-A2          |
| PUB-A3       | Merged PRIV-A2 discharge            | Policy pinned at cycle start; new PRs use new loop                        | Revert PUB-A3           |
| PRIV-A3      | Merged-green PUB-A3 PR/SHA          | Semantic discharge against the pinned source                              | Revert PRIV-A3          |
| PUB-B        | Merged PRIV-A3 discharge            | Existing plans retain declared contract; new plans activate new lifecycle | Revert PUB-B            |
| PRIV-B       | Merged-green PUB-B PR/SHA           | Ordered activation for new private plans                                  | Revert PRIV-B           |
| PUB-C        | Merged PRIV-B plus necessity proof  | Atomic tested repair or explicit no-change source                         | Revert PUB-C with test  |
| PRIV-C       | Merged-green PUB-C or no-change pin | Independent private proof; semantic discharge or explicit N/A             | Revert PRIV-C with test |
| Final public | All tracks terminal                 | Ordered archival after implementation                                     | Revert closure PR       |

### Repeatable same-worktree transition

For **each** PR-producing phase, instantiate the following as separate unit-prefixed completion
records using that phase's repository, branch, paths, commands, and PR body. This is a repeated
atomic checklist, not one global sign-off; no item may be combined with its neighbor:

- [ ] [AI] **Branch sync**: run `git status --porcelain`, `git fetch origin`, and `git switch -C
<boundary-branch> origin/main` except PLAN/PRIV-IDEAS, whose already-authored branches are
      verified without discarding edits; acceptance: the unit starts unstacked in the one worktree.
- [ ] [AI] **Canonical edit**: edit only the active boundary's file-touch ledger paths and invoke
      the canonical rule workflow where applicable; acceptance: `git status --short` has no path
      owned by another unit.
- [ ] [AI] **Size/cohesion** `[Repo-grounded]`: before commit, run `git diff --numstat origin/main`,
      `git diff --name-only origin/main`, and `git ls-files --others --exclude-standard`; count
      untracked hand-authored lines with `wc -l <path>` for every listed file. After commit, rerun
      `git diff --numstat origin/main...HEAD` and `git diff --name-only origin/main...HEAD` as the
      immutable PR-head check. Acceptance: pre-commit and committed counts include staged,
      unstaged, and untracked work; generated paths are separated; and the one-problem judgment is
      recorded, or execution stops for a stable-main split and plan amendment.
- [ ] [AI] **Stage-gate setup and local gates**: after the active boundary's edits are complete, run
      `git add -- <each-explicit-active-ledger-path>`, reconcile `git diff --cached --name-only`
      exactly against the changed paths owned by that boundary, and run the `Before commit — staged
paths` checks under `Local Quality Gates Before Any Push` plus the exact checks named by the
      active phase; acceptance: all required exit codes are 0, pre-commit mutations remain inside
      the active ledger, and the reconciled cache is the proposed commit rather than an incidental
      staging area.
- [ ] [AI] **PR body/ledger**: create `local-tmp/pr-bodies/<boundary>.md`; acceptance: it contains
      dependency, scope/non-goals, reading guide, review focus, verification, PR-native obligation
      entry, integration safety, stable-main proof, rollback, and diagram/omission decision.
- [ ] [AI] **Commit**: do not blanket-restage; re-run `git diff --cached --name-only` and inspect
      `git diff --cached` against the active ledger, repeat the stage-gate setup and pre-commit run
      if any owned file changed afterward, then commit the already-validated staged paths with the
      phase's conventional commit; acceptance: no unowned path entered the cache and the committed
      tree is the exact cache that passed the staged-path gates.
- [ ] [AI] **Push/open**: run the `After commit — before push` checks under `Local Quality Gates
Before Any Push`, then push the fixed branch and open exactly one PR against that repository's
      `main`; acceptance: the pre-push surface is green, the URL is recorded, and no dependent PR is
      open.
- [ ] [AI] **Review/fix/CI**: run the bounded comment/reply cycle and poll `rtk proxy gh pr checks
<PR> --repo wahidyankf/<REPO>`; acceptance: dispositions are terminal and checks are green on
      the reviewed head.
- [ ] [AI] **Merge**: merge only that reviewed head; acceptance: the native PR records the merge
      SHA and no scope/defect/cycle waiver was used.
- [ ] [AI] **Evidence/worktree resync**: fetch `origin/main`, read the complete landed diff, verify
      the merge SHA and clean worktree, and record the next permitted boundary; acceptance: the
      phase gate can be evaluated without local hidden state.

- [ ] [AI] Before every boundary, from the repository root run `git worktree list --porcelain` and
      verify exactly one line ends in `/worktrees/optimize-pr-process`; acceptance: the existing
      plan worktree is reused and no worktree-per-PR exists.
- [ ] [AI] After every merge, in that same worktree run `git status --porcelain`, `git fetch origin`,
      inspect `git log --oneline --decorate HEAD..origin/main` and the full landed diff, and align to
      `origin/main`; only when the next unit assigned to that repository begins, run `git switch -C
<next-fixed-branch-from-table> origin/main`. Acceptance: the other repository's matching wave
      runs first where required, and every next PR begins unstacked from latest merged state.
- [ ] [AI] Before opening every PR, add `Dependency`, `Feature flag / integration safety`, `Stable
main`, and `Rollback` paragraphs to its body; acceptance: a human can explain why the prior
      and next delivery units are ordered and how to reverse this one independently.

### Canonical rule-boundary run

Apply these steps to every PUB-A1/A2/A3/PUB-B and PRIV-A1/A2/A3/PRIV-B boundary. They invoke the
canonical workflow; they are not a parallel manual-copy procedure.

- [ ] [AI] Invoke `repo-governance/workflows/repo/repo-rules-propagation.md` with the boundary's
      decided rule batch, `mode=strict`, and `isolation=current` from the active repository plan
      worktree; acceptance: the run uses no second worktree and its ledger is limited to that
      boundary's file-impact paths.
- [ ] [AI] Complete Step 0 before any write; acceptance: each obligation has one imperative
      statement, separate `Why`, a passing observation, and a violating observation, while any
      unfalsifiable statement halts with a specific blocker.
- [ ] [AI] Complete Steps 2–4 before any write using subject/verb/surface conflict searches that
      accumulate wrapped statements; acceptance: classification, precedence, supersession, and the
      narrowest placement are recorded, and a higher-layer conflict is escalated rather than
      overwritten.
- [ ] [AI] Complete Steps 5–6 within the classified subject; acceptance: any eviction lands in the
      same PR, every subject surface has a change/no-change verdict, duplicates/supersessions and
      indexes are reconciled, no word budget is raised, `.claude/` remains the hand-authored source,
      and affected bindings are generated rather than hand-edited.
- [ ] [AI] Complete Step 7 for every normalized rule; acceptance: the disposition is `covered` only
      when an existing gate is proven to fail the violating observation and pass the conforming
      observation, otherwise human-judgment PR rules record `unenforced by decision — <reason>`.
      Do not declare or build a new validator by default; route any proposed new gate behavior
      through the separate mechanism-necessity/application-plan boundary.
- [ ] [AI] Complete Step 8 with asserted exit codes; acceptance: generated bindings, deterministic
      surface gates, composed repo-rules quality gate at strict mode, demonstrated baseline, and
      ledger/status reconciliation all pass without absorbing unrelated findings.
- [ ] [AI] Complete Step 9 on the fixed boundary branch; acceptance: explicit ledger paths alone
      are staged, and the concise PR-native manifest summary lists normalized rule, destination,
      disposition, supersession/eviction, tidy result, checks, and sibling obligation/discharge.
      The body links deep evidence rather than copying the local generated report.
- [ ] [AI] For a public portable-rule run, record `sibling-obligation: ose-private` and do not edit
      the sibling; acceptance: the obligation remains open until the public PR merges and the
      corresponding separate private run links the merged source and records `discharged` in its
      own PR.

### Cross-repository anti-chain-reaction protocol

The execution DAG is paired and sequential:
`PLAN → PRIV-IDEAS → PUB-A1 → PRIV-A1 → PUB-A2 → PRIV-A2 → PUB-A3 → PRIV-A3 → PUB-B → PRIV-B →
PUB-C? → PRIV-C? → closure`. A question mark means the C wave may terminate with an explicit
no-change record. No dependent node starts from a draft, and no stacked PR substitutes for a merged
edge.

- [ ] [AI] After each public wave merges, record its source pin in the public PR and matching private
      PR draft: public PR URL, merge SHA, reviewed head, required-check URLs/states, normalized rule
      or behavior class, and sibling obligation; acceptance: private editing starts only when the
      pin is merged, green, and readable from native PR artifacts.
- [ ] [AI] Before each private write, fetch both repositories and prove the source pin is still the
      merged public canonical source; acceptance: the private PR links the pin, names its private
      base SHA, and describes semantic correspondence and deliberate deviations. Byte identity is
      neither required nor claimed unless the affected surface has an explicit byte-identity rule.
- [ ] [AI] Record the obligation ledger in native PR bodies/threads rather than a hidden local
      schema; acceptance: each entry contains obligation ID/class, public pin, private disposition,
      deviation or correction link, current status, and superseded pin when applicable. No new bot,
      parser, registry, database, or validator is introduced.
- [ ] [AI] Classify every discovery made during private discharge before editing:
  - `private-only`: repair only the private unit and cite why public semantics are unaffected;
  - `repo-specific deviation`: adapt privately and record the reason in the deviation evidence;
  - `portable source defect`: stop the private unit and repair the public canonical source first;
  - `byte-identity`: stop ordinary semantic propagation and use the existing byte-parity contract
    for that exact surface.
    Acceptance: one classification and its evidence appear in the originating private thread; bare
    “sync drift” is not a classification.
- [ ] [AI] **Pre-push portable-source discovery** `[Judgment call]`: stop private editing before
      push/open; record branch, `HEAD`, base SHA, changed paths, and evidence in the obligation
      ledger, then create one explicit-path checkpoint commit when verified edits exist. Acceptance:
      no private PR exists, the local state is recoverable without stash/reset/dirty rebase, and the
      conditional correction transaction below begins.
- [ ] [AI] **Post-open/review portable-source discovery** `[Judgment call]`: keep the originating
      private finding thread, reply `blocked — portable source correction required`, post an
      AI-marked PR comment with old source pin and correction branch, mark the PR blocked, and close
      it unmerged as `superseded` only after its head/base/paths/checks are pinned. Acceptance: no
      history is erased, the closed PR links the correction and planned replacement, and no two
      private PRs for the unit remain open concurrently.
- [ ] [AI] **Conditional public correction transaction**: substitute the fixed wave slug (`a1`,
      `a2`, `a3`, or `b`) in branch
      `optimize-pr-process-public-<wave>-source-correction-1`, start it from public `origin/main`,
      and execute the full Repeatable same-worktree transition plus Canonical rule-boundary run and
      Local Quality Gates. Acceptance: the one allowed source-correction PR is independently
      reviewable, current-head green, merged, and PR-native; unrelated terminal waves remain valid.
- [ ] [AI] **Conditional private resume/replacement transaction**: after correction merge, mark the
      old pin `superseded`, record the new pin, and create branch
      `optimize-pr-process-private-<wave>-resume-1` from private `origin/main`; cherry-pick only a
      verified checkpoint when one exists. Run the full Repeatable same-worktree transition,
      Canonical rule-boundary run, and Local Quality Gates. Acceptance: pre-push discovery opens the
      unit's sole private PR from the resume branch; post-open discovery opens exactly one linked
      replacement PR after the old PR is closed, and only the affected class is revalidated.
- [ ] [AI+HUMAN] Enforce exactly one upstream public correction per wave **total**, irrespective of
      how many obligation classes are implicated. Multiple non-cohesive classes require a plan
      amendment and human replan instead of multiple correction PRs; any second upstream reversal
      or restoration of retired semantics is oscillation. Acceptance: execution stops with the
      competing pins/evidence and stable options, while unrelated terminal units remain valid.
- [ ] [AI] Before advancing to the next wave, query both PRs and record that all obligation threads
      are resolved by evidence, both current heads are merged/green, neither worktree has residue,
      and the next boundary starts from its own repository's current `origin/main`; acceptance: the
      pair is terminal, reversible, auditable, and unstacked.

Conditional recovery is part of the triggering wave, not an improvised extra wave:

| Conditional unit          | Repository | Fixed branch pattern                                    | PR-native terminal state                                                       |
| ------------------------- | ---------- | ------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `PUB-<WAVE>-CORRECTION-1` | public     | `optimize-pr-process-public-<wave>-source-correction-1` | one merged correction PR                                                       |
| `PRIV-<WAVE>-RESUME-1`    | private    | `optimize-pr-process-private-<wave>-resume-1`           | one merged private PR, or one closed superseded PR plus one merged replacement |

Both conditional units inherit the triggering wave's file-impact owner and correction budget; no
new path enters scope. Every comment/reply/body in this recovery route ends with the exact footer:

```text
---

Generated by AI
```

## File-Touch Ledger

Update this table at the end of each phase and reconcile it against `git status --short` in both
worktrees. Add a path before editing it; any unlisted path is out of scope until this plan is
updated and re-checked.

| Repository    | Planned maximum surface                                                                     | Actual paths                                                                                                     | Boundary                                                  |
| ------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `ose-public`  | Plan docs plus authorized idea/index/link retirement; later paths in the public impact tree | Current IDEA-CONSOLIDATION paths recorded in the public impact tree; populate later boundaries during execution  | IDEA-CONSOLIDATION / PUB-A1/A2/A3 / PUB-B / PUB-C / final |
| `ose-private` | Authorized idea/index/link retirement; later paths in the private impact tree               | Current IDEA-CONSOLIDATION paths recorded in the private impact tree; populate later boundaries during execution | IDEA-CONSOLIDATION / PRIV-A1/A2/A3 / PRIV-B / PRIV-C      |

## Phase 0: Authorized Plan Gate and Baseline

- [x] [HUMAN] Record the 2026-08-23 authorization for the formal plan gate, PLAN, PRIV-IDEAS, and
      full execution; acceptance: the authorization ledger names all four transitions.
- [x] [AI] Run the authorized formal plan gate against only the plan and authorized idea-retirement
      paths, then apply revalidated in-scope findings; acceptance: no rule, binding, workflow,
      application, or library path enters either ledger.
- [x] [AI] In `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process`, run `npm install`
      and `npm run doctor -- --fix`; acceptance: both exit 0 and any toolchain changes are either
      absent or recorded in the ledger before continuing.
- [x] [AI] In `/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process`, run `npm install`
      and `npm run doctor -- --fix`; acceptance: both exit 0 and no secret-bearing environment file
      is read, created, or modified.
- [x] [AI] Record both baseline SHAs, gate result, worktree identities, and `git status --short`;
      acceptance: Phase 0 creates no commit, push, PR, or implementation edit.

### Phase 0 Gate

> All checks below must pass before starting PLAN delivery in Phase 1.

- [x] [AI] Run `git status --short` in both worktrees; acceptance: every Phase 0 toolchain change is
      explicitly reconciled in the ledger, with no unknown file.
- [x] [AI] Confirm the resolved user-decision envelope and formal-plan result are attached to the
      orchestration record; PLAN and PRIV-IDEAS remain unmerged at this boundary.
- [x] [AI] Confirm no commit, push, or PR occurred in Phase 0; acceptance: the recorded SHA/API
      evidence agrees.
- [x] [AI] In each repository root, run `git worktree list --porcelain | rg -c
'^worktree .*/worktrees/optimize-pr-process$'`; acceptance: each command returns exactly `1`.

Phase 0 evidence recorded on 2026-08-23:

- formal audit chain `378d66` passed after two consecutive zero-finding strict checks;
- public baseline: branch `optimize-pr-process`, `HEAD` and `origin/main`
  `800ad2cc0999bfb8ee4662963823a52b1419b40f`;
- private baseline: branch `optimize-pr-process`, `HEAD` and `origin/main`
  `718c20c923707d777a89639f760f98d53740bd70`;
- `npm install` and `npm run doctor -- --fix` passed in both worktrees with 16/16 tools available;
- both worktree-count probes returned `1`; and
- Git status after tool convergence contained only the authorized public PLAN ledger and private
  PRIV-IDEAS ledger. No Phase 0 commit, push, PR, implementation edit, or environment-file change
  occurred.

> **Pause Safety**: both repo-scoped worktrees are synchronized and dependencies are converged, but
> no implementation change has been committed or published. Safe to stop. To resume: run
> `git status --short` in both worktrees and compare each `HEAD` with its recorded Phase 0 SHA.

## Phase 1: Deliver PLAN

- [ ] [AI] **Branch sync**: in the public worktree run `git fetch origin`, verify the current branch
      is `optimize-pr-process`, and record `git merge-base HEAD origin/main`; acceptance: the
      existing plan branch and worktree are reused without discarding plan edits.
- [ ] [AI] **Canonical edit**: apply only formal-gate fixes to
      `plans/in-progress/optimize-pr-process/`, add `optimize-pr-process` to
      `plans/in-progress/README.md`, and apply the authorized public idea/index/link paths;
      acceptance: the active-plan index no longer says there are no active plans,
      `git status --short` matches the PLAN ledger, and no implementation path appears.
- [ ] [AI] **Size**: run the pre-commit worktree-aware and committed-head size commands in
      `Repeatable same-worktree transition`; acceptance: PLAN counts include staged, unstaged, and
      untracked work, remain one plan-establishment concern, and explain human-reviewable atomicity.
- [ ] [AI] **Local gates**: run the plan-authorized checks and `git diff --check`; acceptance: all
      required checks exit 0 and every failure is resolved within PLAN scope.
- [ ] [AI] **PR body/ledger**: draft `local-tmp/pr-bodies/PLAN.md` with scope/non-goals, reading
      guide, review focus, verification, integration safety, rollback, and exact ledger paths;
      acceptance: it says plan-only and links rather than duplicates deep rationale.
- [ ] [AI] **Commit**: stage explicit PLAN ledger paths and run `git commit -m "docs(plans): plan PR
process improvements"`; acceptance: `git diff --cached --name-only` contained no unowned path.
- [ ] [AI] **Push/open**: push `optimize-pr-process` and open one PR against public `main` using the
      PLAN body; acceptance: the PR URL is recorded and no other PR is opened in this phase.
- [ ] [AI] **Review/fix/CI**: run the plan review/fixer cycle and poll current-head checks;
      acceptance: every finding has a same-thread disposition and all required checks are green.
- [ ] [AI] **Merge**: merge only the reviewed current head; acceptance: public `main` contains PLAN
      and the PR records its merge SHA.
- [ ] [AI] **Evidence/resync**: fetch public `origin/main`, read the complete landed diff, and verify
      the same public worktree is clean; acceptance: PLAN's merged-green pin is ready for PRIV-IDEAS.

### Phase 1 Gate

> All checks below must pass before starting PRIV-IDEAS in Phase 2.

- [ ] [AI] Verify PLAN is merged, green, auditable, and contains no implementation path; acceptance:
      PRIV-IDEAS is the only permitted next PR.

> **Pause Safety**: PLAN is merged and the public worktree is clean. Safe to stop. To resume: verify
> the recorded PLAN merge SHA is an ancestor of public `origin/main`.

## Phase 2: Deliver PRIV-IDEAS

- [ ] [AI] **Branch sync**: fetch private `origin/main`, verify the existing private branch is
      `optimize-pr-process`, and record its base; acceptance: the one private worktree is reused.
- [ ] [AI] **Canonical edit**: limit edits to authorized private idea/index/link retirement;
      acceptance: the ledger links merged PLAN and contains no rule implementation.
- [ ] [AI] **Size**: run the pre-commit worktree-aware and committed-head size commands in
      `Repeatable same-worktree transition`; acceptance: counts include untracked private work and
      the unit remains one documentation-retirement concern.
- [ ] [AI] **Local gates**: run private Markdown/link/sync checks and `git diff --check`; acceptance:
      all required checks exit 0.
- [ ] [AI] **PR body/ledger**: draft `local-tmp/pr-bodies/PRIV-IDEAS.md`; acceptance: it links PLAN,
      names exact paths, integration safety, rollback, and the no-implementation boundary.
- [ ] [AI] **Commit**: stage explicit private ledger paths and commit thematically; acceptance: no
      unowned path is staged.
- [ ] [AI] **Push/open**: push the existing private plan branch and open one private PR; acceptance:
      no other PR opens in Phase 2.
- [ ] [AI] **Review/fix/CI**: complete native review/replies and current-head checks; acceptance:
      every finding is disposed and checks are green.
- [ ] [AI] **Merge**: merge the reviewed private head; acceptance: private `main` contains only the
      authorized retirement.
- [ ] [AI] **Evidence/resync**: fetch private `origin/main`, read the landed diff, and verify the
      reused worktree is clean; acceptance: PLAN/PRIV-IDEAS pins are linked and terminal.

### Phase 2 Gate

> All checks below must pass before starting scope freeze in Phase 3.

- [ ] [AI] Verify both document-only PRs are merged and both worktrees are clean; acceptance: no
      implementation branch exists and Phase 3 may freeze evidence.

> **Pause Safety**: PLAN and PRIV-IDEAS are terminal. Safe to stop. To resume: verify both recorded
> merge SHAs against their current `origin/main`.

## Phase 3: Freeze Evidence, Scope, and Source Claims

- [ ] [AI] Re-measure `ose-public#249` with the four `rtk proxy gh`/GraphQL recipes in
      `tech-docs.md` and record the metadata, thread count, consolidated cycle count, workflow-run
      count, final-cycle URL, and merge-audit URL in the implementation notes; acceptance: values
      either match the plan baseline or the discrepancy is corrected in all six plan documents
      before policy work begins.
- [ ] [AI] Re-measure `ose-private#62` with the same recipes; acceptance: metadata, 76 thread/reply
      states, consolidated artifacts, workflow runs, checkpoint, cycle-11 URL, and merge-audit claims
      are reconciled against the PR artifact and any discrepancy is corrected in this plan.
- [ ] [AI] In the public worktree, run an explicit contradiction inventory:
      `rg -n -i "maximum_cycles|ceiling N|seven-cycle|7-cycle|seven cycles|up to seven|of 7|default
seven|two consecutive clean|one clean|extend per-PR|origin main|direct push|machine-readable"
repo-governance .claude .github plans`; acceptance: the known-positive
      `repo-governance/workflows/pr/pr-review-quality-gate/loop-algorithm.md` match is present, every
      public PR/planning-lifecycle match is assigned to PUB-A, PUB-B, or PUB-C, and name-only links,
      historical evidence, unrelated checker/fixer ceilings, and other numeric uses each receive an
      explicit no-change verdict; each private class inventory remains deferred to its matching
      interleaved private wave.
- [ ] [AI] Partition the decided PR/planning rules into the PUB-A1/A2/A3/PUB-B canonical propagation
      inputs without writing a rule surface; acceptance: each input names its subject and intended
      behavior but leaves normalization, conflict scanning, and placement to Steps 0–4, and the
      ledger records that each public run uses `isolation=current` and owes `ose-private` at Step 9.
- [ ] [AI] Read the 22 external sources listed in `README.md` from their authoritative URLs and
      update the source-verification table in `tech-docs.md` only when the current text no longer
      supports the claim; acceptance: every external claim remains `[Web-cited]`, access-dated, and
      conservatively paraphrased, with Stripe clearly limited to CI analogy and no source described
      as setting a universal five-cycle maximum.
- [ ] [AI] Freeze delivery scope from the `README.md` in-scope/out-of-scope table and
      `tech-docs.md` scope decision matrix; acceptance: each PR draft contains only its concise
      boundary/non-goals and links the plan for the full matrix, so every later finding can be
      classified without copying a methodology dump or inventing a new boundary.
- [ ] [AI] Copy the dependency/integration-safety matrix from `tech-docs.md` into the execution
      ledger and assign each fixed boundary its predecessor, feature-flag strategy, stable-main
      invariant, and rollback command; acceptance: no boundary is “TBD” before its first edit.
- [ ] [AI] For every planned PR, decide whether architecture/dependency/state/sequence is materially
      clearer with Mermaid and record `diagram: required` or `diagram: omitted — <reason>` in its
      body draft; acceptance: every required diagram uses the accessible palette and has an adjacent
      prose equivalent, while no decorative diagram is scheduled.
- [ ] [AI] Reconcile the nine retired idea briefs against the disposition table in `README.md` and
      the active boundary ledger; acceptance: every valid requirement has a PUB/PRIV owner, the bot
      identity and new validator/registry proposals are explicitly rejected, independent ideas such
      as merge-queue adoption remain indexed, and no deleted brief remains an unresolved dependency.

### Phase 3 Gate

> All checks below must pass before starting PUB-A1 in Phase 4.

- [ ] [AI] Compare both PR measurements with the plan's baseline; acceptance: each numeric claim is
      reproducible from linked GitHub artifacts or corrected before implementation.
- [ ] [AI] Review the ledger against `tech-docs.md` file-impact trees; acceptance: no application,
      library, spec, infrastructure, dashboard, database, parser, bot, or hosted-service path appears
      except the explicitly reserved existing PUB-C/PRIV-C workflow, registry, Rhino runner,
      validator, test, and Gherkin paths. Those conditional paths have `reserved/untouched` status
      and no write authority until their Phase 12/13 necessity decision passes.
- [ ] [AI] Run `git diff --check -- plans/in-progress/optimize-pr-process`; acceptance: exit 0.
- [ ] [AI] Review every fixed boundary row; acceptance: dependency, scope, feature-flag strategy,
      stable-main proof, and rollback are explicit, and exactly one worktree per repo is recorded.
- [ ] [AI] Verify the propagation-run ledger; acceptance: every portable public rule boundary has
      one planned public run and one separate post-merge private discharge run, with no run assigned
      write authority in both repositories.

> **Pause Safety**: evidence and scope are frozen, while governance and bindings remain unchanged.
> Safe to stop. To resume: rerun the contradiction inventory and compare it with the ledger.

## Phase 4: Deliver PUB-A1 — Human-Readable Authoring

- [ ] [AI] In the public worktree, run
      `git switch -C optimize-pr-process-public-authoring origin/main`; invoke the Canonical
      rule-boundary run for PUB-A1 over the PR-body/size/atomicity conventions and
      `.github/pull_request_template.md` listed in `tech-docs.md`. Acceptance: the placed rules
      implement progressive-disclosure core sections including compact `Review Focus` and `Related
      Work`, conditional `Risk and Rollout` and `Visual Evidence` sections that are removed when
      empty, accessible-diagram/prose-equivalent behavior, 200/10 preference, 400/20 local ceiling,
      cohesion-first review, and human enforcement; `rg -n
"200|400|Reading Guide|Review Focus|Related Work|Visual Evidence|Enforcement"
repo-governance/conventions/structure/plans/prs-open-at-delivery-boundaries-pr-*` shows one
      non-contradictory policy and no industry-standard or mandatory-diagram claim.
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] **PUB-A1 size/cohesion**: run the pre-commit and committed size commands in
      `Repeatable same-worktree transition`; acceptance: counts include staged, unstaged, and
      untracked work, separate generated paths, and record one authoring concern.
- [ ] [AI] **PUB-A1 local gates**: run every command under `Local Quality Gates Before Any Push`;
      acceptance: each exits 0 in the public worktree and the body contains the ordered reading guide.
- [ ] [AI] Complete canonical Step 9 for PUB-A1 using commit subject
      `docs(pr): make PRs readable to humans`; acceptance: the Step 9 PR body contains the concise
      manifest summary and `sibling-obligation: ose-private`, links deep rationale, contains the
      required progressive-disclosure sections, records the PR URL, and uses no direct push to
      `main`.
- [ ] [AI] **PUB-A1 review/fix**: run the bounded review cycle and reply in each native thread;
      acceptance: every finding has one terminal evidence-backed disposition.
- [ ] [AI] **PUB-A1 current-head CI**: run `rtk proxy gh pr checks <PR> --repo
wahidyankf/ose-public`; acceptance: required checks are green on the reviewed head.
- [ ] [AI] **PUB-A1 merge**: merge only the reviewed current head; acceptance: the PR records its
      merge SHA and no waiver is used.
- [ ] [AI] **PUB-A1 evidence/resync**: fetch public `origin/main`, read the full landed diff, and run
      `git status --porcelain`; acceptance: the worktree is clean and the merged-green pin is
      recorded before PRIV-A1.

### Phase 4 Gate

> All checks below must pass before starting PRIV-A1 in Phase 5.

- [ ] [AI] Verify PUB-A1 is merged/green, its obligation and exact source pin are public, and the
      public worktree is clean; acceptance: no later public unit starts before PRIV-A1.

> **Pause Safety**: PUB-A1 is merged and reversible; PRIV-A1 is the only permitted next PR. Safe to
> stop. To resume: recheck the recorded PUB-A1 SHA and required checks.

## Phase 5: Deliver PRIV-A1 — Authoring Discharge

- [ ] [AI] In the private worktree run `git switch -C optimize-pr-process-private-authoring
origin/main`, fetch the merged PUB-A1 pin, run the private contradiction scan for the authoring
      class, and invoke the Canonical rule-boundary run for PRIV-A1; acceptance: the private PR
      describes semantic alignment/deviations, classifies every downstream discovery, and writes no
      byte-identity claim without an existing byte-parity contract.
- [ ] [AI] **PRIV-A1 size/cohesion**: run the pre-commit and committed size commands in
      `Repeatable same-worktree transition`; acceptance: the private unit remains one authoring
      discharge and includes untracked work.
- [ ] [AI] **PRIV-A1 local gates**: run every command under `Local Quality Gates Before Any Push` in
      the private worktree; acceptance: each exits 0.
- [ ] [AI] **PRIV-A1 Step 9**: complete canonical Step 9; acceptance: the PR body links the final
      PUB-A1 pin and marks the obligation `discharged` or enters the bounded correction route.
- [ ] [AI] **PRIV-A1 review/fix**: complete bounded native review and same-thread replies;
      acceptance: every finding is terminal.
- [ ] [AI] **PRIV-A1 current-head CI**: run `rtk proxy gh pr checks <PR> --repo
wahidyankf/ose-private`; acceptance: required checks are green on the reviewed head.
- [ ] [AI] **PRIV-A1 merge**: merge only the reviewed head; acceptance: the PR records its merge SHA.
- [ ] [AI] **PRIV-A1 evidence/resync**: fetch private `origin/main`, read the full landed diff, and
      run `git status --porcelain`; acceptance: both worktrees are clean before PUB-A2.

### Phase 5 Gate

> All checks below must pass before starting PUB-A2 in Phase 6.

- [ ] [AI] Verify the A1 obligation is discharged against the final public pin and both current
      mains are green; acceptance: the paired-wave gate explicitly permits PUB-A2.

> **Pause Safety**: A1 is terminal in both repositories. Safe to stop. To resume: reconcile its two
> PR-native ledger entries before creating PUB-A2.

## Phase 6: Deliver PUB-A2 — Review Conversation

- [ ] [AI] Run `git switch -C optimize-pr-process-public-conversation origin/main`, then invoke the
      Canonical rule-boundary run for PUB-A2 over `review-as-teaching.md`,
      finding-disposition, synthesis/fixer skill references, and affected agent sources to implement
      practical-junior-readable findings, four-way critical appraisal,
      same-thread resolution, native audit primacy, and the exact AI footer. Acceptance: normative
      prose and binding templates match the shapes in `tech-docs.md`; they assume practical coding
      ability but no university/CS coursework in algorithms, operating systems, compilers,
      distributed systems, security, or architecture; each finding is concise and includes an
      observable consequence, reproduction/inspection path, and bounded remedy; Teaching/FYI is
      nonblocking; the hidden schema has no mandatory status without a demonstrated consumer; the
      public applicability/disposition shard either contains the rule its frontmatter promises or
      the promise and empty shard are retired together; PR-review indexes use meaningful annotations;
      and agent references resolve through the catalog or a tracked path rather than stale layout
      guesses.
  - _Suggested executor: `agent-maker`_
- [ ] [AI] **PUB-A2 size/cohesion**: run the worktree-aware size commands; acceptance: normative
      prose and binding remain one cohesive review-conversation concern.
- [ ] [AI] **PUB-A2 local gates**: run `npm run generate:bindings` and every command under `Local
Quality Gates Before Any Push`; acceptance: all exit 0 and mirrors match `.claude/`.
- [ ] [AI] **PUB-A2 Step 9**: complete canonical Step 9 with commit subject
      `docs(pr): make review a traceable conversation`; acceptance: the PR records
      `sibling-obligation: ose-private` and the exact AI footer.
- [ ] [AI] **PUB-A2 review/fix**: run bounded review and same-thread dispositions; acceptance: every
      thread is terminal and reasoned.
- [ ] [AI] **PUB-A2 current-head CI**: run `rtk proxy gh pr checks <PR> --repo
wahidyankf/ose-public`; acceptance: required checks are green on the reviewed head.
- [ ] [AI] **PUB-A2 merge**: merge only the reviewed head; acceptance: the PR records its merge SHA.
- [ ] [AI] **PUB-A2 evidence/resync**: fetch/read public `origin/main` and run
      `git status --porcelain`; acceptance: the clean worktree and merged-green source pin are
      recorded before PRIV-A2.

### Phase 6 Gate

> All checks below must pass before starting PRIV-A2 in Phase 7.

- [ ] [AI] Verify PUB-A2 is merged/green, auditable, and pinned; acceptance: PRIV-A2 is the only
      permitted next PR.

> **Pause Safety**: PUB-A2 is merged and reversible. Safe to stop. To resume: recheck its exact pin
> and unresolved-thread count.

## Phase 7: Deliver PRIV-A2 — Conversation Discharge

- [ ] [AI] In the private worktree run `git switch -C optimize-pr-process-private-conversation
origin/main`, fetch the merged PUB-A2 pin, scan only the conversation/audit class, and invoke
      the Canonical rule-boundary run for PRIV-A2; acceptance: private-only defects and deliberate
      deviations stay private, meaningful PR-review index annotations and catalog-resolving agent
      references are verified in `repo-governance/workflows/pr/pr-review-quality-gate.md`,
      `participants-part-2.md`,
      `repo-governance/development/quality/pr-review-disciplines/rollback-trigger-d6.md`, and
      `.claude/skills/pr-review-synthesis-coordination/SKILL.md`, while any portable source defect
      stops the run and returns to public.
- [ ] [AI] **PRIV-A2 size/cohesion**: run the worktree-aware size commands; acceptance: the unit is
      one private conversation discharge and includes untracked work.
- [ ] [AI] **PRIV-A2 local gates**: run every command under `Local Quality Gates Before Any Push`;
      acceptance: all exit 0 in private.
- [ ] [AI] **PRIV-A2 Step 9**: complete canonical Step 9; acceptance: the final PUB-A2 pin and
      downstream classifications are in the PR-native ledger.
- [ ] [AI] **PRIV-A2 review/fix**: run bounded review and same-thread replies; acceptance: every
      finding is terminal.
- [ ] [AI] **PRIV-A2 current-head CI**: run `rtk proxy gh pr checks <PR> --repo
wahidyankf/ose-private`; acceptance: required checks are green on the reviewed head.
- [ ] [AI] **PRIV-A2 merge**: merge only the reviewed head; acceptance: the PR records its merge SHA.
- [ ] [AI] **PRIV-A2 evidence/resync**: fetch/read private `origin/main` and run
      `git status --porcelain`; acceptance: both worktrees are clean before PUB-A3.

### Phase 7 Gate

> All checks below must pass before starting PUB-A3 in Phase 8.

- [ ] [AI] Verify the A2 obligation is discharged and both repositories are green; acceptance: the
      paired-wave gate explicitly permits PUB-A3.

> **Pause Safety**: A2 is terminal. Safe to stop. To resume: reconcile its public/private pins.

## Phase 8: Deliver PUB-A3 — Bounded Review Loop

- [ ] [AI] Run `git switch -C optimize-pr-process-public-loop origin/main`, then invoke the Canonical
      rule-boundary run for PUB-A3 over scope guard, deferral, loop,
      readiness, convergence, probe, merge-precondition, affected skills, and
      scout/synthesis/fixer agent sources. Acceptance: cycle 1 starts only on a complete,
      self-reviewed, scoped, documented, locally checked head and performs the whole selected probe;
      the fixer closes one cohesive evidence-backed batch; cycles 2–3 narrow to delta/final and exit
      as soon as safe; cycles 4–5 require changed-strategy recovery notes but no human pre-approval;
      5 is the hard maximum and cycle 6 is forbidden; a second occurrence of one causal family
      charters the next bounded root-cause/invariant pass; class closure inspects definitions,
      producers, consumers, validators, root instructions, normative copies, exclusions, and the
      enclosing edited block; classifier evidence has one concrete human-readable definition; and
      the cap never waives a defect.
  - _Suggested executor: `agent-maker`_
- [ ] [AI] **PUB-A3 size/cohesion**: run the worktree-aware size commands; acceptance: all active
      loop-rule edits remain one bounded lifecycle concern.
- [ ] [AI] **PUB-A3 local gates**: run `npm run generate:bindings` and every command under `Local
Quality Gates Before Any Push`; acceptance: all exit 0 and every active seven/unbounded rule
      is removed from PUB-A3-owned surfaces.
- [ ] [AI] **PUB-A3 Step 9**: complete canonical Step 9 with commit subject
      `docs(pr): bound the AI review loop`; acceptance: the manifest records
      `sibling-obligation: ose-private` and the source pin contract.
- [ ] [AI] **PUB-A3 review/fix**: run bounded review and same-thread replies; acceptance: no sixth
      cycle exists and every finding is terminal.
- [ ] [AI] **PUB-A3 current-head CI**: run `rtk proxy gh pr checks <PR> --repo
wahidyankf/ose-public`; acceptance: required checks are green on the reviewed head.
- [ ] [AI] **PUB-A3 merge**: merge only the reviewed head; acceptance: the PR records its merge SHA.
- [ ] [AI] **PUB-A3 evidence/resync**: fetch/read public `origin/main` and run
      `git status --porcelain`; acceptance: the merged-green pin is recorded before PRIV-A3.

### Phase 8 Gate

> All checks below must pass before starting PRIV-A3 in Phase 9.

- [ ] [AI] Verify PUB-A3 is merged/green and its bounded-loop source pin is recorded; acceptance:
      PRIV-A3 is the only permitted next PR.

> **Pause Safety**: PUB-A3 is merged and reversible. Safe to stop. To resume: recheck its pin and
> cycle audit.

## Phase 9: Deliver PRIV-A3 — Bounded-Loop Discharge

- [ ] [AI] In the private worktree run `git switch -C optimize-pr-process-private-loop origin/main`,
      fetch the merged PUB-A3 pin, scan only the scope/loop class, and invoke the Canonical
      rule-boundary run for PRIV-A3; acceptance: classifier/readiness differences are semantic and
      evidence-backed; classifier evidence has one concrete human-readable definition across the
      listed `done-definition`, `hardened-merge-preconditions`, and
      `repo-governance/development/workflow/pr-merge-protocol/` consumers; and any portable source
      defect uses the bounded upstream correction path.
- [ ] [AI] **PRIV-A3 size/cohesion**: run the worktree-aware size commands; acceptance: the unit is
      one private bounded-loop discharge.
- [ ] [AI] **PRIV-A3 local gates**: run every command under `Local Quality Gates Before Any Push`;
      acceptance: all exit 0 in private.
- [ ] [AI] **PRIV-A3 Step 9**: complete canonical Step 9; acceptance: the A3 obligation references
      its final pin and classifier-evidence definition.
- [ ] [AI] **PRIV-A3 review/fix**: run bounded review and same-thread replies; acceptance: every
      finding is terminal.
- [ ] [AI] **PRIV-A3 current-head CI**: run `rtk proxy gh pr checks <PR> --repo
wahidyankf/ose-private`; acceptance: required checks are green on the reviewed head.
- [ ] [AI] **PRIV-A3 merge**: merge only the reviewed head; acceptance: the PR records its merge SHA.
- [ ] [AI] **PRIV-A3 evidence/resync**: fetch/read private `origin/main` and run
      `git status --porcelain`; acceptance: both repositories are clean and ready for Wave B.

### Phase 9 Gate

> All checks below must pass before starting PUB-B in Phase 10.

- [ ] [AI] Open all six merged A-wave PRs as a human reader; acceptance: each body, review,
      line thread, disposition, check, and merge note forms one reconcilable record without a
      private agent log.
- [ ] [AI] Sample at least one `fix` and one evidence-backed `reject` thread from PUB-A2; acceptance:
      a bootcamp-trained engineer with practical coding experience can reproduce or inspect the
      evidence, connect it to the observable result, and understand the bounded disposition without
      assumed university/CS coursework or a general-theory lecture.
- [ ] [AI] Run the public contradiction inventory again; acceptance: no active seven/unbounded
      cycle rule or primary hidden-schema mandate remains in PUB-A-owned surfaces.
- [ ] [AI] Confirm both `origin/main` branches contain the three paired A-wave boundaries and both
      worktrees are clean before PUB-B edits.
- [ ] [AI] Verify each PUB-A PR body records dependency, feature-flag strategy, stable-main proof,
      rollback, and its diagram/omission decision; acceptance: all three intermediate merged states
      are coherent and each repository still has exactly one plan worktree.
- [ ] [AI] Verify each PUB-A Step 9 summary records normalization, placement, enforcement
      disposition, tidy/verification result, and source pin, and each matching private PR records
      its discharge or bounded correction history; acceptance: no A-wave obligation remains open.

> **Pause Safety**: all three public/private A-wave pairs are merged, green, auditable, and clean.
> Safe to stop. To resume: fetch both origins and verify the six recorded pins before Wave B.

## Phase 10: Deliver PUB-B — Planning Contracts

- [ ] [AI] Run `git switch -C optimize-pr-process-public-planning origin/main`, then invoke the
      Canonical rule-boundary run for PUB-B over public plan maker/checker/fixer/execution-checker
      sources and the named planning workflow shards; acceptance: stage ownership matches the
      lifecycle table, checker precedes fixer, validation does not require future artifacts,
      mandatory PR modes override direct-push examples, a formal checker uses complete independently
      scoped lenses over a fixed plan surface before class-complete evidence-backed fixing, no
      branch-side correction ledger becomes its own repeated review target, multi-repo archival
      occurs in a final plan-folder-owning public closure PR after sibling evidence is complete, and
      cleanup follows merge with safety checks. New convergence registries or validators remain
      prohibited without the mechanism-necessity proof.
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] Reconcile the one-public-control-plan deviation in public multi-repo planning docs only
      as an explicit case record, not a blanket replacement of the one-plan-per-repo default;
      acceptance: the current rule remains readable and this plan's choice cannot be silently
      generalized.
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] **PUB-B propagation-contract edit**: update the PUB-B-owned
      `repo-rules-propagation.md` entry and listed scope, related-workflow, Step 9, index, and success
      criteria shards; acceptance: source pins, discharge, one-open-wave, pre/post-open correction,
      replacement, and oscillation behavior are canonical rather than plan-only.
- [ ] [AI] **PUB-B size/cohesion**: run the worktree-aware size commands; acceptance: the unit stays
      within 400/20 or declares the exact rule/binding atomicity exception and reading order.
- [ ] [AI] **PUB-B local gates**: run `npm run generate:bindings` and every command under `Local
Quality Gates Before Any Push`; acceptance: all exit 0, mirrors reflect `.claude/`, and no
      generated file contains a hand-only difference.
- [ ] [AI] Complete canonical Step 9 for PUB-B using commit subject
      `docs(plans): make the PR lifecycle coherent`; acceptance: it targets public `main`, contains
      no PUB-C workflow edit, records raw plus review-relevant counts and a concise manifest summary,
      and records `sibling-obligation: ose-private`.
- [ ] [AI] **PUB-B review/fix**: run bounded review and same-thread replies; acceptance: the PR
      terminates at or before cycle 5 with every finding terminal and no cap-based waiver.
- [ ] [AI] **PUB-B current-head CI**: run `rtk proxy gh pr checks <PR> --repo
wahidyankf/ose-public`; acceptance: required checks are green on the reviewed head.
- [ ] [AI] **PUB-B merge**: merge only the reviewed head; acceptance: the PR records its merge SHA.
- [ ] [AI] **PUB-B evidence/resync**: fetch/read public `origin/main` and run
      `git status --porcelain`; acceptance: the merged-green source pin is recorded before PRIV-B.

### Phase 10 Gate

> All checks below must pass before starting PRIV-B in Phase 11.

- [ ] [AI] Verify PUB-B is merged/green and pinned with no conditional CI edit; acceptance: PRIV-B
      is the only permitted next PR.

> **Pause Safety**: PUB-B is merged and reversible. Safe to stop. To resume: recheck its source pin
> and planning-class checks.

## Phase 11: Deliver PRIV-B — Planning Discharge

- [ ] [AI] In the private worktree run `git switch -C optimize-pr-process-private-planning
origin/main`, fetch the merged PUB-B pin, scan only the planning/archival class, and invoke the
      Canonical rule-boundary run for PRIV-B; acceptance: private stage/sharding differences are
      recorded as deliberate deviations, two-repository plan-folder archival semantics are explicit,
      and portable source defects use the bounded upstream path.
- [ ] [AI] **PRIV-B propagation-contract edit**: adapt the listed private
      `repo-rules-propagation*` surfaces and archival-nuance reference; acceptance: semantics match
      the pinned PUB-B source with repo-specific deviations explicit.
- [ ] [AI] **PRIV-B size/cohesion**: run the worktree-aware size commands; acceptance: the unit is
      one planning/propagation discharge.
- [ ] [AI] **PRIV-B local gates**: run `npm run generate:bindings` and every command under `Local
Quality Gates Before Any Push`; acceptance: all exit 0 in private.
- [ ] [AI] **PRIV-B Step 9**: complete canonical Step 9; acceptance: the obligation ledger
      discharges PUB-B against the final merged pin.
- [ ] [AI] **PRIV-B review/fix**: run bounded review and same-thread replies; acceptance: every
      finding is terminal.
- [ ] [AI] **PRIV-B current-head CI**: run `rtk proxy gh pr checks <PR> --repo
wahidyankf/ose-private`; acceptance: required checks are green on the reviewed head.
- [ ] [AI] **PRIV-B merge**: merge only the reviewed head; acceptance: the PR records its merge SHA.
- [ ] [AI] **PRIV-B evidence/resync**: fetch/read private `origin/main` and run
      `git status --porcelain`; acceptance: the worktree is clean and no stacked successor exists.

### Phase 11 Gate

> All checks below must pass before starting conditional PUB-C in Phase 12.

- [ ] [AI] Run `npm run validate:sync` and the planning-class contradiction inventory on both
      merged `origin/main` branches; acceptance: sync is clean and agent/planning contracts state
      one semantically aligned lifecycle or a deliberate repo-specific deviation.
- [ ] [AI] Compare public normative prose with binding templates manually; acceptance: cycle counts,
      disposition vocabulary, footer, audit source, scope rule, and stage ownership agree.
- [ ] [AI] Confirm both worktrees are clean and based on the newest merged Wave-B boundaries;
      acceptance: `git status --porcelain` is empty in both and both merge diffs were read.
- [ ] [AI] Verify PUB-B retained existing in-progress plan contracts while activating the revised
      lifecycle only for newly established work; acceptance: ordered activation and rollback are
      visible in the PR, and the public repo still has one plan worktree.
- [ ] [AI] Verify PUB-B's Step 9 summary records its enforcement disposition and original
      `ose-private` sibling obligation, and PRIV-B records its final discharge/correction chain;
      acceptance: no manual-copy shortcut or open Wave-B obligation remains.

> **Pause Safety**: Wave B is merged and green in both repositories, its obligation is discharged,
> and both worktrees are clean. Safe to stop before the conditional C assessment.

## Phase 12: Assess and Conditionally Deliver PUB-C — Existing CI Machinery

- [ ] [AI] **Branch sync**: run `git status --porcelain`, `git fetch origin`, and `git switch -C
optimize-pr-process-public-ci origin/main`; acceptance: the reused public worktree is clean
      and PUB-C is unstacked from current public `main`.
- [ ] [AI] **Hypothesis 1 necessity decision — fail-open aggregate** `[Repo-grounded]`: inspect
      `.github/workflows/pr-quality-gate.yml`, `apps/rhino-cli/src/commands/gate/validate.rs`,
      `apps/rhino-cli/tests/gate_specs.rs`, and recent Actions results; acceptance: approve a
      surgical repair only if a failed, cancelled, or unsafe skipped dependency can still yield a
      successful `quality-gate`, otherwise record `N/A — disproved` with linked evidence. Escalate
      to `[AI+HUMAN]` only if the evidence reaches an authority boundary or unresolved judgment the
      agent cannot safely decide.

- [ ] [AI] **Hypothesis 1 RED**: if approved, add the smallest failing scenario to
      `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-validation.feature` and binding in
      `apps/rhino-cli/tests/gate_specs.rs`, then run `npx nx run rhino-cli:test:quick`; acceptance:
      the new aggregate-result test fails for the reproduced reason before workflow/validator edits.

  **Gherkin (binds) →**

  ```gherkin
  Scenario: Aggregate gate rejects an unsafe dependency result
    Given a required quality-gate dependency has an unsafe terminal result
    When the aggregate quality-gate job evaluates its dependencies
    Then the reviewed head is not reported as merge-ready
  ```

- [ ] [AI] **Hypothesis 1 GREEN**: if RED exists, edit only
      `.github/workflows/pr-quality-gate.yml` and the necessary existing validator path
      `apps/rhino-cli/src/commands/gate/validate.rs`; acceptance: `npx nx run
rhino-cli:test:quick` passes and the unsafe result cannot report success.
- [ ] [AI] **Hypothesis 1 REFACTOR**: simplify only the approved aggregate-result repair and rerun
      `npx nx run rhino-cli:test:quick`; acceptance: tests remain green and no new validator,
      framework, service, parser, or bot exists. If disproved, record N/A evidence for RED/GREEN/
      REFACTOR instead of editing code.
- [ ] [AI] **Hypothesis 2 necessity decision — self-mutating formatter** `[Repo-grounded]`: inspect the `format` job in
      `.github/workflows/pr-quality-gate.yml` and a current PR run; acceptance: approve only if the
      gate can commit or push to the reviewed branch, otherwise record `N/A — disproved`. Escalate
      only for an actual authority-dependent or unresolved safety decision.

- [ ] [AI] **Hypothesis 2 RED**: if approved, add a focused workflow-contract scenario to
      `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-validation.feature` and binding in
      `apps/rhino-cli/tests/gate_specs.rs`, then run `npx nx run rhino-cli:test:quick`; acceptance:
      the test fails because the workflow retains write/commit/push behavior.

  **Gherkin (binds) →**

  ```gherkin
  Scenario: Pull request validation does not mutate the reviewed head
    Given a pull request contains formatting drift
    When the PR quality-gate workflow validates the head
    Then the workflow reports the drift without committing or pushing a replacement head
  ```

- [ ] [AI] **Hypothesis 2 GREEN**: if RED exists, edit `.github/workflows/pr-quality-gate.yml` and
      only the existing validator path needed to enforce read-only validation; acceptance: `npx nx
run rhino-cli:test:quick` passes and the workflow cannot move the reviewed head.
- [ ] [AI] **Hypothesis 2 REFACTOR**: remove only duplication exposed by the read-only repair and
      rerun `npx nx run rhino-cli:test:quick`; acceptance: tests remain green and no replacement
      formatting bot or framework exists. If disproved, record N/A evidence for all three stages.
- [ ] [AI] **Hypothesis 3 necessity decision — duplicated work** `[Repo-grounded]`: compare jobs and registry dispatch in
      `.github/workflows/pr-quality-gate.yml`, `repo-config.yml`, and
      `apps/rhino-cli/src/commands/gate/run.rs`; acceptance: approve only an observed duplicate of
      the same expensive gate without a correctness rationale, otherwise record `N/A — disproved`.
      Escalate only for an actual authority-dependent or unresolved safety decision.

- [ ] [AI] **Hypothesis 3 RED**: if approved, add the smallest failing scenario to
      `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature` and binding in
      `apps/rhino-cli/tests/gate_specs.rs`, then run `npx nx run rhino-cli:test:quick`; acceptance:
      the test exposes the exact duplicate dispatch before implementation changes.

  **Gherkin (binds) →**

  ```gherkin
  Scenario: A registered CI gate runs once per quality-gate execution
    Given one required validation is registered for the CI surface
    When the pull request quality gate schedules its work
    Then that validation is not executed twice without a named correctness reason
  ```

- [ ] [AI] **Hypothesis 3 GREEN**: if RED exists, edit only the proven duplicate edge in
      `.github/workflows/pr-quality-gate.yml`, `repo-config.yml`, or
      `apps/rhino-cli/src/commands/gate/run.rs`; acceptance: the focused test passes and required
      coverage still runs once.
- [ ] [AI] **Hypothesis 3 REFACTOR**: simplify only the approved duplicate-work boundary and rerun
      `npx nx run rhino-cli:test:quick`; acceptance: tests remain green and no new orchestration
      subsystem exists. If disproved, record N/A evidence for all three stages.
- [ ] [AI] If no defect clears the necessity gate, add no workflow/test file and post one comment
      on the merged PUB-B PR containing all three N/A dispositions, PUB-B merge SHA, reviewed head,
      required-check URLs/states, public `origin/main` pin, and the exact `Generated by AI` footer;
      acceptance: `git diff --name-only` contains no PUB-C implementation path and the non-circular
      public no-change source is auditable before closure without relying on the later closure PR.
- [ ] [AI] **Size**: if PUB-C has an approved diff, measure review-relevant lines/files against
      public `origin/main` with the pre-commit worktree-aware and committed-head commands in
      `Repeatable same-worktree transition`; acceptance: staged, unstaged, and untracked work is
      included and the repair remains one cohesive existing-machinery concern.
- [ ] [AI] **Local gates**: run `npx nx run rhino-cli:test:quick`, affected gates, and `git diff
--check`; acceptance: all exit 0 and every approved RED/GREEN/REFACTOR record is current.
- [ ] [AI] **PR body/ledger**: draft `local-tmp/pr-bodies/PUB-C.md`; acceptance: it includes each
      hypothesis disposition, reproduction/TDD evidence, cost/benefit, integration safety,
      rollback, current-head checks, and `sibling-obligation: ose-private`.
- [ ] [AI] **Commit**: stage explicit approved paths and run `git commit -m "fix(ci): make the
existing PR gate fail safely"`; acceptance: no unapproved/N/A path is staged.
- [ ] [AI] **Push/open**: push/open at most one PUB-C PR; acceptance: no PR opens when all three
      hypotheses are N/A, and a public no-change pin is recorded instead.
- [ ] [AI] **Review/fix/CI**: complete the native cycle and current-head checks; acceptance: every
      finding is terminal and required checks are green.
- [ ] [AI] **Merge**: merge PUB-C only if it exists and remains approved; acceptance: the final
      public repair/no-change pin is recorded.
- [ ] [AI] **Evidence/resync**: fetch public `origin/main`, read the complete landed diff when one
      exists, and verify the same worktree is clean; acceptance: private may consume only this pin.

### Phase 12 Gate

> All checks below must pass before starting private C assessment in Phase 13.

- [ ] [AI] Verify all three hypotheses have independent approval/N/A evidence and any PUB-C PR is
      merged/green, pinned, and limited to approved existing machinery; acceptance: PRIV-C alone may
      consume the final public repair or no-change pin.

> **Pause Safety**: PUB-C is merged or explicitly N/A and public `main` is green. Safe to stop. To
> resume: verify the exact public pin before private reproduction.

## Phase 13: Assess and Conditionally Deliver PRIV-C — Existing CI Machinery

- [ ] [AI] From the private worktree, consume only the merged-green PUB-C pin or explicit public
      no-change pin, then reproduce/disprove each CI hypothesis independently on private current
      `origin/main`; acceptance: a public reproduction never substitutes for private evidence and
      every discovery receives the anti-chain-reaction classification before editing.
- [ ] [AI] **Private hypothesis 1 necessity decision — fail-open aggregate** `[Repo-grounded]`:
      inspect private `.github/workflows/pr-quality-gate.yml`,
      `apps/rhino-cli/src/commands/gate/validate.rs`, `apps/rhino-cli/tests/gate_specs.rs`, and
      recent private Actions results; acceptance: independently approve one surgical repair or
      record `N/A — disproved` with private evidence, escalating only for an actual
      authority-dependent or unresolved safety decision.
- [ ] [AI] **Private hypothesis 1 RED**: if approved, add the smallest failing private test on its
      exact `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-validation.feature` scenario and
      `apps/rhino-cli/tests/gate_specs.rs` binding, then run `npx nx run rhino-cli:test:quick`;
      acceptance: it fails for the private reproduction before implementation edits.

  **Gherkin (binds) →**

  ```gherkin
  Scenario: Private aggregate gate rejects an unsafe dependency result
    Given a required private quality-gate dependency has an unsafe terminal result
    When the private aggregate quality-gate job evaluates its dependencies
    Then the reviewed private head is not reported as merge-ready
  ```

- [ ] [AI] **Private hypothesis 1 GREEN**: edit only private
      `.github/workflows/pr-quality-gate.yml` and
      `apps/rhino-cli/src/commands/gate/validate.rs`; acceptance: the focused test passes and unsafe
      dependency state cannot report success.
- [ ] [AI] **Private hypothesis 1 REFACTOR**: simplify only the repair and rerun the focused test;
      acceptance: green with no new mechanism, or all three steps carry linked N/A evidence.
- [ ] [AI] **Private hypothesis 2 necessity decision — self-mutating formatter**
      `[Repo-grounded]`: inspect private `.github/workflows/pr-quality-gate.yml` and a current run;
      acceptance: independently approve one surgical repair or record `N/A — disproved`, escalating
      only for an actual authority-dependent or unresolved safety decision.
- [ ] [AI] **Private hypothesis 2 RED**: if approved, add the smallest failing test to the existing
      private `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-validation.feature` and binding
      in `apps/rhino-cli/tests/gate_specs.rs`, then run `npx nx run rhino-cli:test:quick`;
      acceptance: it fails because the workflow can move the head.

  **Gherkin (binds) →**

  ```gherkin
  Scenario: Private pull request validation does not mutate the reviewed head
    Given a private pull request contains formatting drift
    When the private PR quality-gate workflow validates the head
    Then the workflow reports the drift without committing or pushing a replacement head
  ```

- [ ] [AI] **Private hypothesis 2 GREEN**: remove only the proven mutation behavior from the
      existing private workflow; acceptance: the focused test passes and validation is read-only.
- [ ] [AI] **Private hypothesis 2 REFACTOR**: simplify only the repair and rerun the focused test;
      acceptance: green with no replacement bot/framework, or all stages carry N/A evidence.
- [ ] [AI] **Private hypothesis 3 necessity decision — duplicated work** `[Repo-grounded]`: inspect
      private `.github/workflows/pr-quality-gate.yml`, `repo-config.yml`, and
      `apps/rhino-cli/src/commands/gate/run.rs`; acceptance: independently approve one surgical
      repair or record `N/A — disproved`, escalating only for an actual authority-dependent or
      unresolved safety decision.
- [ ] [AI] **Private hypothesis 3 RED**: if approved, add the smallest failing test to the existing
      private `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature` and binding
      in `apps/rhino-cli/tests/gate_specs.rs`, then run `npx nx run rhino-cli:test:quick`;
      acceptance: it exposes the exact duplicate dispatch.

  **Gherkin (binds) →**

  ```gherkin
  Scenario: A private registered CI gate runs once per quality-gate execution
    Given one required validation is registered for the private CI surface
    When the private pull request quality gate schedules its work
    Then that validation is not executed twice without a named correctness reason
  ```

- [ ] [AI] **Private hypothesis 3 GREEN**: remove only the proven duplicate edge from private
      `.github/workflows/pr-quality-gate.yml`, `repo-config.yml`, or
      `apps/rhino-cli/src/commands/gate/run.rs`; acceptance: the focused test passes and required
      validation still runs once.
- [ ] [AI] **Private hypothesis 3 REFACTOR**: simplify only that boundary and rerun the focused
      test; acceptance: green with no new subsystem, or all stages carry N/A evidence.
- [ ] [AI] **Size**: measure the conditional private diff with the pre-commit worktree-aware and
      committed-head commands in `Repeatable same-worktree transition`; acceptance: staged,
      unstaged, and untracked work is included and any repair remains cohesive inside approved paths.
- [ ] [AI] **Local gates**: run private affected gates and `git diff --check`; acceptance: all exit
      0 and no new PR-process tooling exists.
- [ ] [AI] **PR body/ledger**: draft `local-tmp/pr-bodies/PRIV-C.md` only for an approved diff;
      acceptance: it links the public pin, independent evidence, TDD results, integration safety,
      rollback, and exact paths; otherwise post one comment on the merged PRIV-B PR with all three
      private N/A dispositions, PRIV-B merge SHA, reviewed head, required-check URLs/states, final
      public no-change pin, private `origin/main` pin, and the exact `Generated by AI` footer, then
      open no PR. The comment exists before Phase 14 reconciliation.
- [ ] [AI] **Commit**: stage explicit approved paths and commit the conditional repair; acceptance:
      no unapproved or N/A hypothesis path is staged.
- [ ] [AI] **Push/open**: push/open at most one PRIV-C PR; acceptance: no empty PR exists.
- [ ] [AI] **Review/fix/CI**: complete native review/replies and current-head CI; acceptance: every
      finding is terminal and required checks are green.
- [ ] [AI] **Merge**: merge only the reviewed private head; acceptance: private `main` contains the
      approved repair or remains unchanged.
- [ ] [AI] **Evidence/resync**: fetch/read the private merge diff and synchronize the same worktree;
      acceptance: the C obligation is discharged against the final public pin.

### Phase 13 Gate

> All checks below must pass before starting reconciliation in Phase 14.

- [ ] [AI] Verify public `origin/main` has either a tested surgical repair or an explicit no-change
      necessity record; acceptance: no new PR-process enforcement mechanism exists.
- [ ] [AI] Run `npm run validate:sync`,
      `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`, and
      `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` in both worktrees, then
      reconcile each merged unit's boundary record against the scoped-gate evidence required by
      `Local Quality Gates Before Any Push`; acceptance: all current-head commands exit 0,
      `markdownlint` and `md-mermaid` passed through pre-commit while that unit's explicit Markdown
      ledger paths were staged, and `md-links` plus every selected registry-owned pre-push gate
      passed before its push.
- [ ] [AI] Reconcile the merged public pins for PUB-A1/A2/A3, PUB-B, and optional PUB-C against the
      private PRs that consumed them; acceptance: every pin is an exact merged PR/SHA/check tuple,
      and an edited GitHub description cannot silently change the recorded source commit.
- [ ] [AI] Verify PUB-C used an atomic tested-and-revertible change or produced no PR; acceptance:
      public `main` stayed green between units and the public repo still has one plan worktree.
- [ ] [AI] Reconcile the C-wave obligation ledger; acceptance: the public pin is merged-green or an
      explicit no-change record, private independent evidence is terminal, any correction stays
      within the one-correction budget, and both repo worktrees are clean.

> **Pause Safety**: all paired A/B waves and the conditional C wave are terminal in both
> repositories. Safe to stop. To resume: fetch both origins and reconcile the PR-native obligation
> pins before cross-repository verification.

## Phase 14: Reconcile the Interleaved Propagation Waves

- [ ] [AI] Build the PR-native wave table for A1, A2, A3, B, and conditional C with public source
      PR/SHA/check pin, private base and merge SHA, obligation status, discovery classifications,
      correction count, superseded pins, and final evidence links; acceptance: every cell comes from
      a native PR artifact and no private unit consumed a draft.
- [ ] [AI] Compare each final public/private semantic class using the deviation matrix; acceptance:
      every difference is either private-only, a repo-specific deviation, a resolved portable source
      defect, or an explicitly governed byte-identity result.
- [ ] [AI] Verify correction budgets; acceptance: each wave used at most one upstream public
      correction total across all classes, multiple non-cohesive classes stopped for plan
      amendment/human replan, any second reversal stopped as oscillation, and unrelated terminal
      units were not reopened.
- [ ] [AI] Run `npm run validate:sync` and the relevant contradiction inventory in both worktrees;
      acceptance: generated mirrors are clean, all affected-class findings are terminal, and no new
      bot/tooling surface exists.

### Phase 14 Gate

> All checks below must pass before starting Phase 15.

- [ ] [AI] Confirm every public obligation has one linked private terminal disposition and every
      correction has one superseded and one final pin; acceptance: no open or contradictory ledger
      entry remains.
- [ ] [AI] Confirm both worktrees are clean on their current `origin/main` and exactly one plan
      worktree exists per repository.
- [ ] [AI] Confirm every wave records dependency, integration safety, rollback, size/cohesion,
      validation, and diagram/omission evidence; acceptance: each merged intermediate state remains
      coherent, green, reversible, and recoverable.

> **Pause Safety**: all paired waves are reconciled, obligation-complete, and clean. Safe to stop.
> To resume: fetch both origins and compare the final pins with the PR-native wave table.

## Phase 15: Close the Private Track

- [ ] [AI] Post a private closure note in the final private PR or linked issue comment listing
      PRIV-A1, PRIV-A2, PRIV-A3, PRIV-B, conditional PRIV-C/no-change, final public pins,
      superseded pins, discovery
      classifications, deviations, correction counts, audit consistency, current checks, and the
      exact AI footer; acceptance: the private track is auditable without local agent logs.
- [ ] [AI] Run private `npm run validate:sync`,
      `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`, and
      `npx nx affected -t typecheck lint test:quick specs:behavior:coverage`, then reconcile every
      merged private unit's boundary record against the scoped-gate evidence required by `Local
Quality Gates Before Any Push`; acceptance: all current-head commands exit 0,
      `markdownlint` and `md-mermaid` passed through pre-commit while that unit's explicit Markdown
      ledger paths were staged, and `md-links` plus every selected registry-owned pre-push gate
      passed before its push.

### Phase 15 Gate

> All checks below must pass before starting Phase 16.

- [ ] [AI] Verify all private delivery PRs are merged or the track is explicitly blocked; acceptance:
      no final public archival begins while private status is ambiguous.
- [ ] [AI] Verify private closure lists every review cycle and thread disposition consistently;
      acceptance: no analogue of the `ose-private#62` 11-versus-14 audit mismatch remains.
- [ ] [AI] Run `git status --porcelain` in the private worktree; acceptance: empty, with all commits
      ancestors of private `origin/main`.
- [ ] [AI] Verify PRIV-C used an atomic tested-and-revertible change or produced no PR; acceptance:
      private `main` stayed green and the private track used one repo-scoped worktree throughout.
- [ ] [AI] Verify no source-defect chain remains active; acceptance: every affected class has one
      final merged-green pin, no second reversal escaped the oscillation stop, and unrelated units
      remain closed.

> **Pause Safety**: the private track has a complete, independently auditable terminal state. Safe
> to stop. To resume: re-open the private closure note and confirm all linked heads/checks still
> match the recorded merge SHAs.

## Phase 16: Cross-Repository Verification and Process Dogfood

- [ ] [AI] Select the first two qualifying post-rollout delivery PRs in each repository, or all
      rollout PRs when fewer exist, and apply the BRD success-measure checklist; acceptance: results
      are posted as human-readable comments linked from the final public PR.
- [ ] [AI] Verify each sampled PR body has all required sections, current-head evidence,
      review-relevant counts, dependency/integration-safety/rollback fields, and a justified size
      exception when applicable; acceptance: every omission is fixed before final archival or
      recorded as a blocking finding.
- [ ] [AI] For each sampled PR, verify a Mermaid diagram is present only when materially useful and,
      when present, its boundary record shows the staged Markdown path passed the registry-owned
      `md-mermaid` pre-commit gate, uses non-color cues, and has adjacent equivalent prose;
      acceptance: decorative diagrams are absent and omitted diagrams need no replacement.
- [ ] [AI] Verify every sampled blocking thread meets the bootcamp-trained practical-reader
      contract and contains one same-thread disposition; acceptance: observation, observable
      consequence, reproduction/inspection path, relevant concept, evidence, and bounded remedy
      stay concise, and no bare `yes`, `done`, or `disagree` reply remains.
- [ ] [AI] Verify scope growth with `git diff --stat` at each reviewed cycle head; acceptance: every
      material growth maps to an in-scope finding/same-class repair or a linked follow-up, with no
      unexplained adjacent change.
- [ ] [AI] Verify cycle headers, recovery-note claims, thread counts, and merge note against GraphQL
      review artifacts; acceptance: every sampled PR is internally reconcilable and none has a sixth
      AI cycle.
- [ ] [AI] For every sampled cycle after cycle 1, verify the prior finding dispositions and head
      delta; acceptance: no settled point is reopened without new evidence, no known discipline was
      withheld from cycle 1, and every cycle-4/5 note names both the non-convergence cause and a
      changed strategy.
- [ ] [AI] Verify no new bot, parser, dashboard, database, hosted service, PR-size gate, or
      PR-process validator was added in either repo using `git diff --name-only <PHASE0_SHA>..HEAD`
      and the file ledgers; acceptance: only listed governance/binding/template/conditional-existing-
      CI/plan paths appear.
- [ ] [AI] Record manual behavioral assertions as N/A for UI and API because the plan changes no
      runtime screen or endpoint; acceptance: the final public PR explicitly states this rationale
      rather than fabricating browser/curl evidence.

### Phase 16 Gate

> All checks below must pass before starting Phase 17.

- [ ] [AI] Produce a cross-repo closure table with PR URL, merge SHA, reviewed head, cycle count,
      thread count, recovery-note count, current checks, and audit-consistency result; acceptance: no
      cell is unknown or contradictory.
- [ ] [AI] Add dependency, feature-flag strategy, stable-main proof, rollback result, and worktree
      identity to the closure table; acceptance: every delivery unit is traceable and
      `git worktree list` confirms one plan worktree per repo before final cleanup.
- [ ] [AI] Add every public source pin, private obligation disposition, discovery classification,
      correction/supersession link, and correction count to the closure table; acceptance: a reader
      can reconstruct the anti-chain-reaction decisions without local logs or hidden metadata.
- [ ] [AI] Re-run public and private Markdown/link/sync/affected gates; acceptance: every command
      exits 0 on each repo's current merged state.
- [ ] [AI+HUMAN] If a rollout PR remains unsafe after cycle 5, or earlier progress needs product,
      architecture, or merge authority, present the PR-native evidence for human
      split/rework/close/manual-review choice; acceptance: routine cycles 4–5 need no human gate, and
      no automated archival or merge proceeds by treating the cap as success.
- [ ] [AI] Read every merged rollout PR from top to bottom as a retrospective human consumer;
      acceptance: body, reading guide, reviews, line threads, replies, recovery notes, checks, and
      merge note form one concise record without private logs, including PRs merged by an agent.

> **Pause Safety**: both repositories are verified and the final decision is explicit; only
> knowledge capture and public plan archival remain. Safe to stop. To resume: re-run the closure
> table measurement recipes against the recorded PR URLs.

## Phase 17: Knowledge Capture

- [ ] [AI] In the clean public worktree run `git fetch origin` and `git switch -C
optimize-pr-process-public-closure origin/main`; acceptance: every Knowledge Capture edit
      accumulates on the declared Phase 18 closure branch and therefore has a PR route rather than
      being replaced by a later branch reset.
- [ ] [AI] Apply the litmus test to every `learnings.md` entry; acceptance: retain only an entry for
      which a durable surface would prevent or catch the issue next time, and record a one-line
      discard reason for the rest.
- [ ] [AI] Apply the secret/sensitivity gate to every surviving entry; acceptance: sanitize with
      placeholders or discard any entry that cannot be made public safely.
- [ ] [AI] Apply the repo-relevance gate; acceptance: private infrastructure knowledge remains in
      `ose-private`, while general PR/planning governance may route to public durable surfaces.
- [ ] [AI] Route each surviving entry to exactly one durable home, using a small in-scope non-code
      edit or a separate `plans/backlog/<slug>/` follow-up for larger work; acceptance: every entry
      records its terminal route.
- [ ] [AI] Before creating any idea/backlog item, search existing indexes and briefs with
      `rg -n "<key terms>" plans/ideas plans/backlog`; acceptance: no duplicate idea or plan is
      created.
- [ ] [AI] Route any code-homed learning to a separate backlog plan unless it is a defect blocking
      this plan's own completion; acceptance: no unrelated application/library/test code lands in
      the final public PR.
- [ ] [AI] If execution surfaces no generalizable learning, add
      `No generalizable learnings — <reason>` to `learnings.md`; acceptance: the running log has an
      explicit terminal state.

### Phase 17 Gate

> All checks below must pass before starting Phase 18.

- [ ] [AI] Review every `learnings.md` entry; acceptance: all are routed, filed, or discarded, or the
      explicit none escape is present.
- [ ] [AI] Verify no secret/private-only material appears in this public plan with an appropriate
      repository secret scan and manual read; acceptance: no sensitive value or private
      infrastructure detail is present.
- [ ] [AI] Run `git diff --check -- plans/in-progress/optimize-pr-process`; acceptance: exit 0.

> **Pause Safety**: all learning is terminally routed and no execution insight is stranded. Safe to
> stop. To resume: scan `learnings.md` for any heading without a terminal routing statement.

## Local Quality Gates Before Any Push

Apply this checklist inside the active repo worktree for every delivery boundary. Run the
pre-commit portion after edits are complete and immediately before the boundary commit; run the
pre-push portion after that commit and before every push:

### Before commit — staged paths

- [ ] [AI] Run
      `git add -- <each-explicit-active-ledger-path>` and `git diff --cached --name-only`; acceptance:
      every changed path owned by the active boundary is staged, no unowned path is cached, and the
      list is saved in the boundary record before any staged-path gate runs.
- [ ] [AI] Run
      `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-commit` `[Repo-grounded]`;
      acceptance: for every staged affected Markdown path, the existing registry runs
      `markdownlint` and `md-mermaid` and exits 0; no raw whole-repository Markdown or Mermaid check
      is substituted for this staged-path evidence.
- [ ] [AI] Re-run `git diff --cached --name-only`, inspect `git diff --cached`, run
      `git diff --cached --check`, and reconcile `git status --short` against the active ledger;
      acceptance: formatter/restaging mutations touched only owned paths, the cache remains the
      exact intended commit, and it stays staged for the later `Commit` step. If any owned file is
      edited after this point, repeat staging, pre-commit, and cache reconciliation before commit.
- [ ] [AI] Run `npm run validate:sync`; acceptance: source and generated harness bindings match.
- [ ] [AI] Run `npx nx affected -t typecheck lint test:quick specs:behavior:coverage`; acceptance:
      all affected targets exit 0.
- [ ] [AI] Run `git diff --check` and reconcile `git status --short` against the file-touch ledger;
      acceptance: no whitespace defect or unowned path remains.

### After commit — before push

- [ ] [AI] Run
      `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push` `[Repo-grounded]` and inspect
      its result; acceptance: registry-owned `md-links` and every other selected pre-push gate cover
      the committed boundary's declared blast radius and exit 0 without a duplicate raw
      whole-repository Markdown, Mermaid, or link invocation.
- [ ] [AI] Fix all failures at root cause, subject to this plan's scope/authority rules; acceptance:
      no failing check is bypassed, suppressed, or mislabeled as unrelated without an explicit stop.

## Post-Push Verification

- [ ] [AI] After every PR-branch push, run `rtk proxy gh pr checks <PR> --repo
wahidyankf/<REPO>` every two minutes until terminal; acceptance: every required check is green
      on the exact reviewed head and no `gh run watch` is used.
- [ ] [AI] If CI fails, inspect the failing job and fix the root cause on the same boundary branch;
      acceptance: follow-up push is reviewed and the PR audit records the new head.
- [ ] [AI] Before merge, query unresolved threads through GraphQL and compare the cycle/recovery-note
      record; acceptance: no blocking unresolved thread, audit contradiction, or stale-head green
      check remains.

## Commit Guidelines

- [ ] [AI] Commit thematically using Conventional Commits; acceptance: one concern per commit and
      imperative subject with no period.
- [ ] [AI] Stage explicit ledger paths only; acceptance: `git diff --cached --name-only` contains no
      path outside the active boundary.
- [ ] [AI] Keep generated mirrors in the same commit as their `.claude/` source; acceptance:
      `npm run validate:sync` passes at each commit boundary.
- [ ] [AI] Never bundle unrelated quality-gate repairs into a governance commit; acceptance: optional
      PUB-C/PRIV-C remains a separate delivery unit.

## Phase 18: Final Public Closure and Plan Archival

- [ ] [AI] Verify the existing public branch is `optimize-pr-process-public-closure`, its base is the
      Phase 17 recorded public `origin/main`, and `git status --short` contains only Phase 17
      knowledge/closure-ledger paths; acceptance: Phase 18 continues the same branch without
      discarding or orphaning Knowledge Capture edits.
- [ ] [AI] Verify every delivery checkbox is complete or carries an explicit N/A with evidence;
      acceptance: no unchecked substantive step is silently skipped.
- [ ] [AI] Draft the final public PR body with dependency, feature-flag/integration-safety strategy,
      stable-main proof, rollback, and `diagram: required|omitted — <reason>`; acceptance: closure
      is understandable without reconstructing hidden state, and any included Mermaid is accessible
      and followed by equivalent prose.
- [ ] [AI] Verify all public/private delivery PRs, SHAs, checks, thread states, cycle counts,
      recovery notes, and deviations are present in the cross-repo closure table; acceptance: the final
      public PR links a complete audit record.
- [ ] [AI] Run a final `plan-execution-checker` against the implemented outcome, apply revalidated
      in-scope findings, and re-run it; acceptance: zero CRITICAL, HIGH, or MEDIUM completion
      findings remain.
- [ ] [AI] Move the public plan with
      `git mv plans/in-progress/optimize-pr-process
plans/done/<YYYY-MM-DD>__optimize-pr-process`; acceptance: all six files move together and no
      stale old-path reference remains after `rg -n "plans/in-progress/optimize-pr-process" .`.
- [ ] [AI] Update `plans/in-progress/README.md`, `plans/done/README.md`, and every other plan link;
      acceptance: indexes accurately show the archived status and completion date.
- [ ] [AI] Commit archival on the final public PR branch with
      `git commit -m "chore(plans): move optimize-pr-process to done"`, push to that PR branch, and
      run the bounded review/fixer process against the archival-inclusive head; acceptance: no
      direct push to `main`, all threads resolved by evidence-backed disposition, all current-head
      checks green, and no sixth AI cycle.
- [ ] [AI] Merge the final public PR using the verified repository merge method; acceptance: public
      `origin/main` contains the archived plan and cross-repo closure record.
- [ ] [AI] For each repo worktree, run `git status --porcelain`, `git fetch origin`, and
      `git merge-base --is-ancestor "$(git rev-parse HEAD)" origin/main`; acceptance: worktree is
      clean and its head is fully merged before cleanup is considered.
- [ ] [AI] Remove only the two worktrees created/owned by this plan with non-force
      `git worktree remove worktrees/optimize-pr-process` from each repo root, then run
      `git worktree prune`; acceptance: both paths disappear and no concurrent actor's worktree or
      branch is touched. If removal refuses, retain it and report the exact dirty/unmerged state.

### Phase 18 Gate

> All checks below must pass before declaring the plan complete.

- [ ] [AI] Verify the final public closure PR is merged, both repository closure records are
      auditable, and both worktrees are removed or retained with an exact recoverable blocker;
      acceptance: no unpushed commit, unresolved obligation, or hidden-only audit record remains.

> **Pause Safety**: the plan is archived and both repository tracks are terminal. Safe to stop. To
> resume only for audit: remeasure the linked PR artifacts from their recorded merge SHAs.
