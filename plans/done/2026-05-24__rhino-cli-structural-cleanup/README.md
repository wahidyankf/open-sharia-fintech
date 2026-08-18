# rhino-cli Structural Cleanup

**Status**: Not Started
**Project**: `apps/rhino-cli` [Repo-grounded]

## Context

`rhino-cli` was ported from Go to Rust in 2026-05. The port preserved Go's
structural idioms: `internal/` subdirectory, `mod.rs` files everywhere, a `gitutil`
utility module, and coverage output named `cover.out` (Go's convention). The port
also left dead code scaffolding for future parallelism, untracked `tests/cli/` and
`tests/cucumber/` directories (no tracked files), and a shared naming helper stranded
inside `commands/`.

This plan removes the Go-isms and corrects the structural inconsistencies identified
post-port, making the codebase idiomatic Rust 2024.

## Scope

### In Scope

- Remove dead code from `src/internal/git/mod.rs` (`_unused`, dead imports,
  inline `humantime` mini-module)
- Document missing step 6 in the pre-commit pipeline
- Delete untracked directories `tests/cli/` and `tests/cucumber/` (contain no tracked files)
- Rename `cover.out` → `lcov.info` (standard `cargo-llvm-cov` convention) in
  `project.json`, `.gitignore`, and `scripts/shadow-diff.sh`
- Convert all `<name>/mod.rs` module files to Rust 2018+/2024 idiomatic style:
  `<name>.rs` at the parent level, sub-files remain in `<name>/` directory
- Consolidate `gitutil.rs` (Go-ism naming + split concern) into `git/root.rs`
  sub-module; rename `find_git_root` → `find_root`
- Move `commands/naming_reporter.rs` (a shared utility, not a CLI entry point)
  to `internal/naming/reporter.rs`

### Out of Scope

- Flattening the `internal/` directory itself (requires touching every import path
  in the codebase; deferred as a separate plan)
- Renaming CLI commands (user-facing API change; needs independent decision)
- Adding content to `tests/` sub-directories (tracked separately)

## Business Rationale

Technical debt from the Go port creates friction for anyone extending or debugging
rhino-cli:

- **Discoverability**: Go-style `mod.rs` files mean editors and `find` show
  many identically-named files; Rust 2024 flat style is unambiguous.
- **Correctness**: Dead `mpsc`/`thread` imports with `_unused()` suppressor are
  confusing and signal work-in-progress that never landed.
- **Naming clarity**: `cover.out` is a Go artifact name; `lcov.info` is the
  [Repo-grounded / Web-cited] standard used in `cargo-llvm-cov` README and
  VS Code Coverage Gutters auto-detection.
- **Maintainability**: `naming_reporter.rs` is self-described as a shared utility
  but lives in `commands/`; wrong location misleads future contributors.

**Success metric** [Judgment call]: Zero `mod.rs` files under `src/`, no
`gitutil` module, all Nx targets pass CI.

## Technical Approach

### Module naming: `foo/mod.rs` → `foo.rs`

[Web-cited: <https://doc.rust-lang.org/reference/items/modules.html>, accessed 2026-05-24]
The Rust Reference (since 1.30): "It is encouraged to use the new naming convention
as it is more consistent, and avoids having many files named `mod.rs` within a
project." In the new style, the module file lives at the parent level (`foo.rs`)
and sub-files remain in `foo/`. Both resolve identically — no import path changes
are needed.

**Single-file directory modules** (only a `mod.rs`, no sub-files):
Delete the directory; place content in sibling `.rs` file.
Affected: `bcregistry/`, `cliout/`, `envbackup/`, `glossary/`, `mermaid/`.

**Multi-file directory modules** (`mod.rs` + sub-files):
Move `mod.rs` content to a sibling `.rs`; keep the directory and its sub-files.
Affected: `agents/`, `docs/`, `doctor/`, `naming/`, `repo_governance/`,
`speccoverage/`, `testcoverage/`.

**Special — `git/`**: After moving `git/mod.rs` → `git.rs`, keep the `git/`
directory alive for Phase 3's `git/root.rs`.

**Special — top-level `mod.rs` files**:

- `src/internal/mod.rs` → `src/internal.rs` (Rust resolves `pub mod internal;`
  in `lib.rs` to `src/internal.rs` first, then `src/internal/mod.rs`)
- `src/commands/mod.rs` → `src/commands.rs` (same resolution)

### `gitutil` consolidation

[Web-cited: <https://rust-lang.github.io/api-guidelines/naming.html>, accessed 2026-05-24]
The Rust API Guidelines: name modules by domain, not by the "util" suffix (Go-ism).
`find_git_root` also repeats "git" — redundant given the module path. New structure:

```
src/internal/git.rs           # pre-commit runner (was git/mod.rs)
src/internal/git/root.rs      # NEW: was gitutil.rs; exposes find_root()
```

Thirty-five command files import `crate::internal::gitutil::find_git_root()`. After the
change they import `crate::internal::git::root::find_root()`.

### `naming_reporter` relocation

`naming_reporter.rs` is consumed by two commands via `use super::naming_reporter::`.
Moving it to `internal/naming/reporter.rs` and adding `pub mod reporter;` to
`naming.rs` makes the relationship explicit: naming utilities live in `internal`,
commands only hold entry-point dispatch logic.

### `lcov.info` rename

[Web-cited: <https://github.com/taiki-e/cargo-llvm-cov>, accessed 2026-05-24]
`cargo-llvm-cov` README and all GitHub Actions examples use `lcov.info`.
VS Code Coverage Gutters auto-detects `lcov.info` at the project root. Three
locations must change: `project.json` (command string + outputs), `.gitignore`,
and the comment in `scripts/shadow-diff.sh`.

## Worktree

Worktree path: `worktrees/rhino-cli-structural-cleanup/`

Provision before execution (run from repo root):

```bash
claude --worktree rhino-cli-structural-cleanup
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
and [Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

## Product Requirements

**User story**: As a `rhino-cli` maintainer, I want idiomatic Rust 2024 module structure
so that editors, search tools, and future contributors can navigate the codebase without
Go-ism artifacts.

```gherkin
Scenario: No mod.rs files remain in src/
  Given the Phase 2 module normalization is complete
  When `find apps/rhino-cli/src -name mod.rs` is run
  Then it returns no matches

Scenario: gitutil module removed
  Given Phase 3 consolidation is complete
  When `grep -r "gitutil" apps/rhino-cli/src/` is run
  Then it returns no matches

Scenario: naming_reporter lives only in internal
  Given Phase 4 relocation is complete
  When `find apps/rhino-cli/src/commands -name naming_reporter.rs` is run
  Then it returns no matches
  And `apps/rhino-cli/src/internal/naming/reporter.rs` exists

Scenario: lcov.info replaces cover.out
  Given Phase 1 artifact cleanup is complete
  When `grep -r "cover\.out" apps/rhino-cli/` is run
  Then it returns no matches
  And `apps/rhino-cli/project.json` references `lcov.info`

Scenario: All quality targets pass after restructuring
  Given all phases are complete
  When `npx nx run rhino-cli:test:quick` is run
  Then it exits 0 with coverage ≥ 90 % line coverage
  When `npx nx run rhino-cli:lint` is run
  Then it exits 0

Scenario: No dead code in git pre-commit module
  Given Phase 1 dead-code cleanup is complete and Phase 2d module rename is complete
  When `grep -n "_unused\|mpsc::channel\|thread::spawn" apps/rhino-cli/src/internal/git.rs` is run
  Then it returns no matches
```

## Quality Gates

### Local (Before Push)

- `npx nx run rhino-cli:typecheck` — exits 0
- `npx nx run rhino-cli:lint` — exits 0
- `npx nx run rhino-cli:fmt:check` — exits 0
- `npx nx run rhino-cli:test:quick` — exits 0, coverage ≥ 90% line coverage

### CI (After Push)

- `pr-quality-gate.yml` passes for all affected targets (typecheck, lint, test:quick, spec-coverage)

> **Important**: Fix ALL failures found, including preexisting issues not caused by your changes (root cause orientation principle).

## Verification

Work is done when all of the following are true:

1. `find apps/rhino-cli/src -name mod.rs` returns empty
2. `grep -r "gitutil" apps/rhino-cli/src/` returns empty
3. `find apps/rhino-cli/src/commands -name naming_reporter.rs` returns empty
4. `grep -r "cover\.out" apps/rhino-cli/` returns empty
5. `npx nx run rhino-cli:test:quick` exits 0 with coverage ≥ 90%
6. `npx nx run rhino-cli:lint` exits 0
7. CI `pr-quality-gate.yml` passes on `main`
8. Plan archived to `plans/done/`

## Delivery Checklist

### Phase 0: Environment Setup

- [x] Provision worktree: `claude --worktree rhino-cli-structural-cleanup`
- [x] In repo root, run `npm install && npm run doctor -- --fix` to initialize
      the toolchain (see [Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md))
- [x] Verify baseline passes before making changes:
      `npx nx run rhino-cli:test:quick` — must exit 0 and report ≥ 90% line coverage.
      Record the exact coverage percentage as the baseline to compare at the end.

---

### Phase 1: Dead Code and Go Artifact Cleanup

- [x] Edit `apps/rhino-cli/src/internal/git/mod.rs` [Repo-grounded]:
  - Remove `use std::sync::mpsc;` and `use std::thread;` imports
  - Remove `use std::fs;` — it is only used in the dead `_unused()` function being removed (the test module uses `std::fs::create_dir_all` and `std::fs::write` with fully qualified paths that do not depend on this import)
  - Remove the `_unused()` function and its preceding comment block
    (`// Suppress unused warnings...`)
  - Replace `humantime::format_duration(STEP_TIMEOUT)` call (line ~70) with
    `format!("{}s", STEP_TIMEOUT.as_secs())`
  - Delete the `mod humantime { ... }` block at the bottom of the file
  - After the `step5b` call block and before the `step7` call block, insert:
    `// Step 6 (agent-format hook) was present in the Go source but removed`
    `// during the Go→Rust port; gap in numbering is intentional.`
  - Acceptance criterion: `grep -n "_unused\|mpsc\|thread::spawn\|use std::fs;\|mod humantime" apps/rhino-cli/src/internal/git/mod.rs` returns no matches (the suppressor block and dead imports are gone).
  - _Suggested executor: `swe-rust-dev`_

- [x] Delete untracked directories (contain no tracked files — no git history to preserve):

  ```bash
  rm -rf apps/rhino-cli/tests/cli apps/rhino-cli/tests/cucumber
  ```

  Verify: `find apps/rhino-cli/tests -mindepth 1 | wc -l` → `0`

- [x] Edit `apps/rhino-cli/project.json` [Repo-grounded]:
  - In the `test:quick` target `command` string: replace
    `--output-path apps/rhino-cli/cover.out` with
    `--output-path apps/rhino-cli/lcov.info`
  - In the `test:quick` target `outputs` array: replace
    `"{projectRoot}/cover.out"` with `"{projectRoot}/lcov.info"`
  - Verify: `grep "cover.out" apps/rhino-cli/project.json` → no matches; `grep "lcov.info" apps/rhino-cli/project.json` → 2 matches (one in command, one in outputs).
  - _Suggested executor: `swe-rust-dev`_

- [x] Edit `apps/rhino-cli/.gitignore` [Repo-grounded]:
  - Replace `cover.out` with `lcov.info`
  - Replace `cover_spec.out` with `lcov_spec.info`

- [x] Edit `apps/rhino-cli/scripts/shadow-diff.sh` line 9 [Repo-grounded]:
  - Update the example comment from
    `shadow-diff.sh test-coverage validate apps/rhino-cli/cover.out 90` to
    `shadow-diff.sh test-coverage validate apps/rhino-cli/lcov.info 90`

- [x] Verify Phase 1: `cargo check --manifest-path apps/rhino-cli/Cargo.toml --all-targets`
      exits 0; `npx nx run rhino-cli:test:unit` exits 0 with the same test count as the
      Phase 0 baseline (confirms no tests were accidentally deleted with the dead code).
  - _Suggested executor: `swe-rust-dev`_

- [x] Commit: `refactor(rhino-cli): remove dead code and rename cover.out to lcov.info`

---

### Phase 2: Module Naming Normalization (`mod.rs` → flat files)

> All changes in this phase are mechanical: `git mv` to preserve rename history,
> `rmdir` to remove empty directories for single-file modules. No import paths change.

#### 2a: Top-level `mod.rs` files

- [x] Move `apps/rhino-cli/src/internal/mod.rs` → `apps/rhino-cli/src/internal.rs`
      (preserves git rename history):

  ```bash
  git mv apps/rhino-cli/src/internal/mod.rs apps/rhino-cli/src/internal.rs
  ```

  `apps/rhino-cli/src/lib.rs` already has `pub mod internal;` — no change needed.
  - _Suggested executor: `swe-rust-dev`_

- [x] Move `apps/rhino-cli/src/commands/mod.rs` → `apps/rhino-cli/src/commands.rs`:

  ```bash
  git mv apps/rhino-cli/src/commands/mod.rs apps/rhino-cli/src/commands.rs
  ```

#### 2b: Single-file directory modules (move + delete directory)

For each module below: `git mv <module>/mod.rs <module>.rs`, then `rmdir` the
now-empty directory.

- [x] `bcregistry`:

  ```bash
  git mv apps/rhino-cli/src/internal/bcregistry/mod.rs apps/rhino-cli/src/internal/bcregistry.rs
  rmdir apps/rhino-cli/src/internal/bcregistry/
  ```

- [x] `cliout`:

  ```bash
  git mv apps/rhino-cli/src/internal/cliout/mod.rs apps/rhino-cli/src/internal/cliout.rs
  rmdir apps/rhino-cli/src/internal/cliout/
  ```

- [x] `envbackup`:

  ```bash
  git mv apps/rhino-cli/src/internal/envbackup/mod.rs apps/rhino-cli/src/internal/envbackup.rs
  rmdir apps/rhino-cli/src/internal/envbackup/
  ```

- [x] `glossary`:

  ```bash
  git mv apps/rhino-cli/src/internal/glossary/mod.rs apps/rhino-cli/src/internal/glossary.rs
  rmdir apps/rhino-cli/src/internal/glossary/
  ```

- [x] `mermaid`:

  ```bash
  git mv apps/rhino-cli/src/internal/mermaid/mod.rs apps/rhino-cli/src/internal/mermaid.rs
  rmdir apps/rhino-cli/src/internal/mermaid/
  ```

#### 2c: Multi-file directory modules (move `mod.rs` only; keep directory)

For each module below: `git mv <name>/mod.rs <name>.rs` at the `internal/` level.
All sub-files remain in `<name>/` unchanged; the directory is kept.

- [x] `agents`: move `internal/agents/mod.rs` → `internal/agents.rs`:

  ```bash
  git mv apps/rhino-cli/src/internal/agents/mod.rs apps/rhino-cli/src/internal/agents.rs
  ```

- [x] `docs`:

  ```bash
  git mv apps/rhino-cli/src/internal/docs/mod.rs apps/rhino-cli/src/internal/docs.rs
  ```

- [x] `doctor`:

  ```bash
  git mv apps/rhino-cli/src/internal/doctor/mod.rs apps/rhino-cli/src/internal/doctor.rs
  ```

- [x] `naming` (keep `naming/` directory — Phase 4 will add `naming/reporter.rs`):

  ```bash
  git mv apps/rhino-cli/src/internal/naming/mod.rs apps/rhino-cli/src/internal/naming.rs
  ```

- [x] `repo_governance`:

  ```bash
  git mv apps/rhino-cli/src/internal/repo_governance/mod.rs apps/rhino-cli/src/internal/repo_governance.rs
  ```

- [x] `speccoverage`:

  ```bash
  git mv apps/rhino-cli/src/internal/speccoverage/mod.rs apps/rhino-cli/src/internal/speccoverage.rs
  ```

- [x] `testcoverage`:

  ```bash
  git mv apps/rhino-cli/src/internal/testcoverage/mod.rs apps/rhino-cli/src/internal/testcoverage.rs
  ```

#### 2d: Special — `git/` (keep directory for Phase 3)

- [x] Move `git/mod.rs` → `git.rs` at `internal/` level, keep `git/` directory:

  ```bash
  git mv apps/rhino-cli/src/internal/git/mod.rs apps/rhino-cli/src/internal/git.rs
  ```

  The `git/` directory is now empty but will receive `root.rs` in Phase 3.

#### 2e: Update `project.json` coverage ignore regex

- [x] Edit `apps/rhino-cli/project.json` [Repo-grounded]:
      In the `test:quick` `command` string, update the `--ignore-filename-regex` value [Repo-grounded — existing flag in project.json]:
  - Replace `internal/git/mod\\.rs` with `internal/git\\.rs`
  - Replace `internal/doctor/mod\\.rs` with `internal/doctor\\.rs`
  - Verify: `grep "internal/git/mod" apps/rhino-cli/project.json` → no output; `grep "internal/git\\.rs" apps/rhino-cli/project.json` → shows the updated regex.
  - _Suggested executor: `swe-rust-dev`_

- [x] Remove the Go-port origin comments from `apps/rhino-cli/src/internal.rs`
      (was `internal/mod.rs`): delete the two comment lines at the top that reference
      `apps/rhino-cli/internal/<pkg>/` Go paths. Leave a single brief comment if needed.
  - _Suggested executor: `swe-rust-dev`_

- [x] Remove the Go-port origin comment from `apps/rhino-cli/src/commands.rs`
      (was `commands/mod.rs`): delete comment referencing `apps/rhino-cli/cmd/*.go`.
  - _Suggested executor: `swe-rust-dev`_

#### 2f: Verify Phase 2

- [x] Verify compile: `cargo check --manifest-path apps/rhino-cli/Cargo.toml --all-targets`
      exits 0
  - _Suggested executor: `swe-rust-dev`_

- [x] Confirm no `mod.rs` files remain:

  ```bash
  find apps/rhino-cli/src -name mod.rs
  ```

  Must return empty.

- [x] Run full test suite: `npx nx run rhino-cli:test:unit` exits 0

- [x] Commit: `refactor(rhino-cli): convert all mod.rs to Rust 2018+ flat-file style`

---

### Phase 3: Consolidate `gitutil` into `git::root`

- [x] Confirm Red gate — verify existing `gitutil` tests reference `find_git_root`:
      `grep -n "find_git_root" apps/rhino-cli/src/internal/gitutil.rs` — must show
      at least the function definition and its test. Also confirm that `cargo check`
      currently PASSES (Phase 2 complete) before creating the new file. These tests
      will be carried over to `root.rs` and serve as the correctness gate once the
      rename is complete.
  - _Suggested executor: `swe-rust-dev`_

- [x] Create `apps/rhino-cli/src/internal/git/root.rs` [_New file_]:
      Copy the entire content of `apps/rhino-cli/src/internal/gitutil.rs` to this
      new file. Then rename `find_git_root` → `find_root` everywhere in `root.rs`
      (function definition and the test assertion message).
  - _Suggested executor: `swe-rust-dev`_

- [x] Edit `apps/rhino-cli/src/internal/git.rs` [Repo-grounded]:
      Add `pub mod root;` as the first `pub mod` declaration (before any `use`
      statements or function definitions).
  - _Suggested executor: `swe-rust-dev`_

- [x] Edit `apps/rhino-cli/src/internal.rs` [Repo-grounded]:
      Remove the line `pub mod gitutil;` (this line declares the old `gitutil` module;
      removing it causes `cargo check` to fail until all 35 caller files are updated —
      that compile failure is the expected Red gate confirming work is not yet done).
  - _Suggested executor: `swe-rust-dev`_

- [x] Delete `apps/rhino-cli/src/internal/gitutil.rs`:

  ```bash
  rm apps/rhino-cli/src/internal/gitutil.rs
  ```

- [x] Update all 35 caller files — change `use crate::internal::gitutil;` →
      `use crate::internal::git;` and `gitutil::find_git_root()` →
      `git::root::find_root()` [Repo-grounded]. Use this `sed` one-liner to update
      all files atomically:

  ```bash
  grep -rln "gitutil" apps/rhino-cli/src/ | xargs sed -i \
    's/use crate::internal::gitutil;/use crate::internal::git;/g; s/gitutil::find_git_root()/git::root::find_root()/g'
  ```

  The complete list of affected files (for manual verification):
  - `src/commands/agents_detect_duplication.rs`
  - `src/commands/agents_sync.rs`
  - `src/commands/agents_validate_claude.rs`
  - `src/commands/agents_validate_naming.rs`
  - `src/commands/agents_validate_sync.rs`
  - `src/commands/ddd_bc.rs`
  - `src/commands/ddd_ul.rs`
  - `src/commands/docs_validate_frontmatter.rs`
  - `src/commands/docs_validate_heading_hierarchy.rs`
  - `src/commands/docs_validate_links.rs`
  - `src/commands/docs_validate_mermaid.rs`
  - `src/commands/docs_validate_naming.rs`
  - `src/commands/doctor.rs`
  - `src/commands/env_backup.rs`
  - `src/commands/env_init.rs`
  - `src/commands/env_restore.rs`
  - `src/commands/git_pre_commit.rs`
  - `src/commands/governance_agents_md_size.rs`
  - `src/commands/governance_audit.rs`
  - `src/commands/governance_emoji_audit.rs`
  - `src/commands/governance_frontmatter_audit.rs`
  - `src/commands/governance_layer_coherence.rs`
  - `src/commands/governance_license_audit.rs`
  - `src/commands/governance_readme_index_audit.rs`
  - `src/commands/governance_traceability_audit.rs`
  - `src/commands/governance_vendor_audit.rs`
  - `src/commands/spec_coverage_validate.rs`
  - `src/commands/specs_validate_adoption.rs`
  - `src/commands/specs_validate_counts.rs`
  - `src/commands/specs_validate_links.rs`
  - `src/commands/specs_validate_tree.rs`
  - `src/commands/test_coverage_diff.rs`
  - `src/commands/test_coverage_merge.rs`
  - `src/commands/test_coverage_validate.rs`
  - `src/commands/workflows_validate_naming.rs`

  > Run `grep -rn "gitutil" apps/rhino-cli/src/` after edits — must return no matches
  > (Green gate: all callers updated, module removed).
  - _Suggested executor: `swe-rust-dev`_

- [x] Verify: `cargo check --manifest-path apps/rhino-cli/Cargo.toml --all-targets`
      exits 0 (Green gate — confirms `git::root::find_root()` resolves correctly for
      all 35 callers); then `npx nx run rhino-cli:test:unit` exits 0
  - _Suggested executor: `swe-rust-dev`_

- [x] Commit: `refactor(rhino-cli): consolidate gitutil into git::root, rename find_git_root→find_root`

---

### Phase 4: Move `naming_reporter` to `internal/naming/`

- [x] Create `apps/rhino-cli/src/internal/naming/reporter.rs` [_New file_]:
      Copy the entire content of `apps/rhino-cli/src/commands/naming_reporter.rs`
      into this new file. No content changes needed.
  - _Suggested executor: `swe-rust-dev`_

- [x] Edit `apps/rhino-cli/src/internal/naming.rs` [Repo-grounded]:
      Add `pub mod reporter;` as the first `pub mod` line.
  - _Suggested executor: `swe-rust-dev`_

- [x] Delete `apps/rhino-cli/src/commands/naming_reporter.rs`:

  ```bash
  rm apps/rhino-cli/src/commands/naming_reporter.rs
  ```

- [x] Edit `apps/rhino-cli/src/commands.rs` [Repo-grounded]:
      Remove the line `pub mod naming_reporter;`
  - _Suggested executor: `swe-rust-dev`_

- [x] Edit `apps/rhino-cli/src/commands/agents_validate_naming.rs` [Repo-grounded]:
      Replace `use super::naming_reporter::{format_json, format_markdown, format_text};`
      with `use crate::internal::naming::reporter::{format_json, format_markdown, format_text};`
  - _Suggested executor: `swe-rust-dev`_

- [x] Edit `apps/rhino-cli/src/commands/workflows_validate_naming.rs` [Repo-grounded]:
      Same substitution as above.
  - _Suggested executor: `swe-rust-dev`_

- [x] Verify: `cargo check --manifest-path apps/rhino-cli/Cargo.toml --all-targets`
      exits 0; then `npx nx run rhino-cli:test:unit` exits 0
  - _Suggested executor: `swe-rust-dev`_

- [x] Confirm placement:

  ```bash
  find apps/rhino-cli/src/commands -name naming_reporter.rs
  ```

  Must return empty.
  - _Suggested executor: `swe-rust-dev`_

- [x] Commit: `refactor(rhino-cli): move naming_reporter from commands/ to internal/naming/`

---

### Local Quality Gates (Before Push)

- [x] Run full lint: `npx nx run rhino-cli:lint` — exits 0
- [x] Run format check: `npx nx run rhino-cli:fmt:check` — exits 0
- [x] Run typecheck: `npx nx run rhino-cli:typecheck` — exits 0
- [x] Run unit tests with coverage: `npx nx run rhino-cli:test:quick` — exits 0,
      coverage ≥ 90 %
- [x] Confirm no `mod.rs` files: `find apps/rhino-cli/src -name mod.rs` → empty
- [x] Confirm no `gitutil` references: `grep -r "gitutil" apps/rhino-cli/src/` → empty
- [x] Confirm `cover.out` absent: `grep -r "cover\.out" apps/rhino-cli/` → empty
      (Note: remaining `cover.out` refs in testcoverage/\*.rs are semantic — they
      reference Go's coverage format, not the LLVM output file we renamed)

> **Important**: Fix ALL failures found, including any preexisting issues
> encountered during work (root cause orientation principle).

---

### Commit Guidelines

- [x] Commit thematically — one commit per phase
- [x] Follow Conventional Commits: `refactor(rhino-cli): <description>`
- [x] Do not bundle unrelated fixes into a single commit

---

### Post-Push Verification

- [x] Push changes to `main`
- [x] Find the relevant run: `gh run list --branch main --limit 5` — identify the
      run triggered by the push commit
      (Note: `pr-quality-gate.yml` is PR-only — no separate CI fires on direct main
      push for rhino-cli changes; pre-push hook is the quality gate for trunk-based dev)
- [x] Monitor GitHub Actions: `pr-quality-gate.yml` (runs `nx affected -t typecheck lint test:quick spec-coverage` for affected projects including `rhino-cli`)
- [x] Verify all CI checks pass — `gh run view <run-id> --json status,conclusion`
      must show `conclusion: success`
- [x] If any CI check fails, fix immediately and push a follow-up commit
- [x] Do NOT mark plan done until CI is green

---

### Plan Archival

- [x] Verify ALL delivery checklist items are ticked
- [x] Verify ALL quality gates pass (local + CI)
- [x] `git mv plans/in-progress/rhino-cli-structural-cleanup/ plans/done/2026-05-24__rhino-cli-structural-cleanup/`
      (replace `XX-XX` with actual completion date)
- [x] Update `plans/in-progress/README.md` — remove this plan entry
- [x] Update `plans/done/README.md` — add this plan entry with completion date
- [x] Commit: `chore(plans): move rhino-cli-structural-cleanup to done`
