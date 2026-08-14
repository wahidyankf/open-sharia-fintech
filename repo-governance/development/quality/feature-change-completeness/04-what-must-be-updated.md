---
title: "What Must Be Updated"
description: "The full list of artifact types (specs, contracts, tests, docs) a feature change must keep in sync."
category: explanation
subcategory: development
tags:
  - feature-completeness
  - specs
  - contracts
  - testing
  - documentation
  - quality
created: 2026-04-04
when_to_use: "Use when unsure which companion artifact a feature change must also update."
---

# What Must Be Updated

## 1. Specs (Gherkin Feature Files)

**Location**: `specs/apps/*/behavior/organiclever-be/gherkin/`, `specs/apps/*/behavior/organiclever-app-web/gherkin/`, `specs/apps/*/behavior/<product>-cli/gherkin/`, `specs/libs/*/`

**Update when:**

- Adding a new endpoint, procedure, command, or user-facing behavior -- add scenarios
- Modifying request/response shapes, validation rules, or error handling -- update scenarios
- Removing an endpoint, procedure, or command -- remove or archive scenarios
- Changing authentication or authorization requirements -- update scenarios

**Automated enforcement**: `rhino-cli specs coverage` catches missing step definitions. Nx cache inputs include Gherkin specs so stale specs invalidate test caches.

## 2. Contracts (OpenAPI Specs)

**Location**: `specs/apps/*/containers/contracts/`

**Update when:**

- Adding a new REST endpoint -- add path and schema definitions
- Changing request or response shapes -- update schema definitions
- Adding or removing query parameters, headers, or authentication schemes
- Changing status codes or error response formats
- Deprecating or removing an endpoint

**Automated enforcement**: `codegen` targets generate types from contracts. Stale contracts cause `typecheck` to fail because generated types do not match the implementation.

## 3. Tests

**Update when:**

- **Unit tests**: Any logic change requires updated unit tests. Coverage thresholds (90% for backends, 70-80% for frontends) enforce this.
- **Integration tests**: Changes to database interactions, external service calls, or cross-component behavior require updated integration tests.
- **E2E tests**: Changes to user-facing flows, API contracts, or full-stack behavior require updated E2E tests.
- **Accessibility tests**: UI changes require accessibility verification (static analysis via oxlint jsx-a11y plugin, manual WCAG AA checks).

**Automated enforcement**: Coverage thresholds in `test:quick` catch missing unit tests. `specs:coverage` catches missing step definitions.

## 4. Documentation

**Update when:**

- Adding a new feature that users or developers need to know about
- Changing API behavior that is documented in READMEs or docs/
- Adding or removing configuration options
- Changing architectural boundaries (C4 diagrams in specs/)
- Adding or removing dependencies that affect setup instructions

**Manual enforcement**: Documentation updates require human judgment about what is relevant. AI agents should identify documentation that references the changed feature and update it proactively.
