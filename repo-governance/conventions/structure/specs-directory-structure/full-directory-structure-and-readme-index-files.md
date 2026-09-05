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
│   └── <product>/
│       ├── README.md
│       ├── overview.md       # optional: framing shared by several owners
│       └── <owner>/          # one logical owner corpus per deployed surface
│           ├── README.md
│           ├── architecture.md
│           ├── contracts/    # optional: in the owner that serves the contract
│           └── behaviours/
│               └── <domain>/
│                   └── <feature>.feature
└── libs/
    └── <lib-name>/
        ├── README.md
        ├── architecture.md
        └── behaviours/
            └── <domain>/
                └── <feature>.feature
```

### Which Entries Each Project Populates

`README.md`, `architecture.md`, and a non-empty `behaviours/` are required of every corpus. What
varies is how many corpora a product holds and whether the optional entries appear:

- **`<owner>/contracts/`**: Present for a surface that publishes an OpenAPI contract, inside the
  owner that serves it
- **`<product>/overview.md`**: Present when several owners share product-level framing
- **A second owner**: Present for every additional surface the product deploys — a backend beside a
  web client, a build tool beside a site

## README Index Files

Every directory within a spec area must contain a `README.md` index file. README files serve as entry points when browsing on GitHub, providing context about what specifications exist at each level. This follows the same pattern used throughout the repository — see [File Naming Convention](../file-naming.md).

The order of entries in any corpus README listing follows the canonical order: `architecture.md`, `contracts/`, `behaviours/`.
