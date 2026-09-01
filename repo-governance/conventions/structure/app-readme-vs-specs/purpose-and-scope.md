---
title: "App README vs Specs — Purpose and Scope"
description: The three decisions this convention governs, its rollout status, and exactly what it covers vs. what other conventions cover.
when_to_use: Use when checking whether a topic falls inside this convention's scope, or which conventions govern related concerns.
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

# Purpose and Scope

## Purpose

This convention governs THREE interrelated decisions:

1. **Content Split Rule** — which content belongs in an app/infra README (Category A) vs in `specs/apps/<app-family>/` (Category B).
2. **Spec Tree Shape** — what the canonical five-folder C4-aware tree looks like and how it varies by surface profile.
3. **PM-Readability Contract** — six rules every file under `specs/apps/` must satisfy so a SWE-background Technical Product/Project Manager can form a working mental model on first read.

A fourth rule covers adoption expectations for BDD and API contracts.

The convention applies to all apps and infra directories in the monorepo. Its OrganicLever application is the reference pilot. Rollout to `ayokoding`, `ose`, `wahidyankf`, and `rhino` follows the same rules.

## Scope

### What This Convention Covers

- Content placement decisions for app and infra `README.md` files
- The canonical five-folder spec tree (`product/`, `system-context/`, `containers/`, `components/`, `behavior/`) and per-surface variants
- PM-readability requirements for every file under `specs/apps/`
- BDD and API contract adoption expectations by app type
- Cross-link requirements between app READMEs and their corresponding `specs/` trees
- Line-count caps for app and infra READMEs
- Migration path from flat-root spec trees to the C4-aware layout

### What This Convention Does NOT Cover

- Gherkin writing standards — see [Acceptance Criteria Convention](../../../development/infra/acceptance-criteria.md)
- C4 diagram content and internal structure — see the C4 files within each app's spec tree
- OpenAPI authoring standards — see contract project documentation
- README writing quality (voice, scannability, engagement) — see [README Quality Convention](../../writing/readme-quality.md)
- The canonical path pattern for Gherkin feature files within `behavior/` — see [Specs Directory Structure Convention](../specs-directory-structure.md)
