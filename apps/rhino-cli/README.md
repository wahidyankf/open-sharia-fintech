# rhino-cli

**RHINO** – Repository Hygiene & INtegration Orchestrator

Command-line tools for repository management and automation. The canonical implementation is Rust (this crate). The Rust rewrite completed 2026-05-23 (the predecessor Go binary remains recoverable from git history).

## What is rhino-cli?

A Rust CLI binary delivering the same observable contract as the original Go implementation — same commands, same flags, same exit codes, same output formats (text / json / markdown). Built with `clap` (derive macros) and consuming the Gherkin specs in [`specs/apps/rhino/behavior/rhino-cli/gherkin/`](../../specs/apps/rhino/behavior/rhino-cli/gherkin/).

## Status

Production. All commands ported and byte-identical to the original Go binary across shadow-diff corpora. This crate forbids unsafe Rust in both `lib.rs` and `main.rs`; see [`code-quality-standards.md` §Unsafe Code Policy](../../docs/explanation/software-engineering/programming-languages/rust/code-quality-standards.md#unsafe-code-policy).

## Quick Start

```bash
# Build the release binary (Nx)
nx build rhino-cli

# Run the binary
cargo run --manifest-path apps/rhino-cli/Cargo.toml -- --help

# Echo a message
cargo run --manifest-path apps/rhino-cli/Cargo.toml -- --say "hello world"

# Reject invalid output format (exits 1)
cargo run --manifest-path apps/rhino-cli/Cargo.toml -- --output xml --help
```

## Installation

The crate is local to this monorepo. To produce a standalone binary:

```bash
cd apps/rhino-cli
cargo build --release
# Binary at apps/rhino-cli/target/release/rhino-cli
# Or via Nx: nx build rhino-cli → apps/rhino-cli/dist/rhino-cli
```

Toolchain is pinned to Rust 1.95.0 via `rust-toolchain.toml`; the first `cargo` call inside this crate auto-bootstraps the toolchain through `rustup`. MSRV is 1.88 (`cucumber 0.23.0` bound).

> **Note (C-06):** `rust-version = "1.88"` in `Cargo.toml` is the _minimum_ compiler version that can build this crate (MSRV). `channel = "1.95.0"` in `rust-toolchain.toml` is the _installed_ toolchain version used by developers and CI. Both are correct — installed ≥ MSRV is the invariant.

## Nx Targets

| Target             | Command                                                                                 |
| ------------------ | --------------------------------------------------------------------------------------- |
| `build`            | `cargo build --release` → `dist/rhino-cli`                                              |
| `lint`             | `cargo clippy --all-targets -- -D warnings`                                             |
| `typecheck`        | `cargo check --all-targets`                                                             |
| `test:unit`        | `cargo test --lib` (in-source `#[cfg(test)]` modules)                                   |
| `test:integration` | `cargo test --tests` (integration tests under `tests/`)                                 |
| `test:quick`       | `cargo llvm-cov --lib --lcov --fail-under-lines 90` (Phase 1 swaps to native validator) |
| `specs:coverage`   | Phase 0 stub; Phase 1 wires cucumber-rs spec consumption                                |
| `run`              | `cargo run --`                                                                          |
| `install`          | `cargo fetch`                                                                           |

## Global Flags

Global flags (see `src/cli.rs`):

- `--verbose, -v` — verbose output with timestamps
- `--quiet, -q` — quiet mode (errors only)
- `--output, -o text|json|markdown` — output format (default: text). Invalid values exit 1.
- `--no-color` — disable colored output
- `--say <msg>` — echo a message to stdout
- `--help, -h` — print help

## Specs: E2E Coverage Gap Detection

`specs e2e-coverage validate` detects Gherkin scenarios that `playwright-bdd`'s `missingSteps:
"skip-scenario"` setting silently converts to `test.fixme(...)` in generated `.spec.js` output,
checked against a per-project baseline manifest so only _new_ unbound scenarios fail the gate.

```bash
cargo run --manifest-path apps/rhino-cli/Cargo.toml -- specs e2e-coverage validate \
  --features "specs/**/*.feature" --features-gen .features-gen \
  --baseline e2e-coverage-baseline.json --project my-e2e-project
```

| Flag                   | Required | Description                                                                                       |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------- |
| `[PROJECT_DIR]`        | No       | Positional project directory; `--features-gen`/`--baseline` resolve relative to it (default: `.`) |
| `--features <GLOB>`    | Yes      | `.feature` glob(s) this project consumes (repeatable)                                             |
| `--features-gen <DIR>` | Yes      | Directory of `bddgen`-generated `.spec.js` output to scan for `test.fixme(`                       |
| `--baseline <PATH>`    | Yes      | Checked-in baseline manifest path                                                                 |
| `--project <NAME>`     | Yes      | Project name recorded on the baseline when generated via `--update-baseline`                      |
| `--update-baseline`    | No       | Snapshot the current unbound set to `--baseline` instead of validating against it                 |

Exit codes: `0` on pass (no new unbound scenarios beyond the baseline); non-zero when a new
`@e2e`-tagged scenario appears as `test.fixme` without a baseline entry, when a declared `@e2e`
scenario or `Scenario Outline` title is entirely absent from the generated `.spec.js` output (most
notably an `Examples:` table with zero data rows, which playwright-bdd renders no test at all for —
this is folded into the same new-gap/baseline flow as an ordinary unbound scenario, so
`--update-baseline` accepts it like any other gap once the underlying cause is understood and
either fixed or deliberately deferred), or when `--features-gen` names a directory that does not
exist (run `npx bddgen` first). See
[`e2e-coverage.feature`](../../specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature)
for the full behavior contract.

## Dependency Status

Reviewed 2026-05-23. Policy paths per [Dependency Bump Stability & Safety Policy](../../repo-governance/development/workflow/dependency-bump-policy.md).

| Dependency | Pinned | Latest | Path | Decision                                         |
| ---------- | ------ | ------ | ---- | ------------------------------------------------ |
| `chrono`   | 0.4.44 | 0.4.44 | A    | Bumped from 0.4.39; patch-only                   |
| `glob`     | 0.3.3  | 0.3.3  | A    | Bumped from 0.3.2; patch-only                    |
| `sha2`     | 0.11.0 | 0.11.0 | A    | Bumped from 0.10.9; only `{Digest, Sha256}` used |
| `tempfile` | 3.27.0 | 3.27.0 | A    | Bumped from 3.14.0; only `TempDir::new()` used   |

## See also

- Migration plan (completed 2026-05-23, `2026-05-23__rhino-cli-rust-rewrite`): documents the Go implementation that preceded this crate (recoverable from git history; not linked here since `plans/done/` is repo-specific and this crate's README is byte-identical across sibling repos)
- Gherkin specs (shared with Go binary): [`specs/apps/rhino/behavior/rhino-cli/gherkin/`](../../specs/apps/rhino/behavior/rhino-cli/gherkin/)
