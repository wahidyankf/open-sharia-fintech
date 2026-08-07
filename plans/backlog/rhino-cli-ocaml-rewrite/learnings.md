# Learnings — rhino-cli OCaml Rewrite

Running log of generalizable learnings accrued while executing `delivery.md`. Append in the moment
something is noticed; do not reconstruct afterwards. Drained by the Phase 14 Knowledge Capture phase
before archival — this file is never the system of record.

Format per entry: what happened, why it generalizes, and a candidate durable home.

## Entries

### L1 — `apps/rhino-cli/target` is a symlink; `du -sh` on it reports 0B

**Accrued**: 2026-08-07, during plan authoring.

`apps/rhino-cli/target` is a symlink to `~/.cache/ose-cargo-target/<repo>/rhino-cli`. Running
`du -sh apps/rhino-cli/target` reports **0B** because `du` does not follow symlinks by default,
which reads as "the build cache is empty" — and a subsequent "cold build" measurement then returns
0.5 s against a fully warm cache, silently invalidating the whole measurement.

**Why it generalizes**: the same class as the `ls`-is-eza and RTK-trailer traps already recorded —
a tool's default behaviour silently transforms output that a measurement depends on. Any acceptance
clause of the form "directory is empty ⇒ build is cold" is unsound where the path may be a symlink.

**Candidate home**: a measurement-hygiene note in
`repo-governance/development/quality/plan-anti-hallucination.md`, or the cargo-target-share
convention. Genuinely cold Rust builds must use an explicit empty `CARGO_TARGET_DIR`, not a
`du`-based emptiness check.

### L2 — Dead dependencies hide from `use`-line greps

**Accrued**: 2026-08-07, during plan authoring.

`tree-sitter`, `pulldown-cmark`, and `ignore` are declared in `Cargo.toml` with zero references
anywhere. A grep for `^use <crate>` found them absent, but that alone is not proof — Rust allows
fully-qualified `crate::path` use with no `use` line. Confirming required a second grep for
`\b<crate>::`. Both greps were needed; either alone would have been unsound in a different direction.

**Why it generalizes**: same family as the already-recorded
"acceptance clauses must be falsifiable both ways" learning. A negative finding about code usage
needs at least two independent detection paths before it is load-bearing.

**Candidate home**: the acceptance-criteria or plan-anti-hallucination convention. Possibly a
`swe-code-checker` rule: detect declared-but-unreferenced manifest dependencies across languages.

### L3 — Release-profile settings applied to the inner dev loop

**Accrued**: 2026-08-07, during plan authoring.

`rhino-cli`'s incremental rebuild is 68.4 s while `cargo check` is 18.5 s cold. The gap is
`[profile.release]` carrying `lto = "thin"`, `codegen-units = 1`, and `opt-level = 3` — correct for
a shipped binary, wrong for an edit-compile-run loop. It lands in the dev loop because every
validator Nx target invokes `cargo run --release`.

**Why it generalizes**: an Nx target that shells into a compiler with a release profile turns every
gate invocation into a release build. This is a repo-wide pattern check, not a rhino-cli fact — and
it produced a "the language is slow" conclusion that the language did not earn.

**Candidate home**: `repo-governance/development/infra/nx-targets.md` or `anti-patterns.md` — a rule
that validator targets use a fast profile, with release builds reserved for `build`.

### L4 — 5 of 6 rustup toolchains were superseded

**Accrued**: 2026-08-07, during plan authoring.

`~/.rustup` held 7.2 GB across six toolchains while `rust-toolchain.toml` pins exactly one.
Separately, 7.5 GB of the 8.2 GB shared cargo target cache belonged to `ose-primer`, not this repo.
The build-artifact sweeper is documented as reaping gitignored build output but had not reclaimed
either.

**Why it generalizes**: a "the toolchain is too big" complaint deserves a per-component breakdown
before it becomes a rewrite rationale. Roughly 7 of the 16 GB was reclaimable with two commands.

**Candidate home**: `repo-governance/development/infra/build-artifact-sweeper.md` — whether rustup
toolchain pruning belongs in the sweeper's remit, and whether `npm run doctor` should warn on
toolchains that no `rust-toolchain.toml` in any sibling repo pins.

### L5 — Research gaps that must be resolved by measurement, not more research

**Accrued**: 2026-08-07, during plan authoring.

Four decision-relevant figures have **no** authoritative public source: OCaml cold-build time at
~40k LOC, a typical opam switch's disk size in 2026, a stripped OCaml CLI binary size for a real
tool, and F# compile time at 59k LOC (the in-repo measurement is 3,730 LOC — 15.7× smaller and not
linearly extrapolable). Three independent research passes each flagged these as unverified.

**Why it generalizes**: when three research passes converge on "no benchmark exists", further
research is not the answer — a bounded spike is. This is why Phase 2 exists in the shape it does.

**Candidate home**: the plan-planning workflow — a note that a language or framework decision whose
key numbers are unciteable needs a measurement phase, not a longer research phase.
