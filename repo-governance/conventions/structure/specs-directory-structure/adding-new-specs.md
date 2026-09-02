---
title: "Adding New Specs"
description: Step-by-step procedures for adding a feature file to an existing project, scaffolding specs for a brand-new project, or scaffolding specs for a new library
when_to_use: Read this when adding a Gherkin feature file, onboarding a new app's specs, or onboarding a new library's specs.
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

# Adding New Specs

## Adding a Feature File to an Existing Project

1. Identify the correct `<product>-<surface>` slug (e.g., `organiclever-be`, `ayokoding-www`,
   `rhino-cli`). For ayokoding build-time features, use `ayokoding-build-tools`
2. Place the file in the appropriate domain subdirectory under
   `<owner>/behaviors/<domain>/`, creating the domain folder if it does not exist
3. For CLI: choose a domain that matches the command group (e.g., `system/`, `env/`, `links/`); single-feature domains are permitted
4. Update the relevant `README.md` index file

## Adding Specs for a New Project

1. Create the project directory under `specs/apps/<app-family>/`
2. Create `README.md` at the project level
3. Determine the surface profile (full-stack, web-only, CLI-only, multi-CLI)
4. Create only the folders the project needs — see per-surface variant table
5. Create `README.md` index files at each folder level
6. Run `rhino-cli specs validate-tree <app>` to verify the layout

## Adding Specs for a New Lib

1. Create `specs/libs/<lib-name>/`
2. Create `README.md` at the lib level
3. Create `behaviors/` directly under the lib name, beside its `README.md` and `architecture.md`
4. Create package subdirectories under `gherkin/` matching the lib's module structure
