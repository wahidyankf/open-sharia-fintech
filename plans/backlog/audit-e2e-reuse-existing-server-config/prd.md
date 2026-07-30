# Product Requirements: Audit `reuseExistingServer` Across `*-e2e` Playwright Configs

## Persona

An engineer or AI agent running an `*-e2e` Playwright suite — needs the suite to always exercise
the configured `webServer.command` (and its env vars), never a stale, unrelated process that
happens to already be bound to the target port.

## User Story

As an engineer or AI agent running an `*-e2e` Playwright suite, I want `reuseExistingServer` to
never silently substitute an unrelated stale server for the suite's own configured build, so that a
passing (or failing) e2e run reflects the code under test rather than whatever process happened to
already be bound to the port.

## Product Scope

Covers the six `playwright.config.ts` files enumerated in `README.md`'s Context; does not cover the
e2e test scenarios or assertions themselves.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: reuseExistingServer audit and remedy

  Scenario: CI runners are confirmed ephemeral per job
    Given the availability investigation confirms CI runners are ephemeral per job
    When the audit concludes
    Then the remedy is a documentation caveat for local development, not a config change

  Scenario: CI runners are confirmed shared or persistent
    Given the availability investigation confirms CI runners are shared or persistent
    When the audit concludes
    Then each of the six hardcoded-true configs is gated to match
      "organiclever-app-web-e2e"'s "reuseExistingServer: !process.env.CI" pattern

  Scenario: A future *-e2e config is added
    Given the audit's chosen remedy includes an automated guard
    When a new "*-e2e" Playwright config sets "reuseExistingServer: true" unconditionally
    Then the guard flags it before merge
```

## Non-Goals

- Does not change the e2e test scenarios themselves.
- Does not re-litigate the already-fixed `ayokoding-www-tools-ai-benchmark` incident this plan was
  filed from.
