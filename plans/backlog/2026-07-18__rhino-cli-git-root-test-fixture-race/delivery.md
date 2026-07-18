# Delivery Checklist: rhino-cli Git Root Test Fixture Race

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it. `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note. A phase is not complete until its gate is green.

## Worktree

Worktree path: `worktrees/rhino-cli-git-root-test-fixture-race/`

```bash
claude --worktree rhino-cli-git-root-test-fixture-race
```

## Delivery Mode: worktree-to-pr

Work happens in the dedicated worktree; integration target is a draft PR against `main`; the final PR
merge is `[HUMAN]` (unless a session-level AI-merge override is explicitly granted). Runs the
PR-Review Maker→Fixer Cycle (default 3 cycles) before merge.

## Multi-Repo rhino-cli Delivery

This plan changes `rhino-cli` test-only source inside the
[rhino-cli byte-identity boundary](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary).
The fix lands byte-identically in `ose-public`, `ose-primer`, and `ose-infra` — three peer PRs, each
independently reviewed and gated, per the same multi-repo delivery pattern used by
`plans/done/2026-07-18__e2e-scenario-coverage-gap-detector`.

## Phase 0: Setup and Baseline

- [ ] Enter/provision the worktree; `npm install`; `npm run doctor -- --fix`
- [ ] Record `rhino-cli:test:quick` baseline (must be green before starting)
- [ ] Confirm `tempfile` (or equivalent) is already a `rhino-cli` dev-dependency, or add it

### Phase 0 Gate

- [ ] `npm run doctor -- --fix` clean; `rhino-cli:test:quick` green

> **Pause Safety**: safe to stop here; nothing changed yet.

## Phase 1: Root-Cause Confirmation

- [ ] Read `find_root_from_worktree_returns_worktree_path` and every sibling test in
      `apps/rhino-cli/src/infrastructure/git/root.rs` in full
- [ ] Confirm (or refute) DD-1's hypothesis by tracing exactly how the fixture's git operations are
      scoped (CWD-relative vs. explicit path) — record the confirmed mechanism in `tech-docs.md`
- [ ] Audit sibling test files in `apps/rhino-cli/src/infrastructure/git/` for the same pattern; list
      every file needing the same fix

### Phase 1 Gate

- [ ] Root cause confirmed and documented with evidence (not just the prior hypothesis restated)

> **Pause Safety**: safe to stop here; still read-only.

## Phase 2: RED — Reproduce the Race Deterministically

- [ ] Write a new test that runs the existing (pre-fix) fixture concurrently with another
      `CwdLock`-guarded git test and asserts zero change to the real repo's `git worktree list`/`HEAD`
      — confirm this test fails against the current code (proving it actually reproduces the race)

### Phase 2 Gate

- [ ] New test fails against unmodified code, with a failure mode matching the observed symptom

> **Pause Safety**: safe to stop here; only a new failing test exists.

## Phase 3: GREEN — Temp-Dir-Scoped Fixture Rewrite

- [ ] Rewrite `find_root_from_worktree_returns_worktree_path`'s setup (and every sibling identified in
      Phase 1) to construct its git repo/worktree entirely inside a `tempfile::TempDir`, with every
      git invocation using an explicit path argument rather than CWD mutation
- [ ] Re-run the Phase 2 regression test; confirm it now passes

### Phase 3 Gate

- [ ] All git-root tests green, including the new regression test; `cargo test` full suite green

> **Pause Safety**: safe to stop here; fix is in place and tested.

## Phase 4: REFACTOR

- [ ] Extract any shared temp-dir-scoped git fixture helper if 2+ tests now share the same setup
      pattern
- [ ] Doc-comment the fixture explaining why it is temp-dir-scoped (the historical race, briefly)

### Phase 4 Gate

- [ ] `cargo clippy -D warnings` clean; `cargo fmt --check` clean

> **Pause Safety**: safe to stop here.

## Phase 5: Quality Gates

- [ ] `nx affected -t typecheck lint test:quick specs:coverage` green
- [ ] Fix any preexisting failures found incidentally (Root Cause Orientation)

### Phase 5 Gate

- [ ] All affected targets green

> **Pause Safety**: safe to stop here.

## Phase 6: Commit, Push, PR (ose-public)

- [ ] Thematic conventional commit(s)
- [ ] Push to origin PR branch; open draft PR against `main`
- [ ] Monitor CI; verify all checks pass

### Phase 6 Gate

- [ ] CI green on the pushed PR branch

> **Pause Safety**: safe to stop here; PR is open.

## Phase 6a/6b: Sibling Repos (ose-primer, ose-infra)

- [ ] Propagate the byte-identical fix to `ose-primer`; open its own draft PR
- [ ] Propagate the byte-identical fix to `ose-infra`; open its own draft PR
- [ ] Run each sibling's own local quality gates

### Phase 6a/6b Gate

- [ ] Byte-identity holds across all 3 repos; both sibling PRs OPEN with CI green

> **Pause Safety**: safe to stop here.

## Phase 7: PR-Review Cycles (all 3 repos)

- [ ] Run the PR-Review Maker→Fixer Cycle (default 3 cycles) on each of the 3 PRs
- [ ] Confirm all quality gates green on each PR after its cycles complete

### Phase 7 Gate

- [ ] All 3 PRs: 3 cycles complete, CI green, no unresolved blocking findings

> **Pause Safety**: safe to stop here; PRs open and reviewed.

## Phase 8: Knowledge Capture

- [ ] Triage `learnings.md` (litmus test, both safety gates, route each surviving entry)
- [ ] Record the explicit "none" escape if no new generalizable learning surfaced

### Phase 8 Gate

- [ ] Knowledge Capture complete per the
      [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)

> **Pause Safety**: safe to stop here.

## Phase 9: Archival

- [ ] `git mv` this plan folder to `plans/done/YYYY-MM-DD__rhino-cli-git-root-test-fixture-race/`
- [ ] Update `plans/backlog/README.md` and `plans/done/README.md`
- [ ] Commit and push the archival move; wait for CI green

### Phase 9 Gate

- [ ] Archival committed, CI green on that commit

> **Pause Safety**: safe to stop here.

## Final Merge

- [ ] `[HUMAN]` (or AI, if the executing session carries an explicit merge override) merges all 3 PRs

## Quality Gates (summary)

- Local: `cargo test`, `cargo clippy -D warnings`, `cargo fmt --check`,
  `nx affected -t typecheck lint test:quick specs:coverage`
- CI: all checks green on every PR

## Verification

`cargo test --test-threads=<N>` (chosen to reliably reproduce the original race) run repeatedly shows
zero change to the real repository's `git worktree list`/`git reflog` before vs. after.
