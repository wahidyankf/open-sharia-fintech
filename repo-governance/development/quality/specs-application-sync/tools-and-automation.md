---
title: "Tools and Automation"
description: "The validators and checks that enforce specs-application sync."
category: explanation
subcategory: development
tags:
  - specs
  - architecture
  - c4-diagrams
  - gherkin
  - synchronization
  - quality
created: 2026-03-24
when_to_use: "Use when locating the automated check for a sync violation."
---

# Tools and Automation

- **Project-local `test:coverage:*` targets**: Statically enforce exact-one scenario bindings,
  mandatory Unit proof, applicable Integration/E2E proof or valid exemptions, and rejection of
  deferred scenarios. The aggregate `test:coverage` runs in `test:quick` without executing tests.
- **Nx cache inputs**: `test:unit` and `test:quick` targets for API backends declare the project's Gherkin specs as inputs, so Nx invalidates cached results when Gherkin specs change.
- **Contract codegen target**: Generates types from the OpenAPI spec. Declared as a dependency of `typecheck` and `build`, so stale contracts are caught in CI before merge.
- **`specs:structure-validation`**: Validates that required owner folders and corpus structure
  exist. It is separate from scenario-to-adapter coverage.
- **`rules-checker`**: Audits the surrounding repository rules and documentation for drift.
