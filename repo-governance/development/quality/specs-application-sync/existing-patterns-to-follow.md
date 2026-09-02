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

`specs/apps/organiclever/` carries one [logical owner corpus](../../../conventions/structure/specs-directory-structure/logical-owner-corpus.md) per surface OrganicLever deploys:

- `specs/apps/organiclever/be/` — the F# backend: `architecture.md`, `behaviors/`, and `contracts/`, the OpenAPI 3.1 spec the backend serves and the app frontend consumes
- `specs/apps/organiclever/app-web/` — the authenticated application frontend
- `specs/apps/organiclever/www/` — the marketing site, whose `behaviors/` splits into `frontend/` and `backend/` because one deployed site owns both

The contract sits inside `be/` rather than in a shared folder because the backend is what serves it. When a new endpoint is added to the OpenAPI spec in `organiclever-contracts`, the backend corpus gains both the scenarios and the `architecture.md` component in the same delivery unit.

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
