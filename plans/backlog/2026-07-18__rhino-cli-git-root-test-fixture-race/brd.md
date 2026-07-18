# Business Requirements: rhino-cli Git Root Test Fixture Race

## Business Goal and Rationale

`rhino-cli` is the repo's own governance tooling — it must be trustworthy to run, including under the
parallel test fanout every pre-push hook and CI run already performs. A test that can corrupt the
real repository it runs inside (stray commits, stray registered worktrees, mis-attributed authorship)
undermines that trust and costs real recovery time whenever it triggers — 4 occurrences in a single
plan's PR-review cycles this session, each requiring careful manual verification before repair.

## Business Impact

- **Pain points**: Lost time diagnosing an unexplained `"init"` commit; risk of a less-careful
  recovery accidentally discarding real work; mis-attributed commit authorship polluting `git blame`/
  `git log` history on real, already-merged fixes.
- **Expected benefit**: Zero risk of test-triggered repository corruption regardless of parallel test
  load, restoring full trust in `nx affected`/`nx run-many` fanout across this and future plans.

## Affected Roles

- Any agent or human running `nx affected -t test:quick` (or any target that includes
  `rhino-cli:test:unit`) in a worktree, especially under parallel CI/pre-push fanout.

## Success Metrics

- _Observable fact_: the fixture's regression test (added by this plan) passes when run repeatedly
  under `cargo test --test-threads=<N>` for `N` chosen to reliably reproduce the original race, with
  zero writes observable outside its own temp directory (verified via `git worktree list` and
  `git reflog` on the real repo showing no change before/after the test run).
- _Judgment call_: no further stray-commit/stray-worktree incident should recur on any future plan's
  PR-review cycles once this fix lands — tracked qualitatively, not with a fabricated numeric target.

## Business Scope Non-Goals

- Not a general audit of every rhino-cli test's fixture isolation — scoped specifically to the
  `infrastructure/git/root.rs` fixture(s) implicated by this session's incidents (with a narrow,
  explicit audit of sibling tests in the same file/module, per the README's in-scope section).

## Business Risks and Mitigations

- **Risk**: a fix that changes fixture setup could itself introduce a new, subtler test-isolation gap.
  **Mitigation**: the regression test added by this plan must positively prove isolation under
  concurrent execution, not merely re-pass the existing (non-adversarial) test suite.
- **Risk**: fixing this in isolation without auditing sibling tests leaves a similar bug elsewhere in
  the same module. **Mitigation**: the in-scope audit step in README.md/delivery.md.
