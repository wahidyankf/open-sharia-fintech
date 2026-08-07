# Learnings — rhino-cli Optimization

Running log of generalizable learnings accrued while executing `delivery.md`. Append in the moment
something is noticed; do not reconstruct afterwards. Drained by the Phase 15 Knowledge Capture phase
before archival — this file is never the system of record.

Format per entry: what happened, why it generalizes, and a candidate durable home.

Entries L1-L7 were accrued during plan **authoring**, before execution began. They are the reason
the plan has the shape it has, and they are already triaged to candidate homes.

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
`\b<crate>::`. Both greps were needed; either alone would have been unsound in a different
direction.

**Why it generalizes**: same family as the already-recorded "acceptance clauses must be falsifiable
both ways" learning. A negative finding about code usage needs at least two independent detection
paths before it is load-bearing.

**Candidate home**: the acceptance-criteria or plan-anti-hallucination convention. Possibly a
`swe-code-checker` rule: detect declared-but-unreferenced manifest dependencies across languages.

### L3 — Release-profile settings applied to the inner dev loop

**Accrued**: 2026-08-07, during plan authoring.

`rhino-cli`'s incremental rebuild is 68.4 s while the same crate under `dev` with `debug = 0`
rebuilds in **1.83 s** — a 37× spread with no change to the compiler, the machine, or the code. The
gap is `[profile.release]` carrying `lto = "thin"`, `codegen-units = 1`, and `opt-level = 3` —
correct for a shipped binary, wrong for an edit-compile-run loop. It lands in the dev loop because
**53 invocation sites across 27 `project.json` files** invoke `cargo run --release`.

**Why it generalizes**: an Nx target that shells into a compiler with a release profile turns every
gate invocation into a release build. This is a repo-wide pattern check, not a rhino-cli fact — and
it produced a "the language is slow" conclusion that the language did not earn, nearly costing a
59,000-line rewrite.

**Candidate home**: `repo-governance/development/infra/nx-targets.md` or `anti-patterns.md` — a rule
that validator and gate targets use a fast profile, with release builds reserved for `build`.

### L4 — 5 of 6 rustup toolchains were superseded, and nothing owned them

**Accrued**: 2026-08-07, during plan authoring.

`~/.rustup` held 7.2 GB across six toolchains while `rust-toolchain.toml` pins exactly one.
Separately, 7.5 GB of the 8.2 GB shared cargo target cache belonged to `ose-primer`, not this repo —
whose own share is ~300 MB. The build-artifact sweeper is documented as reaping gitignored build
output but had reclaimed neither. Research confirmed why: **rustup has no built-in GC**, and the
upstream feature request for one is still open.

**Why it generalizes**: a "the toolchain is too big" complaint deserves a per-component breakdown
before it becomes a rewrite rationale. Roughly 7 of the 16 GB was reclaimable with two commands, and
the dominant term was the one no tool and no convention owned.

**Candidate home**: `repo-governance/development/infra/build-artifact-sweeper.md` — whether rustup
toolchain pruning belongs in the sweeper's remit, and whether `npm run doctor` should warn on
toolchains that no `rust-toolchain.toml` in any sibling repo pins. Phase 6 implements both.

### L5 — Well-cited build advice failed locally four times out of four

**Accrued**: 2026-08-07, during plan authoring.

Three independent research passes produced a ranked list of build, disk, and type-safety
interventions. Four of the top-ranked ones do nothing, or actively harm, on this workload:

- **Linker replacement** — `mold` has no open-source macOS support, `wild`'s Mach-O backend is
  pre-production, `zld` is dead, and Apple's own linker has been the default since Xcode 15 and is
  now competitive with or faster than `lld`. The widely-repeated "switch to lld/mold" advice is
  2022-era and stale for macOS in 2026.
- **`sccache`** — cannot cache incrementally-compiled crates at all; adopting it requires
  `CARGO_INCREMENTAL=0`, which removes Rust's own incremental caching. It is a cold-build/CI tool,
  and using it for a local dev loop is strictly worse.
- **`cargo-sweep`** — the most-recommended target-dir pruner declares itself unmaintained in its own
  README and points to `cargo-clean-all`.
- **Workspace splitting** — cited as the highest-leverage fix (a real case going 30-45 min → under
  3 min), but the measured pain point here _is_ `src/lib.rs`, the crate root. Splitting a
  foundational crate adds per-boundary overhead without buying isolation for that exact edit.

**Why it generalizes**: general Rust build advice is overwhelmingly written for multi-crate
workspaces on Linux. A single-crate CLI on aarch64-apple-darwin inverts several of its conclusions.
Ranked-by-effect lists are hypotheses about a workload, not facts about it.

**Candidate home**: the plan-planning workflow — this is the direct rationale for the POC-first
rule that every substantive phase in this plan opens with. A plan that acted on the published
ranking without a local POC would have shipped four changes that do nothing here.

### L6 — Strict lints already worked; the audit found the gap somewhere else

**Accrued**: 2026-08-07, during plan authoring.

The type-safety audit expected to find `unwrap()` sprayed through production code. It found
**zero** — all 1,958 occurrences are inside `#[cfg(test)]` modules, exactly as
`unwrap_used = "deny"` intends. The real open surface was elsewhere: 1,983 unchecked index sites
behind a deliberately-deferred lint, and 189 of 190 `#[allow(...)]` attributes carrying no `reason`,
so a considered exception is textually indistinguishable from a silenced warning.

**Why it generalizes**: auditing a codebase for the failure mode you expect confirms the gate that
already exists. The finding worth having was the one nobody was looking for — and it was cheapest
to detect by counting suppressions, not by counting violations.

**Candidate home**: a checker heuristic — reasonless `#[allow(...)]` density as a first-class code
smell, since it measures _undocumented_ exceptions rather than exceptions as such.

### L7 — A concurrent agent in the primary checkout destroyed this plan mid-authoring

**Accrued**: 2026-08-07, during plan authoring.

While these documents were being written on `main` under the plan-docs-only carve-out, a concurrent
agent working a different plan in the **same primary checkout** ran `git reset`
(`reflog HEAD@{2}: reset: moving to HEAD~1`). That restored the tracked tree to `HEAD`, which
reverted this plan's `git mv` and deleted all six rewritten documents at the new path. Nothing
warned; the loss surfaced only when a subsequent `Edit` reported the file missing.

Two things limited the damage, and one thing did not:

- The index edits and file deletions had already been staged, so they survived.
- The documents themselves were unstaged and unrecoverable from git. They were rewritten from
  conversation context, then staged in the scratchpad first so a second reset could not repeat it.
- An earlier `git rm` in the same window failed with `index.lock: File exists` — the correct
  response was to retry, not to remove the lock, and the retry succeeded.

**Why it generalizes**: this is the second recorded instance of the same failure mode in this repo.
The existing guidance says not to run git-capable agents in the main checkout; what this adds is
that the _victim_ can also defend itself — stage early, or stage outside the repo entirely. An
index-lock collision is the visible warning that another actor holds the tree, and it should be
read as a signal to protect uncommitted work, not merely as a transient error to retry through.

**Candidate home**: the existing no-git-agents-in-the-main-tree guidance, extended with the
defensive half: when a plan authors documents in the primary checkout, commit or stage each file as
it is finished rather than at the end of the batch.
