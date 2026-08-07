# rhino-cli OCaml Rewrite

Rewrite [`apps/rhino-cli`](../../../apps/rhino-cli/README.md) — the repository's governance and
quality-gate CLI — from Rust to OCaml, behind an evidence gate that first measures whether the
rewrite actually buys the developer-loop and disk-footprint relief it is meant to buy.

## Context

`rhino-cli` (RHINO — Repository Hygiene & INtegration Orchestrator) is the single binary every
quality gate in this repository runs through. It is invoked by the three Husky hooks, by roughly
thirty Nx project targets, and by six GitHub Actions workflows. It was Go, was ported to Rust on
2026-05-23, and is byte-identical across `ose-public`, `ose-primer`, and `ose-private` under the
[parity manifest](../../../apps/rhino-cli/parity-manifest.sha256); `beaver-nest` carries a fork.

The motivating complaints are concrete and were measured on the maintainer's machine on 2026-08-07:

- **The Rust dev loop is slow.** Touching one line of `src/lib.rs` and rebuilding the release binary
  takes **68.4 s**. `cargo test --lib` takes **93.6 s**.
- **The Rust toolchain eats disk.** `~/.rustup` + `~/.cargo` + the shared cargo target cache total
  **~16 GB** on this machine.

Full measurements, and the four-way language comparison (Rust / Go / OCaml / F#) the maintainer
asked for, are in [`tech-docs.md`](./tech-docs.md).

## Scope

### In scope

| Area                        | What changes                                                                                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `apps/rhino-cli/`           | Rust crate replaced by an OCaml/dune project delivering the identical observable CLI contract                                                    |
| `libs/ocaml-rhino-gherkin/` | **New** — a home-grown Gherkin parser + test harness, since no maintained OCaml Cucumber implementation exists (see [tech-docs](./tech-docs.md)) |
| Nx targets                  | `apps/rhino-cli/project.json` retargeted from `cargo` to `dune`; the ~30 consuming `project.json` files re-pointed at the new binary path        |
| Git hooks + CI              | `.husky/{pre-commit,pre-push,commit-msg}`, `repo-config.yml` gate registry, `.github/workflows/*`, `.github/actions/setup-rust` → `setup-ocaml`  |
| Toolchain provisioning      | `npm run doctor`, `Brewfile`, worktree setup docs gain opam/dune; drop the Rust requirement for this app                                         |
| Specs                       | `specs/apps/rhino/behavior/rhino-cli/gherkin/**` — 67 feature files, 441 scenarios — re-bound to the new harness, **not rewritten**              |
| Cross-repo parity           | `ose-primer` and `ose-private` receive the identical replacement; `beaver-nest`'s fork is re-based                                               |

### Out of scope

- Any change to `rhino-cli`'s **observable contract** — commands, flags, exit codes, stdout/stderr
  bytes. This is a reimplementation, not a redesign. Behaviour changes are a separate plan.
- `libs/rust-commons`, `apps/ayokoding-cli`, `apps/ose-cli` and the `ose-primer` Rust demo apps.
  Rust does not leave the monorepo; only this one app changes language.
- The other three OSE repos' own Rust usage beyond `rhino-cli`.

### Affected subrepos and apps

`ose-public` (this repo), `ose-primer`, `ose-private` — the three repos bound by the `rhino-cli`
byte-identity gate — plus `beaver-nest`, which carries a fork and is re-based rather than
byte-matched. See [Related Repositories](../../../docs/reference/related-repositories.md).

## Approach summary

The plan is deliberately **gated on evidence rather than committed up front**, because the
measurements already collected show the two stated problems are only partly attributable to the
language:

1. **Phase 1 runs the control experiment first.** Roughly 7 GB of the 16 GB Rust footprint is five
   superseded rustup toolchains and a stale sibling-repo target cache — reclaimable today with no
   rewrite. The 68.4 s incremental rebuild is dominated by `lto = "thin"` + `codegen-units = 1` +
   `opt-level = 3` being applied to the **inner dev loop**, because every validator Nx target
   invokes `cargo run --release`. Phase 1 fixes both and re-measures. Whatever relief survives
   Phase 1 is the real size of the problem the rewrite has to solve.
2. **Phase 2 is a bounded OCaml spike** that resolves the five tooling gaps research identified as
   genuinely missing in OCaml (Gherkin harness, clippy-class linter, `cargo-deny` equivalent,
   lcov-emitting coverage with a threshold, a production lockfile) and produces measured — not
   estimated — OCaml build-time, binary-size, and disk numbers for three representative vertical
   slices.
3. **A `[HUMAN]` go/no-go gate closes Phase 2.** The rewrite proceeds only if the spike's measured
   numbers beat the Phase 1 post-tuning baseline by a margin the maintainer judges worth ~59,000
   lines of reimplementation across three repos.
4. **Phases 3-11 are the rewrite itself**, ported command group by command group, each group
   shadow-diffed byte-for-byte against the frozen Rust binary before its PR merges.
5. **Phases 12-14** cut over the hooks, CI, and sibling repos, then decommission the Rust crate.

### A stated concern

The research is not neutral, and the plan says so rather than burying it. Of the four candidate
languages, OCaml is the one whose **tooling** is furthest from what this repository's own governance
conventions already require — it has no clippy-class linter, no `cargo-deny` equivalent, an
unmaintained coverage tool that cannot emit lcov or enforce a threshold, and no production lockfile.
Those are not preferences; they are gates this repo enforces on every other language it ships.
Meanwhile the two problems motivating the rewrite are, on the measured evidence, substantially
addressable without changing language at all. The plan is written in full and is executable as
written — but Phase 1 and the Phase 2 gate exist so the decision is made against measured numbers
instead of expectations. See [`brd.md`](./brd.md) for the full argument and
[`tech-docs.md`](./tech-docs.md) for the four-way comparison.

## Documents

| File                             | Contents                                                                                             |
| -------------------------------- | ---------------------------------------------------------------------------------------------------- |
| [`brd.md`](./brd.md)             | Business rationale, measured cost baseline, success metrics, business risks                          |
| [`prd.md`](./prd.md)             | Personas, user stories, Gherkin acceptance criteria, product scope                                   |
| [`tech-docs.md`](./tech-docs.md) | Four-way language comparison, cost tables, OCaml library/tooling map, file-impact analysis, rollback |
| [`delivery.md`](./delivery.md)   | Phased, DAG-ordered delivery checklist with per-phase gates                                          |
| [`learnings.md`](./learnings.md) | Running log of generalizable learnings, drained by the Knowledge Capture phase                       |

## Delivery Mode

`worktree-to-pr` (repo default). See [`delivery.md`](./delivery.md) for the worktree declaration,
the parallelization model, and the delivery-boundary table.
