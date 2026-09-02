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

- **`<app-family>`** = project name (e.g., `ose`)
- **`<product>-<surface>`** = flat slug combining product name and perspective (e.g.,
  `ose-be`, `ose-app-web`)
- **`{domain}`** = business domain grouping folder (all surfaces, including CLI)
- **`{feature}`** = feature file name in kebab-case

Deprecated slugs (bare `be`, `web`, `cli`, `api`) must not be used for new surfaces; use the
`<product>-<surface>` compound form instead.

### Domain Subdirectory Rules

**Every surface** (BE, web, CLI) uses domain subdirectories — under `gherkin/` in the legacy tree, under `behaviors/` in a [logical owner corpus](./logical-owner-corpus.md). Each domain folder groups related feature files by business domain or command group, not by technical concern. Single-feature domains are permitted when the surface area is small.

```
specs/apps/organiclever/be/behaviors/journal/journal-entries.feature
specs/apps/organiclever/be/behaviors/health/health.feature
specs/apps/organiclever/app-web/behaviors/settings/dark-mode.feature
specs/apps/organiclever/www/behaviors/frontend/home/home.feature
```

AyoKoding's build-time features once sat in their own `ayokoding-build-tools/` surface here. They
now live at `specs/apps/ayokoding/www/behaviors/build-tools/`, inside a
[logical owner corpus](./logical-owner-corpus.md), because they belong to the site they build.

A domain folder may contain one or many feature files.

**CLI specs** use the same domain subdirectory rule as BE and web. Group features by command domain (e.g., `system/`, `env/`, `links/`). Single-feature domains are fine when the CLI surface area is small:

```
specs/apps/rhino/cli/behaviors/system/doctor.feature
specs/apps/rhino/cli/behaviors/env/env-backup.feature
specs/apps/rhino/cli/behaviors/spec-coverage/spec-coverage-validate.feature
specs/apps/crane/cli/behaviors/pdf/pdf-commands.feature
```

`rhino-cli specs validate-tree` enforces this rule: a `.feature` file placed directly under `behavior/<product>-<surface>/gherkin/` (with no domain subdirectory) is a HIGH finding. The four examples above sit in [logical owner corpora](./logical-owner-corpus.md), which keep the same domain subdirectory under `behaviors/`.

## Lib Spec Structure

A library owns exactly one surface, so it has no product directory to separate. The three
[logical owner corpus](./logical-owner-corpus.md) entries therefore sit directly under the library
root:

```
specs/libs/<lib-name>/
├── README.md
├── architecture.md          # the current, as-built library
└── behaviors/
    └── <domain>/            # domain, package, or component subdirectories
        └── <feature>.feature
```

**Examples:**

```
specs/libs/web-ui-token/behaviors/tokens/tokens-export.feature
specs/libs/ts-env-loader/behaviors/env-loader/env-loader.feature
```
