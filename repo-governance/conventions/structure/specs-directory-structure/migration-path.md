---
title: "Migration Path (Flat-Root to C4-Aware)"
description: The atomic-commit procedure and path mapping for migrating an existing flat-root spec tree to the canonical C4-aware five-folder layout
when_to_use: Read this when migrating an app's specs/apps/<app-family>/ tree from a legacy flat-root layout to the C4-aware structure.
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

# Migration Path (Flat-Root to C4-Aware)

For existing spec trees with a flat-root layout (`be/`, `web/`, `cli/`, `c4/`, `contracts/` at the `specs/apps/<app-family>/` root):

1. Create the five top-level folders with placeholder `README.md` files.
2. In ONE atomic commit: `git mv` all old subfolders to their new positions. Update ALL path references in the same commit — rhino-cli path constants, Nx `project.json` `inputs`, step definition files, governance cross-links.
3. Update `specs/apps/<app-family>/README.md` to reflect the new tree.
4. Verify with `rhino-cli specs validate-tree <app>` and `npm run lint:md`.

**Flat-root to C4-aware path mapping:**

| Old path                               | New path                                           |
| -------------------------------------- | -------------------------------------------------- |
| `specs/apps/<app>/be/gherkin/`         | `specs/apps/<app>/behavior/<product>-be/gherkin/`  |
| `specs/apps/<app>/web/gherkin/`        | `specs/apps/<app>/behavior/<product>-web/gherkin/` |
| `specs/apps/<app>/cli/gherkin/`        | `specs/apps/<app>/behavior/<product>-cli/gherkin/` |
| `specs/apps/<app>/c4/context.md`       | `specs/apps/<app>/system-context/context.md`       |
| `specs/apps/<app>/c4/container.md`     | `specs/apps/<app>/containers/container.md`         |
| `specs/apps/<app>/c4/component-be.md`  | `specs/apps/<app>/components/be/component-be.md`   |
| `specs/apps/<app>/c4/component-web.md` | `specs/apps/<app>/components/web/component-web.md` |
| `specs/apps/<app>/contracts/`          | `specs/apps/<app>/containers/contracts/`           |

The atomic commit is mandatory — splitting the move and the path updates causes test failures between commits.

**CLI-flat exception retired (2026-05-23)**: every CLI surface then in the workspace
regrouped under `behavior/<product>-cli/gherkin/<domain>/` during the `specs-tree-uniform`
pass. `rhino-cli specs validate-tree` now enforces domain subdirs for every surface.

**CLI domain-subdir moves (2026-05-23)**. As part of the `specs-tree-uniform` plan, the CLI
apps then in the workspace completed migration to the universal domain-subdir layout, then renamed
to `<product>-<surface>` during the `standardize-app-spec-trees` plan (2026-06-11):

- `crane` — regrouped into domain subdirs (`pdf/`, `content/`, `media/`, `reporting/`,
  `system/`); bare `cli/` renamed to `crane-cli/`.
- `rhino` — regrouped into domain subdirs (`agents/`, `system/`, `env/`, `git/`,
  `docs/`, `spec-coverage/`, `repo-governance/`, `workflows/`); bare `cli/` renamed to
  `rhino-cli/`.

The bare `build-tools` surface was renamed to `ayokoding-build-tools` during the
`standardize-app-spec-trees` plan to follow `<product>-<surface>` naming; it remains an active
surface.
