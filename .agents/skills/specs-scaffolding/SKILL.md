---
name: specs-scaffolding
description: Mechanics for specs-maker — the four surface-profile directory trees, README/feature-file/C4-diagram content generation, and the PM-readability/placement/structure conventions every scaffolded file follows.
when_to_use: When implementing or maintaining specs-maker, or any agent that scaffolds new spec areas under specs/.
---

# Scaffolding New Spec Areas

## Overview

`specs-maker` creates new spec areas, missing READMEs, and Gherkin feature structure at
explicitly specified paths under `specs/` — never deciding what should exist, only building what
the caller names, following the logical owner corpus shape.

## Reference Modules

- [surface-profile-trees.md](reference/surface-profile-trees.md) — the four surface-profile
  directory trees (full-stack, web-only, cli-only, multi-cli) and when each folder is created
- [content-generation.md](reference/content-generation.md) — README inference, Gherkin
  feature file generation, C4 Mermaid diagram generation
- [conventions.md](reference/conventions.md) — the PM-readability contract, feature file
  placement rules, README structure, background steps by surface, folder listing order

## Core Principles

- **Explicit target only.** Creates content only at the caller-specified path(s) — never decides
  which spec areas should exist, never creates content elsewhere.
- **Only scaffold what the surface profile needs.** Empty folders are never pre-created; a
  cli-only app gets no `components/web/`.
- **Follow established patterns, no novel structures.** Every generated file matches the
  conventions in reference module 03.

## Related Agents

`specs-checker` (validates existing specs — different lifecycle stage), `specs-fixer` (fixes
existing specs — different lifecycle stage).
