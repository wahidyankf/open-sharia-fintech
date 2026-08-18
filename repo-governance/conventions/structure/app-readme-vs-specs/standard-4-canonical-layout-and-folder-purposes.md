---
title: "Standard 4 — Spec Tree Shape: Canonical Layout and Folder Purposes"
description: The canonical five-folder C4-aware spec tree layout and why each top-level folder is not nested under another.
when_to_use: Use when creating a new app's spec tree or checking whether an existing tree matches the canonical five-folder shape.
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

New apps create a spec tree at `specs/apps/<app-family>/` following the canonical five-folder layout. Existing apps with flat-root trees (`be/`, `web/`, `cli/`, `c4/`, `contracts/` at the root) migrate to this layout per Standard 4.5.

## Canonical layout

```
specs/apps/<app-family>/
├── README.md
├── product/
│   ├── README.md
│   └── overview.md
├── system-context/
│   ├── README.md
│   └── context.md
├── containers/
│   ├── README.md
│   ├── container.md
│   ├── contracts/          # OpenAPI specs (full-stack only)
│   │   ├── README.md
│   │   ├── openapi.yaml
│   │   ├── paths/
│   │   ├── schemas/
│   │   └── generated/
│   └── deployment.md
├── components/
│   ├── README.md
│   ├── be/                 # Full-stack only
│   │   ├── README.md
│   │   ├── component-be.md
│   │   └── api.md
│   └── web/                # Web and full-stack
│       ├── README.md
│       ├── component-web.md
│       ├── architecture.md
│       ├── design-system.md
│       └── routes-and-screens.md
├── ddd/                    # When DDD adopted (app root, not under components/)
│   ├── README.md
│   ├── bounded-contexts.yaml
│   ├── bounded-context-map.md
│   └── ubiquitous-language/
│       ├── README.md
│       └── <bc>.md
└── behavior/
    ├── README.md
    ├── be/
    │   └── gherkin/        # Full-stack only
    │       ├── README.md
    │       └── <domain>/
    ├── web/
    │   └── gherkin/
    │       ├── README.md
    │       └── <domain>/
    └── cli/
        └── gherkin/        # CLI-only and multi-CLI
            ├── README.md
            └── <domain>/   # Domain subdir — same rule as be/web
```

## Folder purposes

| Folder            | Reader question it answers                                         | Why top-level (not nested)                                                                                                           |
| ----------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| `product/`        | "What does this product do for the user? What is in this version?" | PM-first content. Not architecture (so not under `system-context/`). Not behavior (so not under `behavior/`). Deserves its own home. |
| `system-context/` | "What is the system boundary? Who/what interacts with it?"         | C4 L1 — the canonical system context level.                                                                                          |
| `containers/`     | "What runtime processes exist? What are their boundaries?"         | C4 L2 — naturally hosts API contracts and deployment topology.                                                                       |
| `components/`     | "What is inside each container?"                                   | C4 L3. Internal component breakdown per surface (be/, web/). DDD lives at app root (not nested here) to stay surface-agnostic.       |
| `behavior/`       | "Does the system actually do what the specs say?"                  | Gherkin tests behavior at every C4 level — orthogonal to zoom hierarchy. Forcing it under one C4 level would misrepresent its scope. |
