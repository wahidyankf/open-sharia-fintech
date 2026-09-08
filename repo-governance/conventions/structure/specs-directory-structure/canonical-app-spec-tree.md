---
description: The logical owner corpus every app spec area uses, what each entry answers, and how the populated set varies by surface profile
when_to_use: Read this when scaffolding a new app's specs/apps/<app-family>/ tree or checking which entries a given surface profile should populate.
---

# Canonical App Spec Tree

## Layout

A product directory holds one [logical owner corpus](./logical-owner-corpus.md) per surface it
deploys. The product root carries only its index and whatever product-level document the owners
share.

```
specs/apps/<product>/
├── README.md
├── overview.md                     # optional: PM-first product framing
├── <owner>/                        # one per deployed surface
│   ├── README.md
│   ├── architecture.md             # the current as-built system
│   ├── contracts/                  # optional: OpenAPI, in the owner that serves it
│   │   ├── README.md
│   │   ├── openapi.yaml
│   │   ├── paths/
│   │   ├── schemas/
│   │   └── generated/
│   └── behaviours/
│       ├── README.md
│       └── <domain>/               # domain subdir, required for every surface
│           └── <feature>.feature
```

An owner's `behaviours/` may nest one level further when a single deployed surface carries two
perspectives — `behaviours/frontend/` and `behaviours/backend/` for a site whose API runs inside the
same process. Two perspectives on one deployable are one owner, not two.

## Entry Purposes

| Entry             | Reader question it answers                              |
| ----------------- | ------------------------------------------------------- |
| `README.md`       | "What is here, and where do I go next?"                 |
| `architecture.md` | "What is the system as built, and what constrains it?"  |
| `behaviours/`     | "Does the system do what the specs say?"                |
| `contracts/`      | "What exactly does this surface promise over the wire?" |

`architecture.md` carries the C4 zoom levels as sections rather than folders: context, containers,
and components read top to bottom in one document, because a reader following a change needs all
three and a writer keeping one current has to keep all three current.

## Per-Surface Variants

| Surface profile | Owners                                           | `contracts/`                  |
| --------------- | ------------------------------------------------ | ----------------------------- |
| Full-stack      | one per client, one per service                  | in the service that serves it |
| Web-only        | one per deployed site                            | absent                        |
| CLI-only        | one per binary                                   | absent                        |
| Library         | none — the three entries sit at the library root | absent                        |
