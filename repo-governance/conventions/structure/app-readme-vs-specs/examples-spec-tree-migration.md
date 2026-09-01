---
title: "App README vs Specs — Example: Spec Tree Migration"
description: A worked before/after example and checklist for migrating a flat-root spec tree to the canonical C4-aware five-folder layout.
when_to_use: Use when you need a concrete worked example of migrating an existing flat-root spec tree to the C4-aware layout.
category: explanation
subcategory: conventions
status: "Pilot — initial issue"
tags:
  - conventions
  - readme
  - specs
  - spec-tree-shape
  - pm-readability
  - c4
created: 2026-05-09
---

# Example: Spec Tree Migration (Flat-Root to C4-Aware)

**Before** (flat-root layout):

```
specs/apps/organiclever/
├── be/
│   └── gherkin/
├── web/
│   └── gherkin/
├── c4/
└── contracts/
```

**After** (C4-aware five-folder layout):

```
specs/apps/organiclever/
├── product/
├── system-context/
├── containers/
│   └── contracts/
├── components/
│   ├── be/
│   └── web/
└── behavior/
    ├── be/
    │   └── gherkin/
    │       └── <domain>/
    └── web/
        └── gherkin/
            └── <domain>/
```

**Migration checklist**:

1. Create five top-level folders with `README.md` placeholders.
2. In one atomic `git mv` commit: move `be/gherkin/` → `behavior/<product>-be/gherkin/`,
   `web/gherkin/` → `behavior/<product>-web/gherkin/`,
   `cli/gherkin/` → `behavior/<product>-cli/gherkin/`, `c4/*.md` files → their new positions,
   `contracts/` → `containers/contracts/`.
   Feature files must be nested under a domain subdir — e.g.,
   `behavior/<product>-cli/gherkin/<domain>/<feature>.feature`.
3. In the same commit: update rhino-cli path constants, Nx `project.json` `inputs`, step file references, and governance cross-links.
4. Run `rhino-cli specs validate-tree <app>` to verify.
