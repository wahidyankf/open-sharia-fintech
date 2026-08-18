---
title: "Coverage Enforcement and Threshold Rationale"
description: "How and why coverage is enforced."
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
when_to_use: "Use when a coverage gate fails or its threshold is questioned."
---

# Coverage Enforcement and Threshold Rationale

## Coverage Enforcement

Coverage is enforced at three gates:

- **Pre-push hook** — `test:quick` runs `test:unit` + native `test:coverage` before every push
- **PR quality gate** — same `test:quick` pipeline runs on every pull request in CI

`test:quick` is defined as `test:unit` followed immediately by `test:coverage` (native per-project coverage gate). The threshold is project-specific (see "Coverage Threshold Rationale" below).

Coverage is measured **only at the unit level**. Integration tests (`test:integration`) and E2E tests (`test:e2e`) do not measure coverage. Their purpose is correctness at different isolation boundaries, not code coverage.

## Coverage Threshold Rationale

Different project types carry different coverage thresholds, reflecting the practical testability of each category:

| Threshold | Projects                                                   | Rationale                                                                                           |
| --------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 90%       | API backends (`organiclever-be`), Rust CLI apps, Rust libs | Core business logic with high mock isolation; all execution paths reachable in unit tests           |
| 80%       | Content platforms (`ayokoding-www`, `ose-www`)             | Significant UI rendering code; some React rendering paths are hard to unit-test                     |
| 70%       | FE apps (`organiclever-app-web`)                           | API/auth/query layers are fully mocked by design; threshold reflects intentional mocking boundaries |
