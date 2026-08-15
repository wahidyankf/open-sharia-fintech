# ERP Numbering Sequences and UoM Conversion (Annotated-Concept)

**Course ID**: `erp-numbering-sequences-and-uom-conversion` · **Format**: Annotated-Concept.

**Scope note**: Controls identifiers and quantity conversions; it excludes inventory valuation. License-aware.

## Why this exists · the big idea

- **The problem before the solution**: duplicate identifiers and silent quantity conversion corrupt downstream records.
- **Keep-this-if-you-forget-everything**: identifiers and quantities carry rules, not formatting.

## Prerequisites

- **Prior courses**: `erp-module-map-and-architecture`.
- **Assumed knowledge**: units and ratios.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Original vendor-neutral control concepts.

## Concepts

- **co-01 · sequence-scope** — boundary within which an identifier is unique.
- **co-02 · allocation** — controlled reservation of a new identifier.
- **co-03 · immutability** — issued identifier remains traceable.
- **co-04 · unit-of-measure** — named measurement basis for a quantity.
- **co-05 · conversion-factor** — governed ratio between units.
- **co-06 · rounding-policy** — explicit treatment of non-exact conversion.
- **co-07 · base-unit** — canonical unit for a stored quantity.
- **co-08 · conversion-audit** — retained inputs and rule for a converted value.

## In which paths

- `skills/conventional-erp` — Stage A · master-data control.
- `skills/sharia-erp` — Stage A · master-data control.
