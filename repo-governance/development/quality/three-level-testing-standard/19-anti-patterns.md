---
title: "Anti-Patterns"
description: "Testing anti-patterns to avoid."
category: explanation
subcategory: development
tags:
  - testing
  - unit-tests
  - integration-tests
  - e2e-tests
  - bdd
  - gherkin
created: 2026-03-13
when_to_use: "Use when reviewing a test for anti-patterns."
---

# Anti-Patterns

- **Using HTTP simulation in integration tests**: MockMvc, TestClient, httptest, ConnTest, WebApplicationFactory, fetch, clj-http, Router.oneshot, and similar are all HTTP dispatch mechanisms. Integration tests must bypass the HTTP layer entirely.
- **Using in-memory repositories in integration tests**: The purpose of integration tests is to verify real database behavior. In-memory repositories defeat this purpose.
- **Not consuming Gherkin specs at any level**: Every level must run the shared Gherkin scenarios. A test level that only runs non-BDD tests violates the standard.
- **Measuring coverage at integration or E2E levels**: Coverage is measured only at the unit level. Integration and E2E tests verify correctness at different boundaries, not code coverage.
- **Filtering out BDD tests from unit test runs**: Unit tests must include BDD step definitions that consume Gherkin specs (e.g., `--filter Category=Unit` must not exclude BDD scenarios).
- **Duplicating feature-level tests in unit tests**: Unit tests should consume the shared Gherkin specs via BDD step definitions, not duplicate the same scenarios as non-BDD test methods.
