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

## Scope

**In scope**: a durable, automated guard that fails CI (or a checker report) when a test file
exists outside every configured test-project's glob; investigation phase to design and place that
guard.

**Out of scope**: re-litigating the specific `unit-fe` glob fix already merged in
`ayokoding-www-tools-ai-benchmark`'s PR #122; any change to test content or assertions.

## Business Rationale (Condensed BRD)

**Why this matters**: a silently-zero-executed test file is worse than a missing test — it reads as
covered in every status report (file exists, is well-formed, references real assertions) while
providing zero actual protection. The EWT-003 incident showed this can survive a full green CI run
and a passing PR review; only a targeted revert-and-rerun caught it. **Affected roles**: any
engineer or AI agent adding a new test file under a directory shape not yet covered by an existing
`vitest.config.ts` project (a new feature slice, a new route segment, a new `apps/*`/`libs/*`
project). **Success metric**: zero silently-uncovered test files across all Vitest-configured
projects, verified by an automated check rather than manual glob review — gut-based, no fabricated
KPI.

## Product Requirements (Condensed PRD)

**User story**: As an engineer or AI agent adding a new test file to a Vitest-configured project, I
want an automated check that fails when my test file's path doesn't match any configured project's
`include` glob, so that I learn immediately (not months later via an empirical revert) that my test
provides zero protection.

**Gherkin acceptance criteria**:

```gherkin
Feature: Vitest glob-coverage guard

  Scenario: A new test file lands outside every configured project's include glob
    Given a Vitest-configured project with one or more named "projects" entries
    And a new "*.test.{ts,tsx}" file is added under that project's source tree
    When the file's path matches no configured project's "include" glob
    Then the guard fails with the file path and the reason (glob mismatch)

  Scenario: A test file matches an existing project's include glob
    Given a Vitest-configured project with one or more named "projects" entries
    And a test file whose path matches at least one configured project's "include" glob
    When the guard runs
    Then the guard passes with no findings for that file
```

**Product scope**: covers every `apps/*`/`libs/*` project with a `vitest.config.ts` (or other
test-runner config exposing named `include` globs); does not cover test **content** correctness,
only path-to-glob coverage.

## Technical Approach

This is a config/glob-path-mismatch defect class distinct from a test's own logical correctness. It
can recur anywhere a new test file is added under a new directory shape without checking it matches
an existing `vitest.config.ts` (or other test-runner) project's `include` globs — and because it
fails silently (`passWithNoTests: true` plus a project glob mismatch means zero files matched, not
zero files failed), nothing short of an explicit glob-coverage check would catch it automatically.

**Proposed Investigation**:

- Design a coverage-of-globs check: for each `apps/*`/`libs/*` project with a `vitest.config.ts`
  (or other test-runner config), verify every `*.test.{ts,tsx}` / `*.steps.{ts,tsx}` /
  `*.unit.test.{ts,tsx}` file under that project's source tree matches at least one configured test
  project's `include` glob.
- Decide the home for this check: a new lightweight script wired into an existing Nx target (e.g.
  `test:quick` or a dedicated `specs:coverage`-style target), or an enhancement to an existing
  checker agent (`ci-checker` or `swe-code-checker`).
- Scope whether this should span every `apps/*`/`libs/*` project with a Vitest config, or start
  narrowly with `ayokoding-www` (the project where the gap was found) and expand once proven.

## Worktree

Worktree path: `worktrees/vitest-glob-coverage-guard/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree vitest-glob-coverage-guard
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

## Delivery Checklist

`[AI]` = agent-executable step. `[HUMAN]` = requires a human decision or credential this repo's
agents may not exercise. No `[HUMAN]` step is anticipated for this plan — recorded for completeness
per the legend convention.

### Phase 1: Investigation and Guard Design

- [ ] [AI] Confirm scope: enumerate every `apps/*`/`libs/*` project with a `vitest.config.ts` (or
      equivalent) exposing named `include` globs
- [ ] [AI] Decide the guard's home (new script + Nx target vs. an existing checker agent
      enhancement) and its failure mode (CI-blocking vs. checker-report)
- [ ] [AI] Prototype the guard against the current repo state and confirm it reproduces the
      EWT-003 zero-coverage condition when replayed against the pre-fix glob

### Phase 1 Gate

- [ ] [AI] The guard, run against the current repo, reports zero uncovered test files
- [ ] [AI] The guard, run against a synthetic reintroduction of the EWT-003 glob gap, reports
      exactly that file as uncovered

> **Pause Safety**: this plan is Backlog (not started) — no work has begun, so there is nothing to
> resume. Promotion to `in-progress/` re-reads this README from the top.

## Quality Gates

Local: `npx nx affected -t typecheck lint test:quick` (once the guard lands as code) exits 0.
CI: the same targets green on the PR's own CI run before merge, per this repo's standard PR Merge
Protocol.

## Verification

The plan is complete when the guard exists, is wired into an Nx target or checker agent, passes
against the current repo (zero uncovered test files), and demonstrably fails against a
reintroduced glob-coverage gap (verified by the synthetic-reintroduction check in the Phase 1
Gate above).

## Delivery Mode

`worktree-to-pr` (the repo default) — this is a tooling/CI-guard change, so it is filed as its own
plan per the code-homed-learnings-are-never-landed-inline rule rather than folded into any single
app's plan.
