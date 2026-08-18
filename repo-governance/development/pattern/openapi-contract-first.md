---
title: OpenAPI Contract-First Development
description: Spec-first API development — the OpenAPI YAML is the single source of truth; code is generated from it, not the reverse
category: explanation
subcategory: development
tags:
  - openapi
  - contract-first
  - codegen
  - api
  - drift-enforcement
created: 2026-05-26
when_to_use: "Use when adding or changing an API endpoint, running codegen, or debugging a CI spec/codegen drift failure."
---

# OpenAPI Contract-First Development

Contract-first development means the OpenAPI YAML specification is written before any implementation code.
The spec is the single source of truth for every API contract. Generated code follows from the spec; the
spec never follows from the code.

## Contents

- [Principles and Conventions](./openapi-contract-first/principles-and-conventions.md) — The core principles and conventions this pattern implements - explicitness, reproducibility, automation, simplicity, and the backend hexagonal-architecture layering. Use when you need to trace an OpenAPI contract-first rule back to the principle or convention it implements.
- [Overview and Spec Location](./openapi-contract-first/overview-and-spec-location.md) — How contract-first codegen works end to end, and where each backend app's OpenAPI spec file lives. Use when locating the OpenAPI spec file for a given backend app, or explaining the contract-first workflow.
- [Codegen Tooling and Nx Targets](./openapi-contract-first/codegen-tooling-and-nx-targets.md) — Which codegen tool runs for each app, and the Nx targets that invoke codegen and spec linting. Use when running codegen for an app or looking up which tool generates its client/server types.
- [Drift Enforcement, Scope, and Related](./openapi-contract-first/drift-enforcement-scope-and-related.md) — How CI fails the build on spec/codegen drift, which BE-client pairs participate in contract-first development, and related pattern documentation. Use when a CI drift check fails, or checking whether a given app participates in contract-first codegen.
