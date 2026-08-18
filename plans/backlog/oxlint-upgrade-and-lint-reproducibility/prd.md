# Product Requirements — oxlint Upgrade and Lint-Toolchain Reproducibility

## User Stories

**US-1** — As a contributor, I want CI to fail only because of my change, so that a red gate is a
signal about my work rather than about a third party's release schedule.

**US-2** — As a maintainer, I want the search dialog to avoid cascading re-renders, so that typing in
search does not schedule avoidable render passes.

**US-3** — As a maintainer, I want linter upgrades to be a deliberate, reviewed act, so that new rules
arrive with a decision attached rather than as a surprise outage.

**US-4** — As a maintainer, I want to know every place the toolchain resolves a version at run time,
so that today's fix is not repeated per-tool for the rest of the project's life.

## Acceptance Criteria

### AC-1 — the violation is fixed (US-2)

```gherkin
Feature: Search dialog result visibility

  Scenario: A query below the minimum length shows no results
    Given the search dialog is open
    When the user types "a"
    Then no search results are rendered
    And no additional render is scheduled by an effect

  Scenario: Clearing a query drops previously fetched results
    Given the search dialog is open
    And the user has typed "kubernetes" and results have been rendered
    When the user clears the query
    Then no search results are rendered

  Scenario: A query at or above the minimum length fetches results
    Given the search dialog is open
    When the user types "ku"
    And the debounce interval elapses
    Then search results are rendered
```

The regression test **must fail before the WS-O1 fix and pass after**. A test that passes both ways
does not satisfy this criterion.

### AC-2 — the upgrade is taken deliberately (US-3)

```gherkin
Feature: oxlint version management

  Scenario: The pinned version is current
    Given both repositories declare oxlint as a devDependency
    When the declared version is compared against the latest published release
    Then they match, or a written reason for the gap exists in the plan

  Scenario: Every upgrade finding has a disposition
    Given the upgrade surfaces a set of new lint findings
    When each finding is triaged
    Then it is either fixed in source
    Or disabled in oxlint.json with a stated reason
    And no finding is left unaddressed and unexplained
```

### AC-3 — no lint target resolves at run time (US-1)

```gherkin
Feature: Reproducible lint toolchain

  Scenario: No project fetches a linter during a gate run
    Given every project.json and package.json in the repository
    When they are searched for run-time version resolution
    Then zero lint or gate commands resolve a version at run time

  Scenario: Both repositories agree
    Given ose-public and ose-private both declare oxlint
    When the two declared versions are compared
    Then they are identical
```

**Falsifiability note.** AC-3's first scenario must be checked with a rule that would have caught the
original defect — `npx oxlint@latest`. Confirm the check reports non-zero against a deliberately
reintroduced unpinned invocation before trusting a zero.

### AC-4 — the class is enumerated (US-4)

```gherkin
Feature: Run-time resolution audit

  Scenario: Every run-time resolution has a verdict
    Given a sweep of project.json, package.json, .github/workflows/, and .husky/
    When each run-time-resolving invocation is listed
    Then each carries a verdict of pinned, deliberately floating with reason, or must pin
    And the count of unverdicted entries is zero
```

## Out of Scope

Replacing oxlint or eslint. Adopting a specific dependency-update bot — a candidate outcome of WS-O3,
not a requirement. Fixing the twenty orphaned `rhino-cli` test binaries.
