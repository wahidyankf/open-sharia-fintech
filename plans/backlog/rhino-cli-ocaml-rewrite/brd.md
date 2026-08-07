# BRD — rhino-cli OCaml Rewrite

## Business goal

Reduce the two costs `rhino-cli` imposes on every day of development in this repository — **dev-loop
latency** and **local disk footprint** — without losing any of the correctness guarantees the tool
exists to enforce.

`rhino-cli` is not an ordinary app. It is the enforcement point for the repository's governance
model: 21 of its subcommands run as gates on every commit-and-push cycle, ~30 Nx targets shell into
it, and six CI workflows depend on it. Every second it adds to a rebuild, and every gigabyte it
parks on disk, is paid on every plan, in every worktree, in four repositories.

## Measured cost baseline

All figures measured on the maintainer's machine (Darwin 24.5.0, aarch64) on **2026-08-07**.
The machine was under concurrent load from other agent sessions during measurement, so wall-clock
figures are upper bounds rather than best-case; `user` time is reported where it materially differs.

### Developer-loop latency (Rust, current)

| Operation                                                        | Wall clock | Notes                                          |
| ---------------------------------------------------------------- | ---------- | ---------------------------------------------- |
| Cold `cargo build --release` (empty target, warm crate registry) | **63.2 s** | 82 rlibs compiled; `user` 104.7 s (parallel)   |
| Cold `cargo check --all-targets` (empty target)                  | **18.5 s** | `user` 56.5 s                                  |
| Warm no-op `cargo build --release`                               | 0.25 s     | nothing to do                                  |
| **Incremental release rebuild after touching `src/lib.rs`**      | **68.4 s** | single-crate recompile; `user` 59.4 s — serial |
| `cargo check --all-targets` (warm)                               | 29.9 s     |                                                |
| `cargo clippy --all-targets -- -D warnings` (warm)               | 12.3 s     |                                                |
| `cargo test --lib` (1,351 unit tests)                            | **93.6 s** | 69.6 s of that is test execution               |
| Binary startup, 10× `--help`                                     | 0.44 s     | **≈ 4.4 ms per invocation**                    |

The 68.4 s figure is the one that hurts. It is a **single-crate** recompile — the 82 dependencies
were already built — and it is nearly all serial (`user` 59.4 s against `real` 68.4 s), because
`[profile.release]` sets `codegen-units = 1` and `lto = "thin"`. Every `specs:*`, `gate`, `naming:*`,
`governance:*`, and `env:validation` Nx target invokes `cargo run --release`, so this is the inner
loop, not a release-only cost.

### Disk footprint (Rust, current)

| Item                                                      | Size       |
| --------------------------------------------------------- | ---------- |
| `~/.rustup` — **six** installed toolchains                | **7.2 GB** |
| ├─ `stable`                                               | 1.8 GB     |
| ├─ `1.96.0`                                               | 952 MB     |
| ├─ `1.95.0` ← the version `rust-toolchain.toml` pins      | 999 MB     |
| ├─ `1.94`                                                 | 1.2 GB     |
| ├─ `1.88`                                                 | 1.2 GB     |
| └─ `1.80`                                                 | 1.1 GB     |
| `~/.cargo` (registry 314 MB, bin 41 MB)                   | 434 MB     |
| `~/.cache/ose-cargo-target` — shared target cache         | **8.2 GB** |
| ├─ `ose-primer/crud-be-rust-axum`                         | 3.8 GB     |
| ├─ `ose-primer/rhino-cli`                                 | 3.6 GB     |
| ├─ `ose-public/rhino-cli`                                 | 300 MB     |
| ├─ `ose-private/rhino-cli`                                | 221 MB     |
| └─ `baseerah/rhino-cli`                                   | 210 MB     |
| **Total attributable to Rust**                            | **~16 GB** |
| Per-build artefacts: `target/release` after a build       | 221 MB     |
| Per-build artefacts: `target` after `check --all-targets` | 414 MB     |
| Release binary                                            | 3.88 MiB   |

### The honest read of this baseline

Two facts change the shape of the problem, and both are observable rather than inferred:

1. **~7 GB of the 16 GB is not the language's fault.** Five of the six rustup toolchains are
   superseded — `rust-toolchain.toml` pins `1.95.0`, and `1.80`, `1.88`, `1.94`, and `1.96.0` are
   leftovers alongside a floating `stable`. That is ~5.2 GB reclaimable with
   `rustup toolchain uninstall`. Separately, 7.5 GB of the 8.2 GB target cache belongs to
   **`ose-primer`**, not this repo — `ose-public/rhino-cli` is 300 MB. The
   [build-artifact sweeper](../../../repo-governance/development/infra/build-artifact-sweeper.md) is
   supposed to reap exactly this; that it has not is an operational gap, not a language defect.
2. **The 68.4 s rebuild is a profile choice, not a compiler limit.** The same crate type-checks in
   18.5 s cold and lints in 12.3 s. Release-profile settings tuned for shipping a fast binary are
   being applied to the edit-compile-run loop because the Nx targets use `cargo run --release`.

_Judgment call:_ Phase 1 of the delivery plan tests both hypotheses before the rewrite is committed
to. If tuning alone lands the incremental loop in single-digit seconds and the footprint near 3 GB,
the rewrite's remaining justification is much narrower — and the maintainer should get to see that
number before spending ~59,000 lines of reimplementation across three repositories.

### Three dead dependencies (verified)

`Cargo.toml` declares `tree-sitter 0.26.9`, `pulldown-cmark 0.13.4`, and `ignore 0.4.25`. A
repository-wide search finds **zero** references to `tree_sitter::`, `pulldown_cmark::`, or
`ignore::` anywhere in `apps/rhino-cli/src/` or `apps/rhino-cli/tests/`. They are unused.

This matters disproportionately, because those three crates are exactly where the OCaml research
found its hardest blockers: OCaml has no runtime tree-sitter binding (only a per-grammar code
generator, not published to opam) and no gitignore-aware directory walker at all. Since `rhino-cli`
uses neither capability, **both blockers evaporate** — the tool actually walks directories with
plain `walkdir` and parses markdown with hand-written code plus `regex`.

Removing the three dead dependencies is worth doing regardless of the rewrite decision, per
[Root Cause Orientation](../../../repo-governance/principles/README.md). Phase 1 does it.

## Business impact

### Pain points addressed

| Pain point                                                                                 | Who feels it                                   |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| A one-line change to `rhino-cli` costs 68 s before it can be run                           | Maintainer and every AI agent executing a plan |
| 16 GB of disk on a laptop shared with four repos, N worktrees, and a .NET + Node toolchain | Maintainer                                     |
| A cold CI build spends ~63 s compiling before the first gate executes                      | Every PR in three repositories                 |
| `cargo test --lib` at 93.6 s discourages running tests before pushing                      | Maintainer and agents; drives reliance on CI   |

### Expected benefits

Stated as structural claims, not as fabricated numbers — the numeric targets are set in Phase 2 from
the spike's measurements, not asserted here.

- A faster edit-compile-check cycle for the one binary every gate runs through.
- A smaller resident toolchain, **conditional on using a single shared opam switch**. This is not
  automatic: opam's modern idiom is a per-project local `_opam/` switch that duplicates the whole
  compiler and every dependency per project. Across four repos plus live worktrees, local switches
  would plausibly be **worse** than the current shared cargo target cache. Phase 2 measures this and
  the plan mandates a shared switch if it does not.
- Fewer moving parts in the dependency graph — 183 Cargo packages today; the OCaml equivalent set is
  estimated at 60-90 opam packages (basis and caveats in [`tech-docs.md`](./tech-docs.md)).

### Benefits explicitly NOT claimed

- **Not** faster runtime. `rhino-cli` startup is already 4.4 ms and its workloads are I/O-bound file
  walks. OCaml native code is in the same performance class; there is nothing to win here.
- **Not** better type safety. Rust and OCaml are peers on algebraic data types and exhaustiveness.
  OCaml is _weaker_ in one respect that matters for a tool with 90% coverage gates: exceptions are
  not tracked in the type system, and the OCaml standard library raises them from routine functions
  (`List.find`, `String.sub`), so `result`-everywhere discipline is a convention the compiler will
  not enforce. Rust's `Result` + `#[must_use]` does enforce it.
- **Not** improved ecosystem access. opam indexes ~4,500 packages against crates.io's ~303,000.

## Affected roles

The maintainer wears three hats here, and several agents consume the output:

| Role / agent                         | Interest                                                                      |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| Maintainer (as tool author)          | Bears the rewrite cost and the dev-loop cost                                  |
| Maintainer (as governance owner)     | Must not lose a single enforced gate in the swap                              |
| Maintainer (as machine owner)        | Owns the disk                                                                 |
| `repo-setup-manager`                 | Executes Phase 0; must provision an opam toolchain via `npm run doctor`       |
| `ci-checker` / `ci-fixer`            | Validate the retargeted Nx target set                                         |
| `swe-code-checker`                   | Has no OCaml ruleset today — Phase 2 must produce one or the gate goes silent |
| `pr-review-types-maker`              | Covers TypeScript, Rust, F#, C# — gains no OCaml lens without new work        |
| `repo-harness-compatibility-checker` | Owns the three-repo parity manifest that the cutover must re-generate         |

## Business-level success metrics

Each metric is labelled with how it is established. Per the
[plans convention](../../../repo-governance/conventions/structure/plans.md), no numeric target below
is presented as an already-measured fact unless it is one.

| #   | Metric                                                                                                                                                         | Kind                               |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| M1  | Every one of the 441 Gherkin scenarios under `specs/apps/rhino/behavior/rhino-cli/gherkin/` executes green against the OCaml binary                            | **Observable fact** — test run     |
| M2  | `apps/rhino-cli/scripts/shadow-diff.sh` reports zero byte differences between the frozen Rust binary and the OCaml binary across the full golden-master corpus | **Observable fact** — script exit  |
| M3  | Every gate listed by `rhino-cli gate list` for all three surfaces still runs and still fails on the same inputs                                                | **Observable fact** — gate run     |
| M4  | Incremental rebuild after a one-line source change, measured the same way as the 68.4 s baseline                                                               | Target set at the Phase 2 gate     |
| M5  | Total resident toolchain + build-cache footprint, measured the same way as the 16 GB baseline                                                                  | Target set at the Phase 2 gate     |
| M6  | The five OCaml tooling gaps (Gherkin, lint, dependency audit, coverage threshold, lockfile) each have a named, working replacement — not a waiver              | **Observable fact** — Phase 2 gate |
| M7  | `rhino-cli` remains byte-identical across `ose-public`, `ose-primer`, `ose-private` under a regenerated parity manifest                                        | **Observable fact** — parity gate  |

M4 and M5 are deliberately left unnumbered here. Setting a target before the Phase 1 control
experiment and the Phase 2 spike have run would be exactly the fabricated-baseline failure the
convention forbids.

## Business-scope non-goals

- Changing what `rhino-cli` does. Behaviour parity is absolute; feature work is a different plan.
- Migrating any other Rust code. `libs/rust-commons`, `apps/ayokoding-cli`, `apps/ose-cli`, and the
  `ose-primer` Rust demo apps all stay Rust, so the Rust toolchain does not leave the machine — a
  point that materially weakens the disk-savings case and is stated plainly in
  [`tech-docs.md`](./tech-docs.md).
- Adopting OCaml anywhere else in the platform.
- Rewriting the Gherkin corpus. The 67 feature files are re-bound, never re-authored.

## Business risks and mitigations

| #   | Risk                                                                                                                                                                                  | Severity | Mitigation                                                                                                                                                          |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | The rewrite delivers little relief because the real costs were reclaimable toolchains and a mis-tuned build profile                                                                   | HIGH     | Phase 1 runs the control experiment and re-baselines **before** the go/no-go gate                                                                                   |
| R2  | Governance coverage silently degrades — OCaml has no clippy-class linter, no `cargo-deny` equivalent, and `bisect_ppx` (last release 2023-07) emits no lcov and has no threshold flag | HIGH     | Phase 2 must produce a working replacement for each; the gate fails on a waiver. A silently-weakened gate is worse than a slow one                                  |
| R3  | A single maintainer takes on a second niche language; OCaml's opam index is ~4,500 packages vs ~303,000 crates                                                                        | HIGH     | Counter-signal: Jane Street completed its OCaml 5 production migration and open-sourced OxCaml; Docker is migrating parts of Docker Desktop. Small but not stagnant |
| R4  | Three-repo byte-identity breaks mid-migration, blocking unrelated work in `ose-primer` and `ose-private`                                                                              | HIGH     | Cutover is a single atomic delivery unit across all three repos; the parity manifest regenerates in the same commit                                                 |
| R5  | Rust does not actually leave the machine, so the ~7 GB rustup footprint persists and OCaml's switch is **added** to it                                                                | MEDIUM   | Phase 2 measures the opam switch; the plan mandates one shared switch, not per-project `_opam/`                                                                     |
| R6  | The home-grown Gherkin harness becomes an unmaintained dependency of every gate in four repos                                                                                         | MEDIUM   | Scope it to the corpus's actual grammar subset (measured — see [`tech-docs.md`](./tech-docs.md)) and gate it with its own spec suite                                |
| R7  | Mid-flight plans touching `rhino-cli` — notably `sdlc-gate-registry-enforcement` — collide with the rewrite                                                                           | MEDIUM   | The rewrite is `blockedBy` completion of every in-flight plan that edits `apps/rhino-cli/`; Phase 0 enumerates them                                                 |
| R8  | Reimplementing 58,617 lines reintroduces bugs the Rust port already fixed                                                                                                             | MEDIUM   | Shadow-diff against the frozen Rust binary is a merge precondition for every command-group PR, not a final check                                                    |

## Precedent worth weighing

`rhino-cli` has been rewritten once already — Go to Rust, completed 2026-05-23, delivered
byte-identical across shadow-diff corpora. That migration is the best available evidence that a
rewrite of this tool is _achievable_. It is also evidence about cost: it took a full plan, a shadow-
diff harness, and a golden-master corpus that this plan inherits and reuses.

The Go-to-Rust direction was toward stronger static guarantees. An OCaml rewrite is roughly lateral
on that axis; a Go rewrite would be a regression (no sum types, no exhaustiveness checking, nullable
interfaces, silently ignorable errors) and would undo work completed three months ago. The four-way
comparison is in [`tech-docs.md`](./tech-docs.md).
