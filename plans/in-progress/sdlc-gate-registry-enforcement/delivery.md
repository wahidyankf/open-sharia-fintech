---
title: "Delivery — SDLC Gate Registry Enforcement"
description: Phased, DAG-ordered execution checklist with worktree specs, phase gates, and PR boundaries
category: explanation
subcategory: plans
tags:
  - ci-cd
  - delivery
  - parity
created: 2026-08-02
---

# Delivery — SDLC Gate Registry Enforcement

**Delivery Mode**: `worktree-to-pr` — each change-producing DAG leaf gets its own worktree and its own
PR, strict 1-PR to 1-worktree. Every PR runs the PR-Review Maker to Fixer Cycle (default three
sequential CI-gated cycles) before merge. `[AI]` merges by default.

**Concurrency**: N=3 background agents plus the main thread as orchestrator.

**DAG**: see [tech-docs §5](./tech-docs.md#5-delivery-dag). Phase 1 blocks Phases 2 through 5. Phases
2, 3, 4, 5 are mutually independent. Phase 6 is terminal.

## Worktree Specification

| Phase | Worktree                         | Branch                         | Repo          |
| ----- | -------------------------------- | ------------------------------ | ------------- |
| 0     | none (primary checkout)          | `main`                         | all four      |
| 1     | `worktrees/gate-engine/`         | `gate-registry/engine`         | `ose-public`  |
| 2     | `worktrees/gate-rewire-public/`  | `gate-registry/rewire-public`  | `ose-public`  |
| 3     | `worktrees/gate-rewire-primer/`  | `gate-registry/rewire-primer`  | `ose-primer`  |
| 4     | `worktrees/gate-rewire-private/` | `gate-registry/rewire-private` | `ose-private` |
| 5     | `worktrees/gate-rewire-beaver/`  | `gate-registry/rewire-beaver`  | `beaver-nest` |
| 6     | `worktrees/gate-knowledge/`      | `gate-registry/knowledge`      | `ose-public`  |

After every `git worktree add`, run `npm install` and `npm run doctor -- --fix` before any other
command — see
[Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md).

Plan-document edits (this folder) are made on local `main` under the plan-docs-only carve-out;
execution-time tick marks go in the worktree copy.

---

## Phase 0 — Baseline Convergence

**Opens no PR.** Phase 0 evidence rides the Phase 1 PR.

- [ ] [AI] Run `npm install` then `npm run doctor -- --fix` in each of the four repos — acceptance:
      each exits 0; re-running `npm run doctor` reports no missing tool.
- [ ] [AI] Establish a green baseline in `ose-public`: `npx nx run-many --all -t test:quick` —
      acceptance: exits 0. If any project fails, fix it before Phase 1 (preexisting failures are in
      scope per Root Cause Orientation); record each fix in this checklist as a discovered task.
- [ ] [AI] Confirm every repo is clean and level with origin: for each repo,
      `git status --porcelain` produces no output and
      `git rev-list --left-right --count HEAD...origin/main` reports `0 0` — acceptance: both hold in
      all four. If a repo is dirty, the uncommitted work belongs to another actor: leave it untouched
      and record it here rather than staging it.
- [ ] [AI] Re-capture the audit table in [tech-docs §1](./tech-docs.md#1-audit-baseline--what-actually-runs-today)
      against current `main` in all four repos — acceptance: every row's verdict still holds, or the
      table is amended in the same commit with the row that changed and why.
- [ ] [AI] Record the branch-protection required-status-check names currently configured for each
      repo: `gh api repos/wahidyankf/<repo>/branches/main/protection --jq '.required_status_checks.contexts'`
      — acceptance: the list is written into this checklist. Phase 2 must re-point these before the
      matrix renames any job.

### Phase 0 Gate

Green baseline in all four repos, audit table re-verified, required-status-check names recorded.
Do not start Phase 1 until all four hold.

---

## Phase 1 — Gate Engine (`ose-public`, PR #1)

Delivery unit: the registry schema and the `gate` command family, with nothing wired to it yet. The
engine ships inert — no hook or workflow changes — so this PR is independently shippable and
reversible.

Every code step below uses the RED / GREEN / REFACTOR template.

### 1.1 Registry schema in `repo-config.yml`

- [ ] [AI] **RED** — add a failing test at
      `apps/rhino-cli/tests/repo_config_data_driven.rs` asserting that a `gates:` section
      deserializes into a `Vec<GateEntry>` with `id`, `command`, `kind`, `surfaces` —
      command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven`
      — acceptance: fails with a missing-field or unknown-variant error naming `gates`. Confirm it
      fails _for that reason_, not a compile error unrelated to the new field.
- [ ] [AI] **GREEN** — add the `gates` field and the `GateEntry` / `SurfaceScope` types to the
      `repo-config` domain model, per the field contract in
      [tech-docs §2.2](./tech-docs.md#22-registry-location-and-shape) — command: same as RED —
      acceptance: exits 0.
- [ ] [AI] **REFACTOR** — enum values for `kind`, surface name, and `scope` are `#[serde(rename_all)]`
      strict variants with deny-unknown-fields, so a typo fails rather than defaulting — acceptance:
      a test asserting `scope: sometimes` is rejected exits 0, and the rejection message names the
      allowed values.
- [ ] [AI] Extend `rhino-cli repo-config validate` to reject duplicate gate ids and a gate with an
      empty `surfaces` map — acceptance: two tests, one per condition, each asserting a non-zero exit
      and a message naming the offending id; both pass. Verify the inverse too: a registry with
      unique ids and non-empty surfaces exits 0.

### 1.2 `gate list`

- [ ] [AI] **RED** — failing test: `gate list --surface=ci --format=json` returns only the gates
      declaring the `ci` surface, each carrying `id`, `command`, `scope` — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::list` — acceptance: fails
      because the command does not exist.
- [ ] [AI] **GREEN** — implement `gate list` and wire it into `cli.rs` — acceptance: same command
      exits 0; `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate list --surface=ci --format=json | jq -e 'type == "array"'`
      exits 0.
- [ ] [AI] **REFACTOR** — a surface with no declared gates returns `[]` and exit 0, not an error —
      acceptance: `... -- gate list --surface=cron --format=json` on a registry with no cron gates
      prints `[]` and exits 0.

### 1.3 `gate run`

- [ ] [AI] **RED** — failing tests for: declaration-order execution, stop-at-first-failure, and
      path-gated skip-when-untouched / run-when-touched — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::run` — acceptance: fails
      because the command does not exist.
- [ ] [AI] **GREEN** — implement `gate run --surface=<name> [--only=<id>]` — acceptance: same command
      exits 0.
- [ ] [AI] **REFACTOR** — resolve `repo-config.yml` and all exclude paths from
      `git rev-parse --show-toplevel`, never the main checkout; never call
      `git rev-parse --is-bare-repository` — acceptance: a regression test that runs `gate run` from a
      synthetic linked worktree exits 0 and reads the worktree's own config; and
      `grep -rn "is-bare-repository" apps/rhino-cli/src/` returns no match.

### 1.4 `gate validate`

- [ ] [AI] **RED** — failing tests for all four checks in
      [tech-docs §2.4](./tech-docs.md#24-command-surface): composition-rule violation, missing
      surface shim, undeclared CI command, orphan gate id — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate` — acceptance: fails
      because the command does not exist.
- [ ] [AI] **GREEN** — implement `gate validate` — acceptance: same command exits 0.
- [ ] [AI] **REFACTOR** — the `carve-out: formatter` exemption is applied only to the
      composition-rule check, and `gate list` reports the exemption — acceptance: a test asserting a
      formatter-marked gate with `ci` only passes validation exits 0, **and** a test asserting an
      unmarked gate with `pre-commit` only _fails_ validation exits 0. Both directions must be
      covered; one alone is not a check.

### 1.5 Specs and coverage

- [ ] [AI] Author the Gherkin feature files under
      `specs/apps/rhino/behavior/rhino-cli/gherkin/` from the scenarios in
      [prd.md](./prd.md), with `@covers` markers — acceptance:
      `npx nx run rhino-cli:specs:behavior:coverage` exits 0.
- [ ] [AI] Verify structural specs and coverage floor — acceptance:
      `npx nx run rhino-cli:test:quick` exits 0 (this chains typecheck, lint, unit, coverage, specs).

### 1.6 Land

- [ ] [AI] Create the worktree per the table above, then `npm install` and `npm run doctor -- --fix`.
- [ ] [AI] Commit with scope `rhino-cli`; regenerated harness mirrors ride the **same** commit —
      acceptance: `npm run validate:sync` exits 0 and `git status --porcelain` is empty after commit.
- [ ] [AI] Push, open the PR, run the PR-Review Maker to Fixer Cycle — acceptance: all cycles
      complete, CI green.
- [ ] [AI] Merge.

### Phase 1 Gate

`gate list`, `gate run`, and `gate validate` exist and are tested; **no surface is wired to them yet**;
`nx run rhino-cli:test:quick` green; PR merged.

**Byte-identity window opens here.** `apps/rhino-cli` in `ose-public` now differs from `ose-primer`
and `ose-private`. Phases 3 and 4 close it and must start immediately after this gate.

---

## Phase 2 — Rewire and Retire `main-ci` (`ose-public`, PR #2)

Delivery unit: `ose-public`'s four surfaces derive from the registry, `main-ci.yml` is gone, and the
documents agree. Independently shippable — the other repos are untouched.

### 2.1 Populate the registry

- [ ] [AI] Write the `gates:` section of `repo-config.yml` covering every row of the audit table in
      [tech-docs §1](./tech-docs.md#1-audit-baseline--what-actually-runs-today), preserving each
      check's current excludes verbatim into `args.exclude` — acceptance:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- repo-config validate`
      exits 0, and `... -- gate list --format=json | jq 'length'` equals the audit table's check
      count.
- [ ] [AI] Declare `md-mermaid`, `md-heading-hierarchy`, and the structural specs validator on the
      `ci` surface — acceptance:
      `... -- gate list --surface=ci --format=json | jq -e '[.[].id] | index("md-mermaid") != null and index("md-heading-hierarchy") != null'`
      exits 0. Verify the inverse holds before the edit: the same command returns false on the
      pre-edit registry.
- [ ] [AI] Declare `harness-bindings` on the `ci` surface (closes R-6) — acceptance:
      `... -- gate list --surface=ci --format=json | jq -e '[.[].id] | index("harness-bindings") != null'`
      exits 0.
- [ ] [AI] Declare `format-verify` on the `ci` surface with `carve-out: formatter` (closes R-7) —
      acceptance: `... -- gate list --surface=ci --format=json | jq -e '[.[] | select(.id=="format-verify")] | length == 1'`
      exits 0, and `... -- gate validate` exits 0 (the carve-out suppresses the composition-rule
      demand for a pre-commit counterpart).
- [ ] [AI] Declare `deps-audit` on the `cron` surface only (closes R-8) — acceptance:
      `... -- gate list --surface=pre-push --format=json | jq -e '[.[].id] | index("deps-audit") == null'`
      exits 0.

### 2.2 Rewire the hooks

- [ ] [AI] Replace the check list in `.husky/pre-commit` with `gate run --surface=pre-commit`,
      keeping the two non-check steps (harness bindings **generate**, lockfile sync) as explicit hook
      steps — acceptance: `bash .husky/pre-commit` on a staged no-op exits 0; and
      `grep -c 'gate run --surface=pre-commit' .husky/pre-commit` returns 1.
- [ ] [AI] Replace the check list in `.husky/pre-push` with `gate run --surface=pre-push` —
      acceptance: `grep -c 'gate run --surface=pre-push' .husky/pre-push` returns 1; and
      `grep -cE 'md links validate|md readme-index validate|harness duplication validate' .husky/pre-push`
      returns 0 (they now come from the registry, not the hook text).
- [ ] [AI] Verify no check was dropped in the move: compare
      `... -- gate list --surface=pre-push --format=json` against the pre-edit `.husky/pre-push`
      command list recorded in Phase 0 — acceptance: every pre-edit command appears in the registry
      projection; any deliberate omission is listed here with its reason.

### 2.3 Rewire the PR gate

- [ ] [AI] Replace the hand-listed check jobs in `.github/workflows/pr-quality-gate.yml` with the
      `enumerate` plus `gate` matrix from
      [tech-docs §2.5](./tech-docs.md#25-ci-wiring--matrix-not-a-single-job); keep the per-language
      `test:quick` jobs hand-written — acceptance: `actionlint .github/workflows/pr-quality-gate.yml`
      exits 0.
- [ ] [AI] Unpin the specs job (closes R-5): remove `--projects=rhino-cli` — acceptance:
      `grep -c -- '--projects=rhino-cli' .github/workflows/pr-quality-gate.yml` returns 0; it
      returned 1 before the edit.
- [ ] [AI] Remove `if: github.event_name == 'pull_request'` from the `format` job so the per-file
      pass also runs on push to `main`, and split it: auto-fix-and-commit on `pull_request`, verify-only
      on `push` — acceptance: `actionlint` exits 0; the `push` path runs `format-verify` and performs
      no `git push`.
- [ ] [AI] Update the `quality-gate` join job's `needs:` to depend on the matrix job — acceptance:
      `actionlint` exits 0; a deliberately failing matrix entry turns `quality-gate` red in a scratch
      run.
- [ ] [HUMAN] Re-point branch-protection required status checks to the `quality-gate` join job before
      merge, using the names recorded in Phase 0 — acceptance: `gh api` reports `quality-gate` in
      `required_status_checks.contexts`, and no removed job name remains. **Human-gated**: this is a
      repository-settings change outside the git tree, and a wrong value silently unblocks merges.

### 2.4 Retire `main-ci.yml`

Ordered — do not delete before the fold-in is verified.

- [ ] [AI] Confirm the fold-in landed: every command in `main-ci.yml` is either declared on the `ci`
      surface or deliberately dropped with a reason recorded here — acceptance: a per-command table
      appears in this checklist with a verdict for each; no command is unaccounted for.
- [ ] [AI] `git rm .github/workflows/main-ci.yml` — acceptance:
      `test ! -f .github/workflows/main-ci.yml`.
- [ ] [AI] Scrub references — acceptance: `grep -rn "main-ci" --exclude-dir=node_modules --exclude-dir=.nx --exclude-dir=.git .`
      returns matches only inside `plans/done/` (immutable history) and this plan folder.

### 2.5 Documents

- [ ] [AI] Amend `docs/reference/sdlc-gate-standard.md` per
      [tech-docs §3](./tech-docs.md#3-document-amendments) — acceptance:
      `grep -c 'pre-commit ∪ pre-push) == PR gate == main gate' docs/reference/sdlc-gate-standard.md`
      returns 0 and `grep -c 'pre-commit ∪ pre-push) == PR gate' docs/reference/sdlc-gate-standard.md`
      returns at least 1.
- [ ] [AI] Rewrite `repo-governance/development/workflow/git-hook-lifecycle.md` (closes R-9) —
      acceptance: `grep -c 'specs:coverage' repo-governance/development/workflow/git-hook-lifecycle.md`
      returns 0; it returned at least 1 before the edit. Its command tables are replaced by a pointer
      to `gate list` so the document cannot restale.
- [ ] [AI] Update `repo-governance/development/infra/nx-targets.md`,
      `docs/reference/system-architecture/ci-cd.md`, and the Git Hooks section of `AGENTS.md` —
      acceptance: `npx nx run rhino-cli:instruction-size:validation` exits 0 (the `AGENTS.md` edit
      must not push it over budget).
- [ ] [AI] Propagate the rule change through `repo-rules-maker` rather than hand-editing only the
      obvious files: sweep the convention registers, the checker agents, and the indexes, then
      re-sync bindings — acceptance: `npm run validate:sync` exits 0 and
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md readme-index validate`
      exits 0.

### 2.6 Land

- [ ] [AI] `... -- gate validate` exits 0 — this is the plan's central acceptance criterion.
- [ ] [AI] Commit, push, open the PR, run the PR-Review Maker to Fixer Cycle, verify CI green, merge.
- [ ] [AI] Fast-forward local `main` after the merge — acceptance:
      `git rev-list --left-right --count HEAD...origin/main` reports `0 0`.

### Phase 2 Gate

`gate validate` exits 0; `main-ci.yml` absent and unreferenced outside immutable history;
branch protection re-pointed; PR merged; local `main` fast-forwarded.

---

## Phase 3 — `ose-primer` (PR #3)

Independent of Phases 2, 4, 5. Closes half the byte-identity window.

- [ ] [AI] Create the worktree; `npm install`; `npm run doctor -- --fix`. Note: `ose-primer`'s
      polyglot demo apps need their language toolchains fetched before pre-push will pass in a fresh
      worktree.
- [ ] [AI] Copy `apps/rhino-cli` from the merged `ose-public` Phase 1 result — acceptance: `src/`,
      `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE` and
      `specs/apps/rhino/behavior/rhino-cli/gherkin/` are byte-identical to `ose-public`, verified by
      `diff -r`.
- [ ] [AI] Author `ose-primer`'s `gates:` section, preserving its own excludes (its `md links validate`
      carries the polyglot `deps`/`build`/`target` excludes) and adding its per-language gates —
      acceptance: `... -- repo-config validate` exits 0.
- [ ] [AI] Apply the same surface rewire as Phase 2 sections 2.2 through 2.4 — acceptance:
      `... -- gate validate` exits 0; `test ! -f .github/workflows/main-ci.yml`.
- [ ] [AI] Rename the dependency-audit workflow to the shared descriptive name agreed in Phase 2
      (`ose-primer` currently uses `Nightly Dependency Audit`, the others `deps-audit`) — acceptance:
      the `name:` field matches `ose-public`'s byte-for-byte.
- [ ] [AI] Propagate the amended `sdlc-gate-standard.md` and the rewritten `git-hook-lifecycle.md`
      — acceptance: `grep -c 'validate-markdown.yml' repo-governance/development/workflow/git-hook-lifecycle.md`
      returns 0 (this repo's copy cites that non-existent workflow today).
- [ ] [AI] Propagate this plan folder — acceptance: the folder exists at the same path in `ose-primer`.
- [ ] [AI] Commit, push, PR, review cycle, CI green, merge, fast-forward local `main`.

### Phase 3 Gate

`gate validate` exits 0 in `ose-primer`; `apps/rhino-cli` byte-identical to `ose-public`; PR merged.

---

## Phase 4 — `ose-private` (PR #4)

Independent of Phases 2, 3, 5. Closes the other half of the byte-identity window.

- [ ] [AI] Create the worktree; `npm install`; `npm run doctor -- --fix`.
- [ ] [AI] Copy `apps/rhino-cli` from the merged `ose-public` Phase 1 result — acceptance: `diff -r`
      reports no difference across the byte-identity file set.
- [ ] [AI] Author `ose-private`'s `gates:` section. It carries entries the others do not — the
      `iac-lint` pair (`./scripts/lint-terraform.sh`, `yamllint`) at pre-commit, pre-push, and CI —
      acceptance: `... -- repo-config validate` exits 0 and `... -- gate validate` exits 0, proving
      the schema tolerates a repo-specific entry set.
- [ ] [AI] Note the pre-existing local surplus: this repo's pre-push already runs
      `specs structure validate` and `npm run lint:md`, and its PR gate already has
      `markdown-per-file`. Fold these into registry declarations rather than deleting them —
      acceptance: every command present in the pre-edit `.husky/pre-push` appears in
      `... -- gate list --surface=pre-push --format=json`.
- [ ] [AI] Apply the surface rewire and `main-ci.yml` retirement — acceptance:
      `test ! -f .github/workflows/main-ci.yml`; `actionlint` exits 0.
- [ ] [AI] Create `repo-governance/development/workflow/git-hook-lifecycle.md`, which this repo lacks
      entirely — acceptance: the file exists and
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md readme-index validate`
      exits 0 (the new file must be indexed).
- [ ] [AI] Propagate the amended standard and this plan folder.
- [ ] [AI] Commit, push, PR, review cycle, CI green, merge, fast-forward local `main`.

### Phase 4 Gate

`gate validate` exits 0 in `ose-private`; `apps/rhino-cli` byte-identical across all three bound
repos — **the byte-identity window is now closed**; PR merged.

---

## Phase 5 — `beaver-nest` (PR #5)

Independent of Phases 2, 3, 4. `beaver-nest` carries a **fork** of `rhino-cli` and is outside the
byte-identity boundary, so this is a port, not a copy.

- [ ] [AI] Create the worktree; `npm install`; `npm run doctor -- --fix`.
- [ ] [AI] Port the gate engine into the fork, reconciling any fork-local divergence in the
      `repo-config` domain model — acceptance:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml` exits 0; record every reconciliation in
      [learnings.md](./learnings.md).
- [ ] [AI] Author `beaver-nest`'s `gates:` section — acceptance: `... -- repo-config validate` exits 0.
- [ ] [AI] Apply the surface rewire and `main-ci.yml` retirement — acceptance:
      `... -- gate validate` exits 0; `test ! -f .github/workflows/main-ci.yml`.
- [ ] [AI] Propagate the amended standard, the rewritten hook-lifecycle doc, and this plan folder.
- [ ] [AI] Commit, push, PR, review cycle, CI green, merge, fast-forward local `main`.

### Phase 5 Gate

`gate validate` exits 0 in `beaver-nest`; PR merged.

---

## Phase 6 — Knowledge Capture (`ose-public`, PR #6)

Terminal node. Blocked by Phases 2, 3, 4, and 5.

- [ ] [AI] Verify the end state across all four repos — acceptance: in each,
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate validate`
      exits 0 and `test ! -f .github/workflows/main-ci.yml`.
- [ ] [AI] Verify the composition rule now holds mechanically: introduce a scratch gate declaring
      `pre-commit` with no `ci` and no carve-out, confirm `gate validate` exits non-zero, then revert
      — acceptance: non-zero on the scratch state, zero after revert. A validator that never fails is
      not a validator.
- [ ] [AI] Triage [learnings.md](./learnings.md) — each entry gets a home in `docs/`,
      `repo-governance/`, or is discarded with a reason — acceptance: no untriaged entry remains.
- [ ] [AI] Remove all six worktrees and prune — acceptance: `git worktree list` shows only the
      primary checkout in each repo. Before removing any worktree, read its dirty diff: a merged PR
      does not imply an empty tree, and uncommitted evidence must be recovered to `main` first.
- [ ] [AI] Archive the plan: `git mv plans/in-progress/sdlc-gate-registry-enforcement/ plans/done/YYYY-MM-DD__sdlc-gate-registry-enforcement/`
      with the real completion date, in all four repos — acceptance: the folder exists under `done/`
      with a date prefix, and `plans/in-progress/README.md` no longer lists it.
- [ ] [AI] Update `plans/done/README.md` and `plans/in-progress/README.md` in all four repos —
      acceptance: `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done`
      exits 0.

### Phase 6 Gate

All four repos verified; the validator proven to fail on a real violation; worktrees removed; plan
archived in all four repos.

---

## Open Decision

One item is recorded as decided-with-recommendation rather than settled, and should be confirmed
before Phase 2 section 2.1:

**`deps:audit` placement.** This plan declares it on the `cron` surface only, preserving ratified
rule 3 (uncacheable and non-hermetic tiers never gate a push) while making it visible to the
registry. The alternative — declaring it on `ci` as well — would make a green commit turn red when
the advisory database moves, with no change to the repository. If a gating dependency audit is
wanted, say so and the plan adds `ci: { scope: all-projects }` to that one entry; the rest of the
plan is unaffected. Rationale in
[brd.md](./brd.md#a-standing-rule-this-plan-bends-and-why-it-does-not-break-it).
