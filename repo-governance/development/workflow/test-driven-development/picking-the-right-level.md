---
title: "Applying the required test layers"
description: How Unit proof and applicable higher-layer adapters participate in TDD.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use when deciding which test adapters an observable behaviour change requires.
---

# Applying the required test layers

Every observable behaviour begins with a failing Unit proof. Add failing Integration and E2E
bindings whenever the project's applicable boundaries can express the scenario:

- Unit isolates the production subject through injected dependencies.
- Integration proves owned local files, databases, processes, environment state, streams, or an
  allowlisted loopback socket the test starts and stops, with no external network reach.
- E2E proves a public browser, HTTP, or process boundary.

An inapplicable project-level adapter is omitted. A scenario-level higher-layer exemption is valid
only for a genuine boundary mismatch and substantive alternative proof. Difficulty, runtime,
flakiness, cost, or unfinished work cannot reduce the required adapters. See the
[BDD standard](../../behaviour-driven-development.md).
