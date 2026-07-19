# Product Requirements: rhino-cli Git Root Test Fixture Race

## Product Overview

Make `apps/rhino-cli/src/infrastructure/git/root.rs`'s worktree-root-resolution tests fully isolated
from the real repository, under any concurrency level, so `nx affected`/`nx run-many` fanout can never
again write a stray commit or register a stray linked worktree against the real `.git`.

## Personas

- **Plan executor (AI or human)** running `nx affected -t test:quick` in a worktree, especially under
  parallel pre-push/CI fanout.
- **rhino-cli maintainer** relying on `cargo test` results being trustworthy and non-destructive.

## User Stories

- As a plan executor, I want `cargo test` (and any Nx target that invokes it) to never touch the real
  repository's git state, so that a stray commit or worktree registration cannot silently appear on my
  working branch.
- As a rhino-cli maintainer, I want the git-root test fixture to prove its own isolation under
  concurrent execution, so a future contributor cannot reintroduce this bug without a test failing.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: rhino-cli git-root test fixture isolation

  Scenario: AC-1 - fixture never touches the real repository's .git
    Given the git-root test suite runs from within a real git worktree
    When "find_root_from_worktree_returns_worktree_path" (and any sibling fixture using the same
      real-worktree-creation pattern) executes
    Then no commit is created on the real repository's current branch
    And no linked worktree is registered against the real repository's .git

  Scenario: AC-2 - fixture survives concurrent execution
    Given the git-root test suite is run with test-thread parallelism sufficient to reproduce the
      originally observed race
    When "find_root_from_worktree_returns_worktree_path" runs concurrently with the operation
      identified by Phase 1 as interacting with it (another CwdLock-guarded git test in the same
      module, if hypothesis 1/2 is confirmed; the specs_coverage.rs test suite or an nx
      affected-style multi-process fanout, if hypothesis 3 is confirmed)
    Then both tests pass
    And "git worktree list" and "git reflog" on the real repository show zero change before vs. after
      the run

  Scenario: AC-3 - no leftover git identity contamination
    Given the fixture's own throwaway git identity ("Test <test@test.com>")
    When the test completes, regardless of pass or fail
    Then the real repository's local "git config user.*" is unchanged from before the test ran
```

## Product Scope

**In scope**: `apps/rhino-cli/src/infrastructure/git/root.rs` and any sibling test file in the same
module found by the audit to share the same real-worktree fixture pattern.

**Out of scope**: any other rhino-cli test module unrelated to git-worktree-root resolution.

## Product-Level Risks

- A temp-dir-based rewrite could silently stop testing the real worktree-detection code path if the
  temp dir isn't itself set up as a genuine git worktree — mitigate by keeping the fixture's git
  operations identical in kind (a real `git init` + `git worktree add`), just relocated entirely
  inside a `tempfile::TempDir` (or equivalent) rather than the process's actual CWD/repo.
