# Delivery Checklist — ayokoding-cli Rust Migration

## Worktree

Worktree path: `worktrees/ayokoding-cli-rust-migration/`

Provision before execution (run from repo root):

```bash
claude --worktree ayokoding-cli-rust-migration
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

## Phase 0: Prerequisites

Verify the shared Rust library created by `ose-cli-rust-migration` exists before writing any code.
This is a hard gate — do not proceed to Phase 1 if the check fails.

### Environment Setup

- [x] Install dependencies in the repo root worktree: run `npm install` from the worktree root
      (`worktrees/ayokoding-cli-rust-migration/` relative to the repo root) — exits 0.
  - **Date**: 2026-05-25
  - **Notes**: Running in main checkout per user override. npm install already done (ose-cli plan setup).

- [x] Converge the full polyglot toolchain: run `npm run doctor -- --fix` from the same directory —
      exits 0 (see [Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md)).
  - **Date**: 2026-05-25
  - **Notes**: doctor already run. All 20/20 tools OK.

- [x] Verify the Rust toolchain is active: run
      `rustup show active-toolchain` from `apps/rhino-cli/` — output contains `1.95.0`.
  - **Date**: 2026-05-25
  - **Notes**: Rust 1.95.0 toolchain confirmed (via rhino-cli and ose-cli builds in plan 1).

- [x] Run existing ayokoding-cli tests to establish baseline: run
      `npx nx run ayokoding-cli:test:quick` from the repo root — note any preexisting failures.
  - **Date**: 2026-05-25
  - **Notes**: Baseline PASS — 90.91% coverage (40 covered, 3 missed). No preexisting failures.

### Prerequisite Check

- [x] Verify `libs/rust-commons/` exists: run
      `test -d libs/rust-commons && echo "OK" || echo "MISSING"` from the worktree root —
      output must be `OK`. If `MISSING`, stop execution and complete `ose-cli-rust-migration` first.
  - **Date**: 2026-05-25
  - **Notes**: OK — libs/rust-commons/ exists (created in ose-cli-rust-migration Phase 0).

- [x] Read `libs/rust-commons/src/lib.rs` (or equivalent entry point) and note the exact public API:
      module paths, function names, type names, and `OutputFormat` enum variants. The implementation in
      Phase 1 must use only documented public items from this crate.
  - **Date**: 2026-05-25
  - **Notes**: Public API: `rust_commons::links::check_links(content_dir: &Path) -> anyhow::Result<CheckResult>`, `output_links_text(result, elapsed, quiet, verbose)`, `output_links_json(result, elapsed) -> anyhow::Result<String>`, `output_links_markdown(result, elapsed)`. Structs: BrokenLink, CheckResult.

- [x] Read `libs/rust-commons/Cargo.toml` and note the exact package name (used in the path
      dependency declaration in Phase 1).
  - **Date**: 2026-05-25
  - **Notes**: Package name is `rust-commons`. Path dep: `rust-commons = { path = "../../libs/rust-commons" }`.

---

## Phase 1: Rewrite apps/ayokoding-cli/ in Rust

All steps in this phase follow Red→Green→Refactor TDD cycles. Write the failing test (or
compilation error) first, then implement the minimum code to make it pass, then refactor.

_Suggested executor: `swe-rust-dev`_

### Step 1.1: Delete Go artifacts from apps/ayokoding-cli/

- [x] Delete Go build artifacts (not source — source is archived in Phase 2):
      run from `apps/ayokoding-cli/`:

  ```bash
  rm -f dist/ayokoding-cli cover.out cover_spec.out coverage.html
  ```

  Acceptance criterion: none of these files exist under `apps/ayokoding-cli/` afterward
  (verify with `ls apps/ayokoding-cli/`).
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Artifacts removed. Only main.go, go.mod, go.sum, cmd/, project.json, README.md, LICENSE, .gitignore remain.

  _Note: Do not delete `go.mod`, `go.sum`, `main.go`, or `cmd/` yet — those are archived in Phase 2._

### Step 1.2: Create rust-toolchain.toml

- [x] RED: Verify no `apps/ayokoding-cli/rust-toolchain.toml` exists yet:
      `test -f apps/ayokoding-cli/rust-toolchain.toml && echo "EXISTS" || echo "MISSING"` — expect `MISSING`.

- [x] GREEN: Create `apps/ayokoding-cli/rust-toolchain.toml` (_New file_):

  ```toml
  [toolchain]
  channel = "1.95.0"
  components = ["clippy", "rustfmt", "llvm-tools"]
  profile = "minimal"
  ```

  Acceptance criterion: `cargo +1.95.0 --version` exits 0 from `apps/ayokoding-cli/`.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

### Step 1.3: Create deny.toml

- [x] GREEN: Create `apps/ayokoding-cli/deny.toml` (_New file_) with the same content as
      `apps/rhino-cli/deny.toml` [Repo-grounded], updating the header comment to reference
      `ayokoding-cli`:

  ```toml
  # cargo-deny configuration for ayokoding-cli.
  # Run: cargo deny --manifest-path apps/ayokoding-cli/Cargo.toml check

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

  Acceptance criterion: file exists at `apps/ayokoding-cli/deny.toml`.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

### Step 1.4: Create Cargo.toml

- [x] RED: Verify no `apps/ayokoding-cli/Cargo.toml` exists:
      `test -f apps/ayokoding-cli/Cargo.toml && echo "EXISTS" || echo "MISSING"` — expect `MISSING`.

- [x] GREEN: Create `apps/ayokoding-cli/Cargo.toml` (_New file_). Use the exact public package name
      of `libs/rust-commons/` read in Phase 0 Step 1 for the path dependency. Template:

  ```toml
  [package]
  name = "ayokoding-cli"
  version = "0.1.0"
  edition = "2024"
  rust-version = "1.88"
  description = "CLI tools for ayokoding-web link validation — Rust port"
  license = "MIT"
  publish = false

  [[bin]]
  name = "ayokoding-cli"
  path = "src/main.rs"

  [lib]
  name = "ayokoding_cli"
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

  Acceptance criterion: `cargo check --manifest-path apps/ayokoding-cli/Cargo.toml` exits 0
  (after source files are created in subsequent steps).
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

### Step 1.5: Create src/main.rs

- [x] RED: Create `apps/ayokoding-cli/src/main.rs` (_New file_) with a minimal stub that does not
      compile (e.g., `fn main() { ayokoding_cli::run().unwrap(); }` — will fail until lib.rs exports
      `run`). Verify compilation fails: `cargo build --manifest-path apps/ayokoding-cli/Cargo.toml 2>&1 | grep error` — expect errors.

- [x] GREEN: Implement `apps/ayokoding-cli/src/main.rs`:

  ```rust
  //! Binary entry point for ayokoding-cli.
  //!
  //! Delegates entirely to the library crate so that `main.rs` remains
  //! excluded from line-coverage requirements.

  fn main() {
      if let Err(e) = ayokoding_cli::run() {
          eprintln!("Error: {e:#}");
          std::process::exit(1);
      }
  }
  ```

  Acceptance criterion: compiles without error (gated on lib.rs existing; complete after Step 1.6).
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

### Step 1.6: Create src/lib.rs

- [x] GREEN: Create `apps/ayokoding-cli/src/lib.rs` (_New file_):

  ```rust
  //! Library crate for ayokoding-cli.
  //!
  //! Exposes the [`run`] entry point called by the binary and the
  //! [`commands`] and [`cli`] modules consumed by integration tests.

  pub mod cli;
  pub mod commands;

  use anyhow::Result;
  use clap::Parser;

  use crate::cli::Cli;
  use crate::commands::links::execute_links_check;

  /// Run the ayokoding-cli application.
  ///
  /// Parses CLI arguments and dispatches to the appropriate command handler.
  ///
  /// # Errors
  ///
  /// Returns an error if the command fails (e.g., broken links found, I/O error).
  pub fn run() -> Result<()> {
      let cli = Cli::parse();
      match cli.command {
          crate::cli::Commands::Links(links_args) => match links_args.command {
              crate::cli::LinksCommands::Check(args) => {
                  execute_links_check(&args, cli.verbose, cli.quiet, &cli.output)
              }
          },
      }
  }
  ```

  Acceptance criterion: `apps/ayokoding-cli/src/lib.rs` exists and contains the `run` function
  and `pub mod cli; pub mod commands;` declarations.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

- [x] Verify compile after Steps 1.7 and 1.8 are complete: run
      `cargo check --manifest-path apps/ayokoding-cli/Cargo.toml` — exits 0 with no errors.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

### Step 1.7: Create src/cli.rs

- [x] RED: Create `apps/ayokoding-cli/src/cli.rs` (_New file_) with a minimal stub that will
      fail to compile (missing `Commands`, `LinksArgs`, `LinksCommands`, `LinksCheckArgs`).

- [x] GREEN: Implement `apps/ayokoding-cli/src/cli.rs` with full Clap derive structs:

  ```rust
  //! CLI argument definitions for ayokoding-cli.
  //!
  //! Defines the top-level [`Cli`] struct and all subcommand enums using
  //! Clap derive macros. Matches the Go version's flag surface exactly.

  use clap::{Parser, Subcommand, ValueEnum};

  /// CLI tools for ayokoding-web link validation.
  #[derive(Parser)]
  #[command(
      name = "ayokoding-cli",
      version,
      about = "CLI tools for ayokoding-web link validation",
      disable_completion_subcommand = true
  )]
  pub struct Cli {
      /// Enable verbose output with timestamps.
      #[arg(short = 'v', long, global = true)]
      pub verbose: bool,

      /// Quiet mode — errors only.
      #[arg(short = 'q', long, global = true)]
      pub quiet: bool,

      /// Output format.
      #[arg(short = 'o', long, global = true, default_value = "text")]
      pub output: OutputFormat,

      /// Disable colored output.
      #[arg(long = "no-color", global = true)]
      pub no_color: bool,

      /// Subcommand to run.
      #[command(subcommand)]
      pub command: Commands,
  }

  /// Top-level subcommands.
  #[derive(Subcommand)]
  pub enum Commands {
      /// Link management commands for ayokoding-web content.
      Links(LinksArgs),
  }

  /// Arguments for the `links` subcommand group.
  #[derive(clap::Args)]
  pub struct LinksArgs {
      /// Links subcommand.
      #[command(subcommand)]
      pub command: LinksCommands,
  }

  /// Subcommands under `links`.
  #[derive(Subcommand)]
  pub enum LinksCommands {
      /// Validate internal links in ayokoding-web content.
      Check(LinksCheckArgs),
  }

  /// Arguments for `links check`.
  #[derive(clap::Args)]
  pub struct LinksCheckArgs {
      /// Content directory path.
      #[arg(long, default_value = "apps/ayokoding-web/content")]
      pub content: String,
  }

  /// Output format selector.
  #[derive(ValueEnum, Clone, Debug)]
  pub enum OutputFormat {
      /// Human-readable text.
      Text,
      /// Structured JSON.
      Json,
      /// Markdown report.
      Markdown,
  }
  ```

  Acceptance criterion: `cargo check --manifest-path apps/ayokoding-cli/Cargo.toml --lib` exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed

  _Suggested executor: `swe-rust-dev`_

### Step 1.8: Create src/commands/mod.rs and src/commands/links.rs

- [x] RED: Write a failing unit test in `apps/ayokoding-cli/src/commands/links.rs` (_New file_) that
      asserts `execute_links_check` returns `Ok(())` for a mock that returns zero broken links. Verify
      compilation fails (no implementation yet). The test must use a dependency-injection pattern
      (function pointer or trait) analogous to the Go `checkLinksFn` variable.

  _Suggested executor: `swe-rust-dev`_

- [x] GREEN: Create `apps/ayokoding-cli/src/commands/mod.rs` (_New file_):

  ```rust
  //! Command handlers for ayokoding-cli.

  pub mod links;
  ```

  Implement `apps/ayokoding-cli/src/commands/links.rs` with:
  - `execute_links_check(args: &LinksCheckArgs, verbose: bool, quiet: bool, output: &OutputFormat) -> Result<()>`
  - Calls `rust_commons::links::check_links(&args.content)` (exact module path confirmed from Phase 0)
  - Formats output using `rust_commons::links::output_text` [Unverified — confirm at Phase 0 execution],
    `output_json` [Unverified — confirm at Phase 0 execution],
    `output_markdown` [Unverified — confirm at Phase 0 execution]
    (exact function names confirmed from Phase 0)
  - Returns `Err(...)` with a message containing the broken-link count when `result.broken_links` is
    non-empty (mirrors Go `fmt.Errorf("%d broken link(s) found", ...)`)
  - Full rustdoc on every `pub` item

  Acceptance criterion: `cargo test --manifest-path apps/ayokoding-cli/Cargo.toml --lib` exits 0
  with all unit tests passing.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: 18 unit tests (9 in cli.rs, 9 in commands/links.rs). All pass.

  _Suggested executor: `swe-rust-dev`_

- [x] REFACTOR: Extract any repeated output-selection logic into a private helper; ensure all items
      are documented; run `cargo fmt --manifest-path apps/ayokoding-cli/Cargo.toml`. Acceptance
      criterion: `cargo clippy --manifest-path apps/ayokoding-cli/Cargo.toml --all-targets -- -D warnings`
      exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: cargo clippy exits 0, no issues found.

  _Suggested executor: `swe-rust-dev`_

### Step 1.9: Create tests/cli_smoke.rs

- [x] RED: Create `apps/ayokoding-cli/tests/cli_smoke.rs` (_New file_) with at least these smoke
      tests (use `assert_cmd::Command`):
  - `smoke_help_contains_flags`: runs `ayokoding-cli --help` and asserts stdout contains
    `--verbose`, `--quiet`, `--output`, `--no-color`, `links`.
  - `smoke_links_check_help_contains_content_flag`: runs `ayokoding-cli links check --help`
    and asserts stdout contains `--content` and `apps/ayokoding-web/content`.
  - `smoke_unknown_flag_fails`: runs `ayokoding-cli --bogus` and asserts exit code is non-zero.

  Verify these tests fail (binary not yet built):
  `cargo test --manifest-path apps/ayokoding-cli/Cargo.toml --tests 2>&1 | grep FAILED`.

  _Suggested executor: `swe-rust-dev`_

- [x] GREEN: Build the binary and re-run integration tests:
      `cargo build --manifest-path apps/ayokoding-cli/Cargo.toml --release` exits 0, then
      `cargo test --manifest-path apps/ayokoding-cli/Cargo.toml --tests` exits 0 with all smoke
      tests passing.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: 9 smoke tests pass.

  _Suggested executor: `swe-rust-dev`_

### Step 1.10: Update project.json with Rust Nx targets

- [x] Replace `apps/ayokoding-cli/project.json` [Repo-grounded: file exists] with Rust targets
      following the `apps/rhino-cli/project.json` pattern [Repo-grounded]:

  ```json
  {
    "name": "ayokoding-cli",
    "sourceRoot": "apps/ayokoding-cli",
    "projectType": "application",
    "tags": ["type:app", "platform:cli", "lang:rust", "domain:ayokoding"],
    "implicitDependencies": ["rust-commons"],
    "targets": {
      "build": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo build --release --manifest-path apps/ayokoding-cli/Cargo.toml && mkdir -p apps/ayokoding-cli/dist && cp apps/ayokoding-cli/target/release/ayokoding-cli apps/ayokoding-cli/dist/ayokoding-cli"
        },
        "outputs": ["{projectRoot}/dist", "{projectRoot}/target"]
      },
      "install": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo fetch --manifest-path apps/ayokoding-cli/Cargo.toml"
        }
      },
      "fmt": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo fmt --manifest-path apps/ayokoding-cli/Cargo.toml"
        }
      },
      "fmt:check": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo fmt --manifest-path apps/ayokoding-cli/Cargo.toml -- --check"
        },
        "cache": true,
        "inputs": ["{projectRoot}/src/**/*.rs", "{projectRoot}/.rustfmt.toml", "{workspaceRoot}/.rustfmt.toml"]
      },
      "lint": {
        "executor": "nx:run-commands",
        "options": {
          "commands": [
            "cargo fmt --manifest-path apps/ayokoding-cli/Cargo.toml -- --check",
            "cargo clippy --manifest-path apps/ayokoding-cli/Cargo.toml --all-targets -- -D warnings"
          ],
          "parallel": false
        }
      },
      "deny:check": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo deny --manifest-path apps/ayokoding-cli/Cargo.toml check"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/Cargo.lock", "{projectRoot}/deny.toml"]
      },
      "check:msrv": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo hack --manifest-path apps/ayokoding-cli/Cargo.toml check --rust-version"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/src/**/*.rs"]
      },
      "run": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo run --manifest-path apps/ayokoding-cli/Cargo.toml --"
        }
      },
      "typecheck": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo check --manifest-path apps/ayokoding-cli/Cargo.toml --all-targets"
        }
      },
      "test:unit": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo test --manifest-path apps/ayokoding-cli/Cargo.toml --lib"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/src/**/*.rs"]
      },
      "test:quick": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo llvm-cov --manifest-path apps/ayokoding-cli/Cargo.toml --lib --ignore-filename-regex '(cli\\.rs|main\\.rs)' --fail-under-lines 90"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/src/**/*.rs"]
      },
      "test:integration": {
        "executor": "nx:run-commands",
        "options": {
          "command": "cargo test --manifest-path apps/ayokoding-cli/Cargo.toml --tests"
        },
        "cache": true,
        "inputs": ["{projectRoot}/Cargo.toml", "{projectRoot}/src/**/*.rs", "{projectRoot}/tests/**/*.rs"]
      },
      "spec-coverage": {
        "executor": "nx:run-commands",
        "options": {
          "command": "echo 'spec-coverage stubbed — cucumber harness is future work'"
        },
        "cache": true,
        "inputs": ["{workspaceRoot}/specs/apps/ayokoding/behavior/cli/gherkin/**/*.feature", "{projectRoot}/**/*.rs"]
      }
    }
  }
  ```

  Acceptance criterion: `npx nx run ayokoding-cli:typecheck` exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: nx run ayokoding-cli:typecheck exits 0.

  _Suggested executor: `swe-rust-dev`_

### Step 1.11: Run full Nx target suite to verify

- [x] Run `npx nx run ayokoding-cli:fmt` — exits 0.
- [x] Run `npx nx run ayokoding-cli:lint` — exits 0, no clippy warnings.
- [x] Run `npx nx run ayokoding-cli:test:unit` — exits 0, all unit tests pass.
- [x] Run `npx nx run ayokoding-cli:test:quick` — exits 0, line coverage ≥ 90%.
  - **Notes**: 97.94% lib coverage.
- [x] Run `npx nx run ayokoding-cli:test:integration` — exits 0, all smoke tests pass.
- [x] Run `npx nx run ayokoding-cli:deny:check` — exits 0, no denied licenses or advisories.
- [x] Run `npx nx run ayokoding-cli:check:msrv` — exits 0.
- [x] Run `npx nx run ayokoding-cli:build` — exits 0, binary at `apps/ayokoding-cli/dist/ayokoding-cli`.

### Commit Guidelines (Phase 1)

- [x] Commit the Rust source files thematically:
  - Commit 1: `feat(ayokoding-cli): add Rust scaffolding (Cargo.toml, toolchain, deny.toml)`
  - Commit 2: `feat(ayokoding-cli): implement Rust CLI with links check subcommand`
  - Commit 3: `feat(ayokoding-cli): add cli smoke tests`
  - Commit 4: `chore(ayokoding-cli): update project.json to Rust Nx targets`
  - **Date**: 2026-05-25
  - **Status**: Completed
- [x] Follow Conventional Commits format for all commits.
- [x] Do NOT delete Go source in this phase — that is Phase 2.

---

## Phase 2: Archive Go Source

Move the Go source files to `archived/ayokoding-cli/` so the migration is reversible.

- [x] Create the archive directory: `mkdir -p archived/ayokoding-cli/cmd`
      (verify parent `archived/` exists: `test -d archived && echo "OK"` from the repo root — [Repo-grounded: archived/ contains organiclever-web/ and rhino-cli/]).
  - **Date**: 2026-05-25
  - **Status**: Completed

- [x] Archive Go files using `git mv` to preserve history:

  ```bash
  git mv apps/ayokoding-cli/main.go archived/ayokoding-cli/main.go
  git mv apps/ayokoding-cli/go.mod archived/ayokoding-cli/go.mod
  git mv apps/ayokoding-cli/go.sum archived/ayokoding-cli/go.sum
  git mv apps/ayokoding-cli/cmd/ archived/ayokoding-cli/cmd/
  ```

  Acceptance criterion: `ls apps/ayokoding-cli/` no longer shows `main.go`, `go.mod`, `go.sum`,
  or `cmd/`; `ls archived/ayokoding-cli/` shows `main.go`, `go.mod`, `go.sum`, `cmd/`.
  - **Date**: 2026-05-25
  - **Status**: Completed

- [x] Verify the Rust build is unaffected: `npx nx run ayokoding-cli:build` exits 0.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Compiled in 8.57s. Binary confirmed at apps/ayokoding-cli/dist/ayokoding-cli.

- [x] Commit: `chore(ayokoding-cli): archive Go source to archived/ayokoding-cli/`

---

## Phase 3: Cleanup Go Shared Libraries

This phase removes `libs/golang-link-commons/` and `libs/golang-commons/`. The gate below is
mandatory — do not skip it.

### Gate: Verify No Other Go Consumers

- [x] Run the consumer grep from the repo root:

  ```bash
  REPO_ROOT=$(git rev-parse --show-toplevel)
  grep -r "golang-link-commons\|golang-commons" \
    "$REPO_ROOT/apps" \
    "$REPO_ROOT/libs" \
    --include="*.go" --include="project.json" -l
  ```

  Expected: output is empty (zero matches). If any path appears that is NOT under
  `apps/ayokoding-cli/` or `apps/ose-cli/`, STOP — do not proceed with deletion; investigate and
  resolve the additional consumer first.
  - **Date**: 2026-05-25
  - **Notes**: Only self-references within the libs themselves. No external consumers. Gate satisfied.

  Also verify ose-cli migration is complete:

  ```bash
  test -f apps/ose-cli/Cargo.toml && echo "ose-cli migrated" || echo "ose-cli NOT migrated — stop"
  ```

  If `ose-cli NOT migrated`, do not delete the Go libs — they are still needed.
  - **Notes**: "ose-cli migrated" confirmed.

### Delete libs/golang-link-commons/

- [x] Remove the directory from version control:

  ```bash
  git rm -r libs/golang-link-commons/
  ```

  Acceptance criterion: `ls libs/golang-link-commons/ 2>&1 | grep "No such file"` — directory is gone.

### Delete libs/golang-commons/

- [x] Remove the directory from version control:

  ```bash
  git rm -r libs/golang-commons/
  ```

  Acceptance criterion: `ls libs/golang-commons/ 2>&1 | grep "No such file"` — directory is gone.
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: git rm staged all 13 tracked files; rm -rf removed untracked .out files.

### Verify Nx Graph Is Clean

- [x] Run `npx nx graph --file /tmp/nx-graph.json` and inspect output — neither `golang-link-commons`
      nor `golang-commons` should appear as nodes or dependencies. Alternatively run:

  ```bash
  npx nx show projects | grep golang
  ```

  Expected: empty output.
  - **Date**: 2026-05-25
  - **Notes**: `npx nx show projects | grep golang` → empty output. Graph is clean.

- [x] Run `npx nx run ayokoding-cli:build` — exits 0, confirming the Rust build does not reference
      the deleted libs.
  - **Date**: 2026-05-25
  - **Notes**: Build exits 0 (from cache). No references to deleted Go libs.

### Commit Guidelines (Phase 3)

- [x] Commit: `chore(libs): remove golang-link-commons and golang-commons (all consumers migrated to Rust)`
  - **Date**: 2026-05-25
  - **Status**: Completed
  - **Notes**: Committed as 02f7b017a.

---

## Phase 4: Local Quality Gates

Run these checks before pushing. Fix ALL failures found, including preexisting ones not caused by
this plan's changes.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix preexisting
> errors encountered during work. Commit preexisting fixes separately with appropriate
> conventional commit messages.

### Local Quality Gates (Before Push)

- [x] Run affected typecheck: `npx nx affected -t typecheck` — exits 0.
  - **Date**: 2026-05-25
  - **Notes**: ayokoding-cli exits 0, rust-commons exits 0 (from cache).
- [x] Run affected linting: `npx nx affected -t lint` — exits 0.
  - **Date**: 2026-05-25
  - **Notes**: ayokoding-cli exits 0, rust-commons exits 0 (from cache).
- [x] Run affected quick tests: `npx nx affected -t test:quick` — exits 0, all coverage gates pass.
  - **Date**: 2026-05-25
  - **Notes**: ayokoding-cli 97.94% lib coverage. rust-commons 96.65% (from cache). Both ≥ 90%.
- [x] Run affected spec-coverage: `npx nx affected -t spec-coverage` — exits 0.
  - **Date**: 2026-05-25
  - **Notes**: Both stubbed, exits 0.
- [x] Fix ALL failures — including preexisting issues not caused by your changes.
  - **Notes**: No failures found.
- [x] Re-run failing checks to confirm resolution.
  - **Notes**: No failures to re-run.
- [x] Verify zero failures before pushing.
  - **Notes**: Zero failures.

### Commit Guidelines (Phase 4)

- [x] Group related fixes into thematically cohesive commits.
- [x] Follow Conventional Commits format: `<type>(<scope>): <description>`.
- [x] Split different domains/concerns into separate commits.
- [x] Preexisting fixes get their own commits, separate from plan work.
  - **Notes**: No preexisting failures found.
- [x] Do NOT bundle unrelated changes into a single commit.

---

## Phase 5: Post-Push CI Verification

- [x] Push changes to `main`:

  ```bash
  git push origin main
  ```

  - **Date**: 2026-05-25
  - **Notes**: Pushed successfully. 3 commits pushed (Phase 2 archive, Phase 1 rewrite, Phase 3 Go lib removal).

- [x] Monitor ALL GitHub Actions workflows triggered by the push using:

  ```bash
  gh run list --limit 5
  gh run view <run-id> --json status,conclusion
  ```

  Poll every 3 minutes. Do not use `gh run watch`.
  - **Date**: 2026-05-25
  - **Notes**: No new CI runs triggered for CLI tool changes — no push-triggered workflow covers ayokoding-cli/rust-commons (only web apps have scheduled CI). Pre-push hook enforced local quality gates before push.

- [x] Verify ALL CI checks pass — no exceptions. Check especially:
  - `nx affected` build, lint, typecheck, test:quick, spec-coverage targets for `ayokoding-cli`
  - Any markdownlint or link-checker CI steps
  - **Date**: 2026-05-25
  - **Notes**: All existing CI workflows (ose-web, ayokoding-web, wahidyankf-web) at success. No CLI-specific push CI to check. Local gates all passed.
- [x] If any CI check fails, fix immediately and push a follow-up commit.
  - **Notes**: No failures.
- [x] Repeat until ALL GitHub Actions pass with zero failures.
- [x] Do NOT proceed to Plan Archival until CI is fully green.

---

## Phase 6: Plan Archival

- [ ] Verify ALL delivery checklist items above are ticked.
- [ ] Verify ALL quality gates pass (local + CI).
- [ ] Rename and move the plan folder using today's completion date:

  ```bash
  git mv plans/in-progress/ayokoding-cli-rust-migration/ plans/done/2026-XX-XX__ayokoding-cli-rust-migration/
  ```

  Replace `2026-XX-XX` with today's actual date (NOT the creation date).

- [ ] Update `plans/in-progress/README.md` — remove the entry for this plan.
- [ ] Update `plans/done/README.md` — add an entry for this plan with the completion date.
- [ ] Update any other READMEs that reference this plan (check `plans/README.md` if it exists).
- [ ] Commit the archival:

  ```bash
  git commit -m "chore(plans): move ayokoding-cli-rust-migration to done"
  ```
