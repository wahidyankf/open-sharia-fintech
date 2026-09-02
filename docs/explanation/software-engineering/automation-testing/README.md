---
title: Automation Testing
description: Why and where automated checks build confidence in open-sharia-enterprise
category: explanation
subcategory: software-engineering
tags:
  - automation-testing
  - testing
  - quality
  - index
principles:
  - automation-over-manual
  - explicit-over-implicit
  - reproducibility
created: 2026-02-08
---

# Automation Testing

Automated tests turn an expected product behavior into a repeatable check. They help a product person see whether a promise is protected, and help an engineer change code without relying on memory or a lucky manual click-through.

This section explains the testing tools and patterns used in this repository. It is context, not a substitute for the test targets listed in an application's README or the repository quality rules.

## Start with the question

| If you need to understand…                                      | Start here                                                                                            |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| How browser journeys are automated                              | [Playwright](./tools/playwright/README.md)                                                            |
| Which automation tool pages exist                               | [Testing tools](./tools/README.md) — Find the automation tool guidance used by open-sharia-enterprise |
| How automated checks fit alongside unit and integration testing | [Software Development Practices](../development/README.md)                                            |
| The repository's required quality gates                         | [Code quality](../../../../repo-governance/development/quality/code.md)                               |

## What automated browser checks are for

Browser and end-to-end tests are most valuable when they protect a user-visible path: a page opens, a form can be completed, a saved decision appears where expected, or an integration handles a failure clearly. They complement lower-level tests; they do not need to repeat every unit-level decision.

The repository uses Playwright for browser automation. Individual apps own their test projects and commands, so use the app README to find the correct command for the product area you are working on.

## Keep the learning path practical

If you are new to automated testing, start with a small behavior that a reader or user can observe. Describe the intended outcome in plain language, find the existing test boundary, and then use the detailed Playwright guidance when you need selectors, fixtures, traces, or debugging techniques.

For the test-first practices that connect product examples to implementation, see [Behavior-Driven Development](../development/behavior-driven-development-bdd/README.md) and [Test-Driven Development](../development/test-driven-development-tdd/README.md).

## Related reading

- [Software Engineering](../README.md) — the wider engineering map.
- [Automation Testing Tools](./tools/README.md) — Find the automation tool guidance used by open-sharia-enterprise
- [Code quality](../../../../repo-governance/development/quality/code.md) — repository-level quality rules.
