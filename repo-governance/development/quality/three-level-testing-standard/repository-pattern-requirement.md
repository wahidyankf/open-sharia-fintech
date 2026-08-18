---
title: "Repository Pattern Requirement"
description: "Persistence must go through a repository interface."
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
when_to_use: "Use when adding data access code."
---

# Repository Pattern Requirement

API backends must implement the repository pattern as the isolation boundary between test levels.

- **Unit tests**: Inject mocked repository implementations into service functions. Service logic is tested without touching the database.
- **Integration tests**: Inject real repository implementations backed by PostgreSQL. The same service layer code runs with a different repository implementation.

This means the service layer is the same code at both levels — only the repository implementation changes. Any divergence between unit and integration test behavior indicates a bug in either the mock or the real repository implementation.

```
Unit:        Service -> MockRepository (in-memory)
Integration: Service -> RealRepository -> PostgreSQL
```
