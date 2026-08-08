# Delivery Checklist — Optimize CIs

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.

## Worktree

Worktree path: `worktrees/optimize-cis/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree optimize-cis
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and — capped at one per
repository per plan and reused across every delivery unit landed there — is removed immediately once
the plan is done using this repo, not deferred to archival.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Mandatory in `ose-public` — `main` is branch-protected including for admins, so no direct-push mode
has an executable path here. Exactly one PR per repo (three total) stays open across every phase
that touches it and runs the
[PR-Review Maker→Fixer Cycle](../../../repo-governance/workflows/pr/pr-review-quality-gate.md),
run under this plan's explicit, maintainer-authorized deviation from that workflow's standing
fixed-3-cycle/escalate default — **iteratively until clean, capped at 10 cycles** — before merge;
see §Delivery Boundaries for the deviation's exact terms. `[AI]` merges once the five hardened
preconditions hold.

## Autonomy Contract — this plan runs unattended

**Every one of this plan's steps is `[AI]`. There is no `[HUMAN]` or `[AI+HUMAN]` step.** Maintainer
authorization for that was given on 2026-08-08, and the conditions that make it safe are structural,
not conventional:

| Would normally need a human          | Why it does not here                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Merging PRs                          | `ose-public` `main` requires **0 approving reviews** and exactly one status check, `Quality gate` `[Repo-grounded]`. `[AI]` merges once the five hardened preconditions hold and the review cycle has run to clean or to its 10-cycle cap, under this plan's explicit deviation from the governance workflow's standing fixed-3-cycle/escalate default (§Delivery Boundaries) — and authors no `[HUMAN]` merge gate. |
| Deleting 9.32 GB of scratch          | Restructured as quarantine-then-verify: candidates are `mv`d aside, proven non-load-bearing by `doctor --fix` + `test:quick` + `nx affected -t build`, and only then deleted. Reversible until the final `rm`.                                                                                                                                                                                                       |
| Pruning rustup toolchains            | Fully re-fetchable; the acceptance criterion re-runs `doctor --fix` and `test:quick` to prove restoration.                                                                                                                                                                                                                                                                                                           |
| Deleting the superseded backlog plan | Recoverable from git history; maintainer authorized it explicitly on 2026-08-08.                                                                                                                                                                                                                                                                                                                                     |
| Changing repo settings               | **Never done.** The plan instead treats each repo's required status-check context as a fixed external contract and asserts the emitting job keeps its exact name.                                                                                                                                                                                                                                                    |

**The two hard stops that are not human gates but must halt execution:**

1. A phase gate fails — fix the root cause, never bypass, never proceed.
2. The protected `Quality gate` context stops reporting on a PR — revert the workflow change and
   re-verify before merging. Merging a PR whose required context never reported is forbidden.

A PR's review cycle exhausting its 10-cycle cap is explicitly **not** a hard stop — see §Delivery
Boundaries: merge proceeds regardless of what remains open, recorded rather than silently dropped.

**One thing an agent must never do in this plan**: modify branch protection or any repository setting
to make a merge possible. If merging is blocked, the change is wrong — not the setting.

## Delivery Boundaries

**PR budget: 3 total — exactly one per repo.** `ose-public` opens a single draft PR right after
Phase 1's gate passes and keeps it open through Phase 12; `ose-primer` and `ose-private` each open
their own single PR inside Phase 10. **Phase 0 opens no PR.** No phase opens a second PR in a repo
that already has one open — if a phase is about to open one, stop: that means this section drifted,
not that a new PR is warranted.

**This plan authors an explicit, maintainer-authorized deviation from the
[Plans Organization Convention §PRs Open at Delivery Boundaries](../../../repo-governance/conventions/structure/plans.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule)
HARD RULE**, whose standing shape is one branch → one PR → one delivery unit, opened and merged at
that unit's own boundary, never held open across later units merely to batch them. This plan does
not change that convention, and no other plan inherits the deviation below.

`ose-public`'s work below is still organized into four delivery units (the table's `Unit` column),
each an independently shippable increment. What changes is PR _cardinality_, not unit structure:
instead of four branches/PRs (one opened and merged per unit), all four units land on the same
single PR, opened once after Phase 1 and merged once at plan close. This was considered and chosen
over the convention's default because several phase gates need a **live** PR to check CI/status
against (Phase 6 Gate's `gh pr checks`, Phase 7 Gate's completed-run counts, Phase 8 Gate's
scratch-commit-turns-red check, Phase 10 Gate's "CI green in all three repos") — a boundary model
that only opens the PR at the _end_ of the unit containing those phases cannot satisfy its own
gates, since `pr-quality-gate.yml` only triggers on an open PR or a push to `main` (forbidden here).
Opening one PR early and pushing to it at the end of every phase gate below gives every gate a live
target throughout, and reviewing the whole diff once — iteratively until clean, not at a fixed count,
so nothing is lost by not compartmentalizing the diff — costs less than four narrower PRs plus
resolving the timing contradiction some other way. Maintainer authorization for this deviation was
given 2026-08-08.

| Unit                      | Phases | What it contains                                                                                        |
| ------------------------- | -----: | ------------------------------------------------------------------------------------------------------- |
| **plan + invocation tax** |    1–4 | Local gate speedup: hooks and `lint-staged` work end-to-end with no CI change                           |
| **CI topology**           |    5–7 | Grouped CI: the registry field, the build-once artifact, and the setup slimming land together           |
| **build and disk**        |    8–9 | `test:quick` recomposition and disk hygiene, independent of CI topology                                 |
| **propagation and close** |  10–12 | Cross-repo parity, measurement rollup, Knowledge Capture, and archival — all pushed to the same open PR |

**This plan authors an explicit, maintainer-authorized deviation from the standing
[PR-Review Maker→Fixer Cycle](../../../repo-governance/workflows/pr/pr-review-quality-gate.md)
default for the three PRs it opens.** The governance workflow's standing behavior is a **fixed
3-cycle** loop with no early exit, that **escalates rather than merges** when cycles exhaust with
unresolved findings — `output.final-status: escalated`, and the caller "MUST NOT proceed to the
merge." This plan does not change that workflow, and no other plan or PR in this repo inherits the
deviation below. For this plan's three PRs only, maintainer authorization given 2026-08-08
overrides two parameters:

1. **Iterate until clean, not a fixed 3 cycles.** After each cycle, `pr-review-synthesis-maker`'s
   consolidated review is re-run; if it reports any CRITICAL/HIGH/MEDIUM finding, run another
   fixer pass and repeat. LOW findings never block.
2. **Cap at 10 cycles, then merge unconditionally regardless of what remains open, at any
   severity** — record any still-open finding as accepted-with-reason in the PR description, the
   same accepted-as-is pattern Phase 11 already uses for a missed metric target, and merge. The
   cap is chosen so a clean review is expected well before it binds, not so it is expected to bind
   routinely; reaching it is not a hard stop (Autonomy Contract, above), unlike the governance
   workflow's own exhaustion behavior.

## Parallelization Model

`1 main thread + N background agents`, **N=3**. Dependency DAG:

```text
Phase 0 ──> Phase 1 ──> Phase 2 ──> Phase 3 ─┐
                              └──> Phase 4 ──┼──> Phase 5 ──> Phase 6 ──> Phase 7 ─┐
                                              │                                     │
                                              └──> Phase 8 ──> Phase 9 ─────────────┼──> Phase 10 ──> Phase 11 ──> Phase 12
                                                                                    │
                                                                                    ┘
```

Phases 3 and 4 are independent of each other and may fan out. Phases 8–9 are independent of 5–7 and
may fan out. Phase 10 requires every source change to be final.

## Progress Scoreboard

`plans/in-progress/optimize-cis/scoreboard.md` is an **append-only** ledger, not a single before/after
snapshot. Every phase gate step that (re-)measures a metric appends one row — no row is ever edited
or removed — so a regression is visible at the phase that introduced it, not only at the final rollup.

Row shape: `| Phase | Metric | Value | Δ vs Phase 0 baseline | Δ vs previous row for this metric | vs Target | Status |`.
`Status` is one of `BASELINE` (Phase 0's first row per metric), `IMPROVED`, `REGRESSED`, `UNCHANGED`,
or `PASS`/`FAIL` (only at Phase 11's final row, against the committed target). A `REGRESSED` row is
not itself a failure — cumulative progress toward the target is what phase gates enforce — but it
must never pass unremarked: the step appending it also states the suspected cause inline.

Phase 0 initializes the file with one `BASELINE` row per metric (M1–M9). Every subsequent
measurement step already present in this checklist (Phase 2/3 → M1, Phase 7 → M3/M4/M7, Phase 8 →
M2/M6, Phase 9 → M8 partial, Phase 10 → M3/M8 full/M9, Phase 11 → final PASS/FAIL) appends its row to
this same file instead of only recording into `baseline/measurements.md` or `results.md`. Phase 6
verifies M5 inline against the Phase 0 capture but appends no scoreboard row — M5 is a
byte-identical-or-fail gate check, not a trending measurement. `results.md`
(Phase 11) becomes a rendered summary **derived from** the scoreboard's last row per metric, not an
independent measurement pass.

---

## Phase 0 — Baseline and capture

**Opens no PR.** Everything here is measurement; nothing is changed.

- [x] [AI] Sync the worktree: `git -C . fetch origin && git rebase origin/main` — acceptance: `git status` reports the branch up to date with no conflicts.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: none. **Notes**: worktree already reset to origin/main by orchestrator prior to Phase 0; verified clean and current.
- [x] [AI] Initialize the toolchain from the repo root (not this worktree): `npm install && npm run doctor -- --fix` — acceptance: both commands exit 0.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: none. **Notes**: both exited 0. Preexisting, unrelated npm/Volta PATH drift noted (v11.16.0 active vs v11.11.0 pinned) — warning only, not blocking, out of scope for this plan.
- [x] [AI] Create `plans/in-progress/optimize-cis/learnings.md` if absent, containing the H1 `# Learnings: optimize-cis` — acceptance: `test -f plans/in-progress/optimize-cis/learnings.md` succeeds and `npx markdownlint-cli2 plans/in-progress/optimize-cis/learnings.md` exits 0.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: none. **Notes**: file already existed from plan authoring with H1 header and 2 entries; verified `test -f` and markdownlint pass, no overwrite needed.
- [x] [AI] Capture the executed gate id set for every surface into `plans/in-progress/optimize-cis/baseline/gates-<surface>.txt` for each of `pre-commit`, `pre-push`, `commit-msg`, `ci`, using `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate list --surface=<surface> --format=json` — acceptance: four non-empty files exist; the `ci` file contains at least 36 gate ids.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: added `baseline/gates-{pre-commit,pre-push,commit-msg,ci}.txt`. **Notes**: counts — pre-commit 28, pre-push 11, commit-msg 1, ci 36. Meets the ≥36 acceptance exactly.
  - _This capture is the ground truth for M5/AC-4. Every later phase gate diffs against it._
- [x] [AI] Capture the `rhino-cli` test-name list into `baseline/test-names.txt` via `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib -- --list` — acceptance: file is non-empty and contains one line per test.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: added `baseline/test-names.txt`. **Notes**: non-empty, one test per line, matches the ~754 unit-test count referenced elsewhere in the plan.
- [x] [AI] Measure and record M1 baseline (pre-commit, 10 md files) into `baseline/measurements.md`, using a `bash` loop-and-divide harness — acceptance: a recorded ms figure with the run count stated.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: added `baseline/measurements.md` (M1 section). **Notes**: mean 3,898 ms over N=3 runs (4,315/3,791/3,589 ms) via `bash`, `npx lint-staged --no-stash`. Staged files fully reverted after measurement (`git checkout HEAD --`), net-zero diff confirmed.
  - _Harness constraint: measure under `bash`, never `zsh` (unquoted vars do not word-split), and never with `python3` timestamp subprocesses. See `tech-docs.md` §Method note._
- [x] [AI] Measure and record M2 baseline: `bash -c 'time npx nx run rhino-cli:test:quick --skip-nx-cache'` — acceptance: wall time recorded in `baseline/measurements.md`.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `baseline/measurements.md` (M2 section). **Notes**: 124.3 s wall (2m4.299s; user 2m40.893s, sys 0m35.709s), all 5 subtargets passed.
- [x] [AI] Measure and record M6 baseline: `du -sk` of an isolated `CARGO_TARGET_DIR` after one `test:quick` — acceptance: size in MB recorded.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `baseline/measurements.md` (M6 section). **Notes**: 2,747 MiB (2.75 GiB) after cold `test:quick`.
- [x] [AI] Record M3 and M4 baselines from run history: `gh run list -R wahidyankf/ose-public -L 50 --json databaseId,workflowName,status,conclusion,createdAt,startedAt,updatedAt` plus per-run job durations — acceptance: median runner-seconds and p50 wall-clock recorded for `pr-quality-gate`.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `baseline/measurements.md` (M3/M4 sections). **Notes**: median of 18 completed `pr-quality-gate` runs — M3 = 7,103.5 runner-s, M4 = 974.5 s p50 wall-clock. Both differ from the illustrative brd.md authoring-time figures (10,945 s / from-run-history) since CI state naturally drifts between authoring and execution; this fresh capture is the authoritative Phase 0 baseline that later phases diff against.
- [x] [AI] Record each repo's branch-protection **required status check contexts** into `baseline/required-checks.md`: `gh api repos/wahidyankf/<repo>/branches/main/protection --jq '.required_status_checks.contexts'` for `ose-public`, `ose-primer`, `ose-private` — acceptance: the file records, per repo, the exact context strings (`ose-public` is known to require exactly `Quality gate` `[Repo-grounded]`) or an explicit "no protection payload readable" note.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: added `baseline/required-checks.md`. **Notes**: `ose-public` confirmed `["Quality gate"]`. `ose-primer`: branch-protection API 404s — `main` is protected via a repository **ruleset** instead (PR/linear-history/no-deletion rules, no `required_status_checks` rule type), i.e. no GitHub-required CI context currently gates merges there — recorded verbatim, flagged for Phase 6/10 attention since those phases assume a required CI context. `ose-private`: both protection and ruleset APIs return 403 (private repo, needs GitHub Pro) — recorded as "no protection payload readable" per the acceptance criterion's explicit escape hatch.
  - _**Load-bearing.** A required context is satisfied only by a job reporting under that exact name. Phase 6 rewrites the workflow that emits it; if the name drifts, every PR in that repo becomes permanently unmergeable and only a repo-settings change — which an agent must not make — can undo it._
- [x] [AI] Record M7 baseline: `gh api repos/wahidyankf/ose-public/actions/caches --jq '[.actions_caches[].size_in_bytes] | add'` — acceptance: byte total and percentage of the 10 GiB ceiling recorded.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `baseline/measurements.md` (M7 section). **Notes**: 8,280,363,514 bytes = 7.71 GiB = 77.12% of 10 GiB ceiling. Differs from brd.md's illustrative 98.0% (natural cache-state drift since authoring) — this fresh capture is the authoritative Phase 0 baseline.
- [x] [AI] Record M8 baseline: `du -sk` over each bucket listed in `tech-docs.md` §D.1 — acceptance: per-bucket table recorded.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `baseline/measurements.md` (M8 section). **Notes**: 26.64 GiB total across the 5 §D.1 buckets — matches the 2026-08-08 tech-docs snapshot on 4 of 5 buckets exactly; `~/.cache/ose-cargo-target/` grew 1.97→4.29 GiB from this Phase 0's own M2/M6 measurement runs (expected side effect, not a defect).
- [x] [AI] Record M9 baseline into `baseline/rust-versions.md`: every `rust-toolchain.toml` `channel` and every `Cargo.toml` `rust-version` across `.` (`ose-public`), `/Users/wkf/ose-projects/ose-primer`, `/Users/wkf/ose-projects/ose-private`, and `/Users/wkf/ose-projects/beaver-nest`, plus `rustup toolchain list` — acceptance: the file reproduces the DD-9 evidence table and records 3 distinct declared values. `beaver-nest` is already `channel = "1.95.0"` at both its `rust-toolchain.toml` sites `[Repo-grounded]` — the capture should show it matching, not diverging.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: added `baseline/rust-versions.md`. **Notes**: confirmed 3 distinct declared values — `channel` 1.95.0×9/`stable`×2 (`crud-be-rust-axum`, `coralpolyp-be`); `rust-version` 1.88×9/1.94.0×1; `doctor` validates against the floor not the channel. `beaver-nest` confirmed matching expectation (1.95.0 at both sites, no divergence). `rustup toolchain list` shows all 6 toolchains, matching DD-9 evidence.
- [x] [AI] Initialize `plans/in-progress/optimize-cis/scoreboard.md` with the `## Progress Scoreboard` header and one `BASELINE` row per metric M1–M9, sourced from the measurements just recorded above — acceptance: nine rows exist, each with a non-empty `Value` and `Status = BASELINE`.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: added `plans/in-progress/optimize-cis/scoreboard.md`. **Notes**: 9 BASELINE rows (M1-M9), one per metric, sourced from `baseline/measurements.md` and `baseline/rust-versions.md`; Δ columns read "—" for the baseline row.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] Verify `baseline/` contains four gate-id captures, a test-name list, `measurements.md` with M1–M8 baselines, and `rust-versions.md` with the M9 baseline — acceptance: `ls plans/in-progress/optimize-cis/baseline/` lists all seven artifacts.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: none (verification only). **Notes**: `ls` confirms all 7 named artifacts plus `required-checks.md` (8th, from item 10) present.
- [x] [AI] Verify `scoreboard.md` carries nine `BASELINE` rows, one per metric — acceptance: `grep -c '| BASELINE |' plans/in-progress/optimize-cis/scoreboard.md` returns 9.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: none (verification only). **Notes**: grep returns exactly 9.
- [x] [AI] Verify the working tree is otherwise clean: `git status --porcelain` shows only the new plan and baseline files — acceptance: no unexplained modified file appears.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: none (verification only). **Notes**: `git status --porcelain` shows only `delivery.md` (self-modified by this ritual), `baseline/`, and `scoreboard.md` — no unexplained file.

> **Pause Safety**: nothing has changed; only measurements were recorded. Safe to stop. To resume: re-read `plans/in-progress/optimize-cis/baseline/measurements.md`.

---

## Phase 1 — Supersede the backlog plan and index this one

- [x] [AI] Delete the superseded plan: `git rm -r plans/backlog/rhino-cli-optimization/` — acceptance: the directory no longer exists and `git status` shows the deletions staged.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: deleted `plans/backlog/rhino-cli-optimization/{README,brd,prd,tech-docs,delivery,learnings}.md` (6 files). **Notes**: `git rm -r` staged all 6 deletions.
  - _Decision recorded during pre-write grilling on 2026-08-08: delete outright, do not archive. Its contents were reviewed before this decision._
- [x] [AI] Remove the entry at `plans/backlog/README.md:101` referencing `rhino-cli-optimization` — acceptance: `grep -c "rhino-cli-optimization" plans/backlog/README.md` returns 0.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `plans/backlog/README.md`. **Notes**: removed the full "Toolchain" subsection (bold header + list entry, lines 99-116) since it contained only this one now-deleted plan; `grep -c` confirms 0.
- [x] [AI] Confirm this plan is indexed in `plans/in-progress/README.md` under `## Active Plans` (added at plan-authoring time) — acceptance: `grep -c "optimize-cis" plans/in-progress/README.md` returns at least 1.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: none (verification only). **Notes**: entry already landed with the docs-only PR (#161); grep returns 1.
- [x] [AI] Verify no other file references the deleted plan: `grep -rn "rhino-cli-optimization" --exclude-dir=node_modules --exclude-dir=target --exclude-dir=.git --exclude-dir=local-temp .` — acceptance: returns no hits outside `plans/done/` historical records.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `plans/backlog/beaver-nest-repo-consolidation/{README.md,delivery.md}`, `plans/ideas/q2-not-urgent-important/rhino-cli-sync-validator-wrong-model-drift.md`. **Notes**: found 2 real dangling references beyond this plan's own docs and `plans/in-progress/README.md`'s expected historical mention. (1) `beaver-nest-repo-consolidation` had a live hard `blockedBy` on `rhino-cli-optimization` with substantive hand-off content — redirected to `optimize-cis` after confirming (via grep of this plan's own tech-docs/delivery) it covers the same concerns (resolver shim, `gate_specs.rs`, repo-wide invocation-form sweep) and corrected a stale claim about 2-repo vs 3-repo parity scope to match `optimize-cis`'s actual Phase 10 design (3-repo continuous enforcement). (2) The idea brief's "nx affected rhino-cli-detection gap" cross-reference pointed at `rhino-cli-optimization` Axis A Phase 4 — verified `optimize-cis` does NOT carry this specific concern (no such workstream in its brd.md/tech-docs.md) — corrected to state it is now untracked and needs re-filing, rather than falsely claim coverage. Remaining `grep` hits are all backtick-quoted historical/self-referential prose, not markdown links — `md links validate` (next gate item) confirms no broken links.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `npx markdownlint-cli2 plans/**/*.md` — acceptance: exits 0.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: none (verification only). **Notes**: 178 files linted, 0 errors.
- [x] [AI] `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate` — acceptance: exits 0, proving no dangling link to the deleted plan.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: none (verification only). **Notes**: "All links valid! No broken links found." — confirms the beaver-nest-repo-consolidation and idea-brief link redirects resolve.

> **Pause Safety**: the plan set is coherent — one active plan, no superseded duplicate, no dangling links. Safe to stop. To resume: `npx markdownlint-cli2 plans/**/*.md`.

---

### Open the `ose-public` PR

> This is the plan's **only** `ose-public` PR-open event. Every phase from here through Phase 12
> pushes into this same branch; see §Delivery Boundaries for why it opens this early.

- [x] [AI] Commit Phase 1's changes thematically and push a new branch; open a draft PR against `main` titled `perf(gates): optimize pre-commit, pre-push, and PR quality gate` — acceptance: the PR exists and its number is recorded in `baseline/pr-numbers.md` under `ose-public`.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: 3 commits (Phase 0 baseline, Phase 1 supersession, delivery.md progress ticks); added `baseline/pr-numbers.md`. **Notes**: pushed `worktree/optimize-cis` branch, opened draft PR #162 against `main`. Recorded in `baseline/pr-numbers.md`.

---

## Phase 2 — Resolver shim replaces `cargo run` (DD-1)

- [x] [AI] Add the scenario below to `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-emission.feature` (sibling scenarios already cover emitter behaviour) — acceptance: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs gherkin-cardinality validate specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-emission.feature` exits 0.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-emission.feature`. **Notes**: appended as 4th scenario, after "Generated lint-staged commands may use a declared shell wrapper"; gherkin-cardinality validate exits 0.
  - _Suggested executor: `specs-maker`_
- [x] [AI] **RED**: Write a failing test in the `apps/rhino-cli/src/commands/gate/emit.rs` tests module binding the scenario below
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::emit`
      — acceptance: test fails, reporting the rendered string still contains `cargo run --release`.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `apps/rhino-cli/src/commands/gate/emit.rs`. **Notes**: added `rhino_cli_kind_renders_a_resolver_shim_invocation`; failed for the right reason (assertion mismatch: rendered `"cargo run --release --quiet ..."` instead of the shim), not a compile error. 7 preexisting `gate::emit` tests still passed.
  - **Gherkin (binds) →** "Rhino CLI kind renders a resolver shim invocation"

    ```gherkin
    Scenario: Rhino CLI kind renders a resolver shim invocation
      Given the registry declares a gate of kind "rhino-cli" on surface "pre-commit"
      When "rhino-cli gate emit --surface=pre-commit" runs
      Then the generated command invokes the resolver shim at "apps/rhino-cli/scripts/rhino-bin.sh"
      And the generated command contains no "cargo run" substring
    ```

  - _Suggested executor: `swe-rust-dev`_

- [x] [AI] **GREEN**: Change `command_with_fixed_arguments` in `apps/rhino-cli/src/commands/gate/emit.rs` (lines 122–125) so `GateKind::RhinoCli` renders `apps/rhino-cli/scripts/rhino-bin.sh <command>`
      — command: same as above
      — acceptance: test passes and no other `gate::emit` test breaks.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `apps/rhino-cli/src/commands/gate/emit.rs`. **Notes**: all 8 `gate::emit` tests pass (7 preexisting + 1 new). Updated 2 preexisting tests' stale expected strings (deliberately-replaced old rendering, not weakened): `command_with_fixed_arguments_invokes_rhino_cli_through_the_local_manifest` (renamed, new expected shim string) and `lint_staged_shell_overrides_wrap_or_own_the_derived_file_invocation`.
  - _Suggested executor: `swe-rust-dev`_
- [x] [AI] **REFACTOR**: Extract the shim path to a single named constant in `emit.rs` so the three Husky shims and `validate.rs` share one definition
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib`
      — acceptance: all lib tests pass; `grep -c "cargo run --release" apps/rhino-cli/src/commands/gate/emit.rs` returns 0.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: `apps/rhino-cli/src/commands/gate/emit.rs`. **Notes**: added `pub(crate) const RHINO_CLI_RESOLVER_SHIM: &str = "apps/rhino-cli/scripts/rhino-bin.sh"`. `validate.rs` checked — its only `cargo run --release` occurrences are unrelated test fixtures (hand-authored CI YAML strings for its own prefix-tolerant parsing logic), not production rendering, so nothing to repoint there. Full lib suite: 1366 passed, 0 failed, 1 ignored. `grep -c` returns 0.
- [x] [AI] Create `apps/rhino-cli/scripts/rhino-bin.sh` (sibling: `apps/rhino-cli/scripts/deny-check.sh`) resolving in order: `$RHINO_CLI_BIN` if executable; else `apps/rhino-cli/target/release/rhino-cli` if newer than `src/`; else `cargo build --release` then execute. Make it executable with `chmod +x`
      — command: `shellcheck --severity=warning apps/rhino-cli/scripts/rhino-bin.sh && shfmt -d apps/rhino-cli/scripts/rhino-bin.sh`
      — acceptance: both exit 0.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: added `apps/rhino-cli/scripts/rhino-bin.sh` (executable). **Notes**: **corrected a genuine plan-authoring defect** — this item's original text specified `cargo build --profile gate`/`target/gate/rhino-cli`, but `[profile.gate]` isn't added to `Cargo.toml` until Phase 4 (line ~381), which itself has a dedicated step "Point `rhino-bin.sh` ... at `--profile gate`" confirming the intended sequencing. Built against `--release`/`target/release/rhino-cli` instead for now (matches the old `cargo run --release` behavior this replaces); Phase 4 repoints it. shellcheck and shfmt both exit 0. Manually verified end-to-end: shim resolves the prebuilt release binary and faithfully propagates its exit code. Logged as a learnings.md entry (cross-phase forward-reference class of defect).
  - _Suggested executor: `swe-rust-dev`_
- [x] [AI] Create `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-binary-resolution.feature` containing the two scenarios bound below, copied verbatim from `prd.md` AC-7 and AC-8 — acceptance: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs gherkin-cardinality validate specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-binary-resolution.feature` exits 0.
  - **Date**: 2026-08-08. **Status**: Done. **Files Changed**: added `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-binary-resolution.feature` (`@gate @unit` tag, matching `gate-emission.feature`'s convention). **Notes**: both AC-7/AC-8 scenarios verbatim; gherkin-cardinality validate exits 0.
  - _Suggested executor: `specs-maker`_
- [x] [AI] **RED**: Write a failing integration test in `apps/rhino-cli/tests/gate_specs.rs` binding the scenario below
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_specs`
      — acceptance: test fails because the shim does not yet build-and-retry.
  - **Date**: 2026-08-09. **Status**: Done. **Files Changed**: `apps/rhino-cli/tests/gate_specs.rs`. **Notes**: genuinely RED — `GATE_BIN` in `rhino-bin.sh` was hardcoded to `apps/rhino-cli/target/release/rhino-cli`, so `CARGO_TARGET_DIR` sandboxing had no effect on it and tier 2 silently reused the real prebuilt binary instead of exercising tier 3's build path. Confirmed red before any script change.
  - **Gherkin (binds) →** "A swept target directory produces a slow run, not a failure"

    ```gherkin
    Scenario: A swept target directory produces a slow run, not a failure
      Given the rhino-cli binary is absent because the ambient sweeper removed target/
      When a generated gate command runs through the resolver shim
      Then the shim builds the binary and then executes the requested gate
      And the gate reports the same result it would have reported with the binary present
      And a subsequent invocation reuses the built binary without rebuilding
    ```

  - _Suggested executor: `swe-rust-dev`_

- [x] [AI] **GREEN**: Implement the build-and-retry path in `apps/rhino-cli/scripts/rhino-bin.sh`
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_specs`
      — acceptance: the bound scenario passes.
  - **Date**: 2026-08-09. **Status**: Done. **Files Changed**: `apps/rhino-cli/scripts/rhino-bin.sh`. **Notes**: `GATE_BIN` now derives its target dir from `TARGET_DIR="${CARGO_TARGET_DIR:-${REPO_ROOT}/apps/rhino-cli/target}"`, matching plain `cargo build`'s own env precedence (no extra flag needed since `cargo build` already honors `CARGO_TARGET_DIR`). Real production fix, not test-only scaffolding — any caller pinning `CARGO_TARGET_DIR` now gets consistent shim behavior. Bound scenario passes.
- [x] [AI] **RED**: Write a failing integration test in `apps/rhino-cli/tests/gate_specs.rs` binding the scenario below
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_specs`
      — acceptance: test fails because the override is not yet honoured.
  - **Date**: 2026-08-09. **Status**: Done. **Files Changed**: `apps/rhino-cli/tests/gate_specs.rs`. **Notes**: already GREEN on first run — tier 1's `RHINO_CLI_BIN` short-circuit was already correctly implemented from the initial shim authoring. "No cargo build" proven deterministically by stripping cargo's directory from `PATH` for the invocation (resolved via cargo's own `CARGO` env var): if the shim had fallen through to tier 3 the test would fail with "command not found" instead of succeeding. No script change needed — honestly reported as already-satisfied rather than inventing busywork.
  - **Gherkin (binds) →** "RHINO_CLI_BIN takes precedence over discovery"

    ```gherkin
    Scenario: RHINO_CLI_BIN takes precedence over discovery
      Given the environment variable RHINO_CLI_BIN points at an executable rhino-cli binary
      When a generated gate command runs through the resolver shim
      Then the shim executes the binary at that path
      And it performs no cargo build
    ```

  - _Suggested executor: `swe-rust-dev`_

- [x] [AI] **GREEN**: Implement the `RHINO_CLI_BIN` override path in `apps/rhino-cli/scripts/rhino-bin.sh`
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_specs`
      — acceptance: the bound scenario passes.
  - **Date**: 2026-08-09. **Status**: Done. **Files Changed**: none (already satisfied, see RED note above). **Notes**: confirmed no-op GREEN — tier 1 override already worked correctly; nothing to implement.
- [x] [AI] **REFACTOR**: Collapse the three resolution branches in `rhino-bin.sh` into one ordered lookup
      — command: `shellcheck --severity=warning apps/rhino-cli/scripts/rhino-bin.sh && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --test gate_specs`
      — acceptance: both exit 0.
  - **Date**: 2026-08-09. **Status**: Done. **Files Changed**: `apps/rhino-cli/scripts/rhino-bin.sh`. **Notes**: collapsed the three separate `exec ... "$@"` call sites into a single if/elif/else chain that sets `RESOLVED_BIN` per tier, one `exec` at the bottom. Real DRY win. `shellcheck --severity=warning` and full `gate_specs` suite (7 features/66 scenarios/241 steps) both pass. Also fixed a preexisting unrelated defect found while running the full suite: `gate_specs.rs`'s cucumber harness scans the whole `gate/` feature dir including `gate-emission.feature`; a prior step's "Rhino CLI kind renders a resolver shim invocation" scenario had a stale expected string plus one unbound step — fixed both (root-caused, not routed around) per repo policy on proactively fixing preexisting errors encountered during work. `cargo test --lib`: 1366 passed/0 failed/1 ignored. `cargo fmt --check` and `cargo clippy --test gate_specs -- -D warnings` clean.
- [x] [AI] Regenerate the derived artifacts: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate emit && npm run generate:bindings`
      — acceptance: `.husky/pre-commit`, `.husky/pre-push`, `.husky/commit-msg`, and the `lint-staged` block in `package.json` contain no `cargo run` substring; `npm run validate:sync` exits 0.
  - **Date**: 2026-08-09. **Status**: Done. **Files Changed**: `.husky/pre-commit`, `.husky/pre-push`, `.husky/commit-msg`, `package.json` (lint-staged block, via `gate emit --surface=pre-commit`), `.amazonq/rules/00-agents-md.md`, `.amazonq/cli-agents/ose-default.json` (via `generate:bindings`). **Notes**: **corrected another plan-authoring gap** — `gate emit --surface=<s>` only supports `pre-commit` (errors "currently supports only surface pre-commit" for the other 3); it regenerates only the `lint-staged` block in `package.json`, not the `.husky/*` files themselves. `.husky/pre-commit`/`pre-push`/`commit-msg` are hand-authored static dispatch shims (no Rust codepath writes them — confirmed via grep), each with one bootstrap line invoking `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate run --surface=<s>` to launch rhino-cli itself; this line is outside `GateKind::RhinoCli` rendering (it's not a registry-declared gate command) and so was untouched by the emit.rs change in items 1-3. Hand-edited all 3 to invoke `apps/rhino-cli/scripts/rhino-bin.sh` directly instead, matching DD-1's intent (every `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml --` invocation site, not just declared-gate commands, goes through the shim). Verified: `shellcheck --severity=warning` and `shfmt -d` both exit 0 on all 3; `grep -c "cargo run --release"` returns 0 for all 3 hook files and the lint-staged block; `npm run validate:sync` — 95/95 checks passed, exit 0. `package.json`'s 8 top-level `npm run` script definitions (e.g. `generate:bindings`, `doctor`) still contain `cargo run --release` — out of scope per the acceptance clause's literal wording ("the lint-staged block"), and out of scope for DD-1 (those are direct developer/CI invocations, not gate-declared or hook-dispatch commands); left unchanged.
  - _These generated files land in the SAME commit as `emit.rs`. See [File-Touch Discipline](../../../repo-governance/development/practice/file-touch-discipline.md)._

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate` — acceptance: exits 0, confirming shims and registry agree.
  - **Date**: 2026-08-09. **Status**: Done. **Notes**: exits 0, no output (no disagreement found).
- [x] [AI] Diff the executed gate id set against Phase 0 for all four surfaces — acceptance: byte-identical to `baseline/gates-<surface>.txt` (M5/AC-4).
  - **Date**: 2026-08-09. **Status**: Done. **Notes**: `diff <(jq -r '.[].id' baseline) <(jq -r '.[].id' current) | sort` empty for all 4 surfaces (pre-commit, pre-push, commit-msg, ci) — gate id sets byte-identical to Phase 0. Compared ids only, not full JSON — the `command` field for `rhino-cli`-kind gates legitimately changed (now renders through the shim), which is the expected Phase 2 effect, not a regression.
- [x] [AI] Measure M1 with the same `bash` harness used at baseline, then append a `Phase 2` row to `scoreboard.md` with `Status = IMPROVED`/`REGRESSED`/`UNCHANGED` against the Phase 0 baseline row — acceptance: recorded; expected to fall from 3,047 ms toward ~1,200 ms (the remaining `npx` tax is removed in Phase 3).
  - **Date**: 2026-08-09. **Status**: Done. **Notes**: mean 2,534 ms (N=3: 2,759/2,576/2,266), all exit 0, same 10-file harness (staged trivial reversible append, `npx lint-staged --no-stash`, `git checkout HEAD --`/`git reset --` revert, `git status --porcelain` confirmed identical to pre-measurement state after). vs Phase 0 baseline (3,898 ms): −1,364 ms / −35.0 %, `Status = IMPROVED`. Note: this item's own acceptance text cites a baseline of "3,047 ms" — `baseline/measurements.md`'s actual recorded Phase 0 M1 baseline is 3,898 ms; the 3,047 figure does not match any recorded baseline value and looks like a stale/pre-baseline draft number. Used the real recorded baseline (3,898 ms) for the scoreboard Δ, not the stale 3,047 figure.
- [ ] [AI] Commit this phase's changes thematically and push to the open PR branch — acceptance: push succeeds; the PR's check run starts.

> **Pause Safety**: hooks dispatch through the shim and all gates still run identically. Safe to stop. To resume: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate`.

---

## Phase 3 — Direct `node_modules/.bin` dispatch (DD-2)

- [ ] [AI] Add the scenario below to `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-emission.feature` — acceptance: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs gherkin-cardinality validate specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-emission.feature` exits 0.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] **RED**: Write a failing test in the `apps/rhino-cli/src/commands/gate/emit.rs` tests module binding the scenario below
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::emit`
      — acceptance: test fails on the rendered command string.
  - **Gherkin (binds) →** "Node-resolved external tools render a repository-local bin path"

    ```gherkin
    Scenario: Node-resolved external tools render a repository-local bin path
      Given the registry declares an external gate whose tool resolves from node_modules
      When "rhino-cli gate emit --surface=pre-commit" runs
      Then the generated command invokes that tool through "node_modules/.bin"
      And the generated command contains no "npx" substring
    ```

  - _Suggested executor: `swe-rust-dev`_

- [ ] [AI] **GREEN**: Add node-tool resolution to `emit.rs`, gated on the registry distinguishing node-resolved tools from system tools via the existing `doctor_tools` field
      — command: same as above
      — acceptance: test passes; system tools such as `shellcheck` and `hadolint` are unchanged.
- [ ] [AI] **REFACTOR**: Consolidate the resolution logic so node-tool and rhino-cli resolution share one code path
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib`
      — acceptance: all lib tests pass.
- [ ] [AI] Regenerate: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate emit && npm run generate:bindings`
      — acceptance: `npm run validate:sync` exits 0; the `lint-staged` block references `node_modules/.bin/` for prettier and markdownlint-cli2.

### Phase 3 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] Diff the executed gate id set against Phase 0 for all four surfaces — acceptance: byte-identical (M5/AC-4).
- [ ] [AI] Stage 10 markdown files and measure M1, then append a `Phase 3` row to `scoreboard.md` — acceptance: **mean over three runs is at most 900 ms** (AC-1); figure recorded in `baseline/measurements.md` beside the baseline, and the scoreboard row's `vs Target` column reads `PASS`.
- [ ] [AI] Run a real commit of a markdown-only change and confirm the hook passes — acceptance: `git commit` succeeds and every markdown gate reports its baseline result.
- [ ] [AI] Commit this phase's remaining changes thematically and push to the open PR branch — acceptance: push succeeds; the PR's check run starts.

> **Pause Safety**: pre-commit is at target and coverage is proven unchanged. Safe to stop. To resume: re-measure M1.

---

## Phase 4 — Rust build configuration: profiles and version pin (DD-6, DD-9)

Independent of Phase 3; may run in parallel.

- [ ] [AI] Add `[profile.gate]` to `apps/rhino-cli/Cargo.toml` inheriting from `release` with `lto = false`, `codegen-units = 16`, `opt-level = 1`, leaving `[profile.release]` untouched
      — command: `cargo build --profile gate --manifest-path apps/rhino-cli/Cargo.toml`
      — acceptance: builds successfully and produces `apps/rhino-cli/target/gate/rhino-cli`.
  - _Suggested executor: `swe-rust-dev`_
- [ ] [AI] Measure the cold build under both profiles into isolated target dirs and record both figures
      — command: `rm -rf /tmp/ct && bash -c 'time CARGO_TARGET_DIR=/tmp/ct cargo build --profile gate --manifest-path apps/rhino-cli/Cargo.toml'`
      — acceptance: the gate profile builds materially faster than release; both figures recorded (baseline measured 53.0 s release vs 19.6 s fast).
- [ ] [AI] Confirm runtime parity between the two binaries on the slowest gate
      — command: `bash -c 'time (for i in 1 2 3; do apps/rhino-cli/target/gate/rhino-cli md links validate >/dev/null; done)'`
      — acceptance: within 15 % of the release binary's time for the same command.
- [ ] [AI] Point `apps/rhino-cli/scripts/rhino-bin.sh` and the gate-path Nx targets in `apps/rhino-cli/project.json` at `--profile gate`, leaving `build` on `--release`
      — command: `npx nx run rhino-cli:typecheck`
      — acceptance: exits 0.

### Version unification, `ose-public` side (DD-9)

- [ ] [AI] Confirm `baseline/rust-versions.md` from Phase 0 is still current (no drift since baseline capture): re-run its capture commands and diff — acceptance: identical output, or the delta is recorded and folded into the scoreboard's M9 baseline row before proceeding.
- [ ] [AI] Set `rust-version = "1.95.0"` in all four `ose-public` Rust manifests (`apps/rhino-cli`, `apps/ose-cli`, `apps/ayokoding-cli`, `libs/rust-commons`), matching the `channel` those crates already pin
      — command: `grep -h '^rust-version' apps/*/Cargo.toml libs/*/Cargo.toml | sort -u`
      — acceptance: exactly one line, reading `rust-version = "1.95.0"`.
  - _`ose-public` needs no `channel` edit: all four sites already pin `1.95.0`. Only the floor moves._
- [ ] [AI] Confirm the MSRV move does not break the compatibility gate — command: `npx nx run rhino-cli:compat:min-version` — acceptance: exits 0, and the run installs no toolchain (the floor now equals the already-present pinned channel).
- [ ] [AI] Add the scenario below to `specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature` — acceptance: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs gherkin-cardinality validate specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature` exits 0.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] **RED**: Write a failing test in the `apps/rhino-cli/src/application/doctor/tools.rs` tests module binding the scenario below
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib doctor::tools`
      — acceptance: test fails because the `rust` tool definition still reads `Cargo.toml → rust-version` and compares with `compare_gte`.
  - **Gherkin (binds) →** "doctor compares rustc against the toolchain that builds"

    ```gherkin
    Scenario: doctor compares rustc against the toolchain that builds
      Given the installed rustc differs from the pinned rust-toolchain.toml channel
      When "npm run doctor" runs
      Then it reports the Rust toolchain as mismatched
      And it names the pinned channel as the expected value
    ```

  - _Suggested executor: `swe-rust-dev`_

- [ ] [AI] **GREEN**: Repoint the `rust` entry in `tool_defs_rust()` at `apps/rhino-cli/rust-toolchain.toml → channel` — new `read_req` reader, `source` string updated, and `compare` switched from `compare_gte` to exact equality, since a pinned channel is not a floor
      — command: same as above
      — acceptance: test passes (AC-20).
- [ ] [AI] **REFACTOR**: Fold the `1.88` literals in the existing `read_rust_version` doc comments and tests to the new pinned value where they assert current behaviour, leaving fixtures that only exercise parsing untouched
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib doctor`
      — acceptance: exits 0, and `grep -c '1\.88' apps/rhino-cli/src/application/doctor/` returns only parser-fixture hits, each verified individually.
- [ ] [AI] Update `docs/explanation/software-engineering/programming-languages/rust/README.md:81` so the MSRV bullet states that the floor and the toolchain pin are deliberately the same value — command: `npx markdownlint-cli2 docs/explanation/software-engineering/programming-languages/rust/README.md` — acceptance: exits 0.
  - _Suggested executor: `docs-maker`_

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] `npx nx run rhino-cli:lint` — acceptance: exits 0.
- [ ] [AI] Diff the executed gate id set against Phase 0 — acceptance: byte-identical.
- [ ] [AI] Confirm `[profile.release]` is unchanged: `git diff apps/rhino-cli/Cargo.toml` — acceptance: the release block shows no modification.
- [ ] [AI] Confirm `ose-public` declares one Rust version: `cat $(find . -name rust-toolchain.toml -not -path './target/*' -not -path './node_modules/*') | grep '^channel' | sort -u` and the `^rust-version` equivalent — acceptance: each returns exactly one line and both name `1.95.0` (AC-19, M9 for this repo).
- [ ] [AI] `npm run doctor` — acceptance: exits 0 and reports the Rust source as the `rust-toolchain.toml` channel, not `Cargo.toml → rust-version`.
- [ ] [AI] Run local quality gates (see §Local Quality Gates), then commit this phase's changes thematically and push to the open PR branch — acceptance: local gates exit 0; push succeeds and the PR's check run starts.

> **Pause Safety**: two profiles coexist; the shipped artifact is unchanged; the version change is a one-number revert in five files. Safe to stop. To resume: `cargo build --profile gate --manifest-path apps/rhino-cli/Cargo.toml`.

---

## Phase 5 — `ci_group` becomes a required registry field (DD-3)

- [ ] [AI] Add the scenario below to `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-validation.feature` — acceptance: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs gherkin-cardinality validate specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-validation.feature` exits 0.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] **RED**: Write a failing test in the `apps/rhino-cli/src/commands/gate/validate.rs` tests module binding the scenario below
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate`
      — acceptance: test fails because `ci_group` is not yet required.
  - **Gherkin (binds) →** "A gate declared without a CI group fails validation"

    ```gherkin
    Scenario: A gate declared without a CI group fails validation
      Given a gate entry in repo-config.yml carrying a ci surface and no ci_group field
      When "rhino-cli gate validate" runs
      Then it exits non-zero
      And its output names the offending gate id
      And its output states that ci_group is required
    ```

  - _Suggested executor: `swe-rust-dev`_

- [ ] [AI] **GREEN**: Add the `ci_group` field to the gate schema in the `repo_config` module and enforce its presence in `validate.rs`
      — command: same as above
      — acceptance: test passes (AC-5).
- [ ] [AI] Add the scenario below to `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-enumeration.feature` — acceptance: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs gherkin-cardinality validate specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-enumeration.feature` exits 0.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] **RED**: Write a failing test in the `apps/rhino-cli/src/commands/gate/list.rs` tests module binding the scenario below
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::list`
      — acceptance: test fails because `--by-group` is unrecognized.
  - **Gherkin (binds) →** "Enumeration can group CI gates by declared group"

    ```gherkin
    Scenario: Enumeration can group CI gates by declared group
      Given every ci-surface gate in the registry declares a ci_group
      When "rhino-cli gate list --surface=ci --format=json --by-group" runs
      Then it emits one entry per distinct ci_group value
      And each entry lists its member gate ids in registry declaration order
    ```

  - _Suggested executor: `swe-rust-dev`_

- [ ] [AI] **GREEN**: Implement `--by-group` in `apps/rhino-cli/src/commands/gate/list.rs`
      — command: same as above
      — acceptance: test passes.
- [ ] [AI] Add the scenario below to `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature` — acceptance: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs gherkin-cardinality validate specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature` exits 0.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] **RED**: Write a failing test in the `apps/rhino-cli/src/commands/gate/run.rs` tests module binding the scenario below
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::run`
      — acceptance: test fails because `--group` is unrecognized.
  - **Gherkin (binds) →** "A failing gate inside a group is named in the output"

    ```gherkin
    Scenario: A failing gate inside a group is named in the output
      Given a CI group containing several gates where exactly one fails
      When "rhino-cli gate run --surface=ci --group=<id>" runs
      Then it exits non-zero
      And its output contains a per-gate summary line for every gate in the group
      And the failing gate id appears on a line marked FAIL
    ```

  - _Suggested executor: `swe-rust-dev`_

- [ ] [AI] **GREEN**: Implement `--group` in `apps/rhino-cli/src/commands/gate/run.rs`, including the per-gate summary output
      — command: same as above
      — acceptance: test passes (AC-6).
- [ ] [AI] **REFACTOR**: Deduplicate group filtering between `list.rs` and `run.rs`
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib`
      — acceptance: all lib tests pass.
- [ ] [AI] Add `ci_group` to every gate entry in `repo-config.yml` carrying a `ci` surface. Group by required toolchain, mirroring `beaver-nest`'s proven job names: markdown, shell/docker/actions, governance, specs, naming, formatting-verify
      — command: `cargo run --profile gate --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate`
      — acceptance: exits 0; every `ci`-surface gate declares a group.
- [ ] [AI] Add the CI-topology scenarios AC-9 and AC-10 from `prd.md` to `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature` (AC-5, AC-6, and AC-18 already landed with their RED cycles above)
      — command: `cargo run --profile gate --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs gherkin-cardinality validate specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature`
      — acceptance: exits 0.
  - _Suggested executor: `specs-maker`_

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] Verify the union of gate ids across all declared groups equals the Phase 0 `ci` capture — command: compare `gate list --surface=ci --by-group --format=json` flattened member ids against `baseline/gates-ci.txt` — acceptance: sets are byte-identical (AC-4). **No gate may be orphaned by grouping.**
- [ ] [AI] `npx nx run rhino-cli:test:quick` — acceptance: exits 0.
- [ ] [AI] Commit this phase's changes thematically and push to the open PR branch — acceptance: push succeeds; the PR's check run starts.

> **Pause Safety**: the registry declares groups and the CLI can enumerate and run them; the workflow still uses the old matrix, so CI is unaffected. Safe to stop. To resume: `cargo run --profile gate --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate`.

---

## Phase 6 — Build once, matrix over groups (DD-4)

- [ ] [AI] Add a `build-rhino` job to `.github/workflows/pr-quality-gate.yml` that checks out, sets up Rust, builds `--profile gate`, and uploads `apps/rhino-cli/target/gate/rhino-cli` via `actions/upload-artifact`
      — acceptance: `actionlint .github/workflows/pr-quality-gate.yml` exits 0.
- [ ] [AI] Change the `enumerate` job to emit groups: `gate list --surface=ci --format=json --by-group`
      — acceptance: `actionlint` exits 0.
- [ ] [AI] Change the `gate` job to matrix over groups, download the artifact, export `RHINO_CLI_BIN`, and run `gate run --surface=ci --group="$GROUP_ID"`; remove `./.github/actions/setup-rust` from it
      — acceptance: `actionlint` exits 0 and the job contains no `setup-rust` reference.
- [ ] [AI] Update the workflow-conformance assertions in `apps/rhino-cli/src/commands/gate/validate.rs` (`validate_ci_workflow`, whose assertions currently expect the per-gate `--only=` form; the fixture strings at lines 1473–1480 are one of ~12 `--only=` occurrences to update) to assert the new group form
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate`
      — acceptance: tests pass against the edited workflow.
  - _Suggested executor: `swe-rust-dev`_
- [ ] [AI] Preserve the protected status-check contract: the terminal job in `.github/workflows/pr-quality-gate.yml` MUST keep the job key `quality-gate` and the literal `name: Quality gate`, and must still fail when any dependency job fails — update only its `needs:` list to name the new group matrix — acceptance: `grep -c "name: Quality gate" .github/workflows/pr-quality-gate.yml` returns 1, and the string matches `baseline/required-checks.md` for this repo byte-for-byte.
  - _Renaming this job silently bricks merging for the whole repo. Treat the name as an external API._
- [ ] [AI] Reduce `fetch-depth` from `0` to a targeted fetch on every job that does not need full history — acceptance: only jobs running `nx affected` or `git diff` against a base ref retain `fetch-depth: 0`; `actionlint` exits 0.

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [ ] [AI] Commit this phase's changes thematically, push to the open PR branch, and confirm the workflow runs green — command: `gh run list -R wahidyankf/ose-public -L 1 --json status,conclusion` polled every 2 minutes — acceptance: conclusion is `success`.
  - _Poll at the 2-minute cadence; never `gh run watch`. A queued job is often runner contention across the four repos, not a defect._
- [ ] [AI] Verify every Phase 0 `ci` gate id appears in the run's logs — acceptance: all ids present (AC-4). **This is the phase's most important check.**
- [ ] [AI] Verify no gate job installed a Rust toolchain or ran `cargo install` — acceptance: grep of job logs returns no hits (AC-9).
- [ ] [AI] Verify the protected context still reports on the PR: `gh pr checks <pr> --json name,state` — acceptance: a check named exactly `Quality gate` is present and concluded; **if it is absent, revert the workflow change before merging — do not merge a PR whose required context never reported.**

> **Pause Safety**: CI is green under the grouped topology with coverage proven unchanged. Safe to stop. To resume: `gh run list -R wahidyankf/ose-public -L 1`.

---

## Phase 7 — Slim node setup and fix the cache key (DD-5, DD-8)

- [ ] [AI] Add a boolean input to `.github/actions/setup-node/action.yml` controlling whether `npm ci` runs, defaulting to `true` so existing callers are unaffected
      — acceptance: `actionlint` exits 0 and all existing call sites behave identically.
- [ ] [AI] Set that input to `false` for every gate group whose gates require no node-resolved tool
      — acceptance: those jobs' logs contain no `npm ci` (AC-10).
- [ ] [AI] Remove `-${{ github.sha }}` from the `.nx/cache` key at `.github/actions/setup-node/action.yml:30`, retaining the existing `restore-keys` fallbacks
      — acceptance: the key no longer interpolates `github.sha`; `actionlint` exits 0.

### Phase 7 Gate

> All checks below must pass before starting Phase 10.

- [ ] [AI] Commit this phase's changes thematically, push to the open PR branch, and confirm CI green — acceptance: push succeeds; conclusion is `success` and every Phase 0 `ci` gate id appears in the logs.
- [ ] [AI] Measure M3 over 5 completed runs, then append a `Phase 7` row to `scoreboard.md` — acceptance: **median at most 3,500 runner-seconds** (AC-3).
- [ ] [AI] Measure M4 over 10 completed runs, then append a `Phase 7` row to `scoreboard.md` (`Status = REGRESSED` is a hard stop here, not a note-and-continue — M4 is a no-regression target) — acceptance: **p50 wall-clock no greater than the Phase 0 baseline** (AC-3). If wall-clock regressed, re-balance group composition before proceeding.
- [ ] [AI] After 10 further commits, measure M7, then append a `Phase 7` row to `scoreboard.md` — acceptance: **cache at most 60 % of the 10 GiB ceiling** (AC-11).

> **Pause Safety**: CI topology is complete and measured against targets. Safe to stop. To resume: re-measure M3 and M4.

---

## Phase 8 — Recompose `test:quick` (DD-7)

Independent of Phases 5–7; may run in parallel.

- [ ] [AI] Remove `npx nx run rhino-cli:test:coverage` from the `test:quick` command chain in `apps/rhino-cli/project.json`, leaving the `test:coverage` target itself intact and unchanged
      — command: `npx nx run rhino-cli:test:quick --skip-nx-cache`
      — acceptance: exits 0 and the run no longer produces a `llvm-cov-target` directory.
- [ ] [AI] Add `test:coverage` to the Rust quality-gate job in `.github/workflows/pr-quality-gate.yml` so coverage still gates merge
      — command: `actionlint .github/workflows/pr-quality-gate.yml`
      — acceptance: exits 0 and the job runs `test:coverage` with `--fail-under-lines 90` intact (AC-13).
- [ ] [AI] Collapse the seven sequential `cargo test` invocations in the `test:unit` target where they share a profile, preserving `--test-threads=1` for the lib run
      — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib -- --list`
      — acceptance: the emitted test-name list is byte-identical to `baseline/test-names.txt` (AC-2 guard).
- [ ] [AI] Update `repo-governance/development/infra/nx-targets.md` to document the new `test:quick` composition and state that coverage is enforced on CI
      — command: `npx markdownlint-cli2 repo-governance/development/infra/nx-targets.md`
      — acceptance: exits 0.
  - _Suggested executor: `repo-rules-maker`_

### Phase 8 Gate

> All checks below must pass before starting Phase 9.

- [ ] [AI] Measure M2, then append a `Phase 8` row to `scoreboard.md` — acceptance: **mean over two runs at most 90 s** (AC-2).
- [ ] [AI] Measure M6 into an isolated target dir, then append a `Phase 8` row to `scoreboard.md` — acceptance: **at most 1.2 GB** (AC-12).
- [ ] [AI] Diff the executed test-name list against `baseline/test-names.txt` — acceptance: byte-identical. **A speedup by running fewer tests fails here.**
- [ ] [AI] Commit this phase's changes thematically, push to the open PR branch, and confirm the Rust quality gate still fails on a deliberate coverage drop — acceptance: a scratch commit dropping coverage below 90 % turns the job red (AC-13).
- [ ] [AI] Revert the scratch commit and confirm the job returns green — acceptance: `git log -1 --oneline` no longer shows the scratch commit and the Rust quality gate concludes `success`. **This step is mandatory; the branch must never be left carrying a knowingly-red commit.**

> **Pause Safety**: pre-push is at target, coverage enforcement relocated and proven still binding. Safe to stop. To resume: re-measure M2.

---

## Phase 9 — Disk hygiene (Axis D)

- [ ] [AI] Enumerate `local-temp/` reclaim candidates into `plans/in-progress/optimize-cis/local-temp-reclaim-manifest.md`, admitting a path **only** when every predicate below holds. Each is machine-checkable; no human judgement is involved.
  1. It is a build-artifact directory — its name is `.next`, `dist`, `out`, `build`, `target`, or `node_modules`, **and** for `.next` it contains a `BUILD_ID` file.
  2. A named command regenerates it (record the command per row, e.g. `nx build organiclever-www`).
  3. Its mtime is older than 7 days.
  4. It is not under, and does not contain, any of: `generated-reports/`, any `.env*` file, any git-tracked file, any path inside a `worktrees/` entry from `git worktree list`, or any `.git` directory.
  5. No git-tracked file in any of the four repos references its path (`grep -rl "<path>"` across tracked files returns nothing).
  - acceptance: every row records size, mtime, the matched artifact type, and its regeneration command; rows sum to at least 9 GB; **nothing is moved or deleted by this step**.
- [ ] [AI] Move — do not delete — every manifest row into a dated quarantine: `mkdir -p local-temp/.reclaim-quarantine-$(date +%F)` then `mv` each path into it — acceptance: `du -sk local-temp` is unchanged (the bytes moved, not freed); every manifest path now resolves inside the quarantine; a single `mv` back restores the prior state.
  - _Quarantine-then-verify is what makes this step safely `[AI]`. The destructive act is deferred until after the phase gate has proved nothing load-bearing was taken, and until then the whole operation is one `mv` from undone._
- [ ] [AI] With the quarantine in place, prove nothing load-bearing was captured: `npm run doctor -- --fix && npx nx run rhino-cli:test:quick && npx nx affected -t build` — acceptance: all exit 0. **If any fails, `mv` the quarantine contents back and re-derive the manifest — do not proceed.**
- [ ] [AI] Delete the quarantine: `rm -rf local-temp/.reclaim-quarantine-*` — acceptance: `du -sk local-temp` falls by at least 9 GB; `git status --porcelain` shows no tracked-file change from this phase.

- [ ] [AI] Add a retention rule for `local-temp/` to `repo-governance/development/infra/temporary-files.md`, stating the window and that the sweeper still must not touch it automatically — command: `npx markdownlint-cli2 repo-governance/development/infra/temporary-files.md` — acceptance: exits 0 (AC-14).
  - _Suggested executor: `repo-rules-maker`_
- [ ] [AI] Extend `doctor --fix`'s target-share step to cover worktrees, so `worktrees/*/apps/rhino-cli/target` symlinks into the shared cache rather than duplicating 221.8 MB per worktree — command: `npx nx run rhino-cli:test:unit` — acceptance: the `cargo_target_share` tests pass and a worktree's `target` resolves to a symlink.
  - _Suggested executor: `swe-rust-dev`_
- [ ] [AI] Record the cross-worktree cargo build-lock contention finding (65 s observed block) in `learnings.md` for triage — acceptance: an entry exists with context, observation, and generalization reasoning.
  - _Not fixed here: the shared cache trades disk for serialization, and reversing that tradeoff is a design question deserving its own plan._

### Phase 9 Gate

> All checks below must pass before starting Phase 10.

- [ ] [AI] Measure M8 **partial**, then append a `Phase 9` row to `scoreboard.md` — acceptance: **at least 9 GB reclaimed** versus the Phase 0 bucket table. The remaining ≥1 GB comes from the toolchain prune in Phase 10; M8's full **≥10 GB** target is asserted at the Phase 10 Gate, not here.
- [ ] [AI] `npm run doctor -- --fix` then `npx nx run rhino-cli:test:quick` — acceptance: both exit 0, proving nothing load-bearing was removed.
- [ ] [AI] Run local quality gates (see §Local Quality Gates), then commit this phase's changes thematically and push to the open PR branch — acceptance: local gates exit 0; push succeeds and the PR's check run starts.

> **Pause Safety**: disk reclaimed and hygiene documented; the toolchain rebuilds cleanly. Safe to stop. To resume: `npm run doctor -- --fix`.

---

## Phase 10 — Cross-repo propagation (`ose-primer`, `ose-private`)

**Repo scope is exactly three: `ose-public`, `ose-primer`, `ose-private`.** `beaver-nest` is
excluded — its `rhino-cli` is a fork with no `src/commands/gate/` subsystem, it is already the
fastest repo of the four, and it is slated for deprecation immediately after this plan. See
[`README.md` §Affected repositories](./README.md#affected-repositories--three-of-four).

- [ ] [AI] Resolve the parity-message contradiction this plan trips over. `apps/rhino-cli/src/application/parity.rs:560` and its test at line 867 both state the manifest files are "byte-identical across ose-public, ose-primer, ose-private, and beaver-nest", but `AGENTS.md:445-447` scopes the boundary to three repos and `beaver-nest` has no `apps/rhino-cli/parity-manifest.sha256` — command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib parity` — acceptance: both strings name exactly the three parity repos, the test asserting the message passes, and `grep -c "beaver-nest" apps/rhino-cli/src/application/parity.rs` returns 0.
  - _Not scope creep: this plan edits `apps/rhino-cli/src/` heavily, so every parity failure during this phase prints an instruction to propagate into a repo that has no manifest to propagate into._
  - _Suggested executor: `swe-rust-dev`_
- [ ] [AI] Provision one worktree per sibling repo — `git -C /Users/wkf/ose-projects/ose-primer worktree add worktrees/optimize-cis` and the same for `ose-private` — acceptance: both worktrees exist on a branch off the latest `origin/main`.
  - _One worktree per repo per plan (HARD RULE). Never run git-mutating agents in a primary checkout._
- [ ] [AI] Propagate every `apps/rhino-cli/` source change to both sibling worktrees, then regenerate derived artifacts in each: `cargo run --profile gate --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate emit && npm run generate:bindings` — acceptance: `npm run validate:sync` exits 0 in each, and generated artifacts are staged in the same commit as their source.
- [ ] [AI] Add the `ci_group` field to every `ci`-surface gate in each sibling's `repo-config.yml`, mirroring the group taxonomy adopted in Phase 5 — command: `cargo run --profile gate --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate` in each — acceptance: exits 0 in both; every `ci`-surface gate declares a group.
  - _`ose-private` is the largest single win available: 23 of its 33 `lint-staged` entries are `cargo run` invocations (vs 7 here), and its CI overhead is **91.9 %** `[Repo-grounded]`._
- [ ] [AI] Apply the grouped workflow, `build-rhino` artifact job, conditional `npm ci`, and the `github.sha`-free Nx cache key to `.github/` in each sibling — command: `actionlint .github/workflows/pr-quality-gate.yml` in each — acceptance: exits 0; each sibling's gate jobs contain no `setup-rust` and no `cargo install`.
  - _All three repos carry the same `github.sha` cache-key defect and the same unconditional `npm ci` `[Repo-grounded]`._
- [ ] [AI] Apply the same protected-context guard in each sibling: confirm that repo's terminal job name still matches the contexts captured in `baseline/required-checks.md` — acceptance: for each sibling, either the recorded context string is still emitted by a job, or the file recorded that no protection payload was readable.
- [ ] [AI] Verify per-repo coverage invariance: in each sibling, diff the executed `ci` gate id set against that repo's own pre-change capture — acceptance: byte-identical per repo (AC-4 applied per repo). **A gate must not be orphaned by grouping in any repo.**
- [ ] [AI] Sweep every doc naming the old invocation form across all three repos: `grep -rn "cargo run --release --quiet --manifest-path apps/rhino-cli" --exclude-dir=node_modules --exclude-dir=target --exclude-dir=.git .` — acceptance: remaining hits are only in `plans/done/` historical records, verified per repo with a per-file verdict.
  - _Fix the class, not just the cited sites: enumerate every file stating the rule, per repo._

### Version unification, sibling side (DD-9)

- [ ] [AI] Replace `channel = "stable"` with `channel = "1.95.0"` in `ose-primer/apps/crud-be-rust-axum/rust-toolchain.toml` and `ose-private/apps/coralpolyp-be/rust-toolchain.toml` — acceptance: `grep -h '^channel' $(find . -name rust-toolchain.toml -not -path './target/*' -not -path './node_modules/*') | sort -u` returns exactly one line per repo, reading `1.95.0`.
  - _These two crates are the only sites in any repo that build on a floating alias. Everything else is already pinned._
- [ ] [AI] Align every sibling `rust-version` to `1.95.0`, including the lone `1.94.0` outlier in `ose-primer/apps/crud-be-rust-axum/Cargo.toml` — acceptance: the `^rust-version` `sort -u` returns exactly one line per repo (AC-19).
- [ ] [AI] Propagate the Phase 4 `doctor` change (channel-sourced expected-rustc) into both siblings as part of the `apps/rhino-cli/` propagation, then run `npm run doctor` in each — acceptance: exits 0 in both and reports the `rust-toolchain.toml` channel as the source (AC-20).
- [ ] [AI] Replace `ose-private`'s `dtolnay/rust-toolchain@stable` in `.github/actions/setup-rust/action.yml` with the `actions-rust-lang/setup-rust-toolchain@v1` form the other repos use, so the pinned channel is installed rather than fetched lazily on first `cargo` call — command: `actionlint .github/actions/setup-rust/action.yml` — acceptance: exits 0; the action installs the toolchain `rust-toolchain.toml` names.
  - _Today `ose-private` installs `stable`, never uses it, then downloads `1.95.0` mid-job — a full toolchain fetch per Rust job `[Repo-grounded]`._
- [ ] [AI] Correct the two stale version claims: `ose-private/repo-governance/workflows/infra/infra-development-environment-setup.md:59` states `>= 1.80 (MSRV)` where `apps/coralpolyp-be/Cargo.toml` declares otherwise, and `docs/.../rust/README.md:84` in **both** siblings hardcodes `Rust 1.82+ (stable)` — acceptance: neither file states a version number; both point at the declaring file, matching the `ose-public`/`beaver-nest` pattern.
  - _Fix the class, not the cited sites: `grep -rn 'Rust 1\.\|rustc 1\.\|>= 1\.' docs repo-governance` per repo, with a per-file verdict._
  - _Suggested executor: `docs-fixer`_

### Toolchain prune (DD-9, machine side)

> Runs only after the pin convergence above. Deriving the required set beforehand would read
> `stable` from the two unconverged crates and orphan whatever they then need.

- [ ] [AI] Re-derive the required-toolchain set from **all four** repos — `sort -u` over every `channel` in `rust-toolchain.toml` across `.` (`ose-public`), `/Users/wkf/ose-projects/ose-primer`, `/Users/wkf/ose-projects/ose-private`, and `/Users/wkf/ose-projects/beaver-nest` — acceptance: written to `baseline/rust-versions.md`, and the set is exactly `1.95.0`, matching Phase 0's capture of `beaver-nest` unchanged.
  - _`beaver-nest` is excluded from this plan's **changes**, not from the machine it shares. Pruning a toolchain it pins would break a repo this plan never touched._
- [ ] [AI] Decide `stable`'s fate by predicate, not judgement: `find ~ -name Cargo.toml -not -path '*/ose-projects/*' -not -path '*/.cargo/*' -not -path '*/.rustup/*' -not -path '*/target/*' -not -path '*/node_modules/*'` — acceptance: the result is recorded verbatim; `stable` is admitted to the prune list **only when this returns nothing**, and otherwise retained with the matching paths recorded as the reason.
  - _This is the one step whose blast radius leaves the OSE repos. The predicate is what keeps it `[AI]`: no repo-local evidence can rule out an unrelated consumer, so the plan looks instead of guessing._
- [ ] [AI] Uninstall each toolchain in `rustup toolchain list` absent from the required set (baseline orphans: `1.80` 1.1 GB, `1.94` 1.2 GB, `1.96.0` 952 MB; plus `1.88` 1.2 GB once the MSRV alignment has landed in all three repos) — command: `rustup toolchain uninstall <name>` per orphan — acceptance: `du -sh ~/.rustup` falls by at least 3 GB; `rustup toolchain list` contains only the required set plus any retained `stable`.
  - _Reversible via `rustup toolchain install <name>`, but the undo needs network, so the proof step below runs immediately rather than waiting for the phase gate._
- [ ] [AI] Set the default toolchain explicitly so nothing depends on a floating alias: `rustup default 1.95.0` — acceptance: `rustup show` reports `1.95.0` as active and default.
- [ ] [AI] Prove nothing was over-pruned: `npx nx run rhino-cli:test:quick` in `ose-public`, and `cargo build --manifest-path apps/rhino-cli/Cargo.toml` in each of `ose-primer`, `ose-private`, and `beaver-nest` — acceptance: all exit 0 **and none emits `info: downloading component` or `syncing channel updates`**, proving each needed toolchain was still present rather than silently re-fetched.
  - _Without the no-download assertion this step passes either way: rustup would transparently re-fetch what was just removed and report success. Same false-pass shape as the benchmark trap recorded in `learnings.md`._

- [ ] [AI] Record the `beaver-nest` exclusion and its tripwire in `learnings.md`: if deprecation slips past this plan, file a follow-up `plans/backlog/` entry for the three repo-agnostic wins it would still benefit from (DD-6 gate profile, DD-8 cache key, DD-5 conditional `npm ci`) — acceptance: an entry exists naming all three.
- [ ] [AI] Commit this phase's `ose-public`-side changes (the `parity.rs` message fix) thematically and push to the open `ose-public` PR branch — acceptance: push succeeds and the PR's check run starts. **This step must run before the Phase 10 Gate's "CI green" check below — otherwise that check validates a stale run from before this phase's own change.**

### Sibling PRs — `ose-primer` and `ose-private`

> Each sibling is its own repo with its own PR and its own required-status-check surface. The
> **PR-Review Maker→Fixer Cycle runs independently in each** — running it once in `ose-public` does
> not cover the propagated changes landing in the siblings. This is the step that makes "CI green in
> all three repos" and the identical parity hash in the Phase 10 Gate below actually reachable: both
> assertions need each sibling's changes to have gone through a PR and merged first.

- [ ] [AI] In the `ose-primer` worktree: run that repo's local quality gates, commit thematically, push the branch, and open a draft PR against `main` titled `chore(gates): propagate optimize-cis gate changes and unify Rust version` — acceptance: PR exists and CI (`pr-quality-gate`) has started.
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle on the `ose-primer` PR, iteratively until clean, capped at 10 cycles (see §Delivery Boundaries) — acceptance: a cycle reports zero CRITICAL/HIGH/MEDIUM findings, or the cap is reached with residue recorded as accepted-with-reason.
- [ ] [AI] Flip the `ose-primer` PR to ready for review — `gh pr ready -R wahidyankf/ose-primer <n>` — acceptance: `gh pr view -R wahidyankf/ose-primer <n> --json isDraft` reports `false`.
- [ ] [AI] Merge the `ose-primer` PR once the five hardened preconditions hold — acceptance: `gh pr view -R wahidyankf/ose-primer <n> --json state` reports `MERGED`.
- [ ] [AI] In the `ose-private` worktree: run that repo's local quality gates, commit thematically, push the branch, and open a draft PR against `main` titled `chore(gates): propagate optimize-cis gate changes and unify Rust version` — acceptance: PR exists and CI (`pr-quality-gate`) has started.
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle on the `ose-private` PR, iteratively until clean, capped at 10 cycles (see §Delivery Boundaries) — acceptance: a cycle reports zero CRITICAL/HIGH/MEDIUM findings, or the cap is reached with residue recorded as accepted-with-reason.
- [ ] [AI] Flip the `ose-private` PR to ready for review — `gh pr ready -R wahidyankf/ose-private <n>` — acceptance: `gh pr view -R wahidyankf/ose-private <n> --json isDraft` reports `false`.
- [ ] [AI] Merge the `ose-private` PR once the five hardened preconditions hold — acceptance: `gh pr view -R wahidyankf/ose-private <n> --json state` reports `MERGED`.
- [ ] [AI] Remove both sibling worktrees now that their PRs have merged: `git -C <repo> worktree remove worktrees/optimize-cis` — acceptance: `git worktree list` in each repo no longer lists it.

### Phase 10 Gate

> All checks below must pass before starting Phase 11.

- [ ] [AI] `parity manifest validate` in `ose-public`, `ose-primer`, and `ose-private` — acceptance: exits 0 with an identical manifest hash in all three (AC-15).
- [ ] [AI] CI green in all three repos — acceptance: latest `pr-quality-gate` conclusion is `success` in each.
- [ ] [AI] Measure M3 per sibling repo, then append `Phase 10` rows to `scoreboard.md` (one per repo) — acceptance: `ose-primer` and `ose-private` each record a post-change median runner-seconds figure against their Phase 0 baselines (11,683 s and 9,239 s respectively); both show a reduction.
- [ ] [AI] Confirm `beaver-nest` was not modified — acceptance: `git -C /Users/wkf/ose-projects/beaver-nest status --porcelain` is empty.
- [ ] [AI] Measure M9, then append a `Phase 10` row to `scoreboard.md` — acceptance: across all three repos the `^channel` and `^rust-version` `sort -u` sets each contain **exactly one** value and the two agree (`1.95.0`), down from 3 distinct declared values at baseline (AC-19).
- [ ] [AI] Measure M9's machine half, folded into the same `Phase 10` scoreboard row as the repo-side M9 measurement above — acceptance: every entry of `rustup toolchain list` appears in the required set, except a `stable` retained with its recorded predicate result (AC-21).
- [ ] [AI] Measure M8 **in full**, then append a `Phase 10` row to `scoreboard.md` superseding the Phase 9 partial row — acceptance: **at least 10 GB reclaimed** versus the Phase 0 bucket table, combining the Phase 9 quarantine deletion with this phase's toolchain prune.

> **Pause Safety**: all three parity repos are consistent, their gates pass, and both sibling worktrees are removed. Safe to stop. To resume: re-run `parity manifest validate` in each of the three repos.

---

## Phase 11 — Measurement rollup against targets

- [ ] [AI] Confirm M5 one final time across all four surfaces, then append a `Phase 11` row to `scoreboard.md` — acceptance: gate id sets byte-identical to Phase 0 (AC-4).
- [ ] [AI] Render `plans/in-progress/optimize-cis/results.md` from `scoreboard.md`'s last row per metric (M1–M9) — every row gets a final `Status = PASS`/`FAIL` against its committed target, not just `IMPROVED`/`REGRESSED` — acceptance: nine before/after pairs with a PASS/FAIL verdict, and each links back to the scoreboard phase that produced its final measurement.
- [ ] [AI] For any metric that missed its target, record the measured shortfall and either a follow-up `plans/backlog/` entry or an explicit accepted-as-is note — acceptance: no metric is left without a verdict.
  - _A missed target is a finding to record honestly, not a number to quietly restate._

### Phase 11 Gate

> All checks below must pass before starting Phase 12.

- [ ] [AI] Verify `results.md` carries a verdict for all nine metrics — acceptance: nine PASS/FAIL rows present.
- [ ] [AI] Verify `scoreboard.md` has no gap: every phase that appended a row per this checklist did so — acceptance: the set of `Phase` values in `scoreboard.md` is `{0, 2, 3, 7, 8, 9, 10, 11}` with no phase skipped that was supposed to measure something.

> **Pause Safety**: outcomes are recorded honestly against committed targets. Safe to stop. To resume: read `results.md`.

---

## Phase 12 — Knowledge Capture

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only entries where a durable surface would catch this automatically next time; discard the rest with a one-line reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize to `<placeholder>` tokens or discard if the entry cannot be sanitized without losing its meaning.
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — infra-private content stays in `ose-private` only; public-governance content may route to `ose-public`/`ose-primer`; never cross-route private content into a public repo.
- [ ] [AI] Route each surviving entry to exactly one durable home (`repo-governance/`, `docs/`, `.claude/agents/`, `.claude/skills/`, or a `plans/backlog/` follow-up), landing small non-code edits inline.
  - _Two entries are already expected: the `zsh`-word-splitting measurement trap (a benchmarking-method rule) and the cross-worktree cargo lock contention finding._
- [ ] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing two-pagers FIRST for a brief already covering the same area — fold into that brief rather than creating a new file.
- [ ] [AI] **Code-routing rule**: if a learning's home is `apps/`, `libs/`, or tests, file it as a separate `plans/backlog/` plan — NEVER land it inline in this plan's commits/PR.
- [ ] [AI] Record the terminal state of every entry (routed inline / filed as backlog at `<path>` / discarded with reason) directly in `learnings.md`.
- [ ] [AI] If execution genuinely surfaced no generalizable learning, record the explicit escape `No generalizable learnings — <one-line reason>` instead of individual entries.

### Phase 12 Gate

> All checks below must pass before starting Plan Archival.

- [ ] [AI] Verify every `learnings.md` entry has reached a terminal state or the explicit "none" escape is present — acceptance: no entry left open.
- [ ] [AI] Verify no code-homed learning landed inline — acceptance: every code-routed learning has a corresponding `plans/backlog/` folder.

> **Pause Safety**: all learnings are triaged to durable homes or explicitly discarded. Safe to stop. To resume: re-check `learnings.md` for entries without a terminal-state marker.

---

---

### Close the `ose-public` PR

> This is the plan's only `ose-public` merge event. The PR has been open and accumulating pushed
> commits since the end of Phase 1 — see §Open the `ose-public` PR — through the ose-public side of
> Phase 10 (the `parity.rs` message fix), Phase 11 (`results.md`), and Phase 12 (Knowledge Capture
> routing). The plan folder's `git mv` to `plans/done/` happens here, in this section's first step,
> not inside Phase 12 — it must ride inside this PR before merge, since `main` is branch-protected
> and the PR budget is exactly 3. The `ose-primer`/`ose-private` PRs are separate repos and already
> merged inside Phase 10 — see its "Sibling PRs" subsection; they are not part of this PR's diff.

- [ ] [AI] Move the plan folder — `git mv plans/in-progress/optimize-cis plans/done/YYYY-MM-DD__optimize-cis` using the actual completion date — update `plans/in-progress/README.md` (remove the entry), `plans/done/README.md` (add the entry with completion date), and any other README referencing this plan. This must land inside the open PR: `main` is branch-protected with no direct-push path, and the plan's PR budget is exactly 3 (§Delivery Boundaries) — there is no follow-up PR to carry it — acceptance: `git status` shows the move staged; `grep -rl 'plans/in-progress/optimize-cis' plans/ docs/` (excluding the moved folder itself) returns nothing.
- [ ] [AI] Run local quality gates (see §Local Quality Gates), then commit Phase 11/12's changes and the plan-archival move thematically and push a final time to the open PR branch — acceptance: local gates exit 0; push succeeds and the PR's check run starts.
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle on the `ose-public` PR, iteratively until clean, capped at 10 cycles (see §Delivery Boundaries) — acceptance: a cycle reports zero CRITICAL/HIGH/MEDIUM findings, or the cap is reached with residue recorded as accepted-with-reason.
- [ ] [AI] Flip the `ose-public` PR to ready for review — `gh pr ready -R wahidyankf/ose-public <n>` — acceptance: `gh pr view -R wahidyankf/ose-public <n> --json isDraft` reports `false`.
- [ ] [AI] Merge once the five hardened preconditions hold.
- [ ] [AI] Final confirmation, closing the plan's full PR budget: `parity manifest validate` exits 0 in `ose-public`, `ose-primer`, and `ose-private` with an identical hash, and all 3 PRs opened across this plan (1 per repo) are merged — acceptance: `gh pr list -R wahidyankf/<repo> --state open` returns empty for all three repos.

---

## Local Quality Gates (Before Push)

- [ ] [AI] Run affected typecheck: `npx nx affected -t typecheck`
- [ ] [AI] Run affected linting: `npx nx affected -t lint`
- [ ] [AI] Run affected quick tests: `npx nx affected -t test:quick`
- [ ] [AI] Run affected spec coverage: `npx nx affected -t specs:behavior:coverage`
- [ ] [AI] Fix ALL failures found — including preexisting issues not caused by these changes
- [ ] [AI] Verify all checks pass before pushing

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work.

## Post-Push Verification

- [ ] [AI] Push changes to the PR branch (Delivery Mode is `worktree-to-pr`)
- [ ] [AI] Monitor the PR's check run — poll `gh run view --json status,conclusion` every **2 minutes**; never `gh run watch`
- [ ] [AI] Verify all CI checks pass
- [ ] [AI] If any CI check fails, investigate the root cause and push a follow-up commit — never bypass
- [ ] [AI] Do NOT proceed to the next delivery unit until CI is green

> A queued or stalled job is often runner contention across the four OSE repos, not a code defect.
> Check `gh run list --status=queued --status=in_progress` across repos before debugging code.

## Commit Guidelines

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits
- [ ] [AI] Follow Conventional Commits format: `<type>(<scope>): <description>`
- [ ] [AI] Split different domains/concerns into separate commits
- [ ] [AI] Land every generated artifact in the SAME commit as the source that produced it
- [ ] [AI] Do NOT bundle unrelated fixes into a single commit

## Validation Checklist

- [ ] [AI] All TDD cycles complete (RED→GREEN→REFACTOR for every code change)
- [ ] [AI] All tests pass (`npx nx affected -t test:quick`)
- [ ] [AI] All nine success metrics have a recorded verdict in `results.md`
- [ ] [AI] Gate coverage proven invariant on all four surfaces (M5/AC-4)
- [ ] [AI] Parity manifest identical across `ose-public`, `ose-primer`, and `ose-private`
- [ ] [AI] Documentation updated wherever the old invocation form was named

## Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked
- [ ] [AI] Verify ALL quality gates pass (local + CI)
- [ ] [AI] Confirm the plan-folder move already landed in the merged PR (§Close the `ose-public` PR) —
      acceptance: `plans/done/<completion-date>__optimize-cis/` exists on `main`,
      `plans/in-progress/optimize-cis/` does not, and `plans/in-progress/README.md` /
      `plans/done/README.md` reflect the move. No new commit or PR is created here — the move was
      already committed pre-merge, since `main` is branch-protected and the plan's PR budget is
      exactly 3 (§Delivery Boundaries).
- [ ] [AI] Remove the worktree immediately once this repo's work is done: `git worktree remove worktrees/optimize-cis`

> **Note on manual behavioral assertions**: this plan touches no web UI and no API surface — it
> changes build, hook, and CI plumbing only. The Playwright-MCP and curl verification sections, and
> the rule-15 web-triad and rule-16 API retests, are **not applicable**. Behavioral verification here
> is the coverage-invariance assertion (M5/AC-4), which is stronger for this change class: it proves
> the observable gate behaviour is byte-identical before and after.
