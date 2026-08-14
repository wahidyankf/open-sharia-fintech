---
title: "App README vs Specs — Validation and Refinement Log"
description: The deterministic and LLM-semantic checks that enforce this convention, the forbidden-heading audit, and the history of refinements to the convention itself.
when_to_use: Use when checking how this convention is enforced, or reviewing the history of changes to its rules.
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

# Validation and Refinement Log

## Validation

`repo-rules-checker` and `specs-checker` enforce this convention. The `rhino-cli specs` subcommands handle deterministic checks; `specs-checker` handles semantic and narrative checks.

### Deterministic checks (rhino-cli)

| Check                                             | Command                                    | Finding level |
| ------------------------------------------------- | ------------------------------------------ | ------------- |
| README line-count cap exceeded                    | `rhino-cli specs validate-counts <folder>` | HIGH          |
| Spec tree top-level folder names wrong            | `rhino-cli specs validate-tree <app>`      | HIGH          |
| README count claims differ from actual file count | `rhino-cli specs validate-counts <folder>` | HIGH/MEDIUM   |
| BDD/DDD/Contracts adoption gap                    | `rhino-cli specs validate-adoption <app>`  | HIGH/MEDIUM   |

### LLM semantic checks (specs-checker)

| Check                                                                       | Finding level |
| --------------------------------------------------------------------------- | ------------- |
| Spec file missing required header block (audience + plain-language summary) | HIGH          |
| Section opens with mechanism rather than intent                             | MEDIUM        |
| Niche term used without gloss on first occurrence                           | MEDIUM        |
| Mainstream SWE term glossed unnecessarily                                   | LOW           |
| Code block missing one-sentence introduction                                | LOW           |

### Forbidden content audit (repo-rules-checker)

`repo-rules-checker` scans app READMEs for forbidden headings:

- `## Routes`, `## Screens`, `## API`, `## Endpoints` → HIGH (Category B content in README)
- `## Architecture` with more than 10 lines of content → HIGH (move to `components/*/architecture.md`)
- `## Bounded Context`, `## Design System` → HIGH

A README exceeding its line-count cap is a HIGH finding regardless of content.

## Refinement log

| Date       | Entry                                                                                                                                                                                                                                                                             |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-05-09 | CLI DDD adoption deferred; revisit if a CLI grows past ~10 commands or shows aggregate-shaped state.                                                                                                                                                                              |
| 2026-05-23 | CLI-flat exception retired. All CLI surfaces now use domain subdirs (same rule as BE and web). `ose-app` added to the `AppsWithDDD` allowlist.                                                                                                                                    |
| 2026-06-11 | Flat `<surface>` slugs renamed to `<product>-<surface>` compound form (e.g., `be/` → `organiclever-be/`, `cli/` → `rhino-cli/`). `build-tools` renamed to `ayokoding-build-tools` (kept active). `ose-app` + `ose-platform` merged into `ose` family; allowlist updated to `ose`. |
