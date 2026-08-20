---
title: "Level 1: Unit Tests (`test:unit`)"
description: "Unit test scope and isolation."
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
when_to_use: "Use when writing a unit test."
---

# Level 1: Unit Tests (`test:unit`)

**Purpose**: Verify business logic in complete isolation.

| Aspect            | Rule                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dependencies      | **All mocked, with one documented carve-out** — no real database, no real HTTP, no mutable filesystem; a bounded set of `apps/rhino-cli/tests/*.rs` binaries read the **real repository tree, read-only**, to validate registry/config content that only exists in this repo (e.g. `repo_config_validate.rs`'s `vendored_skill_dirs()` reading `.agents/skills/`, or `cargo_target_share.rs`/`cli_smoke.rs` reading `project.json`) — never a mock for those, because the thing under test is the real file |
| Gherkin specs     | **Must consume** shared specs from the project's `specs/apps/<app-name>/` directory                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Database          | Mocked repositories / in-memory stores                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| HTTP layer        | None — call service functions directly                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| External services | None                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Coverage          | Measured here (>=90% line coverage via `rhino-cli`)                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Nx caching        | `cache: true` (deterministic)                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Nx inputs         | Source files + `generated-contracts/**/*` + Gherkin specs                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Runs in           | `test:quick` (pre-push gate) — for `rhino-cli`, via `test:unit`'s explicit `--test <name>` enumeration of every `tests/*.rs` binary; see [Per-Backend and CLI App Implementation Patterns](./per-backend-and-cli-app-implementation-patterns.md)                                                                                                                                                                                                                                                            |

**Architecture**: Step definitions call service/handler functions directly, injecting mocked repository implementations. No HTTP framework, no routing, no serialization.

```
Gherkin Step -> Service Function -> Mocked Repository
```

**Unit tests may also include non-BDD tests** for logic not covered by Gherkin specs — pure functions, validation helpers, algorithmic logic, error edge cases. However, unit tests must NOT duplicate scenarios already covered by the Gherkin specs. The rule: if a Gherkin scenario tests it, the unit test should not re-test the same behavior.

**Example** (conceptual):

```
Given a user "alice" exists
  -> service.createUser(mockRepo, userData)

When I create a product with name "Widget"
  -> service.createProduct(mockRepo, productData)

Then the product should be created successfully
  -> assert(result.isSuccess)
```
