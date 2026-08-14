---
title: "Tools and Automation"
description: "The agents and checks that enforce feature-change completeness."
category: explanation
subcategory: development
tags:
  - feature-completeness
  - specs
  - contracts
  - testing
  - documentation
  - quality
created: 2026-04-04
when_to_use: "Use when locating the automated check for a feature-completeness violation."
---

# Tools and Automation

- **`rhino-cli specs coverage`**: Enforces Gherkin spec-to-test mapping. Integrated into `test:quick`.
- **`codegen` Nx target**: Generates types from OpenAPI specs. Stale contracts cause `typecheck` to fail.
- **Coverage thresholds**: The native `test:coverage` Nx target enforces minimum line coverage per project.
- **Nx cache inputs**: Gherkin specs are declared as inputs for test targets, invalidating caches when specs change.
- **`repo-rules-checker`**: Validates that specs folders exist for apps that require them.
