---
title: "Standard 4 — Spec Tree Shape: Canonical Layout and Folder Purposes"
description: The canonical logical-owner-corpus spec tree layout and why each entry sits where it does.
when_to_use: Use when creating a new app's spec tree or checking whether an existing tree matches the canonical corpus shape.
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

# Standard 4 — Spec Tree Shape: Canonical Layout and Folder Purposes

New apps create a spec tree at `specs/apps/<app-family>/` holding one
[logical owner corpus](../specs-directory-structure/logical-owner-corpus.md) per deployed surface.
A tree still in the retired five-folder shape migrates per Standard 4.5.

## Canonical layout

```
specs/apps/<product>/
├── README.md
├── overview.md             # optional: PM-first product framing
└── <owner>/                # one per deployed surface
    ├── README.md
    ├── architecture.md     # the current as-built system
    ├── contracts/          # optional: OpenAPI, in the owner that serves it
    │   ├── README.md
    │   ├── openapi.yaml
    │   ├── paths/
    │   ├── schemas/
    │   └── generated/
    └── behaviours/
        ├── README.md
        └── <domain>/
            └── <feature>.feature
```

## Why each entry sits where it does

**`architecture.md` is one document, not four folders.** Context, containers, and components are
zoom levels on the same system. A reader following a change needs all three, and a writer keeping
one current has to keep all three current; splitting them across `system-context/`, `containers/`,
and `components/` made four places to forget rather than four places to look.

**`behaviours/` is recursive and sits inside the owner.** Scenarios belong to the thing that must
satisfy them. A cross-cutting `behaviour/` tree at the product root made every surface's scenarios
a sibling of every other's, which is exactly the relationship they do not have.

**`contracts/` sits inside the owner that serves it.** A contract in a shared folder has no owner;
a contract inside the backend has one.

**The product root carries only what the owners share.** An `overview.md` describing the product
belongs there. Anything describing one surface belongs to that surface.
