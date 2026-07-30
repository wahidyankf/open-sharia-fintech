# Technical Design: Vitest Glob-Coverage Guard

## Defect Class

This is a config/glob-path-mismatch defect class distinct from a test's own logical correctness. It
can recur anywhere a new test file is added under a new directory shape without checking it matches
an existing `vitest.config.ts` (or other test-runner) project's `include` globs — and because it
fails silently (`passWithNoTests: true` plus a project glob mismatch means zero files matched, not
zero files failed), nothing short of an explicit glob-coverage check would catch it automatically.

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
