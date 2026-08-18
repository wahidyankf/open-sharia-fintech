---
title: "Gherkin Feature File Placement and Lib Spec Structure"
description: The canonical path pattern and domain-subdirectory rules for placing .feature files under behavior/, plus the simpler layout used for library specs
when_to_use: Read this when adding or locating a Gherkin .feature file for an app or a library.
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

# Gherkin Feature File Placement, and Lib Spec Structure

## Gherkin Feature File Placement

Gherkin feature files live inside the `behavior/` tree at `specs/apps/<app-family>/behavior/<product>-<surface>/gherkin/`.

### Canonical Path Pattern

```
specs/apps/<app-family>/behavior/<product>-<surface>/gherkin/{domain}/{feature}.feature
```

Where:

- **`<app-family>`** = project name (e.g., `organiclever`, `ayokoding`, `rhino`)
- **`<product>-<surface>`** = flat slug combining product name and perspective (e.g.,
  `organiclever-be`, `ayokoding-www`, `rhino-cli`, `ayokoding-build-tools`)
- **`{domain}`** = business domain grouping folder (all surfaces, including CLI)
- **`{feature}`** = feature file name in kebab-case

Deprecated slugs (bare `be`, `web`, `cli`, `api`) must not be used for new surfaces; use the
`<product>-<surface>` compound form instead.

### Domain Subdirectory Rules

**Every surface** (BE, web, CLI) uses domain subdirectories under `gherkin/`. Each domain folder groups related feature files by business domain or command group, not by technical concern. Single-feature domains are permitted when the surface area is small.

Build-time features for `ayokoding` live under their own surface `ayokoding-build-tools/` —
renamed from the old bare `build-tools/` slug during the `standardize-app-spec-trees` plan.

```
specs/apps/organiclever/behavior/organiclever-be/gherkin/expenses/expense-management.feature
specs/apps/organiclever/behavior/organiclever-be/gherkin/authentication/password-login.feature
specs/apps/organiclever/behavior/organiclever-app-web/gherkin/authentication/google-login.feature
specs/apps/ayokoding/behavior/ayokoding-www/gherkin/accessibility/accessibility.feature
```

A domain folder may contain one or many feature files.

**CLI specs** use the same domain subdirectory rule as BE and web. Group features by command domain (e.g., `system/`, `env/`, `links/`). Single-feature domains are fine when the CLI surface area is small:

```
specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature
specs/apps/rhino/behavior/rhino-cli/gherkin/env/env-backup.feature
specs/apps/rhino/behavior/rhino-cli/gherkin/spec-coverage/spec-coverage-validate.feature
specs/apps/crane/behavior/crane-cli/gherkin/pdf/pdf-commands.feature
```

`rhino-cli specs validate-tree` enforces this rule: a `.feature` file placed directly under `behavior/<product>-<surface>/gherkin/` (with no domain subdirectory) is a HIGH finding.

## Lib Spec Structure

Library specs use a simpler layout with no five-folder tree — libs do not have C4 levels or behavioral architecture in the same sense as deployed apps.

```
specs/libs/<lib-name>/
├── README.md
└── behavior/
    └── gherkin/
        └── <package>/       # Package or module subdirectories
            └── <feature>.feature
```

**Examples:**

```
specs/libs/web-ui-token/behavior/gherkin/tokens/tokens-export.feature
specs/libs/ts-env-loader/behavior/gherkin/env-loader/env-loader.feature
```
