# rhino-cli

**RHINO** – Repository Hygiene & INtegration Orchestrator

Command-line tools for repository management and automation. Canonical implementation is Rust (this crate); the predecessor Go binary is recoverable from git history.

## What is rhino-cli?

A Rust CLI binary with the same commands, flags, exit codes, and output formats (text / json / markdown) as the original Go implementation. Built with `clap` (derive macros), consuming the Gherkin specs in [`specs/apps/rhino/behavior/rhino-cli/gherkin/`](../../specs/apps/rhino/behavior/rhino-cli/gherkin/).

## Status

Production; byte-identical to the Go binary across shadow-diff corpora. Forbids unsafe Rust in both `lib.rs` and `main.rs`; see [`code-quality-standards.md` §Unsafe Code Policy](../../docs/explanation/software-engineering/programming-languages/rust/code-quality-standards.md#unsafe-code-policy).

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

Local to this monorepo. To produce a standalone binary:

```bash
cd apps/rhino-cli
cargo build --release
# Binary at apps/rhino-cli/target/release/rhino-cli
# Or via Nx: nx build rhino-cli → apps/rhino-cli/dist/rhino-cli
```

Toolchain pinned to Rust 1.95.0 via `rust-toolchain.toml`; the first `cargo` call auto-bootstraps it through `rustup`. MSRV is 1.88 (`cucumber 0.23.0` bound) — `Cargo.toml`'s `rust-version` is the minimum buildable compiler; `rust-toolchain.toml`'s `channel` is the installed version. Both are correct: installed ≥ MSRV is the invariant.

## Nx Targets

| Target             | Command                                                 |
| ------------------ | ------------------------------------------------------- |
| `build`            | `cargo build --release` → `dist/rhino-cli`              |
| `lint`             | `cargo clippy --all-targets -- -D warnings`             |
| `typecheck`        | `cargo check --all-targets`                             |
| `test:unit`        | `cargo test --lib` (in-source `#[cfg(test)]` modules)   |
| `test:integration` | `cargo test --tests` (integration tests under `tests/`) |
| `test:quick`       | `cargo llvm-cov --lib --lcov --fail-under-lines 90`     |
| `specs:coverage`   | Phase 0 stub; wires cucumber-rs later                   |
| `run`              | `cargo run --`                                          |
| `install`          | `cargo fetch`                                           |

## Global Flags

See `src/cli.rs`:

- `--verbose, -v` — timestamps
- `--quiet, -q` — errors only
- `--output, -o text|json|markdown` — default text; invalid values exit 1
- `--no-color` — disable color
- `--say <msg>` — echo to stdout
- `--help, -h` — print help

## Specs: E2E Coverage Gap Detection

`specs e2e-coverage validate` detects Gherkin scenarios that `playwright-bdd`'s `missingSteps:
"skip-scenario"` setting silently converts to `test.fixme(...)`, checked against a per-project
baseline manifest so only _new_ unbound scenarios fail the gate.

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
scenario or `Scenario Outline` title is entirely absent from the generated `.spec.js` output (e.g.
an `Examples:` table with zero data rows — folded into the same new-gap/baseline flow as an
ordinary unbound scenario), or when `--features-gen` names a directory that does not exist (run
`npx bddgen` first). See
[`e2e-coverage.feature`](../../specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature)
for the full behavior contract.

## Adding a Gherkin Scenario: Two Binding Sites

A new scenario anywhere under
[`specs/apps/rhino/behavior/rhino-cli/gherkin/`](../../specs/apps/rhino/behavior/rhino-cli/gherkin/README.md)
needs updating in **two** places, not one:

1. the relevant **unit-test module** (e.g. `src/commands/gate/emit.rs`'s `#[cfg(test)]` block) — a
   plain Rust unit test, not a step binding, and
2. **`tests/gate_specs.rs`** — the cucumber harness, the only place carrying actual
   `#[given]`/`#[when]`/`#[then]` step bindings.

The harness scans the entire feature directory regardless of which change a scenario belongs to, so
binding only the unit-test side leaves an undefined-step failure that surfaces on the next
`test:quick` / pre-push run. This has recurred; budget for both sites up front.

```bash
# Verify BEFORE committing — the narrower --lib filter will not catch it
cargo test --test gate_specs
```

**Author a scenario in the phase that creates its behavior, or an earlier one — never a later one.**
The harness requires a literal, _passing_ binding for every scenario at all times, so behavior that
does not exist yet cannot be bound truthfully.

## Dependency Status

Reviewed 2026-05-23 per [Dependency Bump Stability & Safety Policy](../../repo-governance/development/workflow/dependency-bump-policy.md).

| Dependency | Pinned | Path | Decision                               |
| ---------- | ------ | ---- | -------------------------------------- |
| `chrono`   | 0.4.44 | A    | Patch-only bump from 0.4.39            |
| `glob`     | 0.3.3  | A    | Patch-only bump from 0.3.2             |
| `sha2`     | 0.11.0 | A    | Bumped from 0.10.9; used API unchanged |
| `tempfile` | 3.27.0 | A    | Bumped from 3.14.0; used API unchanged |

## See also

- Migration plan (completed 2026-05-23, `2026-05-23__rhino-cli-rust-rewrite`): documents the preceding Go implementation (recoverable from git history; not linked here — `plans/done/` is repo-specific and this README is byte-identical across sibling repos)
- Gherkin specs (shared with Go binary): [`specs/apps/rhino/behavior/rhino-cli/gherkin/`](../../specs/apps/rhino/behavior/rhino-cli/gherkin/)
