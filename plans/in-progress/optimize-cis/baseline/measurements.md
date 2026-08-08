# Baseline Measurements — Phase 0 (captured 2026-08-09)

Machine: Darwin 24.5.0 (Apple Silicon), repo `ose-public` worktree `optimize-cis`. Method: `bash`
loop-and-divide harness per `tech-docs.md` §Method note — never `zsh` (unquoted-var word-split
trap), never `python3` timestamp subprocesses (startup swamps measurement). This session's Bash
tool executes under `zsh` by default, so every timed command below was explicitly wrapped in
`bash script.sh` / `bash -c '...'`, and exit codes were asserted for every run.

## M1 — Pre-commit wall time, markdown-only commit (10 files)

**Mean: 3,898 ms (N=3)** — runs: 4,315 ms, 3,791 ms, 3,589 ms. All 3 runs exited 0.

Method: staged trivial, reversible one-line appends to 10 existing non-critical `.md` files (see
list below), timed `npx lint-staged --no-stash` under `bash` with `date +%s%N` before/after
(nanosecond, bash builtin — no subprocess), then `git checkout HEAD -- <files>` to fully revert
both index and working tree after each run. `git status --porcelain` confirmed clean after the
harness completed (only `plans/in-progress/optimize-cis/baseline/` remained untracked).

Files used:

```text
docs/how-to/add-new-app.md
docs/reference/monorepo-structure.md
repo-governance/conventions/formatting/linking.md
repo-governance/conventions/formatting/indentation.md
repo-governance/conventions/formatting/emoji.md
repo-governance/conventions/writing/quality.md
repo-governance/development/workflow/commit-messages.md
repo-governance/development/workflow/worktree-setup.md
repo-governance/development/quality/markdown.md
repo-governance/conventions/structure/file-naming.md
```

This is the current-form (unoptimized) `lint-staged` `*.md` pipeline: `prettier --write` via
`npx`, `markdownlint-cli2` via `npx`, and four `cargo run --release --quiet --manifest-path
apps/rhino-cli/Cargo.toml -- md {mermaid,heading-hierarchy,naming,frontmatter} validate` gates —
consistent with the per-gate figures in `tech-docs.md` §A.2 (current-form sum 2,659 ms for the
gates alone; the full `npx lint-staged` wrapper adds its own process-launch/glob-matching overhead
on top, which is why the end-to-end figure here is higher than the per-gate sum).

## M2 — `rhino-cli:test:quick` wall time

**Wall: 2m4.299s (124.3 s)** — `user 2m40.893s`, `sys 0m35.709s`.
Command: `bash -c 'time npx nx run rhino-cli:test:quick --skip-nx-cache'`. All five subtargets
(`typecheck`, `lint`, `test:unit` — 1,365 tests passed / 0 failed / 1 ignored, `test:coverage`,
`test:specs` — structure validate + behavior-coverage validate, 67 specs / 447 scenarios / 1,825
steps all covered) succeeded; overall Nx target reported success.

## M3 — CI runner-seconds (`pr-quality-gate`, median)

**Median: 7,103.5 runner-seconds** across 18 completed `pr-quality-gate` runs (of the last 50 CI
runs on `ose-public`, 19 were `pr-quality-gate`, 18 completed). Per-run figure = sum of
`completed_at - started_at` across every job in that run, fetched via
`gh api repos/wahidyankf/ose-public/actions/runs/<id>/jobs`. Sorted per-run totals (seconds):

```text
6960 6963 7016 7016 7027 7042 7048 7065 7100 7107 7125 7162 7211 7213 7247 7283 8940 9076
```

Median = mean of the two middle values (9th/10th of 18): (7,100 + 7,107) / 2 = 7,103.5.

## M4 — CI wall-clock (`pr-quality-gate`, p50)

**p50: 974.5 s (16.2 min)** across the same 18 runs. Per-run wall-clock = `updatedAt - createdAt`
from `gh run list --json databaseId,workflowName,status,conclusion,createdAt,startedAt,updatedAt`.
Sorted per-run totals (seconds):

```text
858 863 875 881 882 885 886 922 931 1018 1035 1155 1216 1234 1392 1957 2044 2465
```

Median = mean of the two middle values (9th/10th of 18): (931 + 1,018) / 2 = 974.5.

Note the wide spread (858 s to 2,465 s) — wall-clock includes queueing/scheduling delay on the
shared GitHub-hosted runner pool, not just execution time; M3 (runner-seconds) is the more stable
signal of actual CI compute cost.

## M6 — `test:quick` isolated `CARGO_TARGET_DIR` size

**Size: 2,747 MiB (2.75 GiB) / 2,880 MB decimal** — `2,813,036 KB` via `du -sk`.

Method: `CARGO_TARGET_DIR=<isolated-tmp-dir> npx nx run rhino-cli:test:quick --skip-nx-cache`
(cold — the isolated dir started empty, so this is a full-rebuild figure across `typecheck`,
`lint`, `test:unit`, `test:coverage` — including `cargo llvm-cov` instrumentation build — and
`test:specs`), then `du -sk` on the isolated dir. `test:quick` exited 0. Scratch dir removed after
measurement (2.8 GB is too large to leave in scratchpad).

## M7 — GitHub Actions cache usage (`ose-public`)

**Total: 8,280,363,514 bytes = 7.71 GiB = 77.12 % of the 10 GiB ceiling.**

Command: `gh api repos/wahidyankf/ose-public/actions/caches --jq '[.actions_caches[].size_in_bytes] | add'`.
30 cache entries currently exist.

## M8 — Disk buckets (`tech-docs.md` §D.1)

Fresh `du -sk` capture, same five buckets as `tech-docs.md` §D.1. **Not directly comparable to the
2026-08-08 tech-docs snapshot** — this session's own Phase 0 work (`npm install`, `doctor --fix`,
two `test:quick` runs for M2/M6) grew `~/.cache/ose-cargo-target/` materially since that snapshot
was taken (post-sweep, pre-work).

| #   | Bucket                                 |   GiB | Share of measured total (26.64 GiB) | `tech-docs.md` 2026-08-08 |
| --- | -------------------------------------- | ----: | ----------------------------------: | ------------------------: |
| 1   | `ose-public/local-temp/`               | 12.31 |                             46.21 % |                     12.31 |
| 2   | `~/.rustup/toolchains/` (6 toolchains) |  7.21 |                             27.05 % |                      7.21 |
| 3   | `~/.cache/ose-cargo-target/`           |  4.29 |                             16.09 % |                      1.97 |
| 4   | `~/.dotnet/`                           |  1.51 |                              5.66 % |                      1.51 |
| 5   | `~/Library/Caches/ms-playwright/`      |  1.33 |                              4.99 % |                      1.33 |

`local-temp`, `~/.rustup/toolchains`, `~/.dotnet`, and `~/Library/Caches/ms-playwright` match the
tech-docs snapshot exactly (unchanged since 2026-08-08). `~/.cache/ose-cargo-target/` grew from
1.97 GiB to 4.29 GiB — expected, driven by this Phase 0's own measurement runs (M2, M6), not drift
or a defect. `node_modules/` duplication remains unmeasured here too (present now after `npm
install`, but not one of the five tracked buckets).
