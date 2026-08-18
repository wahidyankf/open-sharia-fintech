---
title: "Picking the right level"
description: How to pick the cheapest test level that meaningfully exercises a behavior, and why coverage should not duplicate across levels.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use when unsure which test level a bug or behavior belongs at.
---

# Picking the right level

When in doubt, prefer the cheapest test that meaningfully exercises the behavior:

- A pure function bug → unit test (fastest feedback, deterministic).
- A database query bug → integration test (real DB via docker-compose for `organiclever-be`,
  in-process mocks otherwise).
- A user-visible flow bug → E2E (Playwright) plus manual verification before merge.
- A contract change → contract test on the OpenAPI spec round-trip; both producer and
  consumer get failing tests first.

Do not duplicate coverage across levels for the same behavior. One TDD-shaped check per
behavior, at the right level, plus higher-level smoke coverage where flows cross boundaries.
