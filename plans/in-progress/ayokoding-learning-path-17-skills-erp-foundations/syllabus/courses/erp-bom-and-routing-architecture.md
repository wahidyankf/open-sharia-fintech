# ERP BOM and Routing Architecture (By Example)

**Course ID**: `erp-bom-and-routing-architecture` · **Format**: By Example.

**Scope note**: Models product structures and operation paths; it excludes planning and capacity optimization. License-aware.

## Why this exists · the big idea

- **The problem before the solution**: production facts cannot be explained without versioned structure and sequence.
- **Keep-this-if-you-forget-everything**: a manufactured result needs a traceable structure and route version.

## Prerequisites

- **Prior courses**: `erp-conceptual-data-model`.
- **Assumed knowledge**: items and quantities.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Original manufacturing data-model concepts.

## Concepts

- **co-01 · bill-of-materials** — versioned component structure for a finished item.
- **co-02 · component-quantity** — required measured input per structure.
- **co-03 · routing** — ordered operation path for a result.
- **co-04 · operation** — accountable transformation step.
- **co-05 · effective-version** — approved structure or route at a date.
- **co-06 · substitution** — governed alternative component.
- **co-07 · yield** — expected output relation to input.
- **co-08 · trace-link** — evidence connecting result to applied version.

## Worked examples

### Beginner

- **ex-01 · versioned-bom** — select a dated component structure — verify retired version is excluded. (co-01, co-05)

### Intermediate

- **ex-02 · route-sequence** — order operations into a route — verify each transition is explicit. (co-03, co-04)

### Advanced

- **ex-03 · approved-substitution** — apply a substitute component — verify authorization and trace remain. (co-06, co-08)

## In which paths

- `skills/conventional-erp` — Stage A · production architecture.
- `skills/sharia-erp` — Stage A · production architecture.
