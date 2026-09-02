---
title: "Contract-Driven Development"
description: "API contracts drive test development."
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
when_to_use: "Use when an API contract changes."
---

# Contract-Driven Development

Apps with OpenAPI 3.1 contracts use a `codegen` target to define the API surface:

- **OrganicLever**: OpenAPI 3.1 spec at `specs/apps/organiclever/be/contracts/`; the `codegen` Nx target generates types and encoders/decoders into `generated-contracts/` (gitignored)
- **Content platforms**: Use tRPC, which is typed at compile time without a separate contract file

The `typecheck` and `build` Nx targets depend on `codegen`. This means contract violations surface during `nx affected -t typecheck` and the pre-push `test:quick` gate. Rust and Flutter additionally declare `codegen` as a dependency of `test:unit` because generated code is required at compile time.
