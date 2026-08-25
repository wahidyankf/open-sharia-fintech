# Benchmark: the rhino-cli Rust-to-F# rewrite

Nine rows, two columns, one table per repository. Every cell in both columns is seeded with the same
three-letter placeholder and is overwritten only by a real measurement — Phase 0 fills the **Before**
column, Phase 10 fills **After**. The placeholder appears nowhere else in this plan, so a count of it
is an honest progress reading.

The plan documents are single-sourced in `ose-public`; `ose-private` carries no copy of this folder.
Its figures therefore live here, in a second table, rather than in a `benchmark.md` of its own.

Gate arithmetic, counted as **occurrences** rather than lines, because a table row carries both of
its cells on one physical line:

| Point                             | `PH=$(printf 'TB%s' D); /usr/bin/grep -o "$PH" benchmark.md \| wc -l` |
| --------------------------------- | --------------------------------------------------------------------- |
| At seeding (one table)            | 18                                                                    |
| After the `ose-public` Before run | 9                                                                     |
| End of Phase 0 (both tables)      | 18                                                                    |
| End of Phase 10                   | 0                                                                     |

The count returns to 18 at the end of Phase 0 rather than falling to 9, because P0.17 adds the
second table: nine filled `ose-private` **Before** cells and nine fresh **After** placeholders.

The command above assigns `$PH` inline via `printf` so it is self-contained and runnable verbatim
from this page. Copying only the `grep` half without the `PH=...;` prefix silently returns `0` —
which happens to match this same table's "End of Phase 10" row, so a partial copy reads as "done"
when it has measured nothing. Always run the full `PH=...; grep ...` command together. The
placeholder token itself is still never spelled out in prose, because doing so would inflate the
very count these gates read.

**Baseline provenance.** Only **B1** in each table below was re-measured after the tree-sitter
dependency removal — see the [Phase 0 note](#phase-0-note) for both post-removal figures
(17.59 s / 73 crates in `ose-public`, 16.00 s / 73 crates in `ose-private`). Every other row —
**B2 through B8**, in both the `ose-public` and `ose-private` tables — records a Before figure
measured against the **pre-removal** dependency graph (79 crates, tree-sitter still linked) and
has not been re-measured since; each such value is marked `†` below. Read every `†`-marked Before
value as a pre-removal baseline until it is re-measured, and account for that when Phase 10 fills
the After column and Verdict for those rows.

## Measurements — ose-public

| Row  | Metric                        | Before (Rust) | After (F#) | Verdict |
| ---- | ----------------------------- | ------------- | ---------- | ------- |
| B1   | Cold build                    | 17.59 s       | TBD        | —       |
| B2   | Gate-profile build            | 34.44 s †     | TBD        | —       |
| B3   | Warm no-op build              | 0.24 s †      | TBD        | —       |
| B4   | Edit-rebuild loop             | 0.43 s †      | TBD        | —       |
| B5   | Startup, mean of 50           | 11.2 ms †     | TBD        | —       |
| B6   | Full `.husky/pre-commit`      | 5.24 s †      | TBD        | —       |
| B7   | CI critical path, build job   | 70.67 s †     | TBD        | —       |
| B8   | Artifact size                 | 4,489,616 B † | TBD        | —       |
| Size | Source lines (tests included) | 49,460        | TBD        | —       |

## Measurements — ose-private

| Row  | Metric                        | Before (Rust) | After (F#) | Verdict |
| ---- | ----------------------------- | ------------- | ---------- | ------- |
| B1   | Cold build                    | 16.00 s       | TBD        | —       |
| B2   | Gate-profile build            | 35.57 s †     | TBD        | —       |
| B3   | Warm no-op build              | 0.17 s †      | TBD        | —       |
| B4   | Edit-rebuild loop             | 0.35 s †      | TBD        | —       |
| B5   | Startup, mean of 50           | 15.3 ms †     | TBD        | —       |
| B6   | Full `.husky/pre-commit`      | 3.38 s †      | TBD        | —       |
| B7   | CI critical path, build job   | 88.67 s †     | TBD        | —       |
| B8   | Artifact size                 | 4,489,616 B † | TBD        | —       |
| Size | Source lines (tests included) | 49,460        | TBD        | —       |

`†` — pre-removal baseline (79 crates, tree-sitter still linked); see "Baseline provenance" above.

Verdict is filled at Phase 10 with `better` / `worse` / `unchanged` plus the absolute delta, per
repository. No row is dropped for being unfavourable to F#.

**Noise floor for the Verdict column.** Unless a bullet below states an explicit repeat count (B3,
B5, B7), the recorded figure is a **single run** — B1, B2, B4, and B6 were not repeated. This doc's
own repeated measurement shows how much that matters: B3's two consecutive warm-build runs differed
by 42% in `ose-public` and by 4.4x in `ose-private`, and B3's and B4's table values are each smaller
than that spread. At Phase 10, any row's Before/After delta smaller than the larger of (a) the
cross-repo noise floor stated below (~1-2 s) or (b) that row's own observed run-to-run spread, where
one was measured, is recorded as `unchanged`, never `better`/`worse` — the raw delta is still
written alongside so it is not lost, only not over-read as a directional result.

## Measurement commands

Each command is recorded here verbatim so the F# side at Phase 10 is measured the same way rather
than a way that flatters it. Every one asserts exit code 0; a crashing binary must not report a
fast time. Timing is Python `time.time()` around a `subprocess.run`, not `/usr/bin/time -p`, which
dropped its `real` line on several runs here. Both repositories were measured with the same script
on the same machine, though not simultaneously, so cross-repo differences of a second or two are
machine noise rather than signal.

- **B1** — `cargo build --offline` into a throwaway `CARGO_TARGET_DIR`. `ose-public` **17.59 s**,
  73 crates, `debug/rhino-cli` 21,597,000 bytes. `ose-private` **16.00 s**, 73 crates, 21,597,016
  bytes.
- **B2** — `cargo build --profile gate` into a throwaway `CARGO_TARGET_DIR`, the profile CI actually
  builds. `ose-public` **34.44 s** / 79 crates; `ose-private` **35.57 s** / 79 crates.
- **B3** — the same build run twice against a warm target; the second run is the figure.
  `ose-public` 0.34 s then **0.24 s**; `ose-private` 0.75 s then **0.17 s**. Neither second run
  emitted a `Compiling` line or changed the binary mtime.
- **B4** — touch one source file, rebuild. The plan-prescribed target is `src/main.rs`, which is a
  14-line shim over `src/lib.rs`, so only the thin bin crate relinks: **0.43 s** in `ose-public`,
  **0.35 s** in `ose-private`. Because that figure flatters Rust against any F# comparison, the
  honest second measurement is recorded too — touching `src/commands/gate/validate.rs` (2,766 lines)
  costs **13.15 s** in `ose-public` and **15.24 s** in `ose-private`. Phase 10 must reproduce both
  shapes.
- **B5** — 50 invocations of `--help`, exit code asserted per iteration. `ose-public` total 0.562 s,
  mean **11.2 ms**; `ose-private` total 0.767 s, mean **15.3 ms**. Zero non-zero exits in either.
- **B6** — one full `.husky/pre-commit` against a pinned staged set: a single new
  `apps/rhino-cli/bench-probe.md` holding one heading and one paragraph, staged, hook run, then the
  file removed and the index reset. Pinning the staged set is what makes the two repositories
  comparable, because every gate in this hook is file-type scoped. `ose-public` **5.24 s**,
  `ose-private` **3.38 s**, both exit 0, both restored to their exact prior `git status --porcelain`.
  An earlier `ose-public` run against an unpinned staged set read 7.25 s, and an instrumented
  variant of it read 6.66 s while recording **5** rhino-cli binary invocations through a counting
  `RHINO_CLI_BIN` wrapper. That invocation count is the figure Phase 10 compares; the 7.25 s wall
  time is superseded by the pinned-protocol 5.24 s above and is kept only so the change is visible
  rather than silent.
- **B7** — the `build-rhino` job duration from the three most recent green `pr-quality-gate.yml`
  runs on `main`. `ose-public`: 73 s, 69 s, 70 s (runs 32810578748, 32797537004, 32796057166), mean
  **70.67 s**. `ose-private`: 89 s, 88 s, 89 s (runs 32797359073, 32796938182, 32795391522), mean
  **88.67 s**.
- **B8** — byte count of the `gate`-profile binary: **4,489,616** bytes in both repositories, equal
  in size. No digest was taken, so this is evidence of matching size only, not of byte-identity.
  It is also not the parity check: `apps/rhino-cli/parity-manifest.sha256` hashes 603 tracked
  source files and covers no build artifact, so an equal binary size here is a separate, weaker
  observation from what that manifest asserts.

## Source size

Non-blank, non-comment `.rs` lines — **not** non-test lines despite this row's name in the tables
above: the `awk` filter below strips only leading whitespace, blank lines, and `//`-prefixed lines,
with no `#[cfg(test)]` handling. Measured at **49,460** lines across 189 `.rs` files in each
repository, of which 132 files contain at least one `cfg(test)` block; a brace-depth accounting of
those blocks attributes roughly 45% of the 49,460 figure to `#[cfg(test)]` bodies. The exact
command:

```bash
find apps/rhino-cli/src -name '*.rs' -type f -print0 | xargs -0 cat \
  | awk '{ sub(/^[ \t]+/,""); if ($0=="") next; if ($0 ~ /^\/\//) next; print }' | wc -l
```

Phase 10 runs the identical command with `-name '*.fs'` against the F# tree, which counts the same
thing (non-blank, non-comment lines, tests included) — but only if the F# port keeps its tests
inside `src-fsharp/`. If Phase 10 places tests in a separate project outside that path (the
idiomatic xUnit layout), the identical command stops being comparable: the Rust figure is ~45% test
code and the F# figure would be closer to 0%. Phase 10 must record which layout it used before
filling this row's Verdict.

## Phase 0 note

The Before figure for B1 was measured twice in each repository — once as found, and again after the
unused `tree-sitter` dependency was removed from `Cargo.toml`. `ose-public` as found: **19.91 s**,
79 crates, 21,597,224 bytes; after removal **17.59 s**, 73 crates, 21,597,000 bytes. `ose-private`
as found: **22.39 s**, 79 crates, 21,597,240 bytes; after removal **16.00 s**, 73 crates,
21,597,016 bytes. Both tables' **B1** row records the post-removal figure; B2 through B8 do not —
see "Baseline provenance" above the measurement tables.

`rhino-cli:test:quick` exits 0 after the removal in both repositories, so each baseline is a working
one. In `ose-private` the target was also run before the removal, uncached, at 441.72 s, and after
it at 363.06 s; the first `ose-private` run of the day returned a full Nx cache hit in 1.99 s, which
is why every recorded figure here uses `--skip-nx-cache`.
