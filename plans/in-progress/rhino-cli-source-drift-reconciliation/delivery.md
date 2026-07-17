# Delivery Checklist — rhino-cli Source-Drift Reconciliation

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase is
> not complete until its gate is green; do not start phase N+1 while any gate check fails.

## Worktree

**Worktree path (per repo)**: `worktrees/rhino-cli-source-drift-reconciliation/` inside each of the
three repos. Because rhino-cli is byte-identical, the reconciliation runs as one leg per repo
(`ose-public`, `ose-primer`, `ose-infra`). Provision each from the latest `origin/main`; after
`git worktree add`, run `npm install` AND `npm run doctor -- --fix` per
[Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md).
Paths follow the [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
and [Plans Organization Convention § Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

Optional manual pre-provisioning (run from each repo's root — `ose-public`, `ose-primer`, and
`ose-infra` in turn):

```bash
claude --worktree rhino-cli-source-drift-reconciliation
```

## Delivery Mode: worktree-to-pr

Per-repo `worktree-to-pr`: each repo lands the reconciliation via a draft PR from its worktree
branch, running the `pr-review-maker` → `pr-review-fixer` cycle before merge. The single canonical
reconciled source lands identically in all three; only `repo-config.yml` data (and any values moved
into it) is repo-specific. Executed per repo via the
[plan-multi-repo-parity-planning-and-execution workflow](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning-and-execution.md)
(the _executing_ composite — each repo resolves its own `worktree-to-pr` leg). The **planning-only**
[plan-multi-repo-parity-planning workflow](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)
is NOT the execution mechanism `[Repo-grounded]`.

### Multi-Repo rhino-cli Delivery (hard rule)

Because this plan changes `rhino-cli` (inside the byte-identity boundary), the change lands
byte-identically in **all three** sibling repos — `ose-public`, `ose-primer`, `ose-infra` — and
**each repo gets its own full delivery**: (1) apply the identical change, (2) verify tri-repo
byte-identity via `diff`, (3) open a draft PR, (4) run the `pr-review-maker` → `pr-review-fixer`
**3 sequential CI-gated cycles** on that repo's PR, (5) pass **all** quality gates (local
`npx nx affected -t typecheck lint test:quick specs:behavior:coverage` + CI), and (6) `[HUMAN]`
merge that repo's PR only after its 3-cycle review AND all quality gates are green. Three peer PRs,
each independently reviewed and gated — never a single PR with side-propagation. The plan-folder
Knowledge-Capture + archival-in-PR happens only in the `ose-public` PR (the plan lives here).

## Delivery Flow

```mermaid
stateDiagram-v2
    [*] --> P0: env setup + baseline (3 repos)
    P0 --> P1: canonical determination
    P1 --> P2: apply canonical form (TDD)
    P2 --> P3: verify identity + gates
    P3 --> P4: draft PR + review cycle
    P4 --> P5: knowledge capture + archival
    P5 --> P6: [HUMAN] merge + post-verify
    P6 --> Teardown: remove worktrees (all 3 repos)
    Teardown --> [*]
```

---

## Phase 0: Environment Setup and Baseline (all three repos)

> _Suggested executor: `repo-setup-manager` (per repo)_

- [ ] [AI] Confirm all three repos are on `main` and clean:
      `for r in ose-public ose-primer ose-infra; do git -C ../$r status --porcelain; git -C ../$r rev-parse --abbrev-ref HEAD; done`
      — acceptance: each prints `main` with no dirty files.
- [ ] [AI] Provision a worktree in each repo:
      `git worktree add worktrees/rhino-cli-source-drift-reconciliation -b rhino-cli-source-drift-reconciliation origin/main`
      — acceptance: worktree dir + branch exist in each repo.
- [ ] [AI] In each worktree: `npm install` then `npm run doctor -- --fix`
      — acceptance: both exit 0, toolchain converged.
- [ ] [AI] Baseline rhino-cli per repo:
      `npx nx run rhino-cli:test:unit && npx nx run rhino-cli:test:integration && (cd apps/rhino-cli && cargo test)`
      — acceptance: baseline pass/fail recorded per repo; preexisting failures documented.
- [ ] [AI] Capture the pre-reconciliation tri-repo `diff` (the failing baseline) using the command in
      [tech-docs.md § Tri-repo verification command](./tech-docs.md#tri-repo-verification-command-canonical)
      — acceptance: the four drifted files (+ `tests/doctor.rs`) are listed; recorded as the baseline to eliminate.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `for r in ose-public ose-primer ose-infra; do git -C ../$r/worktrees/rhino-cli-source-drift-reconciliation rev-parse --abbrev-ref HEAD; done`
      — acceptance: prints `rhino-cli-source-drift-reconciliation` three times (worktree provisioned
      in every repo).
- [ ] [AI] `for r in ose-public ose-primer ose-infra; do (cd ../$r/worktrees/rhino-cli-source-drift-reconciliation && npm run doctor -- --fix); done`
      — acceptance: exits 0 in each worktree (toolchain converged).
- [ ] [AI] Re-run the tri-repo `diff` from
      [tech-docs.md § Tri-repo verification command](./tech-docs.md#tri-repo-verification-command-canonical)
      — acceptance: still reports the four drifted files + `tests/doctor.rs` (pre-reconciliation
      baseline reconfirmed; nothing changed yet).

> **Pause Safety**: Safe to stop after Phase 0 — only worktrees created, no source edited. Resume
> with the Phase 1 first step. Recovery: re-run the tri-repo `diff` to re-confirm the drift set.

## Phase 1: Per-file canonical determination

- [ ] [AI] For each drifted file (`docs/naming.rs`, `doctor/checker.rs`, `doctor/tools.rs`,
      `repo_governance/instruction_size.rs`, `tests/doctor.rs`), read all three variants side-by-side
      and classify each difference as **union-surface gap** (adopt superset) or **hardcoded per-repo
      value** (move to `repo-config.yml`) per
      [tech-docs.md § Reconciliation approach](./tech-docs.md#reconciliation-approach); append the
      decision (canonical form summary + classification) to `learnings.md` under the
      `## Per-file canonical decisions` heading
      — acceptance: `learnings.md`'s `## Per-file canonical decisions` heading contains one recorded
      decision for each of the five files.
- [ ] [AI] Draft the canonical union content for each file (superset of all three), keeping
      repo-inapplicable branches dormant (selected by `repo-config.yml` data)
      — acceptance: one canonical text per file, reviewed against all three inputs, losing no repo's applicable behavior.
- [ ] [AI] If any value must move to `repo-config.yml`: confirm the new key exists in all three repos'
      `repo-config.yml` with repo-appropriate values, satisfying the schema-parity gate:
      `cargo run --manifest-path apps/rhino-cli/Cargo.toml -- repo-config validate`
      — acceptance: the command exits 0 (passes) when run in all three repos.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] `grep -A20 "## Per-file canonical decisions" learnings.md`
      — acceptance: shows one recorded decision (canonical form + classification) for each of the
      five drifted files.
- [ ] [AI] Where a value moved to `repo-config.yml`:
      `cargo run --manifest-path apps/rhino-cli/Cargo.toml -- repo-config validate` in each of the
      three worktrees — acceptance: exits 0 in all three (skip this check if no value moved).

> **Pause Safety**: Safe to stop after Phase 1 — decisions drafted, no source overwritten yet. Resume
> at Phase 2. Recovery: `grep -A20 "## Per-file canonical decisions" learnings.md` is the source of
> truth for what to apply.

## Phase 2: Apply canonical form (TDD, per file, per repo)

> Reconciliation is source-convergence; guard it with rhino-cli's own tests so no behavior regresses.
> Each of the five drifted files gets its own RED→GREEN→REFACTOR cycle: written once in `ose-public`,
> then propagated byte-for-byte to `ose-primer` and `ose-infra` as explicit, separately-verified
> steps (never bundled into one "repeat in the other repos" action).
> _Suggested executor: `swe-rust-dev`_

### Cycle 1 — `src/application/docs/naming.rs`

- [ ] [AI] **RED** — add/adjust a test asserting the Phase-1-decided canonical naming-rule surface is
      present, run in whichever repo's current source lacks it:
      `cd apps/rhino-cli && cargo test application::docs::naming`
      — acceptance: the relevant test **fails** in the repo(s) whose source lacked the surface
      (proves the gap).
- [ ] [AI] **GREEN (ose-public)** — write the canonical union content decided in Phase 1 into
      `apps/rhino-cli/src/application/docs/naming.rs`; re-run
      `cd apps/rhino-cli && cargo test application::docs::naming`
      — acceptance: the new test and the `docs::naming` suite **pass** in `ose-public`.
- [ ] [AI] **GREEN (ose-primer propagation)** — apply the identical bytes:
      `cp apps/rhino-cli/src/application/docs/naming.rs ../ose-primer/apps/rhino-cli/src/application/docs/naming.rs`;
      re-run `(cd ../ose-primer/apps/rhino-cli && cargo test application::docs::naming)`
      — acceptance: file bytes identical to `ose-public`'s; suite **passes** in `ose-primer`.
- [ ] [AI] **GREEN (ose-infra propagation)** — apply the identical bytes:
      `cp apps/rhino-cli/src/application/docs/naming.rs ../ose-infra/apps/rhino-cli/src/application/docs/naming.rs`;
      re-run `(cd ../ose-infra/apps/rhino-cli && cargo test application::docs::naming)`
      — acceptance: file bytes identical to `ose-public`'s; suite **passes** in `ose-infra`.
- [ ] [AI] **REFACTOR** — apply formatting and re-check lint strictness in all three repos:
      `for r in . ../ose-primer ../ose-infra; do (cd $r/apps/rhino-cli && cargo fmt && cargo clippy --all-targets -- -D warnings); done`
      — acceptance: no fmt diffs and no clippy warnings in any of the three repos.

### Cycle 2 — `src/application/doctor/checker.rs`

- [ ] [AI] **RED** — add/adjust a test asserting the Phase-1-decided canonical doctor-check surface is
      present, run in whichever repo's current source lacks it:
      `cd apps/rhino-cli && cargo test application::doctor::checker`
      — acceptance: the relevant test **fails** in the repo(s) whose source lacked the surface.
- [ ] [AI] **GREEN (ose-public)** — write the canonical union content into
      `apps/rhino-cli/src/application/doctor/checker.rs`; re-run
      `cd apps/rhino-cli && cargo test application::doctor::checker`
      — acceptance: the new test and the `doctor::checker` suite **pass** in `ose-public`.
- [ ] [AI] **GREEN (ose-primer propagation)** — apply the identical bytes:
      `cp apps/rhino-cli/src/application/doctor/checker.rs ../ose-primer/apps/rhino-cli/src/application/doctor/checker.rs`;
      re-run `(cd ../ose-primer/apps/rhino-cli && cargo test application::doctor::checker)`
      — acceptance: file bytes identical to `ose-public`'s; suite **passes** in `ose-primer`.
- [ ] [AI] **GREEN (ose-infra propagation)** — apply the identical bytes:
      `cp apps/rhino-cli/src/application/doctor/checker.rs ../ose-infra/apps/rhino-cli/src/application/doctor/checker.rs`;
      re-run `(cd ../ose-infra/apps/rhino-cli && cargo test application::doctor::checker)`
      — acceptance: file bytes identical to `ose-public`'s; suite **passes** in `ose-infra`.
- [ ] [AI] **REFACTOR** — apply formatting and re-check lint strictness in all three repos:
      `for r in . ../ose-primer ../ose-infra; do (cd $r/apps/rhino-cli && cargo fmt && cargo clippy --all-targets -- -D warnings); done`
      — acceptance: no fmt diffs and no clippy warnings in any of the three repos.

### Cycle 3 — `src/application/doctor/tools.rs`

- [ ] [AI] **RED** — add/adjust a test asserting the union tool-parser surface (e.g.
      `parse_clang_format_version`, OpenTofu version extraction) is reachable, run in whichever repo's
      current source lacks it: `cd apps/rhino-cli && cargo test application::doctor::tools`
      — acceptance: the relevant test **fails** in the repo(s) currently missing that parser.
- [ ] [AI] **GREEN (ose-public)** — write the canonical union content into
      `apps/rhino-cli/src/application/doctor/tools.rs`; re-run
      `cd apps/rhino-cli && cargo test application::doctor::tools`
      — acceptance: the new test and the `doctor::tools` suite **pass** in `ose-public`.
- [ ] [AI] **GREEN (ose-primer propagation)** — apply the identical bytes:
      `cp apps/rhino-cli/src/application/doctor/tools.rs ../ose-primer/apps/rhino-cli/src/application/doctor/tools.rs`;
      re-run `(cd ../ose-primer/apps/rhino-cli && cargo test application::doctor::tools)`
      — acceptance: file bytes identical to `ose-public`'s; suite **passes** in `ose-primer`.
- [ ] [AI] **GREEN (ose-infra propagation)** — apply the identical bytes:
      `cp apps/rhino-cli/src/application/doctor/tools.rs ../ose-infra/apps/rhino-cli/src/application/doctor/tools.rs`;
      re-run `(cd ../ose-infra/apps/rhino-cli && cargo test application::doctor::tools)`
      — acceptance: file bytes identical to `ose-public`'s; suite **passes** in `ose-infra`.
- [ ] [AI] **REFACTOR** — apply formatting and re-check lint strictness in all three repos:
      `for r in . ../ose-primer ../ose-infra; do (cd $r/apps/rhino-cli && cargo fmt && cargo clippy --all-targets -- -D warnings); done`
      — acceptance: no fmt diffs and no clippy warnings in any of the three repos.

### Cycle 4 — `src/application/repo_governance/instruction_size.rs`

- [ ] [AI] **RED** — add/adjust a test asserting the Phase-1-decided canonical form (union surface,
      or a budget value now sourced from `repo-config.yml` if that was Phase 1's classification) is
      present, run in whichever repo's current source lacks it:
      `cd apps/rhino-cli && cargo test application::repo_governance::instruction_size`
      — acceptance: the relevant test **fails** in the repo(s) whose source lacked the canonical form.
- [ ] [AI] **GREEN (ose-public)** — write the canonical content into
      `apps/rhino-cli/src/application/repo_governance/instruction_size.rs`; re-run
      `cd apps/rhino-cli && cargo test application::repo_governance::instruction_size`
      — acceptance: the new test and the `repo_governance::instruction_size` suite **pass** in
      `ose-public`.
- [ ] [AI] **GREEN (ose-primer propagation)** — apply the identical bytes:
      `cp apps/rhino-cli/src/application/repo_governance/instruction_size.rs ../ose-primer/apps/rhino-cli/src/application/repo_governance/instruction_size.rs`;
      re-run `(cd ../ose-primer/apps/rhino-cli && cargo test application::repo_governance::instruction_size)`
      — acceptance: file bytes identical to `ose-public`'s; suite **passes** in `ose-primer`.
- [ ] [AI] **GREEN (ose-infra propagation)** — apply the identical bytes:
      `cp apps/rhino-cli/src/application/repo_governance/instruction_size.rs ../ose-infra/apps/rhino-cli/src/application/repo_governance/instruction_size.rs`;
      re-run `(cd ../ose-infra/apps/rhino-cli && cargo test application::repo_governance::instruction_size)`
      — acceptance: file bytes identical to `ose-public`'s; suite **passes** in `ose-infra`.
- [ ] [AI] **REFACTOR** — apply formatting and re-check lint strictness in all three repos:
      `for r in . ../ose-primer ../ose-infra; do (cd $r/apps/rhino-cli && cargo fmt && cargo clippy --all-targets -- -D warnings); done`
      — acceptance: no fmt diffs and no clippy warnings in any of the three repos.

### Cycle 5 — `tests/doctor.rs`

- [ ] [AI] **RED** — adjust the `tests/doctor.rs` integration binary to assert the canonical doctor
      behavior decided in Phase 1, run in whichever repo's current file lacks it:
      `cd apps/rhino-cli && cargo test --test doctor`
      — acceptance: the relevant assertion **fails** in the repo(s) whose `tests/doctor.rs` lacked it.
- [ ] [AI] **GREEN (ose-public)** — write the canonical content into `apps/rhino-cli/tests/doctor.rs`;
      re-run `cd apps/rhino-cli && cargo test --test doctor`
      — acceptance: `tests/doctor.rs` **passes** in `ose-public`.
- [ ] [AI] **GREEN (ose-primer propagation)** — apply the identical bytes:
      `cp apps/rhino-cli/tests/doctor.rs ../ose-primer/apps/rhino-cli/tests/doctor.rs`;
      re-run `(cd ../ose-primer/apps/rhino-cli && cargo test --test doctor)`
      — acceptance: file bytes identical to `ose-public`'s; **passes** in `ose-primer`.
- [ ] [AI] **GREEN (ose-infra propagation)** — apply the identical bytes:
      `cp apps/rhino-cli/tests/doctor.rs ../ose-infra/apps/rhino-cli/tests/doctor.rs`;
      re-run `(cd ../ose-infra/apps/rhino-cli && cargo test --test doctor)`
      — acceptance: file bytes identical to `ose-public`'s; **passes** in `ose-infra`. If instead
      Phase 1 documented a sanctioned divergence with rationale, skip propagation and record the
      rationale in `learnings.md` in place of this step.
- [ ] [AI] **REFACTOR** — apply formatting and re-check lint strictness in all three repos:
      `for r in . ../ose-primer ../ose-infra; do (cd $r/apps/rhino-cli && cargo fmt && cargo clippy --all-targets -- -D warnings); done`
      — acceptance: no fmt diffs and no clippy warnings in any of the three repos.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `for r in . ../ose-primer ../ose-infra; do (cd $r/apps/rhino-cli && cargo test); done`
      — acceptance: exits 0 in all three repos.
- [ ] [AI] `npx nx run rhino-cli:test:unit` in each of the three worktrees — acceptance: exits 0 in
      all three.
- [ ] [AI] `for r in . ../ose-primer ../ose-infra; do (cd $r/apps/rhino-cli && cargo fmt -- --check); done`
      (verifies formatting stuck — no further mutation, unlike the REFACTOR steps' plain `cargo fmt`)
      — acceptance: exits 0 (no diffs) in all three repos.
- [ ] [AI] `for f in application/docs/naming.rs application/doctor/checker.rs application/doctor/tools.rs application/repo_governance/instruction_size.rs; do diff -q apps/rhino-cli/src/$f ../ose-primer/apps/rhino-cli/src/$f; diff -q apps/rhino-cli/src/$f ../ose-infra/apps/rhino-cli/src/$f; done; diff -q apps/rhino-cli/tests/doctor.rs ../ose-primer/apps/rhino-cli/tests/doctor.rs; diff -q apps/rhino-cli/tests/doctor.rs ../ose-infra/apps/rhino-cli/tests/doctor.rs`
      — acceptance: zero output (identical bytes confirmed across all three repos for every target
      file, or the sanctioned `tests/doctor.rs` divergence documented in `learnings.md`).

> **Pause Safety**: Safe to stop after Phase 2 — each repo compiles and tests green, though the
> tri-repo `diff` is fully verified in Phase 3. Resume at Phase 3. Recovery: re-run
> `(cd apps/rhino-cli && cargo test)` per repo.

## Phase 3: Verify byte-identity + full local gates

- [ ] [AI] Run the tri-repo boundary `diff` from
      [tech-docs.md § Tri-repo verification command](./tech-docs.md#tri-repo-verification-command-canonical)
      — acceptance: **zero output** (all `src/`, manifest files, and gherkin tree byte-identical across every pair).
- [ ] [AI] Confirm `tests/doctor.rs` is identical across all three (or its divergence documented with
      rationale in `learnings.md`) — acceptance: `diff` returns identical, or a written justification exists.
- [ ] [AI] Per repo, run local quality gates on affected projects:
      `npx nx affected -t typecheck lint test:quick specs:behavior:coverage`
      — acceptance: green in all three repos; fix ALL failures found, including any preexisting ones
      (Root Cause Orientation).

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] Re-run the tri-repo boundary `diff` from
      [tech-docs.md § Tri-repo verification command](./tech-docs.md#tri-repo-verification-command-canonical)
      — acceptance: zero output in every repo pair.
- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` in each of the three
      worktrees — acceptance: exits 0 in all three.

> **Pause Safety**: Safe to stop after Phase 3 — identity verified locally, not yet pushed. Resume at
> Phase 4. Recovery: re-run the tri-repo `diff`.

## Phase 4: Multi-repo delivery (draft PR per repo, `worktree-to-pr`)

> **Sibling delivery mode**: each of the three repos delivers under its own `worktree-to-pr` leg —
> the reconciled bytes are identical, but each repo gets its own draft PR, review cycle, and CI run.
> Propagation is the concrete byte-application done in Phase 2 (same file bytes in every repo), not a
> workflow citation. Run the repos one at a time; the commands below are per-repo.

- [ ] [AI] Commit thematically in each repo (Conventional Commits), staging only the reconciled
      rhino-cli files (+ any `repo-config.yml`):
      `git add apps/rhino-cli/src apps/rhino-cli/tests && git commit -m "fix(rhino-cli): reconcile drifted src to canonical union surface"`
      — acceptance: one focused commit per repo; `git status` shows no unrelated staged files.
- [ ] [AI] Open a draft PR in each repo from its worktree branch:
      `gh pr create --draft --fill --base main --head rhino-cli-source-drift-reconciliation`
      — acceptance: a draft PR URL is returned for `ose-public`, `ose-primer`, and `ose-infra`.
- [ ] [AI] Run the `pr-review-maker` → `pr-review-fixer` cycle on each PR (default 3 CI-gated cycles)
      — acceptance: no unresolved CRITICAL/HIGH review findings on any of the three PRs.
- [ ] [AI] Push and verify CI per repo — poll every ~2 min (do NOT tight-loop, do NOT use
      `gh run watch`): `gh run list --limit 5` then `gh run view <run-id> --json status,conclusion`
      — acceptance: every triggered workflow concludes `completed`/`success` in each repo; fix root
      causes (including any preexisting failures) on red.

### Phase 4 Gate

> All checks below must pass before starting Phase 5. **"Done" here = a green reviewed PR handed
> off, NOT merged** — the `[HUMAN]` merge happens on the maintainer's own schedule (see Phase 6) and
> is not required for this gate.

- [ ] [AI] Per repo, from that repo's worktree: `gh pr checks rhino-cli-source-drift-reconciliation`
      — acceptance: all checks report passing in each of the three repos.
- [ ] [AI] Per repo: `gh pr view rhino-cli-source-drift-reconciliation --json reviewDecision`
      — acceptance: no unresolved CRITICAL/HIGH `pr-review-maker` findings remain open on any of the
      three PRs.

> **Pause Safety**: After any repo's PR is green, safe to stop between repos. Resume at the next
> repo's PR. Recovery: `gh run list` / `gh pr view` per repo to check state before continuing.

## Phase 5: Knowledge Capture + Archival (inside the `ose-public` PR, pre-merge)

> Both subsections land as commits **inside** the `ose-public` delivering PR, before its merge, per
> the [PR Review Quality Gate](../../../repo-governance/workflows/pr/pr-review-quality-gate.md)
> done-definition (archival-in-PR).

### Knowledge Capture

> Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md).

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch it automatically next time; discard the rest with a one-line reason
      — acceptance: every entry has either a route or a discard reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable
      — acceptance: `learnings.md` contains no raw secret.
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — infra-private content stays
      in `ose-infra` only and is NEVER cross-routed into `ose-public`/`ose-primer`
      — acceptance: no infra-private content appears in this repo's routed output.
- [ ] [AI] **Code-routing rule**: if a learning's home is `apps/`, `libs/`, or tests, file it as a
      separate `plans/backlog/` plan — NEVER land it inline in this plan's commits/PR. The sole
      carve-out is a bug/lint/test failure that blocks THIS plan's own scope — that is fixed inline as
      ordinary Root Cause Orientation work, not routed as a deferred learning.
      — acceptance: every code-homed learning has a corresponding `plans/backlog/` folder, or none
      exists.
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing
      matrix; in particular, evaluate recommending a **standing tri-repo rhino-cli src-diff gate** as
      a follow-up idea in `plans/ideas.md`
      — acceptance: `learnings.md`'s Triage log records the terminal state (routed / filed / discarded)
      of every entry.
- [ ] [AI] If no generalizable learning surfaced beyond the routed entries, record the explicit escape
      in `learnings.md`: `No generalizable learnings — <one-line reason>`
      — acceptance: `learnings.md`'s Triage log is never silently empty.

### Archival-in-PR

- [ ] [AI] Archive this plan folder in `ose-public` (the only repo that carries it):
      `git mv plans/in-progress/rhino-cli-source-drift-reconciliation plans/done/2026-07-17__rhino-cli-source-drift-reconciliation`
      and commit inside the same PR
      — acceptance: plan folder now under `plans/done/`; committed within the `ose-public` PR before merge.

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] `grep -A5 "## Triage log" plans/done/2026-07-17__rhino-cli-source-drift-reconciliation/learnings.md`
      (path after the archival move) — acceptance: shows completed entries; no
      `_(to be completed)_` placeholder remains.
- [ ] [AI] From the `ose-public` worktree: `gh pr view rhino-cli-source-drift-reconciliation --json files --jq '.files[].path'`
      — acceptance: the output includes a path under
      `plans/done/2026-07-17__rhino-cli-source-drift-reconciliation/` (archival committed inside the
      PR, not as a separate post-merge commit).

> **Pause Safety**: Safe to stop once the archival + triage commits are pushed to the PR branch.
> Recovery: `gh pr view` to confirm the archival commit is present.

## Phase 6: Merge + post-merge verification

- [ ] [HUMAN] Merge each PR once its CI is green and its review cycle is complete (maintainer's own
      schedule; AI-merge only if the maintainer explicitly authorizes it for this plan)
      — acceptance: all three PRs merged; each repo's `main` CI green.
- [ ] [AI] Post-merge: re-run the tri-repo boundary `diff` against the merged `main` of all three
      (command in [tech-docs.md](./tech-docs.md#tri-repo-verification-command-canonical))
      — acceptance: zero differences on merged `main`; the e2e-detector plan's identical-base
      precondition is satisfied.

### Phase 6 Gate

> All checks below must pass — this gate is the plan's completion boundary.

- [ ] [AI] Per repo: `gh pr view rhino-cli-source-drift-reconciliation --json state --jq .state`
      — acceptance: prints `MERGED` for all three repos.
- [ ] [AI] Re-run the post-merge tri-repo `diff` from
      [tech-docs.md § Tri-repo verification command](./tech-docs.md#tri-repo-verification-command-canonical)
      against each repo's `main` — acceptance: zero output (byte-identity confirmed on merged `main`).

> **Pause Safety**: Merge is `[HUMAN]`-paced — safe to stop indefinitely with green PRs awaiting
> merge. Recovery: `gh pr status` per repo.

## Worktree teardown

- [ ] [AI] After all three PRs merged, remove each worktree per repo:
      `git worktree remove worktrees/rhino-cli-source-drift-reconciliation && git branch -d rhino-cli-source-drift-reconciliation`
      — acceptance: worktrees removed in all three repos.
