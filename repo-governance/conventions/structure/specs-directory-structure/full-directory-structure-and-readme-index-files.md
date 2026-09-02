---
title: "Full Directory Structure and README Index Files"
description: The complete specs/ tree layout, which subdirectories each project surface profile actually has, and the README.md index-file requirement at every level
when_to_use: Read this when you need the top-level specs/ layout or the rule for which subdirectories a given project should have README.md files in.
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

# Full Directory Structure, and README Index Files

## Full Directory Structure

The complete `specs/` directory follows this layout:

```
specs/
├── README.md
├── apps/
│   └── <app-family>/         # C4-aware five-folder tree (per app above)
└── libs/
    └── <lib-name>/
        ├── README.md
        └── gherkin/
            └── <package>/
                └── <feature>.feature
```

### Which Projects Have Which Directories

Not every project has all directories. Presence of subdirectories depends on the project's surface profile:

- **`containers/contracts/`**: Present for apps with OpenAPI contract specs (e.g., `ose`)
- **`components/be/`**: Present for apps with a backend container (e.g., `ose`)
- **`behavior/<product>-be/gherkin/`**: Present for apps with backend Gherkin specs (e.g., `behavior/ose-be/gherkin/`)
- **`behavior/<product>-cli/gherkin/`**: Present for a CLI app still on this tree

## README Index Files

Every directory within a spec area must contain a `README.md` index file. README files serve as entry points when browsing on GitHub, providing context about what specifications exist at each level. This follows the same pattern used throughout the repository — see [File Naming Convention](../file-naming.md).

The order of folders in any README listing follows the canonical order: `product/`, `system-context/`, `containers/`, `components/`, `behavior/`.
