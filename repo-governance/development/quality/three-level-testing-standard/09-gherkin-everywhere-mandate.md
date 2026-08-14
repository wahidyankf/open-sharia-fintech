---
title: "Gherkin-Everywhere Mandate"
description: "Every level consumes Gherkin specs."
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
when_to_use: "Use when a test lacks a Gherkin scenario."
---

# Gherkin-Everywhere Mandate

All testable projects must consume Gherkin specs at **all applicable test levels**. The relationship between unit tests and Gherkin is additive:

- **Unit tests are a superset of Gherkin** — they MUST implement ALL Gherkin scenarios PLUS additional non-Gherkin tests (edge cases, error paths, implementation-specific behavior not captured in feature files)
- **Integration tests stick to Gherkin** — integration step definitions consume the same feature files as unit step definitions; no additional non-BDD tests at this level
- **E2E tests stick to Gherkin** — Playwright step definitions map directly to Gherkin scenarios; no additional non-BDD tests at this level

The Gherkin spec is the shared contract. Unit tests honor it and extend it. Integration and E2E tests honor it exactly. Where a project type has **no integration tier** (content platforms and marketing FE), the **unit** tier is the BDD level that consumes the full Gherkin contract — with all external dependencies mocked — and the **e2e** tier consumes it against the running app; `specs:coverage` is satisfied by the unit-tier step definitions.
