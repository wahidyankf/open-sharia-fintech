---
title: "CI Integration, Principles Traceability, and See Also"
description: "CI integration, principle traceability, and related links."
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
when_to_use: "Use for CI wiring, principle tracing, or related docs."
---

# CI Integration, Principles Traceability, and See Also

## CI Integration

Integration and E2E tests run together in per-service GitHub Actions workflows named "Test {service name}". Each workflow:

1. Starts PostgreSQL via docker-compose
2. Runs integration tests (direct service calls with real DB)
3. Starts the application server
4. Runs E2E tests via Playwright

See [Nx Target Standards](../infra/nx-targets.md) for CI schedule details.

## Principles Traceability

| Decision                                              | Principle                                                                                    |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Three distinct levels with non-overlapping boundaries | [Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md) |
| All levels consume shared Gherkin specs               | [Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md) |
| No HTTP in integration tests                          | [Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)      |
| Coverage measured only at unit level                  | [Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)      |

## See Also

- [Code Coverage Reference](../../../../docs/reference/code-coverage.md) - How coverage is measured (rhino-cli algorithm, per-project tools, exclusion patterns)
