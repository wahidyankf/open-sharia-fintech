# rhino-cli Optimization

Make [`apps/rhino-cli`](../../../apps/rhino-cli/README.md) — the repository's governance and
quality-gate CLI — **fast to build**, **cheap on disk**, and **more provably type-safe**, by
attacking each cost at its root rather than by changing language.

## Context

`rhino-cli` (RHINO — Repository Hygiene & INtegration Orchestrator) is the single binary every
quality gate in this repository runs through: three Husky hooks, **53 invocation sites across 27
`project.json` files**, and the `pr-quality-gate` GitHub Actions workflow. It is ~59,000 lines of
Rust across 195 source files with 183 transitive dependencies, and it is byte-identical with
`ose-private` under the
[parity manifest](../../../apps/rhino-cli/parity-manifest.sha256).

Three complaints motivate this plan, and all three were **measured** on the maintainer's machine on
2026-08-07 rather than accepted as premises:

| Complaint            | Measured                                                                            |
| -------------------- | ----------------------------------------------------------------------------------- |
| The build is slow    | Touch one line of `src/lib.rs`, rebuild: **68.4 s**. `cargo test --lib`: **93.6 s** |
| It eats disk         | `~/.rustup` + `~/.cargo` + the shared cargo target cache: **~16 GB**                |
| Type safety has gaps | 1,983 unchecked index/slice sites; 241 `.expect(`; 189 reasonless `#[allow(...)]`   |

Measuring first changed the plan's shape completely. **None of the three is primarily a property of
Rust**, and two of them were already answered by measurements taken during authoring:

- A dev-profile build with `debug = 0` rebuilds after a one-line edit in **1.83 s** — 37× faster
  than the 68.4 s figure, on the same crate, same machine, same compiler. The 68.4 s is a _profile
  choice_: every one of the 53 gate invocation sites shells out to `cargo run --release`, so
  `lto = "thin"` + `codegen-units = 1` + `opt-level = 3` — correct for a shipped artefact — is
  being applied to the inner edit-compile-run loop.
- Of the ~16 GB, **~7.2 GB is five superseded rustup toolchains** that no `rust-toolchain.toml` in
  any sibling repo pins, and **7.5 GB of the 8.2 GB shared target cache belongs to `ose-primer`**,
  not to this repo. `ose-public`'s own `rhino-cli` cache is ~300 MB.

So this is an optimization plan, not a rewrite plan. The full measurement set, the first-principles
cost model, and the ranked lever table — including the levers that research **disqualified** — are
in [`tech-docs.md`](./tech-docs.md).

## First principles

Each complaint is decomposed to the irreducible quantities that produce it. Every phase in
[`delivery.md`](./delivery.md) targets one term, and no phase is justified by folklore.

| Axis                | Cost identity                                                                                    |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| **A — build time**  | `(code recompiled per edit) × (optimization work per unit) + (link work) × (number of binaries)` |
| **B — disk**        | `(toolchains × size) + (target dirs × size) + (debug-info share) + (registry) + (incr. caches)`  |
| **C — type safety** | `(runtime failure modes the compiler is not currently asked to rule out)`                        |

Axis D — re-evaluating the language — exists, but only as a **gated last resort** reached if and
only if A, B, and C are exhausted and the measured targets still stand unmet.

## Position in the plan sequence

This plan is the **middle** of three, in this order:

```text
sdlc-gate-registry-enforcement  →  rhino-cli-optimization  →  beaver-nest-repo-consolidation
```

Both neighbours touch `apps/rhino-cli`, and the ordering is load-bearing in both directions:

- **Upstream**, `sdlc-gate-registry-enforcement` makes `repo-config.yml` the authoritative gate
  registry and `rhino-cli gate run` the dispatch behind the three generated Husky shims. That
  registry _is_ the single indirection for hook-invoked gates, so Axis A builds on it instead of
  inventing a competing wrapper — and Axis A's own indirection work narrows to the 53 `project.json`
  sites the registry does not cover.
- **Downstream**, `beaver-nest-repo-consolidation` edits `apps/rhino-cli` directly and cites
  artefacts this plan changes. Those citations go stale when this plan lands, so
  [`delivery.md`](./delivery.md) carries an explicit hand-off obligation naming each one.

See [`delivery.md` §Sequencing](./delivery.md#sequencing-position) for the full contract in both
directions.

## Scope

### In scope

| Area                        | What changes                                                                                              |
| --------------------------- | --------------------------------------------------------------------------------------------------------- |
| `apps/rhino-cli/Cargo.toml` | A dedicated fast profile; three dead dependencies removed; the lint block tightened (Axis C)              |
| Gate invocation sites       | The 53 `cargo run --release` sites collapse behind **one** indirection that resolves the binary once      |
| `apps/rhino-cli/tests/`     | 28 test files / 22 `harness = false` binaries consolidated so the library is linked once, not 22 times    |
| Toolchain hygiene           | Superseded rustup toolchains pruned; the build-artifact sweeper and `npm run doctor` learn to keep it so  |
| `apps/rhino-cli/src/`       | `indexing_slicing` and `arithmetic_side_effects` enabled crate-wide, applied module by module             |
| `nx affected` detection     | The `ose-public`-only gap that makes `nx affected` skip `apps/rhino-cli/src/**/*.rs` changes, root-caused |
| Cross-repo parity           | `ose-private` receives the identical change set under the byte-identity gate                              |

### Out of scope

- Any change to `rhino-cli`'s **observable contract** — commands, flags, exit codes, stdout/stderr
  bytes. Every phase is behaviour-preserving and is shadow-diffed to prove it.
- New `rhino-cli` features, validators, or subcommands.
- The other Rust crates in the monorepo (`libs/rust-commons`, `apps/ayokoding-cli`, `apps/ose-cli`)
  except where machine-wide toolchain hygiene necessarily touches their shared caches.
- Splitting the crate into a Cargo workspace. Research indicates this would likely make the measured
  pain point **worse**, not better — see [`tech-docs.md`](./tech-docs.md) §Disqualified levers.
- `beaver-nest`'s fork of `rhino-cli`. That fork is discarded, not reconciled, by the downstream
  consolidation plan — so propagating optimization work into it would be wasted effort.

### Affected subrepos and apps

**Exactly two: `ose-public` (this repo) and `ose-private`.** Both other family members are excluded
by design, for different reasons:

- **`beaver-nest`** is folded into `ose-public` and archived by the downstream plan, and its
  `rhino-cli` fork is discarded rather than reconciled. Anything propagated into it would be thrown
  away days later.
- **`ose-primer`** left continuous byte-identity enforcement at commit `a0383faed` and now syncs
  **manually, on a delay**. A delayed-sync repo must not block a delivery unit — that is precisely
  why it left enforcement. It picks these changes up on its own schedule.

One stated exception that is not scope creep: Axis B reclaims `ose-primer`'s stale **gitignored
build cache** on this machine, which is 7.5 GB of the 8.2 GB shared target directory. That touches
no file in that repository. See
[Related Repositories](../../../docs/reference/related-repositories.md).

## Approach summary

**Every substantive phase opens with a small, bounded, throwaway POC.** The POC measures the lever
on the narrowest slice that can produce a real number, in a scratch directory, before any tracked
file changes — and it carries an explicit **abandon-if** criterion. This exists because the
measurements taken during authoring repeatedly contradicted well-cited general advice: linker swaps
are dead on macOS in 2026, `sccache` actively conflicts with incremental compilation, and the
single most-recommended target-dir pruner is unmaintained. A plan that acted on published rankings
without a local POC would have shipped four changes that do nothing here.

1. **Phase 0** re-establishes the baseline in a clean checkout and verifies the sequencing
   assumption. It opens no PR.
2. **Axis A** collapses the 53 release-profile gate invocations onto a fast profile, consolidates
   the 22 test binaries, and root-causes the `nx affected` detection gap — because a gate that is
   silently skipped is not made better by making it faster.
3. **Axis B** reclaims the toolchain and cache gigabytes, then encodes the hygiene so the footprint
   does not regrow: the ambient build-artifact sweeper and `npm run doctor` both learn about
   unpinned toolchains.
4. **Axis C** enables `indexing_slicing` and `arithmetic_side_effects` crate-wide — a large,
   genuinely risky mechanical refactor, which is why it is staged module by module behind a POC
   that measures the real diagnostic count on one module before the sweep is committed to.
5. **Axis D** is entered only if A, B, and C land and the targets are still unmet. It carries the
   four-way Rust/Go/OCaml/F# comparison forward as an appendix decision record, and closes on a
   `[HUMAN]` go/no-go.
6. **A documentation-propagation phase closes the plan**, in two passes. Governance rules go
   through `repo-rules-maker`, because a rule change has to sweep its register, its checker, and
   every index that names it — fixing only the obvious file is a recorded failure mode here.
   Everything outside `repo-governance/` is then swept by hand, grep by grep: `AGENTS.md`,
   `CLAUDE.md`, the `docs/reference/` set, every affected app README, and the agent and skill files
   that name the old invocation form.

### A note on honesty of framing

This plan replaces an earlier one that proposed rewriting `rhino-cli` in OCaml. That plan is not
being abandoned because the rewrite was unattractive — it is being abandoned because the
measurements it collected during its own authoring showed the rewrite was aimed at costs the
language did not cause. The comparison work survives in [`tech-docs.md`](./tech-docs.md) rather
than being discarded, so the question does not need re-researching if Axis D is ever reached.

## Documents

| File                             | Contents                                                                                      |
| -------------------------------- | --------------------------------------------------------------------------------------------- |
| [`brd.md`](./brd.md)             | First-principles cost decomposition, full measurement tables, success metrics, business risks |
| [`prd.md`](./prd.md)             | Personas, user stories, Gherkin acceptance criteria, product scope                            |
| [`tech-docs.md`](./tech-docs.md) | Cost model per axis, ranked and disqualified levers, language-comparison appendix, rollback   |
| [`delivery.md`](./delivery.md)   | Phased, DAG-ordered delivery checklist with POC-first phases and per-phase gates              |
| [`learnings.md`](./learnings.md) | Running log of generalizable learnings, drained by the Knowledge Capture phase                |

## Absorbed ideas

Promoting this plan consumed two `plans/ideas/` two-pagers, deleted and de-indexed on promotion:

- `rhino-cli-language-rewrite-tradeoffs` — its stated promotion signal was _"the non-rewrite Rust
  fixes pursued as their own scoped plan"_ plus _"the `cargo build --timings` baseline run for
  real"_. Both are exactly this plan. Its research is preserved in
  [`tech-docs.md`](./tech-docs.md) §Appendix.
- `ose-public-nx-affected-rhino-cli-gap` — root-causing why `nx affected` misses rhino-cli Rust
  changes in `ose-public` only. Folded into Axis A, because this plan edits the same `project.json`
  surface where the divergence must live.

## Delivery Mode

`worktree-to-pr` (repo default). See [`delivery.md`](./delivery.md) for the worktree declaration,
the parallelization model, and the delivery-boundary table.
