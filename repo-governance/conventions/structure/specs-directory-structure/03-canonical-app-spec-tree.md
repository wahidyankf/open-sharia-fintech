---
title: "Canonical App Spec Tree"
description: The five-folder layout every app spec area uses, what each folder answers, and how the populated folder set varies by surface profile
when_to_use: Read this when scaffolding a new app's specs/apps/<app-family>/ tree or checking which folders a given surface profile should populate.
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

# Canonical App Spec Tree

## Five-Folder Layout

Every app spec area under `specs/apps/<app-family>/` uses the following five-folder layout. Apps create only the folders they need — do not pre-create empty folders.

```
specs/apps/<app-family>/
├── README.md
├── product/                        # PM-first content (not a C4 level)
│   ├── README.md
│   └── overview.md
├── system-context/                 # C4 L1
│   ├── README.md
│   └── context.md
├── containers/                     # C4 L2
│   ├── README.md
│   ├── container.md
│   ├── contracts/                  # OpenAPI specs (full-stack only)
│   │   ├── README.md
│   │   ├── openapi.yaml
│   │   ├── paths/
│   │   ├── schemas/
│   │   └── generated/
│   └── deployment.md
├── components/                     # C4 L3
│   ├── README.md
│   ├── be/                         # Full-stack only
│   │   ├── README.md
│   │   ├── component-be.md
│   │   └── api.md
│   └── web/                        # Web and full-stack
│       ├── README.md
│       ├── component-web.md
│       ├── architecture.md
│       ├── design-system.md
│       └── routes-and-screens.md
├── ddd/                            # App-level DDD (when adopted)
│   ├── README.md
│   ├── bounded-contexts.yaml
│   ├── bounded-context-map.md
│   └── ubiquitous-language/
│       ├── README.md
│       └── <bc>.md
└── behavior/                       # Cross-cutting Gherkin (all C4 levels)
    ├── README.md
    └── <product>-<surface>/         # e.g., organiclever-be, ayokoding-www, rhino-cli
        └── gherkin/
            ├── README.md
            └── <domain>/            # Domain subdir — required for all surfaces
                └── <feature>.feature
```

## Folder Purposes

| Folder            | Reader question it answers                            | Why top-level                                                    |
| ----------------- | ----------------------------------------------------- | ---------------------------------------------------------------- |
| `product/`        | "What does this product do for the user?"             | PM-first content — not architecture, not behavior                |
| `system-context/` | "What is the system boundary? Who interacts with it?" | C4 L1                                                            |
| `containers/`     | "What runtime processes exist?"                       | C4 L2 — hosts API contracts and deployment topology              |
| `components/`     | "What is inside each container?"                      | C4 L3 — bounded contexts are components                          |
| `behavior/`       | "Does the system do what the specs say?"              | Gherkin cuts across all C4 levels — orthogonal to zoom hierarchy |

## Per-Surface Variants

| Surface profile                   | Folders populated                                                                                                                                        | Folders absent or empty                         |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Full-stack (e.g., `organiclever`) | All five; `components/be/` + `components/web/` + `containers/contracts/`; `behavior/organiclever-be/gherkin/` + `behavior/organiclever-app-web/gherkin/` | None                                            |
| Web-only (e.g., `wahidyankf`)     | `product/`, `system-context/`, `containers/`, `components/web/`, `behavior/wahidyankf-www/gherkin/`                                                      | `containers/contracts/`, `components/be/`       |
| CLI-only (e.g., `rhino`)          | `product/`, `system-context/`, `containers/`, `components/cli/`, `behavior/rhino-cli/gherkin/`                                                           | `components/{be,web}/`, `containers/contracts/` |
| Multi-CLI (e.g., `ayokoding`)     | Same as CLI-only, plus web layers if applicable                                                                                                          | Nothing additional omitted                      |
