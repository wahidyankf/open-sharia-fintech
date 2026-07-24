# Product Requirements: Harden `ayokoding-www-fe-e2e` Bulk-Link-Check Concurrency

## Persona

**The plan executor / CI maintainer** running `ayokoding-www-fe-e2e:test:e2e` as part of an affected
suite, a PR gate, or the `main-ci` scheduled sweep — needs a failure in this suite to mean "a link
actually broke," not "the machine was busy."

## User Story

As a plan executor or CI maintainer, I want the bulk-link-check scenarios in
`ia-navigation-revamp.steps.ts` and `course-rehome-redirects.steps.ts` to pass deterministically
under normal concurrent load, so that a red check reliably signals a real content/routing
regression rather than transient network contention.

## Scope

**In scope**: the request-issuing pattern inside the two named step files only.

**Out of scope**: any other e2e project's step files, any product route/redirect logic.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Bulk internal-link checks stay reliable under concurrent load

  Background:
    Given the ayokoding-www-fe-e2e suite includes scenarios that check every internal link on a page

  Scenario: A page with many internal links is checked without exceeding a bounded concurrency limit
    Given a rendered page with more internal links than the configured concurrency limit
    When the "every link resolves" step runs
    Then no more than the configured limit of link checks are in flight at once
    And every link's resolution status is still asserted exactly as before

  Scenario: A single transient network error on one link does not fail the whole check outright
    Given one link's request transiently fails with a network-layer error
    When the step retries that single request once
    Then the retry either succeeds and the check proceeds normally
    Or the retry also fails and the step reports that specific link as the failure

  Scenario: A genuine 404 or drained location still fails the check
    Given a link that resolves to a 404 or a drained/missing location
    When the step runs
    Then the assertion fails on that link, unaffected by the concurrency/retry change
```

## Non-Goals

- Does not change what counts as a passing vs. failing link resolution — only how reliably the check
  itself completes under load.
- Does not add retries to genuine content assertions (title matches, redirect-chain checks) beyond
  the network-transport layer of the request itself.
