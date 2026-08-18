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

- **`rhino-cli specs coverage`**: Enforces spec-to-test mapping for CLI apps. Integrated into `test:quick`. Violations cause CI to fail.
- **Nx cache inputs**: `test:unit` and `test:quick` targets for API backends declare the project's Gherkin specs as inputs, so Nx invalidates cached results when Gherkin specs change.
- **Contract codegen target**: Generates types from the OpenAPI spec. Declared as a dependency of `typecheck` and `build`, so stale contracts are caught in CI before merge.
- **`repo-rules-checker`**: Validates that specs folders exist for apps that require them. Flags missing or misnamed spec folders.
