# rhino-cli

**RHINO** – Repository Hygiene & INtegration Orchestrator

Command-line tools for repository management and automation. Canonical implementation is F# (this
project); the predecessor Rust crate and, before that, the original Go binary are recoverable from
git history.

## What is rhino-cli?

An F# CLI binary with the same commands, flags, exit codes, and output formats (text / json /
markdown) as the retired Rust and Go implementations it replaced. Built with `Argu`
(declarative argument parsing) across four projects — `RhinoCli.Domain`, `RhinoCli.Infrastructure`,
`RhinoCli.Application`, `RhinoCli.Cli` — plus the `RhinoCli.Program` entry point, consuming the
Gherkin specs in
[`specs/apps/rhino/cli/behaviors/`](../../specs/apps/rhino/cli/behaviors/).

## Status

Production. Ported 1:1 from the Rust crate scenario-by-scenario (`rewrite-rhino-cli-to-fsharp`
plan); `shadow-diff.sh` proved byte-identical stdout/stderr/exit-code behavior against the Rust
binary for every namespace before each wave's flip, and `parity manifest validate` now guards
byte-identity of this app's own tree against its checked-in SHA-256 manifest going forward.

## Quick Start

```bash
# Build the self-contained release binary (Nx)
nx build rhino-cli

# Run via dotnet (no prior build required)
dotnet run --project apps/rhino-cli/src/RhinoCli.Program/RhinoCli.Program.fsproj -- --help

# Echo a message
dotnet run --project apps/rhino-cli/src/RhinoCli.Program/RhinoCli.Program.fsproj -- --say "hello world"

# Reject invalid output format (exits 1)
dotnet run --project apps/rhino-cli/src/RhinoCli.Program/RhinoCli.Program.fsproj -- --output xml --help
```

## Installation

Local to this monorepo. To produce a standalone, self-contained binary:

```bash
nx build rhino-cli
# Binary at apps/rhino-cli/src/dist/rhino-cli-fsharp
```

SDK pinned to .NET 10.0.204 via `apps/rhino-cli/global.json` (`rollForward: latestMinor`).
`apps/rhino-cli/scripts/rhino-bin.sh` is the resolver shim every generated gate command invokes: it
prefers an explicit `RHINO_CLI_FSHARP_BIN` override, falls back to the published `dist` binary, and
only shells to `dotnet run` (needing the SDK) as a last resort.

## Nx Targets

| Target                       | Command                                                                           |
| ---------------------------- | --------------------------------------------------------------------------------- |
| `build`                      | `dotnet publish RhinoCli.Program.fsproj -c Release --self-contained` → `src/dist` |
| `lint`                       | `fantomas --check` + `fsharplint` + `fsharp-analyzers` across all five projects   |
| `typecheck`                  | `dotnet build RhinoCli.Program.fsproj --no-restore`                               |
| `test:unit`                  | `dotnet test RhinoCli.UnitTests.fsproj` (TickSpec step definitions + plain xunit) |
| `test:integration`           | `dotnet test RhinoCli.IntegrationTests.fsproj`                                    |
| `test:coverage`              | `dotnet test` with `/p:CollectCoverage=true /p:Threshold=90` (per-module minimum) |
| `test:quick`                 | `typecheck` → `lint` → `test:unit` → `test:specs`, in order                       |
| `specs:structure-validation` | `rhino-cli specs structure validate`                                              |
| `specs:behavior:coverage`    | `rhino-cli specs behavior-coverage validate` — every scenario needs a bound step  |
| `run`                        | `dotnet run --project RhinoCli.Program.fsproj --`                                 |
| `install`                    | `dotnet restore RhinoCli.Program.fsproj`                                          |
| `deps:audit`                 | `scripts/dotnet-deps-audit.sh` (NuGet vulnerability scan)                         |

See `apps/rhino-cli/project.json` for the full target set, including the cross-cutting governance
and env validators this project also owns (`governance:*`, `env:validation`,
`specs:gherkin-cardinality-validation`).

## Global Flags

See `src/RhinoCli.Cli/src/HelpText.fs`:

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
dotnet run --project apps/rhino-cli/src/RhinoCli.Program/RhinoCli.Program.fsproj -- specs e2e-coverage validate \
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
[`e2e-coverage.feature`](../../specs/apps/rhino/cli/behaviors/specs/e2e-coverage.feature)
for the full behavior contract.

## Adding a Gherkin Scenario: One Binding Site

A new scenario anywhere under
[`specs/apps/rhino/cli/behaviors/`](../../specs/apps/rhino/cli/behaviors/README.md)
needs exactly one binding: a `[<Given>]`/`[<When>]`/`[<Then>]`-style method on the relevant
`*Steps.fs` class under `src/tests/unit/Steps/`, discovered by
[TickSpec](https://github.com/fsprojects/TickSpec) at test-run time. Unlike the retired Rust
crate's two-site model (a `#[cfg(test)]` unit test plus a separate `tests/gate_specs.rs` cucumber
binding), F#'s TickSpec step classes are both the binding and the executable assertion — there is
no second file to keep in sync.

`specs:behavior:coverage validate` is the enforcement mechanism: it fails if any scenario under the
shared Gherkin tree lacks a bound step, so an unbound scenario surfaces on the next `test:quick` /
pre-push run rather than silently passing.

```bash
# Verify BEFORE committing
nx run rhino-cli:test:unit
nx run rhino-cli:specs:behavior:coverage
```

**Author a scenario in the phase that creates its behavior, or an earlier one — never a later one.**
TickSpec requires a literal, _passing_ binding for every scenario at all times, so behavior that
does not exist yet cannot be bound truthfully.

## Dependency Status

Core NuGet packages beyond the .NET SDK itself: `Argu` (CLI argument parsing, `RhinoCli.Cli`),
`YamlDotNet` (`RhinoCli.Application`), and `FSharp.Analyzers.Build` +
`G-Research.FSharp.Analyzers` (build-time lint, all five projects). `deps:audit` scans the full
transitive set for known vulnerabilities; see
[Dependency Bump Stability & Safety Policy](../../repo-governance/development/workflow/dependency-bump-policy.md)
for the bump-review process.

## See also

- Rewrite plan (`rewrite-rhino-cli-to-fsharp`, `plans/`): documents the Rust-to-F# port and the
  preceding Rust-to-Go migration plan referenced from its own history (recoverable from git
  history; not linked here — `plans/done/` is repo-specific and this README is byte-identical
  across sibling repos)
- Gherkin specs (shared with the retired Rust and Go binaries):
  [`specs/apps/rhino/cli/behaviors/`](../../specs/apps/rhino/cli/behaviors/)
