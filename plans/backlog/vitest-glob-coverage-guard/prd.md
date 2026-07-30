# Product Requirements: Vitest Glob-Coverage Guard

## Persona

An engineer or AI agent adding a new test file to a Vitest-configured project — needs to learn
immediately, not months later via an empirical revert, that a new test file's path doesn't match
any configured project's `include` glob and therefore provides zero protection.

## User Story

As an engineer or AI agent adding a new test file to a Vitest-configured project, I want an
automated check that fails when my test file's path doesn't match any configured project's
`include` glob, so that I learn immediately (not months later via an empirical revert) that my test
provides zero protection.

## Product Scope

Covers every `apps/*`/`libs/*` project with a `vitest.config.ts` (or other test-runner config
exposing named `include` globs); does not cover test **content** correctness, only path-to-glob
coverage.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Vitest glob-coverage guard

  Scenario: A new test file lands outside every configured project's include glob
    Given a Vitest-configured project with one or more named "projects" entries
    And a new "*.test.{ts,tsx}" file is added under that project's source tree
    When the file's path matches no configured project's "include" glob
    Then the guard fails with the file path and the reason (glob mismatch)

  Scenario: A test file matches an existing project's include glob
    Given a Vitest-configured project with one or more named "projects" entries
    And a test file whose path matches at least one configured project's "include" glob
    When the guard runs
    Then the guard passes with no findings for that file
```

## Non-Goals

- Does not re-litigate the specific `unit-fe` glob fix already merged in
  `ayokoding-www-tools-ai-benchmark`'s PR #122.
- Does not change test content or assertions — only detects glob-coverage gaps.
