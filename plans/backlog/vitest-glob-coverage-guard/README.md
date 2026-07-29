# Vitest Glob-Coverage Guard

> **Status**: Backlog (not started). Filed from a Knowledge Capture learning surfaced during
> [`ayokoding-www-tools-ai-benchmark`](../../done/2026-07-30__ayokoding-www-tools-ai-benchmark/README.md)'s
> PR #122 cycle-3 review (`pr-review-integrity-maker`, HIGH finding F2).

## Context

`apps/ayokoding-www/vitest.config.ts` splits tests into two named `projects` — `unit` (Node
environment, `test/unit/be-steps/**/*.steps.ts` + `**/*.unit.{test,spec}.{ts,tsx}`) and `unit-fe`
(jsdom environment, `test/unit/fe-steps/**/*.steps.{ts,tsx}` + `src/features/**/*.test.{ts,tsx}`).
The EWT-003 regression test (`benchmark-content.test.tsx`) was added under
`src/app/[locale]/tools/ai-benchmark/`, a directory neither project's `include` glob matched.

`pr-review-integrity-maker` proved the consequence empirically: it reverted the actual EWT-003 code
fix and re-ran the full suite, which still passed 144/144 test files with the bug fully
reintroduced — the regression test meant to catch it never executed. No error, no warning, just a
silent zero-execution count. The fix landed inline in this plan (widening `unit-fe`'s glob to also
cover `src/app/**/*.test.{ts,tsx}`, verified not to double-run already-covered `.unit.test.ts`
files), but the underlying defect class — a test file can be well-written and 100% logically
correct and still provide zero protection if it lives outside every configured test-project's
`include` glob — is not itself fixed anywhere else in the repo.

## Why This Generalizes

This is a config/glob-path-mismatch defect class distinct from a test's own logical correctness. It
can recur anywhere a new test file is added under a new directory shape (a new feature slice, a new
route segment, a new `apps/*`/`libs/*` project) without checking it matches an existing
`vitest.config.ts` (or other test-runner) project's `include` globs — and because it fails silently
(`passWithNoTests: true` plus a project glob mismatch means zero files matched, not zero files
failed), nothing short of an explicit glob-coverage check would catch it automatically.

## Proposed Investigation

- Design a coverage-of-globs check: for each `apps/*`/`libs/*` project with a `vitest.config.ts`
  (or other test-runner config), verify every `*.test.{ts,tsx}` / `*.steps.{ts,tsx}` /
  `*.unit.test.{ts,tsx}` file under that project's source tree matches at least one configured test
  project's `include` glob.
- Decide the home for this check: a new lightweight script wired into an existing Nx target (e.g.
  `test:quick` or a dedicated `specs:coverage`-style target), or an enhancement to an existing
  checker agent (`ci-checker` or `swe-code-checker`).
- Scope whether this should span every `apps/*`/`libs/*` project with a Vitest config, or start
  narrowly with `ayokoding-www` (the project where the gap was found) and expand once proven.

## Scope

**In scope**: a durable, automated guard that fails CI (or a checker report) when a test file
exists outside every configured test-project's glob.

**Out of scope**: re-litigating the specific `unit-fe` glob fix already merged in
`ayokoding-www-tools-ai-benchmark`'s PR #122; any change to test content or assertions.

## Delivery Mode

`worktree-to-pr` (the repo default) — this is a tooling/CI-guard change, so it is filed as its own
plan per the code-homed-learnings-are-never-landed-inline rule rather than folded into any single
app's plan.
