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
- **Terminal state**: pending — triage at Phase 6. Candidate route: a worked example inside `C1`
  showing the non-zero reading and the `git fetch origin main:main` recovery.

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
- **Terminal state**: pending — triage at Phase 6. Candidate route:
  `repo-governance/workflows/plan/plan-quality-gate.md`, as a constraint on how iterations are
  briefed rather than a change to the exit condition itself.

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
- **Terminal state**: pending — triage at Phase 6. Candidate routes:
  `repo-governance/development/agents/subagent-orchestration.md` (match the tool grant to the
  acceptance clauses when briefing) and `repo-governance/development/pattern/maker-checker-fixer.md`
  (a disclosed substitution is not a discharged check).

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
- **Terminal state**: pending — triage at Phase 6. Candidate route: before Phase 4 executes, add
  `<GATE>` to the C5-propagation steps (Phase 4 and Phase 5) and to the "remaining five files agree"
  step (which becomes six), mirroring how `<MERGE>` is already handled — this is a correction to
  Phase 4/5's own step list, not yet executed, so it can land as an ordinary edit rather than a
  reopened-and-corrected retrospective note.

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
- **Terminal state**: pending — triage at Phase 6. Candidate route: `plan-multi-repo-parity-planning`
  should require a propagation phase to derive its file list from the source PR's actual diff
  (`git show --stat <merge-sha>`), minus explicitly-excluded paths, rather than from the plan's
  change-ID table.

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
- **Terminal state**: pending — triage at Phase 6. Candidate routes: (1) this plan's Phase 5 step
  for `ose-infra` carries the identical premise and must be re-checked live rather than trusted;
  (2) `plan-multi-repo-parity-planning` — a "verified absent in sibling" claim needs an
  if-present branch, never a bare do-nothing.

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
- **Terminal state**: pending — triage at Phase 6. Candidate route: `plan-multi-repo-parity-planning`
  — propagation acceptance criteria should assert the **post** state only, or measure the sibling's
  pre-state at execution time rather than inheriting the source repo's.

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
- **Terminal state**: pending — triage at Phase 6. Candidate route: rewrite Phase 5's C1 copy step
  and both phases' gate diffs to use `git -C <PUBLIC> show origin/main:<C1>` rather than
  `<PUBLIC>/<C1>`; the same correction belongs in `<C1>` itself wherever it tells a reader to read a
  file from a sibling checkout.

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
- **Terminal state**: pending — triage at Phase 6, but actionable immediately at Phase 5: before
  executing Phase 5 against `ose-infra`, add
  `repo-governance/development/workflow/trunk-based-development.md` and
  `.claude/skills/repo-practicing-trunk-based-development/SKILL.md` to Phase 5's file-agreement/sweep
  steps, applying the same property-bound bareness carve-out to every mode-selection or
  mode-availability statement in both files (not just the sites `ose-primer`'s cycle 2 happened to
  cite), mirroring the sweep `ose-primer` PR #14 cycle 3 performed.

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
- **Terminal state**: pending — triage at Phase 6. **Not fixed here, deliberately**: the same
  archived file exists in `ose-public` (confirmed on its `origin/main`), so this is a cross-repo
  condition and patching only `ose-primer` would manufacture exactly the divergence DD-10 and the
  parity workflow exist to prevent. The class is already tracked in `ose-public` as
  `plans/ideas/ayokoding-mermaid-diagram-remediation.md` ("636 mermaid violations exposed by the
  `detect_kind` fix"). Candidate routes: (1) attach this `plans/done/` instance to that brief;
  (2) widen this plan's own local mermaid gate beyond `repo-governance docs`, or record its scope
  limit explicitly, before Phase 5 runs the same gate against `ose-infra`.

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
- **Terminal state**: pending — triage at Phase 6, and a genuine `<C1>` defect, so it routes through
  the `<C1>` Correction Propagation Sub-Cycle (`ose-public` first, never an in-place sibling edit).
  **Resolved this phase** by deleting the merged ref through the GitHub API
  (`gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<branch>`) — the identical path
  `gh pr merge --delete-branch` takes natively, so no hook was bypassed and no `--no-verify` was
  used; the content had already merged through a fully-gated PR. Candidate `<C1>` fix: state that in
  a bare repo, remote-branch cleanup either happens **before** the worktree is removed (from inside
  it) or through the API path, and say plainly that `--no-verify` is **not** the sanctioned answer.

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
- **Terminal state**: pending — triage at Phase 6. Candidate route: `plan-multi-repo-parity-planning`
  should require propagation steps to assert **post** state only, derive their file list from the
  source PR's actual diff, and carry an explicit if-present branch for every "verified absent" claim.

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
- **Terminal state**: pending — triage at Phase 6. Candidate route: a general rule in
  `repo-governance/development/pattern/maker-checker-fixer.md` or the plan conventions — when a
  change restricts a declared enum, enumerate the maker/producer surfaces explicitly, since the
  checker may be structurally unable to carry the restriction.
