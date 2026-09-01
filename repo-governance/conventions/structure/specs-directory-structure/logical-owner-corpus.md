---
title: "Logical Owner Corpus"
description: "The adopted specs shape — one corpus per logical owner, carrying an index, a canonical as-built architecture.md, and a recursive behaviors/ tree"
when_to_use: "Read this when creating or validating a specs corpus for a logical owner, or when deciding which shape a product directory is measured against."
category: explanation
subcategory: conventions
tags:
  - conventions
  - specs
  - gherkin
  - directory-structure
  - c4
created: 2026-09-01
---

# Logical Owner Corpus

## Adopted Shape

A specification corpus belongs to a **logical owner** — one shippable surface — not to a product
family. Each owner carries exactly three required entries:

```text
specs/apps/<product>/<owner>/
├── README.md          # index for the corpus
├── architecture.md    # canonical, current, as-built C4
└── behaviors/
    ├── README.md
    ├── <domain>/      # optional grouping
    └── *.feature
```

Libraries use the same three entries directly under `specs/libs/<library>/`.

`architecture.md` describes only the current as-built system and is updated in the same delivery
unit as the change that alters it. `behaviors/` is recursive: a feature file may sit at its root or
inside a domain directory, so the flat-feature rule that governs the legacy tree does not apply.

## Which Shape a Product Is Measured Against

Adoption is detected positively. A product directory has adopted this shape as soon as one of its
immediate subdirectories carries an `architecture.md`. From that moment `rhino-cli specs structure
validate` measures the whole product against this convention, and any surviving `product/`,
`system-context/`, `containers/`, `components/`, or `behavior/` folder beside a corpus is a
finding rather than a tolerated leftover.

A product that has not begun the move is still measured against the
[Canonical App Spec Tree](./canonical-app-spec-tree.md). The two shapes never both bind a single
product, so a migration is complete per product rather than per file.

## Why Owner Rather Than Product

A product family often ships several independent surfaces — a site, its backend, and a build tool.
Grouping their specifications under one product tree forces unrelated readers through the same
index and makes a single `architecture.md` describe systems that deploy separately. One corpus per
logical owner keeps each reader's entry point, C4 view, and behavior corpus together, and lets a
dedicated E2E project link to its owner's corpus instead of growing a parallel tree.

## Enforcement

**Enforcement disposition — enforced.** `rhino-cli specs structure validate` reports a missing
`README.md`, `architecture.md`, or `behaviors/` entry, an empty `behaviors/` tree, a missing
`behaviors/README.md`, and any surviving legacy folder beside a corpus. The command runs in
`rhino-cli:test:specs`, which `test:quick` and the pre-push gate both include.

## Related

- [Canonical App Spec Tree](./canonical-app-spec-tree.md) — the legacy five-folder layout this
  shape replaces.
- [Gherkin Feature File Placement and Lib Spec Structure](./gherkin-feature-file-placement-and-lib-spec-structure.md) —
  placement rules for the legacy tree.
