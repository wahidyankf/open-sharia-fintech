---
title: "Nx Testing Targets and Boundaries"
description: "Runtime, static coverage, and Unit/Integration/E2E boundary definitions"
category: explanation
subcategory: development
tags: [ci-cd, nx, testing]
created: 2026-03-31
when_to_use: "Use when classifying a test or selecting its canonical target."
---

# Nx Testing Targets and Boundaries

| Target             | Contract                                                                                      |
| ------------------ | --------------------------------------------------------------------------------------------- |
| `test:unit`        | Execute in-process tests with every OS-facing dependency injected                             |
| `test:integration` | Execute real isolated local-resource tests with no external network                           |
| `test:e2e`         | Execute journeys through a real public browser, HTTP, or process boundary                     |
| `test:coverage:*`  | Statically validate test/corpus coverage; never execute tests                                 |
| `test:coverage`    | Aggregate all applicable static coverage validators                                           |
| `test:quick`       | Run types/lint, Unit runtime where applicable, and every applicable static coverage validator |

Setup and assertions count when classifying a test. Integration may own a loopback socket only
when `repo-config.yml` allowlists the project; external network is always forbidden. E2E requires public-boundary observation, not merely permission to use
network. See the [BDD standard](../../behaviour-driven-development.md) for full boundaries,
applicability, and exemptions.
