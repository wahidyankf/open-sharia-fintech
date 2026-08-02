# Product Requirements — Database Internals Course Ruff Configuration

## Product Overview

The course receives local formatter configuration so its runnable Python examples can be checked by
Ruff without rewriting annotation-heavy source into a less readable form.

## Personas

- A course author maintaining runnable examples.
- A validation agent running formatter checks before a content delivery.

## User Stories

- As a course author, I want the database-internals examples to use a course-local line-length policy
  so that formatting preserves their explanatory annotations.
- As a validation agent, I want one deterministic Ruff command for the course so that formatter
  conformance is verifiable without changing source files.

## Acceptance Criteria

```gherkin
Feature: Database internals formatter configuration

  Scenario: Ruff accepts the course configuration
    Given the database-internals course has its scoped ruff.toml
    When Ruff checks formatting for the course Python corpus
    Then the command exits successfully without rewriting a source file

  Scenario: Formatter scope remains local
    Given the configuration change is staged for review
    When the changed paths are inspected
    Then no manifest, route, or unrelated course file is included
```

## Product Scope

**In scope**: one scoped formatter configuration and its deterministic verification command.

**Out of scope**: new learner-visible capability, a UI change, source-code edits, or a shared Ruff
configuration.

## Product Risks

The configuration can be ineffective if its directory does not cover every target Python file. The
technical approach verifies the whole course tree, including capstone and drill code, rather than a
single representative file.
