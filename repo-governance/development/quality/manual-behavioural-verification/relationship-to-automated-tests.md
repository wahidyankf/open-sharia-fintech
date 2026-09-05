---
title: "Relationship to Automated Tests"
description: "How manual verification relates to automated test coverage."
category: explanation
subcategory: development
tags:
  - verification
  - testing
  - playwright
  - api
  - quality
  - manual-testing
created: 2026-04-04
when_to_use: "Use when deciding whether automated tests already cover manual verification."
---

# Relationship to Automated Tests

Manual verification does **not** replace automated tests. The relationship is complementary:

| Layer                   | What It Catches                                                             | When It Runs                                |
| ----------------------- | --------------------------------------------------------------------------- | ------------------------------------------- |
| **Unit tests**          | Logic errors, edge cases, contract violations                               | On every commit (test:quick)                |
| **Integration tests**   | Cross-component failures, database issues                                   | On demand or CI                             |
| **E2E tests**           | Full-stack flow failures, regression                                        | On demand or CI                             |
| **Manual verification** | Visual regressions, UX issues, integration mismatches, real-world behaviour | After implementation, before declaring done |

A feature is not complete until **both** automated tests pass **and** manual verification confirms the expected behaviour.
