---
title: "OpenAPI Contract-First Development"
description: "Spec-first API development — the OpenAPI YAML is the single source of truth; code is generated from it, not the reverse"
when_to_use: "Read this index to find the right OpenAPI Contract-First Development child document."
---

# OpenAPI Contract-First Development

- [Principles and Conventions](./01-principles-and-conventions.md) — The core principles and conventions this pattern implements - explicitness, reproducibility, automation, simplicity, and the backend hexagonal-architecture layering. Use when you need to trace an OpenAPI contract-first rule back to the principle or convention it implements.
- [Overview and Spec Location](./02-overview-and-spec-location.md) — How contract-first codegen works end to end, and where each backend app's OpenAPI spec file lives. Use when locating the OpenAPI spec file for a given backend app, or explaining the contract-first workflow.
- [Codegen Tooling and Nx Targets](./03-codegen-tooling-and-nx-targets.md) — Which codegen tool runs for each app, and the Nx targets that invoke codegen and spec linting. Use when running codegen for an app or looking up which tool generates its client/server types.
- [Drift Enforcement, Scope, and Related](./04-drift-enforcement-scope-and-related.md) — How CI fails the build on spec/codegen drift, which BE-client pairs participate in contract-first development, and related pattern documentation. Use when a CI drift check fails, or checking whether a given app participates in contract-first codegen.
