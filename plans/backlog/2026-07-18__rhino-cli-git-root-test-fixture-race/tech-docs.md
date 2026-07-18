# Technical Documentation: rhino-cli Git Root Test Fixture Race

## Architecture

`apps/rhino-cli/src/infrastructure/git/root.rs` resolves the repository root from any CWD, including
from inside a linked git worktree. Its test coverage for the worktree case
(`find_root_from_worktree_returns_worktree_path`, ~line 75) needs a REAL linked worktree to exercise
the resolution logic honestly (mocking git's worktree layout would undertest the real behavior) — the
bug is not "using a real worktree," it's "creating that real worktree somewhere that can collide with
the actual repository under concurrent execution."

## Root-Cause Hypothesis (unverified — first task of this plan is to confirm)

The fixture likely does one of:

1. Runs `git init`/`git worktree add` relative to the process's actual current working directory
   instead of a dedicated `tempfile::TempDir`, so if the test's own CWD-restoration (`CwdLock` guard)
   loses a race against another concurrently-running git test in the same binary, the fixture's setup
   commands execute against the real repository instead of an isolated sandbox.
2. Or: the fixture does use a temp dir, but the temp dir itself is created as a child path/symlink
   that resolves back into the real worktree tree under some condition, causing `git worktree add` to
   register against the real `.git/worktrees/` metadata rather than a fully separate `.git`.

Both hypotheses are consistent with all observed evidence (see README.md's Symptom Evidence section):
a real linked worktree appears in `git worktree list` against the real repo, pinned to a "init"-only
commit authored by the fixture's hardcoded `Test <test@test.com>` identity.

## Design Decisions

### DD-1 — Fully temp-dir-scoped fixture, no CWD dependency

Rewrite the fixture to construct its throwaway git repository and any linked worktree entirely via
absolute paths rooted in a fresh `tempfile::TempDir`, with every git invocation passing `-C
<tempdir-path>` (or equivalent) explicitly rather than relying on `std::env::set_current_dir` +
restore. This removes the CWD race entirely rather than trying to make the existing
lock/restore-based approach more robust — a stronger guarantee than tightening the lock.

**Rationale**: `CwdLock`-based approaches only work if every test in the process respects the lock;
one CWD-mutating test elsewhere that doesn't (or a lock implementation bug) reintroduces the race.
Removing the CWD dependency entirely is the strictly safer design.

### DD-2 — Regression test proves isolation adversarially

A new test explicitly runs the fixture concurrently (e.g., spawn multiple threads or processes
executing the fixture's setup logic in parallel) and asserts the real repository's `git
worktree list` / `HEAD` are unchanged before and after — a positive proof of isolation, not just
"the existing suite still passes serially."

## File-Impact Analysis

- `apps/rhino-cli/src/infrastructure/git/root.rs` — fixture rewrite + new regression test.
- Any sibling file in `apps/rhino-cli/src/infrastructure/git/` found by the audit step to share the
  same pattern.

## Testing Strategy

TDD: RED (reproduce the race deterministically, e.g. via a tight concurrent-execution harness) → GREEN
(temp-dir-scoped rewrite) → REFACTOR. Per the
[Regression Test Mandate](../../../repo-governance/development/quality/regression-test-mandate.md),
the regression test must fail against the pre-fix code and pass against the fix.

## Dependencies

None beyond what `rhino-cli` already depends on (likely already has `tempfile` as a dev-dependency;
confirm during Phase 0).

## Risks and Rollback

Low risk — test-only change, no production CLI behavior changes. Rollback is a straightforward
`git revert` of the fixture commit if the rewrite is later found to undertest the real resolution
logic.
