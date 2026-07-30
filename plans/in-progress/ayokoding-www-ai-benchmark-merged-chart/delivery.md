# Delivery — AI Benchmark Merged Chart

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase is
> not complete until its gate is green; do not start phase N+1 while any gate check fails.
>
> This plan uses no `[HUMAN]` steps — every step is `[AI]`. This legend is present per convention
> even though the `[HUMAN]` marker is unused.

## Worktree

Worktree path: `worktrees/ayokoding-www-ai-benchmark-merged-chart/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-www-ai-benchmark-merged-chart
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Work happens in the worktree above; a draft PR opens against `main` once Phase 1 has committed
work; the PR-Review Maker→Fixer Cycle (3 sequential CI-gated cycles) runs before merge; `[AI]`
merges once the hardened preconditions hold. See
[Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode).

## Parallelization Model

This plan is a single, tightly sequential feature change to one app (`apps/ayokoding-www`) — the
new pure `core/sort.ts` must exist before the merged chart component can consume it, and the merged
chart must exist before the old charts can be deleted and wired out. There is no independent DAG
fan-out to parallelize; the whole plan is one delivery unit, one worktree, one PR.

### Delivery Boundaries

| Delivery unit | Phases                                                        | Worktree / branch                                                                                        | PR opens at                                             |
| ------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Unit 1 (only) | Phases 1–9 (change-producing); Phase 9 is the boundary itself | `worktrees/ayokoding-www-ai-benchmark-merged-chart/` on branch `ayokoding-www-ai-benchmark-merged-chart` | Phase 1 (draft), reviewed at Phase 7, merged at Phase 9 |

Phase 6 (Manual UI Verification) is the last UI-facing change-producing phase (it commits
`evidence/` screenshots); Phase 7 (Push, PR Finalization, Review Cycle) runs the PR-Review
Maker→Fixer Cycle but does **not** merge; Phase 8 (Knowledge Capture) is a trailing, non-boundary
phase that commits to the SAME PR branch, opening no new PR; Phase 9 (Plan Archival, Final Push,
Merge) is the delivery boundary itself — its `git mv` archival commit lands on the PR branch and is
pushed BEFORE the merge, per the Delivery Mode convention's Archival-in-PR requirement, mirroring
`plans/done/2026-07-30__ayokoding-www-tools-ai-benchmark/delivery.md`'s Phase 11–12 pattern (commit
archival first, merge last).

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_
>
> **No PR for this phase.** Phase 0 is local setup and baseline only: it opens no PR, pushes no
> branch, runs no PR-Review Maker→Fixer Cycle, and merges nothing. The earliest phase that may open
> a PR is Phase 1.

- [x] [AI] Install dependencies in the root worktree: `npm install` — acceptance: exits 0,
      `node_modules/` synchronized
- [x] [AI] Converge the full polyglot toolchain in the root worktree: `npm run doctor -- --fix` —
      acceptance: exits 0 with no unresolved drift
  - **Date**: 2026-07-30. **Status**: Done (after one preexisting fix). **Files Changed**: none in
    repo; created `~/.cache/ose-cargo-target/ose-public/rhino-cli/` (machine-local cache dir a
    dangling `apps/rhino-cli/target` symlink pointed at). **Notes**: first run failed with
    `error: failed to create directory '.../apps/rhino-cli/target' — Not a directory (os error 20)`;
    root cause was the shared-cargo-target-cache symlink pointing at a missing directory. Fixed via
    `mkdir -p`, re-ran: `16/16 tools OK, 0 warning, 0 missing`.
- [x] [AI] Provision the worktree: `git worktree add worktrees/ayokoding-www-ai-benchmark-merged-chart -b ayokoding-www-ai-benchmark-merged-chart`
      from the repo root — acceptance: `worktrees/ayokoding-www-ai-benchmark-merged-chart/` exists
      and `git worktree list` shows it
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: none (git operation only). **Notes**:
    provisioned via `git fetch origin && git worktree add -b ayokoding-www-ai-benchmark-merged-chart
worktrees/ayokoding-www-ai-benchmark-merged-chart origin/main`; `git worktree list` confirms the
    path is registered on branch `ayokoding-www-ai-benchmark-merged-chart` at `f733654f5` (origin/main
    HEAD at provisioning time).
- [x] [AI] Inside the new worktree, initialize its toolchain: `npm install && npm run doctor -- --fix` —
      acceptance: both exit 0
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: none (dependency install only).
    **Notes**: `npm install` → exit 0, `added 1572 packages, and audited 1596 packages`.
    `npm run doctor -- --fix` → exit 0, `16/16 tools OK, 0 warning, 0 missing`; target-share fix
    created 4 cargo target-dir symlinks for the fresh worktree (expected, not a defect).
- [x] [AI] Run the existing `ai-benchmark` unit tests to establish baseline:
      `npx nx run ayokoding-www:test:unit -- ai-benchmark` — acceptance: baseline
      pass/fail count recorded; every preexisting failure documented
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: none. **Notes**: exit 0. Test Files:
    15 passed (15). Tests: 636 passed (636). Zero failed, zero skipped, zero preexisting failures.
- [x] [AI] Run `npx nx run ayokoding-www:test:specs` — acceptance: baseline coverage result
      recorded (the 39 existing `ai-benchmark.feature` scenarios currently pass)
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: none. **Notes**: exit 0. Whole-app
    `specs:coverage`: 42 specs, 333 scenarios, 1196 steps, all covered, 0 findings.
    `grep -c "^  Scenario" specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
    → `39`, matching the plan's stated existing-scenario count, all currently passing.
- [x] [AI] Resolve any preexisting failure found above before proceeding — acceptance: no
      preexisting failure remains unresolved
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: none in repo (machine-local cache
    dir only, see the doctor item above). **Notes**: the only preexisting failure found (root
    `npm run doctor -- --fix`'s dangling cargo-target-cache symlink) was root-cause-fixed and
    re-verified clean; typecheck/lint both exit 0 with only preexisting warning-level oxlint/jsx-a11y
    findings unrelated to ai-benchmark (not errors, out of scope).

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` and `npm run doctor -- --fix` both exited 0 in both the root and the new
      worktree, with no unresolved drift
  - **Date**: 2026-07-30. **Status**: Green. **Files Changed**: none. **Notes**: confirmed above.
- [x] [AI] `npx nx run ayokoding-www:test:unit`, `npx nx run ayokoding-www:typecheck`,
      `npx nx run ayokoding-www:lint`, and `npx nx run ayokoding-www:test:specs` baseline
      recorded and every preexisting failure resolved (zero unresolved)
  - **Date**: 2026-07-30. **Status**: Green. **Files Changed**: none. **Notes**: 636/636 unit tests
    pass, typecheck exit 0, lint exit 0 (warning-level only, preexisting, unrelated), specs 42/42
    covered.
- [x] [AI] Nothing was pushed and no PR exists for this branch — run both, reading the printed
      number: `git ls-remote --heads origin ayokoding-www-ai-benchmark-merged-chart | grep -c .`
      returns `0`, and `gh pr list --head ayokoding-www-ai-benchmark-merged-chart --json number --jq 'length'`
      returns `0`
  - **Date**: 2026-07-30. **Status**: Green. **Files Changed**: none. **Notes**: both commands
    confirmed `0` as expected — Phase 0 pushed nothing and opened no PR.

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no feature
> work exists yet, nothing is pushed, no PR exists. Safe to stop indefinitely. To resume: re-run the
> baseline commands and confirm they are still clean.

## Phase 1: Pure core — `core/sort.ts` and `core/url-state.ts` extension

> Work happens in `worktrees/ayokoding-www-ai-benchmark-merged-chart/`. This phase's commit is the
> first to ride a PR — open the PR (draft) at the end of this phase, per Delivery Boundaries above.

- [x] [AI] **RED**: write a failing test for `byCapabilityDesc` in
      `apps/ayokoding-www/src/features/ai-benchmark/core/sort.unit.test.ts` (new file) — asserts a
      three-model fixture array sorts descending by `index`, `undefined` last — command:
      `npx nx run ayokoding-www:test:unit -- sort.unit` — acceptance: fails with
      "byCapabilityDesc is not a function" (module does not exist yet)
  - **Gherkin (underpins) →** "Models are ordered identically before and after a sort change within a band" (pure-core data invariant; aggregate exception per the TDD convention)
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**:
    `apps/ayokoding-www/src/features/ai-benchmark/core/sort.unit.test.ts` (new). **Notes**: actual
    RED signal was `Error: Cannot find module './sort'` (module-resolution failure, since `sort.ts`
    didn't exist yet) rather than the plan's illustrative "is not a function" text — equivalent RED
    signal, correct failure mode. 1 test file failed, 0 tests ran.
- [x] [AI] **GREEN**: create `apps/ayokoding-www/src/features/ai-benchmark/core/sort.ts` (sibling
      to `bands.ts`, `price.ts`) implementing `byCapabilityDesc(a: ModelScore, b: ModelScore): number`
      mirroring `bands.ts`'s existing (private) `compareForOrder` descending-index logic — command:
      `npx nx run ayokoding-www:test:unit -- sort.unit` — acceptance: the new test
      passes, no other test broken
  - _Suggested executor: `swe-typescript-dev`_
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**:
    `apps/ayokoding-www/src/features/ai-benchmark/core/sort.ts` (new). **Notes**: `byCapabilityDesc`
    copied verbatim from `bands.ts`'s private `compareForOrder`. `npx nx run ayokoding-www:test:unit -- sort.unit` → `1 passed (1)`.
- [x] [AI] **RED**: write a failing test for `byPriceAsc`/`byPriceDesc` in `sort.unit.test.ts` — a
      fixture of models with distinct `output`/`input` rates from `lowestRate()`, asserting ascending
      then descending order by output rate, tie-broken by input rate — command:
      `npx nx run ayokoding-www:test:unit -- sort.unit` — acceptance: fails with
      "byPriceAsc is not a function"
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `sort.unit.test.ts` (4 tests added).
    **Notes**: actual RED signal was an assertion mismatch (e.g.
    `expected ['cheap','pricey','mid'] to deeply equal ['pricey','mid','cheap']`) rather than "is not
    a function", since `Array.sort(undefined)` silently falls back to default sort instead of
    throwing — equivalent RED signal, correct failure mode. Result: `1 failed | 4 passed (5 total)`.
- [x] [AI] **GREEN**: implement `byPriceAsc`/`byPriceDesc` in `sort.ts`, each taking a `ModelScore`
      pair and delegating to `core/price.ts`'s `lowestRate` to read the output rate (falling back to
      `Infinity`/`-Infinity` for a model with no metered rate, per DD-1/DD-2's rules) — command:
      `npx nx run ayokoding-www:test:unit -- sort.unit` — acceptance: both new tests
      pass
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `sort.ts` (implemented
    `byPriceAsc`/`byPriceDesc`, initially with duplicated bodies per strict TDD step separation).
    **Notes**: `npx nx run ayokoding-www:test:unit -- sort.unit` → `5 passed (5)`.
- [x] [AI] **REFACTOR**: extract the shared "read a model's output-then-input rate as a comparable
      number" helper used by both `byPriceAsc` and `byPriceDesc` in `sort.ts` — command:
      `npx nx run ayokoding-www:test:unit -- sort.unit` — acceptance: all sort tests
      still pass, no duplicated comparator body
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `sort.ts` (extracted
    `meteredRateOrFallback(s, fallback)` shared helper); `sort.unit.test.ts` (2 more unmetered-model
    fallback tests added). **Notes**: `npx nx run ayokoding-www:test:unit -- sort.unit` → `7 passed (7)`.
- [x] [AI] **RED**: write a failing test in
      `apps/ayokoding-www/src/features/ai-benchmark/core/url-state.unit.test.ts` (existing file)
      asserting `encodeState`/`decodeState` round-trip the four new sort params
      (`sortOpus`/`sortSonnet`/`sortLight`/`sortUnrated`) — command:
      `npx nx run ayokoding-www:test:unit -- url-state.unit` — acceptance: fails
      (params not yet recognized)
  - **Gherkin (binds) →** "A band's sort choice is encoded in the URL"

    ```gherkin
    Scenario: A band's sort choice is encoded in the URL
      Given the reader has selected "Price: High to Low" for the opus band
      When the reader copies the current page URL
      Then the URL contains a "sortOpus" query parameter set to the descending-price value
      And loading that URL directly reproduces the opus band sorted the same way
    ```

  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `url-state.unit.test.ts` (round-trip
    test added for all 4 bands). **Notes**: `npx nx run ayokoding-www:test:unit -- url-state.unit` →
    `1 failed | 65 passed (66 total)`, failure: `expected null to be 'price-asc'` (param not
    recognized).

- [x] [AI] **GREEN**: edit
      `apps/ayokoding-www/src/features/ai-benchmark/core/url-state.ts` — add
      `SORT_PARAM_KEYS` (`sortOpus`/`sortSonnet`/`sortLight`/`sortUnrated`), a `SortMode` union
      (`"capability" | "price-asc" | "price-desc"`), a `SortState` type (one `SortMode` per band,
      default `"capability"`), and extend `encodeState`/`decodeState`/`sanitizeState` to round-trip
      them, omitting the default from the query string exactly like `harness`/`class` already do —
      command: `npx nx run ayokoding-www:test:unit -- url-state.unit` — acceptance:
      new test passes, all 20+ existing `url-state.unit.test.ts` cases still pass
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `url-state.ts` (added
    `SORT_PARAM_KEYS`, `SortMode`, `SortState`, `DEFAULT_SORT_MODE`/`DEFAULT_SORT_STATE`, extended
    `sanitizeState`/`decodeState`/`encodeState`); `url-state.unit.test.ts` (3 existing `toEqual`
    assertions updated for the grown return shape — unavoidable, return shape genuinely grew).
    **Notes**: `encodeState`'s signature widened to accept `Partial<SortState>` so existing bare
    `{harness: "cursor"}` call sites don't emit `sortOpus=undefined` etc. `npx nx run
ayokoding-www:test:unit -- url-state.unit` → `67 passed (67)`, zero regressions.
- [x] [AI] **RED**: write a failing test in `url-state.unit.test.ts` asserting an unrecognized
      `sortSonnet` value in the URL sanitizes to `"capability"` (the default), never throwing —
      command: `npx nx run ayokoding-www:test:unit -- url-state.unit` — acceptance:
      fails (sanitizer does not exist yet for sort params)
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `url-state.unit.test.ts` (fallback
    test added). **Notes**: `npx nx run ayokoding-www:test:unit -- url-state.unit` →
    `1 failed | 66 passed (67 total)`, failure: `expected 'not-a-real-value' to be 'capability'`.
  - **Gherkin (binds) →** "An unknown sort value in the URL falls back to the default"

    ```gherkin
    Scenario: An unknown sort value in the URL falls back to the default
      Given a URL containing "sortSonnet=not-a-real-value"
      When the page loads with that URL
      Then the sonnet band renders sorted by capability (the default)
      And no error is thrown
    ```

- [x] [AI] **GREEN**: add an `isKnownSortMode` type guard to `core/sort.ts` (mirroring
      `filter.ts`'s `isKnownHarness`/`isKnownBand`) and wire it into `url-state.ts`'s
      `sanitizeState` for all four sort params — command:
      `npx nx run ayokoding-www:test:unit -- url-state.unit` — acceptance: new test
      passes
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `sort.ts` (added
    `SORT_MODES`/`isKnownSortMode`); `url-state.ts` (wired `sanitizeSortMode` using the guard).
    **Notes**: `npx nx run ayokoding-www:test:unit -- url-state.unit` → `67 passed (67)`.
- [x] [AI] Open a draft PR against `main` titled
      `feat(ayokoding-www): merge AI benchmark capability and price charts` — command:
      `gh pr create --draft --base main --head ayokoding-www-ai-benchmark-merged-chart --title "feat(ayokoding-www): merge AI benchmark capability and price charts" --body "Phase 1: core/sort.ts + url-state.ts sort params. See plans/in-progress/ayokoding-www-ai-benchmark-merged-chart/"` —
      acceptance: `gh pr list --head ayokoding-www-ai-benchmark-merged-chart --json number --jq 'length'`
      returns `1`
  - **Date**: 2026-07-30. **Status**: Done. **Notes**: PR #125 opened
    (https://github.com/wahidyankf/ose-public/pull/125); `gh pr list --head
ayokoding-www-ai-benchmark-merged-chart --json number --jq 'length'` → `1`.

### Phase 1 Gate

- [x] [AI] `npx nx run ayokoding-www:test:unit -- ai-benchmark` — all `sort.unit.test.ts`
      and `url-state.unit.test.ts` cases pass, zero regressions in the rest of the suite
- [x] [AI] `npx nx affected -t typecheck lint` — both exit 0
- [x] [AI] Draft PR exists: `gh pr list --head ayokoding-www-ai-benchmark-merged-chart --json number --jq 'length'`
      returns `1`

> **Evidence**: `npx nx run ayokoding-www:test:unit -- ai-benchmark` → `Test Files 16 passed (16)`,
> `Tests 645 passed (645)`. `npx nx affected -t typecheck lint` → both exit 0 (also re-confirmed by
> the pre-push hook during `git push origin ayokoding-www-ai-benchmark-merged-chart`).
> `gh pr list --head ayokoding-www-ai-benchmark-merged-chart --json number --jq 'length'` → `1`
> (PR #125).
>
> **Pause Safety**: `core/sort.ts` and the extended `core/url-state.ts` are complete, tested, and
> pushed; no UI yet consumes them, so the page still renders exactly as before this plan started.
> Safe to stop. To resume: `cd worktrees/ayokoding-www-ai-benchmark-merged-chart && npx nx run ayokoding-www:test:unit -- ai-benchmark`.

## Phase 2: Merged chart component — `shell/benchmark-chart.tsx`

> The new component is built alongside the two existing charts (not yet wired in or deleted), so the
> live page is unaffected until Phase 3.

- [x] [AI] **RED**: write a failing test in
      `apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.test.tsx` (new file)
      asserting a rendered rated-model row contains one capability `<rect data-slot="chart-bar">`,
      one price-in bar, and one price-out bar (three `data-testid`s per row) — command:
      `npx nx run ayokoding-www:test:unit -- benchmark-chart` — acceptance: fails
      ("Cannot find module './benchmark-chart'")
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `benchmark-chart.test.tsx` (new).
    **Notes**: observed failure: `Error: Failed to resolve import "./benchmark-chart"` — equivalent
    RED signal to the plan's illustrative text, correct failure mode.
  - **Gherkin (binds) →** "A rated model's row carries its capability bar and both price bars together"

    ```gherkin
    Scenario: A rated model's row carries its capability bar and both price bars together
      Given a model in the sonnet band with a metered input and output rate
      When the merged chart renders that model's row
      Then the row shows one capability bar, one price-in bar, and one price-out bar
      And all three bars appear stacked within that single row, not in separate chart sections
    ```

  - _Suggested executor: `swe-typescript-dev`_

- [x] [AI] **GREEN**: create `shell/benchmark-chart.tsx` — one `<BenchmarkChart>` component that,
      per rated model in `computeGroups()`'s output, renders a `<g data-testid="benchmark-chart-row-{id}">`
      containing a capability `<Bar>` (reused from `chart-primitives.tsx`) and two price `<Bar>`s
      stacked beneath it via `y` offsets, reusing `<Axis>`/`<BandGroup>`/`<TickRow>`/`scaleLinear`
      unchanged — command: `npx nx run ayokoding-www:test:unit -- benchmark-chart` —
      acceptance: new test passes
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `benchmark-chart.tsx` (new),
    `translations.ts` (added `aiBenchMergedChartTitle`, both locales — pulled forward from Phase 5
    since the component needs a non-fallback title string to render meaningfully). **Notes**:
    `npx nx run ayokoding-www:test:unit -- benchmark-chart` → `1 passed (1)`. The GREEN
    implementation was written broad enough (scaling, harness prop, DD-1, unrated list, accessible
    svg/title all present from this first pass) to also satisfy several later RED steps below
    immediately — each is still verified independently with its own real test run, and every case
    honestly documented as "already satisfied" where no separate failure occurred.
- [x] [AI] **RED**: write a failing test asserting the capability bar's `width` is proportional to
      `index / COMPOSITE_INDEX_MAX` and the price-out bar's `width` is proportional to
      `output / <band price axis max>` — command:
      `npx nx run ayokoding-www:test:unit -- benchmark-chart` — acceptance: fails
      (widths not yet scaled per-bar-type)
  - **Date**: 2026-07-30. **Status**: Done (already satisfied). **Notes**: test added and run
    immediately passed (`2 passed (2)`) — the base component's GREEN step above already wired real
    `scaleLinear` scaling; recorded honestly rather than fabricating a fail.
  - **Gherkin (binds) →** "Bar length is proportional to its own value"

    ```gherkin
    Scenario: Bar length is proportional to its own value
      Given a model with a composite index of 85.7 and an output rate of $15.00
      When the merged chart renders that model's row
      Then the capability bar's length is proportional to 85.7 over the composite index max
      And the price-out bar's length is proportional to $15.00 over that band's price axis max
    ```

- [x] [AI] **GREEN**: wire two independent `scaleLinear` instances into `benchmark-chart.tsx` — one
      over `COMPOSITE_INDEX_MAX` for the capability bar, one over a shared price axis max across all
      rated bands (mirroring `price-chart.tsx`'s single-axis `axisMaxOf` pattern, ported as
      `priceAxisMaxOf`) for both price bars — command:
      `npx nx run ayokoding-www:test:unit -- benchmark-chart` — acceptance:
      new test passes
  - **Date**: 2026-07-30. **Status**: Done. **Notes**: already implemented in the base GREEN step;
    confirmed by the passing test above.
- [x] [AI] **RED**: write a failing test in `benchmark-chart.test.tsx` asserting that when an
      optional `harness` prop names a specific harness for a model priced differently by two
      harnesses, both price bars use `core/price.ts`'s `rateForHarness` for THAT harness rather than
      `lowestRate` — mirroring `price-chart.tsx`'s existing AC-17/AC-18 behavior (DD-8 in
      `tech-docs.md`) — command: `npx nx run ayokoding-www:test:unit -- benchmark-chart` —
      acceptance: fails (`harness` prop not yet read)
  - **Date**: 2026-07-30. **Status**: Done. **Notes**: genuine RED found — first test fixture
    version failed with `AssertionError: expected 380 to be greater than 380` (a single-model
    fixture makes its own rate always the axis max regardless of harness, so the width comparison
    was vacuous); fixed the fixture to add a fixed-rate anchor model pinning the axis max constant
    across both renders, then observed a real assertion failure before the fixture fix (both widths
    equal) confirming the test could fail.
  - **Gherkin (binds) →** "A harness filter switches the merged chart to that harness's rate"

    ```gherkin
    Scenario: A harness filter switches the merged chart to that harness's rate
      Given a fixture model priced differently by two harnesses
      When the merged chart renders with that harness selected
      Then that model's price bars use that harness's own rate, not its lowest available rate
    ```

- [x] [AI] **GREEN**: add an optional `harness?: HarnessId` prop to `BenchmarkChartProps` and thread
      it into each row's price computation — `rateForHarness(model, harness)` when `harness` is set,
      falling back to `lowestRate(model)` when it is `undefined` — mirroring `price-chart.tsx`'s
      `splitByRate` helper — command:
      `npx nx run ayokoding-www:test:unit -- benchmark-chart` — acceptance: new test passes,
      unfiltered rendering (no `harness` prop) still uses `lowestRate` as before
  - **Date**: 2026-07-30. **Status**: Done. **Notes**: already implemented in the base GREEN step
    (`rate = harness !== undefined ? rateForHarness(...) : lowestRate(...)`); confirmed passing
    (`3 passed (3)`) once the fixture above correctly isolated the harness effect.
- [x] [AI] **RED**: write a failing test asserting selecting "Price: Low to High" in a band's
      `FilterSelect`-styled sort dropdown re-orders only that band's rows, leaving other bands'
      row order untouched — command:
      `npx nx run ayokoding-www:test:unit -- benchmark-chart` — acceptance: fails
      (no sort dropdown exists yet)
  - **Date**: 2026-07-30. **Status**: Done. **Notes**: genuine RED —
    `TestingLibraryElementError: Unable to find an element by: [role="combobox"...]` (no sort
    control rendered yet). A second assertion (row re-order) also failed for an unrelated reason
    (the two-model fixture carries no anchor models, so both land in the `light` band, not
    `sonnet` — fixed by targeting `light` and documenting why in the test).
  - **Gherkin (binds) →** "A band's sort control reorders only that band"

    ```gherkin
    Scenario: A band's sort control reorders only that band
      Given the sonnet band is displaying models in capability-descending order
      When the reader selects "Price: Low to High" from the sonnet band's sort control
      Then the sonnet band's rows re-render sorted by ascending output rate
      And the opus and light bands keep their own independently-selected sort order
    ```

- [x] [AI] **GREEN**: add one `FilterSelect` (reused from `benchmark-filters.tsx`) per rated band,
      rendered above the `<svg>` (a native `<select>` cannot live inside SVG without a
      `foreignObject`), wired to a `SortState` prop and an `onSortChange(band, mode)` callback;
      apply `byCapabilityDesc`/`byPriceAsc`/`byPriceDesc` from `core/sort.ts` to that band's array
      only before rendering its rows — command:
      `npx nx run ayokoding-www:test:unit -- benchmark-chart` — acceptance: new test
      passes
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `benchmark-chart.tsx` (added
    `onSortChange` prop + per-band `FilterSelect` controls), `translations.ts` (added
    `aiBenchSortLabel`/`aiBenchSortCapability`/`aiBenchSortPriceAsc`/`aiBenchSortPriceDesc`, both
    locales — pulled forward from Phase 5 for the same reason as the chart title above). **Notes**:
    `npx nx run ayokoding-www:test:unit -- benchmark-chart` → `5 passed (5)`.
- [x] [AI] **RED**: write a failing test asserting a rated, subscription-only-priced model's row
      shows `Subscription ($10.00)` text (via the reused `model-table.tsx` text pattern) in place of
      its two price bars, while its capability bar still renders normally — command:
      `npx nx run ayokoding-www:test:unit -- benchmark-chart` — acceptance: fails
      (DD-1 branch not yet implemented)
  - **Date**: 2026-07-30. **Status**: Done (already satisfied). **Notes**: test added and run
    immediately passed (`6 passed (6)`) — the base component's GREEN step already implemented the
    DD-1 subscription branch; recorded honestly.
  - **Gherkin (binds) →** "A rated model billed only by subscription shows inline subscription text"

    ```gherkin
    Scenario: A rated model billed only by subscription shows inline subscription text
      Given a model in the light band with no metered rate and one subscription rate
      When the merged chart renders that model's row
      Then the row shows its capability bar as normal
      And the price-bar area of that row shows "Subscription ($cost)" text instead of two bars
    ```

- [x] [AI] **GREEN**: implement DD-1's branch in `benchmark-chart.tsx` — when the row's selected
      rate's `kind === "subscription"`, render the reused subscription-text span instead
      of the two `<Bar>` elements for that row's price area — command:
      `npx nx run ayokoding-www:test:unit -- benchmark-chart` — acceptance: new test
      passes
  - **Date**: 2026-07-30. **Status**: Done. **Notes**: already implemented in the base GREEN step;
    confirmed passing above.
- [x] [AI] **RED**: write a failing test asserting an unrated model (no composite index) never
      renders a `data-testid="benchmark-chart-row-{id}"` and instead appears as a plain text entry in
      the unrated list — command: `npx nx run ayokoding-www:test:unit -- benchmark-chart` —
      acceptance: fails (unrated handling not yet implemented)
  - **Date**: 2026-07-30. **Status**: Done (already satisfied). **Notes**: test added and run
    immediately passed (`7 passed (7)`) — the base component's GREEN step already ported the
    unrated-group text-list; recorded honestly.
  - **Gherkin (binds) →** "An unrated model still renders in the existing text-only list"

    ```gherkin
    Scenario: An unrated model still renders in the existing text-only list
      Given a model with no published composite score on any benchmark
      When the merged chart renders the roster
      Then that model appears in the unrated group's plain text list
      And no capability bar or price bar is rendered for that model
    ```

- [x] [AI] **GREEN**: port `capability-chart.tsx`'s unrated-group text-list rendering into
      `benchmark-chart.tsx` unchanged — command: `npx nx run ayokoding-www:test:unit -- benchmark-chart` —
      acceptance: new test passes
  - **Date**: 2026-07-30. **Status**: Done. **Notes**: already implemented in the base GREEN step;
    confirmed passing above. (The old `price-chart.tsx` cross-band subscription-only list is not
    ported — DD-1's resolution retains that GLOBAL list only for unrated-AND-subscription-only
    models, which the merged chart's own unrated list already covers by name.)
- [x] [AI] **RED**: write a failing test asserting the whole `<BenchmarkChart>` renders as one
      `<svg role="img">` with a single `<title>` matching a localized key, and that every figure it
      shows also appears in a rendered `<ModelTable>` fixture (cross-component reachability check) —
      command: `npx nx run ayokoding-www:test:unit -- benchmark-chart` — acceptance:
      fails (no `<title>`/`role="img"` wiring yet)
  - **Date**: 2026-07-30. **Status**: Done (already satisfied). **Notes**: test added and run
    immediately passed (`8 passed (8)`) — the base component's GREEN step already wrapped the chart
    in `<svg role="img" aria-labelledby>` with a single `<title>`; recorded honestly.
  - **Gherkin (binds) →** "The merged chart keeps its accessible name and text alternative"

    ```gherkin
    Scenario: The merged chart keeps its accessible name and text alternative
      Given the merged chart has replaced the two former charts
      When a screen reader encounters the chart
      Then the chart is one svg with role image and one localized title as its accessible name
      And every figure the chart encodes is still reachable via the unchanged ModelTable below
    ```

- [x] [AI] **GREEN**: wrap `benchmark-chart.tsx`'s markup in one `<svg role="img" aria-labelledby={titleId}>`
      with a `<title id={titleId}>{t(locale, "aiBenchMergedChartTitle")}</title>` — command:
      `npx nx run ayokoding-www:test:unit -- benchmark-chart` — acceptance: new test
      passes
  - **Date**: 2026-07-30. **Status**: Done. **Notes**: already implemented in the base GREEN step
    (the translation key was added early, alongside the base component, rather than deferred to
    Phase 5 — see that step's notes); confirmed passing above.
- [x] [AI] **REFACTOR**: extract the per-row rendering (name/index text + 3 stacked bars) into a
      small internal `BenchmarkRow` helper inside `benchmark-chart.tsx` so the four-band loop stays
      readable — command: `npx nx run ayokoding-www:test:unit -- benchmark-chart` —
      acceptance: all `benchmark-chart.test.tsx` cases still pass
  - **Date**: 2026-07-30. **Status**: Done. **Files Changed**: `benchmark-chart.tsx` (extracted
    `BenchmarkRow` component; the band-loop `.map()` now returns one `<BenchmarkRow>` call).
    **Notes**: `npx nx run ayokoding-www:test:unit -- benchmark-chart` → `8 passed (8)` (no
    regression from the extraction).

### Phase 2 Gate

- [x] [AI] `npx nx run ayokoding-www:test:unit -- benchmark-chart` — all cases pass
- [x] [AI] `npx nx affected -t typecheck lint` — both exit 0
- [x] [AI] `capability-chart.tsx` and `price-chart.tsx` still exist unmodified — `git diff --stat main -- apps/ayokoding-www/src/features/ai-benchmark/shell/capability-chart.tsx apps/ayokoding-www/src/features/ai-benchmark/shell/price-chart.tsx`
      returns no output (the live page still renders the OLD two charts; this phase is additive only)

> **Evidence**: `npx nx run ayokoding-www:test:unit -- ai-benchmark` → `Test Files 17 passed (17)`,
> `Tests 653 passed (653)` (up from 645 before this phase — 8 new `benchmark-chart.test.tsx` cases,
> zero regressions). `npx nx affected -t typecheck lint --base=origin/main` → both exit 0 (2
> projects; only preexisting warnings, no new errors — two real typecheck errors surfaced and were
> fixed during this phase: an unused `fullRosterDataset` import in the new test file, and a
> `Figure` fixture field wrongly named `benchmarkId` instead of `benchmark`, plus one `SortMode`
> import corrected from `core/url-state` to its actual home `core/sort`).
> `git diff --stat main -- ... capability-chart.tsx price-chart.tsx` → empty output (both files
> untouched).
>
> **Pause Safety**: `benchmark-chart.tsx` exists, is fully tested, but is not yet wired into
> `benchmark-content.tsx` — the live page is unaffected. Safe to stop. To resume:
> `npx nx run ayokoding-www:test:unit -- benchmark-chart`.

## Phase 3: Wire in the merged chart, delete the old charts

- [x] [AI] Edit `apps/ayokoding-www/src/app/[locale]/tools/ai-benchmark/benchmark-content.tsx`:
      replace the `<CapabilityChart .../>` and `<PriceChart .../>` calls with one
      `<BenchmarkChart dataset={filteredDataset} fullDataset={dataset} locale={locale} sortState={sortState} onSortChange={handleSortChange} harness={filterState.harness} />`
      — the `harness` prop is REQUIRED here, not optional-and-omitted: `price-chart.tsx` currently
      receives `harness={filterState.harness}` (AC-17/AC-18's harness-specific price display), and
      DD-8 in `tech-docs.md` requires the merged chart preserve that behavior unchanged — threading
      `sortState` from `decodeState(searchParams)` and a new `handleSortChange` that mirrors the
      existing `handleFilterChange`'s `latestFilterStateRef` race-guard pattern — acceptance:
      `npx nx run ayokoding-www:test:unit -- benchmark-content` passes with updated assertions

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: `apps/ayokoding-www/src/app/[locale]/tools/ai-benchmark/benchmark-content.tsx`.
  > **Notes**: Wired `<BenchmarkChart>` in with `sortState` derived from `decodeState(searchParams)`
  > and a new `handleSortChange` mirroring `handleFilterChange`'s race-guard pattern. Found and fixed
  > a real regression along the way: `filterState` and `sortState` were both built by re-typing the
  > SAME `decoded` object returned by `decodeState()` (which carries all 6 keys). That left
  > `latestSortStateRef.current` holding its own explicit `harness: undefined`/`class: undefined`
  > keys, so `{ ...next, ...latestSortStateRef.current }` in `handleFilterChange` let those
  > `undefined`s clobber `next`'s real filter values on every filter change — silently emptying the
  > query string. Confirmed via `git stash`/`git stash pop` that the two pre-existing Rule-15
  > EWT-003 regression tests in `benchmark-content.test.tsx` passed before this wiring and failed
  > after, isolating the cause to the wiring rather than a pre-existing bug. Fixed by picking
  > disjoint key sets explicitly (`filterState`/`sortState` each built from named `decoded.*` fields)
  > instead of aliasing both to `decoded`. Re-ran
  > `npx nx run ayokoding-www:test:unit -- benchmark-content` after the fix: 2/2 tests pass.

- [x] [AI] Edit `apps/ayokoding-www/src/app/[locale]/tools/ai-benchmark/benchmark-content.test.tsx`:
      update render assertions to query for `benchmark-chart` slots instead of `capability-chart`/
      `price-chart` — acceptance: test file compiles and passes

  > **Date**: 2026-07-30. **Status**: DONE (no-op, already satisfied).
  > **Files-Changed**: none.
  > **Notes**: `benchmark-content.test.tsx` only covers the Rule-15 EWT-003 filter-URL race (via
  > `BenchmarkFilters`' harness/class selects) — it never queried `capability-chart`/`price-chart`
  > slots to begin with, and `grep -n "capability-chart\|price-chart\|CapabilityChart\|PriceChart"`
  > against this file returns no output. Nothing to rewrite. The actual dangling references to the
  > old chart components live in `test/unit/fe-steps/ai-benchmark.steps.tsx`, handled by the next
  > checklist item. Re-ran `npx nx run ayokoding-www:test:unit -- benchmark-content`: 2/2 pass.

> **Unplanned fix discovered while preparing the steps rewrite below**: Phase 2's `benchmark-chart.tsx`
> silently dropped AC-12 (a low-coverage model must carry a text marker stating its coverage ratio) —
> `capability-chart.tsx` renders this marker; `BenchmarkRow` did not. Root-cause fixed via RED/GREEN
> in `benchmark-chart.test.tsx`/`benchmark-chart.tsx` (two new tests: marker present + correct text
> when coverage is below `LOW_COVERAGE_THRESHOLD`, absent when at/above it) before proceeding, since
> AC-12's Gherkin binding below must bind against `<BenchmarkChart>` and needs the marker to exist.
> `npx nx run ayokoding-www:test:unit -- benchmark-chart`: 10/10 pass (was 8/10 before this fix).

- [x] [AI] Rewrite `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`'s
      `CapabilityChart`/`PriceChart`-dependent step bindings to target `BenchmarkChart` instead —
      this is a hard prerequisite for the next two deletion steps, not optional cleanup: the file's
      `unit-fe` Vitest project glob (`test/unit/fe-steps/**/*.steps.{ts,tsx}`) still imports both
      components directly (AC-12/13/14/15/16/17/18/36/37's direct-render bindings) and also queries
      them by container test id via the `capabilityChartModelIds()`/`priceChartModelIds()` helper
      functions (AC-22..26's `renderPageWithSearch`-based bindings) — every one of these must be
      re-pointed at `<BenchmarkChart>` and its `benchmark-chart-*` test ids BEFORE the two files are
      deleted below, or `unit-fe` fails to even collect this file (a hard module-resolution crash,
      not a failing assertion) — acceptance: `npx nx run ayokoding-www:test:unit -- fe-steps`
      passes with zero references to `CapabilityChart`/`PriceChart` remaining in the file
      (`grep -c "CapabilityChart\|PriceChart" apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`
      returns `0`)

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`,
  > `apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.tsx`,
  > `apps/ayokoding-www/src/features/ai-benchmark/shell/benchmark-chart.test.tsx`.
  > **Notes**: Replaced the `CapabilityChart`/`PriceChart` imports with `BenchmarkChart`; collapsed
  > `capabilityChartModelIds()`/`priceChartModelIds()` into one `benchmarkChartModelIds()` helper
  > (post-merge, both resolve to the same DOM node set, since `BenchmarkRow` always renders a row —
  > never omitting a priceless model the way the old `price-chart.tsx` did). Re-pointed every
  > direct-render scenario (AC-12/13/14/15/16/17/18/36/37) at `BenchmarkChart` and its
  > `benchmark-chart-*` test ids. `grep -c "CapabilityChart\|PriceChart" ...ai-benchmark.steps.tsx`
  > returns `0`.
  >
  > Three more real gaps surfaced (and fixed via RED/GREEN in `benchmark-chart.test.tsx`/
  > `benchmark-chart.tsx`) while making these scenarios pass, beyond task #121's AC-12 fix already
  > recorded above:
  >
  > 1. **DD-2 price labels missing**: `BenchmarkRow`'s price-in/price-out bars carried no formatted-
  >    price text label at all (AC-15 requires one); added `benchmark-chart-label-in-{id}`/
  >    `-label-out-{id}` text, mirroring `price-chart.tsx`'s left-gutter layout.
  > 2. **AC-17 lowest-rate subtitle missing**: `price-chart.tsx`'s "shows the lowest available
  >    harness rate" subtitle (suppressed once a harness filter is active, AC-18) had no equivalent
  >    in `BenchmarkChart`; added `benchmark-chart-subtitle`.
  > 3. **DD-1's retained global list for unrated+subscription-only models**: `tech-docs.md`'s DD-1
  >    explicitly requires the OLD `price-chart.tsx` cross-band subscription list's per-item text
  >    (plan cost + caps) to be retained for models that are BOTH unrated AND subscription-only
  >    (they have no row to attach inline text to) — `BenchmarkChart`'s unrated list rendered only
  >    the bare model name, dropping this. Added the plan-cost/caps text to the unrated list item
  >    when that model's rate is a subscription.
  >
  > Also discovered a genuine, PLAN-DOCUMENTED behavior change (not a gap): the decision-branches
  > diagram in `tech-docs.md` states an unrated model never renders a capability OR price bar in the
  > merged chart — unlike the old `price-chart.tsx`, which rendered metered bars for unrated models
  > too (its band grouping used all four bands, not just the three rated ones). Three AC-15/17/18
  > fixtures in the steps file relied on that old behavior (`figures: []`, i.e. unrated, yet expected
  > price bars) and needed a figure added to become rated, per the new design — not a bug fix, an
  > intentional carry-forward of the plan's own stated simplification.
  >
  > `npx nx run ayokoding-www:test:unit -- fe-steps`: 32 files / 1208 passed, 6 skipped (pre-existing
  > jsdom-incapable placeholders, unrelated). `npx nx run ayokoding-www:typecheck`: exits 0.
  - _Suggested executor: `swe-typescript-dev`_

- [x] [AI] Delete `apps/ayokoding-www/src/features/ai-benchmark/shell/capability-chart.tsx` and
      `apps/ayokoding-www/src/features/ai-benchmark/shell/capability-chart.test.tsx` — acceptance:
      `git status` shows both deleted; `npx nx run ayokoding-www:typecheck` still exits 0 (no
      dangling import)
- [x] [AI] Delete `apps/ayokoding-www/src/features/ai-benchmark/shell/price-chart.tsx` and
      `apps/ayokoding-www/src/features/ai-benchmark/shell/price-chart.test.tsx` — acceptance: same
      as above

  > **Date**: 2026-07-30. **Status**: DONE (both deletion items).
  > **Files-Changed**: deleted `capability-chart.tsx`, `capability-chart.test.tsx`,
  > `price-chart.tsx`, `price-chart.test.tsx`.
  > **Notes**: `git rm` both pairs. Immediately after, `npx nx run ayokoding-www:typecheck` reported
  > exactly the two EXPECTED failures — `chart-order-parity.test.tsx`'s now-dangling imports —
  > confirming the deletion itself introduced no OTHER dangling reference; that one remaining file
  > is the very next checklist item below.

- [x] [AI] Rewrite `apps/ayokoding-www/src/features/ai-benchmark/shell/chart-order-parity.test.tsx`
      to render `<BenchmarkChart>` alone (not two components) and assert each band's DOM row order
      matches `computeGroups()`'s canonical order for every one of the three sort modes —
      acceptance: `npx nx run ayokoding-www:test:unit -- chart-order-parity` passes

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: `apps/ayokoding-www/src/features/ai-benchmark/shell/chart-order-parity.test.tsx`.
  > **Notes**: The pre-merge version rendered two components and compared their DOM row orders
  > against EACH OTHER — trivially true post-merge (same component, same render). Rewrote as three
  > tests against `<BenchmarkChart>` alone: default (capability) order matches
  > `computeGroups()`'s own canonical order, `sortState.light: "price-asc"` reorders ascending by
  > output price, `"price-desc"` reorders descending — using a fixture whose composite score and
  > output price are deliberately uncorrelated so the three modes produce three different orders.
  > `npx nx run ayokoding-www:test:unit -- chart-order-parity`: 3/3 pass. `typecheck`: exits 0.

- [x] [AI] Run the full `ai-benchmark` unit suite: `npx nx run ayokoding-www:test:unit -- ai-benchmark` —
      acceptance: exits 0, and no dangling reference to the deleted modules remains anywhere in
      `src/` OR `test/` — run
      `grep -rl "capability-chart\|price-chart" apps/ayokoding-www/src/features/ai-benchmark apps/ayokoding-www/src/app apps/ayokoding-www/test/unit/fe-steps`
      (note: `-l`, files WITH a match — NOT `-L`, whose "files without a match" semantics would
      silently pass even if a leftover import exists) and confirm it returns **no output**

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: `chart-primitives.tsx`, `benchmark-chart.tsx`, `benchmark-chart.test.tsx`,
  > `ai-benchmark.steps.tsx`, `translations.ts`.
  > **Notes**: `npx nx run ayokoding-www:test:unit -- ai-benchmark`: 15 files / 646 tests pass. The
  > lowercase `grep -rl` scoped to the three named paths initially returned FOUR files — all
  > historical prose comments citing the retired filenames by name (e.g. "mirrors
  > `capability-chart.tsx`'s RATED_BANDS"), not live imports — reworded each to name the retired
  > component descriptively instead of by its literal deleted filename, so the check now returns
  > true-clean. While at it, also found and removed three genuinely orphaned translation keys
  > (`aiBenchCapabilityChartTitle`, `aiBenchPriceChartTitle`, `aiBenchPriceSubscriptionHeading`,
  > both locales) that no longer had any reader now that both retired charts are gone — confirmed
  > via a repo-wide grep before removal. Re-ran the full suite + typecheck after every edit: still
  > 646/646 and exits 0. Final check: `grep -rl "capability-chart\|price-chart" ...` returns no
  > output.

### Phase 3 Gate

- [x] [AI] `npx nx run ayokoding-www:test:unit -- ai-benchmark` — exits 0
- [x] [AI] `npx nx affected -t typecheck lint` — both exit 0
- [x] [AI] `grep -rl "CapabilityChart\|PriceChart" apps/ayokoding-www/src apps/ayokoding-www/test`
      returns no output (no dangling reference to the deleted component names anywhere, including
      the `test/unit/fe-steps/` step-definition file the plain `src`-only scope would have missed)

  > **Date**: 2026-07-30. **Status**: DONE. All three Phase 3 Gate checks green.
  > **Files-Changed**: none beyond what the phase's own items already record.
  > **Notes**: `test:unit -- ai-benchmark`: 15/15 files, 646/646 tests. `nx affected -t typecheck
lint --base=main`: both exit 0 for `ayokoding-www` and `ayokoding-www-fe-e2e` (warnings only,
  > pre-existing style patterns e.g. `jsx-a11y/prefer-tag-over-role` on the `role="img"` svg — same
  > pattern the retired charts already used). `grep -rl "CapabilityChart\|PriceChart" ...`: no
  > output.

> **Pause Safety**: the live page now renders the merged chart; the two old chart files are gone.
> The repo builds and all unit tests pass. Safe to stop. To resume:
> `npx nx run ayokoding-www:test:unit -- ai-benchmark`.

## Phase 4: Gherkin — rewrite and extend `ai-benchmark.feature`

- [x] [AI] Edit `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`:
      rewrite the scenario "Models are ordered identically in both charts within a band" (AC-11) to
      "Models are ordered identically before and after a sort change within a band" (per prd.md), AND
      separately rewrite AC-18 ("A harness filter switches the price chart to that harness's rate")
      to "A harness filter switches the merged chart to that harness's rate" — copy prd.md's
      Acceptance criteria (Gherkin) section's AC-18 rewrite-target scenario VERBATIM (title AND
      Given/When/Then body, not just the title), because Phase 2's RED step already binds to this
      exact wording via its `**Gherkin (binds) →**` tag and the two must stay verbatim-equal per the
      Gherkin-Tagged Delivery Steps convention. These are the TWO scenarios explicitly named for a
      full title-and-body rewrite, but they are not the only scenarios whose body still names the
      retired components — AC-12/13/14/15/16/17/36/37 (single-chart logic scenarios) and AC-23/AC-24
      (harness/class narrowing, which separately assert against "the capability chart" AND "the price
      chart" as two distinct components) all use `When the capability chart is rendered` / `When the
price chart is rendered` / `the capability chart` / `the price chart` as their subject — reword
      each to reference "the merged chart" (or generalize the wording), merging or splitting scenarios
      where the underlying assertion is now redundant across the two former components, per
      `brd.md`'s own success metric that none be left describing removed UI — acceptance: the
      widened grep below (not a narrower one scoped to "both charts" alone) returns `0`

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`.
  > **Notes**: AC-11 and AC-18 rewritten verbatim from prd.md. AC-12/13/14/15/17/36/37 and AC-23/AC-24
  > reworded to "the merged chart" (AC-36 and AC-23/AC-24 each collapsed two `Then`/`And` chart
  > assertions into one, since there is only one chart to assert against post-merge). AC-16 reworded
  > from "renders in the subscription group" (a container that no longer exists post-merge) to "shows
  > its plan cost in the unrated list", matching DD-1's actual resolution for an unrated+
  > subscription-only model. AC-20's title ("...every figure the charts encode") also singularized.
  > `grep -cE "both charts|capability chart|price chart" ai-benchmark.feature` → `0`.

- [x] [AI] Add the 9 new scenarios from `prd.md`'s Acceptance Criteria section (merged row, bar
      proportionality, per-band sort, URL sort encoding, unknown sort fallback, DD-1 subscription
      text, unrated text list, accessible name, identical breakpoint structure) to the feature file
      — acceptance: `grep -c "^  Scenario" specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      returns `48` (39 existing scenarios, 2 rewritten in place per the two items above — AC-11 and
      AC-18 — net zero change to the count — plus 9 genuinely new scenarios from `prd.md`'s
      11-scenario Acceptance criteria section, of which 2 are the in-place rewrite targets counted
      above (AC-11, AC-18) and 9 are additions: 39 + 9 = 48)

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: `ai-benchmark.feature`.
  > **Notes**: 9 new scenarios (AC-39..AC-47) added verbatim from prd.md, inserted after AC-37.
  > `grep -c "^  Scenario" ai-benchmark.feature` → `48`.

- [x] [AI] Implement or extend the corresponding step definitions in
      `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx` (search for the file first:
      `find apps/ayokoding-www -iname "*ai-benchmark*.steps.*"`) so every new scenario has a passing
      step implementation, building on Phase 3's rewrite of the `CapabilityChart`/`PriceChart`
      bindings — acceptance: `npx nx run ayokoding-www:specs:behavior:coverage` exits 0

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: `apps/ayokoding-www/test/unit/fe-steps/ai-benchmark.steps.tsx`.
  > **Notes**: renamed 19 step-text strings + 8 Scenario titles to match the reworded/rewritten
  > Gherkin exactly (0 orphans). Added a `bandFixtureModel` helper (models scored so index equals
  > `score` directly, via a shared roster-max holder) and a `rowOrderWithin` helper, then implemented
  > full Given/When/Then/And bindings for all 9 new scenarios (AC-39..AC-47), including a genuine
  > multi-band (opus/sonnet/light) fixture for AC-41's per-band sort isolation check — discovered and
  > fixed a real test bug where the sonnet/opus anchor models themselves also render as rows in their
  > own bands (their ids must appear in the expected order arrays, not just the two purpose-built
  > fixture models). `npx nx run ayokoding-www:test:unit -- fe-steps`: 32 files / 1252 passed, 6
  > skipped (pre-existing, unrelated). `npx nx run ayokoding-www:specs:behavior:coverage`: valid, 42
  > specs / 342 scenarios / 1231 steps, all covered.

- [x] [AI] Update `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/README.md` if it lists
      per-feature scenario counts or a C4 diagram referencing the two-chart architecture —
      acceptance: no remaining reference to "capability chart" and "price chart" as two separate
      diagrams in that README

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/README.md`.
  > **Notes**: no C4 diagram present; the one-line feature description ("...harness price chart")
  > reworded to "one merged chart per band showing capability bands, composite index, and
  > per-harness price together".

### Phase 4 Gate

- [x] [AI] `npx nx run ayokoding-www:specs:behavior:coverage` — exits 0
- [x] [AI] `grep -cE "both charts|capability chart|price chart" specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`
      returns `0` — this widened check (not `grep -c "both charts"` alone) is the safety net that
      catches every scenario naming a retired chart component, not just the one scenario explicitly
      named in the first checklist item above

  > **Date**: 2026-07-30. **Status**: DONE. Both Phase 4 Gate checks green.
  > **Files-Changed**: none beyond what the phase's own items already record.
  > **Notes**: `specs:behavior:coverage`: "Spec coverage valid! 42 specs, 342 scenarios, 1231 steps —
  > all covered." Widened grep: no output (exit 1 / count 0). Also re-ran
  > `npx nx run ayokoding-www:test:unit -- ai-benchmark` (15 files/690 tests),
  > `npx nx run ayokoding-www:typecheck` (exits 0), and `npx nx run ayokoding-www:lint` (exits 0,
  > warnings only, pre-existing patterns) to confirm the phase leaves no regression.

> **Pause Safety**: the feature file and its step definitions fully describe the merged-chart
> behavior; `specs:behavior:coverage` is green. Safe to stop. To resume:
> `npx nx run ayokoding-www:specs:behavior:coverage`.

## Phase 5: Translations

- [x] [AI] Edit `apps/ayokoding-www/src/features/i18n/core/translations.ts`: add
      `aiBenchMergedChartTitle`, `aiBenchSortLabel`, `aiBenchSortCapability`,
      `aiBenchSortPriceAsc`, `aiBenchSortPriceDesc` to BOTH the `en` and `id` locale blocks —
      acceptance: `npx nx run ayokoding-www:test:unit -- translations` (or the
      existing no-raw-key-leak test referenced by prd.md's "No raw translation key leaks" scenario)
      passes for both locales

  > **Date**: 2026-07-30. **Status**: DONE (already satisfied — added in Phase 1/2).
  > **Files-Changed**: none this step; verified `apps/ayokoding-www/src/features/i18n/core/translations.ts`
  > already carries all 5 keys in both the `en` (lines 113-117) and `id` (lines 484-488) blocks,
  > added while wiring `BenchmarkChart`'s sort controls in earlier phases.
  > **Notes**: `npx nx run ayokoding-www:test:unit -- translations`: 1 file / 6 tests pass.

- [x] [AI] Run `npx nx run ayokoding-www:test:unit -- ai-benchmark` — acceptance:
      exits 0, no "aiBench" token leaks into rendered text in either locale

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: none.
  > **Notes**: 15 files / 690 tests pass, including AC-35's "No raw translation key leaks on either
  > locale" outline (en + id).

### Phase 5 Gate

- [x] [AI] `npx nx run ayokoding-www:test:unit -- ai-benchmark` — exits 0
- [x] [AI] `grep -c "aiBenchSortLabel" apps/ayokoding-www/src/features/i18n/core/translations.ts`
      returns `2` (once per locale)

  > **Date**: 2026-07-30. **Status**: DONE. Both Phase 5 Gate checks green.
  > **Files-Changed**: none.
  > **Notes**: `test:unit -- ai-benchmark`: 15/15 files, 690/690 tests. `grep -c "aiBenchSortLabel"
translations.ts` → `2`.

> **Pause Safety**: every new UI string is translated in both `en` and `id`. Safe to stop. To
> resume: `npx nx run ayokoding-www:test:unit -- ai-benchmark`.

## Local Quality Gates (Before Push)

- [x] [AI] Run affected typecheck: `npx nx affected -t typecheck`
- [x] [AI] Run affected linting: `npx nx affected -t lint`
- [x] [AI] Run affected quick tests: `npx nx affected -t test:quick`
- [x] [AI] Run affected spec coverage: `npx nx affected -t test:specs`
- [x] [AI] Fix ALL failures — including preexisting issues not caused by your changes
- [x] [AI] Re-run failing checks to confirm resolution
- [x] [AI] Verify zero failures before pushing

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: `apps/ayokoding-www-fe-e2e/src/steps/ai-benchmark.steps.ts` (fixed during
  > this gate — see below).
  > **Notes**: `npx nx affected -t typecheck lint --base=main`: 0 errors, 25 projects (warnings
  > only, pre-existing patterns). First `npx nx affected -t test:quick --base=main` run reported
  > `Failed tasks: ayokoding-www-fe-e2e:test:quick`, but the detail was truncated by the output
  > buffer. Re-ran `npx nx run ayokoding-www-fe-e2e:test:quick --skip-nx-cache` directly: exits 0
  > clean (typecheck, lint, `specs:e2e:coverage` all pass — "0 new unbound scenario(s) beyond
  > baseline"). Re-ran the full `npx nx affected -t test:quick --base=main` a second time with warm
  > cache: `Successfully ran target test:quick for 25 projects and 11 tasks they depend on` — 0
  > failed tasks (35/36 tasks served from cache). Root cause: this repo has a known
  > flaky-`test:quick`-under-parallel-hook-load class of failure (Nx cache warm-up + concurrent
  > agent load), not a real regression — confirmed by the immediate clean pass on direct re-run of
  > the same target with no code changes in between. `npx nx affected -t test:specs --base=main`:
  > passed across all 25 affected projects (from the earlier e2e-coverage-gap fix commit
  > `3ea845211`); `ayokoding-www:specs:behavior:coverage`: "Spec coverage valid! 42 specs, 342
  > scenarios, 1231 steps — all covered."

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix preexisting errors
> encountered during work. Do not defer or skip existing issues. Commit preexisting fixes
> separately with appropriate conventional commit messages.

### Commit Guidelines

- [x] [AI] Commit changes thematically — group related changes into logically cohesive commits
- [x] [AI] Follow Conventional Commits format: `<type>(<scope>): <description>`
- [x] [AI] Split different domains/concerns into separate commits (core, component, wiring/deletion,
      specs, i18n)
- [x] [AI] Preexisting fixes get their own commits, separate from plan work
- [x] [AI] Do NOT bundle unrelated changes into a single commit

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: none this step (verification only).
  > **Notes**: local commit history for this plan is already split thematically: `2a54bde63`
  > (component), `057ec1954`/`554ff306d`/`01a03b972` (Phase 3 wiring/deletion/rebind), `75b6cb297`
  > (plan-doc evidence), `588f8351c` (Phase 4 Gherkin), `05af02af6` (Phase 5 i18n verification),
  > `3ea845211` (preexisting e2e-coverage-gap fix, its own commit per Root Cause Orientation). No
  > unrelated changes bundled; `git status` clean at this checkpoint.

## Phase 6: Manual Verification

### Manual UI Verification (Playwright MCP) — all locales × all breakpoints

- [x] [AI] Discover supported locales: read `apps/ayokoding-www/src/features/i18n/core/config.ts` —
      acceptance: locale set confirmed as `en`, `id`
- [x] [AI] Start dev server: `nx dev ayokoding-www` — acceptance: server listens on port 3101
- [x] [AI] For EACH locale (`en`, `id`) × EACH breakpoint (375 / 768 / 1280 px): navigate to
      `/en/tools/ai-benchmark` and `/id/tools/ai-benchmark` via `browser_navigate` + `browser_resize`
      — acceptance: page renders, no layout break
- [x] [AI] Inspect DOM via `browser_snapshot` at all 6 combinations (2 locales × 3 breakpoints) and
      confirm the merged chart's row structure (name/index text, 3 stacked bars) is IDENTICAL across
      all 3 breakpoints for the same locale (only bar pixel width differs) — acceptance: satisfies
      prd.md's "identical DOM structure at every breakpoint" scenario
- [x] [AI] Exercise the per-band sort dropdowns via `browser_click`/`browser_select_option` for at
      least one band, confirming only that band's rows re-order — acceptance: matches
      "A band's sort control reorders only that band"
- [x] [AI] Copy the URL after selecting a non-default sort and reload it via `browser_navigate` —
      acceptance: the same sort order reappears (matches "A band's sort choice is encoded in the URL")
- [x] [AI] Check for JS errors via `browser_console_messages` — must be zero errors per locale per
      breakpoint
- [x] [AI] Capture one screenshot per locale per breakpoint via `browser_take_screenshot`, saved to
      `evidence/phase-6-benchmark-chart-en-375px.png`, `evidence/phase-6-benchmark-chart-en-768px.png`,
      `evidence/phase-6-benchmark-chart-en-1280px.png`, and the `id` locale equivalents —
      acceptance: 6 files exist in `evidence/`
- [x] [AI] Document evidence in this checklist: reference each screenshot
      (`![AI benchmark merged chart, en locale, 375px](./evidence/phase-6-benchmark-chart-en-375px.png)`,
      and so on for the remaining 5) and note console/network status per locale

  > **Date**: 2026-07-30. **Status**: DONE.
  > **Files-Changed**: `plans/in-progress/ayokoding-www-ai-benchmark-merged-chart/evidence/phase-6-benchmark-chart-{en,id}-{375,768,1280}px.png`
  > (6 new files).
  > **Notes**: Locale set confirmed from `SUPPORTED_LOCALES = ["en", "id"]`. Dev server
  > (`npx nx dev ayokoding-www`) confirmed listening on port 3101 via polled `curl` → `200`.
  > All 6 locale × breakpoint combinations rendered the merged "Capability and price by model"
  > chart (id: "Kemampuan dan harga per model", fully translated, no raw key leaks) with 3 sort
  > comboboxes (Sort — Opus/Sonnet/Light) and stacked capability + input + output price bars per
  > row. DOM comparison (`browser_snapshot` grep at en/375px vs. en/1280px): identical heading,
  > combobox, option, and row-label structure — only pixel geometry differs, confirming
  > `BenchmarkChart` never reads viewport width. Exercised the Sonnet band's sort control
  > (`browser_select_option` → `price-asc`): Sonnet rows re-sorted strictly ascending by output
  > rate ($3.48→$50, "Not reported" last), while Opus (`GPT-5.6 Sol, Claude Opus 5`) and Light
  > (`Qwen3.7 Max → Claude Haiku 4.5`) bands kept their original capability-descending order
  > untouched — confirms "A band's sort control reorders only that band". URL after the change:
  > `?sortSonnet=price-asc`; `browser_navigate` reload of that exact URL reproduced the identical
  > Sonnet order with the combobox's `price-asc` option marked `[selected]` — confirms "A band's
  > sort choice is encoded in the URL". `browser_console_messages` (level: warning, which includes
  > errors) returned 0 errors / 0 warnings across every one of the 6 navigations plus the sort-change
  > and URL-reload checks.
  >
  > ![AI benchmark merged chart, en locale, 375px](./evidence/phase-6-benchmark-chart-en-375px.png)
  > ![AI benchmark merged chart, en locale, 768px](./evidence/phase-6-benchmark-chart-en-768px.png)
  > ![AI benchmark merged chart, en locale, 1280px](./evidence/phase-6-benchmark-chart-en-1280px.png)
  > ![AI benchmark merged chart, id locale, 375px](./evidence/phase-6-benchmark-chart-id-375px.png)
  > ![AI benchmark merged chart, id locale, 768px](./evidence/phase-6-benchmark-chart-id-768px.png)
  > ![AI benchmark merged chart, id locale, 1280px](./evidence/phase-6-benchmark-chart-id-1280px.png)

### Phase 6 Gate

- [x] [AI] All 6 screenshots exist under `evidence/` and are referenced above
- [x] [AI] Zero console errors recorded across all 6 locale/breakpoint combinations
- [x] [AI] `npx nx affected -t typecheck lint test:quick test:specs` — all exit 0

  > **Date**: 2026-07-30. **Status**: DONE. All 3 Phase 6 Gate checks green.
  > **Files-Changed**: none this step (verification only).
  > **Notes**: `ls evidence/` confirms all 6 PNGs present (`{en,id}-{375,768,1280}px`, 765KB-1.8MB
  > each). `browser_console_messages` (level warning, includes errors) returned 0/0 across all 6
  > navigations plus the sort-change and URL-reload checks. `npx nx affected -t typecheck lint
test:quick test:specs --base=main`: `Successfully ran targets typecheck, lint, test:quick,
test:specs for 25 projects and 6 tasks they depend on` — 0 failures.

> **Pause Safety**: the merged chart is manually verified across both locales and all three
> breakpoints, with committed evidence. Safe to stop. To resume: re-run
> `npx nx affected -t typecheck lint test:quick test:specs` and re-open the dev server if a
> visual re-check is needed.

## Phase 7: Delivery Boundary — Push, PR Finalization, Review Cycle

> This phase pushes, opens the PR for review, and runs the PR-Review Maker→Fixer Cycle — it does
> **not** merge. Archival (Phase 9) commits land on this SAME PR branch before the merge; see the
> [Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode)'s
> Archival-in-PR requirement.

### Post-Push CI Verification

- [ ] [AI] Push changes to the PR branch: `git push origin ayokoding-www-ai-benchmark-merged-chart`
- [ ] [AI] Monitor the PR's GitHub Actions check run: `gh pr checks ayokoding-www-ai-benchmark-merged-chart --watch=false`
      polled every 2 minutes (never tight-loop, never `gh run watch`) per
      [CI Monitoring Convention](../../../repo-governance/development/workflow/ci-monitoring.md)
- [ ] [AI] Verify ALL CI checks pass — no exceptions
- [ ] [AI] If any CI check fails, fix immediately and push a follow-up commit; repeat until green
- [ ] [AI] Mark the PR ready for review: `gh pr ready ayokoding-www-ai-benchmark-merged-chart`

### PR-Review Maker→Fixer Cycle

- [ ] [AI] Cycle 1: fan out the eight discipline specialists
      (`pr-review-architecture-maker`, `pr-review-logic-maker`, `pr-review-governance-maker`,
      `pr-review-security-maker`, `pr-review-integrity-maker`, `pr-review-performance-maker`,
      `pr-review-docs-maker`, `pr-review-instruction-maker`) against the PR, consolidate via
      `pr-review-synthesis-maker` (the sole poster of record via the GitHub Reviews API), resolve
      all findings via `pr-review-fixer`, push fixes, re-verify CI green — acceptance: CI green
      after cycle 1's fixes
- [ ] [AI] Cycle 2: repeat the same fan-out → synthesis → fixer → CI-green sequence
- [ ] [AI] Cycle 3: repeat the same fan-out → synthesis → fixer → CI-green sequence
- [ ] [AI] Confirm no unresolved HIGH/CRITICAL finding remains after cycle 3 — acceptance:
      `pr-review-synthesis-maker`'s final consolidated review shows zero open blocking findings

### Rule-15 Three-Tester Retest (before archival)

- [ ] [AI] Run the three live-site testers (the `web-ux-test-fixing-planning` workflow:
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) against the deployed
      preview or local dev server for `/en/tools/ai-benchmark` and `/id/tools/ai-benchmark` —
      acceptance: EWT/UWT/DWT findings + spec-gaps recorded
- [ ] [AI] Append each finding here as a new unchecked checkbox, source-attributed
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`) and
      each SG-###/USS-### into the Gherkin steps in Phase 4
- [ ] [AI] Fix every rule-15 EWT/UWT/DWT defect finding before archival — deferral requires explicit
      user permission (only when genuinely impossible); SG-###/USS-### may be triaged or deferred
      with written rationale
- [ ] [AI] If any rule-15 fix touched app code, push the follow-up commit(s) and re-verify CI green
      before proceeding to Phase 8

### Phase 7 Gate

- [ ] [AI] `gh pr checks ayokoding-www-ai-benchmark-merged-chart --json` (or the equivalent status
      query) shows every CI check passing
- [ ] [AI] `pr-review-synthesis-maker`'s final consolidated review (cycle 3) shows zero open
      blocking findings
- [ ] [AI] Every rule-15 EWT/UWT/DWT defect finding above is ticked, or explicitly deferred with
      written user-granted permission
- [ ] [AI] The PR is NOT YET merged: `gh pr view ayokoding-www-ai-benchmark-merged-chart --json state --jq .state`
      returns `OPEN`

> **Pause Safety**: the PR is open, CI-green, fully reviewed, and rule-15-clean, but deliberately
> not yet merged — the worktree and branch are both still intact. Safe to stop. To resume:
> `gh pr view ayokoding-www-ai-benchmark-merged-chart --json state,mergeable`.

## Phase 8: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._
> **Non-boundary phase** — this phase's commit lands on the SAME PR branch above; it opens no new
> PR and does not push on its own (Phase 9 pushes it together with the archival commit).

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface
      would catch this automatically next time; discard the rest with a one-line reason —
      acceptance: every entry has either a route or a discard reason
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if
      unsanitizable — acceptance: `learnings.md` contains no raw secret
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — this is a public-repo-only
      plan (no infra-private content is possible here), so this gate trivially passes but is still
      checked — acceptance: confirmed
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing
      matrix — non-code homes may land inline (small edit) or as a `plans/backlog/` follow-up
      (large); code homes (`apps/`, `libs/`, tests) are ALWAYS filed as a separate
      `plans/backlog/<slug>/` plan and NEVER landed inline — acceptance: every `learnings.md` entry
      records its terminal routing state
- [ ] [AI] If no generalizable learning surfaced, record the explicit escape in `learnings.md`:
      `No generalizable learnings — <one-line reason>` — acceptance: `learnings.md` is never
      silently empty
- [ ] [AI] Commit the triaged `learnings.md` (and any inline-routed learning) locally in the
      worktree: `git commit -am "docs(plans): triage learnings for ayokoding-www-ai-benchmark-merged-chart"`
      — acceptance: `git log -1 --oneline` shows the commit; NOT pushed yet (Phase 9 pushes it
      together with the archival commit below)

### Phase 8 Gate

- [ ] [AI] Every `learnings.md` entry is in a terminal state (routed inline, filed as backlog, or
      discarded with reason), or the file records the explicit "none" escape
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR

> **Pause Safety**: `learnings.md` is fully triaged and committed locally, not yet pushed. Safe to
> stop. To resume: re-read `learnings.md` and confirm every entry is terminal, then continue to
> Phase 9.

## Phase 9: Plan Archival, Final Push, and Merge

> This is the delivery boundary itself. Per the Delivery Mode convention's Archival-in-PR
> requirement, the `git mv` + README-update archival commit lands and is pushed to the SAME PR
> branch BEFORE the merge — mirroring
> `plans/done/2026-07-30__ayokoding-www-tools-ai-benchmark/delivery.md`'s Phase 11–12 pattern
> (archival commits first, merge and worktree removal last).

### Plan Archival

- [ ] [AI] Verify ALL delivery checklist items above are ticked
- [ ] [AI] Verify the Knowledge Capture phase is complete — every `learnings.md` entry reached a
      terminal state or the file records the explicit "none" escape; both safety gates were applied
- [ ] [AI] Verify ALL quality gates pass locally: `npx nx affected -t typecheck lint test:quick test:specs`
      exits 0
- [ ] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`
- [ ] [AI] Verify ALL supported locales (`en`, `id`) were exercised in UI verification
- [ ] [AI] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires
      explicit user permission (only when genuinely impossible) for defect findings; SG-###/USS-###
      may be triaged or deferred
- [ ] [AI] Rename and move: `git mv plans/in-progress/ayokoding-www-ai-benchmark-merged-chart/ plans/done/YYYY-MM-DD__ayokoding-www-ai-benchmark-merged-chart/`
      using today's date as the completion date (NOT the creation date) — acceptance: the folder
      exists under `plans/done/` and the `evidence/`/`assets/` subfolders moved with it
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date
- [ ] [AI] Update `plans/README.md` if it references this plan
- [ ] [AI] Commit the archival locally in the worktree (the `evidence/`/`assets/` subfolders move
      with the plan): `git commit -am "chore(plans): move ayokoding-www-ai-benchmark-merged-chart to done"`
      — acceptance: `git log -1 --oneline` shows the commit

### Final Push and Merge

- [ ] [AI] Push both trailing commits (Knowledge Capture from Phase 8 + this phase's archival
      commit) to the SAME PR branch: `git push origin ayokoding-www-ai-benchmark-merged-chart` —
      acceptance: `gh pr view ayokoding-www-ai-benchmark-merged-chart --json commits --jq '.commits | length'`
      reflects both new commits
- [ ] [AI] Re-verify CI is green after this push: `gh pr checks ayokoding-www-ai-benchmark-merged-chart --watch=false`,
      polled every 2 minutes — acceptance: all checks pass
- [ ] [AI] Once CI is green on the archival push, merge the PR:
      `gh pr merge ayokoding-www-ai-benchmark-merged-chart --squash --delete-branch=false`
      (branch deletion deferred to worktree cleanup below) — acceptance:
      `gh pr view ayokoding-www-ai-benchmark-merged-chart --json state --jq .state` returns `MERGED`

### Phase 9 Gate

- [ ] [AI] `gh pr view ayokoding-www-ai-benchmark-merged-chart --json state --jq .state` returns
      `MERGED`
- [ ] [AI] CI is green on `main` at the merge commit: `gh run list --branch main --limit 1 --json conclusion --jq '.[0].conclusion'`
      returns `success`
- [ ] [AI] Remove the worktree: `git worktree remove worktrees/ayokoding-www-ai-benchmark-merged-chart` —
      acceptance: `git worktree list` no longer shows it

> **Pause Safety**: the archival commit is merged into `main` along with the rest of the PR, CI is
> green on `main`, and the worktree is removed. Safe to stop indefinitely. To resume: re-check
> `git log main -1` shows the merge commit, and `plans/done/YYYY-MM-DD__ayokoding-www-ai-benchmark-merged-chart/`
> exists.
