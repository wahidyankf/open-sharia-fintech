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

**DAG**: see [tech-docs §5](./tech-docs.md#5-delivery-dag). Phase 1 blocks Phase 1b, and **Phase 1b
blocks Phases 2 through 5** — canonical `apps/rhino-cli` must be de-forked before any repo copies it.
Phases 2, 3, 4, 5 are mutually independent. Phase 6 is terminal.

**Target state is authored, not derived.** Phases 2 through 5 copy from
[`repo-configs/`](./repo-configs/README.md), [`husky-hooks/`](./husky-hooks/README.md), and
[`package-json/`](./package-json/README.md) and verify by diff. An acceptance clause reading "diffs
clean against the authored artifact" is falsifiable; "the registry is correct" is not.

## Worktree Specification

| Phase | Worktree                         | Branch                         | Repo          |
| ----- | -------------------------------- | ------------------------------ | ------------- |
| 0     | none (primary checkout)          | `main`                         | all four      |
| 1     | `worktrees/gate-engine/`         | `gate-registry/engine`         | `ose-public`  |
| 1b    | `worktrees/gate-defork/`         | `gate-registry/defork`         | `ose-public`  |
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
      — acceptance: the list is written into this checklist. In `ose-public` this returned
      `["Quality gate"]` on 2026-08-02 — a single context, matching the `quality-gate` join job's
      `name:`, which this plan keeps. Phase 6 verifies it is unchanged; no re-pointing is expected.
- [ ] [AI] Record the byte-identity baseline across all four repos — acceptance: `diff -rq` output
      over `apps/rhino-cli/{src,tests}` and the gherkin tree is written into this checklist for every
      pair. The 2026-08-02 audit found `sync_validator.rs` differing in `ose-public` and nine source
      files differing in `beaver-nest`; re-verify rather than assume, since these repos are edited
      concurrently by other actors.
- [ ] [AI] Record the tracked-file counts per language per repo that drive formatter pruning —
      `git ls-files` by extension — acceptance: the counts in
      [tech-docs §2.2.4](./tech-docs.md#224-the-full-formatter-and-per-file-inventory) still hold, or
      the table is amended in the same commit. A language gaining its first file changes which
      formatters a repo must declare.

### Phase 0 Gate

Green baseline in all four repos, audit table re-verified, required-status-check names recorded,
byte-identity baseline captured, per-language file counts confirmed. Do not start Phase 1 until all
hold.

---

## Phase 1 — Gate Engine (`ose-public`, PR #1)

Delivery unit: the registry schema and the `gate` command family, with nothing wired to it yet. The
engine ships inert — no hook or workflow changes — so this PR is independently shippable and
reversible.

Every code step below uses the RED / GREEN / REFACTOR template.

### 1.1 Registry schema in `repo-config.yml`

- [ ] [AI] **RED** — add a failing test at
      `apps/rhino-cli/tests/repo_config_data_driven.rs` asserting that a `gates:` section
      deserializes into a `Vec<GateEntry>` with `id`, `type`, `command`, `kind`, `surfaces` —
      command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test repo_config_data_driven`
      — acceptance: fails with a missing-field or unknown-variant error naming `gates`. Confirm it
      fails _for that reason_, not a compile error unrelated to the new field.
- [ ] [AI] **GREEN** — add the `gates` field and the `GateEntry` / `SurfaceScope` types to the
      `repo-config` domain model, per the field contract in
      [tech-docs §2.2](./tech-docs.md#22-registry-location-and-shape) — command: same as RED —
      acceptance: exits 0.
- [ ] [AI] **REFACTOR** — enum values for `type`, `kind`, `wiring`, `carve-out`, surface name, and
      `scope` are `#[serde(rename_all)]` strict variants with deny-unknown-fields, so a typo fails
      rather than defaulting — acceptance: a test asserting `scope: sometimes` is rejected exits 0,
      and the rejection message names the allowed values. Same for `type: cleanup`.
- [ ] [AI] Enforce the field-applicability rules from the contract table: `wiring` and `carve-out`
      are valid only on `type: check`; `restages` only on `type: mutation` — acceptance: three tests,
      one per misapplication, each asserting non-zero exit with a message naming the field and the
      type it does not apply to. Verify the inverse: correctly-applied fields exit 0.
- [ ] [AI] Extend `rhino-cli repo-config validate` to reject duplicate gate ids and a gate with an
      empty `surfaces` map — acceptance: two tests, one per condition, each asserting a non-zero exit
      and a message naming the offending id; both pass. Verify the inverse too: a registry with
      unique ids and non-empty surfaces exits 0.

### 1.2 `gate list`

- [ ] [AI] **RED** — failing test: `gate list --surface=ci --format=json` returns only the gates
      declaring the `ci` surface, each carrying `id`, `type`, `command`, `scope` — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::list` — acceptance: fails
      because the command does not exist.
- [ ] [AI] **GREEN** — implement `gate list` and wire it into `cli.rs` — acceptance: same command
      exits 0; `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate list --surface=ci --format=json | jq -e 'type == "array"'`
      exits 0.
- [ ] [AI] **REFACTOR** — a surface with no declared gates returns `[]` and exit 0, not an error —
      acceptance: `... -- gate list --surface=cron --format=json` on a registry with no cron gates
      prints `[]` and exits 0.
- [ ] [AI] `--format=json` omits `wiring: hand-wired` gates from the projection, so they never
      produce a CI matrix row — acceptance: a test asserting `test-quick` is absent from
      `gate list --surface=ci --format=json` exits 0, **and** a test asserting it is present in
      `--format=text` exits 0. Both directions required.

### 1.2a `git lockfile sync`

The lockfile-sync step is inline shell in `.husky/pre-commit` today and cannot be declared until it
is a real command. See [tech-docs §2.2.1](./tech-docs.md#221-why-mutations-are-in-the-registry).

- [ ] [AI] **RED** — failing test: given a staged `apps/<x>/package.json`, the command regenerates and
      stages `apps/<x>/package-lock.json` — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib git::lockfile` — acceptance: fails
      because the command does not exist.
- [ ] [AI] **GREEN** — implement `rhino-cli git lockfile sync`, porting the hook's existing logic
      verbatim — acceptance: same command exits 0.
- [ ] [AI] **REFACTOR** — no-op cleanly when no `package.json` is staged — acceptance: a test
      asserting exit 0 with no git index mutation passes.

### 1.2b `gate emit`

- [ ] [AI] **RED** — failing test: `gate emit --surface=pre-commit` writes a `lint-staged` block
      matching the registry's per-file gates — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::emit` — acceptance: fails
      because the command does not exist.
- [ ] [AI] **GREEN** — implement `gate emit --surface=pre-commit` — acceptance: same command exits 0.
- [ ] [AI] **REFACTOR** — the emitter is **marker-first**: it locates the already-applied marker
      before the anchor, so a re-run replaces rather than appends — acceptance: a test running the
      emitter twice asserts the second result is byte-identical to the first **and** that the block
      appears exactly once. A test that only checks byte-equality would pass on a duplicated block if
      both runs duplicated identically, so the occurrence count is required.

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

- [ ] [AI] **RED** — failing tests for all six checks in
      [tech-docs §2.4](./tech-docs.md#24-command-surface): composition-rule violation, missing
      surface shim, undeclared CI command, orphan gate id, stale emitted artifact, and a formatter
      mutation with no `verifies`-linked check — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib gate::validate` — acceptance: fails
      because the command does not exist.
- [ ] [AI] **GREEN** — implement `gate validate` — acceptance: same command exits 0.
- [ ] [AI] **REFACTOR** — the composition-rule check applies to `type: check` only, and
      `carve-out: staged-only` exempts a check from it — acceptance: four tests, all required
      because each covers a direction the others do not: a `type: mutation` gate with `pre-commit`
      only **passes**; a `carve-out: staged-only` check with `pre-commit` only **passes**; an
      unmarked `type: check` with `pre-commit` only **fails**; and `gate list` reports the
      exemption. A one-direction test set would pass on a validator that never fires.
- [ ] [AI] Implement check 3's `wiring` split — acceptance: a test asserting a `hand-wired` gate with
      a matching workflow job **passes**, and a test asserting the same gate with its job deleted
      **fails**, both exit 0.

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

`gate list`, `gate run`, `gate emit`, `gate validate`, and `git lockfile sync` exist and are tested;
**no surface is wired to them yet**;
`nx run rhino-cli:test:quick` green; PR merged.

**Byte-identity window opens here.** `apps/rhino-cli` in `ose-public` now differs from every other
repo. Phase 1b widens the window further before closing it — do **not** start Phases 3, 4 or 5 from
this gate, only from the Phase 1b gate. Copying canonical now would propagate the hardcoded app names
Phase 1b exists to remove.

---

## Phase 1b — De-fork Canonical Source and Add the Parity Manifest (`ose-public`, PR #1b)

Delivery unit: `apps/rhino-cli`'s canonical source contains no repository's app names, the dead
pre-commit pipeline is gone, `beaver-nest`'s two improvements are upstreamed, and a checksum manifest
plus its gate exist. Independently shippable: after this PR, canonical is copyable to any repo
without carrying `ose-public`-specific data into it.

**This phase blocks Phases 2, 3, 4, and 5.** Copying a canonical that still hardcodes `ose-public`'s
app names would either recreate `beaver-nest`'s fork or delete capabilities it depends on. See
[tech-docs §2.8.5](./tech-docs.md#285-convergence-sequence--upstream-before-downstream).

### 1b.1 Delete the dead pre-commit pipeline

Blast radius is seven sites — [tech-docs §2.8.2](./tech-docs.md#282-the-dead-pre-commit-pipeline).

- [ ] [AI] **RED** — prove the pipeline is unreachable before deleting it: assert that no CLI
      subcommand dispatches to `commands/git_pre_commit.rs` — acceptance:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- --help > /tmp/help-before.txt`
      succeeds, and `/usr/bin/grep -rn "git_pre_commit" apps/rhino-cli/src/cli.rs` returns no match.
      Record `help-before.txt`; it is the acceptance oracle for the deletion.
- [ ] [AI] **GREEN** — delete `application/git/pre_commit.rs` and `commands/git_pre_commit.rs`;
      remove `pub mod git_pre_commit;` from `commands.rs`; remove
      `pub use crate::application::git::pre_commit::{Deps, run};` from `internal/git.rs`; re-home or
      remove `infrastructure/git/mod.rs`'s `Deps` implementation; delete
      `domain/git/staged_files.rs` once orphaned; update the stale reference in
      `application/fs/mock.rs` — acceptance: `cargo build --release` exits 0,
      `nx run rhino-cli:test:quick` exits 0, and `rhino-cli --help` output is **byte-identical** to
      `help-before.txt` (`diff` exits 0). A changed help surface means the code was not dead.
- [ ] [AI] **REFACTOR** — confirm the largest hardcoded-paths site is gone — acceptance:
      `/usr/bin/grep -rn "ayokoding" apps/rhino-cli/src/` returns no match. Verify the inverse holds
      pre-edit: the same command returns matches before the deletion.

### 1b.2 Extract repo-specific data into `repo-config.yml`

- [ ] [AI] Move `WEBSITE_APP_PREFIXES` (`frontmatter_audit.rs`) into the registry as `args.exclude`
      on the gate that consumes it — acceptance: the const no longer exists
      (`/usr/bin/grep -c "WEBSITE_APP_PREFIXES" apps/rhino-cli/src/` returns 0) and
      `md frontmatter validate` still skips those trees, proven by a fixture under one of them that
      would otherwise fail.
- [ ] [AI] Move the Amazon Q agent-definition name out of `bindings.rs` into the existing `harness`
      section — acceptance: `/usr/bin/grep -c "ose-default" apps/rhino-cli/src/` returns 0, and
      `harness bindings generate` still writes `.amazonq/cli-agents/ose-default.json` in `ose-public`
      because the **config** now says so.
- [ ] [AI] Replace real-repo app names in test fixtures with synthetic names in
      `domain_coverage/mod.rs`, `specs_validate_counts.rs`, and `specs_coverage.rs` — acceptance:
      `/usr/bin/grep -rn "organiclever\|ose-be\|ose-www\|wahidyankf" apps/rhino-cli/src/` returns no
      match, and the test suite still passes. Fixtures must name no real repository's apps, so the
      same source compiles and passes in all four repos.
- [ ] [AI] Genericize the `apps/ose-be/global.json` doc comment in `doctor/tools.rs` — acceptance:
      covered by the grep clause above.

### 1b.3 Upstream `beaver-nest`'s improvements

Direction matters: these flow **up** into canonical before any repo copies canonical **down**.

- [ ] [AI] **RED** — add a failing test asserting `ROADMAP.md` and `SECURITY.md` are exempt from
      `md naming validate` — command:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib docs::naming` — acceptance: fails
      on canonical, which currently exempts neither.
- [ ] [AI] **GREEN** — add both basenames to `is_naming_exempt`'s always-exempt list in `naming.rs`,
      matching `beaver-nest`'s implementation — acceptance: the same test passes, and
      `md naming validate` exits 0 on a `ROADMAP.md` fixture.
- [ ] [AI] Port `beaver-nest`'s corrected `frontmatter_audit.rs` test and the `specs_coverage.rs`
      comment explaining why the misleading integration test was removed — acceptance: the test
      suite passes and the two files no longer differ from `beaver-nest`'s.

### 1b.4 Close the live three-repo violation

- [ ] [AI] Adopt `zai-coding-plan/wrong` in `sync_validator.rs`'s
      `validate_agent_equivalence_fails_on_model_mismatch` fixture, matching `ose-primer` and
      `ose-private` — acceptance:
      `diff <(git show HEAD:apps/rhino-cli/src/application/agents/sync_validator.rs) apps/rhino-cli/src/application/agents/sync_validator.rs`
      shows exactly one changed line, and the model-mismatch test still **fails** on a mismatched
      model (verify by temporarily supplying a matching model and observing the test fail to fire).

### 1b.5 Parity manifest and its gate

- [ ] [AI] **RED** — failing tests for `parity manifest generate` and `parity manifest validate` —
      command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib parity` — acceptance:
      fails because the commands do not exist.
- [ ] [AI] **GREEN** — implement both. The boundary set is `apps/rhino-cli/src/**`,
      `apps/rhino-cli/tests/**`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, and
      `specs/apps/rhino/behavior/rhino-cli/gherkin/**`, enumerated via `git ls-files` so untracked
      files cannot enter — acceptance: same command exits 0.
- [ ] [AI] **REFACTOR** — four properties, each needing its own test because each covers a direction
      the others do not: generation is idempotent (second run byte-identical); an edit to a `src/`
      file fails validation; an edit to a `tests/` file **also** fails validation; and an untracked
      file under `tests/fixtures/` is absent from the manifest and does not fail validation —
      acceptance: all four pass. The untracked case is not hypothetical: `ose-public`'s tree carries
      two untracked `.env` fixtures today, which must never be read, hashed, or listed.
- [ ] [AI] Write the failure message per
      [tech-docs §2.8.4](./tech-docs.md#284-enforcement--a-hermetic-gate-plus-a-non-hermetic-audit) —
      acceptance: the message names the file, states it is byte-identical across all four repos, and
      names `parity manifest generate` as the deliberate remedy.
- [ ] [AI] Declare the `parity-manifest` gate on `pre-push` and `ci`, and **confirm the generator is
      absent from every surface** — acceptance:
      `... -- gate list --format=json | jq -e '[.[] | select(.command=="parity manifest generate")] | length == 0'`
      exits 0. Verify the inverse: adding it to `pre-commit` makes that same command return false.
- [ ] [AI] Generate the manifest and commit it — acceptance:
      `... -- parity manifest validate` exits 0, and re-running `generate` leaves the file unchanged.

### 1b.6 Land

- [ ] [AI] Commit with scope `rhino-cli`; harness mirrors ride the same commit — acceptance:
      `npm run validate:sync` exits 0 and `git status --porcelain` is empty after commit.
- [ ] [AI] Push, open the PR, run the PR-Review Maker to Fixer Cycle, merge.

### Phase 1b Gate

Canonical `apps/rhino-cli` contains no repository's app names; `rhino-cli --help` is unchanged from
the Phase 1 baseline; `ROADMAP.md`/`SECURITY.md` are exempt in canonical; `parity manifest validate`
exits 0; `nx run rhino-cli:test:quick` green; PR merged.

**Only now may any repo copy canonical.** Phases 2 through 5 unblock here, not at Phase 1.

---

## Phase 2 — Rewire and Retire `main-ci` (`ose-public`, PR #2)

Delivery unit: `ose-public`'s four surfaces derive from the registry, `main-ci.yml` is gone, and the
documents agree. Independently shippable — the other repos are untouched.

### 2.1 Populate the registry

- [ ] [AI] Copy the `gates:` section from
      [`repo-configs/repo-config-ose-public.yml`](./repo-configs/repo-config-ose-public.yml) into
      `repo-config.yml`. The target state is authored in this plan, not derived at execution time —
      acceptance:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- repo-config validate`
      exits 0, and `diff <(yq '.gates' repo-config.yml) <(yq '.gates' <plan>/repo-configs/repo-config-ose-public.yml)`
      is empty.
- [ ] [AI] Confirm the registry covers every row of the audit table in
      [tech-docs §1](./tech-docs.md#1-audit-baseline--what-actually-runs-today), with each check's
      current excludes preserved verbatim in `args.exclude` — acceptance: every audit-table command
      appears in `... -- gate list --format=json`, checked row by row with a per-row verdict rather
      than a single count comparison. A count match can hide one missing check offsetting one extra.
- [ ] [AI] Prune the five formatter entries `ose-public` declares for languages it does not track
      (Go, Elixir, C#, Clojure, Dart) — acceptance:
      `... -- gate list --format=json | jq -e '[.[] | select(.category=="formatter")] | length == 9'`
      exits 0, and every surviving formatter's glob matches at least one path in `git ls-files`.
      Verify the inverse: the pre-edit registry fails that same glob-coverage check for exactly five
      entries.
- [ ] [AI] Verify the emitted `lint-staged` block matches the authored target — acceptance:
      `... -- gate emit --surface=pre-commit` then
      `diff <(jq '."lint-staged"' package.json) <plan>/package-json/lint-staged-ose-public.json`
      is empty. This is the falsifiable test of the emitter, and it is a diff, not a judgement.
- [ ] [AI] Verify the rewritten hooks match the authored targets — acceptance: each of
      `.husky/{commit-msg,pre-commit,pre-push}` diffs clean against
      `<plan>/husky-hooks/<hook>-ose-public.sh`.
- [ ] [AI] Declare `md-mermaid`, `md-heading-hierarchy`, and the structural specs validator on the
      `ci` surface — acceptance:
      `... -- gate list --surface=ci --format=json | jq -e '[.[].id] | index("md-mermaid") != null and index("md-heading-hierarchy") != null'`
      exits 0. Verify the inverse holds before the edit: the same command returns false on the
      pre-edit registry.
- [ ] [AI] Declare `harness-bindings` on the `ci` surface (closes R-6) — acceptance:
      `... -- gate list --surface=ci --format=json | jq -e '[.[].id] | index("harness-bindings") != null'`
      exits 0.
- [ ] [AI] Declare **every** formatter in
      [tech-docs §2.2.4](./tech-docs.md#224-the-full-formatter-and-per-file-inventory) as
      `type: mutation` on `pre-commit`, each paired with a `format-verify-*` `type: check` on `ci`
      only, linked by `verifies` (closes R-7) — acceptance:
      `... -- gate list --format=json | jq -e '[.[] | select(.type=="mutation" and .category=="formatter") | .id] - [.[] | select(.verifies) | .verifies] | length == 0'`
      exits 0 (no formatter lacks a verifier), and `... -- gate validate` exits 0. Verify the inverse
      before the edit: deleting one `verifies` field makes both non-zero. **Not** a single
      `format-verify` — one `prettier --check` leaves thirteen languages unverified.
- [ ] [AI] Build the two verify commands that need more than a flag — wrap `gofmt -l` so non-empty
      output fails, and add a check mode to `scripts/format-elixir.sh` (or call
      `mix format --check-formatted` directly) — acceptance: each exits non-zero on a deliberately
      unformatted fixture and 0 on a formatted one.
- [ ] [AI] Declare the remaining mutations — `harness-bindings-generate` and `lockfile-sync` — and
      the two surface-unique checks `env-staged-guard` (`carve-out: staged-only`) and `commitlint`
      (surface `commit-msg`) — acceptance: `... -- gate list --format=json | jq -e '[.[].id] | contains(["harness-bindings-generate","lockfile-sync","env-staged-guard","commitlint"])'`
      exits 0. This is the step that makes the registry a complete source of truth: after it, nothing
      any surface does lives outside `gates:`.
- [ ] [AI] Confirm `deps:audit` is **absent** from the registry — acceptance:
      `... -- gate list --format=json | jq -e '[.[] | select(.command=="deps:audit")] | length == 0'`
      exits 0. It is excluded by decision, not oversight; see
      [tech-docs §2.2.3](./tech-docs.md#223-what-is-deliberately-outside-the-registry).
- [ ] [AI] Declare `test-quick` and `compat-min-version` with `wiring: hand-wired` — acceptance:
      `... -- gate list --surface=ci --format=json | jq -e '[.[].id] | index("test-quick") == null'`
      exits 0 (absent from the matrix) **and** `... -- gate list --format=text` names it (present in
      the registry).

### 2.1a Dependency-audit workflow and its naming-convention amendment

Ordered — the convention must permit the name before the file can legally carry it.

- [ ] [AI] Amend `repo-governance/development/infra/github-actions-workflow-naming.md`: add
      `dependency` to the cross-cutting `{domain}` list and `audit` to the verb-and-qualifier
      vocabulary — acceptance:
      `grep -c 'dependency' repo-governance/development/infra/github-actions-workflow-naming.md`
      returns at least 1 in the domain table, and the same for `audit` in the vocabulary table; both
      returned 0 in those tables before the edit.
- [ ] [AI] Register the cross-cutting workflow set in that convention's Cross-cutting workflows
      table: add `dependency-vulnerability-audit.yml`, remove `main-ci.yml` — acceptance: the table
      lists `pr-quality-gate.yml`, `validate-env.yml`, and the new workflow, and
      `grep -c 'main-ci' repo-governance/development/infra/github-actions-workflow-naming.md`
      returns 0.
- [ ] [AI] Create `.github/workflows/dependency-vulnerability-audit.yml` with
      `name: Dependency Vulnerability Audit`, carrying over the existing `schedule` cron and
      `workflow_dispatch` triggers and the `nx run-many --all -t deps:audit` step verbatim, plus this
      repo's existing toolchain setup actions — acceptance: `actionlint .github/workflows/dependency-vulnerability-audit.yml`
      exits 0.
- [ ] [AI] Verify the name derives to the filename mechanically per the convention:
      `Dependency Vulnerability Audit` → lowercase → spaces to hyphens →
      `dependency-vulnerability-audit` → `.yml` — acceptance: derived string equals the filename
      exactly. This is the check `ose-primer` fails today with `Nightly Dependency Audit` in
      `deps-audit.yml`.
- [ ] [AI] `git rm .github/workflows/deps-audit.yml` — acceptance:
      `test ! -f .github/workflows/deps-audit.yml` and
      `test -f .github/workflows/dependency-vulnerability-audit.yml`. Do not delete before the
      replacement exists and lints — a window with neither workflow present means an unaudited night.
- [ ] [AI] Update `.github/workflows/README.md`: replace the `deps-audit.yml` row, drop the
      `main-ci.yml` row — acceptance: `grep -c 'deps-audit' .github/workflows/README.md` returns 0
      and `grep -c 'dependency-vulnerability-audit' .github/workflows/README.md` returns at least 1.

### 2.2 Rewire the hooks

- [ ] [AI] Run `... -- gate emit --surface=pre-commit` to generate the `lint-staged` block in
      `package.json` from the registry — acceptance: `git diff --stat package.json` shows the block
      changed; `... -- gate validate` reports the emitted artifact fresh; running the emitter a
      second time leaves `package.json` byte-identical and the block present exactly once.
- [ ] [AI] Replace the check list in `.husky/pre-commit` with `gate run --surface=pre-commit`, which
      now drives the mutations too (they are declared, so the hook no longer names them) —
      acceptance: `bash .husky/pre-commit` on a staged no-op exits 0; and
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
- [ ] [AI] Update the `quality-gate` join job's `needs:` to depend on the matrix job, removing the 18
      hand-listed job names it replaces. **This is the real hazard of the rewire**, not the branch
      protection: the join job is `if: always()` and fails only on
      `contains(needs.*.result, 'failure')`, so a `needs:` list that omits the matrix job reports
      green while checking nothing — acceptance: `actionlint` exits 0; a deliberately failing matrix
      entry turns `quality-gate` red in a scratch run; and the inverse, that removing the matrix job
      from `needs:` leaves `quality-gate` green despite that same failing entry, is demonstrated once
      and reverted. Keep the job's `name: Quality gate` **byte-identical** — see the Phase 6
      verification.

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
- [ ] [AI] Copy `apps/rhino-cli` from the merged `ose-public` **Phase 1b** result — acceptance:
      `src/`, `tests/`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`,
      `parity-manifest.sha256` and `specs/apps/rhino/behavior/rhino-cli/gherkin/` are byte-identical
      to `ose-public`, verified by `diff -r`, and `... -- parity manifest validate` exits 0 against
      the copied manifest without regenerating it. Copying from the Phase 1 result instead would
      reintroduce the hardcoded app names Phase 1b removed.
- [ ] [AI] Author `ose-primer`'s `gates:` section, preserving its own excludes (its `md links validate`
      carries the polyglot `deps`/`build`/`target` excludes) and adding its per-language gates —
      acceptance: `... -- repo-config validate` exits 0.
- [ ] [AI] Add the `shfmt -w` mutation and its `shfmt -d` verifier (8 tracked `.sh` files,
      `shellcheck`-ed but never formatted), and add prettier globs for the 46 tracked `.sql` and 3
      tracked `.html` files no glob currently covers — acceptance:
      `... -- gate list --format=json | jq -e '[.[].id] | index("format-shfmt") != null'` exits 0,
      and every tracked file extension in `git ls-files` that has a formatter in
      [tech-docs §2.2.4](./tech-docs.md#224-the-full-formatter-and-per-file-inventory) is matched by
      exactly one glob.
- [ ] [AI] Confirm no formatter is pruned here. `ose-primer` is the polyglot repo and is the **only**
      repo tracking Go, Elixir, C#, Clojure, and Dart — acceptance: every `category: formatter`
      gate's glob matches at least one path in `git ls-files`, with zero entries removed. The two
      formatters needing wrapper work — `gofmt` (prints paths, exits 0) and the Elixir script (no
      check mode) — are `ose-primer`-only, so that work lands here and nowhere else.
- [ ] [AI] Apply the same surface rewire as Phase 2 sections 2.2 through 2.4 — acceptance:
      `... -- gate validate` exits 0; `test ! -f .github/workflows/main-ci.yml`.
- [ ] [AI] Apply Phase 2 section 2.1a here: propagate the naming-convention amendment, create
      `dependency-vulnerability-audit.yml`, delete `deps-audit.yml`, update the workflows README —
      acceptance: `test ! -f .github/workflows/deps-audit.yml`; the new file's `name:` field matches
      `ose-public`'s byte-for-byte; `actionlint` exits 0. This repo is the one that also fixes a
      standing convention violation — it ships `name: Nightly Dependency Audit` inside a file named
      `deps-audit.yml`, which the `name:`-mirrors-filename rule forbids.
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
- [ ] [AI] Copy `apps/rhino-cli` from the merged `ose-public` **Phase 1b** result — acceptance:
      `diff -r` reports no difference across the byte-identity file set (now including `tests/` and
      `parity-manifest.sha256`), and `... -- parity manifest validate` exits 0 without regenerating.
- [ ] [AI] Author `ose-private`'s `gates:` section. It carries entries the others do not — the
      `iac-lint` pair (`./scripts/lint-terraform.sh`, `yamllint`) at pre-commit, pre-push, and CI —
      acceptance: `... -- repo-config validate` exits 0 and `... -- gate validate` exits 0, proving
      the schema tolerates a repo-specific entry set.
- [ ] [AI] Migrate the inline IaC formatting out of `.husky/pre-commit`. This repo formats terraform
      through a hand-written hook block rather than `lint-staged`, so `gate emit` reading the
      per-file registry would not reproduce it and the completeness claim would be false here on day
      one. Declare it as an ordinary `scope: affected-file-type, glob: "*.tf"` mutation with
      `category: formatter` plus its `format-verify-*` counterpart, then delete the inline block —
      acceptance: `grep -c 'fmt' .husky/pre-commit` returns 0, and
      `... -- gate list --surface=pre-commit --format=json | jq -e '[.[] | select(.surfaces."pre-commit".glob=="*.tf")] | length == 1'`
      exits 0. Verify the inverse first: the same `jq` returns false on the pre-edit registry.
- [ ] [AI] Add the `shfmt -w` mutation and its `shfmt -d` verifier (13 tracked `.sh` files,
      `shellcheck`-ed but never formatted) — acceptance:
      `... -- gate list --format=json | jq -e '[.[].id] | index("format-shfmt") != null'` exits 0.
- [ ] [AI] Prune the five formatter entries this repo declares for languages it does not track — F#,
      Python, C#, Clojure, Dart are all **zero** tracked files here — acceptance:
      `... -- gate list --format=json | jq -e '[.[] | select(.category=="formatter")] | length == 4'`
      exits 0 (prettier, rustfmt, shfmt, tofu — the four it actually needs).
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

## Phase 5 — `beaver-nest` Joins the Byte-Identity Boundary (PR #5)

Independent of Phases 2, 3, 4. Blocked by Phase 1b.

`beaver-nest` **stops being a fork**. Phase 1b removed the reason it was one: eight of its nine
source divergences were `ose-public`'s app names hardcoded into shared source, and the ninth — its
`ROADMAP.md`/`SECURITY.md` naming exemptions — is now in canonical. So this becomes a copy like
Phases 3 and 4, not a port. See
[tech-docs §2.8.6](./tech-docs.md#286-the-governance-change-this-requires) for the governance
amendment this depends on.

- [ ] [AI] Create the worktree; `npm install`; `npm run doctor -- --fix`.
- [ ] [AI] **Verify Phase 1b actually absorbed the fork before overwriting anything.** Diff the
      current `beaver-nest` source against merged canonical and confirm every remaining difference is
      one Phase 1b intended to erase — acceptance: `diff -rq` over the boundary set reports only
      files whose divergence is listed in
      [tech-docs §2.8.1](./tech-docs.md#281-audit-result), and **zero** unlisted differences. Any
      unlisted difference is an unmigrated capability: stop, upstream it into `ose-public` first, and
      re-run. This step is the guard against silently deleting work.
- [ ] [AI] Confirm the two upstreamed improvements are present in canonical **before** the copy —
      acceptance: `/usr/bin/grep -c 'ROADMAP.md' <canonical>/apps/rhino-cli/src/application/docs/naming.rs`
      returns a non-zero count, and the same for `SECURITY.md`. Copying without this check is what
      would delete them.
- [ ] [AI] Copy `apps/rhino-cli` from the merged `ose-public` Phase 1b result — acceptance: `diff -r`
      reports no difference across the boundary set, and `... -- parity manifest validate` exits 0
      without regenerating.
- [ ] [AI] Confirm `md naming validate` still passes on this repo's own `ROADMAP.md` and
      `SECURITY.md` after the copy — acceptance: the command exits 0. This is the falsifiable proof
      that the copy preserved the capability rather than reverting it.
- [ ] [AI] Author `beaver-nest`'s `gates:` section from
      [`repo-configs/repo-config-beaver-nest.yml`](./repo-configs/repo-config-beaver-nest.yml),
      which prunes the **nine** formatter entries this repo declares for languages it does not track
      (Go, Elixir, C#, Clojure, Dart, Lua, C, Bazel, Terraform) plus the `*.sql` prettier glob, which
      matches zero tracked files here — acceptance:
      `... -- repo-config validate` exits 0, and
      `... -- gate list --format=json | jq -e '[.[] | select(.category=="formatter")] | length == 5'`
      exits 0 (prettier, rustfmt, shfmt, fantomas, ruff — the five languages it actually tracks).
- [ ] [AI] Apply the surface rewire and `main-ci.yml` retirement — acceptance:
      `... -- gate validate` exits 0; `test ! -f .github/workflows/main-ci.yml`.
- [ ] [AI] Propagate the amended standard, the rewritten hook-lifecycle doc, the governance amendment
      removing the fork language, and this plan folder.
- [ ] [AI] Commit, push, PR, review cycle, CI green, merge, fast-forward local `main`.

### Phase 5 Gate

`gate validate` exits 0 in `beaver-nest`; `apps/rhino-cli` byte-identical to `ose-public`;
`parity manifest validate` exits 0; `md naming validate` passes on this repo's `ROADMAP.md` and
`SECURITY.md`; no document in any repo still calls `beaver-nest` a fork of `rhino-cli`; PR merged.

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
- [ ] [AI] Verify byte-identity across **all four** repos directly, not via the manifest —
      acceptance: `diff -r` over `apps/rhino-cli/{src,tests}`, `Cargo.toml`, `Cargo.lock`,
      `project.json`, `LICENSE`, `parity-manifest.sha256`, and
      `specs/apps/rhino/behavior/rhino-cli/gherkin/` reports **zero** differences for every pair, and
      the four `parity-manifest.sha256` files are byte-identical to one another. This is the
      independent check: the manifests agreeing with their own repos proves nothing about the repos
      agreeing with each other.
- [ ] [AI] Prove the parity gate fails on real drift: edit one boundary file in a scratch worktree,
      confirm `parity manifest validate` exits non-zero and names the file, then discard the scratch
      — acceptance: non-zero before discard, zero after.
- [ ] [AI] Confirm the cross-repo audit workflow runs and reports in each repo — acceptance:
      `gh workflow run rhino-cli-parity-audit.yml` succeeds in all four and each run concludes
      `success` against the converged state. Verify the inverse once in a scratch branch: a
      deliberately divergent manifest makes the audit conclude `failure`.
- [ ] [AI] Confirm no repo declares a formatter for a language it does not track — acceptance: for
      each repo, every `category: formatter` gate's glob matches at least one path in
      `git ls-files`, checked mechanically rather than by review.
- [ ] [AI] Verify branch protection still resolves, in every repo that has it —
      `gh api repos/wahidyankf/<repo>/branches/main/protection --jq '.required_status_checks.contexts'`
      — acceptance: the output equals the value Phase 0 recorded, and every context in it names a job
      that still exists in `pr-quality-gate.yml`. In `ose-public` the required set is the single
      context `"Quality gate"`, which is the `quality-gate` join job's `name:` — a job this plan
      keeps, so **the expected result is that nothing changed**. This step is read-only verification,
      not reconfiguration, which is why it is `[AI]` and why it sits at the end rather than gating a
      merge.
- [ ] [HUMAN] **Only if the step above fails**: update the required-status-check contexts in
      repository settings. Human-gated because it is a settings change outside the git tree, it is
      not covered by any PR review, and a wrong value silently unblocks every future merge. If the
      verification passes, this step is struck as not-applicable rather than performed.
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

## Settled Decisions

No open decisions remain. The one item previously carried as decided-with-recommendation is now
settled:

**`deps:audit` placement — settled 2026-08-02.** Excluded from the registry entirely, not declared
under a `cron` surface as the first draft proposed. It keeps its schedule and moves to its own
descriptively-named workflow, `dependency-vulnerability-audit.yml`. The `cron` surface is removed
from the schema; the registry covers the four gate surfaces and only those. Rationale in
[brd.md §A Standing Rule This Plan Upholds](./brd.md#a-standing-rule-this-plan-upholds) and
[tech-docs §2.2.3](./tech-docs.md#223-what-is-deliberately-outside-the-registry).
