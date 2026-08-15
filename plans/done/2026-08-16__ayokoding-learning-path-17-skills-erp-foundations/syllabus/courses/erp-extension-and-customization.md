# ERP Extension and Customization (By Example)

**Course ID**: `erp-extension-and-customization` · **Format**: By Example.

**Scope note**: Evaluates configuration, extension, and customization boundaries; it excludes SQL implementation detail. License-aware.

## Why this exists · the big idea

- **The problem before the solution**: local changes become upgrade and control debt when their boundary is unclear.
- **Keep-this-if-you-forget-everything**: prefer explicit extension contracts over mutation of core behaviour.

## Prerequisites

- **Prior courses**: `erp-module-map-and-architecture`, `sql-essentials`.
- **Assumed knowledge**: API and data ownership basics.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Original architecture trade-off framing.

## Concepts

- **co-01 · configuration** — supported parameterized variation.
- **co-02 · extension-point** — declared seam for additional behaviour.
- **co-03 · customization** — local change to core behaviour requiring ownership.
- **co-04 · upgrade-risk** — likelihood a change blocks future evolution.
- **co-05 · data-ownership** — accountable authority over a stored fact.
- **co-06 · compatibility-contract** — behaviour preserved across versions.
- **co-07 · migration-path** — controlled transition for changed data.
- **co-08 · decision-record** — durable rationale for selected approach.

## Worked examples

### Beginner

- **ex-01 · configuration-first** — meet a local need with a parameter — verify no core mutation. (co-01)

### Intermediate

- **ex-02 · extension-contract** — add derived behaviour at a declared seam — verify ownership remains explicit. (co-02, co-05)

### Advanced

- **ex-03 · customization-review** — record upgrade and migration risk — verify a decision owner exists. (co-03, co-04, co-08)

## In which paths

- `skills/conventional-erp` — Stage A · evolution boundary.
- `skills/sharia-erp` — Stage A · evolution boundary.
