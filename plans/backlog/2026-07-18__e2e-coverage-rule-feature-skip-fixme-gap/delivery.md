# Delivery Checklist: E2E Coverage Rule/Feature Skip/Fixme Gap

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it. `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` plus a `> **Pause Safety**:` note.

## Worktree

Worktree path: `worktrees/e2e-coverage-rule-feature-skip-fixme-gap/`

```bash
claude --worktree e2e-coverage-rule-feature-skip-fixme-gap
```

## Delivery Mode: worktree-to-pr

Work happens in the dedicated worktree; integration target is a draft PR against `main`; final merge
is `[HUMAN]` (unless a session-level AI-merge override is explicitly granted). Runs the PR-Review
Maker→Fixer Cycle (default 3 cycles) before merge.

## Multi-Repo rhino-cli Delivery

Changes `rhino-cli` source inside the
[rhino-cli byte-identity boundary](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary).
Lands byte-identically in `ose-public`, `ose-primer`, `ose-infra` as three peer PRs, per the same
multi-repo pattern used by the originating plan.

## Phase 0: Setup and Baseline

- [ ] Enter/provision the worktree; `npm install`; `npm run doctor -- --fix`
- [ ] Record `rhino-cli:test:quick` baseline (must be green)
- [ ] Locate the current durable home for the e2e-coverage design-decision doc (see tech-docs.md DD-2)

### Phase 0 Gate

- [ ] Baseline clean and green

> **Pause Safety**: safe to stop here.

## Phase 1: RED

- [ ] Add a `Rule:`-tagged-`@skip` fixture (AC-1) and confirm it currently produces a false PASS
- [ ] Add a `Feature:`-tagged-`@fixme` fixture (AC-2) and confirm it currently produces a false PASS
- [ ] Add/confirm a `.only`-tagged Rule guard fixture (AC-3) and the existing Outline guard (AC-4)

### Phase 1 Gate

- [ ] AC-1/AC-2 fixtures fail (false PASS reproduced); AC-3/AC-4 guards pass against current code

> **Pause Safety**: safe to stop here; only fixtures + failing tests exist.

## Phase 2: GREEN

- [ ] Generalize `scan_skip_or_fixme_describe_titles` per tech-docs.md DD-1
- [ ] Re-run all 4 AC fixtures; confirm all pass

### Phase 2 Gate

- [ ] All 4 ACs pass; `cargo test` full suite green

> **Pause Safety**: safe to stop here.

## Phase 3: REFACTOR

- [ ] Update the function's doc comment to describe Feature/Rule/Outline-level detection uniformly
- [ ] Refresh the design-decision doc per tech-docs.md DD-2

### Phase 3 Gate

- [ ] `cargo clippy -D warnings` clean; `cargo fmt --check` clean

> **Pause Safety**: safe to stop here.

## Phase 4: Quality Gates

- [ ] `nx run-many -t specs:e2e:coverage` across all 11 wired projects — confirm no new false-positive
      failures; baseline any genuine pre-existing gap the stricter check surfaces
- [ ] `nx affected -t typecheck lint test:quick specs:coverage` green

### Phase 4 Gate

- [ ] All affected targets green across all 11 projects

> **Pause Safety**: safe to stop here.

## Phase 5: Commit, Push, PR (ose-public) + Sibling Repos

- [ ] Thematic conventional commit(s); push; open draft PR
- [ ] Propagate byte-identically to `ose-primer` and `ose-infra`; open their draft PRs
- [ ] Verify CI green on all 3 PRs

### Phase 5 Gate

- [ ] All 3 PRs OPEN, CI green

> **Pause Safety**: safe to stop here.

## Phase 6: PR-Review Cycles (all 3 repos)

- [ ] Run the PR-Review Maker→Fixer Cycle (default 3 cycles) on each of the 3 PRs

### Phase 6 Gate

- [ ] All 3 PRs: 3 cycles complete, CI green, no unresolved blocking findings

> **Pause Safety**: safe to stop here.

## Phase 7: Knowledge Capture

- [ ] Triage `learnings.md`; record explicit "none" escape if nothing new surfaced

### Phase 7 Gate

- [ ] Knowledge Capture complete

> **Pause Safety**: safe to stop here.

## Phase 8: Archival

- [ ] `git mv` this plan folder to `plans/done/YYYY-MM-DD__e2e-coverage-rule-feature-skip-fixme-gap/`
- [ ] Update `plans/backlog/README.md` and `plans/done/README.md`
- [ ] Commit, push, wait for CI green

### Phase 8 Gate

- [ ] Archival committed, CI green

> **Pause Safety**: safe to stop here.

## Final Merge

- [ ] `[HUMAN]` (or AI, if the executing session carries an explicit merge override) merges all 3 PRs

## Quality Gates (summary)

- Local: `cargo test`, `cargo clippy -D warnings`, `cargo fmt --check`,
  `nx run-many -t specs:e2e:coverage`, `nx affected -t typecheck lint test:quick specs:coverage`
- CI: all checks green on every PR

## Verification

All 4 Gherkin ACs pass; `nx run-many -t specs:e2e:coverage` exits 0 across all 11 projects.
