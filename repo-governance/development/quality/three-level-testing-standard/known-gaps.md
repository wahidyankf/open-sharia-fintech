---
title: "Known Gaps"
description: "Known testing gaps."
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
when_to_use: "Use to check if a gap is already known."
---

# Known Gaps

The following gaps are known and tracked for future resolution:

- **FE unit tests lack Gherkin**: `organiclever-app-web` does not yet consume Gherkin specs at the unit level. A BDD runner compatible with Vitest-based unit tests needs to be selected.
- **Content platform Gherkin pending**: `ayokoding-www` and `ose-www` do not yet consume Gherkin specs at any test level. Gherkin consumption for content platforms is planned at the **unit + e2e** tiers (content platforms have no integration tier; `test:integration` is a no-op `echo`).
- **specs:coverage deferred for some projects**: Some projects have `specs:coverage` temporarily deferred until step implementations are complete. See "Spec-Coverage Validation" above and [Nx Target Standards](../infra/nx-targets.md) for the deferred project list.
