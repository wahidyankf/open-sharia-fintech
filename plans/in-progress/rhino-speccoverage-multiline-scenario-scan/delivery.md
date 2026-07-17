# Delivery — Rhino speccoverage multi-line scenario scan

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase is
> not complete until its gate is green; do not start phase N+1 while any gate check fails.

## Worktree

Worktree path: `worktrees/rhino-speccoverage-multiline-scenario-scan/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree rhino-speccoverage-multiline-scenario-scan
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Work in `worktrees/rhino-speccoverage-multiline-scenario-scan/`; open a draft PR against `main`;
`[HUMAN]` merges when ready. The finalization phase runs the **PR-Review Maker→Fixer Cycle**
(`pr-review-maker` → `pr-review-fixer`, default 3 sequential CI-gated cycles) before the `[HUMAN]`
merge. "Done" is a green, fully-reviewed PR handed off; "merged" happens on the maintainer's own
schedule. See
[Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode)
and the [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md).
`ose-primer` and `ose-infra` resolve this same `worktree-to-pr` mode independently, each inside its
own repo — see the Multi-Repo rhino-cli Delivery note immediately below.

## Multi-Repo rhino-cli Delivery

This plan changes `apps/rhino-cli` — inside the byte-identity boundary (see
[README.md § Key constraint](./README.md#key-constraint-rhino-cli-byte-identity)) — so the rhino-cli
change (`checker.rs`, the spec-coverage feature scenario, the gherkin README count row, and
`tests/spec_coverage.rs`) MUST land byte-identically in **all three repos**: `ose-public`,
`ose-primer`, `ose-infra`. Each repo goes through its **own full delivery, independently**: its own
draft PR (Phase 1 for `ose-public`; Phase 3 for the siblings), its own `pr-review-maker` →
`pr-review-fixer` **3 sequential CI-gated review cycles**, its own confirmation that ALL quality
gates are green (local `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` + CI),
and only THEN its own `[HUMAN]` merge (Phase 4). **Three peer PRs, each independently reviewed (3
cycles), gated, and merged — never a single PR with side-propagation.** The `libs/web-ui`
`// prettier-ignore` hack removal (Phase 2) is `ose-public`-only and sits outside this tri-repo rule
(`libs/web-ui` is outside the byte-identity boundary). Knowledge Capture and the plan-folder
archival-in-PR (Phase 5 + Plan Archival) happen ONLY in the `ose-public` PR, since this plan's folder
lives in `ose-public` alone.

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Plan already promoted from backlog to in-progress (date prefix stripped) during planning
      — acceptance: folder exists at `plans/in-progress/rhino-speccoverage-multiline-scenario-scan/`
- [ ] [AI] Provision/enter the worktree per the `## Worktree` section above
      — acceptance: shell cwd is `worktrees/rhino-speccoverage-multiline-scenario-scan/`
- [ ] [AI] Install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized
- [ ] [AI] Converge the polyglot toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift (Rust toolchain + cargo present)
- [ ] [AI] Record the rhino-cli baseline:
      `npx nx run rhino-cli:test:unit && npx nx run rhino-cli:specs:behavior:coverage`
      — acceptance: baseline pass/fail recorded in `learnings.md`; preexisting failures documented
- [ ] [AI] Record the web-ui baseline: `npx nx run web-ui:specs:behavior:coverage`
      — acceptance: baseline pass/fail recorded (expected: passes because the hacks are still present)
- [ ] [AI] Resolve any preexisting failures before proceeding
      — acceptance: no unresolved preexisting failures remain

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift
- [ ] [AI] `npx nx run rhino-cli:test:unit` baseline recorded (green) and any preexisting failure resolved
- [ ] [AI] `npx nx run rhino-cli:specs:behavior:coverage` baseline recorded (green)

> **Pause Safety**: only the toolchain was verified and the baseline recorded — no feature work
> exists yet. Safe to stop indefinitely. To resume: re-run
> `npx nx run rhino-cli:test:unit && npx nx run rhino-cli:specs:behavior:coverage` and confirm green.

---

## Phase 1: rhino-cli scanner fix + companion Gherkin

> _Suggested executor: `swe-rust-dev`_
>
> TDD cycle — RED substeps reproduce the cross-line miss at both the behavior and unit level, GREEN
> applies the whole-content scan, REFACTOR tidies. Each substep is its own checkbox.

### 1a. Behavior-level reproducer (cucumber-rs binder)

- [ ] [AI] **RED** — Add the AC-4 scenario to
      `specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature`
      and its cucumber step definitions to `apps/rhino-cli/tests/spec_coverage.rs`. The step def
      builds a fixture whose covering test contains a `Scenario(` token with its title on the NEXT
      physical line, then drives `rhino-cli specs behavior-coverage validate` and asserts success.
      **Gherkin (binds) →** "A scenario whose title wraps onto a following physical line is still
      recognized as covered"
      — command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test spec_coverage`
      — acceptance: the new test FAILS (the wrapped-title scenario is reported as an unimplemented
      gap by the current per-line scanner):

  ```gherkin
  Scenario: A scenario whose title wraps onto a following physical line is still recognized as covered
    Given a feature file whose scenario is bound by a test whose Scenario(...) title wraps onto the next physical line
    When the developer runs behavior-coverage validate on the specs and app directories
    Then the command exits successfully
    And the output does not report the wrapped-title scenario as an unimplemented scenario
  ```

### 1b. Unit-level reproducers (pure-core fixtures)

- [ ] [AI] **RED** — Add a unit fixture in the `#[cfg(test)]` module of
      `apps/rhino-cli/src/application/speccoverage/checker.rs` (alongside
      `extract_ts_scenario_titles_picks_up_double_quoted_title` at ~line 1153) named
      `extract_ts_scenario_titles_picks_up_cross_line_double_quoted_title`, writing a file whose
      content is `Scenario(\n  \"Wrapped double title\",\n  () => {});\n` and asserting the title set
      contains `Wrapped double title`.
      **Gherkin (underpins) →** AC-1.
      — command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib extract_ts_scenario_titles_picks_up_cross_line_double_quoted_title`
      — acceptance: the new test FAILS (title missing under per-line scan)
- [ ] [AI] **RED** — Add a unit fixture
      `extract_ts_scenario_titles_picks_up_cross_line_single_quoted_title` writing
      `Scenario(\n  'Wrapped single title',\n  () => {});\n` and asserting the set contains
      `Wrapped single title`.
      **Gherkin (underpins) →** AC-2.
      — command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib extract_ts_scenario_titles_picks_up_cross_line_single_quoted_title`
      — acceptance: the new test FAILS
- [ ] [AI] **GUARD** (characterization, not RED) — Add an explicit same-line guard fixture
      `extract_ts_scenario_titles_preserves_same_line_titles` asserting both a double- and
      single-quoted same-line title are still returned. This locks the pre-change behavior so the
      GREEN whole-content rewrite cannot silently regress it; it PASSES on current code by design.
      **Gherkin (underpins) →** AC-3.
      — command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib extract_ts_scenario_titles_preserves_same_line_titles`
      — acceptance: the guard test PASSES against the current code, and MUST still pass after the GREEN step

### 1c. Implementation

- [ ] [AI] **GREEN** — Rewrite `extract_ts_scenario_titles` (`checker.rs:613-625`) to scan the whole
      file: replace `for line in content.lines() { for caps in scenario_def_re().captures_iter(line)`
      with a single `for caps in scenario_def_re().captures_iter(&content)` loop (keep the
      `dq`/`sq`/`unescape_string`/`normalize_ws` body unchanged).
      — command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib extract_ts_scenario_titles`
      — acceptance: all `extract_ts_scenario_titles*` unit tests PASS (cross-line + same-line)
- [ ] [AI] **GREEN** — Re-run the behavior binder:
      `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test spec_coverage`
      — acceptance: the AC-4 test PASSES (no false gap for the wrapped binding)

### 1d. Refactor + spec housekeeping

- [ ] [AI] **REFACTOR** — Optionally add a `(?s)` flag to `scenario_def_re()` (`checker.rs:31`) for
      symmetry with `step_def_re()`, with an inline comment noting it is functionally inert for this
      pattern (no `.` metacharacter); update the function doc comment to state the scan is
      whole-content.
      — command: `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib`
      — acceptance: all lib tests still PASS; `npx nx run rhino-cli:lint` exits 0 (clippy clean)
- [ ] [AI] Update the scenario-count table row for `spec-coverage-validate.feature` in the
      **top-level** `specs/apps/rhino/behavior/rhino-cli/gherkin/README.md` (row ~line 94; the table
      lives ONLY in this top-level README — `.../spec-coverage/README.md` is a plain bullet list with
      no count table and must NOT be edited for this). The row currently shows `6`, but the file
      already contains 9 scenarios before this plan's AC-4 addition — a preexisting under-count; this
      single edit reconciles both the preexisting 6-vs-9 drift and the +1 from the new AC-4 scenario.
      — command: `grep -c "^  Scenario:" specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature`
      — acceptance: the `gherkin/README.md` row count equals the grep count (expected: 10 after AC-4 is added)

### Specs & Gherkin Delivery (gate)

- [ ] [AI] Run the behavior-coverage gate:
      `npx nx run rhino-cli:specs:behavior:coverage`
      — acceptance: exits 0; the new AC-4 scenario is reported covered
- [ ] [AI] Run cardinality + structure validators on the edited feature file:
      `npx nx run rhino-cli:specs:gherkin-cardinality-validation && npx nx run rhino-cli:specs:structure-validation`
      — acceptance: both exit 0

### Local Quality Gates (Before Push) — Phase 1

- [ ] [AI] `npx nx affected -t typecheck` — exits 0
- [ ] [AI] `npx nx affected -t lint` — exits 0
- [ ] [AI] `npx nx affected -t test:quick` — exits 0
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` — exits 0
- [ ] [AI] `npx nx run rhino-cli:test:integration` — exits 0 (runs the cucumber `spec_coverage` binder)

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the Root Cause Orientation principle — proactively fix preexisting errors encountered
> during work. Commit preexisting fixes separately with appropriate conventional commit messages.

### Commit Guidelines — Phase 1

- [ ] [AI] Commit thematically, Conventional Commits format, split by concern:
      `fix(rhino-cli): scan whole file content for TS scenario titles` (source + unit fixtures);
      `test(rhino-cli): add cross-line scenario-coverage behavior scenario` (feature + binder);
      `docs(specs): update spec-coverage scenario count` (README table)
- [ ] [AI] Commit and push to origin `rhino-speccoverage-multiline-scenario-scan` (the PR branch)
- [ ] [AI] Create the ose-public draft PR (skip if a PR for this branch already exists):
      `gh pr create --draft --title "fix(rhino-cli): scan whole file content for TS scenario titles" --body "Fixes the speccoverage multi-line Scenario(...) title scan (see plans/in-progress/rhino-speccoverage-multiline-scenario-scan/ for full context)." --base main --head rhino-speccoverage-multiline-scenario-scan`
      — acceptance: `gh pr view --json state` shows OPEN

### Post-Push CI Verification — Phase 1

- [ ] [AI] Monitor GitHub Actions workflows triggered by the push: poll
      `gh run view --json status,conclusion` every ~2 min per the
      [CI monitoring convention](../../../repo-governance/development/workflow/ci-monitoring.md) —
      no tight-loop, never `gh run watch`
- [ ] [AI] Verify ALL CI checks pass; if any fails, fix at root cause and push a follow-up commit
- [ ] [AI] Do NOT proceed to Phase 2 until CI is fully green

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] `cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib extract_ts_scenario_titles` — all pass
- [ ] [AI] `cargo test --manifest-path apps/rhino-cli/Cargo.toml --test spec_coverage` — AC-4 passes
- [ ] [AI] `npx nx run rhino-cli:specs:behavior:coverage` — exits 0
- [ ] [AI] CI is green on the pushed commit

> **Pause Safety**: the scanner is fixed and fully covered; the web-ui hacks are untouched and still
> valid. The repo compiles and all gates pass. Safe to stop. To resume:
> `npx nx run rhino-cli:test:quick`.

---

## Phase 2: web-ui prettier-ignore hack removal (ose-public only)

> _Suggested executor: `swe-typescript-dev`_

- [ ] [AI] Remove the `// prettier-ignore` comment above the two wrapped `Scenario(` calls in
      `libs/web-ui/src/primitives/code-block/code-block.steps.tsx` (comments at lines 155 and 190),
      then run Prettier so it re-wraps the calls naturally:
      `npx prettier --write libs/web-ui/src/primitives/code-block/code-block.steps.tsx`
      — acceptance: `grep -n "prettier-ignore" libs/web-ui/src/primitives/code-block/code-block.steps.tsx` returns no matches
- [ ] [AI] Remove the `// prettier-ignore` comment above the wrapped `Scenario(` call in
      `libs/web-ui/src/primitives/code-block/copy-button.steps.tsx` (comment at line 45), then run
      `npx prettier --write libs/web-ui/src/primitives/code-block/copy-button.steps.tsx`
      — acceptance: `grep -n "prettier-ignore" libs/web-ui/src/primitives/code-block/copy-button.steps.tsx` returns no matches
- [ ] [AI] Verify the web-ui spec-coverage gate stays green now that titles are re-wrapped:
      `npx nx run web-ui:specs:behavior:coverage`
      — acceptance: exits 0 with zero scenario gaps (AC-5)
- [ ] [AI] Verify the web-ui unit tests still pass (step files still execute):
      `npx nx run web-ui:test:unit`
      — acceptance: exits 0

### Local Quality Gates (Before Push) — Phase 2

- [ ] [AI] `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` — all exit 0
- [ ] [AI] Fix ALL failures found, including preexisting ones (Root Cause Orientation)

### Commit Guidelines — Phase 2

- [ ] [AI] Commit: `chore(web-ui): drop prettier-ignore hacks now that speccoverage scans whole file`
- [ ] [AI] Commit and push to origin `rhino-speccoverage-multiline-scenario-scan` (the PR branch)

### Post-Push CI Verification — Phase 2

- [ ] [AI] Monitor GitHub Actions: poll `gh run view --json status,conclusion` every ~2 min per the
      [CI monitoring convention](../../../repo-governance/development/workflow/ci-monitoring.md) —
      no tight-loop, never `gh run watch`; verify ALL checks pass; fix at root cause and re-push on
      failure
- [ ] [AI] Do NOT proceed to Phase 3 until CI is fully green

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `grep -rn "prettier-ignore" libs/web-ui/src/primitives/code-block/` — no matches
- [ ] [AI] `npx nx run web-ui:specs:behavior:coverage` — exits 0
- [ ] [AI] CI is green on the pushed commit

> **Pause Safety**: ose-public carries the full fix and the hacks are gone; coverage is green. The
> sibling repos still carry the old scanner but are internally consistent (byte-identity is
> temporarily diverged but each repo independently passes its own gates). Safe to stop. To resume:
> re-verify `npx nx run web-ui:specs:behavior:coverage` and proceed to parity.

---

## Phase 3: byte-identical rhino-cli parity to ose-primer + ose-infra

> _Executor: direct byte-identical propagation. No cross-repo design deviation exists here — the
> change is a single verbatim diff — so the
> [multi-repo parity **planning** workflow](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)
> (which authors one full plan-per-repo via a grilled deviation matrix) does not apply; that
> workflow's output is a plan document, not an execution mechanism. The heavier
> [plan-multi-repo-parity-planning-and-execution workflow](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning-and-execution.md)
> — which composes planning AND execution across repos behind its own three-grill contract — is
> likewise the wrong tool here: it exists for cross-repo objectives that need per-repo
> deviation-matrix grilling and independent plan authoring, not for propagating a single
> already-decided verbatim diff. This phase instead applies the identical `checker.rs` / feature /
> README / test changes directly and lands each sibling repo's change via its own PR — reviewed,
> gated, and merged independently in Phase 4 — per the Sibling Delivery Mode below._
>
> The byte-identity boundary covers `apps/rhino-cli/src/…/checker.rs`, the
> `spec-coverage-validate.feature` scenario, its scenario-count row in the top-level
> `gherkin/README.md` table, and (for crate coherence) the `tests/spec_coverage.rs` binder — see
> `tech-docs.md §4`. The `libs/web-ui` change from Phase 2 is NOT propagated (ose-public-only).
>
> **Sibling Delivery Mode**: `worktree-to-pr` for both `ose-primer` and `ose-infra` — each sibling
> repo provisions its own worktree at `worktrees/rhino-speccoverage-multiline-scenario-scan/` (the
> same [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
> applied within that sibling's own checkout), commits the byte-identical change on a
> same-named branch, pushes, and opens its own draft PR against its `main`. This phase (3a/3b) only
> gets the draft PR open; each sibling's own 3-cycle review, quality gates, and `[HUMAN]` merge run
> in Phase 4 below, independently and on its own schedule — separate from the ose-public PR, whose
> merge is deferred past Phase 5 (Knowledge Capture + archival-in-PR).

### 3a. ose-primer propagation

- [ ] [AI] Provision the ose-primer worktree:
      `git -C /Users/wkf/ose-projects/ose-primer worktree add worktrees/rhino-speccoverage-multiline-scenario-scan -b rhino-speccoverage-multiline-scenario-scan origin/main`
      — acceptance: directory exists at
      `/Users/wkf/ose-projects/ose-primer/worktrees/rhino-speccoverage-multiline-scenario-scan/`
- [ ] [AI] Copy the byte-identical files into the ose-primer worktree, then run the sibling tests
      — acceptance: both `cargo test` commands exit 0:

  ```bash
  OSE_PRIMER_WT=/Users/wkf/ose-projects/ose-primer/worktrees/rhino-speccoverage-multiline-scenario-scan
  cp /Users/wkf/ose-projects/ose-public/apps/rhino-cli/src/application/speccoverage/checker.rs \
     "$OSE_PRIMER_WT/apps/rhino-cli/src/application/speccoverage/checker.rs"
  cp /Users/wkf/ose-projects/ose-public/specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature \
     "$OSE_PRIMER_WT/specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature"
  cp /Users/wkf/ose-projects/ose-public/specs/apps/rhino/behavior/rhino-cli/gherkin/README.md \
     "$OSE_PRIMER_WT/specs/apps/rhino/behavior/rhino-cli/gherkin/README.md"
  cp /Users/wkf/ose-projects/ose-public/apps/rhino-cli/tests/spec_coverage.rs \
     "$OSE_PRIMER_WT/apps/rhino-cli/tests/spec_coverage.rs"
  cd "$OSE_PRIMER_WT" && cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib extract_ts_scenario_titles && cargo test --manifest-path apps/rhino-cli/Cargo.toml --test spec_coverage
  ```

- [ ] [AI] Verify byte-identity of `checker.rs` between ose-public and the ose-primer worktree:
      `diff /Users/wkf/ose-projects/ose-public/apps/rhino-cli/src/application/speccoverage/checker.rs /Users/wkf/ose-projects/ose-primer/worktrees/rhino-speccoverage-multiline-scenario-scan/apps/rhino-cli/src/application/speccoverage/checker.rs`
      — acceptance: no diff output (byte-identical)
- [ ] [AI] Verify byte-identity of the behavior feature file between ose-public and ose-primer:
      `diff /Users/wkf/ose-projects/ose-public/specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature /Users/wkf/ose-projects/ose-primer/worktrees/rhino-speccoverage-multiline-scenario-scan/specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature`
      — acceptance: no diff output (AC-6)
- [ ] [AI] Run the ose-primer parity gate:
      `cd /Users/wkf/ose-projects/ose-primer/worktrees/rhino-speccoverage-multiline-scenario-scan && npx nx run rhino-cli:specs:behavior:coverage`
      — acceptance: exits 0
- [ ] [AI] Commit, push, and open the ose-primer draft PR
      — acceptance: `gh pr view --json state` (run from that worktree) shows OPEN:

  ```bash
  cd /Users/wkf/ose-projects/ose-primer/worktrees/rhino-speccoverage-multiline-scenario-scan
  git add apps/rhino-cli/src/application/speccoverage/checker.rs \
          specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature \
          specs/apps/rhino/behavior/rhino-cli/gherkin/README.md \
          apps/rhino-cli/tests/spec_coverage.rs
  git commit -m "fix(rhino-cli): scan whole file content for TS scenario titles"
  git push -u origin rhino-speccoverage-multiline-scenario-scan
  gh pr create --draft --title "fix(rhino-cli): scan whole file content for TS scenario titles" \
    --body "Byte-identical parity port from the ose-public fix." \
    --base main --head rhino-speccoverage-multiline-scenario-scan
  ```

### 3b. ose-infra propagation

- [ ] [AI] Provision the ose-infra worktree:
      `git -C /Users/wkf/ose-projects/ose-infra worktree add worktrees/rhino-speccoverage-multiline-scenario-scan -b rhino-speccoverage-multiline-scenario-scan origin/main`
      — acceptance: directory exists at
      `/Users/wkf/ose-projects/ose-infra/worktrees/rhino-speccoverage-multiline-scenario-scan/`
- [ ] [AI] Copy the byte-identical files into the ose-infra worktree, then run the sibling tests
      — acceptance: both `cargo test` commands exit 0:

  ```bash
  OSE_INFRA_WT=/Users/wkf/ose-projects/ose-infra/worktrees/rhino-speccoverage-multiline-scenario-scan
  cp /Users/wkf/ose-projects/ose-public/apps/rhino-cli/src/application/speccoverage/checker.rs \
     "$OSE_INFRA_WT/apps/rhino-cli/src/application/speccoverage/checker.rs"
  cp /Users/wkf/ose-projects/ose-public/specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature \
     "$OSE_INFRA_WT/specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature"
  cp /Users/wkf/ose-projects/ose-public/specs/apps/rhino/behavior/rhino-cli/gherkin/README.md \
     "$OSE_INFRA_WT/specs/apps/rhino/behavior/rhino-cli/gherkin/README.md"
  cp /Users/wkf/ose-projects/ose-public/apps/rhino-cli/tests/spec_coverage.rs \
     "$OSE_INFRA_WT/apps/rhino-cli/tests/spec_coverage.rs"
  cd "$OSE_INFRA_WT" && cargo test --manifest-path apps/rhino-cli/Cargo.toml --lib extract_ts_scenario_titles && cargo test --manifest-path apps/rhino-cli/Cargo.toml --test spec_coverage
  ```

- [ ] [AI] Verify byte-identity of `checker.rs` between ose-public and the ose-infra worktree:
      `diff /Users/wkf/ose-projects/ose-public/apps/rhino-cli/src/application/speccoverage/checker.rs /Users/wkf/ose-projects/ose-infra/worktrees/rhino-speccoverage-multiline-scenario-scan/apps/rhino-cli/src/application/speccoverage/checker.rs`
      — acceptance: no diff output (byte-identical)
- [ ] [AI] Verify byte-identity of the behavior feature file between ose-public and ose-infra:
      `diff /Users/wkf/ose-projects/ose-public/specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature /Users/wkf/ose-projects/ose-infra/worktrees/rhino-speccoverage-multiline-scenario-scan/specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature`
      — acceptance: no diff output (AC-6)
- [ ] [AI] Run the ose-infra parity gate:
      `cd /Users/wkf/ose-projects/ose-infra/worktrees/rhino-speccoverage-multiline-scenario-scan && npx nx run rhino-cli:specs:behavior:coverage`
      — acceptance: exits 0
- [ ] [AI] Commit, push, and open the ose-infra draft PR
      — acceptance: `gh pr view --json state` (run from that worktree) shows OPEN:

  ```bash
  cd /Users/wkf/ose-projects/ose-infra/worktrees/rhino-speccoverage-multiline-scenario-scan
  git add apps/rhino-cli/src/application/speccoverage/checker.rs \
          specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature \
          specs/apps/rhino/behavior/rhino-cli/gherkin/README.md \
          apps/rhino-cli/tests/spec_coverage.rs
  git commit -m "fix(rhino-cli): scan whole file content for TS scenario titles"
  git push -u origin rhino-speccoverage-multiline-scenario-scan
  gh pr create --draft --title "fix(rhino-cli): scan whole file content for TS scenario titles" \
    --body "Byte-identical parity port from the ose-public fix." \
    --base main --head rhino-speccoverage-multiline-scenario-scan
  ```

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] `checker.rs` and `spec-coverage-validate.feature` are byte-identical across all three repos (diffs empty)
- [ ] [AI] `npx nx run rhino-cli:specs:behavior:coverage` exits 0 in ose-public, ose-primer, ose-infra
- [ ] [AI] Each sibling repo's rhino-cli change is committed, pushed, and its own draft PR is OPEN
      (`gh pr view --json state` shows OPEN when run from each sibling's worktree)

> **Pause Safety**: all three repos carry the byte-identical fixed scanner, pass their coverage
> gates, and each sibling has its own open draft PR. Safe to stop. To resume: re-run the three-way
> `diff` on `checker.rs` and confirm empty, and re-check both sibling PRs' state.

---

## Phase 4: Multi-Repo PR-Review Cycles, Quality Gates & Merge

> _Executors: `pr-review-maker` → `pr-review-fixer`, per the
> [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md).
> Per the [Multi-Repo rhino-cli Delivery](#multi-repo-rhino-cli-delivery) rule above, all three legs
> below run the identical shape — default 3 strictly-sequential CI-gated review cycles, then a
> confirmed-green quality-gate check, then `[HUMAN]` merge. The only asymmetry: `ose-public`'s merge
> is deferred past Phase 5 (Knowledge Capture + archival-in-PR, `ose-public`-only), while
> `ose-primer` and `ose-infra` merge as soon as their own leg is green, since neither carries this
> plan's folder._

### 4a. ose-public — PR-Review Cycle (merge deferred to Plan Archival)

- [ ] [AI] Verify the draft PR created in Phase 1's Commit Guidelines step is OPEN with CI green
      (branch `rhino-speccoverage-multiline-scenario-scan`)
      — acceptance: `gh pr view --json state,statusCheckRollup` shows OPEN + all checks green
- [ ] [AI] Cycle 1 — `pr-review-maker` reviews via the GitHub Reviews API; `pr-review-fixer`
      addresses every finding and pushes to the PR branch; wait for CI green
      — acceptance: all cycle-1 findings resolved; CI green
- [ ] [AI] Cycle 2 — repeat maker→fixer; wait for CI green
      — acceptance: all cycle-2 findings resolved; CI green
- [ ] [AI] Cycle 3 — repeat maker→fixer; wait for CI green
      — acceptance: all cycle-3 findings resolved; CI green; no new findings outstanding
- [ ] [AI] Confirm ALL quality gates green on the ose-public PR:
      `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` (run from the
      ose-public worktree) then `gh pr checks rhino-speccoverage-multiline-scenario-scan`
      — acceptance: the local command exits 0; `gh pr checks` reports every check passing
- [ ] [AI] Do NOT merge yet — the `ose-public` `[HUMAN]` merge happens in Plan Archival, after Phase
      5 (Knowledge Capture) and archival-in-PR are committed to this PR branch

### 4b. ose-primer — PR-Review Cycle, Quality Gates & Merge

- [ ] [AI] Verify the draft PR opened in Phase 3a is OPEN with CI green (branch
      `rhino-speccoverage-multiline-scenario-scan`, run from the ose-primer worktree)
      — acceptance: `gh pr view --json state,statusCheckRollup` shows OPEN + all checks green
- [ ] [AI] Cycle 1 — `pr-review-maker` reviews the ose-primer PR via the GitHub Reviews API;
      `pr-review-fixer` addresses every finding and pushes to the PR branch; wait for CI green
      — acceptance: all cycle-1 findings resolved; CI green
- [ ] [AI] Cycle 2 — repeat maker→fixer; wait for CI green
      — acceptance: all cycle-2 findings resolved; CI green
- [ ] [AI] Cycle 3 — repeat maker→fixer; wait for CI green
      — acceptance: all cycle-3 findings resolved; CI green; no new findings outstanding
- [ ] [AI] Confirm ALL quality gates green on the ose-primer PR
      — acceptance: `npx nx affected` exits 0 and `gh pr checks` reports every check passing:

  ```bash
  cd /Users/wkf/ose-projects/ose-primer/worktrees/rhino-speccoverage-multiline-scenario-scan
  npx nx affected -t typecheck lint test:quick specs:behavior:coverage
  gh pr checks rhino-speccoverage-multiline-scenario-scan
  ```

- [ ] [HUMAN] Merge the ose-primer PR to `main` now that its review cycle is complete and all
      quality gates pass — acceptance: `gh pr view --json state` (run from the ose-primer worktree)
      shows MERGED

### 4c. ose-infra — PR-Review Cycle, Quality Gates & Merge

- [ ] [AI] Verify the draft PR opened in Phase 3b is OPEN with CI green (branch
      `rhino-speccoverage-multiline-scenario-scan`, run from the ose-infra worktree)
      — acceptance: `gh pr view --json state,statusCheckRollup` shows OPEN + all checks green
- [ ] [AI] Cycle 1 — `pr-review-maker` reviews the ose-infra PR via the GitHub Reviews API;
      `pr-review-fixer` addresses every finding and pushes to the PR branch; wait for CI green
      — acceptance: all cycle-1 findings resolved; CI green
- [ ] [AI] Cycle 2 — repeat maker→fixer; wait for CI green
      — acceptance: all cycle-2 findings resolved; CI green
- [ ] [AI] Cycle 3 — repeat maker→fixer; wait for CI green
      — acceptance: all cycle-3 findings resolved; CI green; no new findings outstanding
- [ ] [AI] Confirm ALL quality gates green on the ose-infra PR
      — acceptance: `npx nx affected` exits 0 and `gh pr checks` reports every check passing:

  ```bash
  cd /Users/wkf/ose-projects/ose-infra/worktrees/rhino-speccoverage-multiline-scenario-scan
  npx nx affected -t typecheck lint test:quick specs:behavior:coverage
  gh pr checks rhino-speccoverage-multiline-scenario-scan
  ```

- [ ] [HUMAN] Merge the ose-infra PR to `main` now that its review cycle is complete and all quality
      gates pass — acceptance: `gh pr view --json state` (run from the ose-infra worktree) shows
      MERGED

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] `ose-public`: three maker→fixer cycles completed, each CI-gated; quality gates confirmed
      green; PR remains OPEN (merge deferred) with no unresolved review findings
- [ ] [AI] `ose-primer`: three maker→fixer cycles completed, quality gates confirmed green, PR shows
      MERGED
- [ ] [AI] `ose-infra`: three maker→fixer cycles completed, quality gates confirmed green, PR shows
      MERGED

> **Pause Safety**: `ose-primer` and `ose-infra` are fully delivered and merged; `ose-public`'s PR is
> green and fully reviewed, awaiting Knowledge Capture + archival before its own merge. Safe to
> stop. To resume: `gh pr view` (per repo, from that repo's worktree) to confirm state before
> continuing.

---

## Phase 5: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason
      — acceptance: every entry has either a route or a discard reason
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable
      — acceptance: `learnings.md` contains no raw secret
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content stays in `ose-infra` only and is
      never cross-routed into `ose-public`/`ose-primer`; public-governance content may propagate via
      the parity loop
      — acceptance: no infra-private content appears in this repo's routed output
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing
      matrix — non-code homes may land inline (small edit) or as a `plans/backlog/` follow-up (large);
      code homes (`apps/`, `libs/`, tests) are ALWAYS filed as a separate `plans/backlog/<slug>/`
      plan and NEVER landed inline
      — acceptance: every `learnings.md` entry records its terminal routing state
- [ ] [AI] If no generalizable learning surfaced, record the explicit escape in `learnings.md`:
      `No generalizable learnings — <one-line reason>`
      — acceptance: `learnings.md` is never silently empty

### Phase 5 Gate

> All checks below must pass before Plan Archival.

- [ ] [AI] Every `learnings.md` entry is in a terminal state (routed inline, filed as backlog, or
      discarded with reason), or the file records the explicit "none" escape
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR

> **Pause Safety**: `learnings.md` is fully triaged (or explicitly recorded as empty); no future
> process depends on querying it later. Safe to stop. To resume: re-read `learnings.md` and confirm
> every entry is terminal.

---

## Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked
- [ ] [AI] Verify the Knowledge Capture phase is complete — every `learnings.md` entry reached a
      terminal state or the file records the explicit `No generalizable learnings — <reason>` escape;
      both safety gates applied to every surviving entry
- [ ] [AI] Verify ALL quality gates pass (local + CI) across ose-public, ose-primer, ose-infra
- [ ] [AI] Verify the `ose-primer` and `ose-infra` PRs already show MERGED (completed in Phase 4):
      `gh pr view --json state --jq .state` run from each sibling's worktree — acceptance: prints
      `MERGED` for both
- [ ] [AI] Verify `checker.rs` and `spec-coverage-validate.feature` are byte-identical across the three repos
- [ ] [AI] Move and rename: `git mv plans/in-progress/rhino-speccoverage-multiline-scenario-scan plans/done/YYYY-MM-DD__rhino-speccoverage-multiline-scenario-scan` using today's date as the completion date
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date
- [ ] [AI] Update any other READMEs that reference this plan (e.g., `plans/README.md`)
- [ ] [AI] Commit the archival: `chore(plans): move rhino-speccoverage-multiline-scenario-scan to done`
- [ ] [HUMAN] Merge the ose-public PR to `main` when ready — acceptance: PR shows MERGED (this sits
      outside the plan's done-boundary; the plan is "done" once the PR is green and fully reviewed)
