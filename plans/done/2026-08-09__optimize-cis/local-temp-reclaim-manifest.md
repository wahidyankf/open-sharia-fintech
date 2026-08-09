# `local-temp/` Reclaim Manifest

Enumerated 2026-08-09 against `ose-public/local-temp/` (M8 bucket 1, 12.31 GiB — the **primary
checkout's** `local-temp/`, not the worktree's, which holds only 9 MB of this plan's own CI evidence).

Phase 9 admits a path **only** when all five predicates hold. Each was evaluated mechanically.

## Result: zero rows admitted

**No path in `local-temp/` satisfies all five predicates, so nothing is quarantined and nothing is
deleted.** The ≥ 9 GB acceptance is **NOT MET** — see [Why](#why-the-predicates-exclude-everything).

## Candidates evaluated

Sizes via `du -sk`; mtimes via `stat -f '%Sm'`; reference check via `git grep -l -F` across tracked
files in the primary checkout.

| Path (under `local-temp/`)             |     Size | mtime            | P1 name | P2 regen cmd | P3 > 7 d | P4 isolation | P5 unreferenced | Admitted |
| -------------------------------------- | -------: | ---------------- | ------- | ------------ | -------- | ------------ | --------------- | -------- |
| `plan04-next-static-export-diagnostic` | 5.03 GiB | 2026-08-02 16:43 | NO      | NO           | NO       | yes          | yes             | **no**   |
| `plan04-next-diagnostic-stale`         | 2.97 GiB | 2026-08-02 16:40 | NO      | NO           | NO       | yes          | yes             | **no**   |
| `plan04-next-webpack-failed`           | 1.31 GiB | 2026-08-02 16:39 | NO      | NO           | NO       | yes          | yes             | **no**   |
| `plan04-next-overlap-failure`          | 1.15 GiB | 2026-08-02 16:44 | NO      | NO           | NO       | yes          | yes             | **no**   |
| `plan04-next-nx-stale-20260802-1652`   | 0.40 GiB | 2026-08-02 16:50 | NO      | NO           | NO       | yes          | yes             | **no**   |
| `plan04-next-prebuild`                 | 0.08 GiB | 2026-08-02 16:28 | NO      | NO           | NO       | yes          | yes             | **no**   |
| `npm-cache`                            | 0.36 GiB | —                | NO      | n/a          | —        | yes          | yes             | **no**   |
| `rustup-home`                          | 0.31 GiB | —                | NO      | n/a          | —        | yes          | yes             | **no**   |
| `cargo-home`                           | 0.05 GiB | —                | NO      | n/a          | —        | yes          | yes             | **no**   |

Sum of the six `plan04-*` entries: **10.94 GiB** — enough to clear the 9 GB bar, had they qualified.

## Why the predicates exclude everything

**Predicate 1 (artifact-directory name)** requires the directory to be named `.next`, `dist`, `out`,
`build`, `target`, or `node_modules`. A search of `local-temp/` to depth 2 for those names returns
**nothing**. The six large entries are Next.js build outputs — each contains a `BUILD_ID`, satisfying
the `.next` sub-clause — but every one was **renamed** when it was captured, to record which failure
state it represents (`-webpack-failed`, `-overlap-failure`, `-diagnostic-stale`). The predicate tests
the name, and the name no longer says `.next`.

**Predicate 3 (mtime older than 7 days)** fails for all six independently. Newest is 2026-08-02
16:50, oldest 2026-08-02 16:28; evaluated at 2026-08-09 01:46 that is **6 d 9 h** — inside the
window by roughly 15 hours.

**Predicate 2 (a named regeneration command)** cannot be satisfied in principle for four of the six.
They are captures of _specific past failure states_ from plan04 — a stale Nx cache, a webpack
failure, an export/overlap conflict. There is no command that regenerates a particular historical
failure. This is the predicate that matters most: these directories are **evidence**, not artifacts.

Predicates 4 and 5 pass for every row — nothing sits under `generated-reports/`, no `.env*`, no
git-tracked file, no `git worktree list` entry, no `.git`; and no tracked file in the primary
checkout references any of these paths.

## Disposition

Nothing is moved or deleted. Two predicates failing is not a technicality to route around: the
7-day window exists to stop exactly this — reclaiming recent diagnostic captures — and Phase 9 states
its predicates are machine-checkable precisely so that no judgement call can override them. Waiting
out the ~15-hour remainder would still leave predicates 1 and 2 unsatisfied.

The reclaim that **is** legitimately available lands in Phase 10, which already owns the Rust
toolchain prune (M8 bucket 2, 7.21 GiB across six toolchains, of which only `1.95.0` is required
after DD-9 unifies the pins). `~/.cache/ose-cargo-target/` (bucket 3, 4.29 GiB) is a genuine
`target`-named regenerable build directory, but it is outside `local-temp/` and so outside this
step's stated scope.

**Follow-up for the Phase 11 rollup**: predicate 1 tests a directory's _name_ while its intent is
"this is regenerable build output." A `BUILD_ID`-bearing directory is Next.js output whatever it has
been renamed to, so a future revision should test the marker rather than the name — and should pair
that with an explicit _evidence_ exclusion, since the renames here exist precisely to mark these
directories as evidence worth keeping.
