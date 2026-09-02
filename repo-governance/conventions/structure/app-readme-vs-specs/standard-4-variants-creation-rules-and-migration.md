---
title: "Standard 4 — Spec Tree Shape: Per-Surface Variants, Creation Rules, and Migration"
description: How the canonical spec tree varies by surface profile (full-stack/web-only/CLI/multi-CLI), the rules for creating new folders, and the flat-root-to-C4-aware migration path.
when_to_use: Use when determining which spec-tree folders a given app profile needs, or migrating an existing flat-root spec tree to the C4-aware layout.
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

# Standard 4 — Spec Tree Shape: Per-Surface Variants, Creation Rules, and Migration

## Per-surface variant table

| Surface profile                 | Folders populated                                                                                                                                                    | Folders absent or empty                                 |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Full-stack (no current example) | All five top-level folders; `components/be/` + `components/web/` + `containers/contracts/`; `behavior/<product>-be/gherkin/` + `behavior/<product>-app-web/gherkin/` | None — full tree                                        |
| Web-only (no current example)   | `product/`, `system-context/`, `containers/`, `components/web/`, `behavior/<app>-www/gherkin/`                                                                       | `containers/contracts/` (no API), `components/be/`      |
| CLI-only (no current example)   | `product/`, `system-context/`, `containers/`, `components/cli/`, `behavior/<product>-cli/gherkin/`                                                                   | `components/{be,web}/`, `containers/contracts/`         |
| Multi-CLI (no current example)  | Same as CLI-only, with multiple `components/cli/<binary>/` + `behavior/<product>-cli/gherkin/` pairs alongside web layers if applicable                              | Nothing additional omitted — same shape, more populated |

## Creation rules

- New apps create only the folders they need. Do not pre-create empty `behavior/` if there are no Gherkin specs yet.
- Once a folder exists, it carries a `README.md` index pointing at its children.
- The order of folders in any README listing follows the canonical order: `product/`, `system-context/`, `containers/`, `components/`, `behavior/`.

## Standard 4.5 — Migration path (flat-root to C4-aware)

For existing spec trees with a flat-root layout (`be/`, `web/`, `cli/`, `c4/`, `contracts/`):

1. Create the five top-level folders with placeholder `README.md` files (no content moves yet).
2. In one atomic commit: `git mv` all old subfolders to their new positions per the canonical layout. Update ALL path references in the same commit (rhino-cli path constants, Nx cache inputs, step definition files, governance cross-links).
3. Update `specs/apps/<app-family>/README.md` to reflect the new tree.
4. Verify with `rhino-cli specs validate-tree <app>` and `npm run lint:md`.

The commit that moves files and updates paths MUST be atomic — splitting them causes test failures between commits.
