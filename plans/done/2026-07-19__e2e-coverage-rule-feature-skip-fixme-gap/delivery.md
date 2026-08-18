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

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

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
- [ ] Create the `learnings.md` scaffold file at
      `plans/backlog/2026-07-18__e2e-coverage-rule-feature-skip-fixme-gap/learnings.md` (sibling to
      this file) containing only the running-log header comment (see the
      [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)).
      Acceptance: the file exists and contains the header comment only.
- [ ] Run `npx nx run rhino-cli:test:quick` — record the result as the Phase 0 baseline. Acceptance:
      exits 0 (green) before any code changes begin.
- [ ] Search `docs/reference/` (glob `*.md`) and grep `apps/rhino-cli/README.md` for a DD-6-equivalent
      design-decision doc describing the e2e-coverage skip/fixme detection mechanism (see
      `tech-docs.md` DD-2). Acceptance: either a specific target doc path is identified and recorded
      here for Phase 3 to update, or the search confirms none exists (the `## Specs: E2E Coverage Gap
Detection` section of `apps/rhino-cli/README.md` is a CLI usage/flags doc, not a
      design-decision doc, and does not qualify) — in which case DD-2's fallback applies: this plan's
      own `tech-docs.md` remains the durable record and Phase 3's doc-refresh step is a no-op.

### Phase 0 Gate

- [ ] Baseline clean and green

> **Pause Safety**: safe to stop here.

## Phase 1: RED

- [ ] Add a Rust unit-test fixture for AC-1 (`Rule:`-level `@skip`) to
      `apps/rhino-cli/src/application/e2e_coverage/parser.rs`'s `#[cfg(test)] mod tests` block —
      new test `scan_skip_or_fixme_describe_titles_detects_skip_suffixed_rule` (_new test_), mirroring
      the sibling `scan_skip_or_fixme_describe_titles_detects_skip_suffixed_outline` (same file,
      around line 621) but with a `spec_js` string shaped like a `Rule:`-wrapping
      `test.describe.skip(...)` block containing a nested plain `test(...)`. Run
      `npx nx run rhino-cli:test:unit` — acceptance: the new test currently FAILS (the function
      does not yet return the Rule's nested title), reproducing the false-PASS gap.

  **Gherkin (underpins) →** "A Rule-level @skip tag is detected as unbound"

  ```gherkin
  Scenario: A Rule-level @skip tag is detected as unbound
    Given a .feature file with a "Rule:" block tagged "@skip"
    And the Rule contains at least one Scenario
    And the file also has other, non-skipped content so it still generates
    When "specs e2e-coverage validate" runs
    Then every scenario nested under the skipped Rule is reported as unbound
  ```

- [ ] Add a Rust unit-test fixture for AC-2 (`Feature:`-level `@fixme`) to the same test module — new
      test `scan_skip_or_fixme_describe_titles_detects_fixme_suffixed_feature` (_new test_),
      mirroring the sibling `scan_skip_or_fixme_describe_titles_detects_fixme_suffixed_outline`
      (around line 636) with a `Feature:`-wrapping `test.describe.fixme(...)` shape. Run
      `npx nx run rhino-cli:test:unit` — acceptance: the new test currently FAILS, reproducing the
      false-PASS gap.

  **Gherkin (underpins) →** "A Feature-level @fixme tag is detected as unbound"

  ```gherkin
  Scenario: A Feature-level @fixme tag is detected as unbound
    Given a .feature file whose top-level "Feature:" is tagged "@fixme"
    When "specs e2e-coverage validate" runs
    Then every scenario in the file is reported as unbound
  ```

- [ ] Add a Rust unit-test fixture for AC-3 (`.only`-tagged Rule guard) to the same test module — new
      test `scan_skip_or_fixme_describe_titles_ignores_only_suffixed_rule` (_new test_), mirroring
      the sibling `scan_skip_or_fixme_describe_titles_ignores_only_suffixed_outline` (around line
      648). Keep the existing Outline-level tests (around lines 621-654) unmodified as the AC-4
      guard — no new code needed for AC-4. Run `npx nx run rhino-cli:test:unit` — acceptance: the
      AC-3 test and the existing AC-4 (Outline) tests all PASS against current (pre-fix) code.

  **Gherkin (underpins) →** "AC-3 - .only is still excluded (no false positive)"; "AC-4 - existing
  Outline-level detection is unaffected"

  ```gherkin
  Scenario: AC-3 - .only is still excluded (no false positive)
    Given a .feature file with a "Rule:" block tagged "@only"
    When "specs e2e-coverage validate" runs
    Then no scenario under that Rule is reported as unbound

  Scenario: AC-4 - existing Outline-level detection is unaffected
    Given the existing Outline-level @skip/@fixme regression fixture
    When "specs e2e-coverage validate" runs
    Then it still correctly reports the Outline's scenarios as unbound
  ```

### Phase 1 Gate

- [ ] Run `npx nx run rhino-cli:test:unit` — acceptance: the AC-1 and AC-2 tests FAIL (false PASS
      reproduced); the AC-3 and AC-4 guard tests PASS against current code.

> **Pause Safety**: safe to stop here; only fixtures + failing tests exist.

## Phase 2: GREEN

- [ ] Generalize `scan_skip_or_fixme_describe_titles` in
      `apps/rhino-cli/src/application/e2e_coverage/parser.rs` per `tech-docs.md` DD-1 — rewrite it
      to match the wrapping `describe` block's structural shape (a `.skip`/`.fixme`-suffixed block
      with plain unsuffixed `test(...)` calls nested inside) regardless of whether it came from a
      `Scenario Outline`, `Rule`, or `Feature` node.
- [ ] Run `npx nx run rhino-cli:test:unit` — acceptance: all 4 AC tests (AC-1 through AC-4, added in
      Phase 1) pass, and no other existing test in the crate is broken.
- [ ] Add 2 new `@unit`-tagged `Scenario:` blocks to
      `specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature` — "A Rule-level @skip
      tag is detected as unbound" (covering AC-1) and "A Feature-level @fixme tag is detected as
      unbound" (covering AC-2) — mirroring the existing `Given`/`When`/`Then` style already used in
      that file. Tag the AC-1 and AC-2 Rust tests added in Phase 1 with a matching
      `// @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:<Scenario
title>` comment, following the existing convention (e.g.
      `apps/rhino-cli/src/application/e2e_coverage/parser.rs:764`). Acceptance:
      `grep -c "^  Scenario:" specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature`
      increases by 2, and both new Rust tests carry a `@covers` comment.
- [ ] Run `npx nx run rhino-cli:specs:behavior:coverage` — acceptance: exits 0 (the new `@covers`
      links resolve and the behavior-spec tree stays in sync with the Rust test suite).

### Phase 2 Gate

- [ ] All 4 ACs pass; `npx nx run rhino-cli:test:unit` full suite green;
      `npx nx run rhino-cli:specs:behavior:coverage` exits 0.

> **Pause Safety**: safe to stop here.

## Phase 3: REFACTOR

- [ ] Update the doc comment above `scan_skip_or_fixme_describe_titles` in
      `apps/rhino-cli/src/application/e2e_coverage/parser.rs` (currently scoped to describe only the
      `Scenario Outline` case) to describe Feature/Rule/Outline-level detection uniformly.
      Acceptance: the doc comment no longer says "Outline" exclusively; it names all three node
      types.
- [ ] Refresh the design-decision doc identified in Phase 0 (per `tech-docs.md` DD-2) — if Phase 0
      found an existing durable doc (`docs/reference/` or elsewhere), update it to describe the
      generalized Feature/Rule/Outline detection; if Phase 0 confirmed none exists, this step is a
      no-op (this plan's own `tech-docs.md` already documents the decision). Acceptance: either the
      identified doc is updated and cross-referenced here, or the no-op is explicitly recorded here.

### Phase 3 Gate

- [ ] Run `npx nx run rhino-cli:lint` — clean. This bundles
      `cargo fmt --manifest-path apps/rhino-cli/Cargo.toml -- --check` and
      `cargo clippy --manifest-path apps/rhino-cli/Cargo.toml --all-targets -- -D warnings`, matching
      `apps/rhino-cli/project.json`'s actual `lint` target verbatim.

> **Pause Safety**: safe to stop here.

## Phase 4: Quality Gates

- [ ] `nx run-many -t specs:e2e:coverage` across all 11 wired projects — confirm no new
      false-positive failures; baseline any genuine pre-existing gap the stricter check surfaces
- [ ] Run `npx nx affected -t typecheck lint test:quick` — acceptance: all targets green.
      (`test:quick` already runs `test:specs` → `specs:behavior:coverage` for `rhino-cli`, so no
      separate `specs:coverage`/`specs:behavior:coverage` target needs to be listed here.)

> **Important**: Fix ALL failures found during these quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix preexisting errors
> encountered during work. Do not defer or mention-and-skip existing issues.

### Phase 4 Gate

- [ ] All affected targets green across all 11 projects

> **Pause Safety**: safe to stop here.

## Phase 5: Commit, Push, PR (ose-public) + Sibling Repos

- [ ] Commit changes thematically — group related changes into logically cohesive commits. Follow
      Conventional Commits format (`<type>(<scope>): <description>`); split different domains/
      concerns into separate commits (e.g. `feat(rhino-cli): ...` for the parser generalization
      separate from `docs(rhino-cli): ...` for any design-decision doc refresh); do NOT bundle
      unrelated fixes into a single commit. Push and open a draft PR against `main`.
- [ ] Propagate byte-identically to `ose-primer` and `ose-infra`; open their draft PRs.
- [ ] Monitor the `pr-quality-gate` GitHub Actions workflow
      (`.github/workflows/pr-quality-gate.yml`) for each of the 3 PRs — watch for failures, fix
      immediately, and do NOT proceed to Phase 6 until all 3 PRs show `pr-quality-gate` green.

### Phase 5 Gate

- [ ] All 3 PRs OPEN, `pr-quality-gate` green

> **Pause Safety**: safe to stop here.

## Phase 6: PR-Review Cycles (all 3 repos)

- [ ] Run the PR-Review Maker→Fixer Cycle (default 3 cycles) on each of the 3 PRs

### Phase 6 Gate

- [ ] All 3 PRs: 3 cycles complete, CI green, no unresolved blocking findings

> **Pause Safety**: safe to stop here.

## Phase 7: Knowledge Capture

- [ ] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason.
- [ ] Apply the secret/sensitivity gate — sanitize any secret, credential, token, or private
      hostname to a `<placeholder>` token, or discard if unsanitizable.
- [ ] Apply the repo-relevance gate — infra-private content stays in `ose-infra` only and is NEVER
      cross-routed into `ose-public`/`ose-primer`.
- [ ] Route each surviving learning to exactly one durable home per the open-ended routing matrix;
      code homes (`apps/`, `libs/`, tests) are ALWAYS filed as a separate `plans/backlog/<slug>/`
      plan, NEVER landed inline (the only carve-out is a genuine blocker required to finish this
      plan's own scope).
- [ ] Record the terminal state of every entry (routed inline / filed as backlog at `<path>` /
      discarded with reason) directly in `learnings.md`.
- [ ] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md` instead of individual entries.

### Phase 7 Gate

- [ ] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded with
      reason), or the explicit "none" escape is recorded.
- [ ] No code-homed learning landed inline in this plan's own commits/PR.

> **Pause Safety**: `learnings.md` is fully triaged (or explicitly empty). Safe to stop. To resume:
> re-read `learnings.md` and confirm every entry is terminal.

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

- Local: `npx nx run rhino-cli:test:unit`, `npx nx run rhino-cli:lint`,
  `nx run-many -t specs:e2e:coverage` (all 11 wired projects),
  `npx nx affected -t typecheck lint test:quick` (already includes `specs:behavior:coverage` via
  `test:specs`)
- CI: all checks green on every PR (`pr-quality-gate` workflow)

## Verification

All 4 Gherkin ACs pass; `nx run-many -t specs:e2e:coverage` exits 0 across all 11 projects;
`npx nx run rhino-cli:specs:behavior:coverage` exits 0.
