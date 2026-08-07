# Business Requirements — rhino-cli Optimization

## Why this plan exists

`apps/rhino-cli` sits on the critical path of every commit, every push, and every CI run in this
repository. Three costs it imposes were raised as problems: build slowness, disk consumption, and
type-safety gaps. This document decomposes each to its irreducible drivers, records what was
actually measured, and states what "solved" means in numbers a phase gate can fail on.

The controlling decision recorded here: **the plan does not accept any of the three complaints as a
property of the Rust language until the measurement says so.** In two of the three cases, it does
not.

## Measured baseline

All figures collected 2026-08-07 on the maintainer's machine (aarch64-apple-darwin, Rust 1.95.0
pinned by `apps/rhino-cli/rust-toolchain.toml` with `profile = "minimal"`). Every build below ran
against an explicitly empty `CARGO_TARGET_DIR` in a scratch directory — not against
`apps/rhino-cli/target`, which is a **symlink** to `~/.cache/ose-cargo-target/<repo>/rhino-cli` and
therefore reports `0B` under `du -sh`, an artefact that silently invalidated the first measurement
attempt (see [`learnings.md`](./learnings.md) L1).

### Build time

| Configuration                                        | Cold build | One-line-edit rebuild |
| ---------------------------------------------------- | ---------- | --------------------- |
| `release` as shipped: `lto="thin"`, `cgu=1`, `opt=3` | 57.1 s     | **68.4 s**            |
| `release` with `cgu=16`, `lto=off`, `debug=0`        | —          | 11.6 s                |
| `dev` as-is (`debug=2`)                              | 16.8 s     | —                     |
| **`dev` with `debug=0`**                             | 14.4 s     | **1.83 s**            |
| `cargo check --all-targets`                          | 18.5 s     | —                     |
| `cargo clippy`                                       | 12.3 s     | —                     |
| `cargo test --lib` (1,351 tests)                     | —          | 93.6 s                |

The spread between 68.4 s and 1.83 s is **37×**, on one crate, one machine, one compiler version.
Nothing about the language changed between those two rows — only the profile did.

### Disk

| Component                                             | Size       | Notes                                             |
| ----------------------------------------------------- | ---------- | ------------------------------------------------- |
| `~/.rustup` — six toolchains                          | 7.2 GB     | `rust-toolchain.toml` pins exactly **one**        |
| Shared cargo target cache `~/.cache/ose-cargo-target` | 8.2 GB     | **7.5 GB of it belongs to `ose-primer`**          |
| └─ `ose-public` / `rhino-cli` share                   | ~0.3 GB    | The share this repo is actually responsible for   |
| `~/.cargo/registry`                                   | 0.31 GB    | Regenerable; Cargo auto-cleans on a 3-month lag   |
| **Total attributed to "Rust is eating my disk"**      | **~16 GB** |                                                   |
| **Reclaimable today with no code change**             | **~7 GB**  | 5 superseded toolchains + the stale sibling cache |

Per-configuration `target/` composition, same crate:

| Profile                                    | `target/` total | Largest contributor                      |
| ------------------------------------------ | --------------- | ---------------------------------------- |
| `release` (shipped settings)               | 223 MB          | `release/deps` 186 MB                    |
| `release` + `cgu=16`, `lto=off`, `debug=0` | 208 MB          | —                                        |
| `dev` (`debug=2`)                          | 615 MB          | `debug/deps` 419 MB; `incremental` 89 MB |
| **`dev` + `debug=0`**                      | **360 MB**      | Debug info alone accounts for 255 MB     |

Largest single artefacts in `release/deps`: `librhino_cli.rlib` 16 MB, `libsyn` 6.5 MB,
`libregex_syntax` 6.4 MB, `libregex_automata` 5.3 MB. The final stripped binary is 3.9 MB.

### Type safety

`apps/rhino-cli` already denies more than most Rust codebases: `unsafe_code = "forbid"`,
`missing_docs = "deny"`, `clippy::pedantic` at warn, and `unwrap_used`, `panic`,
`missing_errors_doc`, `missing_panics_doc`, `doc_markdown`, `missing_docs_in_private_items` all at
deny. The audit confirms these are working, not decorative:

| Signal                                           | Count | Reading                                                  |
| ------------------------------------------------ | ----- | -------------------------------------------------------- |
| `.unwrap()` in **production** paths              | **0** | The `unwrap_used = "deny"` gate holds                    |
| `.unwrap()` inside `#[cfg(test)]`                | 1,958 | Legitimate; test code is exempt by design                |
| `panic!`/`todo!`/`unimplemented!`/`unreachable!` | 4     | Small enough to inspect individually                     |
| Unchecked index/slice sites                      | 1,983 | Not proven panic-free; the largest open surface          |
| `.expect(` sites                                 | 241   | Each is an undischarged claim that a state is impossible |
| `as` casts                                       | 49    | Each can silently truncate or wrap                       |
| `#[allow(...)]` attributes                       | 190   | **189 carry no `reason`** — suppression without a record |
| `anyhow!`/`bail!`/`ensure!` sites                | 243   | Type-erased; callers cannot branch on failure kind       |
| `&str`/`String` parameters                       | 885   | Primitive obsession surface; path-role confusion likely  |

Two clippy `restriction` lints are **deliberately allowed today** with a written rationale in
`Cargo.toml`: `indexing_slicing` and `arithmetic_side_effects`. The rationale — that this CLI does
file and line counting, not finance or cryptography — is sound for the _arithmetic_ half. It is
weaker for the _indexing_ half: `rhino-cli` parses arbitrary Markdown, YAML, LCOV, Cobertura, and
Gherkin from the working tree and reads `git` subprocess output, all of which is unpredictable
input by definition. An indexing panic on a malformed file aborts a quality gate with a bare panic
message and no exit-code semantics.

### Dead weight

Three dependencies are declared in `Cargo.toml` and referenced **nowhere** in the crate:
`tree-sitter` (0.26.9), `pulldown-cmark` (0.13.4), and `ignore` (0.4.25). Confirming this needed two
independent greps — one for `use <crate>` and one for `\b<crate>::` — because Rust permits
fully-qualified paths with no `use` line, so either grep alone would have been unsound (see
[`learnings.md`](./learnings.md) L2).

## First-principles decomposition

### Axis A — why the build is slow

Build time for one edit is:

```text
T = (units recompiled) × (optimization work per unit) + (link work) × (number of binaries)
```

Term by term, as measured:

| Term                                 | Current value                                       | Why it is what it is                                                                           |
| ------------------------------------ | --------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| units recompiled                     | The whole crate, `codegen-units = 1`                | `cgu = 1` collapses the crate into ~one unit, defeating the parallelism thin-LTO could exploit |
| optimization work per unit           | `opt-level = 3` + `lto = "thin"`                    | The most aggressive setting short of fat LTO — correct for shipping, wrong for an edit loop    |
| link work                            | Apple's default `ld`                                | Already the fastest available on this platform in 2026; not a lever (see `tech-docs.md`)       |
| number of binaries                   | **22** `harness = false` test binaries + lib + bin  | Each statically links the entire library; `cargo check --all-targets` pays for all of them     |
| **why release reaches the dev loop** | **53 invocation sites** shell `cargo run --release` | Across 27 `project.json` files, 3 Husky shims, and `pr-quality-gate.yml`                       |

The last row is the root cause. The other rows are the mechanism.

### Axis B — why the disk fills

```text
D = (toolchains × size) + (target dirs × size) + (debug-info share) + (registry) + (incr. caches)
```

| Term              | Measured                                      | Governed by                                                         |
| ----------------- | --------------------------------------------- | ------------------------------------------------------------------- |
| toolchains × size | 6 × ~1.2 GB = 7.2 GB, of which 5 are unpinned | Nobody. `rustup` has **no built-in GC** — the request is still open |
| target dirs       | 8.2 GB shared, 92% of it a sibling repo's     | The ambient build-artifact sweeper, which had not reclaimed it      |
| debug-info share  | 255 MB of a 615 MB dev `target/` (41%)        | `[profile.dev] debug`, unset today so it defaults to full           |
| registry          | 0.31 GB                                       | Cargo's own `cache.auto-clean-frequency`, on a 3-month lag          |
| incremental cache | 89 MB per dev target dir                      | `[profile.*] incremental`                                           |

The dominant term is the one **nothing owns**. This is why the axis is not solved by a one-time
cleanup: it regrows on the next `rustup update`.

### Axis C — what the compiler is not currently asked to prove

Rust proves memory safety and freedom from data races. It does not prove absence of panics, absence
of arithmetic wraparound in release mode, absence of leaks, absence of deadlocks, or anything at all
about business correctness. Of the failure modes that remain, `rhino-cli`'s configuration already
closes the panic-by-`unwrap` path completely. What stays open, in order of exposure:

1. **Index/slice panics on untrusted input** — 1,983 sites, reachable from any malformed file in
   the working tree. The compiler is not being asked.
2. **Silent wraparound in release mode** — arithmetic panics in debug, wraps in release. Low
   consequence for counters, but the guarantee is absent rather than reasoned about per site.
3. **Undischarged impossibility claims** — 241 `.expect(` sites each assert a state cannot occur,
   with no gate confirming that claim.
4. **Unrecorded suppressions** — 189 `#[allow(...)]` with no `reason`, so nobody can tell a
   considered exception from a silenced warning.
5. **Type-erased errors** — 243 `anyhow` sites mean a caller cannot branch on failure kind without
   a runtime `downcast_ref`.

Items 1 and 2 are the ones the maintainer has chosen to close crate-wide. Items 3-5 come along for
the ride at far lower cost.

## Success metrics

Each is falsifiable in **both** directions: the pre-state must fail the check and the post-state
must pass it, and both are asserted at the phase gate.

| ID  | Metric                                                                                                           | Baseline       | Target             |
| --- | ---------------------------------------------------------------------------------------------------------------- | -------------- | ------------------ |
| M1  | One-line-edit rebuild of the binary the gates actually invoke                                                    | 68.4 s         | **< 10 s**         |
| M2  | `cargo run --release` invocation sites remaining in `project.json`, Husky shims, and workflows                   | 53             | **0**              |
| M3  | Integration-test binaries linking the full library                                                               | 22             | **1**              |
| M4  | `cargo test --lib` wall clock                                                                                    | 93.6 s         | **< 60 s**         |
| M5  | Declared-but-unreferenced dependencies in `Cargo.toml`                                                           | 3              | **0**              |
| M6  | Installed rustup toolchains not pinned by any sibling repo's `rust-toolchain.toml`                               | 5              | **0**              |
| M7  | Total Rust footprint across `~/.rustup`, `~/.cargo`, and the shared target cache                                 | ~16 GB         | **< 6 GB**         |
| M8  | Unpinned toolchains regrowing undetected after a `rustup update`                                                 | undetected     | **`doctor` warns** |
| M9  | `clippy::indexing_slicing` diagnostics at deny, crate-wide                                                       | lint off       | **0 at deny**      |
| M10 | `clippy::arithmetic_side_effects` diagnostics at deny, crate-wide                                                | lint off       | **0 at deny**      |
| M11 | `#[allow(...)]` attributes without a `reason`                                                                    | 189            | **0**              |
| M12 | `.expect(` sites on fallible paths (`expect_used` at deny)                                                       | 241            | **0 at deny**      |
| M13 | A commit touching only `apps/rhino-cli/src/**/*.rs` is listed by `nx show projects --affected`                   | **not listed** | **listed**         |
| M14 | Observable CLI contract — every command's stdout, stderr, and exit code, shadow-diffed against the frozen binary | n/a            | **byte-identical** |
| M15 | `apps/rhino-cli` byte-identity with `ose-private` under the parity manifest                                      | holds          | **still holds**    |
| M16 | Documentation restating a fact this plan invalidates — invocation form, test layout, lint contract, boundary     | many           | **0**              |
| M17 | Downstream `beaver-nest-repo-consolidation` steps citing a path or command this plan removed                     | 5              | **0**              |

M14 is the constraint every other metric is subordinate to. Any phase that improves a number by
changing observable behaviour has failed, not succeeded.

M16 is measured the same way in both directions: the grep that finds the stale statement must
return a non-zero count before the sweep and zero after. A sweep reporting only its post-state
cannot distinguish "fixed" from "the fact was never stated there".

## Affected roles

| Role                       | Effect                                                                                       |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| Repository maintainer      | Commit and push gates stop being a minutes-long wait; ~10 GB of disk returns                 |
| AI agents executing plans  | Faster gate turnaround per iteration; fewer timeouts and stale-lock retries                  |
| CI                         | Shorter `pr-quality-gate` runs; less contention on the shared runner pool                    |
| Future `rhino-cli` authors | A stricter lint contract catches malformed-input panics at compile time, not at gate runtime |

## Business risks

| ID  | Risk                                                                                                                 | Likelihood | Impact | Mitigation                                                                                                                           |
| --- | -------------------------------------------------------------------------------------------------------------------- | ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| R1  | The Axis C crate-wide sweep across 1,983 sites introduces a behavioural regression while "improving" safety          | **High**   | High   | Staged module by module, each stage shadow-diffed against the frozen binary; POC measures real diagnostic count on one module first  |
| R2  | A faster dev profile makes the gate binary slower at runtime, and 21 gate invocations per commit+push amplify it     | Medium     | Medium | POC measures **end-to-end gate wall clock**, not just build time; abandon-if is stated in terms of the gate, not the compiler        |
| R3  | Machine-wide toolchain pruning breaks a sibling repo mid-build                                                       | Medium     | Medium | `rustup` re-fetches on demand from any `rust-toolchain.toml`; prune only toolchains no sibling pins, verified per repo before acting |
| R4  | The byte-identity gate with `ose-private` fails because changes land in one repo and not the other                   | Medium     | High   | The two repos' changes are one delivery unit, landing together, per the parity-manifest obligation                                   |
| R5  | Consolidating 22 test binaries loses test isolation and masks a failure that previously surfaced                     | Medium     | Medium | Test **count** and per-test names are asserted equal before and after; consolidation is mechanical, not a rewrite                    |
| R6  | The `nx affected` gap turns out to be an upstream Nx bug with no local fix                                           | Medium     | Low    | Fall back to a detection-independent pre-push invocation; the gap is already the status quo, so the downside is bounded              |
| R7  | Effort is spent on Axes A-C and the targets are still missed, so Axis D is entered having burned the budget          | **Low**    | Medium | M1's target is already met by a measured 1.83 s figure before the plan starts; the risk is concentrated in Axis C, which is gated    |
| R8  | Removing the three dead dependencies breaks a build path that greps did not reveal                                   | Low        | Low    | Removal is one commit, verified by a full clean build plus the whole test corpus; trivially revertible                               |
| R9  | The downstream `beaver-nest-repo-consolidation` plan's steps go stale, because they cite artefacts this plan changes | **High**   | Medium | Named explicitly as a hand-off obligation in `delivery.md` §Downstream hand-off, and mirrored into that plan's own prerequisites     |
| R10 | A concurrent agent operating in the primary checkout reverts uncommitted plan work                                   | Medium     | Medium | All implementation runs in per-axis worktrees; never run a git-capable agent in the primary tree while plan work is uncommitted      |
| R11 | Documentation is swept only where it was obviously broken, leaving governance rules half-propagated                  | **High**   | Medium | Phase 14 runs two explicit passes — `repo-rules-maker` for the governance surface, grep-driven manual edits for everything else      |
| R12 | `ose-primer`'s delayed manual sync is treated as a blocking participant, stalling a delivery unit                    | Medium     | Low    | Scope is exactly two repos; `ose-primer` picks changes up on its own schedule and nothing in this plan waits for it                  |
