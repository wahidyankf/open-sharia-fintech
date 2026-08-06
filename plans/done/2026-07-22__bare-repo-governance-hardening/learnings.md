<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: bare-repo-governance-hardening

Append one `## Learning: <one-line summary>` section per generalizable observation, sanitized per
the secret/sensitivity gate before it is ever written. Entry shape:

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning
- **Terminal state**: routed inline to `<path>` / filed as `plans/backlog/<slug>/` / discarded — `<reason>`
```

> **Watch for this plan's own highest-yield source**: Phases 4 and 5 execute the very procedure
> `bare-repo-landing-method.md` documents. Any friction between the written steps and what execution
> actually required is a defect in that document — record it here, and Phase 6 routes it back into
> the document in all three repos.
>
> If execution surfaces nothing generalizable, replace this line with the explicit escape:
> `No generalizable learnings — <one-line reason>`. Never leave the file silently empty.

## Learning: the defect reproduced live during this plan's own promotion

- **Context**: promoting the plan from `backlog/` to `in-progress/` on 2026-07-21, re-verifying the
  repo-grounded claims in `tech-docs.md` before running the quality gate.
- **Observation**: both bare siblings read `2 0` on
  `git rev-list --left-right --count origin/main...main` — local `main` two commits behind
  `origin/main` in each. The lagging commits (`c12e1eb7f` + `53d9081b7` in `ose-primer`,
  `474545a69` + `f6ecdcc0b` in `ose-infra`) were landed through side worktrees in an earlier
  session. Nothing failed and nothing warned; the lag is only visible if you ask for it explicitly.
  `tech-docs.md` had recorded `0 0` for both, so the plan's own written state had silently gone
  stale in under a day.
- **Why it might generalize**: this is the plan's motivating failure class, observed without being
  sought, on a repo whose maintainer already knows about it. It is direct evidence for the strength
  of C1's terminal-reconcile step — a rule that is easy to forget is not adequately served by prose
  alone, which is worth weighing against **DD-2**'s no-automation stance at Phase 6 triage.
  It also shows any "verified state" line in a plan needs a re-verification step, not just a date.
- **Terminal state**: **routed inline, already landed** — `<C1>` §"Worked example — the 2026-07-21
  sibling drift" is exactly the proposed route: it shows the `2 0` reading in both siblings, the
  `git fetch origin main:main` recovery, and the resulting `0 0`. The route was satisfied during
  Phase 2 authoring, before this entry was triaged, so no further work is owed. Recorded here rather
  than discarded because the entry is the live evidence that motivated the section.

## Learning: varying the approach each iteration makes a stability-based termination rule unreachable

- **Context**: running `plan-quality-gate` on this plan before execution. The gate terminates on
  **two consecutive zero-finding iterations** and caps at 7 iterations, escalating at 5.
- **Observation**: each iteration was briefed to **vary its approach** so it would not simply repeat
  the last one. The gate then ran 5 (2 MEDIUM), 6 (1 HIGH), 7 (zero) and hit the budget with
  `consecutive_zero_count = 1` — closed at zero outstanding findings, but by exhaustion rather than
  by convergence. The termination rule tests stability by asking whether an **equivalent** check
  returns zero twice running; a deliberately different check each round measures coverage instead, so
  two consecutive zeros were structurally impossible no matter how clean the plan got.
- **Why it might generalize**: it is a general defect in how a saturation loop is driven, not
  specific to this plan. Varying the approach and testing for stability are both individually sound
  and jointly incoherent — the fix is to sequence them (vary while findings are still arriving, then
  hold the approach fixed once a round comes back clean, so the confirming round is genuinely
  equivalent), not to drop either. The same shape applies to any loop-until-dry harness whose exit
  condition counts consecutive empty rounds.
- **Terminal state**: **folded into**
  [`plans/ideas/plan-quality-gate-convergence.md`](../../ideas/q2-not-urgent-important/plan-quality-gate-convergence.md) —
  an existing brief on exactly this loop's convergence, per the ideas folder's integrate-don't-
  duplicate rule. Not landed inline: the fix is a change to how iterations are briefed in a
  governance workflow, which is a design question the brief exists to resolve, not a typo.

## Learning: a checker without the tool its acceptance clauses name will substitute silently

- **Context**: Phases 2 and 3 were executed by agents whose toolset was `Read`/`Write`/`Edit`/
  `Glob`/`Grep` — no `Bash`. Every acceptance clause in those phases names a literal shell command.
- **Observation**: both agents substituted the `Grep` tool's count mode for `grep -Fc` and reported
  the results as the clause's `Result`. Both disclosed the substitution in a tooling note, which is
  the good outcome. But the substitution was **not uniform in reach**: neither could run
  `rhino-cli`/`markdownlint-cli2` at all, so the markdown gates were skipped entirely for the phase —
  and because their disclosed lint runs covered `repo-governance/` but not `plans/`, five
  markdownlint violations reached the pre-commit hook undetected in `delivery.md` itself.
- **Why it might generalize**: the failure is not "the agent lacked a tool" — it is that an
  acceptance clause naming a shell command reads as satisfied when a **differently-scoped**
  substitute returns a plausible number. A phase whose gate is defined in shell commands needs its
  executor's tool grant checked against those commands up front, and any phase that edits markdown
  needs its lint scope to cover **every** path it edited, not just the phase's headline directory.
- **Terminal state**: filed as
  [`plans/ideas/acceptance-clause-vacuity.md`](../../ideas/q1-urgent-important/acceptance-clause-vacuity.md) — the
  tool-grant mismatch is one of four instances that brief carries, all of the same shape: a clause
  that returns a plausible number while certifying nothing. Both candidate surfaces
  (`subagent-orchestration.md`, `maker-checker-fixer.md`) are named in the brief as targets; the
  choice between them is the design question that blocks promotion, so it is not landed inline.

## Learning: Phase 4/5's file-agreement steps do not name `<GATE>`, which cycle 1 turned into a real edit site

- **Context**: PR-review cycle 3 (final) reversed cycle 1's floor-not-ceiling fix to
  `pr-review-quality-gate.md` (`<GATE>`) into a hard-ceiling-not-floor fix, per an explicit user
  ruling. Re-deriving every site touching this rule (per the cycle-3 fixer brief) required rereading
  Phase 4 and Phase 5 in full.
- **Observation**: `<GATE>`'s Path Constants entry (`delivery.md` — the `<GATE>` bullet) still
  describes it as a "source note ... originally left unedited, corrected during PR-review cycle 1,"
  but Phase 4's and Phase 5's propagation steps only name `<MERGE>`, `<PARITY>`, `<PLANS>`, `<SDLC>`,
  `<PROMO>` for the sibling-agreement diff (the "verify the remaining five files agree" step) — never
  `<GATE>`. Since cycle 1 already made `<GATE>` a real `ose-public`-only edit, and cycle 3 edits it
  again, Phase 4/5 as currently written would propagate `<MERGE>`/`<PLANS>`/etc. but silently leave
  the siblings' copies of `<GATE>` un-diffed against the corrected `ose-public` version — nothing
  in Phase 4 or Phase 5 as written would catch a stale sibling `<GATE>`.
- **Why it might generalize**: a source-of-truth file that starts as "read-only, never edited" and
  later becomes a real edit site (as `<GATE>` did across two review cycles) needs its propagation
  bookkeeping updated at the same time the "unedited" claim is retracted — the retraction and the
  propagation-list update are two different edits to two different places, and it is easy to make
  the first without the second.
- **Terminal state**: **discarded as a standalone learning — plan-local, and already acted on.** The
  concrete half was a correction to this plan's own Phase 4/5 step list, applied during execution:
  both phases swept `<GATE>` and the sibling copies were diffed against the corrected `ose-public`
  version. Nothing durable is owed for that. Its generalizable half — a propagation checklist
  enumerated by change ID under-covers the real changeset — is not lost: it is carried by
  [`plans/ideas/propagation-checklist-under-coverage.md`](../../ideas/q2-not-urgent-important/propagation-checklist-under-coverage.md)
  as one of that brief's four consolidated instances.

## Learning: CONFIRMED LIVE in Phase 4 — the `<GATE>` propagation gap is not hypothetical

- **Context**: executing Phase 4 against `ose-primer`. The entry immediately above predicted that
  Phase 4 would propagate `<MERGE>` while leaving the sibling's `<GATE>` stale.
- **Observation**: exactly that. `ose-primer`'s `<MERGE>` carried the **pre-reversal** wording
  ("default 3, a floor not a ceiling") at both precondition-(a) sites, each linking the
  `#saturation-not-a-fixed-count-loop-exit` anchor — the section `ose-public` removed in cycle 3.
  Executing Phase 4's C5 step literally (append the hard-ceiling qualifier to `<MERGE>` only) would
  have produced a repo whose merge protocol says "hard ceiling" while the workflow it cites as
  normative still says "floor, and saturation is the ceiling", with three live inbound links to a
  section that must not survive. The gap is self-revealing at execution time only because the
  sibling's pre-state happened to differ; a reader following the checklist without diffing would
  have shipped the contradiction.
- **Why it might generalize**: a propagation checklist enumerated by **change ID** silently
  under-covers when later review cycles expand a change's site list. The safe unit of propagation is
  the **merged changeset's file list**, not the plan's authoring-time C-list. `ose-public`'s merged
  PR touched 22 files; Phase 4's checklist names 8.
- **Terminal state**: filed as
  [`plans/ideas/propagation-checklist-under-coverage.md`](../../ideas/q2-not-urgent-important/propagation-checklist-under-coverage.md).
  This entry supplies that brief's sharpest data point — the source PR touched 22 files while the
  propagation checklist named 8 — and its proposed route (derive the file list from
  `git show --stat <merge-sha>`) is the brief's lead proposal. Target surface:
  `repo-governance/workflows/plan/plan-multi-repo-parity-planning.md`.

## Learning: a propagation step's "already verified absent in the sibling" premise expires

- **Context**: Phase 4's brief-deletion step asserts, as settled fact, that neither two-pager exists
  in `<PRIMER>` ("zero hits", recorded in `tech-docs.md` §Verified In-Repo State and again in
  DD-10), and instructs the executor to "confirm once and move on" with **no deletion**.
- **Observation**: false at execution time for one of the two briefs.
  `ose-primer/plans/ideas/bare-repo-worktree-landing-hygiene.md` exists, plus its
  `plans/ideas/README.md` index line, landed by `6a5a8b9ee` — the parity mirror of `ose-public`'s
  own `4d229bf9d`, i.e. the brief propagated sideways to the sibling **after** (or unnoticed by) the
  DD-10 survey that declared it absent. The second brief
  (`bare-repo-delivery-mode-governance-hardening`) genuinely is absent, so the premise was half
  right, which is the hardest kind to catch. The step's own acceptance criterion
  (`grep -rF "bare-repo-worktree-landing-hygiene" <PRIMER-WT>` exits 1) **failed** as written, and
  the only action that satisfies it is the deletion the step's prose forbids.
- **Why it might generalize**: the step is written as an assertion with a confirmation, not as a
  check with a branch. When a plan records "verified absent, do nothing", it should still say what
  to do **if present** — otherwise the executor must choose between the prose and the acceptance
  clause, which are in contradiction the moment the world moves. Note also the direction of the
  drift: a sibling gained content from `ose-public` through an unrelated parity commit, so "surveyed
  once at authoring time" is not durable for anything in `plans/ideas/`.
- **Terminal state**: candidate route (1) — re-check the identical premise live at Phase 5 — was
  **executed**, and the premise was false in `ose-infra` too (see the four-premise entry below).
  Route (2) is filed as
  [`plans/ideas/propagation-checklist-under-coverage.md`](../../ideas/q2-not-urgent-important/propagation-checklist-under-coverage.md):
  a "verified absent in sibling" claim needs an explicit if-present branch, never a bare do-nothing.

## Learning: a sibling can be AHEAD of the source of truth on a shared governance document

- **Context**: Phase 4's C4a/C4b/C4c steps instruct the executor to mirror the `ose-public` edit into
  `<PRIMER>`'s copy of `<PARITY>`, each with a falsifiability clause of the form "exits 1 before this
  step".
- **Observation**: `ose-primer`'s `<PARITY>` had **already** been independently hardened for
  bare-repo awareness by an earlier, unpropagated change — its `values:` frontmatter, its
  `main-to-origin-main` mode definition, its deviation-matrix bullet, and its meta-question #1 were
  all property-bound rather than name-bound, and meta-question #1 already refused to offer
  `main-to-origin-main`. So C4a's acceptance grep (`"any bare repo"`) printed **1 and exited 0
  before any edit**, and C4b/C4c were substantially pre-satisfied in different wording. The same
  happened for C6a: `grep -Fc "is-bare-repository"` in the sibling's `<SDLC>` returned 1 pre-edit.
  Meanwhile the sibling's prohibition was the **conditional** form ("from inside a linked worktree")
  that `ose-public`'s own C6c had already ruled operatively wrong — so the sibling was
  simultaneously ahead on structure and behind on correctness.
- **Why it might generalize**: "propagate the source repo's wording verbatim" is sound only for a
  file the source repo **owns outright** (here, `<C1>`, per DD-10's verbatim-copy criterion). For
  every co-evolved document, a propagation phase must diff first and decide per-site, because a
  pre-change baseline measured in the source repo does not predict the sibling's baseline. Any
  acceptance clause asserting a sibling's pre-state is an assumption about a repo the plan did not
  read.
- **Terminal state**: filed as
  [`plans/ideas/propagation-checklist-under-coverage.md`](../../ideas/q2-not-urgent-important/propagation-checklist-under-coverage.md)
  — propagation acceptance criteria should assert the **post** state only, never a sibling's
  pre-state. This entry contributes the brief's most counter-intuitive data point: an acceptance grep
  that passed **before** any edit was made, which is indistinguishable from a successful edit.

## Learning: the plan's own `<PUBLIC>/<C1>` copy source did not exist at Phase 4 time

- **Context**: Phase 4's C1 step says to copy `<C1>` "verbatim from merged `ose-public`", and the
  Phase 4 Gate diffs `<PUBLIC>/<C1>` — a **working-tree path** in the primary checkout — against the
  sibling's `origin/main` copy.
- **Observation**: `<PUBLIC>/repo-governance/development/workflow/bare-repo-landing-method.md` did
  not exist. `ose-public`'s local `main` was diverged from `origin/main` (`1 3`: the merged PR #79
  commit `2b719347a` absent locally, three unrelated plan-doc commits from a concurrent session
  present locally and unpushed), so the primary checkout had never seen the merged file. This is the
  plan's own motivating defect — a local `main` lagging its remote — reproduced a third time, now
  in the **non-bare** repo, and it broke a step that assumed a filesystem path.
- **Why it might generalize**: on a shared machine a plan may not reconcile another session's `main`
  just to read a file. A cross-repo copy step should name a **git ref** (`git show origin/main:<path>`),
  not a working-tree path, so it is correct regardless of any checkout's sync state. Both copies were
  confirmed byte-identical (`b48153277…`) once the ref form was used, so the substitution was safe —
  but the step as written was unexecutable.
- **Terminal state**: **routed** to `<C1>` via the `<C1>` Correction Propagation Sub-Cycle — new
  §"Reading a File From Another Repository", stating that a cross-repo read is addressed by git ref
  (`git -C <other-repo> show origin/main:<path>`) and never by working-tree path, because on a shared
  machine another session's local `main` may lag and a bare source repository has no path to read at
  all. Landed in `ose-public` PR
  [#81](https://github.com/wahidyankf/ose-public/pull/81); propagated to both siblings by the same
  sub-cycle and **landed there too** — `ose-primer` PR
  [#15](https://github.com/wahidyankf/ose-primer/pull/15) (merged `cedabb2f1`) and `ose-infra` PR
  [#17](https://github.com/wahidyankf/ose-infra/pull/17) (merged `1d64990bb`). All three copies of
  `<C1>` are byte-identical at sha1 `618e74ff8ebc5c0a0abf19b2a40c2af9ac2e01db`, verified by `diff`
  against each sibling's `origin/main` blob after fetching. The plan-local half — Phase 5's own copy step — was already switched to the ref form
  during execution.

## Learning: a fourth deviation — carve-outs to trunk-based-development.md and its SKILL.md mirror are unrecorded, and Phase 5's checklist names neither file

- **Context**: `ose-primer`'s PR #14 (Phase 4) PR-review cycle 2 found that
  `repo-governance/development/workflow/trunk-based-development.md` and
  `.claude/skills/repo-practicing-trunk-based-development/SKILL.md` both asserted
  `main-to-origin-main` was unconditionally available, which is false in a bare clone. Cycle 2 fixed
  both files with property-bound bareness carve-outs; cycle 3 then found the carve-outs were applied
  only at the specific lines cited, not to every mode-selection statement in either file, and swept
  both files for the remaining sites (the highest-leverage one being the SKILL.md section that
  literally instructs an agent to select a direct-push mode).
- **Observation**: neither file is in this plan's C1-C7 Phase 4 checklist scope — they are not
  `<C1>` and are not one of `<MERGE>`/`<PARITY>`/`<PLANS>`/`<SDLC>`/`<PROMO>`/`<GATE>`. The edits
  happened only because a PR-review cycle discovered the gap live, not because any plan step named
  these files. `ose-infra` is bare too (asserted by this same PR at
  `docs/reference/sdlc-gate-standard.md` and `plan-multi-repo-parity-planning.md`), and Phase 5
  copies `<C1>` into `ose-infra` and works the identical C1-C7 checklist — which, unchanged, will
  skip both files there exactly as Phase 4's checklist did here, shipping the same
  advertises-an-unavailable-mode defect a second time.
- **Why it might generalize**: this is the same failure class as the `<GATE>`-propagation and
  `<PARITY>`-ahead-of-source learnings recorded above — a propagation checklist enumerated by
  change ID at authoring time silently under-covers sites a later review cycle discovers need the
  same treatment. The fix belongs in the checklist, not in tribal memory of what cycle 2 happened to
  touch in `ose-primer`.
- **Terminal state**: **discarded as a standalone learning — plan-local, and executed.** The
  immediately-actionable half was done: Phase 5 swept both files in `ose-infra` and applied
  property-bound carve-outs to every mode-selection statement, not only the sites `ose-primer`'s
  cycle 2 cited. Its generalizable half is the same class as the entry above and is carried by
  [`plans/ideas/propagation-checklist-under-coverage.md`](../../ideas/q2-not-urgent-important/propagation-checklist-under-coverage.md).
  Worth noting what this entry got right and wrong: it correctly predicted the class would recur in
  `ose-infra`, and it under-predicted the reach — cycle 2 there found the same defect in `AGENTS.md`,
  which neither this entry nor `ose-primer`'s sweep had considered.

## Learning: `ose-primer`'s `main-ci` was already red before Phase 4, and only the scheduled run sees it

- **Context**: Phase 4's gate requires "CI green on its `main`" after the `ose-primer` merge.
  Checking that at merge commit `a94539c03` surfaced a failure that predates this phase entirely.
- **Observation**: `ose-primer` runs three workflows on `main`. Two — `pr-quality-gate` and
  `validate-env` — went **green** at the merge commit. The third, `main-ci`, is **schedule**-driven
  and was already failing at `53d9081b7`, the `origin/main` this phase branched from: two scheduled
  runs (12:24 and 18:17 on 2026-07-21, both **before** this phase's 20:08 merge) failed on
  `Mermaid diagram validation (all .md)` with 3 violations in
  `plans/done/2026-07-03__unify-rhino-cli-sdlc-parity/tech-docs.md`. `git diff --name-only
53d9081b7 a94539c03 -- plans/done/` is **empty** — this merge touched none of the 20 changed files
  under `plans/done/`, so the failure is neither caused nor worsened here. Two compounding reasons it
  went unseen until after the merge: the workflow is scheduled rather than push-triggered (it did not
  run on the merge at all), and the local gate this plan prescribes scopes mermaid validation to
  `repo-governance docs`, which cannot reach `plans/done/`.
- **Why it might generalize**: "CI green on `main`" is not a single observable when a repo mixes
  push-triggered and schedule-triggered workflows — a phase can satisfy every push-gated check and
  still leave `main` red on a cadence nobody watched. And a _repo-wide_ CI validator paired with a
  _directory-scoped_ local gate guarantees a class of failure that is structurally invisible until
  CI runs. The two scopes should match, or the local gate should state which paths it deliberately
  does not cover.
- **Terminal state**: **folded into an existing brief** (details below). **Not fixed here,
  deliberately**: the same
  archived file exists in `ose-public` (confirmed on its `origin/main`), so this is a cross-repo
  condition and patching only `ose-primer` would manufacture exactly the divergence DD-10 and the
  parity workflow exist to prevent. The class is already tracked in `ose-public` as
  `plans/ideas/ayokoding-mermaid-diagram-remediation.md` ("636 mermaid violations exposed by the
  `detect_kind` fix"). **Both candidate routes are now closed.** Route (1): this `plans/done/`
  instance, and the generalizable half (a repo-wide CI validator paired with a directory-scoped local
  gate guarantees a class of failure invisible until CI runs), are **folded into**
  [`plans/ideas/ayokoding-mermaid-diagram-remediation.md`](../../ideas/q2-not-urgent-important/ayokoding-mermaid-diagram-remediation.md).
  Route (2): **executed at Phase 5** — the local gate was widened to
  `repo-governance docs .claude plans/ideas` _and_ CI's own `--exclude`-qualified command was run
  directly against `ose-infra`, and the two agreed at `0 violation(s)`. That measurement also
  established `ose-infra` has **no** equivalent exposure: both its workflows use the qualified form
  and its scheduled runs were green, so the Phase 4 finding does not generalize to it.
- **Root cause corrected at Phase 7 (2026-07-22)** — the account above blamed the local gate's
  directory scope. That is a contributing factor, not the reason `ose-primer` alone is red. The three
  repos invoke the same validator with three different flag sets in `main-ci.yml`: `ose-public` uses
  `--exclude apps/rhino-cli/tests/fixtures --exclude plans/done --exclude apps/ayokoding-www/content`,
  `ose-infra` uses `--max-depth=4 --exclude plans/done --exclude apps/rhino-cli/tests/fixtures`, and
  `ose-primer` uses only `--exclude apps/rhino-cli/tests/fixtures`. `ose-primer` is the sole repo
  missing `--exclude plans/done`, and the file it fails on is **byte-identical** to `ose-public`'s
  copy (`diff` of both `origin/main` blobs: no difference). Identical content, opposite verdicts,
  decided by a flag. Editing the archived diagram would treat the symptom; the root-cause fix is a
  CI-parity decision about which flag set is correct — and `ose-primer`'s stricter form may well be
  the right one, with the other two repos' `plans/done` excludes being the drift. The corrected
  measurement is folded into the same brief.

## Learning: a bare repo cannot push at all — the pre-push hook needs a work tree the repo does not have

- **Context**: the terminal cleanup of Phase 4, after the `ose-primer` worktree was removed and local
  `main` reconciled. The Worktree and Artifact Cleanup Convention requires a plan to delete the
  remote branches it pushed, via `git push origin --delete <branch>` once the PR reports MERGED.
- **Observation**: run from the bare repo, that push **fails**, and not for a content reason:

  ```console
  $ git -C <PRIMER> push origin --delete bare-repo-governance-hardening
  NX  Affected criteria defaulted to --base=origin/main --head=HEAD
  NX  Command failed: git diff --name-only --no-renames --relative HEAD .
  fatal: this operation must be run in a work tree
  husky - pre-push script failed (code 1)
  error: failed to push some refs
  ```

  The husky pre-push hook runs `nx affected`, which shells out to `git diff … HEAD .` — a work-tree
  operation. A bare repo has no work tree, so **every** push originating from it is blocked,
  including a pure ref **deletion** that carries no content and could not fail a quality gate even in
  principle. This is a chicken-and-egg with `<C1>`'s own step order: `<C1>` correctly routes content
  pushes through a linked worktree, but branch cleanup is specified to happen **after** the worktree
  is removed, at which point the only remaining actor is the bare repo that cannot push.

- **Why it might generalize**: it is a structural property of "bare repo + work-tree-dependent
  pre-push hook", not a quirk of this branch or this plan — it will recur on every cleanup in
  `ose-primer` and `ose-infra`, and `<C1>` currently gives the reader no warning and no route.
  Note the trap it sets: the obvious workaround is `--no-verify`, which the Git Push Safety
  Convention requires explicit per-instance user approval for. A rule that is unexecutable as
  written pushes its reader toward the one escape hatch that needs permission.
- **Terminal state**: **routed** — a genuine `<C1>` defect, so it goes through the `<C1>` Correction
  Propagation Sub-Cycle (`ose-public` first, never an in-place sibling edit).
  **Resolved this phase** by deleting the merged ref through the GitHub API
  (`gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<branch>`) — the identical path
  `gh pr merge --delete-branch` takes natively, so no hook was bypassed and no `--no-verify` was
  used; the content had already merged through a fully-gated PR. **The candidate `<C1>` fix is now
  routed and written**: new §"Remote-Branch Cleanup in a Bare Repository" states both working routes
  (delete from inside the linked worktree before removing it, or delete the ref through the forge
  API afterwards), names the ordering trap in `<C1>`'s own step sequence, and says plainly that
  `--no-verify` is **not** the sanctioned answer. Landed in `ose-public` PR
  [#81](https://github.com/wahidyankf/ose-public/pull/81); propagated to both siblings by the same
  sub-cycle and **landed there too** — `ose-primer` PR
  [#15](https://github.com/wahidyankf/ose-primer/pull/15) (merged `cedabb2f1`) and `ose-infra` PR
  [#17](https://github.com/wahidyankf/ose-infra/pull/17) (merged `1d64990bb`). All three copies of
  `<C1>` are byte-identical at sha1 `618e74ff8ebc5c0a0abf19b2a40c2af9ac2e01db`, verified by `diff`
  against each sibling's `origin/main` blob after fetching. **Confirmed a second time at Phase 5** — the identical failure recurred in `ose-infra`
  and the same API route resolved it, which is what upgraded this from a one-off to a documented
  property of the topology.

## Learning: Phase 5 re-verified four suspect premises against `ose-infra` — three were false again

- **Context**: executing Phase 5 (`ose-infra` propagation). The Phase 4 entries above flagged four
  premises as expired or defective. Phase 5's brief required re-verifying each **live** rather than
  inheriting Phase 4's finding, and reporting any clause that already passed before an edit.
- **Observation**, premise by premise:
  1. **`<MERGE>`-only propagation is insufficient — confirmed, and worse here than in `ose-primer`.**
     `ose-infra` carried the pre-reversal wording plus **seven** live links to the deleted
     `#saturation-not-a-fixed-count-loop-exit` section, across four files
     (`pr-review-quality-gate.md` ×3, `pr-merge-protocol.md` ×2, `plans.md` ×1,
     `plan-quality-gate.md` ×1) — `ose-primer` had three. An eighth site the checklist names nowhere,
     `repo-governance/development/workflow/README.md`'s PR Merge Protocol index entry, stated the
     floor rule in prose with no anchor link at all, so no link-based sweep would have found it.
  2. **"Two-pager already absent" — false again, identically half-right.**
     `plans/ideas/bare-repo-worktree-landing-hygiene.md` existed (landed by `2f9beaac0`) with its
     index line; the second brief genuinely was absent. **New defect, distinct from Phase 4's**:
     Phase 5's acceptance clause greps for the **second** slug
     (`bare-repo-delivery-mode-governance-hardening`), which exits 1 vacuously, while its prose
     asserts _both_ are absent. Phase 4's clause at least named the slug that was actually present.
     So Phase 5's step was unfalsifiable in the exact direction it needed to be falsifiable.
  3. **Sibling ahead of the source — confirmed.** `<PARITY>`'s `"any bare repo"` grep printed `1` and
     **exited 0 before any edit**. `ose-infra` additionally carries a §Verifying Bareness (Method)
     section that **neither** `ose-public` nor `ose-primer` has. Its `--is-bare-repository`
     prohibition was the conditional form C6c ruled wrong, so the fix was to make it unconditional
     in place — deleting the section would have broken four inbound `#verifying-bareness-method`
     anchors and destroyed content better than the source repo's.
  4. **`<PUBLIC>/<C1>` path form — did NOT reproduce.** The working-tree path existed this time,
     because `ose-public`'s local `main` had since been fast-forwarded to `origin/main`
     (`415c8f869`). The ref form was used anyway and both agreed at `b48153277`. Worth recording
     because it shows the defect is **intermittent, not latent-but-dormant**: it presents only while
     some other session's `main` is lagging, which is exactly when a reader is least likely to
     suspect it.
- **Why it might generalize**: the score across two siblings is 3-of-4 false, 1-of-4 intermittent.
  A propagation premise measured once at authoring time should be treated as **expired by default**,
  not as fact awaiting contradiction. And an acceptance clause that names a specific slug, file, or
  count is only as good as the accuracy of that identifier — clause 2 above was well-formed,
  falsifiable, and pointed at the wrong string, which is indistinguishable from passing.
- **Terminal state**: split across two briefs, because this entry carries two distinct classes. The
  propagation half — assert **post** state only, derive the file list from the source PR's actual
  diff, carry an explicit if-present branch for every "verified absent" claim — is filed as
  [`plans/ideas/propagation-checklist-under-coverage.md`](../../ideas/q2-not-urgent-important/propagation-checklist-under-coverage.md).
  The clause half — a well-formed, falsifiable clause pointing at the wrong string is
  indistinguishable from passing — is filed as
  [`plans/ideas/acceptance-clause-vacuity.md`](../../ideas/q1-urgent-important/acceptance-clause-vacuity.md).

## Learning: the reading surfaces got the new rule; the writing surfaces did not

- **Context**: PR-review cycle 1 on `ose-infra` PR #16, finding 2 (HIGH, confidence 90).
- **Observation**: after C3/C4/C6 landed, `ose-infra`'s **reading** surfaces correctly stated that a
  bare repo cannot use `main-to-origin-main` or `main-to-pr` — `plans.md`, the parity workflow, the
  SDLC gate standard, `trunk-based-development.md` and its SKILL mirror. But the **writing**
  surfaces, the ones that actually cause a delivery mode to be chosen and written into a plan, still
  offered the full unqualified four-mode vocabulary: `plan-maker`'s Step 7 table, the
  `plan-creating-project-plans` SKILL's §Delivery Mode, `git-push-default.md` Standard 3, and — found
  only by sweeping, cited by no one — `plan-planning.md`'s Step 8 grill question and `plan-fixer`'s
  Delivery Mode Fixes options. `plan-checker` validates only that the value is one of the four mode
  strings, never repo-topology compatibility (by explicit design), so a `main-to-origin-main`
  declaration emitted in a bare repo passes every gate and fails at Step 0 of execution.
- **Why it might generalize**: this is a distinct failure shape from the propagation-under-coverage
  entries above, and a sharper one. Stating a constraint on the documents that **describe** a
  vocabulary does not constrain the agents that **emit** values from it. When a rule narrows a set of
  legal values, the sweep has to cover producers and validators, not just prose — and if the
  validator is deliberately structural (string membership only), the producers are the _only_ place
  the constraint can live.
- **Terminal state**: filed as
  [`plans/ideas/class-sweep-completeness.md`](../../ideas/q2-not-urgent-important/class-sweep-completeness.md) — this entry
  is that brief's first of three instances. The candidate route survives into it: when a change
  restricts a declared enum, enumerate the maker/producer surfaces explicitly, since the checker may
  be structurally unable to carry the restriction. Target surface named there:
  `repo-governance/development/pattern/maker-checker-fixer.md`.

## Learning: the sweep that fixed "every mode-declaring surface" missed the one file every agent auto-loads

- **Context**: PR-review cycle 2 on `ose-infra` PR #16, finding 1 (HIGH, confidence 88).
- **Observation**: cycle 1's fixer commit `9c3656ad3` is titled _"add bareness carve-outs to every
  mode-declaring surface"_ and did reach `plan-maker.md`, `plan-fixer.md`, `plan-planning.md`,
  `git-push-default.md`, and both SKILL files. It missed `AGENTS.md`, where a
  case-insensitive search for `bare` returned **no matches at all** and §Delivery Mode stated all
  four modes flatly with no qualifier. `AGENTS.md` is the root canonical instruction file: every harness auto-loads it on every
  invocation, so it is the highest-traffic mode-declaring surface in the repo and the one most likely
  to be the actual source of a wrong declaration. The sweep enumerated `.claude/`, `.opencode/`, and
  `repo-governance/` and never looked at the repo root.
- **Why it might generalize**: root instruction files (`AGENTS.md`, `CLAUDE.md`, `CONVENTIONS.md`)
  sit outside every directory-scoped sweep, because a sweep is naturally expressed as a walk over the
  directories that hold the artifact class. They are the default blind spot of any "fix the class"
  pass, and they are simultaneously the surface with the widest blast radius. A class sweep must name
  the root instruction files explicitly, not rely on a directory walk reaching them.
- **Second-order constraint discovered while fixing it**: the fix could not be a blockquote. The
  Instruction-File Size Budget (`repo-config.yml` `instruction-size`) puts `AGENTS.md` at
  `target: 24000 / warn: 27000 / fail: 30000`; `ose-infra`'s was 23902 bytes pre-fix and 24096
  post-fix — over the advisory target, inside the passing band. The same clause is **not** currently
  applicable to `ose-public`, whose `AGENTS.md` is **29982 bytes, 18 bytes below its hard-fail
  threshold of 30000**. So the source of truth physically cannot absorb the carve-out that its
  downstream sibling now carries: `ose-infra` leads `ose-public` on this specific surface, and
  closing that gap in `ose-public` requires progressive disclosure first, not an edit.
- **Terminal state**: both routes filed. (1) Root instruction files belong in the enumerated surface
  list wherever a class sweep is prescribed — filed as
  [`plans/ideas/class-sweep-completeness.md`](../../ideas/q2-not-urgent-important/class-sweep-completeness.md), where this is
  the second of three instances. (2) The byte-budget blocker is **folded into**
  [`plans/ideas/agents-md-progressive-disclosure.md`](../../ideas/q1-urgent-important/agents-md-progressive-disclosure.md),
  an existing brief on exactly that ceiling, per the integrate-don't-duplicate rule. The fold matters
  for more than bookkeeping: it converts that brief's premise from a forecast into a recorded event,
  since the ceiling has now blocked a real correction rather than merely threatening to.

## Learning: `ose-infra`'s `setup-rust` composite action has no retry on the toolchain download, and it flaked seven times in one phase

- **Context**: Phase 5, `ose-infra`. **Seven** CI job failures — four on PR #16, three more on `main`
  after the merge — every one in `.github/actions/setup-rust`, at one of two steps that both fetch
  from the same host:

  ```text
  error: could not download file from 'https://static.rust-lang.org/dist/channel-rust-stable.toml'
    ... connection reset    (29868278329, head 9c3656ad3, "Harness duplication validation")
    ... timed out           (29871560447, head 30ec8dedb, "repo-config.yml schema parity")
    ... operation timed out  (29875931376, head 3423c7b69, "Validate env contract")
    ... timed out           (29878539420, main 70a4a463c, "Validate env contract")
  error: command failed: downloader https://static.rust-lang.org/rustup/dist/.../rustup-init
    ... (29875931376 retry, 29878539451 "Governance validators", 29878856211 "repo-config parity")
  ```

- **Observation**: the changeset is **markdown-only** — it maps to no Nx project, and each failing
  job passes cleanly when CI's exact command is run locally. The failures hit a **different job every
  time**, which is the signature of a shared setup step rather than a job-specific defect, and
  several cascaded into a `Quality gate → Check all gates` failure. So a pure-docs change was gated
  seven times by a network fault it could not possibly have caused. Each was resolved with
  `gh run rerun --failed`, which is a retry of a flaked infrastructure step, **not** a gate bypass —
  no `--no-verify`, no hook skipped, no gate marked green by hand.
- **Frequency is the finding.** Seven hits in a single phase is not a rare event to be tolerated; at
  that rate every non-trivial change in this repo pays a re-run tax, and the tax is invisible in any
  per-run report because a re-run reports green. The failure mode also **escalated mid-phase**: the
  first four were the toolchain manifest download, but later ones failed to fetch `rustup-init`
  itself. The CI log shows that installer fetch already carries `curl --retry 10
--retry-connrefused`, so when even it started failing the fault was clearly sustained rather than
  transient — which is why the last retry was preceded by a deliberate wait rather than an immediate
  re-run.
- **Correction, made during Phase 6 triage**: an earlier draft of this entry attributed that
  `curl --retry 10` to `.github/actions/setup-rust/action.yml`'s own first step and built a tidy
  root-cause story on it ("the hardening stopped one step short"). **That attribution was wrong.**
  Re-reading the action confirms it contains no `curl`, no `retry`, and no `rustup-init` invocation
  at all — the retry-wrapped installer fetch lives **inside the third-party action**, and it was
  visible only because the CI log interleaves that action's internal steps with ours. The line was
  read out of a log and assigned to the wrong file. The observable facts (seven failures, the host,
  the escalation) are unchanged; the causal explanation was invented, and it was invented in the
  direction that made the fix look easy.
- **A second correction — the three repos are not the same shape**: this entry originally assumed a
  single shared `setup-rust` whose fix could be copy-pasted. Verified otherwise: `ose-public` and
  `ose-primer` install via `actions-rust-lang/setup-rust-toolchain@v1`, while `ose-infra` uses
  `dtolnay/rust-toolchain@stable`. "Apply the same fix in all three" is therefore a reconciliation
  task, not a copy.
- **Why it might generalize** — two things, and the second is the more valuable. First, the
  technical one: a retry applied to a tool's bootstrap but not to the tool's own first large download
  buys little, since the expensive, most-likely-to-fail fetch is the later one. Second, the process
  one: **a log line is evidence of what happened, not of where the code lives.** Both wrong claims
  above came from reading CI output and inferring repository structure from it, without opening the
  file. Where a fix belongs is a question only the source can answer.
- **Not fixed in this PR, on purpose**: `.github/actions/setup-rust/action.yml` is CI infrastructure
  unrelated to this plan's governance changeset. Patching it inside a governance PR would scope-creep
  the PR, and — given the shape divergence recorded above — a same-text patch would not even have
  applied cleanly across the three repos.
- **Terminal state**: filed as
  [`plans/ideas/ci-setup-rust-toolchain-retry.md`](../../ideas/q2-not-urgent-important/ci-setup-rust-toolchain-retry.md) — a
  retry around the toolchain install in all three repos' `setup-rust`, which the brief records as a
  **reconciliation** rather than a copy, since the three do not share an implementation. It also
  carries the open question of where the retry belongs (in our action, or one layer down in the
  third-party action it delegates to), because the corrected reading above means that is genuinely
  not yet known. This is a code/CI change, so per the Knowledge Capture routing matrix it must become
  its own plan and may **never** land inline in this one; the two-pager is the first stage of that
  route.

## Learning: rewriting a sentence for one reason silently dropped an unrelated conjunct — from the one copy declared normative

- **Context**: PR-review cycle 3 on `ose-infra` PR #16, finding 1 (HIGH, confidence 95).
- **Observation**: the C5 hunk rewrote `<GATE>`'s precondition (a) to carry the floor→ceiling
  reversal. In the course of that rewrite it also **deleted the `and the review loop did not exit
\`escalated\``conjunct**, which has nothing to do with the reversal. Six other surfaces in the very
  same PR kept the conjunct (`<MERGE>` twice, `<PLANS>`,`plan-quality-gate.md`,
  `development/workflow/README.md`,`AGENTS.md`), and`ose-primer` kept it too — so exactly one copy
  lost it. That copy is the one `<MERGE>` designates as **normative**, with the explicit instruction
  "Do not substitute the shorter list that used to live here". `<MERGE>` also spells out the exact
  failure this enables: _"Without this clause the loop exits `done` and an `[AI]` merge proceeds on
  the strength of one side of an unsettled argument."_
- **Why it might generalize**: the loss is invisible to every check anyone would think to run. A
  before/after grep for the **new** wording passes; a grep for the **removed** floor wording passes;
  a link check passes; markdown lint passes. Nothing compares the rest of the sentence. And the
  redundancy that normally saves you — six sibling copies — actively hurt here, because the majority
  stayed right while the authoritative minority went wrong, so a "do these agree?" spot-check on any
  two of the six would have looked fine. The rule: when an edit rewrites a sentence that carries
  **more than one** independent clause, diff the sentence for what was _removed_, not only for what
  was _added_ — and check the normative copy first, since a defect there outranks agreement among
  derivatives.
- **Cycle-2's own fix was half-applied for a related reason** (cycle 3, finding 2, HIGH): the fixer
  changed a worked example's comment line from `main-to-origin-main` to `worktree-to-origin-main` and
  left the two commands under it — `git push origin main`, no `git worktree add` — untouched. The
  label and the body of the same five-line block then contradicted each other. Same shape: the edit
  addressed the string that was cited and not the unit of meaning that contained it.
- **Terminal state**: filed as
  [`plans/ideas/class-sweep-completeness.md`](../../ideas/q2-not-urgent-important/class-sweep-completeness.md) — the third of
  that brief's three instances, and the one that states the unit-of-edit rule most directly: the
  fixer must re-read the **whole enclosing block** it edits (example, list item, precondition, table
  row) and confirm every part still agrees, rather than verifying only that the cited substring
  changed.

## Learning: the terminal reconcile's own acceptance command reports a false clean when run before fetching

- **Context**: Phase 5's terminal reconcile in `ose-infra`, immediately after PR #16 merged.
- **Observation**: `git rev-list --left-right --count origin/main...main` compares two **local**
  refs — `main` and `refs/remotes/origin/main` — and performs no network access. Run before any
  fetch, both were equally stale and it printed **`0 0`**. After `git fetch origin` it printed
  **`1 0`**, the true state. After `git fetch origin main:main` it printed **`0 0`** again, this time
  meaning it. The first and last readings are byte-identical and only one of them means what it
  appears to mean.
- **Why it might generalize**: `<C1>`'s numbered method puts the fetch inside step 8's reconcile
  command, but its acceptance count is stated separately, so a reader who checks the count first —
  the natural thing to do when verifying whether the step is even needed — gets a pass that certifies
  nothing. This is the same vacuous-clause shape recorded elsewhere in this file, reached from a
  different direction: not a clause that can never fail, but a clause whose _timing_ determines
  whether it can fail at all.
- **Terminal state**: **routed** to `<C1>` via the `<C1>` Correction Propagation Sub-Cycle — new
  §"Measure after fetching, never before", carrying the three-reading transcript above as the worked
  example. Landed in `ose-public` PR
  [#81](https://github.com/wahidyankf/ose-public/pull/81); propagated to both siblings by the same
  sub-cycle and **landed there too** — `ose-primer` PR
  [#15](https://github.com/wahidyankf/ose-primer/pull/15) (merged `cedabb2f1`) and `ose-infra` PR
  [#17](https://github.com/wahidyankf/ose-infra/pull/17) (merged `1d64990bb`). All three copies of
  `<C1>` are byte-identical at sha1 `618e74ff8ebc5c0a0abf19b2a40c2af9ac2e01db`, verified by `diff`
  against each sibling's `origin/main` blob after fetching.

## Learning: `ose-public` is now behind both siblings on a document it is the source of truth for

- **Context**: building Phase 5's three-repo agreement table, diffing `<SDLC>`
  (`docs/reference/sdlc-gate-standard.md`) across all three repos.
- **Observation**: two name-bound claims in `ose-public`'s copy are wrong, and both siblings have
  already replaced them. Its §Worktree-Agnostic Execution paragraph says "`ose-infra` is a bare repo
  … so worktree-agnostic execution is a hard requirement **there**", which was true when written and
  is now stale because `ose-primer` is bare too. Its evidence table claims the guardrails were
  "verified from **both the primary checkout and** a linked worktree in all 3" — not merely stale but
  **impossible**, since two of the three repos have no primary checkout to verify from. `ose-primer`
  and `ose-infra` are byte-identical to each other on this file and carry a property-bound
  replacement that also tells the reader to re-verify rather than trust the sentence.
- **Why it might generalize**: DD-8 makes `ose-public` the source of truth, and it is easy to read
  that as "`ose-public` is never the lagging repo". It is a rule about **direction of propagation**,
  not about correctness: a sibling that fixes something locally leaves the source of truth behind,
  and nothing in the parity loop detects that asymmetry. This is the third distinct instance in this
  plan of a sibling being ahead — the pattern is now well-evidenced enough to stop being a surprise.
- **Terminal state**: filed as `plans/ideas/sdlc-gate-standard-property-bound-lag.md` — deliberately
  **not** fixed from Phase 5, because correcting `ose-public` from inside the `ose-infra` propagation
  would invert DD-8's direction and land an unreviewed edit in a repo that phase was not delivering
  to.

## Learning: a filter turned an unrunnable command into a clean pass, discharging a precondition it could not have checked

- **Context**: the Phase 6 `ose-primer` propagation was briefed with a worktree-removal precondition
  phrased as "`git stash list` is empty". `ose-primer` is bare.
- **Observation**: raw `git stash list` in a bare repo answers
  `fatal: this operation must be run in a work tree` and exits non-zero — the command cannot run
  there at all. Through this repo's RTK filter, the same invocation prints `No stashes` and exits
  `0`. Ten stashes actually exist: `git rev-list --walk-reflogs --count refs/stash` → `10`. Both
  readings were reproduced directly rather than taken on the executing agent's word. The agent
  reported this as a gap in `<C1>`; it is not — `grep -rn "stash list" repo-governance/ .claude/`
  returns nothing, so no governance surface has ever stated this precondition. It existed only in an
  orchestrator's briefing text.
- **Why it might generalize**: this is the `grep`-is-ugrep `-L` false-zero again in a different
  wrapper. A filtering layer sits between the clause and the binary, and when the binary fails the
  filter can substitute a plausible, well-formed, wrong answer — the one that happens to discharge
  the check. Nothing about the output looks degraded. Two further facts make the stash version worse
  in a bare repo specifically: `refs/stash` is repo-level rather than per-worktree, so stash
  emptiness is not a statement about any one worktree even where it is readable; and `ose-primer`
  carries ten pre-existing foreign stashes that a "clean up before removing" reading might have
  invited an agent to touch.
- **Terminal state**: **folded into an existing brief** — `plans/ideas/acceptance-clause-vacuity.md`
  gains this as its fifth instance plus a "confirm the named command can run where it is pointed,
  unfiltered" direction, per the ideas folder's integrate-don't-duplicate rule. Deliberately **not**
  routed to `<C1>`: `<C1>` never made this claim, so there is nothing
  there to correct, and opening a third three-repo propagation round for
  a defect no governance surface contains would be cost without a target.
