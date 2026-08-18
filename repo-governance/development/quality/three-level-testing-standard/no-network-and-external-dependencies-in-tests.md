---
title: "No Network in Integration Tests, External Dependencies Optional in E2E"
description: "Network/dependency rules for integration vs. E2E."
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
when_to_use: "Use when a test needs an external dependency."
---

# No Network in Integration Tests, External Dependencies Optional in E2E

## No Network in Integration Tests

Integration tests must not make inbound or outbound network calls. This constraint applies across all project types:

- **API backends**: The test harness calls service/repository functions directly. No HTTP server starts. No HTTP client library is used. The only real external dependency is the PostgreSQL database.
- **Content platforms & marketing FE**: Integration tests do not apply (N/A per "Mandatory Test Levels Matrix"); `test:integration` is a no-op `echo`. The Gherkin contract is consumed at the unit tier (mocked dependencies) and the e2e tier.
- **CLI apps**: Integration tests drive commands via `cmd.RunE()` in-process. No network calls. The only real dependency is the local filesystem (via `/tmp` fixtures).
- **Product app-web (app-tier)**: Integration tests use MSW (Mock Service Worker) or equivalent in-process mocking of the backend API. No real HTTP servers start and no real network calls are made.
- **Libraries**: When integration tests apply, they use real filesystem or in-process fixtures. No network calls.

The principle: integration tests introduce exactly one real dependency per project type (database for backends, filesystem for CLI apps, in-process backend mocking for product app-web). Everything else remains mocked.

## External Dependencies Optional in E2E

E2E tests require real HTTP and a real database. External service dependencies (payment gateways, email providers, SMS services, third-party APIs) are optional at the E2E level and may be mocked:

- The core E2E requirement is real HTTP requests via Playwright against a running server backed by a real database
- External services that are expensive, slow, or environment-dependent may be replaced with test doubles at the E2E level
- When external services are mocked in E2E, the mock boundary must be documented in the test setup so future contributors understand what is real and what is not
