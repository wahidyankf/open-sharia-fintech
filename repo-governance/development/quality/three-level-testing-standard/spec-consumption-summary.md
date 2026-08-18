---
title: "Spec Consumption Summary"
description: "Which level consumes which spec artifact."
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
when_to_use: "Use to check which level consumes a spec."
---

# Spec Consumption Summary

All three levels consume the same shared Gherkin scenarios from the project's `specs/apps/<app-name>/` directory. The difference is HOW the step definitions execute them:

| Level       | Step Implementation                          | What Varies                |
| ----------- | -------------------------------------------- | -------------------------- |
| Unit        | Calls service functions with mocked repos    | Repository implementations |
| Integration | Calls service functions with real PostgreSQL | Database (real vs mock)    |
| E2E         | Sends HTTP requests via Playwright           | Entire stack (HTTP + DB)   |
