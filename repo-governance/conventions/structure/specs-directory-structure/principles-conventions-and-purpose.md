---
title: "Specs Directory Structure: Principles, Conventions, and Purpose"
description: The core principles and sibling conventions this directory-structure convention implements, and why the canonical C4-aware layout exists
when_to_use: Read this when you need the rationale behind the specs/ directory layout or which sibling conventions it implements.
category: explanation
subcategory: conventions
tags:
  - conventions
  - specs
  - gherkin
  - directory-structure
  - organization
  - c4-diagrams
  - openapi
  - c4
created: 2026-04-02
---

# Principles, Conventions, and Purpose

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: The directory structure communicates spec scope through path segments. Reading a path like `specs/apps/organiclever/be/behaviors/expenses/expense-management.feature` immediately reveals the project, C4 level, layer, domain, and feature without any external metadata.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Every surface (BE, web, CLI) uses domain subdirectories under `gherkin/`. Single-feature domains are permitted for CLI surfaces with a small command surface area — the domain name still communicates the command group without requiring multiple files.

- **[Documentation First](../../../principles/content/documentation-first.md)**: The specs directory serves as living documentation of system behavior. Gherkin features describe what the system does in human-readable language, C4 diagrams describe architectural context at three zoom levels, and OpenAPI contracts describe API surfaces.

## Conventions Implemented/Respected

This convention implements/respects the following conventions:

- **[App README vs Specs Convention](../app-readme-vs-specs.md)**: This directory structure is the canonical layout produced by applying the Content Split Rule from that convention. The five-folder tree IS the spec tree shape described there.

- **[Specs-Application Sync Convention](../../../development/quality/specs-application-sync.md)**: The directory structure enables bidirectional sync between specs and application code. The path pattern mirrors the app/lib structure in the workspace.

- **[BDD Spec-Test Mapping](../../../development/infra/bdd-spec-test-mapping.md)**: The Gherkin directory structure directly supports the mapping between feature files and test implementations across all three testing levels.

- **[Three-Level Testing Standard](../../../development/quality/three-level-testing-standard.md)**: All three test levels (unit, integration, E2E) consume the same Gherkin specs from this directory structure. Only step implementations differ.

## Purpose

This convention establishes the canonical directory layout for the `specs/` directory. It defines how Gherkin feature files, C4 architecture diagrams, DDD artifacts, and OpenAPI contracts are organized across apps and libs, ensuring consistency, discoverability, and correct tool integration. The layout uses a C4-aware five-folder tree at the app level that maps directly to the C4 model zoom levels, with a `product/` folder for PM-first content and a `behavior/` folder for Gherkin that cuts across all C4 levels.
