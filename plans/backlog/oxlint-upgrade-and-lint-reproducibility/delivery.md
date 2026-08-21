# Delivery Checklist — oxlint Upgrade and Lint-Toolchain Reproducibility

**Delivery Mode**: `worktree-to-pr`. Phase 0 opens no PR; the earliest PR is Phase 1.

**Repositories**: `ose-public` and `ose-private`. WS-O2 and WS-O3 must land in both or they diverge.

---

## Phase 0 — Baseline

- [ ] [AI] Confirm the current pin in both repos by command, not by memory —
      `python3 -c "import json;print(json.load(open('package.json'))['devDependencies']['oxlint'])"`.
      Acceptance: both print the same version.
- [ ] [AI] Record the current latest published oxlint via `npm view oxlint version`, with the publish
      timestamp from `npm view oxlint time --json`. Acceptance: both figures written to the plan.
- [ ] [AI] Re-run the Three-Path classification in `tech-docs.md` §5 against the execution date's
      60-day cutoff (`npm view oxlint time --json`). Acceptance: the eligible Path B version (or a
      documented Path C waiver) is written to `tech-docs.md`, replacing the authoring-time snapshot.
- [ ] [AI] Run every affected lint target on the current pin and record exit codes. Acceptance: a
      baseline table exists; any already-failing target is resolved before Phase 1 begins.
- [ ] [AI] Confirm `apps/ose-www/src/features/search/shell/search-dialog.tsx` still contains the
      synchronous `setResults([])` guard. Acceptance: if it does not, this plan is already obsolete —
      stop and re-specify.

## Phase 1 — WS-O1: fix the violation (delivery boundary)

- [ ] [AI] RED: write the AC-1 unit test asserting a one-character query renders no results.
      Acceptance: the test **fails** against current `main`. A passing test here is a defective test.
- [ ] [AI] RED: write the AC-1 test asserting a cleared query drops previously-fetched results.
      Acceptance: fails before the fix.
- [ ] [AI] Write the companion Gherkin at `specs/apps/ose-www/` per Feature Change Completeness.
      Acceptance: `rhino-cli` spec-coverage gate exits 0.
- [ ] [AI] GREEN: derive `visibleResults` during render and remove the synchronous `setResults([])`
      guard from the effect. Acceptance: both new tests pass; `npx nx run ose-www:test:quick` exits 0.
- [ ] [AI] Verify against the NEW oxlint, not the pin — run the current published oxlint against
      `apps/ose-www`. Acceptance: `react(set-state-in-effect)` no longer fires on this file.
- [ ] [AI] Confirm no behaviour regression in the three viewports — mobile, tablet, desktop — for the
      search dialog. Acceptance: each viewport named explicitly with its result.
- [ ] [AI] Open the PR and run the review cycle. Acceptance: `pr-quality-gate.yml` green.

### Phase 1 Gates

- [ ] [AI] G1: `npx nx run ose-www:lint` and `ose-www:test:quick` both exit 0.
- [ ] [AI] G2: the two new tests fail on the pre-fix commit and pass on the post-fix commit —
      demonstrated by checking out each and running them, not asserted.

## Phase 2 — WS-O2: take the upgrade (delivery boundary)

- [ ] [AI] Run the current published oxlint against all 22 call sites **before** changing the pin.
      Acceptance: the complete finding list is recorded, per site, with counts.
- [ ] [AI] Triage each finding: fix, or disable in `oxlint.json` with a stated reason.
      Acceptance: the number of findings with no written disposition is zero.
- [ ] [AI] Clear the Phase 0 candidate version against NVD, GitHub Advisories, Snyk, oxlint's own
      security page, and CISA KEV per the
      [CVE Clearance Process](../../../repo-governance/development/workflow/dependency-bump-policy/cve-clearance-process.md);
      record the final `CLEAR`/`CLEAR (patch-of)`/`WAIVER`/`FUNCTIONAL-HOLD` status in the
      `tech-docs.md` Security Clearance Status table before the manifest edit. Acceptance: the
      `PENDING` placeholder is replaced with one of the four allowed statuses.
- [ ] [AI] Raise the pin in `ose-public`'s root `package.json`. Acceptance: `npm install` succeeds and
      `./node_modules/.bin/oxlint --version` prints the intended version.
- [ ] [AI] Raise the pin identically in `ose-private`. Acceptance: both repos print the same version.
- [ ] [AI] Run every affected lint target in both repos. Acceptance: all exit 0.
- [ ] [AI] Open both PRs and run the review cycle on each. Acceptance: both gates green.

### Phase 2 Gates

- [ ] [AI] G1: the two repositories' declared oxlint versions are byte-identical.
- [ ] [AI] G2: every lint target that exists in both repos exits 0 in both.

## Phase 3 — WS-O3: prevent the class (delivery boundary)

- [ ] [AI] Sweep `project.json`, `package.json`, `.github/workflows/`, and `.husky/` for run-time
      version resolution — `npx <pkg>@latest`, bare `npx` on undeclared packages, `curl | sh`
      installers, unpinned `uses:` action refs. Acceptance: a per-item table with a verdict each.
- [ ] [AI] Prove the sweep's detection rule is non-vacuous: reintroduce one unpinned invocation in a
      scratch copy and confirm the rule reports it. Acceptance: non-zero before, zero after removal.
      A zero from an unproven rule is not evidence.
- [ ] [AI] Decide the durable mechanism — governance convention plus validator, dependency-update
      automation, or both. Acceptance: the decision and its rejected alternatives are written down.
- [ ] [AI] If a `rhino-cli` validator is chosen: TDD cycle, companion Gherkin, and the parity manifest
      regenerated and staged **in the same commit**. Acceptance: parity-manifest gate exits 0 in all
      four repos.
- [ ] [AI] Apply the chosen mechanism in both repositories. Acceptance: identical in both.

### Phase 3 Gates

- [ ] [AI] G1: the count of unverdicted run-time-resolving invocations is zero in both repos.
- [ ] [AI] G2: if a validator was added, it fails against a deliberately unpinned fixture and passes
      against the real tree.

## Phase 4 — Close

- [ ] [AI] Knowledge Capture: record what the diagnosis cost and which signal identified the cause
      fastest (the npm publish timestamp versus the CI run timestamps).
- [ ] [AI] Triage every learnings entry through the routing rubric.
- [ ] [AI] Move the plan folder to `plans/done/<YYYY-MM-DD>__oxlint-upgrade-and-lint-reproducibility/`.
- [ ] [AI] Update `plans/README.md`, `plans/backlog/README.md`, and `plans/done/README.md`.
- [ ] [AI] Remove the plan worktrees and fast-forward both root checkouts.
