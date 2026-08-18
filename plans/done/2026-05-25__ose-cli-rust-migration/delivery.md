# Delivery Checklist — ose-cli Rust Migration

## Worktree

Worktree path: `worktrees/ose-cli-rust-migration/`

Provision before execution (run from repo root):

```bash
claude --worktree ose-cli-rust-migration
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and [Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

## Environment Setup

- [x] Install dependencies in the root worktree (run from repo root `worktrees/ose-cli-rust-migration/`):

  ```bash
  npm install
  ```

  Acceptance criterion: exits 0 with no errors.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: npm install exited 0, 1563 packages audited, up to date.

- [x] Converge the full polyglot toolchain:

  ```bash
  npm run doctor -- --fix
  ```

  Acceptance criterion: exits 0; Rust toolchain 1.95.0 confirmed present.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: All 20/20 tools OK, nothing to fix. Rust 1.94.0 default; 1.95.0 toolchain installed and available (confirmed via rustup toolchain list).

- [x] Verify the existing `rhino-cli` build still passes (confirms Rust toolchain is functional):

  ```bash
  npx nx run rhino-cli:build
  ```

  Acceptance criterion: exits 0, binary appears at `apps/rhino-cli/dist/rhino-cli`.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Build passed (from cache). Binary confirmed at apps/rhino-cli/dist/rhino-cli.

- [x] Run existing `ose-cli` Go tests to establish a baseline before any changes:

  ```bash
  npx nx run ose-cli:test:unit
  ```

  Acceptance criterion: note any preexisting failures; do not proceed with changes until baseline is recorded.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Baseline PASS — ok cmd 0.665s, no preexisting failures.

---

## Phase 0: Create libs/rust-commons/

### Step 0.1: Scaffold libs/rust-commons/ directory and Cargo.toml

- [x] Create directory `libs/rust-commons/src/links/` (_New directory_):

  ```bash
  mkdir -p libs/rust-commons/src/links
  ```

  Acceptance criterion: directory exists.
  - **Date**: 2026-05-25
  - **Status**: Completed

- [x] Create `libs/rust-commons/Cargo.toml` (_New file_) with the following content:

  ```toml
  [package]
  name = "rust-commons"
  version = "0.1.0"
  edition = "2024"
  rust-version = "1.88"
  description = "Shared Rust utilities for ose-public CLI tools"
  license = "MIT"
  publish = false

  [lib]
  name = "rust_commons"
  path = "src/lib.rs"

  [dependencies]
  walkdir = "2.5.0"
  regex = "1.12.3"
  serde = { version = "1.0.228", features = ["derive"] }
  serde_json = "1.0.150"
  anyhow = "1.0.102"

  [dev-dependencies]
  tempfile = "3.27.0"

  [lints.rust]
  unsafe_code = "forbid"
  missing_docs = "deny"

  [lints.rustdoc]
  private_intra_doc_links = "deny"

  [lints.clippy]
  pedantic = { level = "warn", priority = -1 }
  struct_excessive_bools = "allow"
  cast_precision_loss = "allow"
  cast_possible_wrap = "allow"
  must_use_candidate = "allow"
  unnecessary_wraps = "allow"
  case_sensitive_file_extension_comparisons = "allow"
  missing_errors_doc = "deny"
  missing_panics_doc = "deny"
  doc_markdown = "deny"
  missing_docs_in_private_items = "deny"
  unwrap_used = "deny"
  panic = "deny"
  undocumented_unsafe_blocks = "deny"
  indexing_slicing = "allow"
  arithmetic_side_effects = "allow"

  [profile.release]
  opt-level = 3
  lto = "thin"
  codegen-units = 1
  panic = "abort"
  strip = "symbols"
  ```

  Acceptance criterion: file exists and `cargo metadata --manifest-path libs/rust-commons/Cargo.toml` exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Created. cargo metadata exits 0, package resolved successfully.

  _Suggested executor: `swe-rust-dev`_

- [x] Create `libs/rust-commons/rust-toolchain.toml` (_New file_):

  ```toml
  [toolchain]
  channel = "1.95.0"
  components = ["clippy", "rustfmt", "llvm-tools"]
  profile = "minimal"
  ```

  Acceptance criterion: file exists.
  - **Date**: 2026-05-25
  - **Status**: Completed

### Step 0.2: Add libs/rust-commons/ to the workspace Cargo.toml (if workspace-level Cargo.toml exists)

- [x] Check whether a workspace-level `Cargo.toml` exists at the repo root:

  ```bash
  test -f Cargo.toml && echo "EXISTS" || echo "NOT_EXISTS"
  ```

  If `NOT_EXISTS`: no action needed (each Rust project has its own standalone manifest, same as `rhino-cli`). If `EXISTS`: add `"libs/rust-commons"` to the `[workspace] members` array. Acceptance criterion: `cargo metadata` resolves the crate.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: NOT_EXISTS — no workspace Cargo.toml. Each Rust crate is standalone, same as rhino-cli pattern. No action needed.

### Step 0.3: Write failing unit tests for libs/rust-commons (RED)

- [x] Create `libs/rust-commons/src/lib.rs` (_New file_) — declare the `links` module:

  ```rust
  //! `rust-commons` — shared Rust utilities for `ose-public` CLI tools.
  //!
  //! # Modules
  //!
  //! - [`links`] — internal link checking for Hugo/Next.js markdown content.
  #![forbid(unsafe_code)]

  pub mod links;
  ```

  Acceptance criterion: file exists.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

- [x] Create `libs/rust-commons/src/links/mod.rs` (_New file_) with the public API surface and failing test stubs. Write tests FIRST (Red phase). The file must define:
  - `pub struct BrokenLink { source_file, line, text, target }` with `#[derive(Debug, Clone, serde::Serialize)]`
  - `pub struct CheckResult { checked_count, error_count, errors, broken_links }`
  - `pub fn check_links(content_dir: &Path) -> anyhow::Result<CheckResult>`
  - `pub fn output_links_text(result: &CheckResult, elapsed: Duration, quiet: bool, verbose: bool)`
  - `pub fn output_links_json(result: &CheckResult, elapsed: Duration) -> anyhow::Result<String>`
  - `pub fn output_links_markdown(result: &CheckResult, elapsed: Duration)`
  - `#[cfg(test)] mod tests` block with at minimum these _New tests_:
    - `test_check_links_returns_ok_for_empty_dir`
    - `test_check_links_detects_broken_link`
    - `test_check_links_skips_code_blocks`
    - `test_check_links_rejects_nonexistent_dir`
    - `test_output_links_json_contains_required_keys`
    - `test_output_links_markdown_contains_headings`

  Verify RED: `cargo test --manifest-path libs/rust-commons/Cargo.toml --lib` — all new tests fail to compile or fail at runtime (stubs return `todo!()`). This is the expected RED state.

  Acceptance criterion: `cargo check --manifest-path libs/rust-commons/Cargo.toml` succeeds (types compile); `cargo test --lib` reports failures or panics on the stubs.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: RED confirmed. cargo check exits 0 (19 crates compiled). cargo test --lib: 0 passed, 6 failed — all panic with "not yet implemented".

  _Suggested executor: `swe-rust-dev`_

### Step 0.4: Implement libs/rust-commons link-checking logic (GREEN)

- [x] Implement the full body of `libs/rust-commons/src/links/mod.rs` (_Modify_), porting logic from `libs/golang-link-commons/links/checker.go` and `libs/golang-link-commons/links/output.go`. Port the following behaviors exactly:
  - Walk `.md` files recursively with `walkdir`
  - Extract markdown links with `regex` pattern `\[([^\]]*)\]\(([^)]+)\)`
  - Skip external links (`http://`, `https://`, `mailto:`, `//`) and same-page anchors (`#`)
  - Skip links with file extensions (e.g. `/updates/index.xml`)
  - Strip fragment (`#`) and query (`?`) from link targets before resolving
  - Resolve targets relative to `content_dir`: check `<target>.md` and `<target>/_index.md`
  - Track fenced code blocks (` ``` ` and `~~~`) and skip link extraction inside them
  - `output_links_json` returns a JSON string with keys: `status`, `timestamp`, `duration_ms`, `checked`, `broken`, `errors`, `broken_links`
  - `output_links_markdown` prints `# Link Check Report`, `## Summary` table, optional `## Broken Links` table

  Verify GREEN: `cargo test --manifest-path libs/rust-commons/Cargo.toml --lib` — all tests in `test` block pass.

  Acceptance criterion: `cargo test --lib` exits 0 with all tests passing.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: All 6 unit tests pass. Added chrono dep for timestamps. Delegated to swe-rust-dev.
  - **Files Changed**: `libs/rust-commons/src/links/mod.rs`, `libs/rust-commons/Cargo.toml` (added chrono)

  _Suggested executor: `swe-rust-dev`_

### Step 0.5: Check coverage threshold (GREEN continued)

- [x] Run coverage check for `libs/rust-commons`:

  ```bash
  cargo llvm-cov --manifest-path libs/rust-commons/Cargo.toml --lib --fail-under-lines 90
  ```

  Acceptance criterion: exits 0 (90% line coverage met). If below threshold, add additional unit tests before proceeding.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Initial run was 73.82% (below threshold). Added 28 new tests (total 34). Final: 96.99% line coverage. Exits 0.
  - **Files Changed**: `libs/rust-commons/src/links/mod.rs` (28 tests added)

  _Suggested executor: `swe-rust-dev`_

### Step 0.6: Refactor libs/rust-commons (REFACTOR)

- [x] Review `libs/rust-commons/src/links/mod.rs` for clarity and idiomatic Rust style:
  - Extract any long functions into private helpers if they exceed ~50 lines
  - Ensure all public items have doc comments (required by `missing_docs = "deny"`)
  - Ensure all `///` doc comments for fallible functions include `# Errors` section (required by `missing_errors_doc = "deny"`)
  - Run `cargo clippy --manifest-path libs/rust-commons/Cargo.toml --all-targets -- -D warnings` and fix all warnings

  Acceptance criterion: `cargo clippy --all-targets -- -D warnings` exits 0; `cargo test --lib` still passes.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: cargo clippy "No issues found". 34 tests pass.

  _Suggested executor: `swe-rust-dev`_

### Step 0.7: Create libs/rust-commons project.json

- [x] Create `libs/rust-commons/project.json` (_New file_):

  ```json
  {
    "name": "rust-commons",
    "sourceRoot": "libs/rust-commons",
    "projectType": "library",
    "tags": ["type:lib", "platform:cli", "lang:rust", "domain:tooling"],
    "implicitDependencies": [],
    "targets": {
      "build": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo build --release --manifest-path libs/rust-commons/Cargo.toml"
        },
        "outputs": ["{projectRoot}/target"]
      },
      "install": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo fetch --manifest-path libs/rust-commons/Cargo.toml"
        }
      },
      "fmt": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo fmt --manifest-path libs/rust-commons/Cargo.toml"
        }
      },
      "fmt:check": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo fmt --manifest-path libs/rust-commons/Cargo.toml -- --check"
        },
        "cache": true,
        "inputs": ["{projectRoot}/src/**/*.rs"]
      },
      "lint": {
        "executor": "nx:run-commands",
        "options": {
          "commands": [
            "cargo fmt --manifest-path libs/rust-commons/Cargo.toml -- --check",
            "cargo clippy --manifest-path libs/rust-commons/Cargo.toml --all-targets -- -D warnings"
          ],
          "parallel": false
        }
      },
      "typecheck": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo check --manifest-path libs/rust-commons/Cargo.toml --all-targets"
        }
      },
      "test:unit": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo test --manifest-path libs/rust-commons/Cargo.toml --lib"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/src/**/*.rs"]
      },
      "test:quick": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo llvm-cov --manifest-path libs/rust-commons/Cargo.toml --lib --fail-under-lines 90"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/src/**/*.rs"]
      },
      "spec-coverage": {
        "executor": "nx:run-commands",
        "options": {
          "command": "echo 'spec-coverage not applicable for library crate rust-commons'"
        },
        "cache": true,
        "inputs": ["{projectRoot}/src/**/*.rs"]
      }
    }
  }
  ```

  Acceptance criterion: `npx nx run rust-commons:typecheck` exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Created. nx run rust-commons:typecheck exits 0.

### Step 0.8: Commit Phase 0

- [x] Format Rust source:

  ```bash
  cargo fmt --manifest-path libs/rust-commons/Cargo.toml
  ```

  Acceptance criterion: `cargo fmt --manifest-path libs/rust-commons/Cargo.toml -- --check` exits 0
  (no changes needed).
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Formatted. -- --check exits 0.

- [x] Stage and commit:

  ```bash
  git add libs/rust-commons/
  git commit -m "feat(rust-commons): add shared link-checking lib crate (Phase 0)"
  ```

  Acceptance criterion: commit exists; `git log --oneline -1` shows the commit message.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Commit 994992bcb. 6 files changed, 1629 insertions.

---

## Phase 1: Rewrite apps/ose-cli/ in Rust

### Step 1.1: Scaffold Rust project files

- [x] Create `apps/ose-cli/rust-toolchain.toml` (_New file_):

  ```toml
  [toolchain]
  channel = "1.95.0"
  components = ["clippy", "rustfmt", "llvm-tools"]
  profile = "minimal"
  ```

  Acceptance criterion: file exists.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

- [x] Create `apps/ose-cli/deny.toml` (_New file_) with the same content as `apps/rhino-cli/deny.toml` [Repo-grounded]:

  ```toml
  # cargo-deny configuration for ose-cli.
  # Run: cargo deny --manifest-path apps/ose-cli/Cargo.toml check

  [graph]
  targets = []

  [advisories]
  version = 2
  ignore = []

  [licenses]
  version = 2
  allow = [
    "MIT",
    "Apache-2.0",
    "Apache-2.0 WITH LLVM-exception",
    "ISC",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "Unicode-3.0",
  ]

  [bans]
  multiple-versions = "warn"
  deny = []

  [sources]
  unknown-registry = "deny"
  unknown-git = "deny"
  allow-registry = ["https://github.com/rust-lang/crates.io-index"]
  ```

  Acceptance criterion: file exists.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Created matching rhino-cli/deny.toml content.

  _Suggested executor: `swe-rust-dev`_

- [x] Create `apps/ose-cli/Cargo.toml` (_New file_):

  ```toml
  [package]
  name = "ose-cli"
  version = "0.1.0"
  edition = "2024"
  rust-version = "1.88"
  description = "CLI tools for ose-web site maintenance"
  license = "MIT"
  publish = false

  [[bin]]
  name = "ose-cli"
  path = "src/main.rs"

  [lib]
  name = "ose_cli"
  path = "src/lib.rs"

  [dependencies]
  clap = { version = "4.6.1", features = ["derive", "env"] }
  rust-commons = { path = "../../libs/rust-commons" }
  anyhow = "1.0.102"
  serde_json = "1.0.150"

  [dev-dependencies]
  assert_cmd = "2.2.2"
  predicates = "3.1.4"
  tempfile = "3.27.0"

  [lints.rust]
  unsafe_code = "forbid"
  missing_docs = "deny"

  [lints.rustdoc]
  private_intra_doc_links = "deny"

  [lints.clippy]
  pedantic = { level = "warn", priority = -1 }
  struct_excessive_bools = "allow"
  cast_precision_loss = "allow"
  cast_possible_wrap = "allow"
  must_use_candidate = "allow"
  unnecessary_wraps = "allow"
  case_sensitive_file_extension_comparisons = "allow"
  missing_errors_doc = "deny"
  missing_panics_doc = "deny"
  doc_markdown = "deny"
  missing_docs_in_private_items = "deny"
  unwrap_used = "deny"
  panic = "deny"
  undocumented_unsafe_blocks = "deny"
  indexing_slicing = "allow"
  arithmetic_side_effects = "allow"

  [profile.release]
  opt-level = 3
  lto = "thin"
  codegen-units = 1
  panic = "abort"
  strip = "symbols"
  ```

  Acceptance criterion: `cargo check --manifest-path apps/ose-cli/Cargo.toml` exits 0 (after source files are created in subsequent steps).
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Created with clap 4.6.1, rust-commons path dep, strict lints matching rhino-cli.

  _Suggested executor: `swe-rust-dev`_

### Step 1.2: Write failing smoke tests (RED)

- [x] Create `apps/ose-cli/tests/` directory and `apps/ose-cli/tests/cli_smoke.rs` (_New file_) with the following failing test stubs (tests will fail until binary is implemented):

  ```rust
  //! Smoke tests for the `ose-cli` binary.
  use assert_cmd::Command;
  use predicates::str::contains;
  use tempfile::TempDir;

  fn cmd() -> Command {
      Command::cargo_bin("ose-cli").expect("binary not found")
  }

  #[test]
  fn help_flag_exits_success() {
      cmd().arg("--help").assert().success();
  }

  #[test]
  fn unknown_subcommand_exits_failure() {
      cmd().arg("not-a-real-command").assert().failure();
  }

  #[test]
  fn invalid_output_format_exits_failure() {
      cmd()
          .args(["--output", "bad-format", "links", "check"])
          .assert()
          .failure();
  }

  #[test]
  fn links_check_passes_on_empty_dir() {
      let dir = TempDir::new().unwrap();
      cmd()
          .args(["links", "check", "--content", dir.path().to_str().unwrap()])
          .assert()
          .success();
  }

  #[test]
  fn links_check_reports_broken_link() {
      let dir = TempDir::new().unwrap();
      std::fs::write(
          dir.path().join("index.md"),
          "[broken](/does-not-exist)\n",
      )
      .unwrap();
      cmd()
          .args(["links", "check", "--content", dir.path().to_str().unwrap()])
          .assert()
          .failure()
          .stdout(contains("does-not-exist"));
  }

  #[test]
  fn links_check_json_output_is_valid() {
      let dir = TempDir::new().unwrap();
      let output = cmd()
          .args(["links", "check", "--content", dir.path().to_str().unwrap(), "-o", "json"])
          .assert()
          .success()
          .get_output()
          .stdout
          .clone();
      let s = String::from_utf8(output).unwrap();
      let v: serde_json::Value = serde_json::from_str(&s).expect("valid JSON");
      assert!(v.get("status").is_some());
      assert!(v.get("checked").is_some());
      assert!(v.get("broken_links").is_some());
  }

  #[test]
  fn links_check_markdown_output_has_headings() {
      let dir = TempDir::new().unwrap();
      cmd()
          .args(["links", "check", "--content", dir.path().to_str().unwrap(), "-o", "markdown"])
          .assert()
          .success()
          .stdout(contains("# Link Check Report"))
          .stdout(contains("## Summary"));
  }

  #[test]
  fn links_check_quiet_mode_no_output_on_success() {
      let dir = TempDir::new().unwrap();
      cmd()
          .args(["links", "check", "--content", dir.path().to_str().unwrap(), "--quiet"])
          .assert()
          .success()
          .stdout(predicates::str::is_empty());
  }

  #[test]
  fn links_check_nonexistent_dir_exits_failure() {
      cmd()
          .args(["links", "check", "--content", "/nonexistent/path/that/does/not/exist"])
          .assert()
          .failure();
  }
  ```

  Verify RED: `cargo test --manifest-path apps/ose-cli/Cargo.toml --tests` — tests fail to compile (binary does not exist yet). Expected RED state.

  Acceptance criterion: file exists; `cargo check --tests --manifest-path apps/ose-cli/Cargo.toml` (after creating src/ stubs) compiles.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Created tests/cli_smoke.rs with 9 smoke test stubs. Binary not built yet (RED state).

  _Suggested executor: `swe-rust-dev`_

### Step 1.3: Implement Rust source files (GREEN)

- [x] Create `apps/ose-cli/src/` directory and `apps/ose-cli/src/main.rs` (_New file_):

  ```rust
  //! `ose-cli` binary entry point.
  #![forbid(unsafe_code)]

  fn main() {
      let exit_code = ose_cli::cli::run();
      std::process::exit(exit_code);
  }
  ```

  Acceptance criterion: file exists.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

- [x] Create `apps/ose-cli/src/lib.rs` (_New file_):

  ```rust
  //! `ose-cli` library crate — CLI tools for `ose-web` site maintenance.
  //!
  //! Exposes the [`cli`] entry point and the [`commands`] dispatch layer.
  #![forbid(unsafe_code)]

  pub mod cli;
  pub mod commands;
  ```

  Acceptance criterion: file exists.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

- [x] Create `apps/ose-cli/src/commands/mod.rs` (_New file_):

  ```rust
  //! Command dispatch modules for `ose-cli`.
  pub mod links;
  ```

  Acceptance criterion: file exists.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

- [x] Create `apps/ose-cli/src/commands/links.rs` (_New file_). This module implements `LinksCheckArgs` (clap args struct) and `run_links_check(args, output_format)` calling `rust_commons::links::check_links()` and the appropriate output function. Mirror the Go `runLinksCheck` behavior from `apps/ose-cli/cmd/links_check.go` [Repo-grounded]:
  - Default `--content` value: `"apps/ose-web/content"`
  - Pass `quiet` and `verbose` flags through to `output_links_text`
  - Return `Err` if broken links found (causes non-zero exit)
  - Validate `output` flag: reject values other than `text`, `json`, `markdown`

  Acceptance criterion: `cargo check --manifest-path apps/ose-cli/Cargo.toml` exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

- [x] Create `apps/ose-cli/src/cli.rs` (_New file_). Implement the `Cli` struct using `#[derive(Parser)]` (clap 4.6.1) and the `run() -> i32` function that parses args and dispatches to `commands::links::run_links_check`. Include:
  - Root flags: `--verbose`/`-v`, `--quiet`/`-q`, `--output`/`-o` (default `"text"`), `--no-color`
  - Subcommand: `links` → `check` (with `--content` flag, default `"apps/ose-web/content"`)
  - `run()` validates output format, dispatches subcommand, returns exit code 0/1/2 (same pattern as `rhino-cli` `cli.rs` [Repo-grounded])

  Acceptance criterion: `cargo test --manifest-path apps/ose-cli/Cargo.toml --tests` — all smoke tests pass (GREEN state).
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: All 9 smoke tests pass. Used `global = true` clap flags to match cobra PersistentFlags behavior. Delegated to swe-rust-dev.
  - **Files Changed**: `apps/ose-cli/src/main.rs`, `apps/ose-cli/src/lib.rs`, `apps/ose-cli/src/commands/mod.rs`, `apps/ose-cli/src/commands/links.rs`, `apps/ose-cli/src/cli.rs`

  _Suggested executor: `swe-rust-dev`_

### Step 1.4: Run integration tests (GREEN verification)

- [x] Run the full smoke test suite:

  ```bash
  cargo test --manifest-path apps/ose-cli/Cargo.toml --tests
  ```

  Acceptance criterion: exits 0; all tests in `tests/cli_smoke.rs` pass.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: 9 passed (3 suites, 0.21s).

  _Suggested executor: `swe-rust-dev`_

### Step 1.5: Run against real ose-web content (integration smoke)

- [x] Run the Rust binary against the real content directory to confirm Go-parity:

  ```bash
  cargo run --manifest-path apps/ose-cli/Cargo.toml -- links check --content apps/ose-web/content
  ```

  Acceptance criterion: exits 0 (assuming the Go version also exits 0 on this directory at baseline); output contains `"Link Check Complete"`.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Checked 3 links, 0 broken. Output contains "Link Check Complete" and "Broken: 0".

  _Suggested executor: `swe-rust-dev`_

### Step 1.6: Refactor (REFACTOR)

- [x] Run `cargo clippy --manifest-path apps/ose-cli/Cargo.toml --all-targets -- -D warnings` and fix
      all reported warnings.

  Acceptance criterion: `cargo clippy --manifest-path apps/ose-cli/Cargo.toml --all-targets -- -D warnings`
  exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Fixed unwrap_used in tests/cli_smoke.rs (replaced .unwrap() with .expect()). clippy "No issues found".

  _Suggested executor: `swe-rust-dev`_

- [x] Run `cargo fmt --manifest-path apps/ose-cli/Cargo.toml` to format all Rust source files.

  Acceptance criterion: `cargo fmt --manifest-path apps/ose-cli/Cargo.toml -- --check` exits 0
  (no changes needed).
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Formatted. -- --check exits 0.

  _Suggested executor: `swe-rust-dev`_

- [x] Verify all public items have doc comments (`missing_docs = "deny"` enforces this at compile time).

  Acceptance criterion: `cargo check --manifest-path apps/ose-cli/Cargo.toml` exits 0 with no
  `missing_docs` errors; `cargo test --manifest-path apps/ose-cli/Cargo.toml --tests` still passes.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: cargo check exits 0, no missing_docs errors. 9 smoke tests pass.

  _Suggested executor: `swe-rust-dev`_

### Step 1.7: Update apps/ose-cli/project.json

- [x] Overwrite `apps/ose-cli/project.json` with Rust Nx targets (replacing Go targets). Use absolute manifest path pattern from `rhino-cli/project.json` [Repo-grounded]:

  ```json
  {
    "name": "ose-cli",
    "sourceRoot": "apps/ose-cli",
    "projectType": "application",
    "tags": ["type:app", "platform:cli", "lang:rust", "domain:ose-platform"],
    "implicitDependencies": ["rust-commons"],
    "targets": {
      "build": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo build --release --manifest-path apps/ose-cli/Cargo.toml && mkdir -p apps/ose-cli/dist && cp apps/ose-cli/target/release/ose-cli apps/ose-cli/dist/ose-cli"
        },
        "outputs": ["{projectRoot}/dist", "{projectRoot}/target"]
      },
      "install": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo fetch --manifest-path apps/ose-cli/Cargo.toml"
        }
      },
      "fmt": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo fmt --manifest-path apps/ose-cli/Cargo.toml"
        }
      },
      "fmt:check": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo fmt --manifest-path apps/ose-cli/Cargo.toml -- --check"
        },
        "cache": true,
        "inputs": ["{projectRoot}/src/**/*.rs"]
      },
      "lint": {
        "executor": "nx:run-commands",
        "options": {
          "commands": [
            "cargo fmt --manifest-path apps/ose-cli/Cargo.toml -- --check",
            "cargo clippy --manifest-path apps/ose-cli/Cargo.toml --all-targets -- -D warnings"
          ],
          "parallel": false
        }
      },
      "deny:check": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo deny --manifest-path apps/ose-cli/Cargo.toml check"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/Cargo.lock", "{projectRoot}/deny.toml"]
      },
      "check:msrv": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo hack --manifest-path apps/ose-cli/Cargo.toml check --rust-version"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/src/**/*.rs"]
      },
      "run": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo run --manifest-path apps/ose-cli/Cargo.toml --"
        }
      },
      "typecheck": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo check --manifest-path apps/ose-cli/Cargo.toml --all-targets"
        }
      },
      "test:unit": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo test --manifest-path apps/ose-cli/Cargo.toml --lib"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/src/**/*.rs"]
      },
      "test:quick": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo llvm-cov --manifest-path apps/ose-cli/Cargo.toml --lib --fail-under-lines 90"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/src/**/*.rs"]
      },
      "test:integration": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo test --manifest-path apps/ose-cli/Cargo.toml --tests"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/src/**/*.rs", "{projectRoot}/tests/**/*.rs"]
      },
      "spec-coverage": {
        "executor": "nx:run-commands",
        "options": {
          "command": "echo 'Phase 0 — spec-coverage stubbed; cucumber harness is future work'"
        },
        "cache": true,
        "inputs": ["{projectRoot}/src/**/*.rs"]
      }
    }
  }
  ```

  Acceptance criterion: `npx nx run ose-cli:typecheck` exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: project.json overwritten with Rust targets. nx run ose-cli:typecheck exits 0.

### Step 1.8: Verify Nx targets work end-to-end

- [x] Build via Nx:

  ```bash
  npx nx run ose-cli:build
  ```

  Acceptance criterion: exits 0; binary present at `apps/ose-cli/dist/ose-cli`.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Compiled in 8.64s. Binary at apps/ose-cli/dist/ose-cli confirmed.

- [x] Test:unit via Nx:

  ```bash
  npx nx run ose-cli:test:unit
  ```

  Acceptance criterion: exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: 0 lib unit tests (all logic is in rust-commons). Exits 0.

- [x] Test:integration via Nx:

  ```bash
  npx nx run ose-cli:test:integration
  ```

  Acceptance criterion: exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: 9 smoke tests in tests/cli_smoke.rs pass. Exits 0.

- [x] Test:quick (coverage) via Nx:

  ```bash
  npx nx run ose-cli:test:quick
  ```

  Acceptance criterion: exits 0 (90% line coverage met for lib).
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Initial run failed (0 lib tests). Added 14 unit tests (7 in commands/links.rs, 7 in cli.rs via extracted dispatch fn). Final: 97.55% lib coverage. 14 passed.

- [x] Lint via Nx:

  ```bash
  npx nx run ose-cli:lint
  ```

  Acceptance criterion: exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Fixed formatting (cargo fmt) then nx run ose-cli:lint exits 0.

### Manual CLI Verification

Verify all output formats and exit code semantics match the acceptance criteria before committing.

- [x] Build the release binary:

  ```bash
  cargo build --manifest-path apps/ose-cli/Cargo.toml --release
  ```

  Acceptance criterion: exits 0; binary present at `apps/ose-cli/target/release/ose-cli`.
  - **Date**: 2026-05-25
  - **Status**: Completed

- [x] Verify text output (AC-4):

  ```bash
  cargo run --manifest-path apps/ose-cli/Cargo.toml -- links check --content apps/ose-web/content
  ```

  Acceptance criterion: exits 0; stdout contains `"Link Check Complete"` and `"Broken:   0"`.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Exits 0. Output: "Link Check Complete", "Broken: 0 link(s)", Checked: 3 links.

- [x] Verify JSON output (AC-6):

  ```bash
  cargo run --manifest-path apps/ose-cli/Cargo.toml -- links check --content apps/ose-web/content -o json | jq '{status, checked, broken, broken_links}'
  ```

  Acceptance criterion: exits 0; output is valid JSON containing all four keys (`status`, `checked`,
  `broken`, `broken_links`).
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Exits 0. Valid JSON: `{"status":"success","checked":3,"broken":0,"broken_links":[]}`. All four keys present.

- [x] Verify markdown output (AC-7):

  ```bash
  cargo run --manifest-path apps/ose-cli/Cargo.toml -- links check --content apps/ose-web/content -o markdown | head -10
  ```

  Acceptance criterion: exits 0; stdout starts with `# Link Check Report` and includes `## Summary`.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Exits 0. Output starts with `# Link Check Report` and includes `## Summary`.

- [x] Verify quiet mode suppresses stdout on success (AC-8):

  ```bash
  cargo run --manifest-path apps/ose-cli/Cargo.toml -- links check --content apps/ose-web/content --quiet
  ```

  Acceptance criterion: exits 0; stdout is empty.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Exits 0. stdout empty (stdout_len: 0).

- [x] Verify non-existent directory exits with code 1:

  ```bash
  cargo run --manifest-path apps/ose-cli/Cargo.toml -- links check --content /nonexistent 2>&1; echo "exit: $?"
  ```

  Acceptance criterion: output line `exit: 1` (or `exit: 2`) — non-zero exit on invalid content dir.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: exit: 1 confirmed.

### Step 1.9: Commit Phase 1

- [x] Stage and commit:

  ```bash
  git add apps/ose-cli/src/ apps/ose-cli/tests/ apps/ose-cli/Cargo.toml apps/ose-cli/rust-toolchain.toml apps/ose-cli/deny.toml apps/ose-cli/project.json
  git commit -m "feat(ose-cli): rewrite in Rust consuming rust-commons (Phase 1)"
  ```

  File classification:
  - New files: `apps/ose-cli/Cargo.toml`, `apps/ose-cli/rust-toolchain.toml`, `apps/ose-cli/deny.toml`,
    `apps/ose-cli/src/` (all Rust source), `apps/ose-cli/tests/` (all integration tests)
  - Modified file: `apps/ose-cli/project.json` — existing file updated to replace Go Nx targets with
    Rust equivalents (Go targets such as `build`, `lint`, `test:unit`, `test:quick` are removed and
    replaced with Rust/Cargo equivalents defined in Step 1.5)

  Acceptance criterion: commit exists; `git log --oneline -1` shows the commit message.

---

## Phase 2: Archive Go Source and Cleanup

### Step 2.1: Create archived/ose-cli/ and copy Go source

- [x] Create `archived/ose-cli/` (_New directory_):

  ```bash
  mkdir -p archived/ose-cli
  ```

- [x] Copy the Go source files to the archive (NOT using `git mv` to avoid losing the Rust files already in `apps/ose-cli/`):

  ```bash
  cp apps/ose-cli/main.go archived/ose-cli/
  cp -r apps/ose-cli/cmd archived/ose-cli/
  cp apps/ose-cli/go.mod archived/ose-cli/
  cp apps/ose-cli/go.sum archived/ose-cli/
  ```

  Acceptance criterion: `archived/ose-cli/main.go` exists; `archived/ose-cli/cmd/` directory exists.
  - **Date**: 2026-05-25
  - **Status**: Completed

### Step 2.2: Add a README to archived/ose-cli/

- [x] Create `archived/ose-cli/README.md` (_New file_):

  ```markdown
  # archived/ose-cli

  This directory contains the archived Go source of `apps/ose-cli/` prior to its Rust
  migration in 2026-05.

  The Go implementation was replaced by a Rust rewrite that consumes `libs/rust-commons/`.
  The Go library `libs/golang-link-commons/` (which this code depended on) is preserved in
  the active workspace until the `ayokoding-cli` Rust migration completes.

  Do not modify files in this directory. They are a historical snapshot only.
  ```

  Acceptance criterion: file exists.
  - **Date**: 2026-05-25
  - **Status**: Completed

### Step 2.3: Delete Go artifacts from apps/ose-cli/

- [x] Delete Go source and artifacts from `apps/ose-cli/` using `git rm`:

  ```bash
  git rm apps/ose-cli/main.go
  git rm -r apps/ose-cli/cmd/
  git rm apps/ose-cli/go.mod
  git rm apps/ose-cli/go.sum
  git rm -f apps/ose-cli/cover.out
  git rm -f apps/ose-cli/cover_spec.out
  git rm -f apps/ose-cli/dist/ose-cli
  git rm -f apps/ose-cli/dist/oseplatform-cli
  ```

  Note: If `cover.out`, `cover_spec.out`, `dist/ose-cli`, or `dist/oseplatform-cli` are gitignored (not tracked), use plain `rm` instead of `git rm -f`. Verify with `git status` after each deletion.

  Acceptance criterion: `git status` shows these files as deleted; `apps/ose-cli/` contains only Rust source, `project.json`, `rust-toolchain.toml`, `deny.toml`, `Cargo.toml`, `Cargo.lock`, `dist/ose-cli` (new Rust binary), and `target/`.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: git rm removed 10 tracked Go files. cover.out and cover_spec.out were gitignored (removed with plain rm).

### Step 2.4: Verify Rust build still works after Go file removal

- [x] Confirm the Rust build is unaffected:

  ```bash
  npx nx run ose-cli:build
  ```

  Acceptance criterion: exits 0; `apps/ose-cli/dist/ose-cli` is the Rust binary (not the old Go binary).
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: nx run ose-cli:build exits 0 (from cache). Binary confirmed at apps/ose-cli/dist/ose-cli.

### Step 2.5: Commit Phase 2

- [x] Stage archived files and commit:

  ```bash
  git add archived/ose-cli/
  git commit -m "chore(ose-cli): archive Go source to archived/ose-cli/ (Phase 2)"
  ```

  Acceptance criterion: commit exists with archived Go source.

### Step 2.6: Update in-progress README if needed

- [x] Check `plans/in-progress/README.md` for any references to `ose-cli` that need updating:

  ```bash
  grep -n "ose-cli" plans/in-progress/README.md
  ```

  If found, update the entry to reflect the plan is in progress. Acceptance criterion: file accurately reflects plan state.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Entry found; already reflects in-progress state. No update needed.

---

## Phase 3: Local Quality Gates

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes. This follows the root cause orientation principle — proactively fix preexisting errors encountered during work. Do not defer or skip existing issues. Commit preexisting fixes separately with appropriate conventional commit messages.

### Commit Guidelines

- [x] Commit changes thematically — group related changes into logically cohesive commits
- [x] Follow Conventional Commits format: `<type>(<scope>): <description>`
- [x] Split different domains/concerns into separate commits (e.g., Phase 0 commit, Phase 1 commit, Phase 2 commit, plus any preexisting fixes as their own commits)
- [x] Preexisting fixes get their own commits, separate from plan work
- [x] Do NOT bundle unrelated changes into a single commit

### Local Quality Gates (Before Push)

- [x] Run affected typecheck:

  ```bash
  npx nx affected -t typecheck
  ```

  Acceptance criterion: exits 0 for all affected projects.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: nx run ose-cli:typecheck exits 0. nx run rust-commons:typecheck exits 0.

- [x] Run affected linting:

  ```bash
  npx nx affected -t lint
  ```

  Acceptance criterion: exits 0 for all affected projects.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: nx run ose-cli:lint exits 0. nx run rust-commons:lint exits 0.

- [x] Run affected quick tests:

  ```bash
  npx nx affected -t test:quick
  ```

  Acceptance criterion: exits 0 for `ose-cli` and `rust-commons`; all other affected projects unchanged.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: ose-cli: 14 tests, 97.56% coverage. rust-commons: 34 tests, 96.65% coverage. Both exits 0.

- [x] Run affected spec-coverage:

  ```bash
  npx nx affected -t spec-coverage
  ```

  Acceptance criterion: exits 0 (stub echo passes for `ose-cli`).
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Both ose-cli and rust-commons spec-coverage stubs exit 0.

- [x] Fix ALL failures — including preexisting issues not caused by your changes.
- [x] Re-run failing checks to confirm resolution.
- [x] Verify zero failures before pushing.
  - **Notes**: No failures found. All gates pass: typecheck, lint, test:quick, spec-coverage.

---

## Phase 4: Post-Push CI Verification

### Post-Push CI Verification

- [x] Push changes to `main`:

  ```bash
  git push origin main
  ```

  Acceptance criterion: push accepted; GitHub confirms commits received.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Pushed 4 commits (Phase 0–3 + delivery.md progress). Push accepted.

- [x] Monitor ALL GitHub Actions workflows triggered by the push using:

  ```bash
  gh run list --limit 5
  ```

  Poll every 3 minutes: `gh run view <run-id> --json status,conclusion`
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: No push-triggered CI workflow exists for ose-cli/rust-commons paths. Web app workflows run on schedule only. crane-cli-integration.yml only fires on crane-cli/ path changes. Pre-push hook ran all quality gates locally (all passed).

- [x] Verify ALL CI checks pass — no exceptions. Acceptance criterion: all runs show `conclusion: success`.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Most recent workflow runs (for prior commits) all show conclusion: success. No new workflow runs triggered by this push (no applicable push path triggers).

- [x] If any CI check fails, fix immediately and push a follow-up commit. Acceptance criterion: follow-up commit resolves the failure before proceeding.
  - **Notes**: No failures to fix.

- [x] Do NOT proceed to Phase 5 until ALL GitHub Actions pass with zero failures.
  - **Notes**: Gate satisfied — no failures.

---

## Phase 5: Plan Archival

### Plan Archival

- [x] Verify ALL delivery checklist items in Phases 0–4 are ticked.
- [x] Verify ALL quality gates pass (local + CI).
- [x] Rename and move the plan folder using today's date as the completion date:

  ```bash
  git mv plans/in-progress/ose-cli-rust-migration/ plans/done/2026-05-25__ose-cli-rust-migration/
  ```

  (Replace `2026-05-25` with the actual completion date — use `date +%Y-%m-%d` to get today's date.)

  Acceptance criterion: `plans/done/YYYY-MM-DD__ose-cli-rust-migration/` directory exists; `plans/in-progress/ose-cli-rust-migration/` no longer exists.

- [x] Update `plans/in-progress/README.md` — remove the `ose-cli-rust-migration` entry if it was added.

  Acceptance criterion: file no longer references `ose-cli-rust-migration` as active.

- [x] Update `plans/done/README.md` — add the plan entry with completion date.

  Acceptance criterion: `plans/done/README.md` lists the completed plan.

- [x] Commit the archival:

  ```bash
  git commit -m "chore(plans): move ose-cli-rust-migration to done"
  ```

  Acceptance criterion: commit exists; `git log --oneline -1` shows the archival commit.
