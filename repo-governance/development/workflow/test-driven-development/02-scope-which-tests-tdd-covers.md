---
title: "Scope: Which Tests TDD Covers"
description: The ten verification levels TDD applies to, from unit tests through security testing, and the rule for each.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use when deciding which test level (unit, integration, E2E, contract, etc.) a behavior's first failing test belongs at.
---

# Scope: Which Tests TDD Covers

TDD applies to **every level of automated and manual verification** that backs a behavioral
guarantee. Pick the level that best captures the behavior under change and write the failing
test there first. A single feature often spans multiple levels — write each level's first
failing test before the implementation for that level lands.

| Test level                       | What it covers                                                       | Tooling examples                                                             |
| -------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Unit**                         | A single function, class, or module in isolation; deps mocked        | Vitest, Go `testing` + Godog, JUnit, ExUnit, xUnit, Pytest, Hspec            |
| **Integration**                  | Real boundaries inside one process or one service                    | MSW, Godog with `//go:build integration`, real PostgreSQL via docker-compose |
| **E2E (UI + API)**               | Real HTTP, real browser, end-to-end flow across services             | Playwright (UI), Playwright API tests (HTTP), Pact-style contract checks     |
| **Contract**                     | API contracts (OpenAPI, Pact) — request/response shape and semantics | OpenAPI spec lint, codegen drift checks, contract round-trip tests           |
| **Property / fuzz**              | Invariants over generated inputs, not handwritten cases              | fast-check (TS), gopter (Go), QuickCheck-family in F#/Elixir/Rust            |
| **Snapshot / visual regression** | Stable rendered output (UI, generated docs)                          | Vitest snapshots, Playwright visual diff                                     |
| **Manual verification**          | Human-driven behavioral check that cannot or should not be automated | Playwright MCP browser session, `curl` for API, Storybook walkthrough        |
| **Performance / load**           | Latency, throughput, resource usage budgets                          | k6, Lighthouse CI, `nx run [project]:bench` targets                          |
| **Accessibility (a11y)**         | WCAG AA conformance, semantic HTML, focus order                      | axe, Storybook a11y addon, Playwright a11y assertions                        |
| **Security**                     | Authn/authz boundaries, input validation, OWASP-class regressions    | Targeted unit/integration tests, fuzz harnesses, security-focused E2E        |

**TDD rule for every level above**: write the failing check first, watch it fail for the
right reason, then implement to make it pass, then refactor.
