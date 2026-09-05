---
title: "Specs Directory Structure: Scope"
description: What the specs/ directory structure convention covers versus what it explicitly delegates to sibling conventions
when_to_use: Read this when you need to confirm whether a specs/ topic (Gherkin writing, C4 content, PM-readability) falls inside or outside this convention.
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

# Scope

## What This Convention Covers

- The logical owner corpus for app spec areas and library spec areas
- **Gherkin feature file placement** for apps (BE, FE/web, CLI) and libs, within an owner's
  `behaviours/` tree
- **Domain subdirectory rules** for grouping related feature files
- **C4 placement** as sections of an owner's `architecture.md` rather than as folders
- **OpenAPI contract placement** within the owner that serves the contract
- **README.md index files** at each navigational level
- **Per-surface variants** (full-stack, web-only, CLI-only, library)
- **Migration path** from the retired five-folder tree to the logical owner corpus

## What This Convention Does NOT Cover

- **Gherkin writing standards** (covered by [Acceptance Criteria Convention](../../../development/infra/acceptance-criteria.md))
- **C4 diagram content** (covered by C4 model documentation within each project)
- **OpenAPI spec authoring** (covered by contract project documentation)
- **Test implementation** (covered by [Behaviour-Driven Development](../../../development/behaviour-driven-development.md))
- **Content split decisions** (what belongs in app README vs specs/) — see [App README vs Specs Convention](../app-readme-vs-specs.md)
- **PM-readability requirements** for spec files — see [App README vs Specs Convention](../app-readme-vs-specs.md)
