---
title: "Existing Patterns to Follow"
description: "Worked spec-organization patterns for organiclever, ayokoding-www, and CLI apps."
category: explanation
subcategory: development
tags:
  - specs
  - architecture
  - c4-diagrams
  - gherkin
  - synchronization
  - quality
created: 2026-03-24
when_to_use: "Use when structuring specs/ for a new app and want an existing pattern to follow."
---

# Existing Patterns to Follow

## organiclever specs

`specs/apps/organiclever/` serves both the backend (`organiclever-be`) and frontend (`organiclever-app-web`) from a shared set of specs:

- `specs/apps/organiclever/system-context/` — C4 L1 context diagram for OrganicLever
- `specs/apps/organiclever/containers/` — C4 L2 container diagram and deployment topology
- `specs/apps/organiclever/components/` — C4 L3 component diagrams (be/, web/)
- `specs/apps/organiclever/behavior/organiclever-be/gherkin/` — Shared Gherkin scenarios consumed by the backend at unit, integration, and E2E levels
- `specs/apps/organiclever/behavior/organiclever-app-web/gherkin/` — Shared Gherkin scenarios consumed by the frontend
- `specs/apps/organiclever/containers/contracts/` — OpenAPI 3.1 contract spec that both backend and frontend implement

When a new endpoint is added to the OpenAPI spec in `organiclever-contracts`, both the corresponding Gherkin scenarios and the C4 component diagram must be updated to reflect the new behavior and component.

## ayokoding-www specs

`specs/apps/ayokoding/www/` is a [logical owner corpus](../../../conventions/structure/specs-directory-structure/logical-owner-corpus.md) for the one site AyoKoding deploys:

- `specs/apps/ayokoding/www/architecture.md` — the as-built C4 view, kept current with the App Router structure and the tRPC routers
- `specs/apps/ayokoding/www/behaviors/backend/` — scenarios for tRPC procedures, consumed by `ayokoding-www-be-e2e`
- `specs/apps/ayokoding/www/behaviors/frontend/` — scenarios for what a learner sees

When a new tRPC router is added to `apps/ayokoding-www/`, `architecture.md` gains the component and `behaviors/backend/` gains the scenarios, in the same delivery unit.

## CLI apps

CLI apps (`rhino-cli`, `crane-cli`) use the automated enforcement path:

- Each Cobra command file maps to a `@tag` in a Gherkin feature file
- `rhino-cli specs coverage` enforces the 1:1 mapping automatically
- Adding a command without a spec causes `test:quick` to fail

See [BDD Spec-to-Test Mapping](../../infra/bdd-spec-test-mapping.md) for the full CLI mapping rules.
