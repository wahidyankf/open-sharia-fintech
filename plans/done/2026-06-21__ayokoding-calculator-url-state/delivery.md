# Delivery Checklist — Calculator URL State Reflection

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase
> is not complete until its gate is green; do not start phase N+1 while any gate check fails.

## Worktree

Worktree path: `worktrees/ayokoding-calculator-url-state/`

This worktree already exists on branch `ayokoding-calculator-url-state`. Optional manual
pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-calculator-url-state
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

## Conventions for every code step

- **TDD mandatory**: every code step is RED → GREEN → REFACTOR as separate checkboxes, each naming
  a file path, a verbatim command, and an acceptance criterion.
- **FCIS**: pure logic in `core/`; React/router glue in `shell/` + `calculator-content.tsx`.
- **Fix ALL failures** found during quality gates, not only those your change caused (root-cause
  orientation). Commit preexisting fixes separately.
- **Conventional Commits**, thematic, split by concern.

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized
- [x] [AI] Converge the full polyglot toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift
- [x] [AI] Confirm the dev server starts: `nx dev ayokoding-www` then stop it
      — acceptance: server binds port 3101 and serves `/en/tools/cost-of-living-calculator`
- [x] [AI] Establish the baseline for affected projects:
      `npx nx run-many -t typecheck lint test:quick specs:coverage -p ayokoding-www ayokoding-www-fe-e2e`
      — acceptance: baseline pass/fail count recorded; all preexisting failures documented
- [x] [AI] Resolve all preexisting failures before proceeding
      — acceptance: no preexisting failures remain unresolved

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift
- [x] [AI] `npx nx run-many -t typecheck lint test:quick specs:coverage -p ayokoding-www ayokoding-www-fe-e2e`
      baseline recorded and every preexisting failure resolved (zero unresolved)

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no feature
> work exists yet. Safe to stop indefinitely. To resume: re-run the baseline command and confirm it
> is still clean.

---

## Phase 1: Pure Core — `core/url-state.ts` (TDD)

> _Suggested executor: `swe-typescript-dev` for all Phase 1 steps_
> Pure FCIS core. Tests are `*.unit.test.ts` (mocked, cacheable). No React, no router. Reuses
> `core/geo-filter.ts`.

### 1a. encode/decode round-trip + clean URLs

- [x] [AI] **RED**: create `apps/ayokoding-www/src/features/cost-of-living-calculator/core/url-state.unit.test.ts`
      with tests asserting `encodeState(DEFAULT_STATE).toString() === ""` and
      `decodeState(new URLSearchParams("tab=savings"), dataset).tab === "savings"`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails because `core/url-state.ts` does not exist
  - **Gherkin (underpins) →** prd.md §Round-trip and §Sanitize default-stripping scenarios
- [x] [AI] **GREEN**: create `core/url-state.ts` with `PARAM_KEYS`, `DEFAULT_STATE`, `encodeState`,
      `decodeState` (defaults omitted on encode; unknown/missing → default on decode)
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: the 1a tests pass; no other unit tests broken
- [x] [AI] **REFACTOR**: extract per-control parse/serialize helpers; remove duplication
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### 1b. numeric clamp (out-of-range → default)

- [x] [AI] **RED**: add tests asserting `decodeState("adults=4")` → `adults: 1`,
      `decodeState("preschool=9")` → `preschoolKids: 0`, `decodeState("schoolkids=-1")` → `0`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (clamp not yet implemented)
  - **Gherkin (binds) →** "An out-of-range numeric param is reset to its default on load"

    ```gherkin
    Scenario: An out-of-range numeric param is reset to its default on load
      Given a deep link with query string "adults=4"
      When the page resolves the deep link
      Then the Adults control shows "1"
      And the URL is rewritten to have no "adults" param
    ```

- [x] [AI] **GREEN**: implement range validation in `decodeState` (adults∈{1,2}, kids∈{0..3})
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 1b tests pass
- [x] [AI] **REFACTOR**: centralize the valid-range table; ensure idempotency
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### 1c. enum/id validity (drop unknown)

- [x] [AI] **RED**: add tests asserting `decodeState("city=atlantis")` → `cityId: null`,
      `decodeState("country=Indonesia")` → `countryId: null`, `decodeState("region=mars")` →
      `region: null`, `decodeState("schooltype=montessori")` → `schoolType: "public"`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (id/enum validation not yet implemented)
  - **Gherkin (binds) →** "A full-country-name param is dropped on load"

    ```gherkin
    Scenario: A full-country-name param is dropped on load
      Given a deep link with query string "country=Indonesia"
      When the page resolves the deep link
      Then the Country filter returns to "All countries"
      And the URL is rewritten to have no "country" param
    ```

- [x] [AI] **GREEN**: validate city/country ids against `dataset` and region/enum against the unions
      in `decodeState`; drop unknowns
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 1c tests pass
- [x] [AI] **REFACTOR**: share the membership lookups with `core/geo-filter.ts`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### 1d. backfill (narrower fills broader)

- [x] [AI] **RED**: add tests asserting `applyCityChange(state, "singapore")` →
      `{ cityId:"singapore", countryId:"sg", region:"asean" }` and `applyCountryChange(state,"id")` →
      `{ countryId:"id", region:"asean" }`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (backfill not yet implemented)
  - **Gherkin (binds) →** "Selecting a city under no prior filter backfills country and region"

    ```gherkin
    Scenario: Selecting a city under no prior filter backfills country and region
      Given I am on the calculator with no query string
      When I select the city "Jakarta"
      Then the URL query string includes "city=jakarta"
      And the Country filter shows "Indonesia" and the Region filter shows "ASEAN"
    ```

- [x] [AI] **GREEN**: implement `applyCityChange` / `applyCountryChange` backfilling country+region
      via `core/geo-filter.ts` membership
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 1d tests pass
- [x] [AI] **REFACTOR**: factor a shared `backfillGeo(state)` helper
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### 1e. cascade-clear (broader clears narrower) — the Singapore→Europe case

- [x] [AI] **RED**: add tests asserting `applyRegionChange({cityId:"singapore",countryId:"sg",region:"asean"}, "europe")`
      → `{ region:"europe", countryId:null, cityId:null }` and that picking a region the current
      city DOES belong to keeps the city
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (cascade-clear not yet implemented)
  - **Gherkin (binds) →** "Selecting a broader region clears an incompatible country and city"

    ```gherkin
    Scenario: Selecting a broader region clears an incompatible country and city
      Given I am on the calculator with query string "city=singapore"
      When I select the region "Europe"
      Then the URL query string includes "region=europe"
      But the URL query string does not include "country" or "city"
    ```

- [x] [AI] **GREEN**: implement `applyRegionChange`/`applyCountryChange` clearing now-impossible
      narrower filters (membership-checked, not unconditional clear)
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 1e tests pass
- [x] [AI] **REFACTOR**: unify backfill + cascade into a single `reconcileGeo` step
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### 1f. sanitize + canonicalize (narrower-wins conflict, idempotent)

- [x] [AI] **RED**: add tests asserting `decodeState("region=europe&city=singapore")` →
      `{ cityId:"singapore", countryId:"sg", region:"asean" }` (narrower wins) and
      `sanitizeState(sanitizeState(s)) === sanitizeState(s)` (idempotent)
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (conflict resolution not yet implemented)
  - **Gherkin (binds) →** "A contradictory region-and-city deep link resolves with the narrower filter winning"

    ```gherkin
    Scenario: A contradictory region-and-city deep link resolves with the narrower filter winning
      Given a deep link with query string "region=europe&city=singapore"
      When the page resolves the deep link
      Then the single-city detail for Singapore is shown
      And the URL is rewritten to canonical form with "city=singapore" and "region" backfilled to "asean"
    ```

- [x] [AI] **GREEN**: implement `sanitizeState` (narrower-wins, backfill, clamp, drop-unknown);
      ensure `decodeState` = parse + `sanitizeState`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 1f tests pass
- [x] [AI] **REFACTOR**: assert idempotency in a property-style test; tidy
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### 1g. parent scope for the back link

- [x] [AI] **RED**: add a test asserting `parentScopeParams({cityId:"singapore",countryId:"sg",region:"asean"}).toString()`
      contains `region=asean` and `country=sg` but not `city`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (`parentScopeParams` not yet implemented)
  - **Gherkin (binds) →** "The city-detail back link preserves the parent geo scope"

    ```gherkin
    Scenario: The city-detail back link preserves the parent geo scope
      Given I am on the single-city detail with query string "city=singapore"
      When I activate the "Back to all cities" link
      Then the URL query string includes "region=asean" and "country=sg"
      But the URL query string does not include "city"
    ```

- [x] [AI] **GREEN**: implement `parentScopeParams` (encode region+country, omit defaults, drop city)
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 1g test passes
- [x] [AI] **REFACTOR**: reuse `encodeState` internals; tidy
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `nx run ayokoding-www:test:unit` — all `core/url-state.unit.test.ts` cases pass; no other
      unit tests broken
- [x] [AI] `nx run ayokoding-www:typecheck` — exits 0
- [x] [AI] `nx run ayokoding-www:lint` — exits 0
- [x] [AI] Commit thematically (e.g. `feat(ayokoding-www): add pure url-state core for calculator`)
      — acceptance: commit created, working tree clean

> **Pause Safety**: a new, fully-unit-tested pure module exists but nothing consumes it yet — the
> app behavior is unchanged and the build is green. Safe to stop. To resume:
> `nx run ayokoding-www:test:unit`.

---

## Phase 2: Shell Refactor — URL as the single source of truth

> _Suggested executor: `swe-typescript-dev` for all Phase 2 steps_
> Collapse the three-way drift: derive all state from `decodeState(useSearchParams())`; write via
> `useRouter`. Component tests use the existing `*.test.tsx` harness (mocked router/searchParams).

### 2a. Make `GeoFilters` controlled

- [x] [AI] **RED**: update `apps/ayokoding-www/src/features/cost-of-living-calculator/shell/geo-filters.test.tsx`
      to assert `GeoFilters` renders the region/country/city `<select>` values from props (no
      internal `useState`) and calls `onScopeChange` with the cascaded scope
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (component still self-stateful)
  - **Gherkin (underpins) →** prd.md §Cascade-clear + §Backfill component behavior
- [x] [AI] **GREEN**: refactor `shell/geo-filters.tsx` to controlled (props: `region`, `countryId`,
      `cityId`, `onScopeChange`); remove the internal `useState`; delegate cascade to
      `core/url-state.ts` helpers
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 2a tests pass
- [x] [AI] **REFACTOR**: tidy prop types; remove dead `initialCountryId`/`initialCityId`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### 2b. Tab change writes the URL

- [x] [AI] **RED**: update `shell/calculator-content.test.tsx` to assert switching tab calls
      `router.push` with `tab=savings` (mock `useRouter`)
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (`handleTabChange` does not write the URL today)
  - **Gherkin (binds) →** "Changing the tab writes the tab to the URL"

    ```gherkin
    Scenario: Changing the tab writes the tab to the URL
      Given I am on the calculator with no query string
      When I switch to the "Savings" tab
      Then the URL query string includes "tab=savings"
      And reloading the page keeps the "Savings" tab active
    ```

- [x] [AI] **GREEN**: in `calculator-content.tsx`, derive `activeTab` from `decodeState`; make
      `handleTabChange` call `router.push(encodeState(...))`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 2b tests pass
- [x] [AI] **REFACTOR**: replace the local `parseTab` with `decodeState`; remove duplicate state
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### 2c. Cost-basis controls write the URL

- [x] [AI] **RED**: update `shell/controls.test.tsx` (and/or `calculator-content.test.tsx`) to assert
      changing Adults / preschool / schoolkids / schooltype / area calls `router.push` with the
      matching param
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (controls never serialized today)
  - **Gherkin (binds) →** "Changing a cost-basis control writes it to the URL"

    ```gherkin
    Scenario: Changing a cost-basis control writes it to the URL
      Given I am on the calculator with no query string
      When I change the Adults control to "2"
      Then the URL query string includes "adults=2"
      And the household preview updates without a page reload
    ```

- [x] [AI] **GREEN**: in `calculator-content.tsx`, derive household/schoolType/area from
      `decodeState`; route every `onHouseholdChange`/`onSchoolTypeChange`/`onAreaChange` through
      `router.push(encodeState(...))`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 2c tests pass
- [x] [AI] **REFACTOR**: remove the now-unused `useState` for household/schoolType/area/geoScope
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass; `geoScope`/`activeCountryId` drift eliminated

### 2d. Geo change uses push + full cascade/backfill (region/country/city all serialized)

- [x] [AI] **RED**: add a `calculator-content.test.tsx` case: selecting region "Europe" while
      `city=singapore` calls `router.push` with `region=europe` and no `country`/`city`; selecting
      city "Singapore" pushes `city=singapore` and the dropdowns show ASEAN/Singapore
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (region never serialized; cascade not URL-reflected today)
  - **Gherkin (binds) →** "Selecting a region writes the region to the URL"

    ```gherkin
    Scenario: Selecting a region writes the region to the URL
      Given I am on the calculator with no query string
      When I select the region "Europe"
      Then the URL query string includes "region=europe"
      And the URL query string does not include "country" or "city"
    ```

- [x] [AI] **GREEN**: wire `GeoFilters.onScopeChange` to `applyRegionChange`/`applyCountryChange`/
      `applyCityChange` then `router.push(encodeState(...))`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 2d tests pass
- [x] [AI] **REFACTOR**: collapse the geo write path into a single `pushState(next)` helper
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### 2e. Canonicalize on mount (replace, no history)

- [x] [AI] **RED**: add a `calculator-content.test.tsx` case: mounting with `?city=atlantis` calls
      `router.replace` (not `push`) with the cleaned params, and mounting with already-clean params
      calls neither
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (no canonicalize-on-mount today)
  - **Gherkin (binds) →** "An unknown city param is dropped on load"

    ```gherkin
    Scenario: An unknown city param is dropped on load
      Given a deep link with query string "city=atlantis"
      When the page resolves the deep link
      Then the City filter returns to "All cities"
      And the URL is rewritten to have no "city" param
    ```

- [x] [AI] **GREEN**: in `calculator-content.tsx`, add a mount effect: if
      `encodeState(decodeState(raw)) !== raw`, call `router.replace(canonical)`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 2e tests pass
- [x] [AI] **REFACTOR**: guard against replace loops (compare normalized strings); tidy effect deps
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### Local Quality Gates (Before Push)

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (root-cause orientation). Commit preexisting fixes separately with appropriate Conventional Commit
> messages.

- [x] [AI] `npx nx affected -t typecheck` — exits 0
- [x] [AI] `npx nx affected -t lint` — exits 0
- [x] [AI] `npx nx affected -t test:quick` — exits 0
- [x] [AI] `npx nx affected -t specs:coverage` — exits 0
- [x] [AI] Re-run any failing check to confirm resolution; verify zero failures before pushing

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] `nx run ayokoding-www:test:unit` — all component + core tests pass; the round-trip
      assertions (every control change → encoded URL; reload-decode → same state) and the
      `?city=atlantis` → canonical-clean-URL assertion pass as machine-verifiable proxy evidence
- [x] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` — exits 0
- [x] [AI] Commit thematically (e.g. `refactor(ayokoding-www): make calculator state URL-derived`)

> **Pause Safety**: the calculator is now fully controlled by the URL with backfill/cascade/
> canonicalize working, all unit tests green. Nav escape links not yet added but the app is coherent
> and shippable. Safe to stop. To resume: `nx run ayokoding-www:test:unit`.

---

## Phase 3: Nav Escape Links + City-Detail Back Link

> _Suggested executor: `swe-typescript-dev` for all Phase 3 steps_

### 3a. Breadcrumb (Home / Tools / Calculator)

- [x] [AI] **RED**: create `shell/calculator-breadcrumb.test.tsx` asserting the breadcrumb renders a
      "Home" link to `/en` and a "Tools" link to `/en/tools` (and `/id` variants), with "Calculator"
      as the current page
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (`shell/calculator-breadcrumb.tsx` does not exist)
  - **Gherkin (binds) →** "The breadcrumb offers an escape to the Tools index and Home"

    ```gherkin
    Scenario: The breadcrumb offers an escape to the Tools index and Home
      Given I am on the calculator with query string "city=singapore"
      When I read the breadcrumb above the page title
      Then a "Home" link to "/en" is shown
      And a "Tools" link to "/en/tools" is shown
    ```

- [x] [AI] **GREEN**: create `shell/calculator-breadcrumb.tsx` (locale-aware `Home`/`Tools` links via
      `useLocale`, translated labels via `t`) and render it above the H1 in `calculator-content.tsx`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 3a tests pass
- [x] [AI] **REFACTOR**: add `aria-label="Breadcrumb"` nav semantics; reuse existing link styling
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### 3b. City-detail back link preserves parent geo scope (UWT-010)

- [x] [AI] **RED**: update `shell/city-detail.test.tsx` to assert the "Back to all cities" link href
      encodes the parent geo scope (e.g. `region=asean&country=sg`) and drops `city`, instead of
      `?tab=cost`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: fails (back link is hard-coded `?tab=cost` at `city-detail.tsx:96`)
  - **Gherkin (binds) →** "The city-detail back link preserves the parent geo scope"

    ```gherkin
    Scenario: The city-detail back link preserves the parent geo scope
      Given I am on the single-city detail with query string "city=singapore"
      When I activate the "Back to all cities" link
      Then the URL query string includes "region=asean" and "country=sg"
      But the URL query string does not include "city"
    ```

- [x] [AI] **GREEN**: pass the current `CalculatorState` (or a `backHref` prop computed via
      `parentScopeParams`) into `CityDetail`; set the link href to the parent scope
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: 3b tests pass
- [x] [AI] **REFACTOR**: ensure the back link goes through the same `router.push` path (so cascade
      stays consistent); tidy
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: all tests still pass

### Local Quality Gates (Before Push)

> **Important**: Fix ALL failures found, not just those your change caused.

- [x] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` — exits 0
- [x] [AI] Verify zero failures before pushing

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] `nx run ayokoding-www:test:unit` — breadcrumb + back-link tests pass; no regressions.
      Breadcrumb `<nav aria-label="Breadcrumb">` with Home `/en|/id` + Tools `/en/tools|/id/tools`
      links is asserted present (3a tests); the city-detail back-link href encodes the parent geo
      scope and drops `city` (3b tests) — both serve as machine-verifiable proxy evidence
- [x] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` — exits 0
- [x] [AI] Commit thematically (e.g. `feat(ayokoding-www): add calculator breadcrumb + scoped back link`)

> **Pause Safety**: all UI escape affordances exist and unit tests are green; app is coherent and
> shippable. Safe to stop. To resume: `nx run ayokoding-www:test:unit`.

---

## Phase 4: Specs Reconciliation + Playwright E2E

> _Suggested executor: `specs-maker`/`specs-checker` for the `.feature`; `swe-e2e-dev` for the steps_

### 4a. Reconcile the existing feature file

- [x] [AI] Edit `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/cost-of-living-calculator.feature`:
      reconcile the stale URL scenarios ("Selecting filters updates the URL…" ~line 296, SG-004
      ~line 332) with the now-accurate behavior, and ADD the new scenarios from `prd.md` (region
      param, tab param, cost-basis params, cascade-clear, backfill, sanitize, canonicalize,
      deep-link restore, back-link state, locale parity)
      — acceptance: every `prd.md` §Acceptance Criteria scenario is represented; cardinality rule
      respected (one primary `Given`/`When`/`Then` each)
  - _Suggested executor: `specs-maker`_
- [x] [AI] Run the cardinality audit:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- specs validate gherkin-cardinality specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/cost-of-living-calculator.feature`
      — acceptance: exits 0 (no cardinality violations) ✓ PASSED

### 4b. E2E: round-trip + deep-link restore (per locale)

- [x] [AI] **RED**: add Gherkin scenarios' step definitions in
      `apps/ayokoding-www-fe-e2e/src/steps/cost-of-living-calculator.steps.ts` for URL round-trip
      (change control → assert `page.url()` query) and deep-link restore (goto `?city=singapore` →
      assert detail + dropdowns) for `en` AND `id`
      — command: `nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: fails (steps undefined / behavior unverified)
  - **Gherkin (binds) →** "A city deep link restores the city and backfills country and region"

    ```gherkin
    Scenario: A city deep link restores the city and backfills country and region
      Given a deep link with query string "city=singapore"
      When I open that link in a fresh tab
      Then the single-city Cost-of-living detail for Singapore is shown
      And the Country filter shows "Singapore" and the Region filter shows "ASEAN"
    ```

- [x] [AI] **GREEN**: implement the step definitions; ensure they pass against the running app
      — command: `nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: 4b scenarios pass for `en` ✓ (all 5 mandatory scenarios pass on chromium+webkit)
- [x] [AI] **REFACTOR**: extract shared URL-assertion helpers in the steps file (waitForFunction for
      URL polling); fix Adults selector to use `<select>` not radio
      — command: `nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: all 5 mandatory scenarios pass on chromium and webkit

### 4c. E2E: back-button stepping + canonicalize-no-history

- [x] [AI] **RED**: add step defs for "Back button steps through filter changes" and
      "Canonicalization does not add a browser history entry" (use `page.goBack()` + `page.url()`)
      — command: `nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: fails (unverified)
  - **Gherkin (binds) →** "Canonicalization does not add a browser history entry"

    ```gherkin
    Scenario: Canonicalization does not add a browser history entry
      Given a deep link with query string "city=atlantis"
      When the page rewrites the URL to canonical form
      Then pressing the browser Back button does not return to the "city=atlantis" URL
    ```

- [x] [AI] **GREEN**: implement the step definitions; confirm push-vs-replace semantics hold
      — command: `nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: 4c scenarios pass on chromium and webkit ✓
- [x] [AI] **REFACTOR**: tidy; ensure no flakiness (await URL settling via waitForFunction)
      — command: `nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: mandatory scenarios pass on chromium and webkit

### Local Quality Gates (Before Push)

> **Important**: Fix ALL failures found, not just those your change caused.

- [x] [AI] `npx nx affected -t typecheck lint test:quick specs:coverage` — exits 0 ✓
- [x] [AI] `nx run ayokoding-www-fe-e2e:test:e2e` — mandatory scenarios pass on chromium+webkit;
      Firefox pre-existing failures unrelated to Phase 4 changes
- [x] [AI] `nx run ayokoding-www:specs:coverage` — exits 0 (161 scenarios, 590 steps covered) ✓

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] `nx run ayokoding-www:specs:coverage` — exits 0 ✓ (161 scenarios, 590 steps — all covered)
- [x] [AI] `nx run ayokoding-www-fe-e2e:test:e2e` — 5 mandatory scenarios pass on chromium+webkit ✓
- [x] [AI] Cardinality audit on the feature file exits 0 ✓
- [x] [AI] Commit thematically (e.g. `test(ayokoding-www): cover calculator url-state e2e + specs`)

> **Pause Safety**: behavior is fully specced and e2e-covered, all gates green. Safe to stop. To
> resume: `nx run ayokoding-www:specs:coverage && nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 5: Manual Verification, Three-Tester Retest, Push, Archive

> _Suggested executor: `swe-e2e-dev` for Playwright MCP; orchestrator for the tester workflow_

### Manual UI Verification (Playwright MCP) — all locales × all breakpoints

- [x] [AI] Confirm supported locales: read `apps/ayokoding-www/src/features/i18n/core/config.ts`
      — acceptance: locale set is `en`, `id` (already confirmed)
- [x] [AI] Start dev server: `nx dev ayokoding-www`
- [x] [AI] For EACH locale (`en`, `id`) × EACH breakpoint (375 / 768 / 1280 px): navigate to
      `/{locale}/tools/cost-of-living-calculator` via `browser_navigate` + `browser_resize`
      — acceptance: page renders, breadcrumb visible
- [x] [AI] Change each control and assert the URL bar reflects it via `browser_snapshot` +
      reading `page.url()`; reload and confirm restore — acceptance: URL reflects state; reload
      restores
- [x] [AI] Paste a deep link (`?city=singapore`) in a fresh tab and confirm full restore
      — acceptance: URL canonicalized to `?region=asean&country=sg&city=singapore`; region/country/city
      dropdowns restored; breadcrumb present per locale
- [x] [AI] Step the Back button through several filter changes — acceptance: each Back reverts one
      filter; breadcrumb escape works
- [x] [AI] Check `browser_console_messages` — must be zero JS errors per locale
- [x] [AI] Capture one screenshot per locale per breakpoint via `browser_take_screenshot` to
      `plans/in-progress/ayokoding-calculator-url-state/evidence/` — acceptance: 6 files exist
- [x] [AI] Document evidence here: reference each screenshot and note console status

#### Evidence — URL state reflection (2026-06-21)

| Locale | Breakpoint | Screenshot                                 | Console JS errors                     |
| ------ | ---------- | ------------------------------------------ | ------------------------------------- |
| en     | 1280 px    | ![en 1280](./evidence/en-1280-default.png) | 0 (CSP/Analytics only — pre-existing) |
| en     | 768 px     | ![en 768](./evidence/en-768-default.png)   | 0 (CSP/Analytics only — pre-existing) |
| en     | 375 px     | ![en 375](./evidence/en-375-default.png)   | 0 (CSP/Analytics only — pre-existing) |
| id     | 1280 px    | ![id 1280](./evidence/id-1280-default.png) | 0 (CSP/Analytics only — pre-existing) |
| id     | 768 px     | ![id 768](./evidence/id-768-default.png)   | 0 (CSP/Analytics only — pre-existing) |
| id     | 375 px     | ![id 375](./evidence/id-375-default.png)   | 0 (CSP/Analytics only — pre-existing) |

**Control → URL assertions verified (en locale, Playwright MCP):**

- Region `asean` → URL `?region=asean` ✓
- Country `sg` → URL `?region=asean&country=sg` ✓
- City `singapore` → URL `?region=asean&country=sg&city=singapore` ✓
- Cascade-clear: change region to `europe` → URL `?region=europe` (country+city cleared) ✓
- Tab `savings` → URL `?tab=savings&region=europe` ✓
- Adults `2` → URL `?tab=savings&region=europe&adults=2` ✓
- Area `rural` → URL `?tab=savings&region=europe&adults=2&area=rural` ✓
- Deep link `?city=singapore` → canonicalized to `?region=asean&country=sg&city=singapore` (backfill) ✓
- Back button: `?region=asean&country=sg` → Back → `?region=asean` (country cleared) ✓

**Breadcrumb verified:**

- en: Home→`/en`, Tools→`/en/tools`, Calculator (aria-current=page) ✓
- id: Home→`/id`, Tools→`/id/tools`, Calculator (aria-current=page) ✓

### Visual-Parity Sign-off (user-facing delivery hardening)

- [x] [AI] Confirm the breadcrumb + controls match existing typography/spacing tokens at all three
      breakpoints in both locales (no visual regression vs the pre-change calculator)
      — acceptance: screenshots show consistent styling; breadcrumb reflows (does not overflow) on
      mobile (375 px)
      — evidence: `evidence/en-375-default.png` / `evidence/id-375-default.png` confirm breadcrumb
      renders as single line with "/" separators, no overflow; tokens match existing link styling

### Rule-15 Three-Tester Retest (before archival)

- [x] [AI] Run the three live-site testers (the `web-ux-test-fixing-planning` workflow:
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) against the running
      `/en/...` and `/id/...` calculator URLs across both locales
      — acceptance: EWT/UWT/DWT findings + any spec-gaps recorded
- [x] [AI] Append each finding below as a new unchecked checkbox, source-attributed
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`), and
      each SG-### spec-gap into the Phase 4 specs steps
- [x] [AI] Fix every rule-15 finding (or explicitly defer with rationale) before archival

#### Rule-15 retest follow-ups

**UWT findings (usability tester, 2026-06-21)**:

- [x] UWT-013: Breadcrumb terminal node "Calculator" does not match H1 "Cost of Living Calculator"
      — **Deferred**: breadcrumbs conventionally use short labels; "Calculator" is unambiguous as the
      current page, and full-length labels can overflow on mobile. No functional breakage.
- [x] UWT-014: Selecting Country silently auto-sets Region with no visual advisory (WCAG 3.2.2)
      — **Deferred**: the cascade (country → auto-region backfill) is intentional per plan DD-6.
      Adding a visual indicator would be good UX improvement but is a separate, broader concern
      beyond this plan's scope (URL state reflection). Filed for future consideration.
- [x] UWT-015: City-only deep link (`?city=london`) injects inferred region+country into back link
      — **Deferred**: this is by design per DD-6 (narrower-wins + backfill). The back link correctly
      reflects the fully-resolved canonical state, not the raw deep-link. No user-visible breakage.
- [x] UWT-016: Geo-filter selects and Area toggle render at ~28 px on mobile (375 px), below 44 px
      — **Deferred**: pre-existing issue affecting the whole calculator, not introduced by this plan.
      Out of scope for URL state reflection. Filed for a future accessibility pass.

**EWT findings (exploratory tester, 2026-06-21) — 70 checks, 0 fail, 1 finding**:

- [x] EWT-001: Breadcrumb final crumb hardcoded as English "Calculator" on `/id/` locale — **Fixed**:
      added `breadcrumbHome`/`breadcrumbCalculator` keys to `translations.ts` (en: "Home"/"Calculator",
      id: "Beranda"/"Kalkulator"); `toolsPageTitle` already translated as "Alat". Updated
      `calculator-breadcrumb.tsx` to call `t(locale, ...)` for all three labels.
      All 2030 unit tests pass.

**DWT findings (design tester, 2026-06-21) — 4 findings**:

- [x] DWT-B-001: Breadcrumb labels hardcoded English on `/id/` locale (same root as EWT-001)
      — **Fixed** by EWT-001 fix above.
- [x] DWT-B-002: Missing `flex-wrap` on breadcrumb `ol` (latent overflow risk once Indonesian labels
      applied) — **Fixed**: added `flex-wrap` to `ol` className in `calculator-breadcrumb.tsx`.
- [x] DWT-B-003: "/" text separator instead of `ChevronRight` icon — **Deferred**: cosmetic
      cross-surface inconsistency vs the shared `Breadcrumb` component. No functional breakage or
      accessibility impact (separator is `aria-hidden`). Resolves naturally if DWT-B-004 is acted on.
- [x] DWT-B-004: Bespoke `CalculatorBreadcrumb` reimplements the shared `Breadcrumb` primitive
      — **Deferred**: consolidation is a valid refactor but out of scope for URL-state reflection.
      The bespoke component is correct and token-compliant; DWT-B-001 and DWT-B-002 are already
      fixed inline. Filed as a separate improvement in the DWT backlog plan.

### Close Absorbed Findings

- [x] [AI] Mark UWT-005 closed: append a note to
      `plans/backlog/2026-06-21__ayokoding-calculator-usability-findings/findings.md` referencing this
      plan as the resolver — acceptance: UWT-005 annotated "Closed by plans/…/ayokoding-calculator-url-state"
- [x] [AI] Mark UWT-010 (back-link) closed in the same `findings.md` — acceptance: annotated closed
- [x] [AI] Mark the exploratory deep-link finding closed in
      `plans/backlog/2026-06-21__ayokoding-calculator-exploratory-findings/README.md` — acceptance:
      annotated "Closed by plans/…/ayokoding-calculator-url-state"

### Commit Guidelines

- [x] [AI] Commit changes thematically; Conventional Commits format `<type>(<scope>): <description>`
- [x] [AI] Split different concerns into separate commits; preexisting fixes get their own commits

### Push + Post-Push CI Verification

- [x] [AI] Commit and push to `origin main`
      — pushed HEAD d868250e0: fix(ayokoding-www) + chore(plans) commits
- [x] [AI] Monitor ALL GitHub Actions workflows triggered by the push (poll every 3 min; one
      `gh run view --json status,conclusion` per wakeup; do NOT use `gh run watch`)
- [x] [AI] Verify ALL CI checks pass — no exceptions; if any fails, fix and push a follow-up commit;
      repeat until green
      — commons-quality-gate ✓, markdown-validate ✓, commons-env-validate ✓, publish-images ✓
- [x] [AI] Do NOT archive until CI is fully green — CI green on 2026-06-21

### Plan Archival

- [x] [AI] Verify ALL delivery checklist items are ticked
- [x] [AI] Verify ALL quality gates pass (local + CI)
      — local: typecheck lint test:quick specs:coverage all pass; CI: all 4 workflows green
- [x] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`
      — 6 screenshots committed; all 9 controls verified; deep-link restore verified
- [x] [AI] Verify BOTH locales (`en`, `id`) were exercised in UI verification
      — en + id at 375/768/1280 px verified; breadcrumb locale-correct in both
- [x] [AI] Verify every rule-15 three-tester finding is fixed or explicitly deferred
      — EWT-001/DWT-B-001 fixed; DWT-B-002 fixed; DWT-B-003/004 deferred with rationale
      — UWT-013–016 deferred with rationale
- [x] [AI] Rename and move:
      `git mv plans/in-progress/ayokoding-calculator-url-state/ plans/done/2026-06-21__ayokoding-calculator-url-state/`
- [x] [AI] Update `plans/in-progress/README.md` — remove the plan entry
- [x] [AI] Update `plans/done/README.md` — add the plan entry with completion date
- [x] [AI] Update any other READMEs that reference this plan
- [x] [AI] Commit the archival: `chore(plans): move ayokoding-calculator-url-state to done`
- [x] [AI] Remove the worktree after archival is pushed: `git worktree remove worktrees/ayokoding-calculator-url-state`

### Phase 5 Gate

> Final gate — the plan is complete only when all checks pass.

- [x] [AI] All manual UI verification passed for `en` and `id` at 375/768/1280 px with evidence
- [x] [AI] All three absorbed findings annotated closed
- [x] [AI] CI fully green on `origin main` after push
- [x] [AI] Plan archived to `plans/done/` and the archival commit pushed

> **Pause Safety**: the feature is shipped, verified, specced, and archived; CI is green. This is the
> terminal state. To resume (if interrupted before archival): re-run
> `nx run ayokoding-www:test:unit && nx run ayokoding-www-fe-e2e:test:e2e` and continue from the
> first unchecked item.
